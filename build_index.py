#!/usr/bin/env python3
"""
Build custom index page for ArchiMate models.
Outputs to _site/index.html.

Replaces embed-iframe approach with clean directory navigation:
- One card per model, linking to the full Archi viewer
- Cards for PDF/DOCX exports
- Optional dedicated viewer page (viewer.html) for embedded browsing
"""
import re
from pathlib import Path

model_count = len(list(Path("models").glob("*.archimate")))

html = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ArchiMate Models — RegenTribes</title>
<style>
:root{--bg:#000;--text:#888;--heading:#fff;--muted:#555;--border:#222;--code-bg:#0a0a0a}
body{background:var(--bg);color:var(--text);font-family:system-ui,sans-serif;margin:0;padding:2rem;transition:background .2s,color .2s}
.light{--bg:#fff;--text:#333;--heading:#000;--muted:#888;--border:#e0e0e0;--code-bg:#f5f5f5}
a{color:#4a9eff;text-decoration:none}
a:hover{text-decoration:underline}
h1{color:var(--heading);margin:0 0 1rem;font-size:1.6rem}
h2{color:var(--heading);margin:2rem 0 1rem;font-size:1.1rem}
p{color:var(--muted);margin:0 0 1.5rem;font-size:0.9rem}
nav{margin-bottom:2rem;display:flex;gap:1rem;align-items:center}
button{background:var(--border);color:var(--text);border:1px solid var(--muted);padding:.3rem .8rem;cursor:pointer;border-radius:4px}
.card{background:var(--code-bg);border:1px solid var(--border);padding:1.25rem;border-radius:4px;transition:border-color .2s}
.card:hover{border-color:var(--muted)}
.card h3{color:var(--heading);margin:0 0 .4rem;font-size:1rem}
.card p{color:var(--muted);margin:0;font-size:0.85rem}
.card a{display:block;color:#4a9eff;font-size:0.82rem;margin-top:.5rem}
.card a:hover{text-decoration:underline}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:1rem;margin:1rem 0}
.section{margin-bottom:2.5rem}
.badge{display:inline-block;background:var(--border);color:var(--muted);font-size:.7rem;padding:1px 8px;border-radius:10px;margin-bottom:.5rem}
footer{border-top:1px solid var(--border);padding:1.5rem 0;margin-top:3rem;color:var(--muted);font-size:.8rem}
footer a{color:var(--muted)}
</style>
<script>
document.addEventListener("DOMContentLoaded",function(){
  var t=localStorage.getItem("theme")||"dark";
  document.body.className=t;
});
</script>
</head>
<body>
<nav>
  <button onclick="document.body.className=document.body.className==='dark'?'light':'dark';localStorage.setItem('theme',document.body.className)">&#9790;</button>
  <a href="index.html" style="color:#4a9eff;font-size:.85rem">&#8594; Open full Archi viewer</a>
</nav>

<h1>ArchiMate Models — RegenTribes</h1>
<p>Enterprise architecture models rendered by Archi v5.7.0 via archimate-ci-image.</p>

<div class="section">
  <span class="badge">Own Models</span>
  <div class="grid">
    <div class="card">
      <h3>Regenerative Neighbourhood</h3>
      <p>Physical, knowledge, and governance infrastructure for regenerative communities.</p>
      <a href="index.html">&#8594; Open in Archi viewer</a>
      <a href="ArchiMetal.pdf">&#8595; PDF Report</a>
      <a href="ArchiMetal.docx">&#8595; DOCX Report</a>
    </div>
    <div class="card">
      <h3>Integral Collective Node</h3>
      <p>OAD → ITC → CDS → COS → FRS five-subsystem governance loop.</p>
      <a href="index.html">&#8594; Open in Archi viewer</a>
      <a href="ArchiMetal.pdf">&#8595; PDF Report</a>
      <a href="ArchiMetal.docx">&#8595; DOCX Report</a>
    </div>
  </div>
</div>

<div class="section">
  <span class="badge">ArchiMetal Reference Model</span>
  <div class="card" style="max-width:600px">
    <h3>ArchiMetal (archimate-ci-image example)</h3>
    <p>Full ArchiMate model demonstrating the archimate-ci-image report generation.</p>
    <a href="index.html">&#8594; Open in Archi viewer</a>
    <a href="ArchiMetal.pdf">&#8595; PDF Report</a>
    <a href="ArchiMetal.docx">&#8595; DOCX Report</a>
  </div>
</div>

<footer>
  <a href="https://github.com/regentribes/genesis-zero-bot-arch">genesis-zero-bot-arch</a>
  — Archi HTML reports via
  <a href="https://github.com/marketplace/actions/deploy-archi-report">deploy-archi-report</a>
  (WoozyMasta/archimate-ci-image@5.7.0-1.0.6)
</footer>
</body>
</html>'''

Path("_site/index.html").write_text(html)
print(f"Custom index written: {model_count} models")