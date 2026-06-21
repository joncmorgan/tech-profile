# ==============================================================================
# JON MORGAN ADVISORY - PDF GENERATOR CORESCRIPT
# Version: 1.4.2 (Secure metadata stripping & absolute path sanitization release)
# Last Updated: June 2026
# ==============================================================================

import argparse
import sys
import secrets
from datetime import datetime, timezone
from pathlib import Path

import frontmatter
import markdown
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from pypdf import PdfReader, PdfWriter
from pypdf.constants import UserAccessPermissions

# Resolve static directories at the start of the script.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
TEMPLATES_DIR = PROJECT_ROOT / "src" / "templates"


def parse_and_validate_markdown(content_path):
    """
    Parses a markdown file and validates compliance parameters inside the YAML frontmatter.
    Returns parsed metadata dictionary and the markdown body text.
    """
    with open(content_path, 'r', encoding='utf-8') as f:
        raw_content = f.read()

    try:
        post = frontmatter.loads(raw_content)
        metadata = post.metadata
        content = post.content
    except Exception as e:
        print(f"Error parsing YAML frontmatter: {e}", file=sys.stderr)
        sys.exit(1)

    # 1. Verification Key Validation
    compiler_key = metadata.get('compiler')
    if not compiler_key or str(compiler_key).strip().lower() != 'jonmorgan':
        print("\n[Validation Error] Compilation halted.", file=sys.stderr)
        print("This document does not contain the required verification identifier key.", file=sys.stderr)
        print("Please ensure your frontmatter contains:  compiler: jonmorgan\n", file=sys.stderr)
        sys.exit(1)

    # 2. Document Type Key Validation
    doc_type = metadata.get('document_type')
    if not doc_type:
        print("\n[Validation Error] Compilation halted.", file=sys.stderr)
        print("This document is missing the 'document_type' property in the frontmatter.", file=sys.stderr)
        print("Please ensure your frontmatter contains:  document_type: [memo|letter|report|etc]\n", file=sys.stderr)
        sys.exit(1)

    return metadata, content


def apply_pdf_security_and_metadata(pdf_path, metadata):
    """
    Reads the generated PDF, injects administrative metadata, completely clears 
    the Catalog-level XMP stream to eliminate hidden absolute local file system 
    path leaks, and applies a secure, empty-user-password print-only lock.
    """
    print(f"[{pdf_path.name}] Applying sanitized PDF metadata and secure permissions lock...")
    
    reader = PdfReader(pdf_path)
    writer = PdfWriter()
    
    for page in reader.pages:
        writer.add_page(page)

    # Generate a clean timestamp for creation and modification in compliant PDF format (D:YYYYMMDDHHmmSSZ)
    now = datetime.now(timezone.utc)
    date_str = now.strftime("D:%Y%m%d%H%M%S") + "Z"

    # Ingest PDF Document Metadata properties
    doc_title = metadata.get('subject', 'Specialist Advisory Memorandum')
    doc_author = metadata.get('from', 'Jon Morgan Advisory')
    
    # 1. Completely replace standard metadata dictionary (removes default/hidden tool-injected keys)
    writer.metadata = {
        "/Title": doc_title,
        "/Author": doc_author,
        "/Subject": "Specialist Engineering and Built Environment Advisory",
        "/Creator": "Jon Morgan",
        "/Producer": "Jon Morgan",
        "/CreationDate": date_str,
        "/ModDate": date_str,
    }

    # 2. Force-purge Catalog-level XMP Metadata streams (which house WeasyPrint's base_url path leakages)
    try:
        writer.xmp_metadata = None
    except Exception:
        pass

    try:
        if "/Metadata" in writer.root_object:
            del writer.root_object["/Metadata"]
    except Exception:
        pass

    # Restrict modifications while allowing high-resolution printing, copy-paste extraction, and accessibility
    # Compute permission bits: Print (4) + Copy/Extract (16) + Accessibility (512) + High-Res Print (2048) = 2580
    try:
        permissions = (
            UserAccessPermissions.PRINT
            | UserAccessPermissions.EXTRACT
            | UserAccessPermissions.EXTRACT_TEXT_AND_GRAPHICS
            | UserAccessPermissions.PRINT_TO_REPRESENTATION
        )
    except AttributeError:
        # Fallback to direct bitmask if pypdf constant mapping varies in older installations
        permissions = 2580

    # Generate a strong, secure random owner password to secure the access control list
    owner_pwd = secrets.token_hex(32)

    writer.encrypt(
        user_password="",        # Empty user password means the reader opens instantly
        owner_password=owner_pwd,  # Restricts modifications unless owner password is supplied
        permissions_flag=permissions
    )

    # Overwrite the unencrypted PDF in-place with the secure variant
    with open(pdf_path, "wb") as f:
        writer.write(f)


def compile_document(content_path):
    """
    Loads markdown and metadata, dynamically selects the HTML template, 
    converts to print-ready HTML, compiles PDF, and applies metadata and security locks.
    """
    content_path = Path(content_path).resolve()
    output_path = content_path.with_suffix('.pdf')

    print(f"[{content_path.name}] Reading and validating document structure...")
    metadata, markdown_prose = parse_and_validate_markdown(content_path)
    
    doc_type = str(metadata.get('document_type')).strip().lower()
    print(f"[{content_path.name}] Verification Key: Verified ('compiler: jonmorgan')")
    print(f"[{content_path.name}] Document Type: '{doc_type}' detected")

    print(f"[{content_path.name}] Converting Markdown prose to semantic HTML...")
    html_body = markdown.markdown(markdown_prose, extensions=['extra', 'nl2br'])

    # Route to the appropriate document template
    template_file = TEMPLATES_DIR / f"{doc_type}.html"
    
    if not template_file.exists():
        fallback_template = TEMPLATES_DIR / "memo.html"
        print(f"[{content_path.name}] Warning: Custom template '{template_file.name}' not found.")
        print(f"[{content_path.name}] Falling back to standard layout: '{fallback_template.name}'")
        template_file = fallback_template
        
        if not template_file.exists():
            print(f"Error: Standard template not found at {fallback_template}", file=sys.stderr)
            sys.exit(1)
    else:
        print(f"[{content_path.name}] Routing template: Using '{template_file.name}'")

    # Setup Jinja2 and render HTML
    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))
    template = env.get_template(template_file.name)
    rendered_html = template.render(meta=metadata, content=html_body)

    # Generate PDF in-place (same directory as input markdown file) using absolute file URI references
    print(f"[{content_path.name}] Compiling high-end PDF via WeasyPrint...")
    HTML(string=rendered_html, base_url=TEMPLATES_DIR.as_uri()).write_pdf(str(output_path))
    
    # Apply standard metadata injection and security permissions lock
    try:
        apply_pdf_security_and_metadata(output_path, metadata)
    except Exception as e:
        print(f"[{content_path.name}] Warning: Could not apply security/metadata lock: {e}", file=sys.stderr)

    print(f"\nSuccess! Secure PDF compiled cleanly in-place to:")
    print(f"-> {output_path}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Compile a compliant advisory Markdown file into an in-place secure PDF."
    )
    parser.add_argument(
        "input_file",
        help="Path to the input Markdown (.md) document to compile."
    )

    args = parser.parse_args()
    input_file = Path(args.input_file).resolve()

    if not input_file.exists():
        print(f"Error: Input file not found at: {input_file}", file=sys.stderr)
        sys.exit(1)

    try:
        compile_document(input_file)
    except Exception as e:
        print(f"Compilation failed with error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()