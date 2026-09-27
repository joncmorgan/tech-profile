# Plaud Diary Contact Tracker

Voice-driven contact follow-up system. Speak diary notes, Plaud transcribes them, daemon parses with Claude, dashboard shows who to call.

## Setup

### 1. Fastmail App Password

1. Go to [Fastmail Settings → Security → App Passwords](https://app.fastmail.com/settings/security)
2. Create a new app password
3. Copy it

### 2. Anthropic API Key

1. Get your API key from [Anthropic Console](https://console.anthropic.com/)
2. Make sure it has access to Claude

### 3. Environment Variables

```bash
cp scripts/.env.example scripts/.env
# Edit scripts/.env with your credentials
```

### 4. Install Dependencies

```bash
uv sync
```

## Running

```bash
uv run scripts/contact_daemon.py
```

Opens dashboard at `http://localhost:5000`

## Workflow

1. **Record in Plaud**: Say "Diary. Call Pete Buffett Monday. Follow up with Ian Adams next week."
2. **Plaud AutoFlow**: Automatically emails transcript to `jonmorgan+plaude@fastmail.com`
3. **Click "Run Now"** on dashboard
4. **Daemon**:
   - Fetches new emails from inbox
   - Sends transcript to Claude: "Extract who to call and when"
   - Parses response, merges into contact list
   - Updates `vault/plaud-contacts.json`
5. **Dashboard** shows updated list

## Files

- `contact_daemon.py` — Flask server + IMAP + Claude parsing
- `vault/plaud-contacts.json` — Your contact list (auto-generated, derived from diary entries)
- `vault/plaud-diary-entries.json` — Intermediate store of raw diary notes (email + manual backfill)
- `vault/.plaud-processed-uids` — Tracks which emails we've already processed (gitignored)

## Backfilling Diary Entries

You can manually add diary entries to backfill contacts that haven't come via email:

1. Copy the example: `cp scripts/plaud-diary-entries.example.json vault/plaud-diary-entries.json`
2. Edit `vault/plaud-diary-entries.json` with your past diary notes:
   ```json
   {
     "entries": [
       {
         "id": "2026-09-27T09:00:00",
         "timestamp": "2026-09-27T09:00:00",
         "source": "manual",
         "text": "Call Pete Buffett Monday about director role"
       },
       {
         "id": "2026-09-27T10:30:00",
         "timestamp": "2026-09-27T10:30:00",
         "source": "manual",
         "text": "Follow up with Steve Downing next week"
       }
     ]
   }
   ```
3. Click "Run Now" — daemon will parse all entries and populate `plaud-contacts.json`

The `id` and `timestamp` can be any ISO timestamp. Use `source: "manual"` for hand-entered entries.

## Configuration

**Plaud AutoFlow Setup:**
- In Plaud app, set up AutoFlow rule:
  - Trigger: New recordings with tag/template "diary"
  - Action: Email transcript to `jonmorgan+plaude@fastmail.com`

## Notes

- Each click of "Run Now" checks for new emails since last run
- Contacts are deduplicated by name + date
- If Claude parsing fails on an email, it's logged but doesn't stop the daemon
- Dashboard auto-refreshes contact list after each run
