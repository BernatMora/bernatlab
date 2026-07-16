# Exercici practic — Capitol 6: InfluxDB per a dades de sensors

> 40-50 min · Real al teu sistema

## Objectiu

Instal·lar InfluxDB 2 amb Docker, inserir lectures de sensors amb HTTP API, practicar consultes en Flux i fer un backup.

## Requisits

- Tailscale actiu
- Connexio SSH a la RPi
- Docker funcionant
- 40-50 minuts

## Pas 1: Aixeca InfluxDB 2 (10 min)

```bash
mkdir -p /home/pi/bernatlab/influxdb/data
mkdir -p /home/pi/bernatlab/influxdb/config

docker run -d --name bernatlab-influxdb \
  -p 127.0.0.1:8086:8086 \
  -v /home/pi/bernatlab/influxdb/data:/var/lib/influxdb2 \
  -v /home/pi/bernatlab/influxdb/config:/etc/influxdb2 \
  -e DOCKER_INFLUXDB_INIT_MODE=setup \
  -e DOCKER_INFLUXDB_INIT_USERNAME=bernatlab \
  -e DOCKER_INFLUXDB_INIT_PASSWORD=prova1234 \
  -e DOCKER_INFLUXDB_INIT_ORG=bernatlab \
  -e DOCKER_INFLUXDB_INIT_BUCKET=hort \
  -e DOCKER_INFLUXDB_INIT_RETENTION=30d \
  influxdb:2.7-alpine

sleep 15
docker ps | grep bernatlab-influxdb
```

## Pas 2: Accedeix a la UI web (5 min)

Obre al navegador: `http://localhost:8086` (via Tailscale o tunel SSH). Login: `bernatlab` / `prova1234`. 

A la UI:
1. Ves a **Load Data > API Tokens**
2. Crea un token nou (nom: "lectures-script")
3. **Guarda'l** (es la unica vegada que el veuras)

## Pas 3: Escriu dades amb HTTP API (5 min)

```bash
TOKEN="el_teu_token_aqui"

# Escriu una lectura
curl -XPOST "http://localhost:8086/api/v2/write?org=bernatlab&bucket=hort" \
  --header "Authorization: Token $TOKEN" \
  --data-raw "temperatura,sensor=t1,ubicacio=hivernacle value=22.5"

curl -XPOST "http://localhost:8086/api/v2/write?org=bernatlab&bucket=hort" \
  --header "Authorization: Token $TOKEN" \
  --data-raw "temperatura,sensor=t1,ubicacio=hivernacle value=22.8"

curl -XPOST "http://localhost:8086/api/v2/write?org=bernatlab&bucket=hort" \
  --header "Authorization: Token $TOKEN" \
  --data-raw "humitat,sensor=t1,ubicacio=hivernacle value=65.0"
```

## Pas 4: Escriu moltes dades amb Python (10 min)

```bash
cat > /home/pi/bernatlab/proves/insertar-influx.py <<'PY'
import urllib.request
import random
import time

TOKEN = "posa_aqui_el_teu_token"
URL = f"http://localhost:8086/api/v2/write?org=bernatlab&bucket=hort"
headers = {
    "Authorization": f"Token {TOKEN}",
    "Content-Type": "text/plain"
}

# Genera 1000 lectures aleatories
for i in range(1000):
    temp = 20 + random.random() * 10
    hum = 50 + random.random() * 30
    data = f"temperatura,sensor=t1 value={temp}\nhumitat,sensor=t1 value={hum}"
    req = urllib.request.Request(URL, data=data.encode(), headers=headers)
    urllib.request.urlopen(req)
    if i % 100 == 0:
        print(f"Escrites {i} lectures...")
    time.sleep(0.01)

print("Fet! 1000 lectures escrites.")
PY

# Substitueix el TOKEN dins el fitxer
nano /home/pi/bernatlab/proves/insertar-influx.py

python3 /home/pi/bernatlab/proves/insertar-influx.py
```

## Pas 5: Consulta amb Flux (10 min)

Des de la UI web, ves a **Data Explorer** i prova aquestes consultes:

```flux
// Ultimes 10 lectures
from(bucket: "hort")
  |> range(start: -1h)
  |> limit(n: 10)

// Mitjana per hora els darrers 7 dies
from(bucket: "hort")
  |> range(start: -7d)
  |> filter(fn: (r) => r._measurement == "temperatura")
  |> aggregateWindow(every: 1h, fn: mean, createEmpty: false)

// Maxim per dia
from(bucket: "hort")
  |> range(start: -30d)
  |> filter(fn: (r) => r._measurement == "temperatura")
  |> aggregateWindow(every: 1d, fn: max, createEmpty: false)
```

## Pas 6: Backup (5 min)

```bash
# Crea un bucket admin a la UI (Settings > Buckets > Add: hort_backup amb retencio 90d)

# Fes el backup
docker exec bernatlab-influxdb influx backup /tmp/backup-hort

# Copia'l fora del contenidor
docker cp bernatlab-influxdb:/tmp/backup-hort \
  /home/pi/bernatlab/backups/influx-$(date +%Y%m%d)

ls -lh /home/pi/bernatlab/backups/
```

## Pas 7: Neteja (opcional)

```bash
docker stop bernatlab-influxdb
docker rm bernatlab-influxdb
```

## Validacio

Has acabat si:

- [ ] Has aixecat InfluxDB 2 amb Docker.
- [ ] Has accedit a la UI web i has creat un token.
- [ ] Has escrit lectures amb HTTP API i amb Python.
- [ ] Has fet consultes en Flux (range, filter, aggregateWindow).
- [ ] Has vist agregacions per hora/dia.
- [ ] Has fet un backup amb `influx backup`.

## Per aprofundir

- Configura una **consulta continua** que agregui per hora automaticament.
- Investiga com usar **Telegraf** per a recollir dades automaticament.
- Compara el rendiment agregant 100.000 lectures a InfluxDB vs PostgreSQL.
- Practica el **downsampling** amb una tasca scheduled.
- Investiga com connectar InfluxDB a **Grafana** (cap 10).
