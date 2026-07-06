import json
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

def build_resume():
    # Absolute Repo Paths (for assets and templates)
    REPO_ROOT_DIR = Path(__file__).resolve().parents[2]
    TEMPLATE_DIR = REPO_ROOT_DIR / "src" / "templates"
    TEMPLATE_FILE = "resume_template.html"
    
    # Active Working Directory Paths (for local data and generated outputs)
    WORKING_DIR = Path.cwd()
    DATA_FILE = WORKING_DIR / "resume.json"
    OUTPUT_HTML = WORKING_DIR / "resume.html"
    OUTPUT_PDF = WORKING_DIR / "resume.pdf"

    # Dependencies Guard Checks
    if not DATA_FILE.exists():
        print(f"Error: Local data file not found at: '{DATA_FILE}'")
        return
    if not (TEMPLATE_DIR / TEMPLATE_FILE).exists():
        print(f"Error: Repository template structure not found at: '{TEMPLATE_DIR / TEMPLATE_FILE}'")
        return

    # Load JSON Dataset from the active working directory
    print(f"Parsing local dataset from working directory: {DATA_FILE}")
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        resume_data = json.load(f)

    # Initialize Jinja Template Compiler pointed at the repo template folder
    print(f"Loading template engine from repository directory: {TEMPLATE_DIR}")
    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
    template = env.get_template(TEMPLATE_FILE)

    # Generate layout markup
    print("Compiling data parameters and styling structures into static HTML code...")
    rendered_html = template.render(data=resume_data)

    # Output HTML asset to the active working directory
    print(f"Emitting static layout preview file: {OUTPUT_HTML}")
    with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
        f.write(rendered_html)

    # Compile into standard printed format using WeasyPrint matching @media print rules
    print(f"Compiling document into high-fidelity PDF asset: {OUTPUT_PDF}")
    try:
        HTML(filename=str(OUTPUT_HTML)).write_pdf(str(OUTPUT_PDF))
        print("Success! Both 'resume.html' and 'resume.pdf' are successfully created locally.")
    except Exception as e:
        print(f"Fatal PDF Generation Error: {e}")

if __name__ == '__main__':
    build_resume()