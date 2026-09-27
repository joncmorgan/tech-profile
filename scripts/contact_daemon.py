#!/usr/bin/env python3
"""
Plaud Diary Contact Tracker Daemon
Fetches diary transcripts from email, parses with Claude, updates contact list
"""

import json
import logging
import os
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
        logger.info("IMAP search found %d matching email(s)", len(messages))

        new_messages = []
        for uid in messages:
            if uid not in processed:
                data = server.fetch([uid], ["RFC822"])
                if uid in data:
                    email_data = data[uid][b"RFC822"]
                    new_messages.append((uid, email_data))

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
    """Send transcript to Claude, extract contacts, companies, and events of interest"""
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


def rebuild_from_diary_entries():
    """Re-parse every stored diary entry with Claude and rebuild contacts.json and
    plaud-interests.json from scratch.

    Always starts from empty lists (rather than the existing files) so this
    can be re-run any time - e.g. after a prompt/parsing fix - without needing
    new mail, and without piling up duplicate touchpoints.
    """
    diary = load_diary_entries()
    all_contacts, all_companies, all_events = [], [], []

    for entry in diary["entries"]:
        noted_at = entry.get("noted_at")
        reference_date = datetime.fromisoformat(noted_at) if noted_at else None
        extracted = parse_transcript_with_claude(entry["text"], reference_date=reference_date)

        for bucket in (extracted["contacts"], extracted["companies"], extracted["events"]):
            for item in bucket:
                item["diary_entry_id"] = entry["id"]
                item["noted_at"] = noted_at

        all_contacts.extend(extracted["contacts"])
        all_companies.extend(extracted["companies"])
        all_events.extend(extracted["events"])

    merged_contacts = merge_contacts({"contacts": []}, all_contacts)
    save_contacts(merged_contacts)

    merged_interests = merge_interests({"companies": [], "events": []}, all_companies, all_events)
    save_interests(merged_interests)

    return merged_contacts, merged_interests


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


@app.route("/api/fetch-mail", methods=["POST"])
def fetch_mail():
    """Fetch new diary emails from the mail server, store their raw text, then
    process the local diary store so contacts stay in sync with what's fetched.
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
        merged_contacts, merged_interests = rebuild_from_diary_entries()

        message = f"Fetched {emails_saved} new email(s)" if emails_saved else "No new emails"
        return jsonify({
            "message": message,
            "emails_fetched": emails_saved,
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
    """Re-parse all stored diary entries with Claude and rebuild contacts.json and plaud-interests.json"""
    try:
        merged_contacts, merged_interests = rebuild_from_diary_entries()
        return jsonify({
            "message": f"Processed {len(load_diary_entries()['entries'])} diary entrie(s)",
            "total_contacts": len(merged_contacts["contacts"]),
            "total_companies": len(merged_interests["companies"]),
            "total_events": len(merged_interests["events"]),
        })

    except Exception as e:
        logger.exception("process_local_data failed")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
