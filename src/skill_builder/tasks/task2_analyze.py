# ==============================================================================
# MODULE:  src.tasks.task2_analyze
# VERSION: 3.0.0
# STATUS:  Bite-Sized Multi-Stage Deconstructed Analytical Core
# ==============================================================================

import json
import ollama
from typing import Dict, Any
from src.paths import load_prompt_blueprint

def extract_domain_brief(context: Dict[str, Any], model_name: str) -> str:
    """Stage 2a: Focuses purely on analyzing raw texts and drafting notes."""
    target_organization = context.get("target_organization", "")
    target_description = context.get("target_description", "")
    
    # Create an unconstrained prompt for raw note collection
    prompt = f"""
    You are a corporate strategy analyst. Review the following details.
    
    COMPANY PROFILE:
    {target_organization}
    
    JOB SPECIFICATION:
    {target_description}
    
    TASK:
    Draft a comprehensive raw notes brief detailing:
    1. What industry vertical do they operate in? (Pay close attention to infrastructure, engineering, or construction indicators).
    2. What high-stakes operational pain or project risk are they trying to resolve by hiring this person?
    3. What mandatory technical requirements or delivery frameworks are explicitly requested?
    
    Linguistic Rule: Output your response in standard Australian English.
    """
    
    response = ollama.generate(model=model_name, prompt=prompt, options={"temperature": 0.4})
    output = response.get("response", "").strip()
    
    if "</think>" in output:
        output = output.split("</think>")[-1].strip()
    return output

def structure_brief_to_json(brief_content: str, model_name: str) -> Dict[str, Any]:
    """Stage 2b: Focuses exclusively on mapping text down to strict JSON syntax parameters."""
    
    # Load your blueprint layout schema requirements
    prompt = load_prompt_blueprint("task2_analyze.txt", target_organization=brief_content, target_description="[Processed in Brief]")

    response = ollama.generate(model=model_name, prompt=prompt, options={"temperature": 0.1})
    output_text = response.get("response", "").strip()
    
    if "</think>" in output_text:
        output_text = output_text.split("</think>")[-1].strip()
        
    if output_text.startswith("```"):
        lines = output_text.splitlines()
        if lines[0].startswith("```json") or lines[0].startswith("```"):
            output_text = "\n".join(lines[1:-1]).strip()
            
    try:
        return json.loads(output_text)
    except Exception:
        # Graceful parsing safety fallbacks
        return {
            "industry_sector": "Identified Sector Block",
            "mission_critical_focus": "High-stakes execution focus.",
            "extracted_core_requirements": ["Mandatory Skill 1"],
            "value_proposition_points": ["Candidate alignment strategy point"]
        }