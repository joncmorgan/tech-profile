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
import argparse
from weasyprint import HTML, CSS

def generate_profile_pdf(html_path, output_path):
    """
    Loads the HTML portfolio and compiles it into an elegant, highly polished executive PDF.
    Dynamically injects print-specific layout scaling and defensive page-breaking rules.
    """
    if not os.path.exists(html_path):
        print(f"Error: Target HTML file '{html_path}' not found.")
        sys.exit(1)

    print(f"[*] Initializing compilation of {html_path}...")
    
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
                    content: "Jon Morgan • Technical Director";
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
        
        print(f"[✓] Success! PDF compiled flawlessly.")
        print(f"[✓] File written to: {os.path.abspath(output_path)}")
        
    except Exception as e:
        print(f"\n[!] Compilation failed: {str(e)}")
        print("[!] Ensure system-level dependencies (Pango/GTK) are correctly installed on your OS.")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compile modern HTML portfolio to high-contrast PDF.")
    parser.add_argument(
        "-i", "--input", 
        default="index.html", 
        help="Path to source HTML file (default: index.html)"
    )
    parser.add_argument(
        "-o", "--output", 
        default="Jon_Morgan_Technical_Profile.pdf", 
        help="Path to destination PDF file (default: Jon_Morgan_Technical_Profile.pdf)"
    )
    
    args = parser.parse_args()
    generate_profile_pdf(args.input, args.output)