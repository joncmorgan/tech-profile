# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "jinja2",
#     "weasyprint",
#     "python-frontmatter",
#     "markdown",
# ]
# ///

#!/usr/bin/env python3
"""
Jon Morgan Advisory - PDF Document Generator (v1.3.0)
Compiles markdown files with structured YAML frontmatter (or lenient headers) 
and Jinja2 HTML templates into high-end, editorial PDFs using WeasyPrint.
Includes advanced debugging diagnostics.
"""

import os
import sys
import argparse
from pathlib import Path

__version__ = "1.3.0"

try:
    import frontmatter
except ImportError:
    print("[ERROR] 'python-frontmatter' is required. Run via 'uv run' to auto-install.", file=sys.stderr)
    sys.exit(1)

try:
    import markdown
except ImportError:
    print("[ERROR] 'markdown' is required. Run via 'uv run' to auto-install.", file=sys.stderr)
    sys.exit(1)

try:
    from jinja2 import Environment, FileSystemLoader
except ImportError:
    print("[ERROR] 'jinja2' is required. Run via 'uv run' to auto-install.", file=sys.stderr)
    sys.exit(1)

try:
    from weasyprint import HTML
except ImportError:
    print("[ERROR] 'weasyprint' is required. Run via 'uv run' to auto-install.", file=sys.stderr)
    print("Note: Weasyprint requires system-level libraries (Pango, Cairo, etc.).", file=sys.stderr)
    sys.exit(1)


def parse_markdown_document(content_path):
    """
    Parses a markdown file. Supports standard YAML frontmatter (enclosed by '---')
    and fallback/lenient key-value parsing at the top of the file.
    """
    print(f"[DEBUG] Opening file for reading: {content_path.resolve()}")
    with open(content_path, 'r', encoding='utf-8') as f:
        raw_content = f.read()

    print(f"[DEBUG] Raw file size: {len(raw_content)} characters.")

    # 1. Try parsing using standard frontmatter block (starts/ends with ---)
    try:
        print("[DEBUG] Attempting standard YAML frontmatter parsing via 'python-frontmatter'...")
        post = frontmatter.loads(raw_content)
        if post.metadata:
            print(f"[DEBUG] Standard parsing successful! Found metadata keys: {list(post.metadata.keys())}")
            # Ensure we strip leading/trailing whitespace from the parsed body
            body_text = post.content.strip()
            print(f"[DEBUG] Parsed body text length: {len(body_text)} characters.")
            return post.metadata, body_text
        else:
            print("[DEBUG] Standard parsing parsed successfully but found 0 metadata keys. Trying fallback.")
    except Exception as e:
        print(f"[DEBUG] Standard YAML frontmatter parsing failed or was skipped. Reason: {e}")

    # 2. Fallback Lenient Parsing: Read keys line-by-line until first content paragraph
    print("[DEBUG] Initiating fallback lenient key-value parser...")
    metadata = {}
    content_lines = []
    parsing_metadata = True

    for line in raw_content.splitlines():
        stripped = line.strip()
        if parsing_metadata:
            # Empty line indicates transition from metadata to body prose
            if not stripped:
                if metadata:
                    print(f"[DEBUG] Fallback parser found empty line: shifting from metadata to prose. Keys found: {list(metadata.keys())}")
                    parsing_metadata = False
                continue
            
            # Clean up potential markdown headings (e.g., "## to:" -> "to:")
            clean_line = stripped.lstrip('#').lstrip('*').lstrip('-').strip()
            if ':' in clean_line:
                key, val = clean_line.split(':', 1)
                key = key.strip().lower()
                # Accept typical alphabetic meta tags
                if key.isalnum() or '_' in key:
                    metadata[key] = val.strip()
                    continue
            
            # If any line doesn't match key-value criteria, wrap up metadata parsing
            print(f"[DEBUG] Fallback parser encountered non-metadata line, shifting to prose: '{stripped[:30]}...'")
            parsing_metadata = False

        content_lines.append(line)

    body_text = '\n'.join(content_lines).strip()
    print(f"[DEBUG] Fallback parser complete. Metadata keys: {list(metadata.keys())} | Body length: {len(body_text)} characters.")
    return metadata, body_text


def compile_document(content_path, template_path, output_path):
    """
    Loads markdown and metadata, converts to print-ready HTML, and compiles the PDF.
    """
    content_path = Path(content_path)
    template_path = Path(template_path)
    output_path = Path(output_path)

    # 1. Parse Markdown and Metadata
    print(f"\n--- [STEP 1: PARSING CONTENT] ---")
    metadata, markdown_prose = parse_markdown_document(content_path)

    if not metadata:
        print("[WARNING] No document metadata (to, from, subject, etc.) could be parsed from the file header!")
    else:
        print("[INFO] Final metadata resolved for rendering:")
        for k, v in metadata.items():
            print(f"  - {k}: {v}")

    if not markdown_prose:
        print("[ERROR] Resolved markdown prose content is completely EMPTY. Check your markdown file layout!")
    else:
        print(f"[INFO] First 150 characters of resolved markdown text:\n\"\"\"\n{markdown_prose[:150]}...\n\"\"\"")

    # 2. Convert Markdown body to structured HTML
    print(f"\n--- [STEP 2: CONVERTING MARKDOWN TO HTML] ---")
    # Using 'extra' extension for markdown tables, definitions, and footers
    html_body = markdown.markdown(markdown_prose, extensions=['extra', 'nl2br'])
    print(f"[INFO] Markdown converted to HTML successfully. Converted HTML length: {len(html_body)} characters.")
    print(f"[DEBUG] First 150 characters of converted HTML:\n\"\"\"\n{html_body[:150]}...\n\"\"\"")

    # 3. Setup Jinja2 and render final HTML
    print(f"\n--- [STEP 3: RENDERING JINJA2 TEMPLATE] ---")
    print(f"[DEBUG] Looking for templates folder at: {template_path.parent}")
    env = Environment(loader=FileSystemLoader(str(template_path.parent)))
    template = env.get_template(template_path.name)

    # Render template, passing both the metadata object and raw compiled body content
    print("[DEBUG] Intersecting metadata & body context into Jinja layout...")
    rendered_html = template.render(meta=metadata, content=html_body)
    print(f"[INFO] Rendered template HTML length: {len(rendered_html)} characters.")

    # 4. Generate the PDF output using WeasyPrint
    print(f"\n--- [STEP 4: COMPILING PDF VIA WEASYPRINT] ---")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"[INFO] Exporting static output file to: {output_path.resolve()}")
    # We pass the template directory as the base URL to resolve any relative assets
    HTML(string=rendered_html, base_url=str(template_path.parent)).write_pdf(str(output_path))
    print(f"[SUCCESS] PDF compiled cleanly! Check: {output_path.resolve()}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Compile structured Markdown and HTML templates into print-exact PDFs with extensive logging."
    )
    parser.add_argument(
        "--content", 
        default="content/memo.md",
        help="Path to the Markdown content file (default: content/memo.md)"
    )
    parser.add_argument(
        "--template", 
        default="src/templates/memo.html",
        help="Path to the HTML template (default: src/templates/memo.html)"
    )
    parser.add_argument(
        "--output", 
        default="output/memo_delivery.pdf",
        help="Path for the compiled output PDF (default: output/memo_delivery.pdf)"
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"generate_pdf.py v{__version__}"
    )

    args = parser.parse_args()

    # Align paths relative to project root directory (two folders up from src/scripts/generate_pdf.py)
    project_root = Path(__file__).resolve().parents[2]
    
    content_file = project_root / args.content
    template_file = project_root / args.template
    output_file = project_root / args.output

    print(f"==================================================")
    print(f" JON MORGAN ADVISORY - PDF GENERATOR v{__version__}")
    print(f"==================================================")
    print(f"[DEBUG] Project Root: {project_root.resolve()}")
    print(f"[DEBUG] Target Content: {content_file.resolve()}")
    print(f"[DEBUG] Target Template: {template_file.resolve()}")
    print(f"[DEBUG] Target Output: {output_file.resolve()}")

    if not content_file.exists():
        print(f"[ERROR] Content file not found at: {content_file.resolve()}", file=sys.stderr)
        sys.exit(1)
        
    if not template_file.exists():
        print(f"[ERROR] Template file not found at: {template_file.resolve()}", file=sys.stderr)
        sys.exit(1)

    try:
        compile_document(content_file, template_file, output_file)
    except Exception as e:
        print(f"[FATAL ERROR] Compilation failed: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()