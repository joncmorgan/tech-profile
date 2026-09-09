import os
import json
import argparse
from pathlib import Path
from dotenv import load_dotenv
import anthropic

class AstroProjectTransformer:
    def __init__(self, model: str = "claude-sonnet-5"):
        load_dotenv()
        api_key = os.getenv("ANTHROPIC_API_KEY")

        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables or .env file.")

        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model

        # Resolve paths
        self.script_dir = Path(__file__).resolve().parent
        self.src_root_dir = self.script_dir.parent
        self.repo_root_dir = self.src_root_dir.parent
        self.projects_json_path = self.repo_root_dir / "data" / "projects.json"
        self.output_path = self.src_root_dir / "data" / "master_experience.json"
        self.prompt_path = self.script_dir / "prompt_resume.txt"

    def load_projects(self) -> dict:
        with open(self.projects_json_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def load_transformed_projects(self) -> list:
        if self.output_path.exists():
            try:
                with open(self.output_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []

    def save_transformed_projects(self, projects_list: list):
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.output_path, "w", encoding="utf-8") as f:
            json.dump(projects_list, f, indent=4)

    def get_project_id(self, project: dict) -> str:
        """Retrieves an explicit ID or generates a stable slug from the title."""
        if "id" in project and project["id"]:
            return str(project["id"])
        title = project.get("title", "untitled")
        return "".join(c.lower() if c.isalnum() else "-" for c in title).strip("-")

    def load_prompt_template(self) -> str:
        with open(self.prompt_path, "r", encoding="utf-8") as f:
            return f.read()

    def transform_project_with_claude(self, project: dict, template: str) -> dict:
        project_id = self.get_project_id(project)
        title = project.get("title", "")
        primary_cat = project.get("primaryCategory", "")
        secondary_cat = project.get("secondaryCategory", "")
        outcome = project.get("outcome", "")
        context = project.get("context", "")
        execution = json.dumps(project.get("execution", []))

        prompt = template.format(
            project_id=project_id,
            title=title,
            primary_cat=primary_cat,
            secondary_cat=secondary_cat,
            outcome=outcome,
            context=context,
            execution=execution
        )

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )

        content_text = ""
        for block in response.content:
            if hasattr(block, "text") and block.text:
                content_text = block.text.strip()
                break

        if not content_text:
            raise ValueError("No text content found in Claude's response.")
        
        if content_text.startswith("```json"):
            content_text = content_text[7:]
        if content_text.endswith("```"):
            content_text = content_text[:-3]
            
        return json.loads(content_text.strip())

    def run_single(self):
        """Default mode: processes just one unprocessed project and appends it."""
        raw_data = self.load_projects()
        prompt_template = self.load_prompt_template()
        all_raw_projects = raw_data.get("projects", [])

        if not all_raw_projects:
            print("No projects found in projects.json.")
            return

        existing_transformed = self.load_transformed_projects()
        processed_ids = {str(p.get("id")) for p in existing_transformed if "id" in p}

        unprocessed = [p for p in all_raw_projects if self.get_project_id(p) not in processed_ids]

        if not unprocessed:
            print("All projects are already processed! Use --menu if you want to reprocess a specific item.")
            return

        target = unprocessed[0]
        title = target.get("title", "Untitled")
        print(f"Processing next pending project: '{title}'...")

        try:
            transformed = self.transform_project_with_claude(target, prompt_template)
            # Ensure proper ID replacement if updating
            pid = self.get_project_id(target)
            existing_transformed = [p for p in existing_transformed if str(p.get("id")) != pid]
            existing_transformed.append(transformed)
            
            self.save_transformed_projects(existing_transformed)
            print(f"Successfully processed and saved to {self.output_path}")
        except Exception as e:
            print(f"Error processing project '{title}': {e}")

    def run_batch(self, force: bool = False):
        """Processes all pending projects, or all projects if force=True."""
        raw_data = self.load_projects()
        prompt_template = self.load_prompt_template()
        all_raw_projects = raw_data.get("projects", [])

        if not all_raw_projects:
            print("No projects found in projects.json.")
            return

        existing_transformed = self.load_transformed_projects()

        if force:
            print("Force rebuild enabled: Re-processing ALL projects from scratch.")
            existing_transformed = []
            targets = all_raw_projects
        else:
            processed_ids = {str(p.get("id")) for p in existing_transformed if "id" in p}
            targets = [p for p in all_raw_projects if self.get_project_id(p) not in processed_ids]
            if not targets:
                print("No pending projects to process.")
                return
            print(f"Processing {len(targets)} pending project(s)...")

        for i, project in enumerate(targets, 1):
            title = project.get("title", "Untitled")
            print(f"[{i}/{len(targets)}] Processing via Claude: '{title}'...")
            try:
                transformed = self.transform_project_with_claude(project, prompt_template)
                pid = self.get_project_id(project)
                existing_transformed = [p for p in existing_transformed if str(p.get("id")) != pid]
                existing_transformed.append(transformed)
            except Exception as e:
                print(f"Error processing project '{title}': {e}")

        self.save_transformed_projects(existing_transformed)
        print(f"Successfully updated {self.output_path}")

    def run_interactive_menu(self):
        raw_data = self.load_projects()
        all_raw_projects = raw_data.get("projects", [])
        if not all_raw_projects:
            print("No projects found in projects.json.")
            return

        while True:
            existing_transformed = self.load_transformed_projects()
            processed_map = {str(p.get("id")): p for p in existing_transformed if "id" in p}

            print("\n--- Project Transformation Menu ---")
            for idx, proj in enumerate(all_raw_projects, 1):
                pid = self.get_project_id(proj)
                status = "[PROCESSED]" if pid in processed_map else "[PENDING]"
                title = proj.get("title", "Untitled")
                print(f"{idx:2d}. {status} ({pid}) {title}")

            print("\nOptions:")
            print("  [Number] : Enter project number to force re-process that specific project")
            print("  a        : Process all remaining (unprocessed) projects")
            print("  f        : Force rebuild ALL projects from scratch")
            print("  q        : Quit")
            
            choice = input("\nSelect an option: ").strip().lower()

            if choice == 'q':
                print("Exiting.")
                break
            elif choice == 'a':
                self.run_batch(force=False)
            elif choice == 'f':
                confirm = input("Are you sure you want to force rebuild ALL projects? (y/n): ").strip().lower()
                if confirm == 'y':
                    self.run_batch(force=True)
            elif choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(all_raw_projects):
                    target = all_raw_projects[idx]
                    title = target.get("title", "Untitled")
                    print(f"\nForce-processing '{title}' via Claude...")
                    
                    try:
                        prompt_template = self.load_prompt_template()
                        new_transformed = self.transform_project_with_claude(target, prompt_template)
                        
                        pid = self.get_project_id(target)
                        existing_transformed = [p for p in existing_transformed if str(p.get("id")) != pid]
                        existing_transformed.append(new_transformed)
                        
                        self.save_transformed_projects(existing_transformed)
                        print(f"Successfully updated '{title}'.")
                    except Exception as e:
                        print(f"Error processing project: {e}")
                else:
                    print("Invalid project number.")
            else:
                print("Invalid option. Try again.")


def main():
    parser = argparse.ArgumentParser(description="Transform projects.json into Astro format using Claude.")
    parser.add_argument(
        "--menu", 
        action="store_true", 
        help="Open an interactive menu to view status and reprocess specific projects."
    )
    parser.add_argument(
        "--force", 
        action="store_true", 
        help="Force rebuild all projects from scratch."
    )
    args = parser.parse_args()

    transformer = AstroProjectTransformer()
    
    if args.menu:
        transformer.run_interactive_menu()
    elif args.force:
        transformer.run_batch(force=True)
    else:
        transformer.run_single()


if __name__ == "__main__":
    main()