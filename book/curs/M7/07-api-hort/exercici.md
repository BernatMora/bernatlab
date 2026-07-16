# Exercici practic - Capitol 7: API REST per a l'Hort Osona

> 40-60 min · Real a la RPi amb Python

## Objectiu

Construir una API REST amb Flask que llegeix d'InfluxDB i exposa 4 endpoints: `/sensors`, `/sensors/<id>/latest`, `/sensors/<id>/history`, i `/health`. Acabaras amb una API documentada i provada.

## Requisits

- RPi amb Python 3.10+
- InfluxDB ja funcionant (de l'exercici del cap 6)
- 40-60 min

## Pas 1: Prepara el projecte (5 min)

```bash
mkdir -p ~/hort-osona/api
cd ~/hort-osona/api
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install flask flask-cors influxdb-client gunicorn python-dotenv
```

Crea `.env`:

```bash
INFLUXDB_URL=http://localhost:8086
INFLUXDB_TOKEN=adminsecret
INFLUXDB_ORG=bernatlab
INFLUXDB_BUCKET=hort-osona
HORT_API_KEY=hort-osona-test-key-2026
CORS_ORIGINS=http://localhost:*,http://127.0.0.1:*
```

## Pas 2: L'API basica (15 min)

Crea `app.py`:

```python
"""API REST de l'Hort Osona."""
import os
import logging
from datetime import datetime, timezone
from functools import wraps
from flask import Flask, jsonify, request
from flask_cors import CORS
from influxdb_client import InfluxDBClient
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s')
log = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, origins=os.environ.get("CORS_ORIGINS", "*").split(","))

# InfluxDB
influx = InfluxDBClient(
    url=os.environ["INFLUXDB_URL"],
    token=os.environ["INFLUXDB_TOKEN"],
    org=os.environ["INFLUXDB_ORG"]
)
query_api = influx.query_api()
INFLUXDB_BUCKET = os.environ["INFLUXDB_BUCKET"]

API_KEY = os.environ.get("HORT_API_KEY", "secret")

# Definicio de sectors
SECTORS = [
    {"id": "toma-cherry", "cultiu": "Tomàquet cherry",
     "hivernacle": True, "reg": "automatic", "superficie_m2": 12},
    {"id": "enciam-fulla", "cultiu": "Enciam fulla de roure",
     "hivernacle": False, "reg": "manual", "superficie_m2": 8},
    {"id": "pebrot-italia", "cultiu": "Pebrot italia",
     "hivernacle": False, "reg": "automatic", "superficie_m2": 10},
    {"id": "carxofa", "cultiu": "Carxofa",
     "hivernacle": False, "reg": "gota", "superficie_m2": 15},
]


def require_api_key(f):
    """Decorator per requerir API key."""
    @wraps(f)
    def decorated(*args, **kwargs):
        key = request.headers.get("X-API-Key")
        if not key or key != API_KEY:
            log.warning(f"Unauthorized: {request.remote_addr}")
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated


def run_query(flux):
    """Helper per executar queries a InfluxDB."""
    try:
        return query_api.query(flux)
    except Exception as e:
        log.error(f"InfluxDB error: {e}")
        return []


# Endpoints
@app.route("/api/v1/health")
def health():
    """Health check (no auth)."""
    return jsonify({
        "status": "ok",
        "ts": datetime.now(timezone.utc).isoformat()
    }), 200


@app.route("/api/v1/sectors")
@require_api_key
def get_sectors():
    """Llista tots els sectors de l'hort."""
    return jsonify(SECTORS), 200


@app.route("/api/v1/sectors/<sector_id>")
@require_api_key
def get_sector(sector_id):
    """Detalls d'un sector concret."""
    for s in SECTORS:
        if s["id"] == sector_id:
            return jsonify(s), 200
    return jsonify({"error": "Sector not found"}), 404


@app.route("/api/v1/sensors/<device_id>/latest")
@require_api_key
def get_sensor_latest(device_id):
    """Ultima lectura d'un sensor."""
    flux = f'''
    from(bucket: "{INFLUXDB_BUCKET}")
      |> range(start: -1h)
      |> filter(fn: (r) => r.device == "{device_id}")
      |> last()
    '''
    result = run_query(flux)
    if not result or not result[0].records:
        return jsonify({"error": "No data"}), 404

    data = {"device": device_id, "ts": None, "fields": {}}
    for record in result[0].records:
        data["ts"] = record.get_time().isoformat()
        data["fields"][record.get_field()] = record.get_value()
    return jsonify(data), 200


@app.route("/api/v1/sensors/<device_id>/history")
@require_api_key
def get_sensor_history(device_id):
    """Historic d'un sensor."""
    try:
        hours = int(request.args.get("h", 24))
    except ValueError:
        return jsonify({"error": "Invalid h"}), 400

    field = request.args.get("field", "soil_moisture")
    window = request.args.get("window", "15m")

    flux = f'''
    from(bucket: "{INFLUXDB_BUCKET}")
      |> range(start: -{hours}h)
      |> filter(fn: (r) => r.device == "{device_id}")
      |> filter(fn: (r) => r._field == "{field}")
      |> aggregateWindow(every: {window}, fn: mean, createEmpty: false)
    '''
    result = run_query(flux)
    points = [
        {"ts": r.get_time().isoformat(), "value": r.get_value()}
        for table in result for r in table.records
    ]
    return jsonify({
        "device": device_id, "field": field,
        "hours": hours, "window": window,
        "points": points
    }), 200


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
```

## Pas 3: Prova l'API (5 min)

```bash
source .venv/bin/activate
python3 app.py
```

En una altra terminal:

```bash
# Health check
curl http://localhost:5000/api/v1/health
# {"status":"ok","ts":"2026-04-12T10:00:00.000Z"}

# Sense API key -> 401
curl -i http://localhost:5000/api/v1/sectors
# HTTP/1.1 401 UNAUTHORIZED

# Amb API key
curl -H "X-API-Key: hort-osona-test-key-2026" \
   http://localhost:5000/api/v1/sectors
# [{"id":"toma-cherry","cultiu":"Tomàquet cherry",...}]

# Ultima lectura
curl -H "X-API-Key: hort-osona-test-key-2026" \
   http://localhost:5000/api/v1/sensors/miflora-1B32/latest

# Historic 7 dies
curl -H "X-API-Key: hort-osona-test-key-2026" \
   "http://localhost:5000/api/v1/sensors/miflora-1B32/history?h=168&field=soil_moisture&window=1h" \
   | python3 -m json.tool | head -30
```

## Pas 4: Dockerfile i docker-compose (10 min)

Crea `Dockerfile`:

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:app"]
```

Crea `requirements.txt`:

```
flask==3.0.0
flask-cors==4.0.0
influxdb-client==1.39.0
gunicorn==21.2.0
python-dotenv==1.0.0
```

Afegeix al `docker-compose.yml` del projecte (a `/home/pi/hort-osona/`):

```yaml
  api:
    build: ./api
    container_name: hort-api
    ports:
      - "5000:5000"
    env_file: ./api/.env
    depends_on:
      - influxdb
    restart: unless-stopped
```

Aixeca'l:

```bash
cd ~/hort-osona
docker compose up -d --build api
docker compose logs -f api
```

## Pas 5: Documentacio OpenAPI (10 min)

Crea `openapi.yaml`:

```yaml
openapi: 3.0.0
info:
  title: Hort Osona API
  version: 1.0.0
  description: API per accedir a les dades de sensors i sectors
servers:
  - url: http://localhost:5000
    description: Desenvolupament local
components:
  securitySchemes:
    ApiKey:
      type: apiKey
      in: header
      name: X-API-Key
security:
  - ApiKey: []
paths:
  /api/v1/health:
    get:
      summary: Health check
      security: []
      responses:
        200:
          description: Servei operatiu
  /api/v1/sectors:
    get:
      summary: Llista sectors
      responses:
        200:
          description: Array de sectors
  /api/v1/sensors/{device_id}/latest:
    get:
      summary: Ultima lectura
      parameters:
        - name: device_id
          in: path
          required: true
          schema: {type: string}
      responses:
        200: {description: Lectura exitosa}
        404: {description: Sensor sense dades}
  /api/v1/sensors/{device_id}/history:
    get:
      summary: Historic d'un sensor
      parameters:
        - name: device_id
          in: path
          required: true
          schema: {type: string}
        - name: h
          in: query
          schema: {type: integer, default: 24}
        - name: field
          in: query
          schema: {type: string, default: soil_moisture}
        - name: window
          in: query
          schema: {type: string, default: 15m}
      responses:
        200: {description: Llista de punts}
```

Pots visualitzar-lo a https://editor.swagger.io copiant-hi el contingut.

## Pas 6: Tests amb pytest (10 min)

Crea `test_app.py`:

```python
import os
import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c

def test_health_no_auth(client):
    r = client.get("/api/v1/health")
    assert r.status_code == 200
    assert r.json["status"] == "ok"

def test_sectors_requires_auth(client):
    r = client.get("/api/v1/sectors")
    assert r.status_code == 401

def test_sectors_with_auth(client):
    r = client.get("/api/v1/sectors",
                   headers={"X-API-Key": os.environ["HORT_API_KEY"]})
    assert r.status_code == 200
    assert isinstance(r.json, list)
    assert len(r.json) > 0

def test_sector_not_found(client):
    r = client.get("/api/v1/sectors/no-existeix",
                   headers={"X-API-Key": os.environ["HORT_API_KEY"]})
    assert r.status_code == 404
```

```bash
source .venv/bin/activate
HORT_API_KEY=hort-osona-test-key-2026 python3 -m pytest test_app.py -v
```

## Validacio

Has acabat si:

- [ ] Has aixecat l'API Flask amb 4 endpoints.
- [ ] Tots els endpoints responen correctament amb `curl`.
- [ ] L'autenticacio amb API key funciona (401 sense, 200 amb).
- [ ] Has creat un Dockerfile i integrat a docker-compose.
- [ ] Has escrit l'OpenAPI i els tests amb pytest.

## Per aprofundir

- Afegeix un endpoint POST per crear esdeveniments al calendari (amb PostgreSQL).
- Implementa rate limiting amb `flask-limiter`.
- Activa HTTPS amb un proxy invers (Caddy o nginx).
- Afegeix WebSockets per actualitzar la UI en temps real.
- Genera l'OpenAPI automaticament amb `flask-smorest` o `apispec`.
