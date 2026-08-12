#!/usr/bin/env python3
"""
Executive Cover Letter Generator
Converts JSON structure (from Canvas) to beautifully typeset WeasyPrint PDF.
Handles markdown bold conversion (**text** -> <strong>text</strong>) automatically.
Can be executed from any directory; looks for cover_letter.json in the current working directory.
"""

import os
import json
import re
import copy
from pathlib import Path

# Try importing required template and printing dependencies
try:
    from jinja2 import Environment, FileSystemLoader
except ImportError:
    print("Error: 'jinja2' is required. Run 'uv pip install jinja2' or 'pip install jinja2'")
    exit(1)

try:
    from weasyprint import HTML
except ImportError:
    print("Error: 'weasyprint' is required. Run 'uv pip install weasyprint' or 'pip install weasyprint'")
    exit(1)

# Absolute Repo Paths (for assets and templates)
REPO_ROOT_DIR = Path(__file__).resolve().parents[2]
TEMPLATE_DIR = REPO_ROOT_DIR / "src" / "templates"
TEMPLATE_FILE = "cover_letter_template.html"
SIGNATURE_FILE = REPO_ROOT_DIR / "src" / "sig-jon.png"

# Runtime Environment Paths (for input JSON and output PDF)
CURRENT_RUN_DIR = Path.cwd()
JSON_FILE = CURRENT_RUN_DIR / "cover_letter.json"
OUTPUT_PDF = CURRENT_RUN_DIR / "cover_letter.pdf"

# Robust default data structure containing embedded personal details for Jon Morgan.
# This ensures that even if local JSONs lack contact info or structural keys,
# compilation never fails with an UndefinedError.
DEFAULT_DATA = {
    "meta": {
        "candidate": {
            "name": "Jon Morgan",
            "phone": "+61 429 357 751",
            "email": "jonmorgan@fastmail.com",
            "linkedin": "linkedin.com/in/linkjonmorgan"
        },
        "recipient": {
            "organization": "Propel Ventures",
            "partner_agency": "Buddy Advisory",
            "location": "Melbourne, VIC",
            "date": "July 1, 2026"
        },
        "application_details": {
            "target_role": "AI Enablement Lead",
            "subject_line": "RE: Application for AI Enablement Lead"
        }
    },
    "sections": {
        "executive_pivot": {
            "content": ""
        },
        "strategic_pillars": []
    },
    "organizational_alignment": {
        "content": ""
    },
    "action_oriented_close": {
        "content": ""
    },
    "sign_off": {
        "salutation": "Sincerely,",
        "signature": "Jon Morgan"
    }
}


def md_bold_to_html(text: str) -> str:
    """Helper to convert Markdown bold tags (**word**) to HTML strong tags."""
    if not isinstance(text, str):
        return text
    return re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", text)


def process_markdown_fields(data: dict) -> dict:
    """Recursively walks the JSON-derived dictionary to process markdown bold text."""
    if isinstance(data, dict):
        return {k: process_markdown_fields(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [process_markdown_fields(item) for item in data]
    elif isinstance(data, str):
        return md_bold_to_html(data)
    return data


def strip_placeholders(data):
    """Recursively removes keys containing '[YOUR ...]' placeholders so deep_merge falls back to defaults."""
    if isinstance(data, dict):
        clean_dict = {}
        for k, v in data.items():
            if isinstance(v, (dict, list)):
                clean_dict[k] = strip_placeholders(v)
            elif isinstance(v, str):
                # Check if the string contains placeholder formatting like [YOUR NAME] or matches a bracketed format
                if not re.search(r'\[YOUR\s+.*?\]', v, re.IGNORECASE) and v.strip() != "":
                    clean_dict[k] = v
            else:
                clean_dict[k] = v
        return clean_dict
    elif isinstance(data, list):
        return [strip_placeholders(item) for item in data]
    return data


def deep_merge(dict1: dict, dict2: dict) -> dict:
    """Recursively merges dict2 into dict1 in place, supporting nested dictionaries."""
    for k, v in dict2.items():
        if k in dict1 and isinstance(dict1[k], dict) and isinstance(v, dict):
            deep_merge(dict1[k], v)
        else:
            dict1[k] = v
    return dict1


def generate_pdf():
    print("🚀 Initiating Executive Cover Letter compilation pipeline...")
    print(f"📁 Target Working Directory: {CURRENT_RUN_DIR}")

    # 1. Load the JSON state from the Current Working Directory
    if not JSON_FILE.exists():
        print(f"❌ Error: Source JSON file not found at: {JSON_FILE}")
        print("Please ensure you are running the script from a directory containing 'cover_letter.json'.")
        return

    with open(JSON_FILE, "r", encoding="utf-8") as f:
        try:
            raw_data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing JSON file: {e}")
            return

    # 2. Strip standard '[YOUR NAME]' placeholder tokens from raw_data
    # This ensures the deep merge fallback pipeline functions as intended
    sanitized_raw_data = strip_placeholders(raw_data)

    # 3. Preprocess JSON values to support Markdown styling (like bold text)
    processed_raw_data = process_markdown_fields(sanitized_raw_data)

    # 4. Create a master state by deep-merging user data on top of robust defaults
    # This prevents any Jinja2 UndefinedError if fields are omitted in the JSON
    processed_data = copy.deepcopy(DEFAULT_DATA)
    processed_data = deep_merge(processed_data, processed_raw_data)

    # 5. Handle signature existence configuration
    sig_exists = SIGNATURE_FILE.exists()
    processed_data["signature_path_exists"] = sig_exists
    processed_data["signature_path"] = str(SIGNATURE_FILE.resolve()) if sig_exists else ""

    if sig_exists:
        print(f"✍ *Signature asset found in repo: {SIGNATURE_FILE.name}")
    else:
        print(f"⚠️ Warning: Signature asset missing from repo path: {SIGNATURE_FILE}. Leaving clean spacing instead.")

    # 6. Initialize Jinja2 Environment
    if not (TEMPLATE_DIR / TEMPLATE_FILE).exists():
        print(f"❌ Error: HTML template missing from: {TEMPLATE_DIR / TEMPLATE_FILE}")
        return

    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
    template = env.get_template(TEMPLATE_FILE)

    # 7. Render Template Context safely
    print("🎨 Rendering HTML template with Jinja2 engine...")
    try:
        html_content = template.render(**processed_data)
    except Exception as e:
        print(f"❌ Templating Error: {str(e)}")
        return

    # Write temporary build file to the repo directory for compilation to keep current directory clean
    temp_html_path = REPO_ROOT_DIR / "cover_letter_build.html"
    with open(temp_html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    # 8. Compile via WeasyPrint API into the Current Working Directory
    print(f"📄 Compiling output to high-fidelity PDF with WeasyPrint...")
    try:
        HTML(filename=str(temp_html_path)).write_pdf(target=str(OUTPUT_PDF))
        print(f"✨ Success! Your executive cover letter has been compiled to: {OUTPUT_PDF}")
    except Exception as e:
        print(f"❌ Error generating PDF: {str(e)}")
    finally:
        # Clean up intermediate artifact from the repo root
        if temp_html_path.exists():
            os.remove(temp_html_path)


if __name__ == "__main__":
    generate_pdf()