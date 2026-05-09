#!/usr/bin/env python3
"""Build models.html with model cards linking to HTML viewers."""
from pathlib import Path

MODELS = {
    "regen-neighbourhood": {
        "title": "Regenerative Neighbourhood",
        "desc": "Physical, knowledge, and governance infrastructure for regenerative communities.",
        "color": "#4a9eff",
    },
    "integral-collective": {
        "title": "Integral Collective Node",
        "desc": "OAD → ITC → CDS → COS → FRS five-subsystem governance loop.",
        "color": "#50c878",
    },
    "ai-skills-dev": {
        "title": "AI Skills Development",
        "desc": "Community AI skills verification system aligned with NVIDIA certification tiers.",
        "color": "#ffa500",
    },
}

cards = []
for slug, meta in MODELS.items():
    cards.append(f"""<a class="model-card" href="model-{slug}.html" style="--accent:{meta['color']}">
  <div class="card-inner">
    <h2>{meta["title"]}</h2>
    <p>{meta["desc"]}</p>
    <span class="cta">Open viewer &#8594;</span>
  </div>
</a>""")

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ArchiMate Models — RegenTribes</title>
  <style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
:root{{--bg:#000;--text:#888;--heading:#fff;--muted:#555;--border:#222}}
body{{background:var(--bg);color:var(--text);font-family:system-ui,-apple-system,sans-serif;min-height:100vh;line-height:1.6}}
header{{border-bottom:1px solid var(--border);padding:2rem;text-align:center}}
header h1{{color:var(--heading);font-size:1.4rem;margin-bottom:.4rem}}
header p{{color:var(--muted);font-size:.875rem}}
main{{max-width:960px;margin:0 auto;padding:2.5rem 2rem 4rem}}
h2.section{{color:var(--heading);font-size:.75rem;font-weight:500;text-transform:uppercase;letter-spacing:.1em;margin-bottom:1.5rem}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:1.25rem}}
.model-card{{background:#0a0a0a;border:1px solid var(--border);border-radius:6px;text-decoration:none;transition:border-color .2s,transform .15s;display:block}}
.model-card:hover{{border-color:var(--accent,#4a9eff);transform:translateY(-2px)}}
.card-inner{{padding:1.5rem}}
.model-card h2{{color:var(--heading);font-size:1rem;margin-bottom:.5rem}}
.model-card p{{color:var(--text);font-size:.85rem;margin-bottom:1rem;line-height:1.5}}
.cta{{color:var(--accent,#4a9eff);font-size:.85rem}}
footer{{border-top:1px solid var(--border);padding:1.5rem 2rem;text-align:center;color:var(--muted);font-size:.8rem}}
@media(max-width:600px){{main{{padding:1.5rem 1rem 3rem}}}}
  </style>
</head>
<body>
  <header>
    <h1>ArchiMate Models</h1>
    <p>Enterprise architecture rendered by Archi v5.7.0</p>
  </header>
  <main>
    <h2 class="section">Community Models</h2>
    <div class="grid">
      {"".join(cards)}
    </div>
  </main>
  <footer>genesis-zero-bot-arch — Archi reports via archimate-ci-image</footer>
</body>
</html>"""

Path(__file__).parent.joinpath("models.html").write_text(html)
print("Generated models.html")
