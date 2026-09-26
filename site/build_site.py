"""
Builds jonmorgan.au (site/dist/index.html) from output/profile-brief.md —
the same generated file used to keep LinkedIn and Seek in sync with the CV.

This script does NOT invent or rewrite content. It only:
  1. Splits profile-brief.md into its "## " sections.
  2. Drops instructional notes-to-self (parenthetical lines meant for
     editing LinkedIn/Seek by hand, not for public display).
  3. Converts each section's markdown to HTML fragments.
  4. Drops those fragments into template.html's {{PLACEHOLDER}} slots.

If the site reads wrong, fix vault/00-Facts or vault/02-Positioning and
regenerate profile-brief.md (cv/build_profile_brief.py) — not this script
or the HTML.

Usage:
    uv run site/build_site.py        # -> site/dist/index.html, dist/style.css
"""

import re
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
PROFILE_BRIEF = ROOT / "output" / "profile-brief.md"
SITE_DIR = Path(__file__).resolve().parent
TEMPLATE = SITE_DIR / "template.html"
STYLE = SITE_DIR / "style.css"
DIST = SITE_DIR / "dist"


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
        "{{SKILLS}}": to_html(sections.get("Skills / Domain Expertise", "")),
        "{{CREDENTIALS}}": to_html(sections.get("Credentials", "")),
        "{{EDUCATION}}": to_html(sections.get("Education", "")),
    }

    html = TEMPLATE.read_text(encoding="utf-8")
    for placeholder, value in replacements.items():
        html = html.replace(placeholder, value)

    DIST.mkdir(exist_ok=True)
    (DIST / "index.html").write_text(html, encoding="utf-8")
    (DIST / "style.css").write_text(STYLE.read_text(encoding="utf-8"), encoding="utf-8")

    print(f"Wrote {DIST / 'index.html'}")
    print(f"Wrote {DIST / 'style.css'}")


if __name__ == "__main__":
    main()