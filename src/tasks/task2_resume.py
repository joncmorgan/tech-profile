# src/tasks/task2_resume.py
import sys
import time
import ollama
from typing import Dict, Any

def run_tailor_resume(context: Dict[str, Any], model_name: str) -> Dict[str, str]:
    print(f"\n🤖 [{time.strftime('%H:%M:%S')}] [Task 2/4] Initializing Career Tailoring Engine...")
    
    prompt_base = f"""
    TARGET ROLE: {context['target_description']}
    ORG INFO: {context['target_organization']}
    HISTORY: {context['work_history']}
    SKILLS: {context['core_skills']}
    """
    
    # --- SUB-TASK A: Summary Generation ---
    print(f"⏳ [{time.strftime('%H:%M:%S')}] A. Requesting Executive Summary & Core Skills matching...")
    start_time = time.time()
    
    response_stream = ollama.chat(
        model=model_name, 
        messages=[
            {"role": "system", "content": "You are a staff technical resume writer. Write a factual 3-sentence executive summary paragraph matching the background to the target job description. Do not embellish."},
            {"role": "user", "content": prompt_base}
        ],
        stream=True
    )
    
    basics_content = ""
    for chunk in response_stream:
        text = chunk["message"]["content"]
        basics_content += text
        sys.stdout.write(text)
        sys.stdout.flush()
    
    print(f"\n✅ Finished Summary Pass (Took {time.time() - start_time:.2f}s)\n")

    # --- SUB-TASK B: History Bullets Generation ---
    print(f"⏳ [{time.strftime('%H:%M:%S')}] B. Tailoring Career History Bullet Points (3-4 high-impact items per role)...")
    start_time = time.time()
    
    response_stream_bullets = ollama.chat(
        model=model_name, 
        messages=[
            {"role": "system", "content": "Review the history. For each job, produce exactly 3 to 4 high-impact bullet points focusing on metrics and engineering outcomes matching the target role requirements."},
            {"role": "user", "content": prompt_base}
        ],
        stream=True
    )
    
    bullets_content = ""
    for chunk in response_stream_bullets:
        text = chunk["message"]["content"]
        bullets_content += text
        sys.stdout.write(text)
        sys.stdout.flush()
        
    print(f"\n✅ Finished Bullets Pass (Took {time.time() - start_time:.2f}s)\n")
    
    return {
        "summary_and_skills": basics_content.strip(),
        "history_bullets": bullets_content.strip()
    }