#!/usr/bin/env python3
"""
build_wiki.py — Genera una wiki estàtica HTML a partir dels capítols Markdown.

Sortida: book/wiki/
  - index.html                    (portada amb índex de tots els mòduls)
  - modul-1.html .. modul-3.html  (un fitxer per mòdul amb tots els capítols)
  - css/wiki.css                  (estil comú)

Característiques:
  - HTML estàtic, allotjable a GitHub Pages.
  - Navegació lateral amb índex de capítols.
  - Cap dependència externa (només Python estàndard).
  - Es pot regenerar quan s'escriuen nous capítols.

Ús:
    python book/build_wiki.py
    python book/build_wiki.py --open  (obrir al navegador després de generar)
"""

import argparse
import html
import re
import sys
import webbrowser
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuració
# ---------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parent
CHAPTERS_DIR = ROOT / "chapters"
WIKI_DIR = ROOT / "wiki"

# Glossari global (termes clau → definició breu). Si volem ampliar, aquí.
GLOSSARY = {
    "Docker": "Plataforma de contenidors que permet empaquetar aplicacions amb les seves dependències.",
    "Docker Compose": "Eina per definir i executar múltiples contenidors Docker amb un sol fitxer YAML.",
    "Portainer": "Interfície web per gestionar Docker visualment.",
    "MQTT": "Protocol de missatgeria lleuger dissenyat per a dispositius IoT.",
    "Mosquitto": "Broker MQTT de codi obert, àmpliament utilitzat.",
    "InfluxDB": "Base de dades de sèries temporals optimitzada per a dades amb marca de temps.",
    "Telegraf": "Agent que recull mètriques i les envia a InfluxDB o altres.",
    "Node-RED": "Eina de programació visual basada en fluxos, ideal per a IoT.",
    "Grafana": "Plataforma de visualització i alertes per a dades temporals.",
    "LoRa": "Tecnologia de ràdio de llarg abast i baix consum (Long Range).",
    "LoRaWAN": "Protocol de xarxa que usa LoRa com a capa física, gestionat per un network server.",
    "LoRa P2P": "Comunicació LoRa directa entre dos dispositius, sense network server.",
    "TTN": "The Things Network, network server LoRaWAN comunitari i gratuït.",
    "Concentratord": "Programari per a gateways LoRaWAN basats en SX1302/SX1303.",
    "SX1262": "Xip transceiver LoRa de Semtech per a 868/915/923 MHz.",
    "SX1302": "Xip concentrador LoRa que pot rebre 8 canals simultàniament.",
    "ESP32": "Microcontrolador de baix cost amb Wi-Fi i Bluetooth, molt utilitzat en IoT.",
    "ESP32-S3": "Variant de l'ESP32 amb més potència i suport per a USB OTG.",
    "BME280": "Sensor digital que mesura temperatura, humitat i pressió.",
    "CayenneLPP": "Format de payload eficient per a LoRaWAN, basat en canals i tipus.",
    "RSSI": "Indicador de potència del senyal rebut, en dBm.",
    "SNR": "Relació senyal-soroll, en dB. Indica la qualitat del senyal.",
    "SF": "Spreading Factor. Com més alt, més abast però més lent.",
    "BW": "Bandwidth, amplada de banda del canal LoRa.",
    "OTAA": "Over-The-Air Activation, mètode recomanat d'unió a LoRaWAN.",
    "ABP": "Activation By Personalization, mètode alternatiu amb claus preconfigurades.",
    "DevEUI": "Identificador únic de 64 bits d'un dispositiu LoRaWAN.",
    "AppEUI": "Identificador de l'aplicació LoRaWAN a la qual pertany el node.",
    "AppKey": "Clau mestra de 128 bits per autenticar el node durant el join.",
    "Tailscale": "Xarxa privada basada en WireGuard que permet accedir a dispositius sense obrir ports.",
    "MagicDNS": "Servei DNS de Tailscale que resol noms dins del tailnet.",
    "Debian": "Distribució Linux estable i àmpliament utilitzada en servidors.",
    "systemd": "Sistema d'inicialització i gestió de serveis en Linux modern.",
    "systemctl": "Eina de línia d'ordres per gestionar serveis systemd.",
    "Homepage": "Dashboard modern per a serveis autoallotjats, configurable via YAML.",
    "Uptime Kuma": "Eina de monitoratge autoallotjada amb alertes per Telegram, correu, etc.",
    "Git": "Sistema de control de versions distribuït.",
    "commit": "Instantània dels canvis en un repositori Git.",
    "branch": "Línia de desenvolupament independent en Git.",
    "merge": "Combinar canvis d'una branca a una altra.",
    "pull request": "Proposta de canvis per revisar i fusionar en una branca.",
    "SSH": "Protocol segur per accedir a servidors remots.",
    "TLS": "Transport Layer Security, protocol de xifrat per a comunicacions.",
    "HTTPS": "HTTP sobre TLS, la versió segura del web.",
    "reverse proxy": "Servidor que rep peticions i les redirigeix a altres servidors.",
    "firewall": "Sistema que filtra el tràfic de xarxa segons regles.",
    "Ollama": "Aplicació de codi obert per executar models d'IA localment al teu Mac o PC.",
    "LLM": "Large Language Model, model de llengua gran entrenat per generar text.",
    "RAG": "Retrieval-Augmented Generation, tècnica que combina cerca de documents amb generació de text.",
    "embedding": "Representació numèrica d'un text que captura el seu significat.",
    "vectorstore": "Base de dades optimitzada per emmagatzemar i cercar vectors.",
    "ChromaDB": "Base vectorial de codi obert, simple d'utilitzar, ideal per a homelabs.",
    "FAISS": "Llibreria de Facebook per a cerca vectorial ràpida.",
    "Whisper": "Model d'OpenAI per transcriure àudio a text, multilingüe i en local.",
    "Piper": "Sistema de síntesi de veu local, lleuger i multilingüe.",
    "FastAPI": "Framework Python modern per construir APIs HTTP, ràpid i amb documentació automàtica.",
    "Quantització": "Tècnica per reduir la mida d'un model compriments els pesos en menys bits.",
}


# ---------------------------------------------------------------------------
# Parser Markdown minimalista (només el que usem al llibre)
# ---------------------------------------------------------------------------

def md_to_html(text: str) -> str:
    """Converteix Markdown a HTML. Implementació minimalista per a wiki."""

    # 1. Escapa HTML per defecte en blocs de codi
    #    (els gestionem per separat)
    lines = text.split('\n')
    out = []
    in_code = False
    code_buf = []
    code_lang = ''

    def flush_code():
        nonlocal code_buf
        if code_buf:
            esc = html.escape('\n'.join(code_buf))
            out.append(f'<pre class="code"><code class="language-{code_lang}">{esc}</code></pre>')
            code_buf = []

    for line in lines:
        if line.startswith('```'):
            if in_code:
                flush_code()
                in_code = False
            else:
                in_code = True
                code_lang = line[3:].strip()
        elif in_code:
            code_buf.append(line)
        else:
            out.append(line)
    if in_code:
        flush_code()

    text = '\n'.join(out)

    # 2. Capçaleres
    text = re.sub(r'^# (.+)$', r'<h1>\1</h1>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.+)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r'^### (.+)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)

    # 3. Negreta i cursiva
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)

    # 4. Links [text](url)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)

    # 5. Bloc Mermaid (es mostra com a text)
    text = re.sub(
        r'```mermaid\n(.*?)\n```',
        r'<pre class="mermaid">\1</pre>',
        text,
        flags=re.DOTALL,
    )

    # 6. Llistes (- o *)
    lines = text.split('\n')
    new_lines = []
    in_list = False
    for line in lines:
        m = re.match(r'^\s*[-*]\s+(.+)$', line)
        if m:
            if not in_list:
                new_lines.append('<ul>')
                in_list = True
            new_lines.append(f'<li>{m.group(1)}</li>')
        else:
            if in_list:
                new_lines.append('</ul>')
                in_list = False
            new_lines.append(line)
    if in_list:
        new_lines.append('</ul>')
    text = '\n'.join(new_lines)

    # 7. Paràgrafs (línies en blanc separen)
    paragraphs = re.split(r'\n\s*\n', text)
    final = []
    for p in paragraphs:
        p = p.strip()
        if not p:
            continue
        if p.startswith(('<h1', '<h2', '<h3', '<ul', '<pre', '<blockquote', '<hr')):
            final.append(p)
        else:
            final.append(f'<p>{p}</p>')
    return '\n'.join(final)


# ---------------------------------------------------------------------------
# Generació
# ---------------------------------------------------------------------------

CSS = """
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    line-height: 1.6;
    color: #222;
    max-width: 1100px;
    margin: 0 auto;
    padding: 0 20px;
    background: #fafafa;
}
.layout { display: flex; gap: 30px; }
nav {
    flex: 0 0 260px;
    background: #fff;
    padding: 20px;
    border-right: 1px solid #e0e0e0;
    height: 100vh;
    overflow-y: auto;
    position: sticky;
    top: 0;
}
nav h2 {
    font-size: 1.1em;
    margin-top: 1.5em;
    color: #1F3A5F;
    border-bottom: 1px solid #ddd;
    padding-bottom: 4px;
}
nav h2:first-child { margin-top: 0; }
nav a {
    display: block;
    padding: 4px 0;
    color: #333;
    text-decoration: none;
    font-size: 0.95em;
}
nav a:hover { color: #1F3A5F; text-decoration: underline; }
nav .toc-num { color: #888; margin-right: 6px; }
main { flex: 1; padding: 20px 0; max-width: 800px; background: #fff; padding: 30px; }
h1, h2, h3 { color: #1F3A5F; }
h1 { border-bottom: 2px solid #1F3A5F; padding-bottom: 8px; }
h2 { border-bottom: 1px solid #ddd; padding-bottom: 4px; margin-top: 2em; }
h3 { margin-top: 1.5em; }
pre.code, pre.mermaid {
    background: #1e1e1e;
    color: #d4d4d4;
    padding: 12px;
    border-radius: 4px;
    overflow-x: auto;
    font-size: 0.9em;
}
pre.mermaid { background: #f6f8fa; color: #333; }
code { background: #f0f0f0; padding: 1px 4px; border-radius: 3px; font-size: 0.9em; }
pre code { background: none; padding: 0; }
blockquote { border-left: 4px solid #1F3A5F; margin: 1em 0; padding: 0.5em 1em; color: #555; background: #f8f8f8; }
table { border-collapse: collapse; margin: 1em 0; }
th, td { border: 1px solid #ddd; padding: 6px 10px; }
th { background: #f0f0f0; }
hr { border: none; border-top: 1px solid #ddd; margin: 2em 0; }
ul, ol { padding-left: 1.5em; }
a { color: #1F3A5F; }
.glossary { font-size: 0.95em; }
.glossary dt { font-weight: bold; color: #1F3A5F; margin-top: 0.5em; }
.glossary dd { margin-left: 1em; color: #444; }
footer { color: #888; font-size: 0.9em; text-align: center; padding: 20px; }
"""


def render_module_page(module_label: str, module_subtitle: str,
                       chapters: list, all_modules_links: dict) -> str:
    """Genera la pàgina HTML d'un mòdul."""

    nav = ['<nav>']
    nav.append('<h2>BernatLab</h2>')
    nav.append('<p style="color: #888; font-size: 0.9em;">Wiki del manual tècnic</p>')
    for label, fname in all_modules_links.items():
        nav.append(f'<a href="{fname}">{label}</a>')
    nav.append('<h2>Capítols</h2>')
    for ch_file, ch_title in chapters:
        ch_id = Path(ch_file).stem
        # Comptar número a partir del nom (ex: 23-que-es-lora.md → 23)
        m = re.match(r'(\d+)-', ch_file)
        num = m.group(1) if m else "?"
        nav.append(
            f'<a href="#{ch_id}"><span class="toc-num">{num}</span>{ch_title}</a>'
        )
    nav.append('</nav>')

    main = ['<main>']
    main.append(f'<h1>{module_label}</h1>')
    main.append(f'<p><em>{html.escape(module_subtitle)}</em></p>')
    main.append('<hr>')

    for ch_file, ch_title in chapters:
        ch_path = CHAPTERS_DIR / ch_file
        ch_id = Path(ch_file).stem
        if not ch_path.exists():
            main.append(f'<h2 id="{ch_id}">{html.escape(ch_title)} ⚠️</h2>')
            main.append('<p><em>El fitxer d\'aquest capítol no existeix.</em></p>')
            continue
        content = ch_path.read_text(encoding='utf-8')
        # Treure la primera línia amb "# Capítol X — ..." perquè ja tenim el títol
        content = re.sub(r'^# .+\n', '', content, count=1)
        main.append(f'<h2 id="{ch_id}">{html.escape(ch_title)}</h2>')
        main.append(md_to_html(content))
        main.append('<hr>')
    main.append('</main>')

    return f'''<!DOCTYPE html>
<html lang="ca">
<head>
    <meta charset="UTF-8">
    <title>{html.escape(module_label)} — BernatLab Wiki</title>
    <link rel="stylesheet" href="css/wiki.css">
</head>
<body>
<div class="layout">
{chr(10).join(nav)}
{chr(10).join(main)}
</div>
<footer>
    BernatLab Wiki · Generada automàticament a partir dels capítols Markdown.
</footer>
</body>
</html>'''


def render_index(modules: list) -> str:
    """Genera la pàgina d'inici de la wiki."""

    nav = ['<nav>']
    nav.append('<h2>BernatLab</h2>')
    nav.append('<p style="color: #888; font-size: 0.9em;">Wiki del manual tècnic</p>')
    for label, fname, _ in modules:
        nav.append(f'<a href="{fname}">{label}</a>')
    nav.append('<h2>Glossari</h2>')
    nav.append('<a href="#glossari">Termes clau</a>')
    nav.append('</nav>')

    main = ['<main>']
    main.append('<h1>BernatLab — Wiki</h1>')
    main.append('<p>Documentació navegable del servidor personal BernatLab. '
                'Generada automàticament a partir del llibre tècnic.</p>')
    main.append('<h2>Mòduls disponibles</h2>')
    main.append('<ul>')
    for label, fname, sub in modules:
        main.append(
            f'<li><a href="{fname}"><strong>{html.escape(label)}</strong></a> '
            f'<em>— {html.escape(sub)}</em></li>'
        )
    main.append('</ul>')

    main.append('<h2 id="glossari">Glossari</h2>')
    main.append('<p>Termes clau del manual, en ordre alfabètic.</p>')
    main.append('<dl class="glossary">')
    for term, definition in sorted(GLOSSARY.items()):
        main.append(f'<dt>{html.escape(term)}</dt>')
        main.append(f'<dd>{html.escape(definition)}</dd>')
    main.append('</dl>')

    main.append('</main>')

    return f'''<!DOCTYPE html>
<html lang="ca">
<head>
    <meta charset="UTF-8">
    <title>BernatLab — Wiki</title>
    <link rel="stylesheet" href="css/wiki.css">
</head>
<body>
<div class="layout">
{chr(10).join(nav)}
{chr(10).join(main)}
</div>
<footer>
    BernatLab Wiki · Generada automàticament a partir dels capítols Markdown.
</footer>
</body>
</html>'''


def main():
    parser = argparse.ArgumentParser(description="Genera la wiki estàtica del BernatLab")
    parser.add_argument("--open", action="store_true", help="Obre al navegador després de generar")
    args = parser.parse_args()

    if not CHAPTERS_DIR.exists():
        print(f"ERROR: no trobo {CHAPTERS_DIR}")
        sys.exit(1)

    # Crear estructura
    WIKI_DIR.mkdir(exist_ok=True)
    (WIKI_DIR / "css").mkdir(exist_ok=True)
    (WIKI_DIR / "css" / "wiki.css").write_text(CSS, encoding="utf-8")

    # Definir mòduls
    from make_book import CHAPTERS_M1, CHAPTERS_M2, CHAPTERS_M3, CHAPTERS_M4, CHAPTERS_M5, CHAPTERS_M6
    modules = [
        ("Mòdul 1", "modul-1.html", "Fonaments, contenidors i pràctica", CHAPTERS_M1),
        ("Mòdul 2", "modul-2.html", "Dades operatives, MQTT, Grafana, web", CHAPTERS_M2),
        ("Mòdul 3", "modul-3.html", "LoRa, sensors remots, xarxa 868 MHz", CHAPTERS_M3),
        ("Mòdul 4", "modul-4.html", "IA local amb Ollama i RAG", CHAPTERS_M4),
        ("Mòdul 5", "modul-5.html", "Seguretat i còpies de seguretat", CHAPTERS_M5),
        ("Mòdul 6", "modul-6.html", "Operativa 24/7, monitoratge i manteniment", CHAPTERS_M6),
    ]
    all_links = {label: fname for label, fname, _, _ in modules}

    # Generar cada mòdul
    for label, fname, sub, chapters in modules:
        html_content = render_module_page(label, sub, chapters, all_links)
        out = WIKI_DIR / fname
        out.write_text(html_content, encoding="utf-8")
        size = out.stat().st_size
        print(f"  ✓ {fname} ({size:,} bytes)")

    # Generar índex
    modules_simple = [(label, fname, sub) for label, fname, sub, _ in modules]
    index_html = render_index(modules_simple)
    out = WIKI_DIR / "index.html"
    out.write_text(index_html, encoding="utf-8")
    print(f"  ✓ index.html ({out.stat().st_size:,} bytes)")

    # Generar README per saber què és
    readme = WIKI_DIR / "README.md"
    readme.write_text(
        "# BernatLab Wiki\n\n"
        "Wiki estàtica generada a partir dels capítols Markdown del llibre.\n\n"
        "Per regenerar-la:\n\n"
        "```bash\n"
        "python book/build_wiki.py\n"
        "```\n\n"
        "Estructura:\n\n"
        "- `index.html` — portada amb índex i glossari.\n"
        "- `modul-1.html` .. `modul-3.html` — un per mòdul.\n"
        "- `css/wiki.css` — full d'estil comú.\n",
        encoding="utf-8",
    )

    print(f"\n[fet] Wiki generada a {WIKI_DIR}")
    if args.open:
        webbrowser.open(f"file://{WIKI_DIR / 'index.html'}")


if __name__ == "__main__":
    main()
