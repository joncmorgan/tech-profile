# src/pipeline.py
from pathlib import Path
from src.tasks.task1_ingest import run_ingest
from src.tasks.task2_resume import run_tailor_resume
from src.tasks.task3_letter import run_tailor_letter
from src.tasks.task4_compile import run_compile_typst

class TailorPipeline:
    def __init__(self, model_name: str = "qwen2.5-coder:1.5b"):
        self.model_name = model_name
        self.base_dir = Path(__file__).resolve().parent.parent
        self.target_dir = Path(".target_job")
        self.data_dir = self.base_dir / "data"
        self.output_dir = self.base_dir / "output"
        
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def execute(self):
        context = run_ingest(self.base_dir, self.target_job, self.data_dir) if hasattr(self, 'target_job') else run_ingest(self.base_dir, self.target_dir, self.data_dir)
        resume_out = run_tailor_resume(context, self.model_name)
        letter_out = run_tailor_letter(context, self.model_name)
        
        # Now passing context directly to hydrate personal tokens
        run_compile_typst(self.output_dir, context, resume_out, letter_out)