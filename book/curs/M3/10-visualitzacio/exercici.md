# Exercici practic — Capitol 10: Visualitzacio amb Grafana

> 40-50 min · Real al teu sistema

## Objectiu

Instal·lar Grafana amb Docker, connectar-la a InfluxDB, crear un dashboard amb diversos panells i configurar una alerta.

## Requisits

- Tailscale actiu
- Connexio SSH a la RPi
- Docker funcionant
- InfluxDB ja funcionant (del cap 6)
- 40-50 minuts

## Pas 1: Instal·la Grafana amb Docker (5 min)

```bash
mkdir -p /home/pi/bernatlab/grafana/{data,config}

docker run -d --name bernatlab-grafana \
  -p 127.0.0.1:3000:3000 \
  -e GF_SECURITY_ADMIN_USER=bernat \
  -e GF_SECURITY_ADMIN_PASSWORD=bernat2025 \
  -e GF_INSTALL_PLUGINS="" \
  -v /home/pi/bernatlab/grafana/data:/var/lib/grafana \
  -v /home/pi/bernatlab/grafana/config:/etc/grafana \
  grafana/grafana-oss:latest

sleep 15
docker ps | grep grafana
```

## Pas 2: Accedeix a la UI web (5 min)

Obre `http://localhost:3000` (via Tailscale). Login: `bernat` / `bernat2025`. **Canvia la contrasenya!**

## Pas 3: Connecta a InfluxDB (10 min)

1. **Connections > Data Sources > Add data source > InfluxDB**
2. Configura:
   - Query language: **Flux**
   - URL: `http://bernatlab-influxdb:8086`
   - Organization: `bernatlab`
   - Token: el token que vas crear al cap 6
   - Default bucket: `hort`
3. **Save & test**: hauria de dir "datasource is working".

## Pas 4: Crea un panell de temperatura (10 min)

1. **Dashboards > New > New dashboard**
2. **Add visualization**
3. Font de dades: InfluxDB
4. Codi Flux:

```flux
from(bucket: "hort")
  |> range(start: -24h)
  |> filter(fn: (r) => r._measurement == "temperatura")
  |> aggregateWindow(every: 5m, fn: mean, createEmpty: false)
```

5. Tipus: **Time series**
6. Titol: "Temperatura ultimes 24h"
7. Guarda el panell

## Pas 5: Afegeix mes panells (10 min)

Repeteix per crear:

1. **Humitat actual**: tipus Stat, consulta:
   ```flux
   from(bucket: "hort")
     |> range(start: -1h)
     |> filter(fn: (r) => r._measurement == "humitat")
     |> last()
   ```

2. **Mitjana temperatura 7 dies**: tipus Bar chart, agrega per dia.

3. **Gauge d'humitat**: tipus Gauge, amb llindars 0-40 (sec), 40-70 (normal), 70-100 (humit).

## Pas 6: Configura una alerta (5 min)

1. Edita el panell de temperatura
2. **Alert > Create alert rule**
3. Condicio: `WHEN last() IS BELOW 2`
4. Avaluacio: cada 1m durant 5m
5. Contact point: (configura'n un, per exemple webhook a Telegram)
6. Guarda

## Pas 7: Exporta el dashboard (5 min)

1. **Share > Export > View JSON**
2. Copia el JSON
3. Desa'l a `/home/pi/bernatlab/grafana/dashboards/hort.json`

## Validacio

Has acabat si:

- [ ] Has instal·lat Grafana amb Docker.
- [ ] T'has connectat i has canviat la contrasenya.
- [ ] Has afegit InfluxDB com a font de dades.
- [ ] Has creat un dashboard amb almenys 3 panells.
- [ ] Has configurat una alerta.
- [ ] Has exportat el dashboard a JSON.

## Per aprofundir

- Investiga com **compartir** dashboards publicament (anonymous access).
- Prova de configurar alertes per **Telegram** o **Discord** via webhook.
- Importa una **plantilla oficial** de Grafana (per exemple, Docker monitoring).
- Investiga com **provisioning** automatic de dashboards (via fitxers YAML).
- Practica amb **variables** per fer dashboards dinamics.
