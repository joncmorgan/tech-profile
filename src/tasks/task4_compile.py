# src/tasks/task4_compile.py
import json
import time
import typst
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

def markdown_to_typst(text: str) -> str:
    """Safely normalizes primary Markdown elements into Typst structures."""
    if not text:
        return ""
    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        # Convert markdown unordered lists '*' to Typst list items '-'
        if stripped.startswith("* ") or stripped.startswith("- "):
            line = f"- {stripped[2:]}"
        lines.append(line)
    return "\n".join(lines)

def run_compile_typst(output_dir: Path, context: Dict[str, Any], resume_data: Dict[str, str], letter_data: str):

    print(f"\n📝 [{time.strftime('%H:%M:%S')}] [Task 4/4] Processing text and hydrating Typst templates...")
    
    # Resolve file paths
    base_dir = Path(__file__).resolve().parent.parent.parent
    personal_file = base_dir / "data" / "personal_details.json"
    template_dir = base_dir / "data" / "templates"
    
    # 1. Fetch contact attributes from the static card
    personal = {}
    if personal_file.exists():
        with open(personal_file, "r", encoding="utf-8") as f:
            personal = json.load(f)
            
    name = personal.get("name", "Candidate")
    contact = f"{personal.get('location', '')} | {personal.get('phone', '')} | {personal.get('email', '')} | {personal.get('linkedin', '')}"
    current_date = datetime.today().strftime("%d %B %Y")
    
    # 2. Construct the entire experience section block right here in Python
    history_blocks = []
    for job in context.get("work_history", []):
        title = job.get("title", "")
        company = job.get("company", "")
        start = job.get("start_date", "")
        end = job.get("end_date", "")
        memories = job.get("memories", "")
        
        # Format the job header using clean native Typst syntax
        header = f"\n#v(8pt)\n*_{title}_* // {company} ({start} - {end})\n"
        
        # Clean up any potential markdown content formatting glitches
        formatted_memories = markdown_to_typst(memories)
        
        history_blocks.append(f"{header}\n{formatted_memories}")
        
    unified_history = "\n".join(history_blocks)
    
    # 3. Clean up the tailored LLM strings before handing them off
    clean_summary = markdown_to_typst(resume_data.get('summary_and_skills', ''))
    clean_letter_body = markdown_to_typst(letter_data)

    # 4. Map everything to the strict primitive input strings Typst requires
    inputs_resume = {
        "name": name,
        "contact": contact,
        "summary": clean_summary,
        "history": unified_history
    }
    
    inputs_letter = {
        "name": name,
        "contact": f"{personal.get('phone', '')} | {personal.get('email', '')} | {personal.get('linkedin', '')}",
        "date": current_date,
        "body": clean_letter_body
    }
    
    print(f"⚙️ [{time.strftime('%H:%M:%S')}] Rendering compiled templates using python-typst engine...")
    try:
        typst.compile(str(template_dir / "resume.typ"), output=str(output_dir / "resume.pdf"), sys_inputs=inputs_resume)
        print(f"   📊 PDF Successfully Rendered: {output_dir / 'resume.pdf'}")
        
        typst.compile(str(template_dir / "letter.typ"), output=str(output_dir / "cover_letter.pdf"), sys_inputs=inputs_letter)
        print(f"   ✉️  PDF Successfully Rendered: {output_dir / 'cover_letter.pdf'}")
        print("\n✨ All tasks finished successfully! Your tailored application is ready.")
    except Exception as e:
        print(f"❌ Python Typst Rendering Breakdown: {e}")