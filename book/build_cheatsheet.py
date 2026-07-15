"""
Genera book/cheatsheet.html i book/cheatsheet.md a partir de cheatsheet-data.json.

HTML: una pàgina amb cerca local (filtre per text) i botons copiar.
MD: una pàgina Markdown imprimible amb totes les comandes agrupades.
"""
import json
from pathlib import Path
from collections import defaultdict

BOOK = Path(r"C:\Users\iadmin\bernatlab\book")
data = json.loads((BOOK / "cheatsheet-data.json").read_text(encoding="utf-8"))

# ---------- HTML ----------
html = """<!DOCTYPE html>
<html lang="ca">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>BernatLab · Chuleta de comandes</title>
<style>
:root {
    --bg: #0f1115;
    --bg-card: #1a1d24;
    --bg-code: #0d1117;
    --fg: #e6e6e6;
    --fg-dim: #9aa3b2;
    --accent: #7fc3a0;
    --border: #2a2f3a;
    --highlight: #ffd966;
}
* { box-sizing: border-box; }
body {
    margin: 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;
    background: var(--bg);
    color: var(--fg);
    line-height: 1.5;
}
header {
    position: sticky;
    top: 0;
    background: var(--bg);
    border-bottom: 1px solid var(--border);
    padding: 1rem 1.5rem;
    z-index: 10;
    backdrop-filter: blur(8px);
}
h1 {
    margin: 0 0 0.5rem 0;
    font-size: 1.5rem;
    color: var(--accent);
}
.subtitle {
    color: var(--fg-dim);
    font-size: 0.9rem;
    margin-bottom: 1rem;
}
.hort-banner {
    background: linear-gradient(135deg, rgba(127, 195, 160, 0.1), rgba(58, 90, 58, 0.2));
    border: 1px solid rgba(127, 195, 160, 0.3);
    border-left: 4px solid var(--accent);
    padding: 0.7rem 1rem;
    border-radius: 6px;
    margin-bottom: 1rem;
    font-size: 0.9rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.hort-banner a {
    color: var(--accent);
    text-decoration: none;
    font-weight: 600;
    border-bottom: 1px dashed var(--accent);
}
.hort-banner a:hover {
    border-bottom-style: solid;
}
.search-box {
    width: 100%;
    padding: 0.6rem 0.9rem;
    font-size: 1rem;
    background: var(--bg-card);
    color: var(--fg);
    border: 1px solid var(--border);
    border-radius: 6px;
    outline: none;
    font-family: inherit;
}
.search-box:focus {
    border-color: var(--accent);
}
main {
    padding: 1.5rem;
    max-width: 1100px;
    margin: 0 auto;
}
.category {
    margin-bottom: 2rem;
}
.category h2 {
    color: var(--accent);
    border-bottom: 1px solid var(--border);
    padding-bottom: 0.4rem;
    margin-bottom: 1rem;
    font-size: 1.2rem;
}
.category-count {
    color: var(--fg-dim);
    font-size: 0.85rem;
    font-weight: normal;
    margin-left: 0.5rem;
}
.cmd {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 6px;
    margin-bottom: 0.6rem;
    overflow: hidden;
    transition: border-color 0.15s;
}
.cmd:hover {
    border-color: var(--accent);
}
.cmd-main {
    display: flex;
    align-items: stretch;
    gap: 0.5rem;
}
pre {
    margin: 0;
    padding: 0.7rem 0.9rem;
    background: var(--bg-code);
    color: var(--fg);
    font-family: "SF Mono", "Cascadia Code", "Consolas", "Courier New", monospace;
    font-size: 0.85rem;
    flex: 1;
    overflow-x: auto;
    white-space: pre;
    line-height: 1.4;
}
.copy-btn {
    background: var(--bg-card);
    color: var(--fg-dim);
    border: none;
    border-left: 1px solid var(--border);
    padding: 0 0.8rem;
    cursor: pointer;
    font-size: 0.75rem;
    font-family: inherit;
    transition: background 0.15s;
}
.copy-btn:hover {
    background: var(--accent);
    color: var(--bg);
}
.cmd-meta {
    padding: 0.3rem 0.9rem;
    font-size: 0.75rem;
    color: var(--fg-dim);
    background: rgba(255,255,255,0.02);
    border-top: 1px solid var(--border);
}
.cmd-meta .topic {
    color: var(--accent);
    margin-right: 0.5rem;
}
.empty {
    color: var(--fg-dim);
    text-align: center;
    padding: 3rem 1rem;
    font-style: italic;
}
mark {
    background: var(--highlight);
    color: var(--bg);
    padding: 0 2px;
    border-radius: 2px;
}
footer {
    text-align: center;
    color: var(--fg-dim);
    font-size: 0.8rem;
    padding: 2rem 1rem;
    border-top: 1px solid var(--border);
    margin-top: 2rem;
}
@media (max-width: 600px) {
    pre { font-size: 0.78rem; }
    h1 { font-size: 1.2rem; }
}
</style>
</head>
<body>
<header>
    <h1>📋 BernatLab · Chuleta de comandes</h1>
    <div class="subtitle">""" + str(sum(len(v) for v in data.values())) + """ comandes extretes dels 7 mòduls del manual. Cerca amb <kbd>Ctrl+F</kbd> o el quadre de cerca.</div>
    <div class="hort-banner">
        <span>🌱</span>
        <span>El BernatLab alimenta la web pública <a href="https://bernatmora.github.io/hort-osona/" target="_blank" rel="noopener">Hort Osona</a>, on es publiquen les dades dels sensors del teu hort.</span>
    </div>
    <input type="text" id="search" class="search-box" placeholder="Cerca comandes (per text, categoria, tema...)" autofocus>
</header>
<main id="main">
"""

# Categories amb les seves comandes
for cat in sorted(data.keys()):
    cmds = data[cat]
    html += f'<div class="category" data-cat="{cat}">\n'
    html += f'<h2>{cat} <span class="category-count">({len(cmds)} comandes)</span></h2>\n'
    for item in cmds:
        cmd_esc = item["cmd"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
        html += f'<div class="cmd" data-text="{cat} {item["topic"]} {item["cmd"]}">\n'
        html += '  <div class="cmd-main">\n'
        html += f'    <pre>{cmd_esc}</pre>\n'
        html += f'    <button class="copy-btn" data-cmd="{cmd_esc}">Copiar</button>\n'
        html += '  </div>\n'
        html += f'  <div class="cmd-meta"><span class="topic">{item["topic"]}</span>Capítol {item["cap"]}</div>\n'
        html += '</div>\n'
    html += '</div>\n'

html += """</main>
<footer>
    <p>Generada automàticament des dels capítols del BernatLab · <a href="index.html">Tornar a la wiki</a> · <a href="https://github.com/BernatMora/bernatlab">Repo a GitHub</a></p>
</footer>
<script>
// Cerca instantània
const search = document.getElementById('search');
const cmds = document.querySelectorAll('.cmd');
const categories = document.querySelectorAll('.category');
search.addEventListener('input', () => {
    const q = search.value.toLowerCase().trim();
    let visibleCount = 0;
    cmds.forEach(el => {
        const text = el.dataset.text.toLowerCase();
        const matches = !q || text.includes(q);
        el.style.display = matches ? '' : 'none';
        if (matches) visibleCount++;
    });
    // Amagar categories buides
    categories.forEach(cat => {
        const any = Array.from(cat.querySelectorAll('.cmd')).some(c => c.style.display !== 'none');
        cat.style.display = any ? '' : 'none';
    });
});

// Copiar comanda
document.addEventListener('click', e => {
    if (e.target.classList.contains('copy-btn')) {
        const cmd = e.target.dataset.cmd;
        // El text ve amb HTML entities escapades
        const decoded = cmd.replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"');
        navigator.clipboard.writeText(decoded).then(() => {
            const orig = e.target.textContent;
            e.target.textContent = '✓ Copiat!';
            setTimeout(() => { e.target.textContent = orig; }, 1200);
        });
    }
});

// Drecera Ctrl+K per anar a la cerca
document.addEventListener('keydown', e => {
    if (e.ctrlKey && e.key === 'k') {
        e.preventDefault();
        search.focus();
    }
});
</script>
</body>
</html>
"""

(BOOK / "cheatsheet.html").write_text(html, encoding="utf-8")

# ---------- Markdown ----------
md_lines = [
    "# BernatLab · Chuleta de comandes",
    "",
    f"Chuleta ràpida amb les {sum(len(v) for v in data.values())} comandes més útils",
    "extretes dels 7 mòduls del manual. Útil per imprimir o per tenir a mà",
    "quan treballes a la RPi.",
    "",
    "Versió web amb cerca i botons de copiar: [`book/cheatsheet.html`](./cheatsheet.html)",
    "",
    "---",
    "",
]

for cat in sorted(data.keys()):
    cmds = data[cat]
    md_lines.append(f"## {cat} ({len(cmds)} comandes)")
    md_lines.append("")
    for item in cmds:
        # Codi amb marca del capítol
        md_lines.append(f"```{item['cmd']}```")
        md_lines.append(f"_{item['topic']} · Cap {item['cap']}_")
        md_lines.append("")

(BOOK / "cheatsheet.md").write_text("\n".join(md_lines), encoding="utf-8")

nl = "\n"
print(f"OK cheatsheet.html ({len(html):,} bytes)")
print(f"OK cheatsheet.md ({len(nl.join(md_lines)):,} chars)")
