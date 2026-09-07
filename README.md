# Tech Profile & Portfolio

A high-signal, minimalist professional profile and project portfolio built with [Astro](https://astro.build), styled with Tailwind CSS, and optimized for local-first software engineering systems and computational models.

## 🛠️ Tech Stack

* **Framework:** [Astro](https://astro.build) (with Client Router view transitions)
* **Styling:** [Tailwind CSS](https://tailwindcss.com) & [DaisyUI](https://daisyui.com)
* **Language:** TypeScript / JavaScript
* **Hosting:** GitHub Pages (Automated via GitHub Actions)

## 📁 Project Structure

```text
├── .github/
│   └── workflows/      # GitHub Pages deployment action
├── src/
│   ├── assets/         # Images and static assets
│   ├── components/     # UI components (Navbar, Footer, etc.)
│   ├── layouts/        # Page layout wrappers (Layout.astro)
│   ├── pages/          # Astro pages (Home, Projects)
│   ├── settings.ts     # Global profile and site configuration
│   └── projects.ts     # Curated project data structure
├── astro.config.mjs    # Astro configuration
└── package.json        # Dependencies and scripts