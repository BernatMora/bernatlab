# Resum - M8 Cap 6: Obsidian + Git

## Per que importa

Si tens un projecte (com el BernatLab), acabes acumulant **moltes notes**:
- Idees que vols explorar.
- Errors que has tingut.
- Decisions que has pres.
- Procediments que funcionen.
- Referencies utils.

Si ho tens **espargit** (paper, notes del mobil, un .txt per aqui, un altre per allà), acabes **perdent-ho**. I el dia que necessites una cosa, no la trobes.

**Obsidian + Git** es la solucio:
- **Obsidian**: editor de notes en Markdown, local, gratuit per a us personal.
- **Git**: sistema de versionat, et permet tenir historial i sincronitzar entre PCs.

## Que es Obsidian

Obsidian es una aplicacio d'escriptori per a **notes en Markdown**. Caracteristiques:
- **Local-first**: totes les notes estan en fitxers al teu disc. No al núvol.
- **Markdown natiu**: les notes son fitxers `.md` que pots obrir amb qualsevol editor.
- **Vincles entre notes**: pots crear enllaços entre notes (`[[nom-de-la-nota]]`).
- **Graf de coneixement**: visualitza les connexions entre notes.
- **Plugins**: milers de plugins per a tota mena de funcions.
- **Gratis** per a us personal (només pagues si vols comercial).

## Per que Obsidian i no Notion o Evernote

| Eina | Local? | Markdown? | Privadesa | Preu |
|---|---|---|---|---|
| **Obsidian** | Si | Si | Total | Gratis |
| **Notion** | No | Parcial | Dubtosa | Gratis (limitat) |
| **Evernote** | No | No | Dubtosa | ~10 USD/mes |
| **Apple Notes** | Parcial | No | Apple | Gratis |
| **Google Keep** | No | No | Google | Gratis |

Per a un homelab on vols **privadesa i control**, Obsidian es la millor opcio.

## Instal·lacio

1. Descarrega de https://obsidian.md
2. Instal·la (Windows, Mac, Linux).
3. Obre per primera vegada.
4. Crea un **vault** (carpeta de notes). Et recomano `C:\Users\usuari\obsidian\bernatlab`.

## Us basic

### Crear una nota

- Click al signe **+** a l'esquerra.
- Titol + contingut.
- Tot en Markdown.

### Enllaçar notes

Dins d'una nota, escriu `[[` i selecciona una altra nota. Obsidian crea un vincle.

Exemple: en una nota pots escriure:
```markdown
Per a mes info, veure [[runbook-recuperacio-tailscale]].
```

### Tags

Pots afegir tags amb `#`:
```markdown
#bernatlab #ssh #emergencia
```

### Cerca

`Ctrl+Shift+F` busca a totes les notes.

### Graf

Click al **node graph** (icona de graf). Veuras totes les notes com a nodes, i els vincles com a arestes.

## Integracio amb Git

Per sincronitzar el vault entre PCs i tenir historial:

1. Instal·la **Git** (ja l'hauries de tenir).
2. Dins de la carpeta del vault, obre un terminal:
```bash
cd C:\Users\usuari\obsidian\bernatlab
git init
git add .
git commit -m "Inici del vault del BernatLab"
```

3. Crea un repo a GitHub (per exemple `bernatlab-notes` o nomes dins del repo principal).
4. Afegeix el remote:
```bash
git remote add origin https://github.com/BernatMora/bernatlab.git
git push -u origin main
```

## Plugins utils per al BernatLab

- **Calendar** - vista de calendario per veure notes per data.
- **Dataview** - consulta notes com si fos una base de dades.
- **Excalidraw** - dibuixos a ma.
- **Mind map** - mapes mentals.
- **Spaced Repetition** - flashcards per al curs!

## Connexions

- **M8 cap 7** - Els runbooks es poden guardar a Obsidian.
- **BernatLab** - El curs es pot consultar des d'Obsidian.
- **M9 del llibre** - Documentacio del projecte.

## Bones practiques

- **Un vault per projecte** (BernatLab, Hort Osona, feina, personal).
- **Estructura clara** amb carpetes (00-index, 01-arquitectura, 02-runbooks, etc.).
- **Naming consistent** (kebab-case, dates en YYYY-MM-DD).
- **Commit sovint** - cada canvi important.
- **No posar secrets** - mai al repo.
