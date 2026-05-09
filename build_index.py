#!/usr/bin/env python3
"""
Build custom index.html from models/ directory.
Generates models.html with model cards linking to HTML viewers + PDFs.
"""
import os, re
from pathlib import Path

MODELS_DIR = Path(__file__).parent / "models"
OUT = Path(__file__).parent / "models.html"

# Model metadata
MODELS = {
    "regen-neighbourhood": {
        "title": "Regenerative Neighbourhood",
        "desc": "Physical, knowledge, and governance infrastructure for regenerative communities.",
        "hash": "id-af41e8d15c6d4d3dba2672387862904c",
    },
    "integral-collective": {
        "title": "Integral Collective Node",
        "desc": "OAD → ITC → CDS → COS → FRS five-subsystem governance loop.",
        "hash": "id-291109ba69b34282a34bc0695e8c44a7",
    },
    "ai-skills-dev": {
        "title": "AI Skills Development",
        "desc": "Community AI skills verification system aligned with NVIDIA certification tiers.",
        "hash": "id-e5d8e6d7751e40b6ad09e1f9e0dcc0d6",
    },
}

def get_model_pdf(model):
    """Check if PDF exists for model."""
    pdf = MODELS_DIR / f"{model}.pdf"
    return f"models/{model}.pdf" if pdf.exists() else None

cards = []
for slug, meta in MODELS.items():
    pdf = get_model_pdf(slug)
    viewer_url = f"viewers/{slug}/index.html"
    pdf_url = f"models/{slug}.pdf" if pdf else None

    cards.append(f"""<div class="model-card">
  <h2>{meta["title"]}</h2>
  <p>{meta["desc"]}</p>
  <div class="model-links">
    <a href="{viewer_url}">&#8594; Open {meta["title"]} viewer</a>
    {f'<a href="{pdf_url}">&#8595; PDF Report</a>' if pdf_url else ''}
  </div>
</div>""")

content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ArchiMate Models — RegenTribes</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
<header>
  <h1>ArchiMate Models</h1>
  <p>Enterprise architecture models rendered by Archi v5.7.0 via archimate-ci-image.</p>
</header>
<main>
  <h2>Custom Models</h2>
  {"".join(cards)}
</main>
<footer>
  <p>genesis-zero-bot-arch — Archi HTML reports via deploy-archi-report (WoozyMasta/archimate-ci-image@5.7.0-1.0.6)</p>
</footer>
</body>
</html>"""

Path(OUT).write_text(content)
print(f"Generated {OUT}")
