"""
Small, dependency-free loader for the vault's markdown files.

The frontmatter in this repo is deliberately simple (flat scalars, plus
occasional inline JSON arrays like ["a", "b"]), so a hand-rolled parser
avoids pulling in a real YAML library just for this. If the vault's
frontmatter ever gets more complex (nested objects, multi-line strings),
switch to PyYAML instead of extending this.
"""
import json
import re
from pathlib import Path

FRONTMATTER_RE = re.compile(r"^---\r?\n(.*?)\r?\n---\r?\n?(.*)$", re.S)
HEADING_RE = re.compile(r"^##\s+(.*)$")
KEY_RE = re.compile(r"^([A-Za-z0-9_]+):\s*(.*)$")


def parse_scalar(value: str):
    value = value.strip()
    if value.startswith("[") and value.endswith("]"):
        try:
            return json.loads(value)
        except ValueError:
            return value
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1].replace('\\"', '"')
    return value


def parse_frontmatter(raw: str):
    m = FRONTMATTER_RE.match(raw)
    if not m:
        return {}, raw
    fm_block, body = m.group(1), m.group(2)
    data = {}
    for line in fm_block.splitlines():
        if not line.strip():
            continue
        km = KEY_RE.match(line)
        if not km:
            continue
        key, raw_value = km.group(1), km.group(2)
        data[key] = parse_scalar(raw_value)
    return data, body.lstrip("\n")


def load_file(path: Path):
    raw = path.read_text(encoding="utf-8")
    return parse_frontmatter(raw)


def split_sections(body: str) -> dict:
    """Split a markdown body into sections keyed by '## Heading' (H2 only)."""
    sections = {}
    current = None
    buf = []

    def flush():
        if current is not None:
            sections[current] = "\n".join(buf).strip()

    for line in body.splitlines():
        m = HEADING_RE.match(line)
        if m:
            flush()
            buf.clear()
            current = m.group(1).strip()
        elif current is not None:
            buf.append(line)
    flush()
    return sections


def bullets_from(section_text: str):
    if not section_text:
        return []
    out = []
    for line in section_text.splitlines():
        line = line.strip()
        if line.startswith("- "):
            out.append(line[2:].strip())
    return out


def load_profile(vault_dir: Path) -> dict:
    data, body = load_file(vault_dir / "00-Facts" / "profile.md")
    sections = split_sections(body)
    return {
        "name": data.get("name"),
        "email": data.get("email"),
        "phone": data.get("phone"),
        "location": data.get("location"),
        "linkedin": data.get("linkedin"),
        "credentials": bullets_from(sections.get("Credentials")),
        "education": bullets_from(sections.get("Education")),
    }


def load_positioning(vault_dir: Path) -> dict:
    _, body = load_file(vault_dir / "02-Positioning" / "CV-Positioning.md")
    sections = split_sections(body)
    return {
        "headline": sections.get("Headline", "").strip(),
        "target_roles": sections.get("Target roles", "").strip(),
        "summary": sections.get("Summary", "").strip(),
        "quote": sections.get("Quote", "").strip(),
        "core_competencies": bullets_from(sections.get("Core competencies")),
        "domain_expertise": sections.get("Technical & domain expertise", "").strip(),
    }


def load_employment(vault_dir: Path, order):
    out = []
    for id_ in order:
        data, body = load_file(vault_dir / "02-Positioning" / "employment" / f"{id_}.md")
        out.append(
            {
                "id": id_,
                "display_label": data.get("displayLabel"),
                "period": data.get("period"),
                "location": data.get("location"),
                "type": data.get("type", "paragraph"),
                "body": re.sub(r"<!--.*?-->", "", body, flags=re.S).strip(),
            }
        )
    return out


def load_project_highlights(vault_dir: Path, selected_ids):
    _, body = load_file(vault_dir / "02-Positioning" / "CV-Project-Highlights.md")
    sections = split_sections(body)
    out = []
    for id_ in selected_ids:
        raw = sections.get(id_)
        if raw is None:
            raise ValueError(
                f'No CV highlight found for project id "{id_}" in '
                "CV-Project-Highlights.md. Either add one, or remove it "
                "from cv/config.json's selectedProjects."
            )
        text = re.sub(r"<!--.*?-->", "", raw, flags=re.S).strip()
        out.append({"id": id_, "text": text})
    return out
