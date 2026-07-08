# tailor.py
from src.pipeline import TailorPipeline

if __name__ == "__main__":
    # Boots up the multi-task stage orchestration sequence safely
    pipeline = TailorPipeline(model_name="qwen2.5-coder:1.5b")
    pipeline.execute()