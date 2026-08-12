import sys
import json
import shutil
from pathlib import Path

try:
    import typst
except ImportError:
    print("❌ Error: The 'typst' Python package is not installed.\n👉 Run: uv add typst", file=sys.stderr)
    sys.exit(1)

# Paths (UNCHANGED)
SCRIPT_DIR = Path(__file__).parent.resolve()
PROJECT_ROOT = SCRIPT_DIR.parents[1]
DATA_DIR = PROJECT_ROOT / "data"

SIGNATURE_SOURCE = DATA_DIR / "sig-jon.png"

TARGETS = [
    ("resume.typ", "jon_morgan_resume.pdf"),
    ("letter.typ", "jon_morgan_cover_letter.pdf")
]

DEFAULT_CONFIG = {
    "profile": "ai_solutions",
    "tags": ["stream:boutique", "layer:handson", "domain:ai"],
    "inspect_only": False
}

def ensure_control_config(cwd: Path) -> dict:
    """Loads build_config.json from CWD or creates a default template if missing."""
    config_path = cwd / "build_config.json"
    
    if not config_path.exists():
        print(f"⚙️  `build_config.json` not found in `{cwd}`.")
        print(f"📄 Generating template `build_config.json`...")
        try:
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(DEFAULT_CONFIG, f, indent=2)
            print(f"✨ Default config created successfully: `{config_path.name}`\n")
        except Exception as e:
            print(f"❌ Error creating template config: {e}", file=sys.stderr)
            sys.exit(1)
        return DEFAULT_CONFIG

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            print(f"📋 Loaded control config: `{config_path.name}`")
            return json.load(f)
    except Exception as e:
        print(f"⚠️ Warning: Failed to parse `{config_path}`: {e}. Falling back to defaults.", file=sys.stderr)
        return DEFAULT_CONFIG

def filter_master_resume(master_path: Path, profile_key: str = None, target_tags: list = None) -> dict:
    """Filters master_resume.json into the standard resume_data.json schema."""
    with open(master_path, "r", encoding="utf-8") as f:
        master = json.load(f)

    # 1. Resolve Profile & Target Tags
    profiles = master.get("profiles", {})
    if profile_key and profile_key in profiles:
        selected_profile = profiles[profile_key]
    else:
        # Fallback to first profile if not specified or invalid key
        first_key = list(profiles.keys())[0] if profiles else None
        selected_profile = profiles.get(first_key, {}) if first_key else {}
        profile_key = first_key

    # Combine tags from explicit target_tags + profile defaults
    profile_tags = selected_profile.get("tags", [])
    active_tags = set(target_tags or profile_tags)

    def matches_tags(item_tags):
        if not active_tags:
            return True
        return bool(active_tags.intersection(set(item_tags or [])))

    # 2. Filter Capabilities
    filtered_capabilities = []
    for cap in master.get("capabilities_pool", []):
        if matches_tags(cap.get("tags", [])):
            filtered_capabilities.append({
                "title": cap.get("title", ""),
                "description": cap.get("description", "")
            })
    filtered_capabilities = filtered_capabilities[:4]  # Constrain to top 4 for layout

    # 3. Filter Experience Highlights
    filtered_experience = []
    for exp in master.get("experience", []):
        matching_highlights = []
        for hl in exp.get("highlights", []):
            if isinstance(hl, dict):
                if matches_tags(hl.get("tags", [])):
                    matching_highlights.append(hl.get("text", ""))
            elif isinstance(hl, str):
                matching_highlights.append(hl)

        filtered_experience.append({
            "company": exp.get("company", ""),
            "role": exp.get("role", ""),
            "period": exp.get("period", ""),
            "summary": exp.get("summary", ""),
            "highlights": matching_highlights
        })

    # 4. Filter Technical Skills
    filtered_skills = []
    for skill in master.get("technical_skills", []):
        if matches_tags(skill.get("tags", [])) or "tags" not in skill:
            filtered_skills.append({
                "title": skill.get("group", skill.get("title", "")),
                "description": skill.get("description", "")
            })

    # Assemble Output Schema
    contact = master.get("contact", {})
    return {
        "name": contact.get("name", "Jon Morgan"),
        "post_nominals": contact.get("post_nominals", ""),
        "title": selected_profile.get("title", ""),
        "contact": contact,
        "about": selected_profile.get("about", ""),
        "capabilities": filtered_capabilities,
        "experience": filtered_experience,
        "technical_skills": filtered_skills,
        "education": master.get("education", [])
    }

def generate_intermediate_json(cwd: Path, profile_key: str = None, target_tags: list = None) -> Path:
    """Locates master JSON, runs filtering, and writes resume_data.json to CWD."""
    master_path = cwd / "master_resume.json"
    if not master_path.exists():
        master_path = DATA_DIR / "master_resume.json"

    if not master_path.exists():
        print(f"❌ Error: `master_resume.json` not found in `{cwd}` or `{DATA_DIR}`.", file=sys.stderr)
        sys.exit(1)

    print(f"🔍 Processing Master Schema: `{master_path.name}`")
    if profile_key:
        print(f"🎯 Target Profile        : `{profile_key}`")
    if target_tags:
        print(f"🏷️  Target Tags           : {target_tags}")

    filtered_data = filter_master_resume(master_path, profile_key, target_tags)
    output_path = cwd / "resume_data.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(filtered_data, f, indent=2)

    print(f"📝 Intermediate file generated: `{output_path}` (Ready for inspection)\n")
    return output_path

def compile_documents():
    cwd = Path.cwd()
    print("🚀 Initiating Branded Document Generation Pipeline...")
    print(f"📂 Templates Dir: {SCRIPT_DIR}")
    print(f"📂 Working Dir  : {cwd}\n")

    # Ensure required job JSON files exist in working directory
    resume_json = cwd / "resume_data.json"
    letter_json = cwd / "letter_data.json"

    if not resume_json.exists():
        print(f"❌ Error: Required `{resume_json.name}` missing in `{cwd}`.", file=sys.stderr)
        sys.exit(1)

    # Copy signature into working directory temporarily if needed by templates
    temp_sig_path = cwd / "sig-jon.png"
    sig_copied = False
    
    if SIGNATURE_SOURCE.exists() and not temp_sig_path.exists():
        shutil.copy2(SIGNATURE_SOURCE, temp_sig_path)
        sig_copied = True

    try:
        for template_name, output_name in TARGETS:
            source_template = SCRIPT_DIR / template_name
            if not source_template.exists():
                print(f"⚠️ Warning: Template `{template_name}` not found in `{SCRIPT_DIR}`.")
                continue

            # Skip cover letter compilation if letter_data.json isn't provided
            if template_name == "letter.typ" and not letter_json.exists():
                print(f"ℹ️ Skipping `{template_name}` (no `letter_data.json` in CWD).")
                continue

            # Copy template into CWD so Typst evaluates relative imports against CWD
            cwd_template_path = cwd / template_name
            output_path = cwd / output_name
            
            print(f"⚡ Compiling target: {template_name} -> {output_name}")
            try:
                shutil.copy2(source_template, cwd_template_path)
                typst.compile(str(cwd_template_path), output=str(output_path))
                print(f"🎉 Success! Generated `{output_name}`")
            except Exception as e:
                print(f"❌ Error compiling {template_name}:\n{e}", file=sys.stderr)
            finally:
                if cwd_template_path.exists():
                    cwd_template_path.unlink()
                    
    finally:
        if sig_copied and temp_sig_path.exists():
            temp_sig_path.unlink()

if __name__ == "__main__":
    cwd = Path.cwd()

    # Step 1: Ensure control config exists in CWD (creates template if missing)
    config = ensure_control_config(cwd)
    profile_key = config.get("profile")
    target_tags = config.get("tags")
    inspect_only = config.get("inspect_only", False)

    # Step 2: Filter master and output intermediate resume_data.json in CWD
    generate_intermediate_json(cwd, profile_key=profile_key, target_tags=target_tags)

    # Step 3: Compile documents unless inspect_only is set to true in config
    if not inspect_only:
        compile_documents()
    else:
        print("⏸️  `inspect_only` is set to true in `build_config.json`. Skipping PDF compilation.")