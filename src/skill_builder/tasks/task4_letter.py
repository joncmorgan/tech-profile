# ==============================================================================
# MODULE:  src.tasks.task4_letter
# VERSION: 2.4.0
# STATUS:  Airtight Prompt-Decoupled Cover Letter Engine
# ==============================================================================

import time
import ollama
from typing import Dict, Any
from src.paths import load_prompt_blueprint

def run_tailor_letter(context: Dict[str, Any], model_name: str) -> str:
    print(f"\n✉️  [{time.strftime('%H:%M:%S')}] [Task 4/5] Drafting realistic cover letter prose via LLM...")
    
    analysis_brief = context.get("strategic_analysis", {}).get("value_proposition", "")
    work_history = context.get("work_history", [])
    
    # Process dynamic context mappings
    experience_summary = []
    for job in work_history[:2]:
        experience_summary.append(
            f"COMPANY: {job.get('company')}\n"
            f"TITLE: {job.get('title')}\n"
            f"REAL ROLES & COMPLETED EXPERIENCES:\n{job.get('memories')}"
        )
    recent_experience_context = "\n\n---\n\n".join(experience_summary)

    # Hydrate decoupled external file assets using native python keyword parameters
    system_instruction = load_prompt_blueprint("task4_letter_system.txt").format(
        analysis_brief=analysis_brief
    )
    prompt = load_prompt_blueprint("task4_letter_user.txt").format(
        recent_experience_context=recent_experience_context
    )
    
    try:
        response = ollama.generate(
            model=model_name,
            system=system_instruction,
            prompt=prompt,
            options={"temperature": 0.1}
        )
        
        output_text = response.get("response", "").strip()
        
        if "<think>" in output_text:
            output_text = output_text.split("</think>")[-1].strip()
            
        if "<letter_body>" in output_text and "</letter_body>" in output_text:
            return output_text.split("<letter_body>")[-1].split("</letter_body>")[0].strip()
            
        return "\n".join([line for line in output_text.splitlines() if not line.strip().startswith(("---", "###", "Certainly"))]).strip()
        
    except Exception as e:
        print(f"   ❌ LLM prompt blueprint execution failed: {e}")
        return "I am writing to express my strong interest in joining your infrastructure team..."