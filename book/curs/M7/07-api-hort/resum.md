# Resum - Capitol 7: API REST per a l'Hort Osona

## La idea clau

L'**API REST** es el pont entre les dades guardades (InfluxDB, PostgreSQL) i el mon exterior (PWA, scripts, altres aplicacions). Es una **interficie HTTP** que respon peticions GET/POST amb dades en **JSON**. A l'Hort Osona la implementem amb **Flask** (Python) per la seva simplicitat. Qualsevol cosa que sàpiga fer una peticio HTTP pot consumir l'API: un navegador, una app, un altre script, una Raspberry, una pàgina estàtica.

## Que es una API REST

REST (Representational State Transfer) es un estil d'arquitectura per a serveis web. Les regles son simples:

- **Recursos identificats per URLs**: `/api/v1/sensors/1B32` = el sensor amb MAC 1B32.
- **Verbs HTTP estandard**: GET (llegir), POST (crear), PUT (actualitzar), DELETE (esborrar).
- **Stateless**: cada peticio conte tota la informacio necessaria. El servidor no recorda res entre peticions.
- **Respostes en JSON** (o XML, pero JSON es l'estandard modern).

Exemple de peticio a l'API de l'Hort Osona:

```bash
curl http://localhost:5000/api/v1/sensors/miflora-1B32/latest
```

Resposta:

```json
{
  "device": "miflora-1B32",
  "ts": "2026-04-12T10:00:00Z",
  "soil_moisture": 42.0,
  "soil_temp_c": 18.5,
  "ec_us_cm": 820,
  "lux": 18000,
  "battery": 87
}
```

## Per que Flask i no altres

Hi ha molts frameworks per fer APIs en Python:

- **Flask**: minimalista, facil d'apendre, ideal per a APIs petites. El que usem a l'Hort Osona.
- **FastAPI**: modern, amb type hints, validacio automatica, OpenAPI. Mes potent pero mes complex.
- **Django REST Framework**: complet, amb admin, ORM. Overkill per a una API petita.
- **Bottle**: encara mes minimalista. Bo per a projectes molt petits.

A l'Hort Osona usem **Flask** perque:
- API de 5-10 endpoints, no cal mes.
- L'equip ja el coneix.
- Ecosistema madur (Flask-RESTful, Flask-CORS, etc.).

## Estructura de l'API

A l'Hort Osona l'API te uns 15 endpoints organitzats en 4 grups:

```
/api/v1/
  /sensors
    GET    /sensors/                   -> llista tots els sensors
    GET    /sensors/<id>              -> info d'un sensor
    GET    /sensors/<id>/latest       -> ultima lectura
    GET    /sensors/<id>/history?h=24 -> historic (ultimes 24h)
  /sectors
    GET    /sectors                    -> sectors de l'hort
    GET    /sectors/<id>/summary       -> resum d'un sector
  /calendar
    GET    /calendar/<year>/<month>    -> esdeveniments del mes
    POST   /calendar/events            -> crear un esdeveniment
  /alerts
    GET    /alerts/active              -> alertes actives
    POST   /alerts/acknowledge/<id>    -> reconeixer una alerta
```

Cada endpoint es una **funcio Python** que rep la peticio i torna JSON.

## Exemple: GET /sensors/miflora-1B32/latest

```python
from flask import Flask, jsonify
from influxdb_client import InfluxDBClient
from datetime import datetime, timezone

app = Flask(__name__)
influx = InfluxDBClient(url="http://influxdb:8086",
                       token="...", org="bernatlab")
query_api = influx.query_api()

@app.route("/api/v1/sensors/<device_id>/latest", methods=["GET"])
def get_sensor_latest(device_id):
    query = f'''
    from(bucket: "hort-osona")
      |> range(start: -1h)
      |> filter(fn: (r) => r._measurement == "miflora")
      |> filter(fn: (r) => r.device == "{device_id}")
      |> last()
    '''
    result = query_api.query(query)

    if not result or not result[0].records:
        return jsonify({"error": "Sensor not found"}), 404

    # Construeix resposta
    data = {"device": device_id, "ts": None, "fields": {}}
    for record in result[0].records:
        data["ts"] = record.get_time().isoformat()
        data["fields"][record.get_field()] = record.get_value()

    return jsonify(data), 200
```

Aixo es un endpoint senzill. La gràcia es que es pot testejar amb `curl` directament.

## CORS: per que la PWA pot trucar l'API

Si la PWA esta allotjada a `https://hort-osona.github.io` i l'API a `http://la-meva-rpi.local:5000`, el navegador **bloqueja** les peticions per seguretat (CORS - Cross-Origin Resource Sharing).

Solucio: afegir els headers CORS a Flask amb `flask-cors`:

```python
from flask_cors import CORS
CORS(app, origins=["https://hort-osona.github.io", "http://localhost:*"])
```

A l'Hort Osona permetem:
- `http://localhost:*` (per desenvolupament)
- `https://*.github.io` (per GitHub Pages)

En produccio, val la pena ser mes restrictiu.

## Autenticacio: API keys i JWT

L'API de l'Hort Osona es **privada** (no volem que Google ens indexi les dades). Tenim dos nivells:

1. **API key** (simple): el client passa `X-API-Key: secret` als headers. La clau es valida contra una llista a `.env`.

2. **JWT** (mes potent): el client fa login amb usuari/password, rep un token, l'envia a cada peticio. Mes complexe pero permet usuaris amb rols.

Per a l'Hort Osona fem servir **API key** per la PWA i a scripts, i **JWT** nomes per l'admin web (entrar al panell de configuracio).

Exemple amb API key:

```python
from functools import wraps
from flask import request, jsonify
import os

API_KEY = os.environ.get("HORT_API_KEY", "secret")

def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        key = request.headers.get("X-API-Key")
        if key != API_KEY:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated

@app.route("/api/v1/sensors/<device_id>/latest")
@require_api_key
def get_sensor_latest(device_id):
    ...
```

## Documentacio automatica amb OpenAPI

FastAPI genera OpenAPI automaticament. Amb Flask podem fer-ho amb `flask-smorest` o `apispec`. Pero el mes simple es tenir un fitxer `docs/openapi.yaml` a ma amb tots els endpoints.

Exemple:

```yaml
openapi: 3.0.0
info:
  title: Hort Osona API
  version: 1.0.0
paths:
  /api/v1/sensors/{id}/latest:
    get:
      summary: Ultima lectura d'un sensor
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      responses:
        200:
          description: Lectura exitosa
          content:
            application/json:
              schema:
                type: object
                properties:
                  device: {type: string}
                  ts: {type: string, format: date-time}
                  fields: {type: object}
```

## Exemple complet: app Flask amb /sensors

Crea `~/hort-osona/api/app.py`:

```python
import os
import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
from influxdb_client import InfluxDBClient
from functools import wraps
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app, origins=os.environ.get("CORS_ORIGINS", "*").split(","))

# Clients
influx = InfluxDBClient(
    url=os.environ["INFLUXDB_URL"],
    token=os.environ["INFLUXDB_TOKEN"],
    org=os.environ["INFLUXDB_ORG"]
)
query_api = influx.query_api()

API_KEY = os.environ.get("HORT_API_KEY", "secret")

def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        key = request.headers.get("X-API-Key")
        if not key or key != API_KEY:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated

def query_influx(flux_query):
    """Helper per executar queries."""
    try:
        result = query_api.query(flux_query)
        return result
    except Exception as e:
        app.logger.error(f"InfluxDB error: {e}")
        return []

@app.route("/api/v1/sensors/<device_id>/latest")
@require_api_key
def get_latest(device_id):
    q = f'''
    from(bucket: "hort-osona")
      |> range(start: -1h)
      |> filter(fn: (r) => r._measurement =~ /^.*$/)
      |> filter(fn: (r) => r.device == "{device_id}")
      |> last()
    '''
    result = query_influx(q)
    if not result or not result[0].records:
        return jsonify({"error": "No data"}), 404

    data = {"device": device_id, "ts": None, "fields": {}}
    for record in result[0].records:
        data["ts"] = record.get_time().isoformat()
        data["fields"][record.get_field()] = record.get_value()
    return jsonify(data), 200

@app.route("/api/v1/sensors/<device_id>/history")
@require_api_key
def get_history(device_id):
    hours = int(request.args.get("h", 24))
    field = request.args.get("field", "soil_moisture")
    q = f'''
    from(bucket: "hort-osona")
      |> range(start: -{hours}h)
      |> filter(fn: (r) => r._measurement =~ /^.*$/)
      |> filter(fn: (r) => r.device == "{device_id}")
      |> filter(fn: (r) => r._field == "{field}")
      |> aggregateWindow(every: 15m, fn: mean, createEmpty: false)
    '''
    result = query_influx(q)
    points = []
    for table in result:
        for record in table.records:
            points.append({
                "ts": record.get_time().isoformat(),
                "value": record.get_value()
            })
    return jsonify({"device": device_id, "field": field,
                    "hours": hours, "points": points}), 200

@app.route("/api/v1/sectors")
@require_api_key
def get_sectors():
    sectors = [
        {"id": "toma-cherry", "cultiu": "Tomàquet cherry",
         "hivernacle": True, "reg": "automatic"},
        {"id": "enciam-fulla", "cultiu": "Enciam fulla de roure",
         "hivernacle": False, "reg": "manual"},
        {"id": "pebrot-italia", "cultiu": "Pebrot italia",
         "hivernacle": False, "reg": "automatic"},
        {"id": "carxofa", "cultiu": "Carxofa",
         "hivernacle": False, "reg": "gota"},
    ]
    return jsonify(sectors), 200

@app.route("/api/v1/health")
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
```

Aixeca'l:

```bash
cd ~/hort-osona/api
HORT_API_KEY=miclau python3 app.py
```

## Deployment a Docker

Per a l'Hort Osona, l'API es un contenidor mes:

```yaml
# docker-compose.yml
services:
  api:
    build: ./api
    ports:
      - "5000:5000"
    environment:
      - INFLUXDB_URL=http://influxdb:8086
      - INFLUXDB_TOKEN=adminsecret
      - INFLUXDB_ORG=bernatlab
      - HORT_API_KEY=miclau
      - CORS_ORIGINS=https://hort-osona.github.io,http://localhost:*
    depends_on:
      - influxdb
```

Dockerfile:

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:app"]
```

## Proves amb curl

```bash
# Health check (no requereix API key)
curl http://localhost:5000/api/v1/health

# Sense clau -> 401
curl http://localhost:5000/api/v1/sensors/miflora-1B32/latest

# Amb clau -> 200
curl -H "X-API-Key: miclau" \
   http://localhost:5000/api/v1/sensors/miflora-1B32/latest

# Historic 48h
curl -H "X-API-Key: miclau" \
   "http://localhost:5000/api/v1/sensors/miflora-1B32/history?h=48&field=soil_moisture"
```

## Connexions amb altres capitols

- **M7 Cap 4** - L'API es la capa 6 del pipeline.
- **M7 Cap 6** - Llegeix d'InfluxDB per construir respostes.
- **M7 Cap 8** - La PWA consumeix aquesta API.
- **M7 Cap 9** - Els endpoints de calendar serveixen per al frontend.
