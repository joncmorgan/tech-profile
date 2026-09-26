"""
Builds jonmorgan.au (site/dist/index.html) from output/profile-brief.md —
the same generated file used to keep LinkedIn and Seek in sync with the CV.

This script does NOT invent or rewrite content. It only:
  1. Splits profile-brief.md into its "## " sections.
  2. Drops instructional notes-to-self (parenthetical lines meant for
     editing LinkedIn/Seek by hand, not for public display).
  3. Converts each section's markdown to HTML fragments.
  4. Drops those fragments into template.html's {{PLACEHOLDER}} slots.
  5. Converts output/Jon_Morgan_CV.docx to a PDF (via headless LibreOffice)
     and links it from the page, for anyone who wants a hard copy.

If the site reads wrong, fix vault/00-Facts or vault/02-Positioning and
regenerate profile-brief.md (cv/build_profile_brief.py) — not this script
or the HTML.

Usage:
    uv run site/build_site.py        # -> site/dist/index.html, dist/style.css
"""

import re
import shutil
import subprocess
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
PROFILE_BRIEF = ROOT / "output" / "profile-brief.md"
CV_DOCX = ROOT / "output" / "Jon_Morgan_CV.docx"
SITE_DIR = Path(__file__).resolve().parent
TEMPLATE = SITE_DIR / "template.html"
STYLE = SITE_DIR / "style.css"
DIST = SITE_DIR / "dist"
CV_PDF_NAME = "Jon_Morgan_CV.pdf"


def strip_meta_notes(text: str) -> str:
    """Drop whole-line parenthetical notes-to-self, e.g.
    '(LinkedIn headline field is capped at 220 characters -- ...)'."""
    lines = []
    for line in text.split("\n"):
        stripped = line.strip()
        if stripped.startswith("(") and stripped.endswith(")"):
            continue
        lines.append(line)
    return "\n".join(lines).strip()


def parse_sections(md_text: str) -> dict[str, str]:
    """Split on '## Heading' lines, return {heading: body}."""
    parts = re.split(r"\n## ", "\n" + md_text)
    sections = {}
    for part in parts[1:]:
        heading, _, body = part.partition("\n")
        sections[heading.strip()] = strip_meta_notes(body)
    return sections


def to_html(md_text: str) -> str:
    return markdown.markdown(md_text.strip(), extensions=["extra"])


def style_quote_paragraph(html: str) -> str:
    """profile-brief.md's pull-quote is a plain paragraph wrapped in
    curly/straight quotes, not markdown blockquote syntax. Turn the first
    such paragraph in the summary into a real <blockquote> so style.css's
    pull-quote styling applies."""
    return re.sub(
        r"<p>([\"“][^<]*[\"”])</p>",
        r"<blockquote>\1</blockquote>",
        html,
        count=1,
    )


def build_cv_pdf() -> bool:
    """Convert output/Jon_Morgan_CV.docx to a PDF in dist/ via headless
    LibreOffice, so the site can offer a hard-copy download. Returns True
    on success. If soffice isn't installed (e.g. a quick local run), skips
    with a warning rather than failing the whole build — the CI workflow
    installs LibreOffice specifically so this step works there."""
    if not CV_DOCX.exists():
        print(f"WARNING: {CV_DOCX} not found — skipping CV PDF link.")
        return False
    if shutil.which("soffice") is None:
        print("WARNING: 'soffice' (LibreOffice) not found on PATH — "
              "skipping CV PDF conversion. Install LibreOffice to enable "
              "the CV download link locally; CI installs it automatically.")
        return False

    result = subprocess.run(
        ["soffice", "--headless", "--convert-to", "pdf",
         "--outdir", str(DIST), str(CV_DOCX)],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"WARNING: LibreOffice PDF conversion failed:\n{result.stderr}")
        return False

    produced = DIST / (CV_DOCX.stem + ".pdf")
    if produced.name != CV_PDF_NAME:
        produced.rename(DIST / CV_PDF_NAME)
    return True


def skills_to_pills(skills_line: str) -> str:
    """profile-brief.md's skills line is a single '·'-separated string.
    Wrap each term as its own span so style.css can render them as pill
    tags — same words, just individually taggable markup."""
    terms = [t.strip() for t in skills_line.strip().split("·") if t.strip()]
    spans = "".join(f"<span class='pill'>{t}</span>" for t in terms)
    return f"<p>{spans}</p>"


def build_name_headline_contact(sections: dict) -> tuple[str, str, str]:
    name_block = sections.get("Name / Headline", "").strip().split("\n")
    name = name_block[0].strip() if name_block else "Jon Morgan"
    headline = name_block[1].strip() if len(name_block) > 1 else ""
    contact = sections.get("Contact", "").strip()
    return name, headline, contact


def main():
    if not PROFILE_BRIEF.exists():
        raise SystemExit(
            f"{PROFILE_BRIEF} not found — run "
            "cv/build_profile_brief.py first."
        )

    md_text = PROFILE_BRIEF.read_text(encoding="utf-8")
    sections = parse_sections(md_text)

    name, headline, contact = build_name_headline_contact(sections)

    summary_section = sections.get("Summary / About", "")
    summary_html = style_quote_paragraph(to_html(summary_section))

    replacements = {
        "{{NAME}}": name,
        "{{HEADLINE}}": headline,
        "{{CONTACT}}": contact,
        "{{SUMMARY}}": summary_html,
        "{{CORE_COMPETENCIES}}": to_html(sections.get("Core Competencies", "")),
        "{{CAREER_HISTORY}}": to_html(
            sections.get(
                "Career History (use identical dates/titles across LinkedIn, Seek and the CV)",
                "",
            )
        ),
        "{{SELECTED_PROJECTS}}": to_html(
            sections.get(
                "Selected Projects (for LinkedIn's Featured/Projects section or Seek's summary)",
                "",
            )
        ),
        "{{SKILLS}}": skills_to_pills(sections.get("Skills / Domain Expertise", "")),
        "{{CREDENTIALS}}": to_html(sections.get("Credentials", "")),
        "{{EDUCATION}}": to_html(sections.get("Education", "")),
    }

    DIST.mkdir(exist_ok=True)
    cv_pdf_available = build_cv_pdf()
    replacements["{{CV_PDF_FILENAME}}"] = CV_PDF_NAME if cv_pdf_available else "#"

    html = TEMPLATE.read_text(encoding="utf-8")
    for placeholder, value in replacements.items():
        html = html.replace(placeholder, value)

    if not cv_pdf_available:
        # No PDF this run — don't ship a dead download link.
        html = html.replace(
            '<a class="cv-download" href="#" download>Download CV (PDF)</a>',
            "",
        )

    (DIST / "index.html").write_text(html, encoding="utf-8")
    (DIST / "style.css").write_text(STYLE.read_text(encoding="utf-8"), encoding="utf-8")

    print(f"Wrote {DIST / 'index.html'}")
    print(f"Wrote {DIST / 'style.css'}")
    if cv_pdf_available:
        print(f"Wrote {DIST / CV_PDF_NAME}")


if __name__ == "__main__":
    main()
