# Resum - Capitol 6: InfluxDB per a l'Hort Osona

## La idea clau

**InfluxDB** es la base de dades de series temporals (TSDB) que l'Hort Osona fa servir per guardar totes les lectures de sensors. Es com una base de dades SQL pero optimitzada per emmagatzemar **milions de punts amb un timestamp** i fer consultes sobre intervals de temps de manera rapidissima. A diferencia de PostgreSQL o MySQL, no te taules ni files: te **measurements, tags i fields**. La diferencia es critica quan tens 100.000 lectures al dia.

## Que es una base de dades de series temporals

Una TSDB (Time Series Database) te un model de dades especialitzat:

```
Mesura   Tags                  Fields                Time
miflora  device=1B32, sec=toma soil_moisture=42,     2026-04-12T10:00:00Z
                                     soil_temp=18.5,
                                     ec=820, lux=18000
```

- **Measurement**: el "tipus" de dada (miflora, bme, lora, cmd).
- **Tags**: indexats, per agrupar (device, sector, hivernacle). Son strings.
- **Fields**: els valors numerics (soil_moisture, temp_c, ec, lux). Son float64/int64/bool/string.
- **Time**: timestamp nanosecond-precision.

A PostgreSQL ho fariem amb una taula `lectures(id, device, ts, moisture, temp, ec, lux)`. Pero aquesta taula creix rapidissim i les consultes "mitjana de les ultimes 24 hores per device" son lentes perque has d'escanellar moltes files. InfluxDB esta dissenyat exactament per aquestes consultes.

## Per que InfluxDB i no PostgreSQL

| Aspecte | PostgreSQL | InfluxDB |
|---------|------------|----------|
| Tipus | Relacional | Time series |
| Consultes "ultims 7 dies per device" | Lent amb milions de files | Rapidisim |
| Compressio | Baixa | ~10x millor |
| Retencio automatica | Cal scripts | Natiu (1d, 7d, 30d, inf) |
| Downsampling | Cal fer-ho a ma | Natiu amb "tasks" |
| APIs | SQL | Flux, InfluxQL, SQL |
| Recursos | Pesat | Lleuger per a TSDB |

A l'Hort Osona fem servir **els dos**: InfluxDB per a series temporals, PostgreSQL per a dades relacionals (calendar, regs, configuracio). Es la regla d'or: **usa la BD adequada per a cada mena de dada**.

## InfluxDB 1.x vs 2.x vs 3.x

Hi ha tres versions principals:

- **InfluxDB 1.x**: classic, nomes InfluxQL. Lleuger i estable. Es la versio que molta gent encara usa.
- **InfluxDB 2.x**: amb UI web, tasks, checks, dashboards basics. La mes utilitzada actualment.
- **InfluxDB 3.0 (IOx)**: reescrit en Rust, amb motor columnar i suport SQL. Mes rapid pero relativament nou.

A l'Hort Osona usem **InfluxDB 2.7** perque te UI web (per depurar), suport nadiu de tasks (per downsample), i llibreries Python cuidades.

## Arquitectura d'InfluxDB 2.x

InfluxDB 2.x te aquests conceptes:

- **Organization (Org)**: contenidor aillat, com un "tenant". A l'Hort Osona tenim `bernatlab`.
- **Bucket**: contenidor de dades amb retencio. Tenim `hort-osona` amb retencio 30 dies raw i 1 any downsample 1h.
- **Measurement**: com una "taula" a SQL.
- **Tag**: indexat.
- **Field**: valor numeric.
- **Point**: un registre amb timestamp, measurement, tags i fields.
- **Task**: proces automatic que pot agafar dades i transformar-les.
- **Check + Notification Rule**: alerta quan una query retorna valor problematic.

```
+--------------------------------+
|  Organization: bernatlab       |
+--------------------------------+
|                                |
|  Bucket: hort-osona            |
|    - Retention: 30d            |
|    - Measurements: miflora,    |
|      bme, lora, cmd            |
|                                |
|  Tasks:                        |
|    - downsample_1h             |
|    - alert_frost               |
|                                |
+--------------------------------+
```

## El llenguatge Flux

Flux es el llenguatge de consulta d'InfluxDB 2.x. Es funcional (com una pipeline):

```flux
from(bucket: "hort-osona")
  |> range(start: -24h)
  |> filter(fn: (r) => r._measurement == "miflora")
  |> filter(fn: (r) => r._field == "soil_moisture")
  |> filter(fn: (r) => r.device == "miflora-1B32")
  |> aggregateWindow(every: 1h, fn: mean, createEmpty: false)
  |> yield(name: "mitjana")
```

Cada funcio es un "operador" amb `|>`. Es similar a les pipes Unix.

Alternativa: **InfluxQL** (llenguatge SQL-like). Mes facil si vens de SQL pero menys potent. A l'Hort Osona usem Flux per a tasques complexes i InfluxQL per a consultes basiques del dashboard.

## Com escriure dades amb Python

Exemple usant la llibreria `influxdb-client`:

```python
from datetime import datetime, timezone
from influxdb_client import InfluxDBClient, Point, WriteOptions

client = InfluxDBClient(
    url="http://localhost:8086",
    token="adminsecret",
    org="bernatlab"
)
write_api = client.write_api(write_options=WriteOptions(batch_size=500, flush_interval=10_000))

# Escriure un punt
point = Point("miflora").tag("device", "miflora-1B32") \
    .field("soil_moisture", 42.0) \
    .field("soil_temp_c", 18.5) \
    .field("ec_us_cm", 820) \
    .field("lux", 18000) \
    .time(datetime.now(timezone.utc))

write_api.write(bucket="hort-osona", org="bernatlab", record=point)
```

La `WriteOptions` permet fer **batch**: agrupes 500 punts i els escrius tots de cop, molt mes rapid.

## Com llegir dades amb Python

```python
from influxdb_client import InfluxDBClient

client = InfluxDBClient(url="http://localhost:8086",
                        token="adminsecret", org="bernatlab")
query_api = client.query_api()

# Consulta Flux
query = '''
from(bucket: "hort-osona")
  |> range(start: -1h)
  |> filter(fn: (r) => r._measurement == "miflora")
  |> filter(fn: (r) => r._field == "soil_moisture")
  |> filter(fn: (r) => r.device == "miflora-1B32")
'''

result = query_api.query(query)
for table in result:
    for record in table.records:
        print(f"{record.get_time()} {record.get_field()}={record.get_value()}")
```

## Retention policies i downsampling

InfluxDB 2.x te **tasks** per aixo. Exemple: cada hora, agafem les lectures raw i les agregem a una mesura `_1h` amb la mitjana:

```flux
option task = {name: "downsample_1h", every: 1h}

from(bucket: "hort-osona")
  |> range(start: -1h, stop: now())
  |> filter(fn: (r) => r._measurement =~ /^(miflora|bme|lora)$/)
  |> aggregateWindow(every: 1h, fn: mean, createEmpty: false)
  |> to(bucket: "hort-osona-downsampled", org: "bernatlab")
```

Aixo permet:
- Guardar les dades raw durant 30 dies.
- Guardar les dades agregades a 1h durant 1 any.
- Guardar les dades agregades a 1dia durant 5 anys.

I les consultes son rapidissimes perquè la finestra es mes petita.

## Alertes amb InfluxDB

Una **Check** es una consulta que es evalua periodicament. Si el resultat passa d'un llindar, s'activa una **Notification Rule** que pot enviar:

- Correu electronic
- Webhook (e.g. Telegram, Slack)
- Alerta a la UI

Exemple de check de gelada:

```flux
from(bucket: "hort-osona")
  |> range(start: -5m)
  |> filter(fn: (r) => r._measurement == "bme")
  |> filter(fn: (r) => r._field == "temp_c")
  |> mean()
  |> yield(name: "temp_mitjana")
  |> map(fn: (r) => ({r with critico: r._value < 2.0}))
```

Si la temperatura mitjana dels ultims 5 min es < 2°C, s'envia una alerta per Telegram a l'hortola.

## Line Protocol: comandes crues

Si no tens una llibreria, pots escriure directament amb el "line protocol":

```bash
# Escriure un punt amb curl
curl -XPOST "http://localhost:8086/api/v2/write?org=bernatlab&bucket=hort-osona" \
   -H "Authorization: Token adminsecret" \
   --data 'miflora,device=miflora-1B32 soil_moisture=42,soil_temp_c=18.5 1712926800000000000'
```

Format: `measurement,tag=value,tag=value field=value,field=value timestamp_ns`.

El timestamp en nanosegons. Per obtenir-lo en Python:

```python
import time
ts_ns = int(time.time() * 1e9)
```

## Instal·lacio a la RPi

Amb Docker:

```bash
docker run -d --name hort-influxdb \
   -p 8086:8086 \
   -v influxdb-data:/var/lib/influxdb2 \
   -e DOCKER_INFLUXDB_INIT_MODE=setup \
   -e DOCKER_INFLUXDB_INIT_USERNAME=admin \
   -e DOCKER_INFLUXDB_INIT_PASSWORD=adminsecret \
   -e DOCKER_INFLUXDB_INIT_ORG=bernatlab \
   -e DOCKER_INFLUXDB_INIT_BUCKET=hort-osona \
   -e DOCKER_INFLUXDB_INIT_RETENTION=30d \
   influxdb:2.7
```

Despres accedeix a `http://<ip-rpi>:8086` per la UI web. Aqui pots:

- Crear buckets.
- Veure les dades amb Data Explorer.
- Crear tasks i checks.
- Gestionar usuaris i tokens.

## Backups

InfluxDB te una eina nativa de backup:

```bash
# Backup
docker exec hort-influxdb influx backup /tmp/backup
docker cp hort-influxdb:/tmp/backup ./influxdb-backup-$(date +%Y%m%d)

# Restore
docker cp ./influxdb-backup-20260412 hort-influxdb:/tmp/restore
docker exec hort-influxdb influx restore /tmp/restore
```

A l'Hort Osona fem backup diari automatic amb un cron job.

## Connexions amb altres capitols

- **M7 Cap 1** - InfluxDB es on acaben les dades de sensors.
- **M7 Cap 4** - El pipeline acaba aqui.
- **M7 Cap 5** - Les dades arriben via MQTT.
- **M7 Cap 7** - L'API consulta InfluxDB per exposar-les.
- **M7 Cap 10** - Casos reals amb queries de InfluxDB.
