# ==============================================================================
# MODULE:  src.tasks.task3_resume
# VERSION: 5.0.0
# STATUS:  Bite-Sized Modular Execution Engine supporting State-Cached Passes
# ==============================================================================

import time
import json
import ollama
from typing import Dict, Any, List, Optional
from src.paths import load_prompt_blueprint, WORKING_DIR, CHECKPOINT_RESUME

CACHE_FILE = WORKING_DIR / ".resume_cache.json"

def _clean_llm_json(raw_text: str) -> str:
    """Helper method to remove reasoning tags and extract markdown JSON code blocks."""
    if "</think>" in raw_text:
        raw_text = raw_text.split("</think>")[-1].strip()
    if raw_text.startswith("```"):
        lines = raw_text.splitlines()
        if lines[0].startswith("```json") or lines[0].startswith("```"):
            raw_text = "\n".join(lines[1:-1]).strip()
    return raw_text.strip()

def _load_cache() -> Dict[str, Any]:
    """Helper to maintain state between isolated CLI pass calls."""
    if CACHE_FILE.exists():
        try:
            return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {
        "initialized_history": [], "heavy_hitters": [], "historical_context": [],
        "candidate_profile": {}, "tailored_profile": {},
        "tailored_recent_history": [], "tailored_older_history": []
    }

def _save_cache(cache_data: Dict[str, Any]):
    """Helper to write state adjustments safely back to disk."""
    CACHE_FILE.write_text(json.dumps(cache_data, indent=2, ensure_ascii=False), encoding="utf-8")

def run_tailor_resume(context: Dict[str, Any], model_name: str, target_pass: Optional[int] = None) -> Dict[str, Any]:
    print(f"\n📊 [{time.strftime('%H:%M:%S')}] [Task 3/5] Processing Resume Construction Chain (Target Pass: {target_pass if target_pass is not None else 'ALL'})...")
    
    work_history = context.get("work_history", [])
    strategic_analysis = context.get("strategic_analysis", {})
    core_skills = context.get("core_skills", {})
    education = context.get("education", [])

    if not work_history and target_pass in [0, None]:
        print("   ⚠️  Warning: No raw work history records discovered in context.")
        return {}

    # Load previously computed blocks if we are running granular updates
    state = _load_cache()

    # Define execution boundaries based on your parameters
    run_all = target_pass is None

    # --------------------------------------------------------------------------
    # PASS 0: Foundation Initialization Layer
    # --------------------------------------------------------------------------
    if run_all or target_pass == 0:
        print("   ↳ Pass 0/5: Isolating baseline data and framing structural matrices...")
        raw_history_strings = []
        for job in work_history:
            raw_history_strings.append(
                f"COMPANY: {job.get('company')}\n"
                f"TITLE: {job.get('title')}\n"
                f"DATES: {job.get('start_date', 'N/A')} - {job.get('end_date', 'Present')}\n"
                f"STRATEGIC PRIORITY: {job.get('strategic_priority', 99)}\n"
                f"RENDER TIER: {job.get('render_tier', 'historical_context')}\n"
                f"RAW BULLETS & MEMORIES:\n{job.get('memories', '')}"
            )
        full_raw_data = "\n\n---\n\n".join(raw_history_strings)

        init_prompt = load_prompt_blueprint(
            "task3_pass0_init.txt", 
            work_history=full_raw_data, 
            strategic_analysis=json.dumps(strategic_analysis, indent=2, ensure_ascii=False)
        )
        
        response = ollama.generate(model=model_name, prompt=init_prompt, options={"temperature": 0.1})
        pass0_data = json.loads(_clean_llm_json(response.get("response", "")))
        
        state["initialized_history"] = pass0_data.get("initialized_history", [])
        state["candidate_profile"] = pass0_data.get("candidate_profile", {})

        # Distribute into designated data tiers programmatically
        state["heavy_hitters"], state["historical_context"] = [], []
        for init_job in state["initialized_history"]:
            company_name = init_job.get("company", "").lower()
            matching_meta = next((j for j in work_history if j.get("company", "").lower() in company_name), {})
            if matching_meta.get("render_tier") == "heavy_hitter":
                state["heavy_hitters"].append(init_job)
            else:
                state["historical_context"].append(init_job)

        if not state["heavy_hitters"] and state["initialized_history"]:
            state["heavy_hitters"] = [state["initialized_history"][0]]
            state["historical_context"] = state["initialized_history"][1:]
        
        _save_cache(state)

    # --------------------------------------------------------------------------
    # PASS 1: Sculpt Executive Profile Summary Narrative
    # --------------------------------------------------------------------------
    if run_all or target_pass == 1:
        print("   ↳ Pass 1/5: Formatting grounded Executive Profile and Core Strength narrative...")
        pass1_prompt = load_prompt_blueprint(
            "task3_pass1_profile.txt",
            candidate_profile=json.dumps(state["candidate_profile"], indent=2, ensure_ascii=False),
            strategic_analysis=json.dumps(strategic_analysis, indent=2, ensure_ascii=False)
        )
        
        response = ollama.generate(model=model_name, prompt=pass1_prompt, options={"temperature": 0.1})
        pass1_data = json.loads(_clean_llm_json(response.get("response", "")))
        state["tailored_profile"] = pass1_data.get("tailored_profile", {})
        _save_cache(state)

    # --------------------------------------------------------------------------
    # PASS 2: Optimise Recent Heavy-Hitter Experience Roles
    # --------------------------------------------------------------------------
    if run_all or target_pass == 2:
        print(f"   ↳ Pass 2/5: Re-architecting {len(state['heavy_hitters'])} primary achievements...")
        pass2_prompt = load_prompt_blueprint(
            "task3_pass2_recent.txt",
            initialized_history=json.dumps(state["heavy_hitters"], indent=2, ensure_ascii=False),
            strategic_analysis=json.dumps(strategic_analysis, indent=2, ensure_ascii=False)
        )
        
        response = ollama.generate(model=model_name, prompt=pass2_prompt, options={"temperature": 0.1})
        pass2_data = json.loads(_clean_llm_json(response.get("response", "")))
        state["tailored_recent_history"] = pass2_data.get("tailored_recent_history", [])
        _save_cache(state)

    # --------------------------------------------------------------------------
    # PASS 3: Condense Historical Time Horizons 
    # --------------------------------------------------------------------------
    if run_all or target_pass == 3:
        print(f"   ↳ Pass 3/5: Compressing {len(state['historical_context'])} older historical entries...")
        pass3_prompt = load_prompt_blueprint(
            "task3_pass3_older.txt",
            initialized_history=json.dumps(state["historical_context"], indent=2, ensure_ascii=False),
            strategic_analysis=json.dumps(strategic_analysis, indent=2, ensure_ascii=False)
        )
        
        response = ollama.generate(model=model_name, prompt=pass3_prompt, options={"temperature": 0.1})
        pass3_data = json.loads(_clean_llm_json(response.get("response", "")))
        state["tailored_older_history"] = pass3_data.get("tailored_older_history", [])
        _save_cache(state)

    # --------------------------------------------------------------------------
    # PASS 4: Consolidated Aggregation & Structural Formatting
    # --------------------------------------------------------------------------
    if run_all or target_pass == 4:
        print("   ↳ Pass 4/5: Compiling final metrics map payload for Typst syntax validation...")
        pass4_prompt = load_prompt_blueprint(
            "task3_pass4_format.txt",
            tailored_profile=json.dumps(state["tailored_profile"], indent=2, ensure_ascii=False),
            tailored_recent_history=json.dumps(state["tailored_recent_history"], indent=2, ensure_ascii=False),
            tailored_older_history=json.dumps(state["tailored_older_history"], indent=2, ensure_ascii=False),
            core_skills=json.dumps(core_skills, indent=2, ensure_ascii=False),
            education=json.dumps(education, indent=2, ensure_ascii=False)
        )
        
        response = ollama.generate(model=model_name, prompt=pass4_prompt, options={"temperature": 0.1})
        resume_data = json.loads(_clean_llm_json(response.get("response", "")))
        
        print("   ✅ Full multi-pass resume data block successfully synthesised.")
        return resume_data

    # Return whatever the state cache looks like at this point if a middle sub-pass was updated
    return state.get("resume_data", {})