# BernatLab

> Sistema integral personal basat en una Raspberry Pi 4 amb Docker, Tailscale i serveis autoallotjats per a Hort Osona, sensors LoRa, meteorologia, IA, música, automatitzacions i desenvolupament web.

Aquest repositori és la **font de la veritat documental i de configuració versionada** del projecte. L'estat operatiu real s'ha de verificar als equips abans de desplegar o canviar serveis.

## Estat i seguretat

- Estat de referència: [`PROJECT_STATE.md`](PROJECT_STATE.md).
- Les dades reals de xarxa, credencials i configuracions locals no es publiquen.
- Els exemples versionats han d'usar placeholders i fitxers `.env.example`.
- Els canvis de serveis s'han de validar amb `docker compose config` abans del desplegament.
- La documentació i el curs tenen comprovacions automàtiques a GitHub Actions.

Conté:

```
bernatlab/
├── book/               Llibre/manual tècnic (Mòdul 1 + Mòdul 2, 206 pàgines)
├── homelab/            Configuració del servidor (Docker Compose, scripts, docs)
├── projects/           Subprojectes (hort-osona com a submodule)
├── backups/            Còpies de seguretat manuals
└── README.md           Aquest fitxer
```

## Llibre tècnic

El llibre es compon de capítols en Markdown a `book/chapters/`. Es genera automàticament com a PDF i DOCX a `book/output/`:

```bash
cd book
python make_book.py          # genera M1 i M2
python make_book.py 1        # només M1
python make_book.py 2        # només M2
```

- **Mòdul 1** — Fonaments, contenidors i pràctica (10 capítols)
- **Mòdul 2** — Sensors, dades i visualització (12 capítols)

Més detalls a [`book/README.md`](book/README.md).

## Homelab

Tot el que té a veure amb la Raspberry Pi 4 (la "BernatLab" original) viu a `homelab/`:

- `homelab/compose/` — fitxers `docker-compose.yml` organitzats per piles (core, monitoring, iot, data, etc.).
- `homelab/scripts/` — scripts de manteniment (backup, alerting, etc.).
- `homelab/docs/` — documentació operativa (procediments, notes, runbooks).

L'estructura segueix la regla d'or: **un sol `docker-compose.yml` per tema, bind mounts a `/home/bernat/homelab/data/`**.

## Subprojectes

`projects/` allotja subprojectes que tenen vida pròpia:

- `projects/hort-osona/` — la web pública Hort Osona (afegida com a **Git submodule** de `bernatmora/hort-osona`).

Per clonar el submodule:

```bash
git clone https://github.com/bernatmora/bernatlab.git
cd bernatlab
git submodule update --init --recursive
```

Per actualitzar el submodule quan hi hagi canvis a hort-osona:

```bash
cd projects/hort-osona
git pull origin main
cd ../..
git add projects/hort-osona
git commit -m "Actualitza hort-osona"
git push
```

## Workflow

Aquest repositori segueix un workflow de **publicació viva**:

1. S'escriu o corregeix un capítol a `book/chapters/`.
2. Es regenera el PDF/DOCX amb `make_book.py`.
3. Es revisen explícitament els fitxers amb `git status` i `git diff --staged`; després es fa commit i push.
4. La còpia es descarrega a la Raspberry Pi 4 via `rsync` o `git pull`.

Per automatitzar, hi ha un script a `homelab/scripts/publish.sh`.

## Estructura física esperada al servidor

Quan es cloni a la Raspberry:

```
/home/bernat/
├── bernatlab/          ← aquest repo
├── homelab/            ← dades persistents (volums Docker)
└── backups/            ← còpies de seguretat
```

## Llicència

Document personal compartit públicament. Consulta [US-I-AUTORIA.md](US-I-AUTORIA.md). Si hi trobes errors, reporta’ls al repositori.

— Bernat
