# BernatLab — Mòdul 2

**Sensors, dades i visualització**
*De MQTT a Hort Osona*

---

## Què és aquest mòdul

El Mòdul 1 del BernatLab va establir les bases: entendre la Raspberry, administrar Linux, configurar xarxa i SSH, desplegar serveis amb Docker i tenir un panell, una eina de monitorització i un sistema de control de versions. Tot plegat, la infraestructura d'un homelab seriós.

Ara toca fer-lo servir per a alguna cosa concreta. I la cosa concreta és **Hort Osona**: un projecte de seguiment d'un hort familiar a 245 metres de casa, amb sensors al terreny, dades al servidor, gràfiques a la web pública, i alertes al mòbil quan alguna cosa va malament.

Aquest mòdul cobreix tota la cadena:

```
Sensor → MQTT → Telegraf → InfluxDB → Grafana
                                 ↓
                            Node-RED (neteja, alertes)
                                 ↓
                              API FastAPI
                                 ↓
                       Web Hort Osona (consumeix API)
```

## A qui va adreçat

A qualsevol persona que:

1. Vol **connectar sensors a un servidor** i tractar-ne les dades.
2. Vol entendre **MQTT, InfluxDB, Telegraf, Grafana i Node-RED** a fons, no només copiar ordres.
3. Vol construir una **API pública** que serveixi les dades a una web o a una aplicació mòbil.
4. Vol **integrar el BernatLab amb un projecte real**, en el nostre cas Hort Osona.

## Estructura del mòdul

| # | Títol | Què aprendràs |
|---|---|---|
| 11 | Del Mòdul 1 al M2 | Visió general, arquitectura, què connecta amb què |
| 12 | MQTT des de zero | El protocol que parlen els sensors |
| 13 | Mosquitto al BernatLab | El broker MQTT en funcionament |
| 14 | Publicar dades: els sensors | Com parlen els sensors amb el servidor |
| 15 | InfluxDB: base de dades de sèries temporals | On i com es guarden les dades |
| 16 | Telegraf: el pont | Com les dades passen de MQTT a InfluxDB |
| 17 | Node-RED: programació visual | L'eina de fluxos per netejar i transformar |
| 18 | Fluxos pràctics | Exemples reals: mitjanes, gelades, alertes |
| 19 | Grafana: visualitzar | Gràfiques, panells, alertes visuals |
| 20 | API pública | Com servir les dades al món |
| 21 | Integració amb Hort Osona | La web consumeix l'API |
| 22 | Operativa | Còpies, retenció, escalat, manteniment |

## Com es llegeix

- En ordre, si vols construir tot el sistema des de zero.
- Per capítols, si ja tens una base i vols aprofundir en una part.
- Cada capítol segueix la mateixa estructura del Mòdul 1: teoria, aplicació al BernatLab, esquemes, comandes, errors, exercicis, resum.

## Context del sistema

Tot el que s'explica assumeix:

- BernatLab en marxa (Mòdul 1 complet).
- Raspberry Pi 4 amb Debian 13 Lite, 4 GB RAM.
- Tailscale funcionant.
- Portainer, Uptime Kuma, Homepage desplegats.
- Carpeta de treball `/home/bernat/homelab/`.
- L'hort a 245 metres de casa, amb sensors equipats amb mòduls ràdio (potser LoRa, potser Wi-Fi, potser mixt).

> **Nota important**: a data d'avui, **la Raspberry Pi 4 encara no ha arribat** (juliol 2026). Tot el que s'explica en aquest mòdul s'ha dissenyat perquè es pugui implementar tan bon punt la màquina estigui disponible. Les configuracions s'han provat conceptualment, però no s'han pogut desplegar en el hardware real. Quan la RPi arribi, serà el moment de fer les proves de camp i ajustar els detalls que inevitablement caldrà ajustar.

## Com es genera

Aquest mòdul s'ha escrit en **Markdown** i es converteix a **PDF** i **DOCX** amb `make_book.py`, el mateix generador del Mòdul 1 (ampliat). Tots els fitxers font són a la carpeta `chapters/`. El procés és reproduïble.

## Llicència

Manual personal, com el Mòdul 1. Si algú el llegeix, que en tregui profit. Si hi troba errors, que me'ls digui.

— Bernat
