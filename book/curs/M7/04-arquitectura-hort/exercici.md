# Exercici practic - Capitol 4: Arquitectura de l'Hort Osona

> 40-60 min · Real a la RPi amb Docker

## Objectiu

Muntar l'arquitectura completa de l'Hort Osona en local amb Docker Compose: Mosquitto + InfluxDB + un script Python que escolta MQTT i escriu a InfluxDB. Acabaras amb el pipeline funcionant.

## Requisits

- RPi amb Docker i Docker Compose
- 40-60 min

## Pas 1: Estructura del projecte (5 min)

Crea la estructura de carpetes per al projecte:

```bash
mkdir -p ~/hort-osona/{mosquitto/config,mosquitto/data,influxdb,scripts,grafana,api}
cd ~/hort-osona
```

Estructura final:

```
hort-osona/
   docker-compose.yml
   mosquitto/
      config/
         mosquitto.conf
      data/
   influxdb/
   scripts/
      mqtt_to_influxdb.py
      requirements.txt
   api/
   grafana/
```

## Pas 2: Configura Mosquitto (5 min)

Crea `mosquitto/config/mosquitto.conf`:

```conf
persistence true
persistence_location /mosquitto/data/

listener 1883
allow_anonymous false
password_file /mosquitto/config/passwd

log_dest stdout
log_type error
log_type warning
log_type notice
log_type information
```

Crea un usuari amb password:

```bash
# Dins del contenidor o amb docker
docker run --rm -it eclipse-mosquitto:2 \
   sh -c "mosquitto_passwd -c -b /tmp/passwd hort-osona secretpass"
```

Copia el fitxer `passwd` a `mosquitto/config/passwd`.

## Pas 3: Crea el docker-compose.yml (10 min)

```yaml
version: "3.9"

services:
  mosquitto:
    image: eclipse-mosquitto:2
    container_name: hort-mosquitto
    ports:
      - "1883:1883"
    volumes:
      - ./mosquitto/config:/mosquitto/config
      - ./mosquitto/data:/mosquitto/data
    restart: unless-stopped

  influxdb:
    image: influxdb:2.7
    container_name: hort-influxdb
    ports:
      - "8086:8086"
    environment:
      - DOCKER_INFLUXDB_INIT_MODE=setup
      - DOCKER_INFLUXDB_INIT_USERNAME=admin
      - DOCKER_INFLUXDB_INIT_PASSWORD=adminsecret
      - DOCKER_INFLUXDB_INIT_ORG=bernatlab
      - DOCKER_INFLUXDB_INIT_BUCKET=hort-osona
      - DOCKER_INFLUXDB_INIT_RETENTION=30d
    volumes:
      - influxdb-data:/var/lib/influxdb2
    restart: unless-stopped

  mqtt-to-influx:
    build: ./scripts
    container_name: hort-mqtt-influx
    depends_on:
      - mosquitto
      - influxdb
    environment:
      - MQTT_HOST=mosquitto
      - MQTT_PORT=1883
      - INFLUXDB_URL=http://influxdb:8086
      - INFLUXDB_TOKEN=adminsecret
      - INFLUXDB_ORG=bernatlab
      - INFLUXDB_BUCKET=hort-osona
    restart: unless-stopped

  grafana:
    image: grafana/grafana:10.4
    container_name: hort-grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana-data:/var/lib/grafana
    depends_on:
      - influxdb
    restart: unless-stopped

volumes:
  influxdb-data:
  grafana-data:
```

Aixeca tot:

```bash
cd ~/hort-osona
docker compose up -d
docker compose ps
```

## Pas 4: Crea el servei mqtt-to-influx (15 min)

Crea `scripts/Dockerfile`:

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY mqtt_to_influxdb.py .
CMD ["python", "mqtt_to_influxdb.py"]
```

Crea `scripts/requirements.txt`:

```
paho-mqtt==1.6.1
influxdb-client==1.39.0
pyyaml==6.0
```

Crea `scripts/mqtt_to_influxdb.py`:

```python
#!/usr/bin/env python3
"""Escolta MQTT i escriu a InfluxDB."""

import os
import json
import logging
from datetime import datetime, timezone
import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point, WriteOptions

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s')
log = logging.getLogger(__name__)

MQTT_HOST = os.environ["MQTT_HOST"]
MQTT_PORT = int(os.environ.get("MQTT_PORT", 1883))
INFLUX_URL = os.environ["INFLUXDB_URL"]
INFLUX_TOKEN = os.environ["INFLUXDB_TOKEN"]
INFLUX_ORG = os.environ["INFLUXDB_ORG"]
INFLUX_BUCKET = os.environ["INFLUXDB_BUCKET"]

# InfluxDB
influx = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
write_api = influx.write_api(write_options=WriteOptions(batch_size=200,
                                                         flush_interval=10s))


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        log.info("Connectat a MQTT, subscribint...")
        client.subscribe("hort-osona/#")
    else:
        log.error(f"Error connectant MQTT: {rc}")


def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload)
    except json.JSONDecodeError:
        log.warning(f"Payload no JSON: {msg.topic}")
        return

    topic_parts = msg.topic.split("/")
    # hort-osona/miflora/1B32 -> measurement="miflora", tags=device=1B32
    if len(topic_parts) < 3:
        return

    family = topic_parts[1]  # miflora, bme, lora
    device = topic_parts[2] if len(topic_parts) > 2 else "unknown"

    point = Point(family).tag("device", device).tag("topic", msg.topic)
    for k, v in payload.items():
        if isinstance(v, (int, float)):
            point = point.field(k, v)
        elif k == "ts":
            try:
                t = datetime.fromisoformat(v.replace("Z", "+00:00"))
                point = point.time(t)
            except ValueError:
                pass

    write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=point)
    log.info(f"Escrit {family}/{device} amb {len(payload)} camps")


client = mqtt.Client("mqtt-to-influx")
client.username_pw_set("hort-osona", "secretpass")
client.on_connect = on_connect
client.on_message = on_message

log.info(f"Connectant a {MQTT_HOST}:{MQTT_PORT}...")
client.connect(MQTT_HOST, MQTT_PORT, 60)
client.loop_forever()
```

Compila el servei:

```bash
docker compose build mqtt-to-influx
docker compose up -d mqtt-to-influx
```

## Pas 5: Publica dades de prova (5 min)

Publica un missatge MQTT d'exemple:

```bash
mosquitto_pub -h localhost -p 1883 \
   -u hort-osona -P secretpass \
   -t "hort-osona/miflora/1B32" \
   -m '{"device":"miflora-1B32","ts":"2026-04-12T12:00:00Z","soil_moisture":42,"soil_temp_c":18.5,"ec_us_cm":820,"lux":18000,"battery":87}'
```

Mira els logs del servei:

```bash
docker compose logs -f mqtt-to-influx
```

Hauries de veure:

```
[2026-04-12 12:00:00] Connectat a MQTT, subscribint...
[2026-04-12 12:00:01] Escrit miflora/1B32 amb 6 camps
```

## Pas 6: Verifica amb InfluxDB CLI (5 min)

```bash
docker compose exec influxdb influx query \
   'from(bucket:"hort-osona") |> range(start:-1h) |> filter(fn: (r) => r._measurement == "miflora")' \
   --org bernatlab
```

Hauries de veure les dades. Tambe pots entrar a Grafana (`http://<ip-rpi>:3000`, admin/admin) i crear un dashboard:

- Add data source: InfluxDB, URL `http://influxdb:8086`, org `bernatlab`, token `adminsecret`, bucket `hort-osona`.
- New dashboard -> Add panel.
- Query: `from(bucket: "hort-osona") |> range(start: v.timeRangeStart) |> filter(fn: (r) => r._measurement == "miflora" and r._field == "soil_moisture")`.

## Validacio

Has acabat si:

- [ ] Has aixecat Mosquitto, InfluxDB, Grafana i mqtt-to-influx amb `docker compose up`.
- [ ] Has publicat un missatge amb `mosquitto_pub` i ha estat rebut.
- [ ] El servei mqtt-to-influx ha escrit el punt a InfluxDB.
- [ ] Has verificat amb `influx query` que la dada esta emmagatzemada.
- [ ] Has configurat Grafana per visualitzar les dades.

## Per aprofundir

- Afegeix autenticacio TLS a Mosquitto per seguretat.
- Configura retencio automatica (downsample) a InfluxDB.
- Connecta el servei MiFlora del capitol 2 a aquest pipeline.
- Afegeix una alerta de gelada amb un script Python que escolti `hort-osona/bme/#` i enviï un correu si temp < 2°C.
- Monitora els serveis amb Prometheus + Grafana (meta-monitoratge).
