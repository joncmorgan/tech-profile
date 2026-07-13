# ==============================================================================
# MODULE:  src.tasks.task5_compile
# VERSION: 5.1.1
# STATUS:  Production-Grade Hardened Compilation Target - Root Data Path Aligned
# ==============================================================================

import json
import typst
from pathlib import Path
from typing import Dict, Any, List
from src.paths import TEMPLATE_DIR

def compile_resume(output_dir: Path, resume_data: Dict[str, Any], education_data: List[Dict[str, Any]]):
    print(f"   📊 Hydrating resume layout blueprint fields from multi-pass schema...")
    
    # 💡 REPO ROOT ALIGNMENT FIX: Resolve the true root-level data folder location
    # TEMPLATE_DIR is typically 'my_repo/data/templates', so its grandparent is 'my_repo/'
    repo_root = TEMPLATE_DIR.parent.parent
    personal_file = repo_root / "data" / "personal_details.json"
    
    personal = {}
    if personal_file.exists():
        try:
            personal = json.loads(personal_file.read_text(encoding="utf-8"))
            print(f"      👤 Loaded personal contact data on-demand from '{personal_file}'")
        except Exception as e:
            print(f"      ⚠️ Warning: Could not parse personal details JSON: {e}")
    else:
        print(f"      ⚠️ Warning: '{personal_file}' not found at repo root. Using template defaults.")

    # 1. Extract Profile Data Structs
    profile_block = resume_data.get("profile", {})
    profile_summary = profile_block.get("headline", "")
    
    core_strengths = profile_block.get("core_strengths", [])
    if core_strengths:
        strengths_bullets = "\n" + "\n".join([f"- {cs}" for cs in core_strengths])
        profile_summary += strengths_bullets

    # 2. Extract Recent Primary Experience (Heavy Hitters)
    recent_experience = resume_data.get("recent_experience", [])
    job1 = recent_experience[0] if len(recent_experience) > 0 else {}
    job2 = recent_experience[1] if len(recent_experience) > 1 else {}

    # 3. Extract and Process Older Context Lines Dynamically
    older_experience = resume_data.get("older_experience", [])
    collapsed_lines = []
    for old_job in older_experience:
        company = old_job.get("company", "")
        role = old_job.get("role", "")
        duration = old_job.get("duration", "")
        summary = old_job.get("summary", "")
        
        entry = f"- **{role}** | {company} ({duration}) \n  {summary}"
        collapsed_lines.append(entry)
    
    # 4. Extract and Process Education Dynamic Lines
    edu_lines = []
    for edu in education_data:
        degree = edu.get("degree", "")
        institution = edu.get("institution", "")
        year = edu.get("year", "")
        edu_lines.append(f"- **{degree}** – {institution}, {year}")

    # 5. Pack strict sys_inputs exactly as required by resume.typ layout
    inputs = {
        "name": personal.get("name", "Jon Morgan"),
        "contact": f"{personal.get('location', '')} | {personal.get('phone', '')} | {personal.get('email', '')} | {personal.get('linkedin', '')}",
        "profile_summary": profile_summary,
        
        "job1_title": job1.get("role", ""),
        "job1_company": job1.get("company", ""),
        "job1_dates": job1.get("duration", ""),
        "job1_context": "Core Technical Achievements & Strategic Scale Delivery:",
        "job1_bullets": json.dumps(job1.get("highlights", [])),
        
        "job2_title": job2.get("role", ""),
        "job2_company": job2.get("company", ""),
        "job2_dates": job2.get("duration", ""),
        "job2_context": "Core Technical Achievements & Strategic Scale Delivery:" if job2 else "",
        "job2_bullets": json.dumps(job2.get("highlights", [])),
        
        "collapsed_history": "\n".join(collapsed_lines) if collapsed_lines else "",
        "education_block": "\n".join(edu_lines) if edu_lines else ""
    }
    
    try:
        typst.compile(
            str(TEMPLATE_DIR / "resume.typ"), 
            output=str(output_dir / "resume.pdf"), 
            sys_inputs=inputs
        )
        print(f"      ✓ CV PDF Successfully Rendered: {output_dir / 'resume.pdf'}")
    except Exception as e:
        print(f"      ❌ Resume Typst Hydration Breakdown: {e}")

def run_compile_task(*args, **kwargs):
    """Hardened parameter matching engine parsing data payload structures."""
    context = {}
    output_dir = "output"

    for arg in args:
        if isinstance(arg, dict):
            context = arg
        elif isinstance(arg, (str, Path)):
            output_dir = str(arg)

    if "context" in kwargs: context = kwargs["context"]
    if "output_dir" in kwargs: output_dir = str(kwargs["output_dir"])

    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    
    # Dynamically read the multi-pass resume block payload safely
    tailored_resume_data = context.get("tailored_resume", {})
    education_records = tailored_resume_data.get("education_records", context.get("education", []))
    
    compile_resume(out_path, tailored_resume_data, education_records)