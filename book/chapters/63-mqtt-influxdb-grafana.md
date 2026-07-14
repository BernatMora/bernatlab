# Capítol 63 — La cadena de dades: MQTT, InfluxDB, Grafana

> *"Aquest capítol és el cor de l'hort. Tot el que vingui després (nodes LoRa, sensors, automatitzacions) acaba passant per aquí."*

## 63.1 Què aprendràs

- Què és MQTT i per què és el protocol estàndard per a IoT.
- Com instal·lar **Mosquitto** (broker MQTT).
- Com instal·lar **InfluxDB** (base de dades de sèries temporals).
- Com instal·lar **Telegraf** (ponte entre MQTT i InfluxDB).
- Com instal·lar **Grafana** (visualització).
- Com veure les primeres dades a Grafana.

## 63.2 Durada estimada

1-1.5 hores.

## 63.3 L'arquitectura de dades

Abans de tocar res, entenem què construirem:

```
Sensor (LoRa, ESP32, etc.)
   │
   │ publica a MQTT
   ↓
[ Mosquitto ]  ← broker MQTT (port 1883)
   │
   │ rep dades
   ↓
[ Telegraf ]   ← agent que escolta MQTT i escriu a InfluxDB
   │
   │ escriu a
   ↓
[ InfluxDB ]   ← base de dades de sèries temporals
   │
   │ llegeix
   ↓
[ Grafana ]    ← panell web amb gràfiques
```

Aquesta és la cadena estàndard per a IoT. Funciona.

Alternatives:

- **InfluxDB 1.x** amb el seu propi plugin MQTT (sense Telegraf). Més simple però menys flexible.
- **MQTT → Node-RED → InfluxDB → Grafana**. Node-RED pot fer la part de Telegraf, però afegeix complexitat.
- **MQTT → base de dades SQL → Grafana**. Més potència per a consultes, menys per a sèries temporals.

La meva recomanació: **Telegraf** per la seva senzillesa i perquè és part de la stack InfluxData (els mateixos que fan InfluxDB).

## 63.4 Instal·lar Mosquitto

Crea `~/homelab/secrets/mqtt.env`:

```
MQTT_USER=bernat
MQTT_PASSWORD=una-contrasenya-forta-de-32-caracters
```

**Mai** posis la contrasenya directament al docker-compose.

Crea `~/homelab/compose/mqtt.yml`:

```yaml
version: "3.8"

services:
  mosquitto:
    image: eclipse-mosquitto:2
    container_name: mosquitto
    restart: unless-stopped
    ports:
      - "1883:1883"
      - "9001:9001"
    volumes:
      - ./data/mosquitto/data:/mosquitto/data
      - ./data/mosquitto/log:/mosquitto/log
      - ./mosquitto/mosquitto.conf:/mosquitto/config/mosquitto.conf
      - ./mosquitto/passwd:/mosquitto/config/passwd
    env_file:
      - ../secrets/mqtt.env
```

Crea `~/homelab/compose/mosquitto/mosquitto.conf`:

```
# Configuració bàsica de Mosquitto
persistence true
persistence_location /mosquitto/data/
log_dest stdout

# Autenticació
allow_anonymous false
password_file /mosquitto/config/passwd

# Listener MQTT
listener 1883
protocol mqtt

# Listener WebSockets (opcional, per accedir des del navegador)
listener 9001
protocol websockets
```

Crea el fitxer de contrasenyes:

```bash
cd ~/homelab/compose
docker run --rm -it \
    -v $(pwd)/mosquitto/passwd:/mosquitto/config/passwd \
    eclipse-mosquitto:2 \
    mosquitto_passwd -c /mosquitto/config/passwd $MQTT_USER
```

(Substitueix `$MQTT_USER` pel valor del .env, o passa'l manualment.)

Engega:

```bash
cd ~/homelab/compose
docker compose -f mqtt.yml up -d
```

## 63.5 Provar Mosquitto

Des del teu ordinador, publica un missatge:

```bash
# Publicar
mosquitto_pub -h hortosona -p 1883 \
    -u bernat -P 'contrasenya' \
    -t 'test/hort' -m 'Hola des del BernatLab!'

# Subscriure (en un altre terminal)
mosquitto_sub -h hortosona -p 1883 \
    -u bernat -P 'contrasenya' \
    -t 'test/#' -v
```

Si veus el missatge al segon terminal, tot funciona.

## 63.6 Instal·lar InfluxDB

Crea `~/homelab/secrets/influxdb.env`:

```
DOCKER_INFLUXDB_INIT_MODE=setup
DOCKER_INFLUXDB_INIT_USERNAME=admin
DOCKER_INFLUXDB_INIT_PASSWORD=una-altra-contrasenya-forta
DOCKER_INFLUXDB_INIT_ORG=bernatlab
DOCKER_INFLUXDB_INIT_BUCKET=hort
DOCKER_INFLUXDB_INIT_RETENTION=1y
DOCKER_INFLUXDB_INIT_ADMIN_TOKEN=un-token-llarg-aleatori-de-32-chars
```

Crea `~/homelab/compose/influxdb.yml`:

```yaml
version: "3.8"

services:
  influxdb:
    image: influxdb:2
    container_name: influxdb
    restart: unless-stopped
    ports:
      - "8086:8086"
    volumes:
      - ./data/influxdb:/var/lib/influxdb2
    env_file:
      - ../secrets/influxdb.env
```

Engega:

```bash
cd ~/homelab/compose
docker compose -f influxdb.yml up -d
```

Obre `http://hortosona:8086` al navegador. Hauries de veure la pantalla de benvinguda. Ja està configurat (les variables d'entorn ho fan).

## 63.7 Instal·lar Telegraf

Telegraf escolta MQTT i escriu a InfluxDB.

Crea `~/homelab/compose/telegraf.conf`:

```toml
[agent]
interval = "30s"
flush_interval = "10s"

[[outputs.influxdb_v2]]
urls = ["http://influxdb:8086"]
token = "${INFLUX_TOKEN}"
org = "bernatlab"
bucket = "hort"

[[inputs.mqtt_consumer]]
servers = ["tcp://mosquitto:1883"]
topics = ["sensors/#", "bernatlab/#"]
qos = 0
username = "${MQTT_USER}"
password = "${MQTT_PASSWORD}"
data_format = "json"
tag_keys = ["node", "sensor"]
json_string_fields = ["value"]
```

Crea `~/homelab/compose/telegraf.yml`:

```yaml
version: "3.8"

services:
  telegraf:
    image: telegraf:1.30
    container_name: telegraf
    restart: unless-stopped
    depends_on:
      - mosquitto
      - influxdb
    volumes:
      - ./telegraf.conf:/etc/telegraf/telegraf.conf:ro
    environment:
      - INFLUX_TOKEN=${DOCKER_INFLUXDB_INIT_ADMIN_TOKEN}
      - MQTT_USER=${MQTT_USER}
      - MQTT_PASSWORD=${MQTT_PASSWORD}
    env_file:
      - ../secrets/mqtt.env
      - ../secrets/influxdb.env
```

Engega:

```bash
cd ~/homelab/compose
docker compose -f telegraf.yml up -d
```

Verifica els logs:

```bash
docker logs telegraf
```

Si tot va bé, veuràs línies tipus:

```
2026-07-09T12:00:00Z I! Loaded inputs: mqtt_consumer
2026-07-09T12:00:00Z I! Loaded aggregators:
2026-07-09T12:00:00Z I! Loaded processors:
2026-07-09T12:00:00Z I! Loaded outputs: influxdb_v2
```

## 63.8 Instal·lar Grafana

Crea `~/homelab/compose/grafana.yml`:

```yaml
version: "3.8"

services:
  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    restart: unless-stopped
    ports:
      - "3000:3000"
    volumes:
      - ./data/grafana:/var/lib/grafana
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
      - GF_USERS_ALLOW_SIGN_UP=false
    env_file:
      - ../secrets/grafana.env
```

Crea `~/homelab/secrets/grafana.env`:

```
GRAFANA_PASSWORD=una-contrasenya-forta
```

Engega:

```bash
cd ~/homelab/compose
docker compose -f grafana.yml up -d
```

Obre `http://hortosona:3000`. Login: `admin` / la teva contrasenya. Canvia la contrasenya al primer login.

## 63.9 Connectar Grafana a InfluxDB

A Grafana:

1. **Connections** → **Data sources** → **Add data source**.
2. Tria **InfluxDB**.
3. Configura:
   - URL: `http://influxdb:8086`
   - Organization: `bernatlab`
   - Token: el que has posat al `.env` d'InfluxDB
   - Default bucket: `hort`
4. **Save & test**. Si tot va bé, veuràs "Data source is working".

## 63.10 Provar la cadena sencera

Des de la terminal:

```bash
mosquitto_pub -h hortosona -p 1883 \
    -u bernat -P 'contrasenya' \
    -t 'sensors/hort1/temperatura' \
    -m '{"node":"hort1","sensor":"temperatura","value":23.5,"unit":"C"}'
```

A Grafana:

1. **Explore** (la icona de brúixola a l'esquerra).
2. Tria el data source InfluxDB.
3. Escriu una query com `SELECT mean("value") FROM "hort" WHERE ("sensor" = 'temperatura') GROUP BY time($__interval), node fill(null)`.
4. Veuràs un punt a la gràfica.

Si veus el punt, **tens la cadena sencera funcionant**: del teu terminal a una gràfica a Grafana, passant per MQTT, Telegraf i InfluxDB.

## 63.11 El primer panell

Crea un dashboard:

1. **+** → **Dashboard** → **Add visualization**.
2. Tria InfluxDB.
3. Configura:
   - **From**: `hort`
   - **Measurement**: `mqtt_consumer` (Telegraf usa aquest nom per defecte).
   - **Field**: `value`.
   - **Filters**: `sensor = temperatura`.
4. Tria el tipus de visualització (Time series).
5. Desa el panell.
6. Desa el dashboard.

Ara cada cop que algú publiqui una temperatura a `sensors/hort1/temperatura`, apareixerà al panell.

## 63.12 Com organitzar les dades

A l'hora de publicar a MQTT, tria un esquema de temes clar. Jo uso:

- `sensors/<ubicacio>/<sensor>` per a dades de sensors.
- `bernatlab/<servei>/<accio>` per a esdeveniments del sistema.
- `alerts/<severitat>/<servei>` per a alertes.

Exemple:

- `sensors/hort1/temperatura` → temperatura de l'hort 1.
- `sensors/hort1/humitat` → humitat de l'hort 1.
- `sensors/ciutat/temperatura` → temperatura al sensor de la ciutat.
- `bernatlab/mqtt/disconnect` → esdeveniment de desconnexió.
- `alerts/critical/grafana` → alerta crítica a Grafana.

Això et permetrà filtrar fàcilment a Grafana i Node-RED.

## 63.13 Què ve després

Ja tens la cadena de dades. Al **Cap 64** afegirem **Node-RED**, que ens permetrà fer automatitzacions reals (si la temperatura baixa de 5°C, encén la calefacció de l'hivernacle).

## 63.14 Errors habituals

**Error 1: "Connection refused" a MQTT**.

Comprova que el port 1883 està exposat i que el contenidor està en marxa.

**Error 2: Telegraf no escriu a InfluxDB**.

Mira els logs de Telegraf. Sovint és un token mal copiat o un nom de bucket incorrecte.

**Error 3: Grafana no es connecta a InfluxDB**.

Comprova la URL, el token i el nom d'organització. El "Save & test" t'ho dirà.

**Error 4: les dades arriben però Grafana no les mostra**.

El tema de la query és delicat. Comença amb `SELECT * FROM "mqtt_consumer" LIMIT 10` per veure què hi ha, i refina després.

## 63.15 Resum

Ara tens la cadena de dades completa:

- **Mosquitto** (MQTT) escolta publicacions.
- **Telegraf** les tradueix i les envia a InfluxDB.
- **InfluxDB** les emmagatzema.
- **Grafana** les visualitza.

Això és la base sobre la qual vindrà tot: nodes LoRa, sensors, alertes, automatitzacions. La combinació MQTT + InfluxDB + Grafana és el cor de l'IoT modern.

## 63.16 Exercicis pràctics

1. Instal·la Mosquitto, InfluxDB, Telegraf i Grafana.
2. Configura l'autenticació a Mosquitto.
3. Publica una dada de prova.
4. Connecta Grafana a InfluxDB.
5. Crea el teu primer panell.
6. Publica 5 dades de prova amb valors diferents.
7. Afegeix un monitor d'Uptime Kuma per a Grafana i Mosquitto.
8. Documenta els temes MQTT que has triat.
