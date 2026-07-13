# ==============================================================================
# MODULE:  src.pipeline
# VERSION: 4.2.1
# STATUS:  Cleaned and Standardised Uniform Stateful Engine (Syntax Verified)
# ==============================================================================

import json
import time
from pathlib import Path
from typing import Dict, Any

# Central Path and Checkpoint Constants
from src.paths import (
    GLOBAL_DATA_DIR,
    TARGET_JOB_DIR,
    OUTPUT_DIR,
    STATE_DIR,
    verify_workspace_paths
)

# Core Module Task Imports
from src.tasks.task1_ingest import run_ingest
from src.tasks.task2_analyze import run_strategic_analysis
from src.tasks.task3_resume import run_tailor_resume
from src.tasks.task4_letter import run_tailor_letter
from src.tasks.task5_compile import run_compile_task 

class TailorPipeline:
    def __init__(self, model_name: str, state_dir: Path = STATE_DIR, **kwargs):
        self.model_name = model_name
        self.state_dir = state_dir
        self.context: Dict[str, Any] = {}
        self.force_run = kwargs.get("force_run", False)
        
        # Enforce file system write verification upon pipeline initialization
        verify_workspace_paths()

    def _get_checkpoint_path(self, step_name: str) -> Path:
        return self.state_dir / f"{step_name}.json"

    def _save_checkpoint(self, step_name: str, data: Dict[str, Any]):
        path = self._get_checkpoint_path(step_name)
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    def _load_checkpoint(self, step_name: str) -> Dict[str, Any]:
        path = self._get_checkpoint_path(step_name)
        if path.exists():
            print(f"📦 [{time.strftime('%H:%M:%S')}] Checkpoint Hit: Loaded {step_name.replace('_', ' ').title()} data.")
            return json.loads(path.read_text(encoding="utf-8"))
        return {}

    def execute(self, *args, **kwargs):
        # Operational arguments fall back directly onto src.paths variables
        target_step = "all"
        output_directory = str(OUTPUT_DIR)

        if len(args) > 0: target_step = str(args[0])
        if len(args) > 1: output_directory = str(args[1])

        target_step = kwargs.get("target_step", kwargs.get("step", target_step))
        output_directory = kwargs.get("output_directory", kwargs.get("output_dir", output_directory))

        # ----------------------------------------------------------------------
        # STEP 1: Profile Ingestion Layer
        # ----------------------------------------------------------------------
        step1_data = self._load_checkpoint("01_ingested_raw")
        if not step1_data or self.force_run:
            # Pass correct tracking paths directly out of src.paths definitions
            step1_data = run_ingest(GLOBAL_DATA_DIR, TARGET_JOB_DIR)
            self._save_checkpoint("01_ingested_raw", step1_data)

        self.context["target_organization"] = step1_data.get("target_organization", "")
        self.context["target_description"] = step1_data.get("target_description", "")
        self.context["target_recipient"] = step1_data.get("target_recipient", {})
        self.context["core_skills"] = step1_data.get("core_skills", {})        
        self.context["personal_info"] = step1_data.get("personal_info", {})
        self.context["work_history"] = step1_data.get("work_history", [])
        self.context["education"] = step1_data.get("education", [])

        if target_step.lower() == "ingest": return

        # ----------------------------------------------------------------------
        # STEP 2: Strategic Persona Analysis
        # ----------------------------------------------------------------------
        step2_data = self._load_checkpoint("02_strategic_analysis")
        if (not step2_data and target_step.lower() != "compile") or self.force_run:
            step2_data = run_strategic_analysis(self.context, self.model_name)
            self._save_checkpoint("02_strategic_analysis", step2_data)
        
        self.context["strategic_analysis"] = step2_data

        if target_step.lower() == "analyze": return

        # ----------------------------------------------------------------------
        # STEP 3: Multi-Pass Resume Matrix Tailoring
        # ----------------------------------------------------------------------
        step3_data = self._load_checkpoint("03_tailored_resume")
        if (not step3_data and target_step.lower() != "compile") or self.force_run:
            step3_data = run_tailor_resume(self.context, self.model_name)
            self._save_checkpoint("03_tailored_resume", step3_data)
        
        self.context["tailored_resume"] = step3_data

        if target_step.lower() == "resume": return

        # ----------------------------------------------------------------------
        # STEP 4: Cover Letter Prose Writing
        # ----------------------------------------------------------------------
        step4_data = self._load_checkpoint("04_tailored_letter")
        if (not step4_data and target_step.lower() != "compile") or self.force_run:
            letter_text = run_tailor_letter(self.context, self.model_name)
            step4_data = {"letter_body": letter_text}
            self._save_checkpoint("04_tailored_letter", step4_data)
        
        self.context["tailored_letter"] = step4_data

        if target_step.lower() == "letter": return

        # ----------------------------------------------------------------------
        # STEP 5: Typst Compilation Layer
        # ----------------------------------------------------------------------
        if target_step.lower() in ["compile", "all"]:
            run_compile_task(self.context, output_directory)
            print(f"\n✨ [{time.strftime('%H:%M:%S')}] Execution pipeline completed successfully.")