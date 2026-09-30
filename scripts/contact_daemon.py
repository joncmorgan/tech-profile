#!/usr/bin/env python3
"""
Plaud Diary Contact Tracker Daemon
Fetches diary transcripts from email, parses with Claude, updates contact list
"""

import json
import logging
import os
import re
import uuid
from datetime import datetime
from email import message_from_bytes, policy
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from anthropic import Anthropic
import imapclient

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("contact_daemon")

app = Flask(__name__)

# Configuration
VAULT_PATH = Path("/data/src/sites/tech-profile/vault")
CONTACTS_FILE = VAULT_PATH / "plaud-contacts.json"
INTERESTS_FILE = VAULT_PATH / "plaud-interests.json"
DIARY_ENTRIES_FILE = VAULT_PATH / "plaud-diary-entries.json"
CORRECTIONS_FILE = VAULT_PATH / "plaud-corrections.json"
EXTRACTIONS_FILE = VAULT_PATH / "plaud-extractions.json"
OBSIDIAN_CONTACTS_DIR = VAULT_PATH / "Channels" / "Contacts"
OBSIDIAN_COMPANIES_DIR = VAULT_PATH / "Channels" / "Companies"
SMTP_EMAIL = os.getenv("FASTMAIL_EMAIL")
SMTP_PASSWORD = os.getenv("FASTMAIL_PASSWORD")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
PLAUD_FOLDER = os.getenv("PLAUD_FOLDER", "INBOX")

# Initialize clients
anthropic_client = Anthropic(api_key=ANTHROPIC_API_KEY)

# Track processed email UIDs to avoid reprocessing
PROCESSED_FILE = VAULT_PATH / ".plaud-processed-uids"


def load_processed_uids():
    """Load set of already-processed email UIDs"""
    if PROCESSED_FILE.exists():
        with open(PROCESSED_FILE) as f:
            return set(json.load(f))
    return set()


def save_processed_uids(uids):
    """Save processed UIDs"""
    PROCESSED_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(PROCESSED_FILE, "w") as f:
        json.dump(list(uids), f)


def load_contacts():
    """Load current contacts from JSON file"""
    if CONTACTS_FILE.exists():
        with open(CONTACTS_FILE) as f:
            return json.load(f)
    return {"contacts": [], "last_updated": None}


def save_contacts(data):
    """Save contacts to JSON file"""
    VAULT_PATH.mkdir(parents=True, exist_ok=True)
    data["last_updated"] = datetime.now().isoformat()
    with open(CONTACTS_FILE, "w") as f:
        json.dump(data, f, indent=2)


def load_interests():
    """Load companies/events of interest from JSON file"""
    if INTERESTS_FILE.exists():
        with open(INTERESTS_FILE) as f:
            return json.load(f)
    return {"companies": [], "events": [], "last_updated": None}


def save_interests(data):
    """Save companies/events of interest to JSON file"""
    VAULT_PATH.mkdir(parents=True, exist_ok=True)
    data["last_updated"] = datetime.now().isoformat()
    with open(INTERESTS_FILE, "w") as f:
        json.dump(data, f, indent=2)


def load_corrections():
    """Load manual name corrections: correct name -> list of wrong variants seen for it, per item type.

    Auto-migrates the old flat "wrong -> correct" format in place if found, so
    corrections made before this format change aren't lost.
    """
    if not CORRECTIONS_FILE.exists():
        return {"contacts": {}, "companies": {}, "events": {}}

    with open(CORRECTIONS_FILE) as f:
        data = json.load(f)

    migrated = {}
    for item_type in ("contacts", "companies", "events"):
        table = data.get(item_type, {})
        if table and isinstance(next(iter(table.values())), str):
            # Old format: wrong_name -> correct_name. Invert to correct_name -> [wrong_name, ...]
            inverted = {}
            for wrong_name, correct_name in table.items():
                inverted.setdefault(correct_name, []).append(wrong_name)
            migrated[item_type] = inverted
        else:
            migrated[item_type] = table
    return migrated


def save_corrections(data):
    """Save manual name corrections"""
    VAULT_PATH.mkdir(parents=True, exist_ok=True)
    with open(CORRECTIONS_FILE, "w") as f:
        json.dump(data, f, indent=2)


def load_extractions():
    """Load cached per-diary-entry Claude extractions, keyed by diary entry id"""
    if EXTRACTIONS_FILE.exists():
        with open(EXTRACTIONS_FILE) as f:
            return json.load(f)
    return {}


def save_extractions(data):
    """Save cached per-diary-entry Claude extractions"""
    VAULT_PATH.mkdir(parents=True, exist_ok=True)
    with open(EXTRACTIONS_FILE, "w") as f:
        json.dump(data, f, indent=2)


def apply_corrections(items, corrections_for_type):
    """Rename any item whose name matches a known wrong variant (case-insensitive)"""
    alias_lookup = {
        wrong_name.lower(): correct_name
        for correct_name, wrong_names in corrections_for_type.items()
        for wrong_name in wrong_names
    }
    for item in items:
        corrected = alias_lookup.get(item["name"].lower())
        if corrected:
            item["name"] = corrected


def load_diary_entries():
    """Load diary entries from intermediate store"""
    if DIARY_ENTRIES_FILE.exists():
        with open(DIARY_ENTRIES_FILE) as f:
            return json.load(f)
    return {"entries": []}


def save_diary_entries(data):
    """Save diary entries to intermediate store"""
    VAULT_PATH.mkdir(parents=True, exist_ok=True)
    with open(DIARY_ENTRIES_FILE, "w") as f:
        json.dump(data, f, indent=2)


def add_diary_entry(text, source="email", noted_at=None):
    """Add new diary entry to store.

    `noted_at` is when the note itself was recorded (e.g. the email's Date
    header), as opposed to `timestamp`, which is when the daemon processed
    it - they can differ if a run picks up an older email.
    """
    entries = load_diary_entries()
    now = datetime.now()
    entry = {
        "id": uuid.uuid4().hex,
        "timestamp": now.isoformat(),
        "noted_at": (noted_at or now).isoformat(),
        "source": source,
        "text": text,
    }
    entries["entries"].append(entry)
    save_diary_entries(entries)
    return entry


def fetch_diary_emails():
    """Fetch new diary emails from Fastmail.

    Raises on IMAP connection/auth failures instead of swallowing them -
    callers need to know when a fetch didn't actually happen.
    """
    processed = load_processed_uids()
    server = imapclient.IMAPClient("imap.fastmail.com", ssl=True)
    try:
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        server.select_folder(PLAUD_FOLDER)

        # Search for emails with "[Plaud-AutoFlow]" in subject
        messages = server.search(["SUBJECT", "[Plaud-AutoFlow]"])
        new_uids = [uid for uid in messages if uid not in processed]
        logger.info("IMAP search found %d matching email(s), %d new", len(messages), len(new_uids))

        new_messages = []
        if new_uids:
            data = server.fetch(new_uids, ["RFC822"])
            new_messages = [(uid, data[uid][b"RFC822"]) for uid in new_uids if uid in data]

        return new_messages, processed
    finally:
        try:
            server.logout()
        except Exception:
            logger.warning("IMAP logout failed", exc_info=True)


def extract_email_body(raw_email_bytes):
    """Parse a raw RFC822 email and return (body_text, email_date).

    Handles multipart/MIME and quoted-printable encoding properly instead of
    naively splitting on the header/body blank line, which breaks for
    anything but a bare single-part plaintext email.
    """
    msg = message_from_bytes(raw_email_bytes, policy=policy.default)

    body_part = msg.get_body(preferencelist=("plain", "html"))
    body_text = body_part.get_content() if body_part is not None else ""

    email_date = msg.get("Date")
    if email_date is not None:
        email_date = email_date.datetime

    return body_text, email_date


def parse_transcript_with_claude(transcript_text, reference_date=None):
    """Send transcript to Claude, extract contacts, companies, and events of interest.

    Name correctness (mis-transcribed names) is handled downstream by the
    deterministic alias table in apply_corrections(), not here - this keeps
    the prompt simple and this call cheap and cacheable per diary entry.
    """
    reference_date = reference_date or datetime.now()
    reference_str = reference_date.strftime("%A, %Y-%m-%d")
    empty_result = {"contacts": [], "companies": [], "events": []}

    prompt = f"""Extract three things from this diary note: people to follow up with, companies of interest, and events of interest.

This diary note was recorded on {reference_str}. Resolve any relative date expressions ("Monday", "next week", "tomorrow") to an absolute date in YYYY-MM-DD format using that as the reference date. If no date is mentioned or it truly cannot be resolved, use "TBD".

Only include a company or event if it's explicitly of interest (a lead, a target, something to attend) - not every company or event mentioned in passing.

Format:
{{
  "contacts": [{{"name": "string", "action": "string", "date": "YYYY-MM-DD or 'TBD'"}}],
  "companies": [{{"name": "string", "note": "why it's of interest"}}],
  "events": [{{"name": "string", "note": "why it's of interest", "date": "YYYY-MM-DD or 'TBD'"}}]
}}

Examples (assuming the note was recorded on Wednesday, 2026-09-24):
- "Call Pete Buffett Monday" → contacts: [{{"name": "Pete Buffett", "action": "call", "date": "2026-09-28"}}]
- "Organica might have short-term work for me" → companies: [{{"name": "Organica", "note": "potential short-term work"}}]
- "The ESD conference is on the 12th, I should go" → events: [{{"name": "ESD conference", "note": "should attend", "date": "2026-10-12"}}]

Diary note:
{transcript_text}

Return ONLY valid JSON, no other text."""

    message = anthropic_client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )

    try:
        response_text = message.content[0].text.strip()
        # Try to extract JSON if wrapped in markdown code blocks
        if "```" in response_text:
            response_text = response_text.split("```")[1].replace("json", "").strip()
        result = json.loads(response_text)
        return {
            "contacts": result.get("contacts", []),
            "companies": result.get("companies", []),
            "events": result.get("events", []),
        }
    except (json.JSONDecodeError, IndexError, AttributeError) as e:
        logger.warning("Failed to parse Claude response as JSON: %s", e)
        return empty_result


def _build_touchpoint(item, fields):
    """Build a touchpoint record from an extracted item, keeping only `fields` plus provenance"""
    touchpoint = {field: item.get(field, "") for field in fields}
    touchpoint["diary_entry_id"] = item.get("diary_entry_id")
    touchpoint["noted_at"] = item.get("noted_at")
    return touchpoint


def _merge_named_touchpoints(existing_items, new_items, fields):
    """Merge new items into per-name touchpoint history, keyed by name (case-insensitive).

    A later mention of the same name never overwrites an earlier one - it's
    appended, so the full history of mentions stays visible (e.g. "call
    Monday" followed later by "spoke, follow up next week").
    """
    by_name = {}
    for item in existing_items:
        key = item["name"].lower()
        if "touchpoints" in item:
            by_name[key] = {"name": item["name"], "touchpoints": list(item["touchpoints"])}
        else:
            # Legacy record from before touchpoint history existed - keep it
            # as the first entry in its history rather than losing it.
            by_name[key] = {"name": item["name"], "touchpoints": [_build_touchpoint(item, fields)]}

    for item in new_items:
        key = item["name"].lower()
        record = by_name.setdefault(key, {"name": item["name"], "touchpoints": []})
        record["touchpoints"].append(_build_touchpoint(item, fields))

    for record in by_name.values():
        record["touchpoints"].sort(key=lambda t: t.get("noted_at") or "")

    return list(by_name.values())


def merge_contacts(existing_data, new_contacts):
    """Merge new touchpoints into each contact's history (see _merge_named_touchpoints)"""
    contacts = _merge_named_touchpoints(existing_data.get("contacts", []), new_contacts, fields=["action", "date"])
    contacts.sort(key=lambda c: (c["touchpoints"][-1].get("date") or "ZZZZ", c["name"]))
    return {"contacts": contacts, "last_updated": datetime.now().isoformat()}


def merge_interests(existing_data, new_companies, new_events):
    """Merge new company/event mentions into their touchpoint histories"""
    companies = _merge_named_touchpoints(existing_data.get("companies", []), new_companies, fields=["note"])
    events = _merge_named_touchpoints(existing_data.get("events", []), new_events, fields=["note", "date"])
    companies.sort(key=lambda c: c["name"])
    events.sort(key=lambda e: (e["touchpoints"][-1].get("date") or "ZZZZ", e["name"]))
    return {"companies": companies, "events": events, "last_updated": datetime.now().isoformat()}


def extract_new_diary_entries():
    """Run Claude extraction only on diary entries not already in the extraction cache.

    This is the only function that calls Claude. Results are cached forever per
    diary entry id, so re-running this later costs nothing for entries already
    extracted - only genuinely new diary notes get sent to the model.
    """
    diary = load_diary_entries()
    extractions = load_extractions()

    new_entries = [e for e in diary["entries"] if e["id"] not in extractions]
    logger.info("Extraction cache: %d entrie(s) cached, %d new", len(extractions), len(new_entries))

    for entry in new_entries:
        noted_at = entry.get("noted_at")
        reference_date = datetime.fromisoformat(noted_at) if noted_at else None
        logger.info("Extracting diary entry %s with Claude", entry["id"])
        extracted = parse_transcript_with_claude(entry["text"], reference_date=reference_date)
        extractions[entry["id"]] = {**extracted, "noted_at": noted_at, "extracted_at": datetime.now().isoformat()}

    if new_entries:
        save_extractions(extractions)

    return len(new_entries)


def apply_substitutions_and_merge():
    """Deterministic pass: read cached extractions, apply name corrections, and
    rebuild contacts.json / plaud-interests.json from scratch.

    No LLM calls happen here - cheap enough to re-run any time (e.g. right
    after adding a new correction) so a fix reflects across all history
    instantly, and always starts from empty lists so touchpoints never pile up.
    """
    extractions = load_extractions()
    corrections = load_corrections()
    all_contacts, all_companies, all_events = [], [], []

    diary_entry_count = len(load_diary_entries()["entries"])
    if not extractions and diary_entry_count > 0:
        logger.warning(
            "Extraction cache is empty but %d diary entrie(s) exist - merging now would wipe "
            "contacts.json/plaud-interests.json. Call extract_new_diary_entries() first.",
            diary_entry_count,
        )

    for entry_id, extracted in extractions.items():
        noted_at = extracted.get("noted_at")
        for item_type, target in (
            ("contacts", all_contacts),
            ("companies", all_companies),
            ("events", all_events),
        ):
            items = [dict(item) for item in extracted.get(item_type, [])]
            apply_corrections(items, corrections.get(item_type, {}))
            for item in items:
                item["diary_entry_id"] = entry_id
                item["noted_at"] = noted_at
            target.extend(items)

    logger.info(
        "Substitution/merge: %d cached extraction(s) -> %d contacts, %d companies, %d events",
        len(extractions), len(all_contacts), len(all_companies), len(all_events),
    )

    merged_contacts = merge_contacts({"contacts": []}, all_contacts)
    save_contacts(merged_contacts)

    merged_interests = merge_interests({"companies": [], "events": []}, all_companies, all_events)
    save_interests(merged_interests)

    return merged_contacts, merged_interests


def process_diary_store():
    """Extract anything new (the only step that can call Claude), then
    deterministically substitute known aliases and merge.
    """
    newly_extracted = extract_new_diary_entries()
    merged_contacts, merged_interests = apply_substitutions_and_merge()
    return newly_extracted, merged_contacts, merged_interests


_INVALID_FILENAME_CHARS = re.compile(r'[/\\:*?"<>|\x00-\x1f]')


def _sanitize_filename(name):
    """Strip characters that aren't safe in a filename"""
    return _INVALID_FILENAME_CHARS.sub("", name).strip()


def _existing_note_stems(directory):
    """Lowercased filename stems (without extension) already present in `directory`"""
    if not directory.exists():
        return set()
    return {p.stem.lower() for p in directory.iterdir() if p.is_file()}


def _create_missing_notes(names, directory):
    """Create a `# Name` placeholder note for any name not already present
    (case-insensitively) in `directory`. Never touches an existing file,
    regardless of its content or size.
    """
    directory.mkdir(parents=True, exist_ok=True)
    existing = _existing_note_stems(directory)
    created = []

    for name in names:
        filename = _sanitize_filename(name)
        if not filename or filename.lower() in existing:
            continue
        path = directory / f"{filename}.md"
        path.write_text(f"# {name}\n")
        existing.add(filename.lower())
        created.append(name)
        logger.info("Created Obsidian placeholder note: %s", path)

    return created


def sync_obsidian_placeholders():
    """Ensure every contact/company currently on the tracker has a note file in
    the Obsidian vault, creating a minimal `# Name` placeholder for any that
    don't. Reads only from load_contacts()/load_interests() - the same
    post-correction, merged data the dashboard itself displays - never from
    the raw pre-correction extraction cache. Never modifies or removes an
    existing note.
    """
    contact_names = [c["name"] for c in load_contacts().get("contacts", [])]
    company_names = [c["name"] for c in load_interests().get("companies", [])]

    contacts_created = _create_missing_notes(contact_names, OBSIDIAN_CONTACTS_DIR)
    companies_created = _create_missing_notes(company_names, OBSIDIAN_COMPANIES_DIR)

    logger.info(
        "Obsidian sync: %d contact note(s) created, %d company note(s) created",
        len(contacts_created), len(companies_created),
    )

    return contacts_created, companies_created


@app.route("/")
def dashboard():
    """Serve dashboard"""
    return render_template("dashboard.html")


@app.route("/api/contacts")
def get_contacts():
    """Return current contacts as JSON"""
    data = load_contacts()
    return jsonify(data)


@app.route("/api/interests")
def get_interests():
    """Return current companies/events of interest as JSON"""
    data = load_interests()
    return jsonify(data)


@app.route("/api/sync-obsidian", methods=["POST"])
def sync_obsidian():
    """Create placeholder notes in the Obsidian vault for any tracked contact/company
    that doesn't have one yet. Never touches an existing note.
    """
    try:
        contacts_created, companies_created = sync_obsidian_placeholders()
        return jsonify({
            "message": f"Created {len(contacts_created)} contact note(s), {len(companies_created)} company note(s)",
            "contacts_created": contacts_created,
            "companies_created": companies_created,
        })

    except Exception as e:
        logger.exception("sync_obsidian failed")
        return jsonify({"error": str(e)}), 500


@app.route("/api/corrections", methods=["POST"])
def add_correction():
    """Record a manual name correction and immediately re-apply it.

    Corrections are stored separately from contacts.json/plaud-interests.json
    (which are fully regenerated by apply_substitutions_and_merge) and
    re-applied every time, so a fix survives future runs. Goes through
    process_diary_store() (not apply_substitutions_and_merge() directly) so
    that if the extraction cache is empty or stale for any reason, it gets
    (re)populated first instead of merging against nothing and wiping
    contacts.json/plaud-interests.json - in the normal case, where the cache
    is already warm, this still costs zero Claude calls.
    """
    try:
        body = request.get_json(force=True)
        item_type = body.get("type")
        wrong_name = (body.get("wrong_name") or "").strip()
        correct_name = (body.get("correct_name") or "").strip()

        if item_type not in ("contacts", "companies", "events") or not wrong_name or not correct_name:
            return jsonify({"error": "type, wrong_name, and correct_name are all required"}), 400

        corrections = load_corrections()
        aliases = corrections.setdefault(item_type, {}).setdefault(correct_name, [])
        if wrong_name.lower() not in (a.lower() for a in aliases):
            aliases.append(wrong_name)
        save_corrections(corrections)
        logger.info('Correction added: "%s" -> "%s" (%s)', wrong_name, correct_name, item_type)

        newly_extracted, merged_contacts, merged_interests = process_diary_store()
        return jsonify({
            "message": f'Renamed "{wrong_name}" to "{correct_name}"',
            "new_extractions": newly_extracted,
            "total_contacts": len(merged_contacts["contacts"]),
            "total_companies": len(merged_interests["companies"]),
            "total_events": len(merged_interests["events"]),
        })

    except Exception as e:
        logger.exception("add_correction failed")
        return jsonify({"error": str(e)}), 500


@app.route("/api/fetch-mail", methods=["POST"])
def fetch_mail():
    """Fetch new diary emails from the mail server, store their raw text, then
    process the local diary store (extract anything new, then merge).
    """
    try:
        new_messages, processed_uids = fetch_diary_emails()
        emails_saved = 0

        for uid, email_data in new_messages:
            try:
                body, email_date = extract_email_body(email_data)
                add_diary_entry(body, source="email", noted_at=email_date)
                processed_uids.add(uid)
                emails_saved += 1
            except Exception:
                logger.exception("Error processing email %s", uid)
                continue

        save_processed_uids(processed_uids)
        newly_extracted, merged_contacts, merged_interests = process_diary_store()

        message = f"Fetched {emails_saved} new email(s)" if emails_saved else "No new emails"
        return jsonify({
            "message": message,
            "emails_fetched": emails_saved,
            "new_extractions": newly_extracted,
            "diary_entries": len(load_diary_entries()["entries"]),
            "total_contacts": len(merged_contacts["contacts"]),
            "total_companies": len(merged_interests["companies"]),
            "total_events": len(merged_interests["events"]),
        })

    except Exception as e:
        logger.exception("fetch_mail failed")
        return jsonify({"error": str(e)}), 500


@app.route("/api/process", methods=["POST"])
def process_local_data():
    """Extract any diary entries not yet extracted, then re-apply corrections and
    merge. Cheap in the common case - only new entries ever reach Claude.
    """
    try:
        newly_extracted, merged_contacts, merged_interests = process_diary_store()
        return jsonify({
            "message": f"Extracted {newly_extracted} new diary entrie(s), merged {len(load_diary_entries()['entries'])} total",
            "new_extractions": newly_extracted,
            "total_contacts": len(merged_contacts["contacts"]),
            "total_companies": len(merged_interests["companies"]),
            "total_events": len(merged_interests["events"]),
        })

    except Exception as e:
        logger.exception("process_local_data failed")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
