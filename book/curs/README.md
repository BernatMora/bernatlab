# Curs del BernatLab

> Aprèn el BernatLab al teu ritme amb resums, qüestionaris i exercicis pràctics.

Aquest curs està basat en el llibre **BernatLab — Construint el meu servidor intel·ligent** (562 pàgines, 7 mòduls, 69 capítols). Cada mòdul té:

- **Resum** del capítol amb les idees clau.
- **Qüestionari** per validar la comprensió.
- **Exercici pràctic** a fer al teu servidor o al teu hort.
- **Respostes** per autoavaluar-te.

## Estructura

| Mòdul | Contingut | Estat |
|---|---|---|
| **M1. Fonaments** | Què és un homelab, Raspberry Pi, Linux, Xarxa | ✅ Pilot |
| M2. Contenidors | Docker, Portainer, Uptime Kuma, Homepage | ⏳ Pendent |
| M3. Dades | Git, còpies, documentació, gestió | ⏳ Pendent |
| M4. Intel·ligència | Ollama, RAG, models locals | ⏳ Pendent |
| M5. Seguretat | SSH, Tailscale, firewall, VPN | ⏳ Pendent |
| M6. Operativa | Monitorització 24/7, alertes, manteniment | ⏳ Pendent |
| M7. Hort Osona | Sistema IoT, sensors, gràfiques | ⏳ Pendent |

## Com fer-lo servir

1. **Llegeix el resum** del capítol (5-10 min).
2. **Fes el qüestionari** amb l'script `quiz.py` (15-20 min).
3. **Fes l'exercici pràctic** al teu servidor / hort (20-60 min).
4. **Repassa al cap de 15 dies** — 3-5 preguntes aleatòries del capítol.

## Ús de l'script de qüestionaris

```bash
# Des del directori arrel del BernatLab
cd C:\Users\iadmin\bernatlab
.venv/Scripts/python.exe book/curs/quiz.py
```

L'script et preguntarà:
- Quin mòdul vols fer (1-7).
- Quin capítol vols repassar (1-N).
- Si vols preguntes noves o repàs de 15 dies.
- I et donarà una nota al final.

## Historial

Les teves respostes queden registrades a `~/.bernatlab/quiz_history.json` per poder fer repàs espaiat.

## Com estendre

Si vols afegir un mòdul nou:
1. Crea `book/curs/MX-nom/`
2. Crea un subdirectori per a cada capítol: `capitol-NY/`
3. Dins, posa-hi `resum.md`, `quiz.md`, `exercici.md`, `respostes.md`.
4. Segueix el format de `M1/01-que-es-bernatlab/` (capítol pilot).

## Mètode d'aprenentatge

Aquest curs aplica el mètode de **repàs espaiat** (spaced repetition):

- **Dia 0**: llegeix resum + fes quiz + exercici pràctic.
- **Dia 3**: repassa les preguntes que has fallat.
- **Dia 15**: repassa 3-5 preguntes aleatòries.
- **Dia 45**: repassa 3-5 preguntes aleatòries.

Això fixa els coneixements a la memòria de llarg termini. La ciència cognitiva diu que calen entre 3 i 5 repàs per retenir informació nova.

## Recursos

- [`recursos/recuperacio-emergencia-tailscale.md`](recursos/recuperacio-emergencia-tailscale.md) — Què fer si Tailscale falla i no pots accedir a la RPi.
