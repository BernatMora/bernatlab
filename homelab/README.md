# homelab/

Configuració del servidor BernatLab (Raspberry Pi 4 amb Debian 13 Lite).

Estructura recomanada:

```
homelab/
├── compose/
│   ├── core/         # portainer, homepage, uptime-kuma
│   ├── iot/          # mosquitto, nodered, telegraf
│   ├── monitoring/   # grafana, influxdb
│   ├── data/         # postgres, filebrowser
│   └── api/          # fastapi (API pública Hort Osona)
├── scripts/          # scripts de manteniment
│   ├── backup.sh
│   ├── publish.sh
│   └── update.sh
├── docs/             # documentació operativa
│   ├── runbook.md
│   ├── incidents.md
│   └── security.md
└── data/             # bind mounts persistents (no versionat)
```

## A tenir en compte

- Tots els serveis segueixen el patró descrit al **Mòdul 1, Capítol 5** (Docker des de zero).
- Les dades viuen a `homelab/data/` i **no es versionen** (estan al `.gitignore`).
- Cada servei té un usuari propi a Mosquitto (veure Mòdul 2, Capítol 13).
- Les claus secretes van al `.env` del projecte (no al codi).
- La integració amb la Raspberry es fa via Tailscale (Mòdul 1, Capítol 4).

## Per començar

Quan la Raspberry Pi 4 estigui disponible:

```bash
ssh bernat@100.x.y.z
cd /home/bernat
git clone https://github.com/bernatmora/bernatlab.git
cd bernatlab/homelab
# Copiar el fitxer .env.example a .env i omplir les claus
cp compose/core/.env.example compose/core/.env
$EDITOR compose/core/.env
# Aixecar els serveis
cd compose/core && docker compose up -d
```

## Documentació detallada

La descripció completa de cada servei és al llibre:

- **Portainer**: Mòdul 1, Capítol 6
- **Uptime Kuma**: Mòdul 1, Capítol 7
- **Homepage**: Mòdul 1, Capítol 8
- **Mosquitto**: Mòdul 2, Capítol 13
- **InfluxDB**: Mòdul 2, Capítol 15
- **Telegraf**: Mòdul 2, Capítol 16
- **Node-RED**: Mòdul 2, Capítol 17
- **Grafana**: Mòdul 2, Capítol 19
- **API FastAPI**: Mòdul 2, Capítol 20
- **Integració Hort Osona**: Mòdul 2, Capítol 21
- **Operativa**: Mòdul 2, Capítol 22
