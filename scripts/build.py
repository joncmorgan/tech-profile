import sys
import shutil
from pathlib import Path

try:
    import typst
except ImportError:
    print("❌ Error: The 'typst' Python package is not installed.\n👉 Run: uv add typst", file=sys.stderr)
    sys.exit(1)

# Paths where the source templates and assets live
SCRIPT_DIR = Path(__file__).parent.resolve()
SIGNATURE_NAME = "sig-jon.png"

TARGETS = [
    ("resume.typ", "jon_morgan_resume.pdf"),
    ("letter.typ", "jon_morgan_cover_letter.pdf")
]

def compile_documents():
    print("🚀 Initiating Branded Document Generation Pipeline...")
    cwd = Path.cwd()
    
    # Quick sanity check for local JSON files
    if not (cwd / "resume_data.json").exists() or not (cwd / "letter_data.json").exists():
        print(f"❌ Error: Required JSON data files not found in current directory ({cwd})", file=sys.stderr)
        sys.exit(1)
        
    # Copy the signature image into the job folder temporarily
    source_sig = SCRIPT_DIR / SIGNATURE_NAME
    temp_sig_path = cwd / SIGNATURE_NAME
    sig_copied = False
    
    try:
        if source_sig.exists():
            shutil.copy2(source_sig, temp_sig_path)
            sig_copied = True

        for template_name, output_name in TARGETS:
            source_template = SCRIPT_DIR / template_name
            if not source_template.exists():
                continue
                
            # Copy template to CWD next to the JSON files so paths match perfectly
            temp_template_path = cwd / f"__temp_{template_name}"
            output_path = cwd / output_name
            
            print(f"⚡ Compiling target: {template_name}...")
            try:
                shutil.copy2(source_template, temp_template_path)
                typst.compile(str(temp_template_path), output=str(output_path))
                print(f"🎉 Success! Generated: `{output_name}`")
            except Exception as e:
                print(f"❌ Error compiling {template_name}:\n{e}", file=sys.stderr)
            finally:
                if temp_template_path.exists():
                    temp_template_path.unlink()
                    
    finally:
        # Clean up the signature image out of your job directory
        if sig_copied and temp_sig_path.exists():
            temp_sig_path.unlink()

if __name__ == "__main__":
    compile_documents()