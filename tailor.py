# tailor.py
import sys
from src.pipeline import TailorPipeline

if __name__ == "__main__":
    # Check if a cache override string flag is present in execution call
    use_cache_flag = "--fast" in sys.argv or "--cache" in sys.argv
    
    # Boots up using class defaults natively
    pipeline = TailorPipeline(model_name="qwen2.5-coder:1.5b", use_cache=use_cache_flag)
    pipeline.execute()