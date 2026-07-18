# Curs del BernatLab

> Aprèn el BernatLab al teu ritme amb resums, qüestionaris i exercicis pràctics.

Aquest curs està basat en el llibre **BernatLab — Construint el meu servidor intel·ligent** i amplia el material amb un itinerari d’autoformació de **8 mòduls, 77 capítols i 1.087 preguntes**. Cada capítol té:

- **Resum** del capítol amb les idees clau.
- **Qüestionari** per validar la comprensió.
- **Exercici pràctic** a fer al teu servidor o al teu hort.
- **Respostes** per autoavaluar-te.

## Estructura

| Mòdul | Contingut | Estat |
|---|---|---|
| **M1. Fonaments** | Homelab, Raspberry Pi, Linux, xarxa | ✅ 10 capítols |
| M2. Contenidors | Docker avançat i operativa de contenidors | ✅ 10 capítols |
| M3. Dades | Backups, bases de dades, fitxers i visualització | ✅ 10 capítols |
| M4. Intel·ligència | Ollama, RAG i models locals | ✅ 10 capítols |
| M5. Seguretat | SSH, Tailscale, firewall, secrets i auditoria | ✅ 10 capítols |
| M6. Operativa | Monitorització 24/7, alertes i manteniment | ✅ 10 capítols |
| M7. Hort Osona | Sistema IoT, sensors, API i PWA | ✅ 10 capítols |
| M8. Eines | SSH, PowerShell, Obsidian, Git i runbooks | ✅ 7 capítols |

## Com fer-lo servir

1. **Llegeix el resum** del capítol (5-10 min).
2. **Fes el qüestionari** directament al web o amb `quiz.py` (15-20 min).
3. **Fes l'exercici pràctic** al teu servidor / hort (20-60 min).
4. **Repassa al cap de 15 dies** — 3-5 preguntes aleatòries del capítol.

## Ús de l'script de qüestionaris

```bash
# Des del directori arrel del BernatLab
cd /ruta/al/bernatlab
python book/curs/quiz.py
```

L'script et preguntarà:

- Si vols fer un qüestionari, repàs espaiat, veure estadístiques o llistar capítols.
- Quin capítol vols fer, quan tries un qüestionari.
- I et donarà una nota al final.

També pots obrir directament un capítol: `python book/curs/quiz.py --module M4 --chapter 3`.

## Historial

Les teves respostes queden registrades a `~/.bernatlab/quiz_history.json` per poder fer repàs espaiat.

## Com estendre

Si vols afegir un mòdul nou:

1. Crea `book/curs/MX/`.
2. Per cada capítol, crea `book/curs/MX/NN-nom.html` i el directori `book/curs/MX/NN-nom/`.
3. Dins el directori del capítol, posa-hi `resum.md`, `quiz.md`, `exercici.md` i `respostes.md`.
4. Segueix el format de `M1/01-que-es-bernatlab/` (capítol pilot).
5. Afegeix el nom del mòdul a `MODULE_NAMES` dins `build_course.py`.
6. Executa `python book/curs/build_course.py` per regenerar el manifest i validar l’estructura.

## Mètode d'aprenentatge

Aquest curs aplica el mètode de **repàs espaiat** (spaced repetition):

- **Dia 0**: llegeix resum + fes quiz + exercici pràctic.
- **Dia 3**: repassa les preguntes que has fallat.
- **Dia 15**: repassa 3-5 preguntes aleatòries.
- **Dia 45**: repassa 3-5 preguntes aleatòries.

Això fixa els coneixements a la memòria de llarg termini. La ciència cognitiva diu que calen entre 3 i 5 repàs per retenir informació nova.

## Recursos

- [`recursos/recuperacio-emergencia-tailscale.md`](recursos/recuperacio-emergencia-tailscale.md) — Què fer si Tailscale falla i no pots accedir a la RPi.
