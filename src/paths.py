# ==============================================================================
# MODULE:  src.paths
# VERSION: 1.1.0
# STATUS:  Central Space Path Configurations & State Checkpoints
# ==============================================================================

import os
from pathlib import Path

SRC_ROOT = Path(__file__).resolve().parent.parent

# Central static asset locations
GLOBAL_DATA_DIR = SRC_ROOT / "data"
TEMPLATE_DIR = GLOBAL_DATA_DIR / "templates"
PERSONAL_FILE = GLOBAL_DATA_DIR / "personal_details.json"

# Active working directories (dynamic evaluation bounds)
WORKING_DIR = Path.cwd()
TARGET_JOB_DIR = WORKING_DIR / ".target_job"
OUTPUT_DIR = WORKING_DIR / "output"

# Granular State Machine Checkpoint File Mappings
STATE_DIR = WORKING_DIR / ".pipeline_state"
CHECKPOINT_INGEST = STATE_DIR / "01_ingested_raw.json"
CHECKPOINT_ANALYZE = STATE_DIR / "02_strategic_analysis.json"
CHECKPOINT_RESUME = STATE_DIR / "03_tailored_resume.json"
CHECKPOINT_LETTER = STATE_DIR / "04_tailored_letter.json"

# Add this directory tracking map to the middle of src/paths.py
PROMPT_DIR = GLOBAL_DATA_DIR / "prompts"

def __load_prompt_blueprint(filename: str) -> str:
    """Safely retrieves a raw prompt profile template string from disk."""
    prompt_file = PROMPT_DIR / filename
    if not prompt_file.exists():
        raise FileNotFoundError(f"❌ Critical Configuration File Missing: {prompt_file}")
    return prompt_file.read_text(encoding="utf-8").strip()

def load_prompt_blueprint(filename: str, **kwargs) -> str:
    """
    Safely retrieves a raw prompt blueprint from disk.
    If context variables are provided via kwargs, it substitutes them, 
    exports the rendered prompt to the working directory for tracking, 
    and returns the fully populated string text.
    """
    prompt_file = PROMPT_DIR / filename
    if not prompt_file.exists():
        raise FileNotFoundError(f"❌ Critical Configuration File Missing: {prompt_file}")
        
    raw_text = prompt_file.read_text(encoding="utf-8").strip()
    
    # If variables are provided, perform safe replacement substituting keys
    if kwargs:
        rendered_text = raw_text
        for key, value in kwargs.items():
            placeholder = f"{{{key}}}"
            rendered_text = rendered_text.replace(placeholder, str(value))
        
        # Determine tracking file name (e.g., rendered_task2_analyze.txt)
        export_file = WORKING_DIR / f"rendered_{filename}"
        try:
            export_file.write_text(rendered_text, encoding="utf-8")
            print(f"   📝 Debug Export: Saved rendered prompt straight to {export_file.name}")
        except Exception as e:
            print(f"   ⚠️  Could not write rendered debug prompt text to disk: {e}")
            
        return rendered_text

    return raw_text

def verify_workspace_paths() -> bool:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    
    if not os.access(WORKING_DIR, os.W_OK):
        raise PermissionError(f"❌ Write access denied in active terminal path: {WORKING_DIR}")
    return True