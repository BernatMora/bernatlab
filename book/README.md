# BernatLab — Llibre tècnic pràctic

Llibre d'autoformació i consulta per al projecte BernatLab. S'escriu en
**Markdown** (font de la veritat), es publica en **PDF** i **DOCX** (artefactes
generats), i es pot consultar com a **wiki HTML estàtica** (navegable, allotjable
a GitHub Pages).

## Estructura

```
book/
├── chapters/        ← Markdown (font de la veritat)
│   ├── 01-que-es-bernatlab.md
│   ├── 02-raspberry-pi.md
│   ├── ...
│   ├── 23-que-es-lora.md
│   ├── ...
│   └── 32-proves-camp.md
├── output/          ← PDF i DOCX generats
│   ├── BernatLab_Manual_Modul_1.pdf
│   ├── BernatLab_Manual_Modul_1.docx
│   ├── BernatLab_Manual_Modul_2.pdf
│   ├── BernatLab_Manual_Modul_2.docx
│   ├── BernatLab_Manual_Modul_3.pdf
│   └── BernatLab_Manual_Modul_3.docx
├── templates/       ← Plantilles Markdown per a nous capítols
├── diagrams/        ← Esquemes Mermaid i imatges
├── assets/          ← Recursos compartits (CSS, JS, icones)
├── images/          ← Captures i il·lustracions
├── wiki/            ← Wiki HTML estàtica (generada)
│   ├── index.html
│   ├── modul-1.html
│   ├── modul-2.html
│   └── modul-3.html
├── make_book.py     ← Genera PDF i DOCX
├── build_wiki.py    ← Genera la wiki HTML
├── index.md         ← Índex general del llibre
└── README.md        ← Aquest fitxer
```

## Mòduls

- **Mòdul 1 — Fonaments, contenidors i pràctica** (10 capítols, 84 pàgines)
- **Mòdul 2 — Sensors, dades i visualització** (12 capítols, 122 pàgines)
- **Mòdul 3 — LoRa, sensors remots i xarxa de camp** (10 capítols, 84 pàgines)

Total: **32 capítols · 290 pàgines · 522 KB de text font**.

## Com regenerar els artefactes

### PDF i DOCX

```bash
# Tots tres mòduls
.venv/Scripts/python.exe book/make_book.py all

# Un sol mòdul
.venv/Scripts/python.exe book/make_book.py 3

# Mòduls 1 i 2 (per compatibilitat)
.venv/Scripts/python.exe book/make_book.py both
```

El script llegeix els capítols de `book/chapters/`, els processa amb un parser
Markdown propi, i genera PDF (amb reportlab) i DOCX (amb python-docx).

### Wiki HTML

```bash
.venv/Scripts/python.exe book/build_wiki.py
.venv/Scripts/python.exe book/build_wiki.py --open  # obre al navegador
```

Genera un site HTML estàtic amb:

- Portada amb índex dels tres mòduls.
- Glossari de 47 termes clau (Docker, MQTT, LoRaWAN, etc.).
- Un fitxer per mòdul amb tots els capítols.
- Navegació lateral amb TOC.
- CSS lleuger, sense JavaScript, allotjable a GitHub Pages.

## Workflow de publicació

Després d'editar o afegir capítols:

```bash
# 1. Validar i generar
.venv/Scripts/python.exe book/make_book.py all
.venv/Scripts/python.exe book/build_wiki.py

# 2. Publicar a GitHub
git add book/
git commit -m "Actualitza capítols i artefactes"
git push origin main
```

També tenim el script `homelab/scripts/publish.py` que automatitza tot el cicle.

## Estil dels capítols

Cada capítol segueix una estructura comuna:

1. Explicació teòrica.
2. Aplicació concreta al BernatLab.
3. Esquemes en text o Mermaid.
4. Comandes útils.
5. Què està passant realment.
6. Errors habituals.
7. Exercicis pràctics.
8. Resum final.

Tots els capítols comencen amb una cita breu (en format Markdown blockquote)
que resumeix l'esperit del capítol, i acaben amb un llistat de "Paraules clau".

## Llicència

Aquest llibre és un projecte personal de Bernat Mora. Si vols reutilitzar
parts, cita la font.
