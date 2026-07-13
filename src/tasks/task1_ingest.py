# ==============================================================================
# MODULE:  src.tasks.task1_ingest
# VERSION: 2.2.0
# STATUS:  Target Mandate & Distributed Experience Ingestion Engine (Clean Paths)
# ==============================================================================

import json
import time
from pathlib import Path
from typing import Dict, Any
from src.paths import PERSONAL_FILE

def run_ingest(data_dir: Path, target_dir: Path) -> Dict[str, Any]:
    print(f"📥 [{time.strftime('%H:%M:%S')}] [Task 1/5] Ingesting distributed work memories and local job specs...")
    
    # 1. Experience folders live inside data/experience/
    history_path = data_dir / "experience"
    job_records = []


    if history_path.exists():
        raw_folders = [f for f in history_path.iterdir() if f.is_dir()]
        
        for folder in raw_folders:
            meta_file = folder / "meta.json"
            if not meta_file.exists():
                continue
            with open(meta_file, "r", encoding="utf-8") as f:
                meta = json.load(f)
            
            memories = [md.read_text(encoding="utf-8") for md in folder.glob("*.md")]
            meta["memories"] = "\n\n".join(memories)
            
            # Inject robust fallbacks so the pipeline doesn't crash if keys are missing
            meta["strategic_priority"] = meta.get("strategic_priority", 99)
            meta["render_tier"] = meta.get("render_tier", "historical_context")
            
            job_records.append(meta)

        # Explicitly sort by strategic priority tier first, then chronologically if matching
        job_records.sort(key=lambda x: (x["strategic_priority"], x.get("start_date", "")))

    # if history_path.exists():
    #     job_folders = sorted([f for f in history_path.iterdir() if f.is_dir()], key=lambda x: x.name)
        
    #     for folder in job_folders:
    #         meta_file = folder / "meta.json"
    #         if not meta_file.exists():
    #             continue
    #         with open(meta_file, "r", encoding="utf-8") as f:
    #             meta = json.load(f)
            
    #         # Extract content strings from your memory_bank.md files
    #         memories = [md.read_text(encoding="utf-8") for md in folder.glob("*.md")]
    #         meta["memories"] = "\n\n".join(memories)
    #         job_records.append(meta)

    print(f"   📊 Collected {len(job_records)} career history records.")

    # 2. Extract static parameters using your exact tree positions
    edu_file = history_path / "education.json"
    skills_file = history_path / "core_skills.json"
    
    # 3. Harvest targets from the true workspace target folder (.target_job)
    desc_file = target_dir / "description.txt"
    org_file = target_dir / "organization.txt"
    recipient_file = target_dir / "recipient.json"
    
    recipient_data = {}
    if recipient_file.exists():
        try:
            recipient_data = json.loads(recipient_file.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"   ⚠️  Failed to parse recipient.json: {e}")

    return {
        "target_description": desc_file.read_text(encoding="utf-8").strip() if desc_file.exists() else "",
        "target_organization": org_file.read_text(encoding="utf-8").strip() if org_file.exists() else "",
        "target_recipient": recipient_data,
        "personal_info": json.loads(PERSONAL_FILE.read_text(encoding="utf-8")) if PERSONAL_FILE.exists() else {},
        "work_history": job_records,
        "education": json.loads(edu_file.read_text(encoding="utf-8")) if edu_file.exists() else [],
        "core_skills": json.loads(skills_file.read_text(encoding="utf-8")) if skills_file.exists() else {}
    }