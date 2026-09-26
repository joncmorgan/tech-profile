#!/usr/bin/env python3
"""
Convert data/projects.json into one markdown file per project under
vault/01-Projects/, with YAML frontmatter and a neutral, fact-only markdown
body (Context + Execution). No positioning/marketing language, no
per-project "role" field (real titles live in vault/00-Facts/employment/).

Usage:
    python build_project_notes.py [--input data/projects.json] [--output vault/01-Projects]

Safe to re-run: overwrites files it previously generated.
"""
import argparse
import json
import re
from pathlib import Path

# ----------------------------------------------------------------------
# Per-project overrides. Keyed by project "id" from projects.json.
# ----------------------------------------------------------------------
CORRECTIONS = {
    "fire-behaviour-smoke-dynamics": {
        "execution_replacements": {
            "Team Leadership & Mentorship: Led the Australasia Building Physics group, "
            "training and mentoring graduate analysts and junior mechanical engineers "
            "in computational physics and simulation pipelines.":
            "Technical Leadership: Held the formal title of Australasia Building Physics "
            "Lead with two direct reports; provided informal technical leadership and "
            "mentoring across ~10 further staff embedded in other teams (mechanical, "
            "facades) throughout APAC."
        },
    },
    "commercial-rebrand-operational-overhaul": {
        "confidentiality": "needs-review",
    },
    "enterprise-infrastructure-risk-audit": {
        "confidentiality": "needs-review",
    },
    "bespoke-2.5d-to-3d-computational-geometry-engine": {
        "status": "delivered",
        "company_override": "Co-Perform",
        "note": "IP note: this implementation belongs to Co-Perform. Not available "
                "for reuse in any new engagement (e.g. the BER-Engine concept) now "
                "that Jon has left the practice — any future build starts from "
                "scratch. Co-Perform continues to use this version.",
    },
    "city-of-melbourne-sustainable-building-standards": {
        "execution_replacements": {
            "Resilient Infrastructure Guidelines: Formulated strategic protocols for "
            "retrofitting existing facilities and designing new builds to withstand "
            "future climate extremes, including bushfire smoke events, severe "
            "heatwaves, and flooding. Addressed mechanical service adaptation, "
            "backup/off-grid power generation, and solar-battery integration.":
            "Resilient Infrastructure Guidelines: Formulated strategic protocols for "
            "retrofitting existing facilities and designing new builds to withstand "
            "future climate extremes, including bushfire smoke events and severe "
            "heatwaves. Addressed mechanical service adaptation, backup/off-grid "
            "power generation, and solar-battery integration."
        },
    },
    "government-resilient-housing-prototype": {
        "execution_replacements": {
            "Physical Build Benchmark: Evaluated building resilience under extreme "
            "stress testing to guide envelope parameters, resulting in a physical "
            "build that stands as a recognised benchmark of climate-adaptive "
            "architecture.":
            "Physical Build: Evaluated building resilience under extreme stress "
            "testing to guide envelope parameters, resulting in a completed "
            "physical build."
        },
        "note": "Unverified: Jon believes this may be one of relatively few built "
                "examples of this kind of climate-adaptive housing prototype in "
                "Australia, and that it may have received some form of recognition "
                "or award — neither has been confirmed. Do not state as fact "
                "until checked.",
    },
    "comprehensive-thermal-comfort-modelling-suite": {
        "context_replace": (
            "Over 25 years of deep research, academic literature review, and custom "
            "implementation of human thermal comfort indices across diverse global "
            "master plans and environments (including White City in London, "
            "numerous shopping centres, outdoor public spaces across Melbourne and "
            "regional areas, and Singapore).",
            "Applied, career-spanning work (not academic research — Jon has "
            "always worked as an applied engineer, not a researcher) on human "
            "thermal comfort indices across diverse global master plans and "
            "environments, including White City in London, numerous shopping "
            "centres, outdoor public spaces across Melbourne and regional areas, "
            "and Singapore."
        ),
    },
    "battery-energy-storage-systems-digital-twin": {
        "execution_replacements": {
            "Agentic Tooling & Container Architecture: Built as one of the earliest "
            "AI agentic tooling experiments prototyped in VS Code. Wrapped the NREL "
            "System Advisory Model (SAM) engine into a custom Python codebase "
            "packaged into a container for on-demand ephemeral execution.":
            "Agentic Tooling & Container Architecture: Built as one of Jon's first "
            "personal experiments with AI agentic tooling, prototyped in VS Code. "
            "Wrapped the NREL System Advisory Model (SAM) engine into a custom "
            "Python codebase packaged into a container for on-demand ephemeral "
            "execution."
        },
    },
    "offshore-platform-blast-modelling": {
        "execution_replacements": {
            "Workflow Acceleration & Accuracy: Eliminated manual CAD geometry "
            "recreation, saving hundreds of engineering hours per project while "
            "increasing solver accuracy.":
            "Workflow Acceleration & Accuracy: Eliminated manual CAD geometry "
            "recreation, reducing engineering time per project and increasing "
            "solver accuracy. (No verified figures for time saved — Jon's own "
            "estimate is on the order of hundreds of hours per project, not "
            "independently confirmed.)"
        },
    },
    "reflected-glare-hazard-studies": {
        "execution_replacements": {
            "Reporting Artifacts & Industry Benchmark: Produced structured "
            "technical reports, visual mapping diagrams, and communication "
            "artifacts for transport infrastructure and property development "
            "clients. Pioneered an automated numerical approach at Arup that "
            "established the technical foundation for subsequent internal glare "
            "assessment workflows.":
            "Reporting Artifacts: Produced structured technical reports, visual "
            "mapping diagrams, and communication artifacts for transport "
            "infrastructure and property development clients. Built the automated "
            "Radiance-based numerical glare-calculation workflow from scratch — "
            "to Jon's knowledge this approach had not been done before at Arup. "
            "Whether it continued to be used there after he left has not been "
            "verified."
        },
    },
    "daylight-solar-access-visual-comfort": {
        "execution_replacements": {
            "Design Optimisation & Visual Comfort: Conducted seasonal daylight and "
            "internal glare assessments to resolve functional design challenges: "
            "evaluating visual comfort in commercial offices to eliminate disabling "
            "glare on computer visual display units (VDUs); assessing direct "
            "daylight hours in aged care facilities to guarantee residents had "
            "sufficient natural light to comfortably read newspapers adjacent to "
            "windows; and guiding architectural massing, sizing, and geometric "
            "proportioning of internal light wells and light courts.":
            "Design Optimisation & Visual Comfort: Conducted seasonal daylight and "
            "internal glare assessments to resolve functional design challenges: "
            "evaluating visual comfort in commercial offices to eliminate disabling "
            "glare on computer visual display units (VDUs); assessing direct "
            "daylight hours in aged care facilities to help ensure residents had "
            "sufficient natural light to comfortably read newspapers adjacent to "
            "windows; and guiding architectural massing, sizing, and geometric "
            "proportioning of internal light wells and light courts."
        },
    },
    "physics-informed-ml-surrogate-model": {
        "note": "UNCONFIRMED (24 Sep 2026): Jon was unsure of the details when asked "
                "— believes this may actually have been done at Moreland Energy "
                "Foundation (building performance, not solar generation) as a "
                "prototype, rather than at Co-Perform/Arup as currently listed. "
                "Needs Jon's confirmation before company/status fields are trusted.",
    },
}

PERIODS = [
    ("DSTO", (1996, 2000)),
    ("British Maritime Technology", (2002, 2004)),
    ("BMT", (2002, 2004)),
    ("Arup", (2004, 2014)),
    ("Physical Computing Practice", (2004, 2014)),
    ("Independent Consultant", (2004, 2014)),
    ("Moreland", (2014, 2018)),
    ("MEFL", (2014, 2018)),
    ("DHHS", (2014, 2018)),
    ("Co-Perform", (2018, 2026)),
    ("Nation Partners", (2018, 2026)),
    ("MAV", (2018, 2026)),
    ("CASBE", (2018, 2026)),
]


def guess_period(company: str) -> str:
    spans = [span for key, span in PERIODS if key.lower() in company.lower()]
    if not spans:
        return "TBC - verify"
    start = min(s for s, _ in spans)
    end = max(e for _, e in spans)
    return f"{start}-{end}"


def yq(value: str) -> str:
    return '"' + str(value).replace('"', '\\"') + '"'


def slugify(project_id: str) -> str:
    return re.sub(r"[^a-z0-9-]", "-", project_id.lower())


def build_note(project: dict) -> str:
    pid = project["id"]
    corr = CORRECTIONS.get(pid, {})

    status = corr.get("status", "delivered")
    confidentiality = corr.get("confidentiality", "public")
    company = corr.get("company_override", project.get("company", ""))
    period = guess_period(company)

    context = project.get("context", "").strip()
    if "context_replace" in corr:
        old, new = corr["context_replace"]
        context = context.replace(old, new)

    replacements = corr.get("execution_replacements", {})
    execution_lines = []
    for bullet in project.get("execution", []):
        bullet = replacements.get(bullet, bullet)
        execution_lines.append(f"- {bullet}")

    frontmatter = "\n".join([
        "---",
        f"id: {yq(pid)}",
        f"title: {yq(project.get('title', ''))}",
        f"company: {yq(company)}",
        f"period: {yq(period)}",
        f"outcome: {yq(project.get('outcome', ''))}",
        f"primaryCategory: {yq(project.get('primaryCategory', ''))}",
        f"secondaryCategory: {yq(project.get('secondaryCategory', ''))}",
        f"status: {yq(status)}",
        f"confidentiality: {yq(confidentiality)}",
        "---",
    ])

    body_parts = [
        "",
        f"# {project.get('title', '')}",
        "",
        "## Context",
        context,
        "",
        "## Execution",
        *execution_lines,
        "",
    ]

    if "note" in corr:
        body_parts += ["## Note", corr["note"], ""]

    return frontmatter + "\n".join(body_parts)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/projects.json")
    parser.add_argument("--output", default="vault/01-Projects")
    args = parser.parse_args()

    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)

    written = []
    for project in data["projects"]:
        note = build_note(project)
        filename = slugify(project["id"]) + ".md"
        out_path = out_dir / filename
        out_path.write_text(note, encoding="utf-8")
        written.append(out_path)

    print(f"Wrote {len(written)} project notes to {out_dir}/")
    flagged = [p["id"] for p in data["projects"] if p["id"] in CORRECTIONS]
    if flagged:
        print("Corrections applied to:", ", ".join(flagged))


if __name__ == "__main__":
    main()
