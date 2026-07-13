#!/usr/bin/env python3
"""
PDF Generation Engine for Executive Technical Profile
Uses WeasyPrint to compile modern HTML/CSS with system-native @media print overrides.

Prerequisites:
    1. Install Python package:
       pip install weasyprint

    2. System-level PDF rendering engines (Required by WeasyPrint for font/layout compiling):
       - macOS:   brew install pango libffi
       - Ubuntu:  sudo apt-get install python3-pip python3-cffi python3-brotli libpango-1.0-0 libharfbuzz0b libpangoft2-1.0-0
       - Windows: Install the GTK3 installer (https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer)
"""

import os
import sys
import glob
import argparse
from datetime import datetime
from weasyprint import HTML, CSS

def select_html_file():
    """
    Scans the current directory for HTML files and presents an interactive menu
    allowing the user to select which file to compile.
    """
    html_files = glob.glob("*.html")
    
    if not html_files:
        print("\n[!] Error: No HTML files found in the current directory.")
        print("[*] Please make sure your HTML profile is saved in the same folder as this script.")
        sys.exit(1)
        
    if len(html_files) == 1:
        print(f"[*] Found 1 HTML file: '{html_files[0]}'")
        return html_files[0]
        
    print("\nAvailable HTML files in this folder:")
    for idx, filename in enumerate(html_files, 1):
        print(f"  [{idx}] {filename}")
        
    while True:
        try:
            choice = input(f"\nSelect a file to convert (1-{len(html_files)}) [Default: 1]: ").strip()
            if not choice:
                return html_files[0]
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(html_files):
                return html_files[choice_idx]
            else:
                print(f"[!] Please enter a number between 1 and {len(html_files)}.")
        except ValueError:
            print("[!] Invalid input. Please enter a valid menu number.")

def generate_profile_pdf(html_path, output_path):
    """
    Loads the selected HTML portfolio and compiles it into an elegant, highly polished executive PDF.
    Dynamically injects print-specific layout scaling and defensive page-breaking rules.
    """
    if not os.path.exists(html_path):
        print(f"[!] Error: Target HTML file '{html_path}' not found.")
        sys.exit(1)

    print(f"\n[*] Initializing compilation of '{html_path}'...")
    
    try:
        # Initialize the HTML engine with the source file
        html_document = HTML(filename=html_path)
        
        print("[*] Generating dynamic paged-media layouts, footers, and page-break overrides...")
        
        # Inject print rule micro-overrides to optimize pagination and eliminate awkward blank spaces
        print_overrides = CSS(string="""
            @page {
                size: A4;
                /* Balanced margin configuration to increase vertical room while maintaining a premium feel */
                margin: 18mm 20mm 22mm 20mm;
                
                @bottom-right {
                    content: "Page " counter(page) " of " counter(pages);
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                    font-size: 7.5pt;
                    color: #64748b;
                }
                @bottom-left {
                    content: "Jon Morgan • Technical Director (Built Environment & Digital Integration)";
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                    font-size: 7.5pt;
                    color: #64748b;
                }
            }
            
            /* Global Scale: Lifted font size slightly for much-improved physical legibility */
            body {
                font-size: 9.6pt !important;
                line-height: 1.35 !important;
            }
            
            h1 {
                font-size: 21pt !important;
                margin-bottom: 6px !important;
            }
            
            .title-sub {
                font-size: 11.5pt !important;
                margin-bottom: 2px !important;
                
            }
            
            .contact-bar {
                font-size: 8.8pt !important;
            }
            
            .thesis-box {
                padding: 15px !important;
                margin-bottom: 20px !important;
                font-size: 10pt !important;
                line-height: 1.4 !important;
            }
            
            h2 {
                font-size: 12pt !important;
                margin-top: 24px !important;
                margin-bottom: 10px !important;
                padding-bottom: 4px !important;
                break-after: avoid-page !important;
                page-break-after: avoid !important;
            }
            
            h2::before {
                height: 14px !important;
                width: 3px !important;
                margin-right: 8px !important;
            }
            
            /* Defensive Page-Breaking: Strictly prevent orphan headers */
            h1, h2, h3, h4, .timeline-header, .role-title {
                break-after: avoid-page !important;
                page-break-after: avoid !important;
            }
            
            /* Granular Page-Breaking Rules:
               Instead of preventing breaks within entire blocks or entire lists (which causes large voids),
               we allow the lists to break across pages but keep individual bullet points unbroken. */
            .timeline-item {
                break-inside: auto !important;
                page-break-inside: auto !important;
                margin-bottom: 16px !important;
            }
            
            ul {
                break-inside: auto !important;
                page-break-inside: auto !important;
                margin-top: 4px !important;
            }
            
            li {
                break-inside: avoid !important;
                page-break-inside: avoid !important;
                margin-bottom: 3px !important;
            }
            
            p {
                margin-top: 0 !important;
                margin-bottom: 8px !important;
                orphans: 3;
                widows: 3;
            }
            
            .contact-footer {
                margin-top: 25px !important;
                padding-top: 15px !important;
            }
        """)
        
        print("[*] Parsing CSS variables and compiling document...")
        
        # Compile and write directly to the target PDF destination
        html_document.write_pdf(
            target=output_path,
            presentational_hints=True,
            stylesheets=[print_overrides]
        )
        
        print(f"\n[✓] Success! PDF compiled flawlessly.")
        print(f"[✓] Output written to: {os.path.abspath(output_path)}\n")
        
    except Exception as e:
        print(f"\n[!] Compilation failed: {str(e)}")
        print("[!] Ensure system-level dependencies (Pango/GTK) are correctly installed on your OS.")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compile modern HTML portfolio or cover letter to high-contrast PDF.")
    parser.add_argument(
        "-i", "--input", 
        default=None, 
        help="Path to source HTML file (If omitted, script will launch interactive menu)"
    )
    parser.add_argument(
        "-o", "--output", 
        default=None, 
        help="Path to destination PDF file (If omitted, a name will be suggested dynamically based on the input filename)"
    )
    
    args = parser.parse_args()
    
    # Resolve target HTML file
    target_html = args.input
    if target_html is None:
        target_html = select_html_file()
        
    # Generate a dynamic default filename incorporating the formatted short month and year (e.g. Jun_2026)
    short_month_year = datetime.now().strftime("%b_%Y")
    html_basename = os.path.basename(target_html).lower()
    
    if "resume" in html_basename:
        default_pdf_name = f"Jon_Morgan_Resume_{short_month_year}.pdf"
    elif "letter" in html_basename:
        default_pdf_name = f"Jon_Morgan_Cover_Letter_{short_month_year}.pdf"
    else:
        # Fallback incorporating the original HTML name
        clean_html_name = os.path.splitext(os.path.basename(target_html))[0].replace(" ", "_")
        default_pdf_name = f"Jon_Morgan_{clean_html_name}_{short_month_year}.pdf"
        
    # Resolve target PDF output filename
    if args.output is None:
        # If the user ran without CLI arguments, let them confirm or rename the dynamically resolved default
        user_pdf_name = input(f"Output filename [Default: {default_pdf_name}]: ").strip()
        if user_pdf_name:
            if not user_pdf_name.lower().endswith(".pdf"):
                user_pdf_name += ".pdf"
            target_pdf = user_pdf_name
        else:
            target_pdf = default_pdf_name
    else:
        target_pdf = args.output
        if not target_pdf.lower().endswith(".pdf"):
            target_pdf += ".pdf"
            
    generate_profile_pdf(target_html, target_pdf)