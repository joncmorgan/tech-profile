# src/tasks/task1_ingest.py
import json
from pathlib import Path
from typing import Dict, Any

def run_ingest(base_dir: Path, target_dir: Path, data_dir: Path) -> Dict[str, Any]:
    print("📥 [Task 1/4] Aggregating distributed work memories, job targets, and identity info...")
    
    # 1. Harvest work history (reversing alphabetical index for reverse-chronological layout)
    history_path = data_dir / "experience"
    job_records = []
    
    if history_path.exists():
        job_folders = sorted([f for f in history_path.iterdir() if f.is_dir()], key=lambda x: x.name)
        job_folders.reverse() 
        
        for folder in job_folders:
            meta_file = folder / "meta.json"
            if not meta_file.exists():
                continue
            with open(meta_file, "r", encoding="utf-8") as f:
                meta = json.load(f)
            
            memories = [md.read_text(encoding="utf-8") for md in folder.glob("*.md")]
            meta["memories"] = "\n\n".join(memories)
            job_records.append(meta)

    # 2. Load target specs and data files
    desc_file = target_dir / "description.txt"
    org_file = target_dir / "organization.txt"
    edu_file = data_dir / "education.json"
    skills_file = data_dir / "core_skills.json"
    personal_file = data_dir / "personal_details.json" # New path
    
    return {
        "target_description": desc_file.read_text(encoding="utf-8").strip() if desc_file.exists() else "",
        "target_organization": org_file.read_text(encoding="utf-8").strip() if org_file.exists() else "",
        "work_history": job_records,
        "education": json.loads(edu_file.read_text(encoding="utf-8")) if edu_file.exists() else [],
        "core_skills": json.loads(skills_file.read_text(encoding="utf-8")) if skills_file.exists() else {},
        "personal": json.loads(personal_file.read_text(encoding="utf-8")) if personal_file.exists() else {} # Injected
    }