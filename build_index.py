#!/usr/bin/env python3
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
a{color:#4a9eff}
h1{color:var(--heading);margin:0 0 1rem}
h2{color:var(--heading);margin:2rem 0 .5rem;font-size:1.2rem}
p{color:var(--muted);margin:0 0 1.5rem}
nav{margin-bottom:2rem}
button{background:var(--border);color:var(--text);border:1px solid var(--muted);padding:.3rem .8rem;cursor:pointer}
iframe{width:100%;height:600px;border:1px solid var(--border);background:#fff;margin-top:1rem}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:1rem;margin:1rem 0}
.card{background:var(--code-bg);border:1px solid var(--border);padding:1rem;border-radius:4px}
.card h3{color:var(--heading);margin:0 0 .5rem;font-size:1rem}
.card p{color:var(--muted);margin:0}
</style>
<script>
document.addEventListener("DOMContentLoaded",function(){
  var t=localStorage.getItem("theme")||"dark";
  document.body.className=t;
});
</script>
</head>
<body>
<nav><button onclick="document.body.className=document.body.className==='dark'?'light':'dark';localStorage.setItem('theme',document.body.className)">&#9790;</button></nav>
<h1>ArchiMate Models — RegenTribes</h1>
<p>Enterprise architecture models. ''' + str(model_count) + ''' models. Archi v5.7.0 via archimate-ci-image.</p>

<h2>Regenerative Neighbourhood</h2>
<div class="grid">
  <div class="card"><h3>Core Architecture</h3><p>Physical, knowledge, and governance infrastructure for regenerative communities.</p></div>
</div>
<iframe src="html/index.html?model=regen-neighbourhood" title="Regen Neighbourhood"></iframe>

<h2>Integral Collective Node</h2>
<div class="grid">
  <div class="card"><h3>OAD → ITC → CDS → COS → FRS</h3><p>Five-subsystem governance loop for regenerative community nodes.</p></div>
</div>
<iframe src="html/index.html?model=integral-collective" title="Integral Collective"></iframe>

<h2>Reference Models (archimate-ci-image)</h2>
<div class="grid">
  <div class="card"><h3>ArchiMetal Reference</h3><p>Full ArchiMate model demonstrating deploy-archi-report integration.</p></div>
</div>
<iframe src="html/index.html" title="ArchiMetal"></iframe>

<p style="margin-top:2rem;color:var(--muted);font-size:.85rem">
Built by <a href="https://github.com/regentribes/genesis-zero-bot-arch">genesis-zero-bot-arch</a>
— Archi HTML reports via <a href="https://github.com/marketplace/actions/deploy-archi-report">deploy-archi-report</a>
</p>
</body>
</html>'''

Path("_site/index.html").write_text(html)
print("Custom index written: " + str(model_count) + " models")
