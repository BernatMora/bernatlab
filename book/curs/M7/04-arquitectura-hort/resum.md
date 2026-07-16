# Resum - Capitol 4: Arquitectura de l'Hort Osona

## La idea clau

L'Hort Osona te una **arquitectura modular**: cada peça fa una cosa i la fa be, i totes es comuniquen a traves d'un **bus de missatges (MQTT)**. Aixo es diu **arquitectura basada en events** o **pipe-and-filter**. Si una peça falla, la resta continua. Es el mateix patro que segueixen les grans plataformes IoT (AWS IoT, Google Cloud IoT, etc.) pero en petit, a la teva RPi.

## El pipeline de dades

El flux de dades de l'hort es pot resumir en 6 etapes:

```
Sensors -> Gateway -> MQTT broker -> Processadors -> Emmagatzematge -> API/Web
   |          |           |               |                |              |
 MiFlora    RPi         Mosquitto     Python/Node      InfluxDB      PWA
 BME280     ESP32                     scripts          PostgreSQL    GitHub
 LoRa       gateway                   InfluxDB-relay   MinIO         Pages
```

Pas a pas:

1. **Sensor (MiFlora, BME280, SX1262)**: captura la dada cada N minuts.
2. **Gateway (RPi o ESP32)**: llegeix el sensor i el publica a MQTT.
3. **Broker MQTT (Mosquitto)**: rep el missatge i el distribueix a tots els subscriptors interessats.
4. **Processador (Python script)**: agafa els missatges i els escriu a la base de dades pertinent.
5. **Emmagatzematge (InfluxDB, PostgreSQL, MinIO)**: guarda la dada en format adequat.
6. **API/Web (Flask, PWA)**: llegeix les dades i les mostra a l'hortola.

Cada etapa es **independent**: si la PWA no funciona, les dades segueixen entrant a InfluxDB. Si un processador falla, el buffer de Mosquitto retè els missatges.

## Diagrama complet

```
                  HORT OSONA
                  ==========

  +---------+    +---------+    +---------+
  | MiFlora |    | BME280  |    | SX1262  |
  |  (BLE)  |    |  (I2C)  |    |  (LoRa) |
  +----+----+    +----+----+    +----+----+
       |              |              |
       | BLE          | I2C          | 868 MHz
       v              v              v
  +---------+    +---------+    +---------+
  | RPi     |    | ESP32   |    | RPi     |
  | gateway |    | gateway |    | gateway |
  +----+----+    +----+----+    +----+----+
       |              |              |
       +------+-------+-----+--------+
              |             |
              v             v
        +-----------------------+
        |   Mosquitto MQTT      |
        |   (broker :1883)      |
        +-----------+-----------+
                    |
        +-----------+-----------+
        |                       |
        v                       v
  +-------------+       +-------------+
  | InfluxDB    |       | PostgreSQL  |
  | (sensors)   |       | (calendar,  |
  |             |       |  regs)      |
  +------+------+       +------+------+
         |                     |
         +----------+----------+
                    |
                    v
           +----------------+
           |  Flask API      |
           |  (port 5000)   |
           +-------+--------+
                   |
                   v
           +----------------+
           |  PWA (client)  |
           |  GitHub Pages  |
           +----------------+
```

## Per que MQTT i no peticions HTTP

Podriem fer que cada sensor faci una peticio HTTP POST a una API cada vegada. Pero MQTT te avantatges clars:

- **Push en lloc de pull**: el sensor publica i el broker distribueix. No cal que el servidor pregunti.
- **Desacoblat**: el sensor no sap qui consumeix les seves dades. Qualsevol subscriptor pot afegir-se.
- **QoS (Quality of Service)**: pots garantir que el missatge arriba (QoS 1 o 2).
- **Last Will and Testament (LWT)**: pots saber si un sensor ha caigut.
- **Buffer integrat**: si el consumidor esta offline, el broker retè els missatges.
- **Topic-based routing**: pots subsriure't nomes als missatges que t'interessen (e.g. `hort-osona/miflora/#`).

HTTP esta be per a peticions puntuals (API REST, formularis), pero per a **streaming de dades** MQTT es la opcio natural.

## Com es comuniquen les peces: els topics

A l'Hort Osona usem un esquema de topics **jerarquic**:

```
hort-osona/
   miflora/
      miflora-1B32    <- sensor del toma-cherry
      miflora-1B33    <- pebrot
      miflora-1B34    <- enciam
   bme/
      hivernacle
      exterior
   lora/
      node1           <- sensor al camp de cereals
      node2           <- pou
   cmd/
      reg/toma-cherry <- ordres de reg
      llum/hivernacle
   status/
      gateway/rpi1
      gateway/rpi2
```

Qualsevol subscriptor pot escoltar tot el que passa amb `hort-osona/#`, o nomes una part amb `hort-osona/miflora/#`. Es el que fan els dashboards de Grafana, les alertes, etc.

## Les diferents capes de software

A l'Hort Osona cada "servei" es un **contenidor Docker** (o podria ser-ho). Els motius:

- Cada servei te el seu propi entorn (Python 3.11, Python 3.9, Node 18).
- Es poden actualitzar independentment.
- Es poden moure a una altra maquina amb un sol `docker run`.
- Es poden escalar (varios contenidors del mateix servei).

Exemple de `docker-compose.yml` (resumit):

```yaml
services:
  mosquitto:
    image: eclipse-mosquitto:2
    ports:
      - "1883:1883"
    volumes:
      - ./mosquitto/config:/mosquitto/config
      - ./mosquitto/data:/mosquitto/data

  influxdb:
    image: influxdb:2.7
    ports:
      - "8086:8086"
    volumes:
      - influxdb-data:/var/lib/influxdb2

  api:
    build: ./api
    ports:
      - "5000:5000"
    environment:
      - INFLUXDB_URL=http://influxdb:8086
      - MQTT_HOST=mosquitto

  miflora-gateway:
    build: ./gateways/miflora
    devices:
      - "/dev/bluetooth:/dev/bluetooth"
    privileged: true
```

## La RPi central: el cor de l'hort

A l'Hort Osona tenim una **RPi 4B** (4 GB RAM) al centre que corre:

- Mosquitto (broker MQTT)
- InfluxDB (series temporals)
- PostgreSQL (dades de gestio)
- MinIO (emmagatzematge d'imatges)
- Flask API
- Diversos scripts Python (gateways BLE, LoRa, etc.)
- Grafana (visualitzacio interna)

Això son molts serveis en una sola RPi. Funciona perque:

- La RPi 4 te 4 GB de RAM i 4 nuclis.
- Molts serveis son llegers (Mosquitto gasta 30 MB, Grafana 200 MB).
- Disquet SSD extern per a la base de dades.

Si el sistema creix, podem moure Grafana a un altre maquina, o afegir una RPi secundaria.

## Alta disponibilitat: què passa quan algo falla

A l'Hort Osona tenim varies capes de tolerancies a falles:

1. **Sensor**: si la pila es mor, el sensor calla. Solucio: pila nova o canviar de sensor.
2. **Gateway RPi**: si la RPi cau, els missatges es perden (BLE no te buffer). Solucio: afegir un gateway secundari.
3. **Mosquitto**: te buffer a disc per defecte. Si cau, els missatges nous es perden pero l'historic es conserva.
4. **InfluxDB**: te write-ahead log (WAL). Si cau, en reiniciar pot recuperar les ultimes escriptures.
5. **API/PWA**: si cauen, les dades segueixen entrant. La visualitzacio nomes es perd temporalment.

El pitjor cas es que **la RPi central** es mori. Aixo pasa amb microSD (escriptores limit). Solucio:

- Usar **SSD extern** en lloc de microSD.
- Fer **backups** diaries d'InfluxDB i PostgreSQL.
- Considerar un **mini PC** o una segona RPi per failover.

## Patrons de procesament

A l'Hort Osona usem tres patrons basics:

1. **Pipeline (flux lineal)**: sensor -> MQTT -> InfluxDB. Per a la majoria de dades.
2. **Fan-out (un a molts)**: un missatge MQTT el llegeixen multiples processadors (e.g. InfluxDB + alerta de gelada).
3. **Fan-in (molts a un)**: multiples sensors agregats en un resum (e.g. temperatura mitjana de l'hort).

Exemple de fan-out amb Python:

```python
# Un missatge de BME280 activa 3 subscriptors:
# 1. influxdb_writer.py: guarda a InfluxDB
# 2. frost_alert.py: si temp < 2°C, envia alerta
# 3. dashboard_cache.py: actualitza Redis per la PWA
```

## Connexions amb altres capitols

- **M7 Cap 2, 3** - Sensors concrets que alimenten el pipeline.
- **M7 Cap 5** - MQTT es el bus central.
- **M7 Cap 6** - InfluxDB es on acaben les dades.
- **M7 Cap 7** - L'API exposa les dades a la web.
- **M7 Cap 8** - La PWA consumeix l'API.
