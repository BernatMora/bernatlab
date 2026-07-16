# Resum — Capítol 1: Què és BernatLab

## La idea clau

Un **homelab** és un servidor personal a casa teva, amb el qual aprens, experimentes i automates coses. El **BernatLab** és l'homelab de Bernat Mora: una Raspberry Pi 4 amb Debian 13, Docker, Tailscale, MQTT, sensors, IA local, i una web pública (Hort Osona).

## Per què construir un servidor propi?

Tres motius clars:

1. **Aprenentatge real** — Res és tan efectiu com tenir un sistema que funciona a casa teva. Llegeixes sobre Docker, proves Docker, entens Docker.
2. **Privadesa** — Les teves dades (temperatura, humitat, fotos, calendaris) són a casa teva, no pas a Google o Amazon.
3. **Independència** — No depens de ningú. Si vols canviar una cosa, la canvies. Si vols afegir una cosa, l'afegeixes.

## Arquitectura general del BernatLab

```
┌─────────────────────────────────────────────────────────┐
│                      Internet                            │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │       Tailscale       │   ← VPN privada,
              │   (100.x.x.x IPs)     │     sense obrir
              │                       │     ports al router
              └──────────┬───────────┘
                         │
                         ▼
         ┌──────────────────────────────┐
         │   Raspberry Pi 4 (4 GB RAM)  │
         │   Debian 13 Lite · arm64     │
         │   hostname: hortosona        │
         ├──────────────────────────────┤
         │                               │
         │  ┌─────┐  ┌─────┐  ┌──────┐ │
         │  │Portn│  │Uptm │  │Homep │ │   ← Serveis
         │  │9443 │  │3001 │  │3000  │ │     Docker
         │  └─────┘  └─────┘  └──────┘ │
         │                               │
         │  ┌─────┐  ┌─────┐  ┌──────┐ │
         │  │Dockr│  │Tails│  │MQTT  │ │   ← Infra
         │  └─────┘  └─────┘  └──────┘ │
         │                               │
         └──────────────────────────────┘
```

## Els 7 serveis que ja tens desplegats

| Servei | Port | Què fa |
|---|---|---|
| **Tailscale** | — | VPN privada per accedir des de fora |
| **Docker** | — | Contenidors (aïlla serveis) |
| **Portainer** | 9443 | GUI per gestionar Docker |
| **Uptime Kuma** | 3001 | Monitorització 24/7 |
| **Homepage** | 3000 | Panell central amb tots els serveis |
| **MQTT** | 1883 | (previst) Bus de missatges per a sensors |
| **Grafana** | 3000 | (previst) Gràfiques de sensors |

## Filosofia del projecte

1. **Funcionar abans que semblar bonic** — Millor un sistema lleig que funciona, que un de bonic que no.
2. **Documentar-ho tot** — El jo del futur agrairà al jo del passat.
3. **Versionar tot el que es pugui** — Git és el millor amic.
4. **Iterar sobre els artefactes** — v1 → v2 → v3, sense esperar la perfecció.
5. **Validar amb execució real** — No pas prometre; fer.

## Què vindrà

El full de ruta:
1. Ara: Docker, Portainer, Uptime Kuma, Homepage, Tailscale.
2. Pròxim: File Browser, Node-RED, Mosquitto MQTT, InfluxDB, Grafana, PostgreSQL.
3. Més endavant: integració LoRa SX1262 868 MHz, API d'Hort Osona, Telegram, IA local (Ollama).

## Connexions amb altres capítols

- **Cap 2** — Com és la Raspberry Pi 4 per dins.
- **Cap 3** — Com administrar Linux bàsicament.
- **Cap 4** — Com funciona la xarxa i SSH.
- **Cap 5** — Com funciona Docker (el cor del BernatLab).
- **Cap 6-8** — Els tres serveis principals: Portainer, Uptime Kuma, Homepage.
- **Cap 9** — Com versionar-ho tot amb Git.
- **Cap 10** — El full de ruta complet.
