# Repository Agent Instructions

This repository is a multi-purpose workspace combining a modern **Astro web project** (at the root) and a **Python-based resume and CV generation pipeline** (`cv/` directory using `uv` and Typst).

---

## 1. Environment & Execution Rules

*   **Node/Astro:** Always execute Astro CLI commands using `npx` (or via `npm run`) to ensure local `node_modules` binaries are resolved correctly. Never run `astro` directly.
*   **Python/Resume Pipeline:** Always execute Python scripts using `uv` with the project flag pointing to the repository root to ensure the correct virtual environment and dependencies (`typst`) are loaded:
    ```bash
    uv --project . python cv/scripts/<script_name>.py
    ```

---

## 2. Web Development (Astro)

When starting the development server, use background mode:

```bash
npx astro dev --background