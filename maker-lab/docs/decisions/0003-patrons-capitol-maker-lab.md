# ADR 0003 - Patrons de capitol del Maker Lab dins del BernatLab

> **Estat**: Acceptada · **Data**: 2026-08-03 · **Autor**: Bernat + Hermes

## Context

El BernatLab ja te un sistema madur de documentacio amb dos eixos:

- **Llibre tecnic** (`book/chapters/`) - text complet llarg amb PDF i DOCX generats per `make_book.py`.
- **Curs** (`book/curs/M1..M8/`) - capitols amb resum, quiz, exercici i respostes, generats per `build_course.py`.

Volem afegir el Maker Lab com a **Modul 9 del curs** i un **Capitol 70 del llibre** d'entrada, sense trencar el sistema existent.

## Alternatives considerades

| Alternativa | Pros | Contres |
|---|---|---|
| **A. M9 al curs + Capitol 70 al llibre** | Consistent amb el sistema existent, integrat a `make_book.py` i `book/index.md`. | Cal editar 3 fitxers sensibles (`make_book.py`, `index.md`, `build_course.py`). |
| B. Tot a `maker-lab/llibre/` independent | Autocontingut, no toca res del BernatLab. | Trenca el patro del llibre i del curs, genera duplicacio. |
| C. Només `maker-lab/` standalone | Senzill, no toca res. | No aprofitem la feina ja feta al BernatLab. |
| D. Integrar-ho al M7 (Hort Osona) | Tematicament proper. | El M7 es "Hort Osona en accio", el Maker Lab es generic. Forca el sentit. |

## Decisio

**Opcio A: M9 al curs + Capitol 70 al llibre**, amb una carpeta operativa `maker-lab/` per al codi i la documentacio tecnica.

## Raonament

1. **Reutilitza el sistema existent**: el `build_course.py` ja te logica per afegir moduls nous automaticament (nomes cal afegir `MODULE_NAMES["M9"]`).
2. **Integracio consistent**: el Capitol 70 entra al llibre PDF/DOCX del M8, igual que la resta de capitols.
3. **Separacio de responsabilitats**:
   - `book/curs/M9/` - el relat pedagogic (resum, quiz, exercici, respostes).
   - `book/chapters/70-...md` - el capitol llarg dentrada al llibre.
   - `maker-lab/` - el material operatiu (codi, esquemes, decisions, projectes, idees).
4. **No trenca res existent**: totes les modificacions son addicions, no substitucions.
5. **Es extensible**: quan afegim P1, P2, etc., nomes cal afegir carpetes `book/curs/M9/02-.../`, i la resta del sistema els detectara automaticament.

## Estructura resultant

```
bernatlab/
├── book/
│   ├── chapters/
│   │   └── 70-bernat-maker-lab.md          ← Capitol 70 del llibre
│   ├── curs/
│   │   └── M9/                              ← Modul 9 del curs
│   │       └── 01-blink-i-led-via-web/      ← P0: Blink + LED via web
│   │           ├── resum.md
│   │           ├── quiz.md
│   │           ├── exercici.md
│   │           └── respostes.md
│   │       └── 01-blink-i-led-via-web.html  ← Pagina web del capitol
│   ├── index.md                             ← Afegit: seccio "Modul 8 - Bernat Maker Lab"
│   ├── make_book.py                         ← Afegit: CHAPTERS_M8 + logica del modul 8
│   └── curs/build_course.py                 ← Afegit: MODULE_NAMES["M9"]
│
└── maker-lab/                               ← Tot el material operatiu
    ├── README.md                            ← Porta dentrada
    ├── inventari/                           ← Material del laboratori
    ├── docs/decisions/                      ← ADR especifiques del Maker Lab
    ├── idees-futures/                       ← Cataleg didees
    └── projectes/                           ← Projectes individuals
        └── p0-blink-i-led-web/              ← P0: detall tecnic operatiu
            └── README.md
```

## Conseqüencies

- Cal mantenir 3 carpetes en sincronia: `book/curs/M9/`, `book/chapters/70-...md` i `maker-lab/projectes/`.
- El `course-manifest.json` es regenera automaticament amb `python book/curs/build_course.py`.
- El PDF/DOCX del M8 es regenera amb `.venv/Scripts/python.exe book/make_book.py 8`.
- Tots els nous projectes seguiran el mateix patro (carpeta del capitol al curs + capitol opcional al llibre + projecte operatiu a `maker-lab/`).

## Quan afegir nous projectes (P1, P2, ...)

Per a cada nou projecte:

1. Crear `book/curs/M9/NN-nom-del-projecte/{resum,quiz,exercici,respostes}.md` + `.html`.
2. Si es prou important, afegir un capitol al llibre amb el numero que toqui (71, 72, ...).
3. Crear `maker-lab/projectes/pN-nom/` amb el codi operatiu.
4. Executar `python book/curs/build_course.py` per regenerar el manifest.
5. Si sha afegit capitol al llibre, executar `.venv/Scripts/python.exe book/make_book.py N`.

## Glossari i inventari

- El glossari es compartit amb el BernatLab general: `book/glossari.md`. Si cal afegir-hi termes nous del Maker Lab, sha de fer allà (no duplicar).
- Linventari es propi del Maker Lab: `maker-lab/inventari/`. No sha de barrejar amb el de lhort o el de `bernatlab-cyberlab/`.
