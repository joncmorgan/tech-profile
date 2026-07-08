# src/tasks/task3_letter.py
import sys
import time
import ollama
from typing import Dict, Any

def run_tailor_letter(context: Dict[str, Any], model_name: str) -> str:
    print(f"🤖 [{time.strftime('%H:%M:%S')}] [Task 3/4] Initializing Cover Letter Generation...")
    
    prompt_base = f"""
    TARGET ROLE: {context['target_description']}
    COMPANY: {context['target_organization']}
    HISTORY: {context['work_history']}
    """
    
    start_time = time.time()
    response_stream = ollama.chat(
        model=model_name, 
        messages=[
            {"role": "system", "content": "Write a punchy, professional three-paragraph cover letter bridging the candidate's core engineering milestones to the company's stated organizational mission."},
            {"role": "user", "content": prompt_base}
        ],
        stream=True
    )
    
    letter_content = ""
    for chunk in response_stream:
        text = chunk["message"]["content"]
        letter_content += text
        sys.stdout.write(text)
        sys.stdout.flush()
        
    print(f"\n✅ Finished Cover Letter Pass (Took {time.time() - start_time:.2f}s)\n")
    return letter_content.strip()