import os
from pathlib import Path
import ollama

# --- CONFIGURATION ---
# Swap between these two depending on what you need:
MODEL_NAME = "qwen2.5-coder:7b"  # Fast, clean formatting, excellent tone
# MODEL_NAME = "deepseek-r1:14b"  # Deep analysis, handles ambiguity, slower

DATA_DIR = Path("./data")
MASTER_CV_PATH = DATA_DIR / "master_resume.md"
JD_PATH = DATA_DIR / "job_description.md"
OUTPUT_PATH = DATA_DIR / "tailored_resume.md"

def load_text(file_path: Path) -> str:
    if not file_path.exists():
        raise FileNotFoundError(f"Missing required file: {file_path}")
    return file_path.read_text(encoding="utf-8")

def main():
    master_cv = load_text(MASTER_CV_PATH)
    job_desc = load_text(JD_PATH)

    system_prompt = (
        "You are an expert technical resume writer. "
        "Analyze the provided Job Description and extract relevant experience "
        "from the User's Master Resume to create a highly tailored, clean CV.\n\n"
        "CRITICAL RULES:\n"
        "1. DO NOT invent or assume any experience. If it's not in the Master Resume, omit it.\n"
        "2. Keep the tone authentic, grounded, and technical. Speak like a real engineer who ships code.\n"
        "3. Avoid corporate buzzwords ('leveraged bleeding-edge synergy').\n"
        "4. Emphasize actual stacks used and quantitative impact.\n"
        "5. Output the result in beautiful, clear Markdown format."
    )

    user_prompt = f"### TARGET JOB DESCRIPTION:\n{job_desc}\n\n### MY MASTER RESUME:\n{master_cv}"

    print(f"🚀 Prompting local model '{MODEL_NAME}' via Ollama...")
    
    # Dynamic arguments to prevent 400 errors on standard models
    chat_kwargs = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "stream": True
    }
    
    if "deepseek-r1" in MODEL_NAME.lower():
        chat_kwargs["think"] = True

    try:
        response_stream = ollama.chat(**chat_kwargs)

        tailored_content = []
        started_thinking = False
        started_content = False
        
        for chunk in response_stream:
            message = chunk.get('message', {})
            
            # Catch and stream the internal reasoning path (DeepSeek only)
            thinking = message.get('thinking', '')
            if thinking:
                if not started_thinking:
                    print("\n🧠 AI REASONING/THINKING TRACK:")
                    print("=============================")
                    started_thinking = True
                print(thinking, end='', flush=True)
                continue

            # Catch and stream the actual resume payload
            content = message.get('content', '')
            if content:
                if not started_content:
                    print("\n\n📄 GENERATING TAILORED RESUME:")
                    print("=============================")
                    started_content = True
                print(content, end='', flush=True)
                tailored_content.append(content)
            
        print("\n\n✅ Generation complete.")

        if tailored_content:
            OUTPUT_PATH.write_text("".join(tailored_content), encoding="utf-8")
            print(f"💾 Clean tailored resume saved to: {OUTPUT_PATH}")
        else:
            print("⚠️ No content was generated. Check your model status.")

    except Exception as e:
        print(f"\n❌ Error connecting to Ollama: {e}")

if __name__ == "__main__":
    main()