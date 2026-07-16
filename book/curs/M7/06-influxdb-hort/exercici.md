# Exercici practic - Capitol 6: InfluxDB per a l'Hort Osona

> 40-60 min · Real a la RPi amb Docker

## Objectiu

Instal·lar InfluxDB 2.7 amb Docker, crear buckets, escriure dades d'exemple amb Python, fer consultes amb Flux, i muntar una task de downsampling. Acabaras amb una TSDB funcional amb dades reials.

## Requisits

- RPi amb Docker
- Python 3.10+
- 40-60 min

## Pas 1: Inicia InfluxDB amb Docker (5 min)

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

docker logs hort-influxdb
```

Espera uns 30 segons i accedeix a `http://<ip-rpi>:8086`. Hauries de veure la UI d'InfluxDB. Login: `admin` / `adminsecret`.

A la UI:

- Crea un bucket `hort-osona-downsampled` amb retencio 365d.
- Crea un token amb permisos de lectura/escriptura a `bernatlab`. Guarda'l.

## Pas 2: Instal·la les dependencies Python (5 min)

```bash
mkdir -p ~/hort-osona/scripts
cd ~/hort-osona/scripts
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install influxdb-client pyyaml
```

Crea `.env`:

```bash
INFLUXDB_URL=http://localhost:8086
INFLUXDB_TOKEN=adminsecret
INFLUXDB_ORG=bernatlab
INFLUXDB_BUCKET=hort-osona
```

## Pas 3: Escriu dades d'exemple (10 min)

Crea `seed_data.py`:

```python
#!/usr/bin/env python3
"""Genera 1000 punts fake dels ultims 7 dies."""

import os
import random
import time
from datetime import datetime, timedelta, timezone
from influxdb_client import InfluxDBClient, Point, WriteOptions
from dotenv import load_dotenv

load_dotenv()

URL = os.environ["INFLUXDB_URL"]
TOKEN = os.environ["INFLUXDB_TOKEN"]
ORG = os.environ["INFLUXDB_ORG"]
BUCKET = os.environ["INFLUXDB_BUCKET"]

client = InfluxDBClient(url=URL, token=TOKEN, org=ORG)
write_api = client.write_api(
    write_options=WriteOptions(batch_size=200, flush_interval=10_000)
)

devices = ["miflora-1B32", "miflora-1B33", "miflora-1B34"]
now = datetime.now(timezone.utc)

print("Generant 1000 punts...")
for i in range(1000):
    device = random.choice(devices)
    ts = now - timedelta(hours=random.uniform(0, 168))  # 7 dies

    point = Point("miflora").tag("device", device) \
        .field("soil_moisture", round(30 + random.random() * 30, 1)) \
        .field("soil_temp_c", round(15 + random.random() * 8, 1)) \
        .field("ec_us_cm", random.randint(400, 1200)) \
        .field("lux", random.randint(5000, 30000)) \
        .time(ts)

    write_api.write(bucket=BUCKET, org=ORG, record=point)

    if (i + 1) % 100 == 0:
        print(f"  {i + 1} punts...")

write_api.close()
client.close()
print("Fet!")
```

Necessites `python-dotenv`:

```bash
pip install python-dotenv
python3 seed_data.py
```

Hauries de veure "1000 punts... Fet!". A la UI d'InfluxDB, ves a Data Explorer i selecciona el bucket `hort-osona`, measurement `miflora`. Hauries de veure les dades.

## Pas 4: Consulta amb Python (10 min)

Crea `query_data.py`:

```python
#!/usr/bin/env python3
"""Consulta dades a InfluxDB."""

import os
from influxdb_client import InfluxDBClient
from dotenv import load_dotenv

load_dotenv()

client = InfluxDBClient(
    url=os.environ["INFLUXDB_URL"],
    token=os.environ["INFLUXDB_TOKEN"],
    org=os.environ["INFLUXDB_ORG"]
)
query_api = client.query_api()

# Ultimes 24 h de soil_moisture de tots els sensors
query = '''
from(bucket: "hort-osona")
  |> range(start: -24h)
  |> filter(fn: (r) => r._measurement == "miflora")
  |> filter(fn: (r) => r._field == "soil_moisture")
  |> aggregateWindow(every: 1h, fn: mean, createEmpty: false)
  |> group(columns: ["device"])
'''

print("Consulta: mitjana horaria de humitat del soll (ultimes 24h)")
print("=" * 70)
result = query_api.query(query)
for table in result:
    for record in table.records:
        device = record.values.get("device", "unknown")
        print(f"  {device}: {record.get_time()} = {record.get_value():.1f}%")

# Consulta mes complexa: comptar quantes lectures per device
query2 = '''
from(bucket: "hort-osona")
  |> range(start: -7d)
  |> filter(fn: (r) => r._measurement == "miflora")
  |> group(columns: ["device"])
  |> count()
'''

print("\nComptatge de lectures per device (ultims 7 dies):")
print("=" * 70)
result2 = query_api.query(query2)
for table in result2:
    for record in table.records:
        device = record.values.get("device", "unknown")
        print(f"  {device}: {record.get_value()} lectures")

client.close()
```

```bash
python3 query_data.py
```

## Pas 5: Crea una task de downsampling (15 min)

Volem que cada hora, les lectures raw s'agreguin a una mesura `_1h` amb la mitjana, i es guardin al bucket `hort-osona-downsampled`.

A la UI d'InfluxDB, ves a Tasks -> Create Task. Enganxa aquest Flux:

```flux
import "strings"

option task = {
   name: "downsample_1h",
   every: 1h,
   offset: 5m
}

measurements = ["miflora", "bme", "lora"]

from(bucket: "hort-osona")
  |> range(start: -1h, stop: now())
  |> filter(fn: (r) => contains(value: r._measurement, set: measurements))
  |> aggregateWindow(every: 1h, fn: mean, createEmpty: false)
  |> set(key: "_measurement", value: strings.concatStr(v: r._measurement, v: "_1h"))
  |> to(bucket: "hort-osona-downsampled", org: "bernatlab")
```

Guarda-la i activa-la. Aprofitar el `offset: 5m` per donar temps a que arribin les ultimes lectures.

Ara pots consultar el bucket downsampled:

```bash
docker exec hort-influxdb influx query \
   'from(bucket:"hort-osona-downsampled") |> range(start:-1h) |> limit(n:5)' \
   --org bernatlab
```

## Pas 6: Crea una alerta de gelada (10 min)

A la UI d'InfluxDB:

1. **Checks** -> Create Check.
2. Query:

   ```flux
   from(bucket: "hort-osona")
     |> range(start: -10m)
     |> filter(fn: (r) => r._measurement == "bme")
     |> filter(fn: (r) => r._field == "temp_c")
     |> mean()
   ```

3. **Conditions**: `value < 2.0` per critico.
4. **Notification Rule**: crea una que enviï a un webhook (e.g. Telegram o ntfy.sh). Pots obtenir una URL gratuita a https://ntfy.sh.

Prova enviant una temperatura baixa:

```bash
curl -XPOST "http://localhost:8086/api/v2/write?org=bernatlab&bucket=hort-osona" \
   -H "Authorization: Token adminsecret" \
   --data 'bme,device=bme-hivernacle temp_c=1.5,humidity=85'
```

Hauries de rebre la notificacio a ntfy.sh.

## Validacio

Has acabat si:

- [ ] Has iniciat InfluxDB amb Docker i has creat el token.
- [ ] Has generat 1000 punts fake i els veus a la UI.
- [ ] Has executat una consulta Flux amb Python i has vist resultats.
- [ ] Has creat la task de downsampling i funciona.
- [ ] Has configurat una alerta i has vist la notificacio.

## Per aprofundir

- Configura retencio automatica raw=7d, 1h=90d, 1d=2y.
- Exporta les dades a un fitxer Parquet per a machine learning.
- Compara Flux vs InfluxQL amb consultes equivalents.
- Activa autenticacio TLS a la API HTTP.
- Connecta Grafana per visualitzar les dades amb grafiques d'alta qualitat.
