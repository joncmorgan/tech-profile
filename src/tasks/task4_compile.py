# src/tasks/task4_compile.py
import subprocess
import shutil
import time
from pathlib import Path
from typing import Dict, Any

def run_compile_typst(output_dir: Path, context: Dict[str, Any], resume_data: Dict[str, str], letter_data: str):
    print(f"\n📝 [{time.strftime('%H:%M:%S')}] [Task 4/4] Injecting personal tokens and writing Typst files...")
    
    personal = context.get("personal", {})
    name = personal.get("name", "Candidate")
    email = personal.get("email", "")
    phone = personal.get("phone", "")
    location = personal.get("location", "")
    linkedin = personal.get("linkedin", "")
    
    resume_path = output_dir / "resume.typ"
    letter_path = output_dir / "cover_letter.typ"
    
    # 1. Build Resume Markup File
    resume_typ = f"""
    #set page(paper: "a4", margin: (x: 2cm, y: 2.5cm))
    #set text(font: "Liberation Sans", size: 10pt)

    = {name}
    #text(size: 9pt, fill: gray)[{location} | {phone} | {email} | {linkedin}]
    #line(length: 100%, stroke: 0.5pt)

    == Executive Summary
    {resume_data['summary_and_skills']}

    == Professional Experience
    {resume_data['history_bullets']}
    """
    
    # 2. Build Cover Letter Markup File
    letter_typ = f"""
    #set page(paper: "a4", margin: (x: 2cm, y: 2.5cm))
    #set text(font: "Liberation Sans", size: 11pt)

    = {name}
    #text(size: 9pt, fill: gray)[{phone} | {email} | {linkedin}]
    #v(10pt)
    #align(right)[#datetime.today().display("[day] [month repr:long] [year]")]

    To the Hiring Team,

    #v(10pt)
    {letter_data}

    #v(20pt)
    Sincerely,\n
    {name}
    """
    
    resume_path.write_text(resume_typ.strip(), encoding="utf-8")
    letter_path.write_text(letter_typ.strip(), encoding="utf-8")
    
    # 3. Check for Local Typst System Compiler Binary
    if not shutil.which("typst"):
        print("⚠️ Typst compiler binary not detected in your system PATH.")
        print("💡 Install it on Linux via: 'sudo snap install typst' or download the binary directly.")
        return

    # 4. Trigger Automatic Compilation
    print(f"⚙️ [{time.strftime('%H:%M:%S')}] Triggering native Typst engine compiler rendering...")
    try:
        subprocess.run(["typst", "compile", str(resume_path)], check=True)
        print(f"   📊 PDF Generated: {resume_path.with_suffix('.pdf')}")
        
        subprocess.run(["typst", "compile", str(letter_path)], check=True)
        print(f"   ✉️  PDF Generated: {letter_path.with_suffix('.pdf')}")
        print("\n✨ All tasks finished successfully. Clean, pixel-perfect documents are ready!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Typst Compilation Breakdown: {e}")