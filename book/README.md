# BernatLab — Llibre tècnic pràctic

Llibre d'autoformació i consulta per al projecte BernatLab. S'escriu en Markdown, es publica en PDF i DOCX, i es versiona amb Git.

## Estructura

```
book/
├── chapters/            Capítols en Markdown (01-..., 02-..., ...)
├── images/              Imatges (per a futures il·lustracions)
├── output/              PDF i DOCX generats (sí, es versionen!)
├── index.md             Índex general del llibre
├── README.md            Aquest fitxer
├── README_M2.md         Descripció específica del Mòdul 2
└── make_book.py         Generador de PDF i DOCX
```

## Per què versionem els PDF/DOCX

A diferència d'un projecte de programari, els artefactes del llibre (PDF, DOCX) són la **forma final de consum**. Versionar-los permet:

- Accedir a qualsevol versió publicada des de GitHub Releases.
- Comparar canvis visuals entre versions.
- Evitar que tothom hagi de regenerar el llibre per llegir-lo.

Si en algun moment volem deixar de versionar-los (per exemple, si el repo creix massa), només cal comentar les dues línies del `.gitignore` que exclouen `book/output/*.pdf` i `book/output/*.docx`.

## Mòduls actuals

### Mòdul 1 — Fonaments, contenidors i pràctica

10 capítols (84 pàgines):

1. Què és BernatLab
2. La Raspberry Pi 4 per dins
3. Linux per administrar un servidor
4. Xarxa, SSH i Tailscale
5. Docker des de zero
6. Portainer
7. Uptime Kuma
8. Homepage
9. Git i documentació
10. Full de ruta del BernatLab

### Mòdul 2 — Sensors, dades i visualització

12 capítols (122 pàgines):

11. Del Mòdul 1 al M2: què construïm
12. MQTT des de zero
13. Mosquitto al BernatLab
14. Publicar dades: els sensors
15. InfluxDB: base de dades de sèries temporals
16. Telegraf: el pont
17. Node-RED: programació visual
18. Fluxos pràctics
19. Grafana: visualitzar les dades
20. API pública: servir les dades al món
21. Integració amb Hort Osona
22. Operativa: còpies, alertes, escalat

**Total actual: 22 capítols, 206 pàgines.**

## Generar el llibre

### Requisits

```bash
# Crear un entorn virtual a la carpeta pare del projecte
cd ~/bernatlab
python -m venv ../.venv
source ../.venv/bin/activate   # Linux/Mac
# o
../.venv/Scripts/activate      # Windows

# Instal·lar dependències
pip install reportlab python-docx
```

### Generar

```bash
cd book
python make_book.py            # Tots dos mòduls
python make_book.py 1          # Només M1
python make_book.py 2          # Només M2
```

Tarda 1-2 minuts per mòdul. La sortida va a `book/output/`.

## Pròxims mòduls previstos

- **Mòdul 3** — IoT i LoRa SX1262 868 MHz
- **Mòdul 4** — IA local amb Ollama i RAG

## Convencions d'escriptura

- Català, amb normalització Bàsic/General.
- Capítols numerats amb dos dígims: `01-`, `02-`, ..., `22-`.
- Primera capçalera de cada capítol és el títol (`# Capítol N — ...`).
- Cada capítol té 8 seccions: teoria, aplicació al BernatLab, esquemes, comandes, "què passa realment", errors habituals, exercicis pràctics, resum.
- Mermaid: s'escriu com a text dins d'un bloc de codi `mermaid` (la generació gràfica és per a una versió futura).

## Edició

Per afegir o corregir un capítol:

```bash
$EDITOR chapters/12-mqtt-des-de-zero.md
python make_book.py 2          # regenera només el M2
git add chapters/12-mqtt-des-de-zero.md book/output/
git commit -m "Corregeix capítol 12: afeg exemple de wildcard +"
git push
```
