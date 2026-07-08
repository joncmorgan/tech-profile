# src/pipeline.py
import json
import time
from pathlib import Path

from src.tasks.task1_ingest import run_ingest
from src.tasks.task2_resume import run_tailor_resume
from src.tasks.task3_letter import run_tailor_letter
from src.tasks.task4_compile import run_compile_typst

class TailorPipeline:
    def __init__(self, model_name: str = "qwen2.5-coder:1.5b", use_cache: bool = False):
        self.model_name = model_name
        self.use_cache = use_cache
        
        self.base_dir = Path(__file__).resolve().parent.parent
        self.target_dir = Path(".target_job")
        self.data_dir = self.base_dir / "data"
        self.output_dir = self.base_dir / "output"
        self.cache_file = self.base_dir / ".pipeline_cache" / "llm_snapshot.json"
        
        # Ensure directory paths exist safely
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)

    def execute(self):
        # Always run Ingest to keep personal info and target text completely live
        context = run_ingest(self.base_dir, self.target_dir, self.data_dir)
        
        # Initialize asset buckets
        resume_out = {}
        letter_out = ""

        # Check if we should short-circuit the LLM steps via Cache
        if self.use_cache and self.cache_file.exists():
            print(f"⚡ [{time.strftime('%H:%M:%S')}] CACHE HIT: Skipping local LLM inference passes...")
            with open(self.cache_file, "r", encoding="utf-8") as f:
                cached_data = json.load(f)
                resume_out = cached_data["resume_out"]
                letter_out = cached_data["letter_out"]
        else:
            if self.use_cache:
                print(f"⚠️ [{time.strftime('%H:%M:%S')}] Cache flag active, but no snapshot found. Running fresh LLM queries...")

            # Execute full processing paths
            resume_out = run_tailor_resume(context, self.model_name)
            letter_out = run_tailor_letter(context, self.model_name)
            
            # Save the generation snapshot to disk immediately for next runs
            snapshot = {
                "resume_out": resume_out,
                "letter_out": letter_out
            }
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(snapshot, f, indent=2)
            print(f"💾 [{time.strftime('%H:%M:%S')}] Factual LLM outputs written safely to snapshot cache.")

        # Step 4: Pass straight to compilation tasks
        run_compile_typst(self.output_dir, context, resume_out, letter_out)