# CV builder

Generates `output/Jon_Morgan_CV.docx` and `output/profile-brief.md` from the
Obsidian vault. This is the only CV pipeline in this repo — an earlier
Typst-based one (multi-variant resumes + cover letters) was retired
2026-09-24 as part of moving to a single canonical CV and a facts/positioning
split in the vault. Plain Python + `python-docx`, deliberately kept simple
so any change can be made — or reviewed — without needing to trust the code
blindly.

## Architecture — read this before editing anything

Three layers, each with a different job. Getting content into the wrong
layer is the one mistake to avoid here.

- **`vault/00-Facts/`** — neutral, verifiable facts only. Dates, employers,
  what actually happened. No marketing language, no audience-specific
  phrasing, no "role" labels invented for a document. If it reads like it
  was written to impress someone, it doesn't belong here.
- **`vault/02-Positioning/`** — curated prose, written deliberately (usually
  in conversation with Claude), sourced from the facts above. This is where
  CV/LinkedIn/Seek wording actually lives: `CV-Positioning.md` (headline,
  summary, quote, competencies), `employment/*.md` (per-employer CV
  paragraphs), `CV-Project-Highlights.md` (per-project blurbs). Positioning
  changes as your market approach evolves — that's expected and fine, it's
  why this is separate from facts.
- **`vault/01-Projects/`** — one fact-only note per project. Like
  `00-Facts`, not `02-Positioning`.
- **`cv/config.json`** — which projects appear on the CV, in what order, and
  which employer entries appear in what order. This is the only place
  "curation" (as opposed to "content") lives.

The scripts in this folder only **assemble** — they read the above and lay
it out as a document. They never invent or rewrite wording. If the CV reads
wrong, fix the source file in `vault/`, not the script.

## Usage

```bash
cd cv
pip install -r requirements.txt   # or: uv pip install -r requirements.txt
python build_cv.py                # -> ../output/Jon_Morgan_CV.docx
python build_profile_brief.py     # -> ../output/profile-brief.md
```

`lib/load_vault.py` is the only shared code — a small, dependency-free
frontmatter parser (no PyYAML needed, since the vault's frontmatter is
simple flat key/value pairs plus the occasional inline array). Both scripts
import it the same way; there's nothing else in the pipeline.

## Keeping LinkedIn and Seek consistent with the CV

`profile-brief.md` is generated from the exact same sources as the CV. When
updating LinkedIn or Seek by hand, copy the wording, dates and titles from
that file rather than from memory or from what's currently live on those
platforms — that's what keeps all three in sync. If you change something on
LinkedIn/Seek that should also change on the CV, make the edit in
`vault/02-Positioning` (or `vault/00-Facts` if it's a factual change) and
regenerate both outputs, rather than editing LinkedIn and the CV separately.

## Common maintenance tasks

- **A fact changed** (new job, corrected dates, etc.) → edit
  `vault/00-Facts/...`. If the CV's prose for that employer/project also
  needs to change, update the matching file in `vault/02-Positioning/` too —
  the two aren't linked automatically, by design (see Architecture above).
- **Want different projects on the CV** → edit `cv/config.json`'s
  `selectedProjects` (must be ids that exist as `## <id>` sections in
  `vault/02-Positioning/CV-Project-Highlights.md` — the script raises a
  clear error if you reference one that doesn't exist yet, rather than
  silently skipping it).
- **Adding a new employer or project entirely** → add the fact file under
  `00-Facts`, then a matching positioning file, then reference it from
  `cv/config.json`.
- **Styling changes** (colour, fonts, margins) → `build_cv.py`, near the
  top: `ACCENT_COLOR`, `TEXT_COLOR`, `MUTED_COLOR`, `FONT_NAME`.

## Known gaps

- `ACCENT_COLOR` in `build_cv.py` is a placeholder red — the exact hex from
  the earlier "signal red" theme wasn't recovered when this was rebuilt.
  Confirm/replace it if it doesn't match.
- `vault/01-Projects/physics-informed-ml-surrogate-model.md` has an
  unconfirmed employer attribution — resolve that before treating anything
  about that project as settled fact.
