# ==============================================================================
# MODULE:  cli.main
# VERSION: 5.2.0
# STATUS:  Human-in-the-Loop Granular CLI Task Orchestrator
# ==============================================================================

import sys
import json
import argparse
from src.paths import verify_workspace_paths

# Core Module Task Imports
from src.tasks.task1_ingest import run_ingest
from src.tasks.task2_analyze import extract_domain_brief, structure_brief_to_json
from src.tasks.task3_resume import run_tailor_resume
from src.tasks.task4_letter import run_tailor_letter
from src.tasks.task5_compile import run_compile_task

def run_pipeline_cli():
    """Master command parser and process router for the tailoring workspace."""
    # Enforce directory tracking maps before processing commands
    verify_workspace_paths()

    parser = argparse.ArgumentParser(description="Human-in-the-Loop Resume & Letter Tailoring System")
    parser.add_argument(
        "command", 
        choices=["ingest", "analyze-domain", "analyze-json", "resume", "letter", "compile"], 
        help="The explicit execution step to run independently."
    )
    parser.add_argument("--model", default="deepseek-r1:14b", help="The Ollama local model instance tag to target.")
    parser.add_argument("--pass_num", type=int, choices=[0, 1, 2, 3, 4], default=None,
                        help="Target a single specific pass inside the resume loop.")

    args = parser.parse_args()

    # Routing matrix map
    if args.command == "ingest":
        run_ingest_step()
    elif args.command == "analyze-domain":
        run_analyze_domain_step(args.model)
    elif args.command == "analyze-json":
        run_analyze_json_step(args.model)
    elif args.command == "resume":
        run_resume_step(args.model, args.pass_num)
    elif args.command == "letter":
        run_letter_step(args.model)
    elif args.command == "compile":
        run_compile_step()

# ------------------------------------------------------------------------------
# ISOLATED ATOMIC COMMAND EXECUTORS
# ------------------------------------------------------------------------------

def run_ingest_step():
    """Executes Stage 1: Harvesting workspace text records into an asset cache."""
    from src.paths import GLOBAL_DATA_DIR, TARGET_JOB_DIR, CHECKPOINT_INGEST
    
    raw_data = run_ingest(GLOBAL_DATA_DIR, TARGET_JOB_DIR)
    CHECKPOINT_INGEST.write_text(json.dumps(raw_data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n✅ Ingestion Complete! Open and inspect/edit: '{CHECKPOINT_INGEST}'")


def run_analyze_domain_step(model: str):
    """Executes Stage 2a: Pure text reading and freeform domain extraction brief."""
    from src.paths import CHECKPOINT_INGEST, WORKING_DIR
    
    if not CHECKPOINT_INGEST.exists():
        print(f"❌ Error: Missing raw ingestion checkpoint. Run 'python tailor.py ingest' first.")
        sys.exit(1)
        
    context = json.loads(CHECKPOINT_INGEST.read_text(encoding="utf-8"))
    
    # Generate plain-text scratchpad notes directly in your workspace root
    brief_text = extract_domain_brief(context, model)
    brief_file = WORKING_DIR / "02a_domain_brief.txt"
    brief_file.write_text(brief_text, encoding="utf-8")
    
    print(f"\n📝 Domain Extraction Brief Created! Open and inspect: '02a_domain_brief.txt'")
    print(f"   👉 Type your construction and corporate notes directly into this text file right now!")


def run_analyze_json_step(model: str):
    """Executes Stage 2b: Structural transformation of human-validated brief to JSON schema."""
    from src.paths import WORKING_DIR, CHECKPOINT_ANALYZE
    
    brief_file = WORKING_DIR / "02a_domain_brief.txt"
    if not brief_file.exists():
        print(f"❌ Error: Missing domain brief text file. Run 'python tailor.py analyze-domain' first.")
        sys.exit(1)
        
    brief_content = brief_file.read_text(encoding="utf-8")
    analysis_json = structure_brief_to_json(brief_content, model)
    
    CHECKPOINT_ANALYZE.write_text(json.dumps(analysis_json, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n✅ Analysis Step Finalised! Clean JSON payload structured inside: '{CHECKPOINT_ANALYZE}'")


def run_resume_step(model: str, pass_num: int):
    """Executes Stage 3: Builds the multi-pass structured resume matrix payload."""
    from src.paths import CHECKPOINT_INGEST, CHECKPOINT_ANALYZE, CHECKPOINT_RESUME
    
    if not CHECKPOINT_ANALYZE.exists():
        print(f"❌ Error: Missing strategic analysis file. Run 'python tailor.py analyze-json' first.")
        sys.exit(1)
        
    ingest_data = json.loads(CHECKPOINT_INGEST.read_text(encoding="utf-8"))
    analysis_data = json.loads(CHECKPOINT_ANALYZE.read_text(encoding="utf-8"))
    
    # Securely couple active state pipelines together
    context = {**ingest_data, "strategic_analysis": analysis_data}
    final_resume = run_tailor_resume(context, model, target_pass=pass_num)
    
    if final_resume: 
        CHECKPOINT_RESUME.write_text(json.dumps(final_resume, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\n✅ Resume Generation Complete! Polish your bullets directly inside: '{CHECKPOINT_RESUME}'")


def run_letter_step(model: str):
    """Executes Stage 4: Formulates a highly aligned targeted application cover letter."""
    from src.paths import CHECKPOINT_INGEST, CHECKPOINT_ANALYZE, CHECKPOINT_LETTER
    
    if not CHECKPOINT_ANALYZE.exists():
        print(f"❌ Error: Missing analysis file. Run 'python tailor.py analyze-json' first.")
        sys.exit(1)
        
    context = json.loads(CHECKPOINT_INGEST.read_text(encoding="utf-8"))
    context["strategic_analysis"] = json.loads(CHECKPOINT_ANALYZE.read_text(encoding="utf-8"))
    
    letter_text = run_tailor_letter(context, model)
    CHECKPOINT_LETTER.write_text(json.dumps({"letter_body": letter_text}, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n✅ Cover Letter Drafted! Review prose parameters inside: '{CHECKPOINT_LETTER}'")


def run_compile_step():
    """Executes Stage 5: Maps finalized state assets straight to the Typst compilation layout engine."""
    from src.paths import CHECKPOINT_RESUME, CHECKPOINT_LETTER, OUTPUT_DIR
    
    if not CHECKPOINT_RESUME.exists():
        print(f"❌ Error: No finalised resume matrix discovered. Build it first.")
        sys.exit(1)
        
    resume_data = json.loads(CHECKPOINT_RESUME.read_text(encoding="utf-8"))
    letter_data = json.loads(CHECKPOINT_LETTER.read_text(encoding="utf-8")) if CHECKPOINT_LETTER.exists() else {}
    
    context = {"tailored_resume": resume_data, "tailored_letter": letter_data}
    run_compile_task(context, str(OUTPUT_DIR))
    print(f"\n✨ Compilation Finished! Final Typst layout generated inside: '{OUTPUT_DIR}/'")