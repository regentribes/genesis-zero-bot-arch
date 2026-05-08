#!/usr/bin/env python3
"""
Archimate build.py — generates rendered exports from ArchiMate models.

Uses the archimate-ci-image Docker container for rendering.
Falls back to local processing when Docker is unavailable.

Pipeline:
1. Scan models/ directory for .archimate XML files
2. Run Docker container to produce HTML/SVG/PNG exports
3. Copy assets (aligned CSS)
4. Build index page linking to all model exports
"""

import subprocess
import shutil
import re
from pathlib import Path

ARCHIMATE_DOCKER = "ghcr.io/woozymasta/archimate-ci-image:5.7.0-1.0.6"
MODELS_DIR = Path(__file__).parent / "models"
EXPORTS_DIR = Path(__file__).parent / "exports"
ASSETS_DIR = Path(__file__).parent / "assets"
SITE_DIR = Path(__file__).parent / "_site"


THEME_SCRIPT = '''<script>
function toggleTheme(){
  var b=document.body,d=b.classList.contains("dark");
  b.classList.toggle("dark");b.classList.toggle("light");
  var v=[["--bg",d?"#000000":"#ffffff"],["--text",d?"#888888":"#333333"],
         ["--heading",d?"#ffffff":"#000000"],["--muted",d?"#555555":"#888888"],
         ["--border",d?"#222222":"#e0e0e0"],["--code-bg",d?"#0a0a0a":"#f5f5f5"]];
  for(var i=0;i<v.length;i++){b.style.setProperty(v[i][0],v[i][1]);
    document.documentElement.style.setProperty(v[i][0],v[i][1]);}
  localStorage.setItem("theme",b.classList.contains("dark")?"dark":"light");
}
document.addEventListener("DOMContentLoaded",function(){
  var s=localStorage.getItem("theme");
  var isDark=!s||s==="dark"||(!s&&window.matchMedia("(prefers-color-scheme:dark)").matches);
  document.body.className=isDark?"dark":"light";
  var dark=document.body.classList.contains("dark");
  var v=[["--bg",dark?"#000000":"#ffffff"],["--text",dark?"#888888":"#333333"],
         ["--heading",dark?"#ffffff":"#000000"],["--muted",dark?"#555555":"#888888"],
         ["--border",dark?"#222222":"#e0e0e0"],["--code-bg",dark?"#0a0a0a":"#f5f5f5"]];
  for(var i=0;i<v.length;i++){document.body.style.setProperty(v[i][0],v[i][1]);
    document.documentElement.style.setProperty(v[i][0],v[i][1]);}
});
</script>'''

SITE_HEADER = '''<header class="site-header">
  <div class="container">
    <h1><a href="index.html">ArchiMate Models</a></h1>
    <p>Regenerative Neighbourhood Architecture</p>
    <button id="theme-toggle" onclick="toggleTheme()">&#9790;</button>
  </div>
</header>'''

SITE_FOOTER = '''<footer>
  <p>Generated from ArchiMate models · deployed via GitHub Actions</p>
</footer>'''


def docker_available():
    """Check if Docker is available and image is pulled."""
    result = subprocess.run(["docker", "images", ARCHIMATE_DOCKER], 
                          capture_output=True, text=True)
    return result.returncode == 0 and ARCHIMATE_DOCKER.split(":")[0] in result.stdout


def parse_archimate_model(xml_path):
    """Parse .archimate XML and extract model metadata."""
    try:
        content = xml_path.read_text(encoding="utf-8")
    except Exception:
        return None
    
    name_match = re.search(r'name="([^"]+)"', content)
    id_match = re.search(r'id="model-([^"]+)"', content)
    version_match = re.search(r'version="([^"]+)"', content)
    
    # Count elements by layer
    layers = {
        "motivation": len(re.findall(r'<motivation:', content)),
        "strategy": len(re.findall(r'<strategy:', content)),
        "business": len(re.findall(r'<business-', content)),
        "application": len(re.findall(r'<application-', content)),
        "technology": len(re.findall(r'<technology-', content)),
        "implementation": len(re.findall(r'<implementation-', content)),
    }
    
    relationships = len(re.findall(r'<relationship', content))
    views = len(re.findall(r'<view', content))
    
    return {
        "name": name_match.group(1) if name_match else xml_path.stem,
        "id": id_match.group(1) if id_match else xml_path.stem,
        "version": version_match.group(1) if version_match else "1.0",
        "layers": layers,
        "relationships": relationships,
        "views": views,
        "file": str(xml_path)
    }


def generate_model_index(models):
    """Generate index page listing all models."""
    model_cards = []
    
    for m in models:
        layer_bars = " ".join([f'<span class="layer-tag">{k}: {v}</span>' 
                               for k, v in m['layers'].items() if v > 0])
        
        card = f'''<div class="model-card">
  <h2><a href="model-{m['id']}.html">{m['name']}</a></h2>
  <div class="model-meta">
    <span>v{m['version']}</span>
    <span>{m['views']} views</span>
    <span>{m['relationships']} relationships</span>
  </div>
  <div class="model-layers">{layer_bars}</div>
  <p><a href="model-{m['id']}.html">View model →</a></p>
</div>'''
        model_cards.append(card)
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ArchiMate Models — RegenTribes</title>
  <link rel="stylesheet" href="assets/style.css">
  {THEME_SCRIPT}
  <style>
    .model-card {{ background: var(--feature-bg); border: 1px solid var(--feature-border); border-radius: 4px; padding: 1.25rem; margin-bottom: 1rem; }}
    .model-card h2 {{ margin: 0 0 0.5rem; font-size: 1.1rem; }}
    .model-card h2 a {{ color: var(--heading); text-decoration: none; }}
    .model-card h2 a:hover {{ color: var(--text); }}
    .model-meta {{ display: flex; gap: 1rem; font-size: 0.8rem; color: var(--muted); margin-bottom: 0.5rem; }}
    .model-layers {{ display: flex; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 0.75rem; }}
    .layer-tag {{ background: var(--bg); border: 1px solid var(--border); padding: 2px 8px; border-radius: 10px; font-size: 0.72rem; color: var(--muted); }}
  </style>
</head>
<body>
{SITE_HEADER}
<main>
  <h1 style="color:var(--heading);margin-bottom:2rem;">Archimate Models</h1>
  <p style="color:var(--muted);margin-bottom:2.5rem;">Enterprise architecture models for regenerative communities and Integral Collective nodes. Click a model to explore its layers, elements, and relationships.</p>
  {"".join(model_cards)}
</main>
{SITE_FOOTER}
</body>
</html>'''
    
    return html


def generate_model_page(model):
    """Generate individual model page with layer breakdown."""
    layer_details = []
    for layer_name, count in model['layers'].items():
        if count > 0:
            layer_details.append(f'<li><strong>{layer_name.title()}</strong>: {count} elements</li>')
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{model['name']} — ArchiMate Model</title>
  <link rel="stylesheet" href="assets/style.css">
  {THEME_SCRIPT}
  <style>
    .model-header {{ background: var(--feature-bg); border: 1px solid var(--feature-border); border-radius: 4px; padding: 1.5rem; margin-bottom: 1.5rem; }}
    .model-header h1 {{ color: var(--heading); margin: 0 0 0.5rem; }}
    .stats-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin: 1rem 0; }}
    .stat {{ background: var(--bg); border: 1px solid var(--border); padding: 0.75rem; border-radius: 4px; text-align: center; }}
    .stat .num {{ font-size: 1.5rem; font-weight: 600; color: var(--heading); }}
    .stat .label {{ font-size: 0.75rem; color: var(--muted); text-transform: uppercase; letter-spacing: 0.05em; }}
    .layer-list {{ list-style: none; padding: 0; }}
    .layer-list li {{ padding: 0.5rem 0; border-bottom: 1px solid var(--border); }}
    .layer-list li:last-child {{ border-bottom: none; }}
  </style>
</head>
<body>
{SITE_HEADER}
<main>
  <p style="margin-bottom:1.5rem;"><a href="index.html" style="color:var(--muted);">← All Models</a></p>

  <div class="model-header">
    <h1>{model['name']}</h1>
    <p style="color:var(--muted);font-size:0.85rem;">Version {model['version']} · ID: {model['id']}</p>
    
    <div class="stats-grid">
      <div class="stat"><div class="num">{sum(model['layers'].values())}</div><div class="label">Elements</div></div>
      <div class="stat"><div class="num">{model['relationships']}</div><div class="label">Relationships</div></div>
      <div class="stat"><div class="num">{model['views']}</div><div class="label">Views</div></div>
    </div>
  </div>

  <h2 style="color:var(--heading);margin-bottom:1rem;">Layers</h2>
  <ul class="layer-list">
    {"".join(layer_details)}
  </ul>

  <h2 style="color:var(--heading);margin:1.5rem 0 1rem;">Architecture Notes</h2>
  <p style="color:var(--text);">This model represents the {model['name']} architecture for regenerative community operations. Use the views to navigate between motivation, strategy, business, application, technology, and implementation layers.</p>
</main>
{SITE_FOOTER}
</body>
</html>'''
    
    return html


def build():
    """Main build function."""
    print("Building ArchiMate exports...")
    
    # Create output dirs
    EXPORTS_DIR.mkdir(exist_ok=True)
    SITE_DIR.mkdir(exist_ok=True)
    
    # Copy assets
    if ASSETS_DIR.exists():
        site_assets = SITE_DIR / "assets"
        site_assets.mkdir(exist_ok=True)
        for f in ASSETS_DIR.glob("*"):
            shutil.copy2(f, site_assets / f.name)
        print(f"  [✓] Assets copied")
    
    # Find all .archimate files
    archimate_files = list(MODELS_DIR.rglob("*.archimate"))
    print(f"  Found {len(archimate_files)} model files")
    
    models = []
    for fp in archimate_files:
        rel_path = fp.relative_to(MODELS_DIR)
        model = parse_archimate_model(fp)
        if model:
            model['id'] = str(rel_path).replace('/', '-').replace('\\', '-').replace('.archimate', '')
            models.append(model)
            
            # Generate model page
            html = generate_model_page(model)
            SITE_DIR.joinpath(f"model-{model['id']}.html").write_text(html, encoding="utf-8")
            
            print(f"  [✓] {fp.name} → {sum(model['layers'].values())} elements, {model['relationships']} rels")
    
    # Generate index
    index_html = generate_model_index(models)
    SITE_DIR.joinpath("index.html").write_text(index_html, encoding="utf-8")
    
    # Docker export if available
    if docker_available():
        print("\n  [*] Running Docker export...")
        try:
            subprocess.run([
                "docker", "run", "--rm",
                "-v", f"{MODELS_DIR.absolute()}:/archi/project",
                "-v", f"{EXPORTS_DIR.absolute()}:/archi/report",
                "-e", f"ARCHI_PROJECT_PATH=/archi/project",
                "-e", "ARCHI_HTML_REPORT_ENABLED=true",
                "-e", "ARCHI_EXPORT_MODEL_ENABLED=true",
                ARCHIMATE_DOCKER
            ], check=True, timeout=300)
            print("  [✓] Docker export complete")
        except Exception as e:
            print(f"  [!] Docker export skipped: {e}")
    else:
        print("\n  [!] Docker not available — building static pages only")
        print("      Install Docker and pull ghcr.io/woozymasta/archimate-ci-image:5.7.0-1.0.6 for full exports")
    
    print(f"\nBuilt {len(models)} models → {SITE_DIR}/")
    print(f"Index: {SITE_DIR}/index.html")


if __name__ == "__main__":
    build()