"""
Genera book/glossari.html a partir de book/glossari.md.

Estil consistent amb book/cheatsheet.html (dark theme, accent verd BernatLab).
Afegeix:
  - TOC lateral automatic a partir dels H2
  - Cerca filtrant entrades (.term h3 + el parraf seguent + l'exemple)
  - Ancoratges als H2 / H3 per enllac directe
"""
from __future__ import annotations

import re
from pathlib import Path

import markdown

ROOT = Path(__file__).parent
SRC = ROOT / "glossari.md"
DST = ROOT / "glossari.html"


def slugify(text: str) -> str:
    s = text.lower()
    s = re.sub(r"[^\w\s-]", "", s, flags=re.UNICODE)
    s = re.sub(r"\s+", "-", s.strip())
    return s


def build_toc(md_text: str) -> tuple[str, list[tuple[str, str, str]]]:
    """Retorna (md amb ancoratges, llista de (nivell, text, slug))."""
    toc: list[tuple[str, str, str]] = []
    lines = md_text.splitlines()
    out: list[str] = []
    in_code = False
    for line in lines:
        if line.startswith("```"):
            in_code = not in_code
            out.append(line)
            continue
        if in_code:
            out.append(line)
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            hashes, text = m.group(1), m.group(2).strip()
            level = len(hashes)
            if level in (2, 3):
                slug = slugify(text)
                toc.append((str(level), text, slug))
                out.append(f"{hashes} {text} {{ #{slug} }}")
                continue
        out.append(line)
    return "\n".join(out), toc


def render_toc_html(toc: list[tuple[str, str, str]]) -> str:
    parts = ['<nav class="toc" aria-label="Taula de continguts">']
    parts.append("<h2>Index</h2>")
    parts.append('<input type="search" id="filter" placeholder="Cerca un terme..." aria-label="Filtrar termes">')
    parts.append("<ul>")
    for level, text, slug in toc:
        if level == "2":
            parts.append(
                f'<li class="lvl2"><a href="#{slug}">{text}</a></li>'
            )
    parts.append("</ul>")
    parts.append("</nav>")
    return "\n".join(parts)


def main() -> None:
    md_src = SRC.read_text(encoding="utf-8")
    md_with_ids, toc = build_toc(md_src)

    body_html = markdown.markdown(
        md_with_ids,
        extensions=["fenced_code", "tables", "sane_lists"],
        output_format="html5",
    )

    # Forcem que els termes (H3) tinguin classe per a la cerca
    # i netegem qualsevol { #slug } que hagi quedat dins del text.
    def _clean_h3(m: "re.Match[str]") -> str:
        attrs = m.group(1)
        inner = m.group(2)
        inner = re.sub(r"\s*\{\s*#[^}]+\}\s*", "", inner)
        return f'<h3 class="term"{attrs}>{inner}</h3>'

    body_html = re.sub(
        r"<h3([^>]*)>(.*?)</h3>",
        _clean_h3,
        body_html,
        flags=re.DOTALL,
    )
    # Igual per H2.
    def _clean_h2(m: "re.Match[str]") -> str:
        attrs = m.group(1)
        inner = m.group(2)
        inner = re.sub(r"\s*\{\s*#[^}]+\}\s*", "", inner)
        return f'<h2{attrs}>{inner}</h2>'

    body_html = re.sub(
        r"<h2([^>]*)>(.*?)</h2>",
        _clean_h2,
        body_html,
        flags=re.DOTALL,
    )
    # Els exemples que comencen amb **Al BernatLab:** els marquem.
    body_html = re.sub(
        r'<p>\*\*Al BernatLab:\*\*',
        r'<p class="exemple"><strong>Al BernatLab:</strong>',
        body_html,
    )
    body_html = re.sub(
        r'<p><strong>Veure:</strong>',
        r'<p class="veure"><strong>Veure:</strong>',
        body_html,
    )

    toc_html = render_toc_html(toc)

    title = "BernatLab · Glossari"

    html = f"""<!DOCTYPE html>
<html lang="ca">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
:root {{
    --bg: #0f1115;
    --bg-card: #1a1d24;
    --bg-code: #0d1117;
    --fg: #e6e6e6;
    --fg-dim: #9aa3b2;
    --accent: #7fc3a0;
    --accent-strong: #5da784;
    --border: #2a2f3a;
    --highlight: #ffd966;
    --warn: #e6a23c;
    --exemple-bg: rgba(127, 195, 160, 0.06);
}}
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; padding: 0; }}
body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;
    background: var(--bg);
    color: var(--fg);
    line-height: 1.6;
}}
header {{
    position: sticky; top: 0; z-index: 20;
    background: rgba(15, 17, 21, 0.92);
    border-bottom: 1px solid var(--border);
    padding: 1rem 1.5rem;
    backdrop-filter: blur(8px);
}}
h1 {{
    margin: 0 0 0.4rem 0;
    font-size: 1.6rem;
    color: var(--accent);
}}
header .subtitle {{
    color: var(--fg-dim);
    font-size: 0.9rem;
}}
.layout {{
    display: grid;
    grid-template-columns: 280px minmax(0, 1fr);
    gap: 0;
}}
@media (max-width: 900px) {{
    .layout {{ grid-template-columns: 1fr; }}
    nav.toc {{ position: static !important; height: auto !important; border-right: 0 !important; border-bottom: 1px solid var(--border); }}
}}
nav.toc {{
    position: sticky; top: 88px; align-self: start;
    height: calc(100vh - 100px);
    overflow-y: auto;
    padding: 1.5rem 1.2rem;
    border-right: 1px solid var(--border);
    background: var(--bg);
}}
nav.toc h2 {{
    margin: 0 0 0.8rem 0;
    font-size: 1rem;
    color: var(--fg-dim);
    text-transform: uppercase;
    letter-spacing: 0.05em;
}}
nav.toc input[type="search"] {{
    width: 100%;
    padding: 0.5rem 0.7rem;
    background: var(--bg-card);
    color: var(--fg);
    border: 1px solid var(--border);
    border-radius: 6px;
    font-size: 0.9rem;
    margin-bottom: 1rem;
}}
nav.toc input[type="search"]:focus {{
    outline: none;
    border-color: var(--accent);
}}
nav.toc ul {{
    list-style: none;
    padding: 0;
    margin: 0;
}}
nav.toc li.lvl2 {{
    margin: 0.15rem 0;
}}
nav.toc a {{
    color: var(--fg);
    text-decoration: none;
    display: block;
    padding: 0.35rem 0.6rem;
    border-radius: 4px;
    font-size: 0.92rem;
    border-left: 2px solid transparent;
    transition: background 0.15s, border-color 0.15s;
}}
nav.toc a:hover {{
    background: var(--bg-card);
    border-left-color: var(--accent);
}}
main {{
    padding: 1.5rem 2rem 4rem;
    max-width: 920px;
}}
main h1, main h2 {{
    border-bottom: 1px solid var(--border);
    padding-bottom: 0.3rem;
}}
main h2 {{
    margin-top: 2.5rem;
    color: var(--accent);
    font-size: 1.4rem;
    scroll-margin-top: 100px;
}}
main h3.term {{
    margin-top: 1.6rem;
    color: var(--accent-strong);
    font-size: 1.05rem;
    border-left: 3px solid var(--accent);
    padding-left: 0.6rem;
    scroll-margin-top: 100px;
}}
main p {{
    margin: 0.5rem 0;
}}
main p.exemple {{
    background: var(--exemple-bg);
    border-left: 3px solid var(--accent);
    padding: 0.5rem 0.8rem;
    border-radius: 0 6px 6px 0;
    margin: 0.5rem 0 0.6rem 0;
    font-size: 0.95rem;
}}
main p.veure {{
    color: var(--fg-dim);
    font-size: 0.88rem;
    font-style: italic;
    margin: 0.2rem 0 1.4rem 0;
}}
main code {{
    background: var(--bg-code);
    padding: 0.1rem 0.35rem;
    border-radius: 3px;
    font-size: 0.88em;
    border: 1px solid var(--border);
}}
main pre {{
    background: var(--bg-code);
    padding: 0.8rem 1rem;
    border-radius: 6px;
    overflow-x: auto;
    border: 1px solid var(--border);
}}
main blockquote {{
    border-left: 3px solid var(--border);
    margin: 0.8rem 0;
    padding: 0.4rem 1rem;
    color: var(--fg-dim);
}}
main hr {{
    border: 0;
    border-top: 1px solid var(--border);
    margin: 2rem 0;
}}
main a {{ color: var(--accent); text-decoration: none; }}
main a:hover {{ text-decoration: underline; }}
mark.hl {{
    background: var(--highlight);
    color: #1a1d24;
    padding: 0 2px;
    border-radius: 2px;
}}
.hidden {{ display: none !important; }}
footer {{
    text-align: center;
    color: var(--fg-dim);
    font-size: 0.85rem;
    padding: 2rem 1rem;
    border-top: 1px solid var(--border);
    margin-top: 3rem;
}}
</style>
</head>
<body>
<header>
    <h1>BernatLab &middot; Glossari</h1>
    <div class="subtitle">Tots els termes tecnics del projecte, explicats en catala. Cerca al panell lateral.</div>
</header>
<div class="layout">
{toc_html}
<main>
{body_html}
</main>
</div>
<footer>
    Generat automaticament a partir de <code>book/glossari.md</code> &middot; BernatLab
</footer>
<script>
(function () {{
    // Filtre de termes (cerca al panell lateral + marcar coincidencies al main).
    const filter = document.getElementById('filter');
    const main = document.querySelector('main');
    if (!filter || !main) return;

    const items = Array.from(main.querySelectorAll('h3.term'));

    // Agrupem cada terme amb el seu paragraf d'exemple i "veure" seguent.
    const groups = items.map((h) => {{
        const group = [h];
        let n = h.nextElementSibling;
        let safety = 6;
        while (n && safety-- > 0) {{
            if (n.tagName === 'H3' || n.tagName === 'H2') break;
            group.push(n);
            n = n.nextElementSibling;
        }}
        return group;
    }});

    function clearHighlights() {{
        main.querySelectorAll('mark.hl').forEach((m) => {{
            const t = document.createTextNode(m.textContent);
            m.parentNode.replaceChild(t, m);
        }});
    }}

    function highlight(text) {{
        if (!text) return;
        const walker = document.createTreeWalker(main, NodeFilter.SHOW_TEXT);
        const nodes = [];
        let n;
        while ((n = walker.nextNode())) nodes.push(n);
        const re = new RegExp(text.replace(/[.*+?^${{}}()|[\\]\\\\]/g, '\\\\$&'), 'gi');
        nodes.forEach((node) => {{
            if (!node.parentNode || node.parentNode.tagName === 'SCRIPT' || node.parentNode.tagName === 'STYLE') return;
            const m = node.nodeValue.match(re);
            if (!m) return;
            const span = document.createTextNode(node.nodeValue);
            let html = node.nodeValue;
            html = html.replace(re, (match) => `<mark class="hl">${{match}}</mark>`);
            const tmp = document.createElement('span');
            tmp.innerHTML = html;
            const frag = document.createDocumentFragment();
            while (tmp.firstChild) frag.appendChild(tmp.firstChild);
            node.parentNode.replaceChild(frag, node);
        }});
    }}

    filter.addEventListener('input', () => {{
        clearHighlights();
        const q = filter.value.trim().toLowerCase();
        groups.forEach((g) => {{
            const text = g.map((el) => el.textContent).join(' ').toLowerCase();
            const match = !q || text.includes(q);
            g.forEach((el) => el.classList.toggle('hidden', !match));
        }});
        if (q) highlight(q);
    }});
}})();
</script>
</body>
</html>
"""
    DST.write_text(html, encoding="utf-8")
    print(f"OK: {DST} ({DST.stat().st_size} bytes, {len(toc)} entrades TOC)")


if __name__ == "__main__":
    main()
