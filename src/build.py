#!/usr/bin/env python3
import os

def read_file(filepath):
    """Safely reads content from a file if it exists."""
    if not os.path.exists(filepath):
        print(f"Warning: {filepath} not found. Skipping.")
        return ""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def build_resume():
    # Paths to files
    style_path = "style.css"
    content_dir = "content"
    output_path = "index.html"
    
    # Order of HTML components to join inside the profile container wrapper
    fragments = [
        "header.html",
        "nav.html",
        "about.html",
        "capabilities.html",
        "experience.html",
        "education.html",
        "strategy.html"
    ]
    
    print("Reading styles...")
    css_content = read_file(style_path)
    
    print("Assembling content sections...")
    body_content = ""
    for fragment in fragments:
        frag_path = os.path.join(content_dir, fragment)
        body_content += read_file(frag_path) + "\n"
        
    # Python-based multi-line document generation layout
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="document-version" content="3.0">
    <title>Jon Morgan | Technical Director – Built Environment & Digital Integration</title>
    <style>
{css_content}
    </style>
</head>
<body>

    <div class="profile-container">
{body_content}
    </div>

    <script>
        // Global Collapse Toggle Engine
        function toggleDetails(btn, containerId) {{
            const content = document.getElementById(containerId);
            const isExpanded = content.classList.contains('expanded');
            
            if (isExpanded) {{
                content.classList.remove('expanded');
                btn.innerHTML = 'Show more ↓';
                btn.setAttribute('aria-expanded', 'false');
            }} else {{
                content.classList.add('expanded');
                btn.innerHTML = 'Show less ↑';
                btn.setAttribute('aria-expanded', 'true');
            }}
        }}
    </script>
</body>
</html>"""

    print(f"Writing unified production layout to {output_path}...")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_template)
        
    print("Build Complete Success.")

if __name__ == "__main__":
    build_resume()