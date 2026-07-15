# BernatLab — Llibre tècnic pràctic

Llibre d'autoformació i consulta per al projecte BernatLab. S'escriu en
**Markdown** (font de la veritat), es publica en **PDF** i **DOCX** (artefactes
generats), es consulta com a **wiki HTML navegable**, i es complementa amb
una **chuleta de comandes** per a ús immediat a la RPi.

## 🌐 Web pública

El llibre té una web pública a **https://bernatmora.github.io/bernatlab/**
amb portada, mòduls navegables, chuleta i descàrregues.

## 📂 Estructura

```
book/
├── chapters/        ← Markdown (font de la veritat, 69 capítols)
├── images/          ← Captures i il·lustracions
├── diagrams/        ← Esquemes Mermaid i altres
├── output/          ← PDF i DOCX generats (7 mòduls × 2 formats)
├── wiki/            ← Wiki HTML estàtica generada
│   ├── index.html
│   ├── modul-1.html ... modul-7.html
│   ├── css/wiki.css
│   └── README.md
├── index.html       ← Portada HTML (per a GitHub Pages)
├── cheatsheet.html  ← Chuleta de comandes amb cerca (303 comandes)
├── cheatsheet.md    ← Versió Markdown imprimible
├── cheatsheet-data.json  ← Dades extretes
├── extract_cheatsheet.py ← Extreu comandes dels capítols
├── build_cheatsheet.py   ← Genera la chuleta
├── make_book.py          ← Genera PDF i DOCX
├── build_wiki.py         ← Genera la wiki HTML
└── README.md        ← Aquest fitxer
```

## 📚 Mòduls

| # | Mòdul | Capítols | Pàgines PDF |
|---|---|---|---|
| 1 | Fonaments, contenidors i pràctica | 10 | 84 |
| 2 | Sensors, dades i visualització | 12 | 122 |
| 3 | LoRa, sensors remots i xarxa de camp | 10 | 84 |
| 4 | IA local amb Ollama i RAG | 10 | 76 |
| 5 | Seguretat i còpies de seguretat | 8 | 63 |
| 6 | Operativa 24/7, monitoratge i manteniment | 7 | 50 |
| 7 | Hort Osona en acció (curs pràctic) | 12 | 83 |
| **Total** | | **69** | **562** |

## 🚀 Com regenerar els artefactes

Des del directori arrel del repo:

```bash
# Activar el venv
uv venv .venv
uv pip install --python .venv/Scripts/python.exe reportlab python-docx pypdf

# Generar un mòdul específic
.venv/Scripts/python.exe book/make_book.py 1

# Generar tots
.venv/Scripts/python.exe book/make_book.py all

# Regenerar la wiki HTML
.venv/Scripts/python.exe book/build_wiki.py

# Regenerar la chuleta
.venv/Scripts/python.exe book/extract_cheatsheet.py
.venv/Scripts/python.exe book/build_cheatsheet.py
```

## 📋 Chuleta de comandes

La chuleta és un recull de les **303 comandes més útils** extretes
automàticament dels capítols, organitzades en 20 categories (Docker, MQTT,
Grafana, SSH, Tailscale, Seguretat, etc.).

- **Versió web**: `book/cheatsheet.html` — cerca instantània + botó copiar.
- **Versió imprimible**: `book/cheatsheet.md` — totes les comandes en Markdown.

## 🎯 A qui va dirigit

- **Al pagès digital** que vol muntar un sistema complet per al seu hort.
- **Al tècnic** que vol aprendre IoT, xarxes, i administració de sistemes amb un cas pràctic.
- **A tu del futur** que oblidarà com es configurava tot. La documentació és per a tu d'aquí un any.
- **A una altra persona** que vulgui replicar el BernatLab al seu hort.

Cada capítol té 8 seccions estàndard:

1. Explicació teòrica.
2. Aplicació concreta al BernatLab.
3. Esquemes en text o Mermaid.
4. Comandes útils.
5. Què està passant realment.
6. Errors habituals.
7. Exercicis pràctics.
8. Resum final.

Tots els capítols comencen amb una cita breu que resumeix l'esperit del
capítol, i acaben amb un resum i exercicis pràctics.

## 🔗 Enllaços

- **Web pública**: https://bernatmora.github.io/bernatlab/
- **Repo a GitHub**: https://github.com/BernatMora/bernatlab
- **Web d'Hort Osona**: https://bernatmora.github.io/hort-osona/

## Llicència

Aquest llibre és un projecte personal de Bernat Mora. Si vols reutilitzar
parts, cita la font.
