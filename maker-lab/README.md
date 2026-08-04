# Bernat Maker Lab

> El laboratori personal per aprendre electronics, programacio de microcontroladors i disseny de dispositius propis amb plaques com ESP32, Arduino, Raspberry Pi Pico i similars.

## Que es

El **Bernat Maker Lab** es la part del projecte BernatLab dedicada a **aprendre fent** amb plaques electroniques. Es diferencia del BernatLab "classic" (servidors, Docker, IA) en que aqui el focus es:

- **Aprendre electronics** des de zero amb projectes petits i verificables.
- **Construir coses noves**: sensors, llums, alarmes, panells interactius, robots petits, instruments musicals, ...
- **Tot local-first**: la regla es que tot funcioni a la teva xarxa local, sense dependre del nuvol.

## Per on començar

1. **Llegeix el Capitol 70** del llibre (`book/chapters/70-bernat-maker-lab.md`) - es la porta dentrada conceptual.
2. **Fes el Capitol 1 del curs M9** (`book/curs/M9/01-blink-i-led-via-web/`) - es el primer projecte practic (P0: Blink + LED via web).
3. **Consulta el README del projecte P0** (`maker-lab/projectes/p0-blink-i-led-web/`) per la part tecnica operativa.
4. **Quan acabis P0**, captura pantalla i pasa a P1.

## Estructura daquesta carpeta

```
maker-lab/
├── README.md                  ← aquest fitxer
├── inventari/                 ← inventari propi del material del laboratori
├── docs/
│   └── decisions/             ← ADR especifiques del Maker Lab
├── idees-futures/             ← cataleg didees per a projectes nous
└── projectes/                 ← projectes individuals amb el seu propi README
    └── p0-blink-i-led-web/    ← P0: Blink + LED via web
```

## Connexions amb la resta del BernatLab

- **Curs M9** (`book/curs/M9/`) - capitols practic amb resum, quiz, exercici, respostes.
- **Llibre Capitol 70** (`book/chapters/70-bernat-maker-lab.md`) - porta dentrada conceptual.
- **Glossari general** (`book/glossari.md`) - termes tecnics compartits.
- **Curs M2 (Cap 12 - MQTT des de zero)** - protocol que farem servir a P3.
- **Curs M2 (Cap 20 - API publica)** - com fer el panell web propi per a P4.
- **Curs M3 (Caps 23-32 - LoRa)** - per quan vulguis fer nodes a llarga distancia.

## Estat actual

- [x] **P0 - Blink + LED via web** - documentat i llest per fer (cal comprar el material).
- [ ] P1 - Termometre amb pagina web - pendent.
- [ ] P2 - Dos ESP32 amb polsador i LED creuat - pendent.
- [ ] P3 - MQTT entre ESP32 i Raspberry Pi - pendent.
- [ ] P4 - Panell web propi a la Raspberry - pendent.

## Regles dor

- **Mai 230 V directe a un ESP32** ni a cap GPIO. Per a carregues de 230 V usa moduls de rele protegits i, si tens dubtes, consulta un electricista.
- **Mai 5 V a un GPIO de l'ESP32** (es 3,3 V). Usa un conversor de nivell logic si cal.
- **Sempre una resistencia en serie amb un LED** (220-330 ohm).
- **Un multimete es obligatori**, no opcional.
- **Desconnecta l'ESP32 abans de canviar el circuit**.
- **Valida sempre amb execucio real** abans de reportar "fet".
- **Documenta cada projecte** amb el patro README + hardware/ + firmware/ + proves/.

## Pressupost inicial

| Component | Preu aprox. |
|---|---|
| 2 × ESP32 DevKit v1 | 10-14 EUR |
| Kit basic de components | 22-28 EUR |
| Conversor de nivell + estoig + brides | 4 EUR |
| Multimete digital basic | 10-15 EUR |
| **Total** | **46-61 EUR** |

Cap daquestes peces es compartida amb el projecte de lhort. Lhort te la seva propia infraestructura.

---

*Ultima actualitzacio: 3 dagost del 2026.*
