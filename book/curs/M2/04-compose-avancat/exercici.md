# Exercici practic - Capitol 4: Compose avançat

> 40-60 min · Real al teu sistema

## Objectiu

Crear un stack multi-servei amb Docker Compose usant perfils, dependencies, secrets i extends. Practicarem una configuracio realista de tipus "blog" amb frontend, API, base de dades i eines de dev nomes per a desenvolupament.

## Requisits

- Docker i Docker Compose instal·lats
- 40-60 minuts
- Coneixement basic de YAML

## Pas 1: Estructura del projecte (5 min)

```bash
mkdir -p ~/compose-avancat
cd ~/compose-avancat
mkdir -p frontend backend db-data secrets
```

## Pas 2: Crea el docker-compose.yml base (10 min)

```yaml
# docker-compose.yml
version: "3.9"

services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"
    networks:
      - frontend
    depends_on:
      api:
        condition: service_started
    profiles: [prod, dev]  # actiu en tots dos

  api:
    build: ./backend
    environment:
      - DB_HOST=db
      - DB_PORT=5432
      - DB_USER=blog
      - DB_PASSWORD_FILE=/run/secrets/db_password
    networks:
      - frontend
      - backend
    depends_on:
      db:
        condition: service_healthy
    secrets:
      - db_password
    profiles: [prod, dev]

  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_USER=blog
      - POSTGRES_PASSWORD_FILE=/run/secrets/db_password
      - POSTGRES_DB=blogdb
    volumes:
      - db-data:/var/lib/postgresql/data
    networks:
      - backend
    secrets:
      - db_password
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U blog"]
      interval: 10s
      timeout: 3s
      retries: 5
    profiles: [prod, dev]

  phpmyadmin:
    image: phpmyadmin:latest
    ports:
      - "8081:80"
    environment:
      - PMA_HOST=db
    networks:
      - backend
    depends_on:
      - db
    profiles: [dev]  # nomes dev!

volumes:
  db-data:

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge

secrets:
  db_password:
    file: ./secrets/db_password.txt
```

## Pas 3: Crea el secret i el Dockerfile de l'API (5 min)

Crea un password aleatori:

```bash
echo "supersecret123" > secrets/db_password.txt
chmod 600 secrets/db_password.txt
```

Crea `backend/Dockerfile`:

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
USER 1000
EXPOSE 8000
CMD ["python", "app.py"]
```

Crea `backend/requirements.txt`:

```
flask==3.0.0
psycopg2-binary==2.9.9
```

Crea `backend/app.py`:

```python
import os
from flask import Flask, jsonify

app = Flask(__name__)

def read_secret(name):
    with open(f"/run/secrets/{name}") as f:
        return f.read().strip()

@app.route("/")
def home():
    return jsonify({"msg": "Hola des de l'API", "status": "ok"})

@app.route("/db")
def db_info():
    return jsonify({
        "host": os.environ.get("DB_HOST"),
        "user": os.environ.get("DB_USER"),
        "secret_loaded": bool(read_secret("db_password"))
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
```

## Pas 4: Arrenca nomes el perfil de dev (10 min)

```bash
# Mira quins serveis hi ha disponibles
docker compose --profile dev config --services

# Arrenca nomes els serveis amb perfil dev
docker compose --profile dev up -d

# Mira quins serveis estan actius
docker compose ps

# Comprova el frontend
curl http://localhost:8080

# Comprova l'API
docker compose exec api curl http://localhost:8000/db
# o accedeix des de l'amfitrio si has exposat l'api
docker compose exec api cat /run/secrets/db_password

# Comprova phpMyAdmin (nomes dev)
curl http://localhost:8081
```

## Pas 5: Prova el perfil prod (10 min)

```bash
# Atura tot
docker compose --profile dev down

# Arrenca nomes prod
docker compose --profile prod up -d

# Quins serveis hi ha?
docker compose ps
# Hauries de veure web, api, db PER NO phpmyadmin

# Comprova el frontend
curl http://localhost:8080

# Comprova que phpmyadmin NO esta exposat
curl http://localhost:8081
# Hauria de fallar
```

## Pas 6: Experimenta amb depends_on i healthchecks (10 min)

```bash
# Mira l'ordre d'arrencada
docker compose --profile prod up
# Fixa't que db primer, despres api (espera healthy), despres web

# Comprova els logs
docker compose logs db
docker compose logs api
docker compose logs -f
```

## Pas 7: Prova extends (10 min)

Crea un `docker-compose.base.yml`:

```yaml
# docker-compose.base.yml
x-common-env: &common-env
  LOG_LEVEL: info
  TZ: Europe/Madrid
```

Modifica `docker-compose.yml` per usar extends:

```yaml
services:
  api:
    build: ./backend
    environment:
      - LOG_LEVEL=debug  # override
      - TZ=Europe/Madrid
    networks:
      - backend
```

(En aquest cas hem optat per duplicar l'entorn, pero en arquitectures mes grans extends es molt util per a serveis compartits).

## Pas 8: Neteja final

```bash
docker compose --profile prod down -v
docker compose --profile dev down -v
ls
```

## Validacio

Has acabat si:

- [ ] Has creat un docker-compose.yml amb serveis, xarxes, volums i secrets.
- [ ] Has vist com els perfils permeten activar/desactivar serveis.
- [ ] Has provat el perfil dev amb phpMyAdmin i el perfil prod sense.
- [ ] Has comprovat que el secret es carrega correctament.
- [ ] Has vist l'ordre d'arrencada amb depends_on i healthcheck.
- [ ] Has netejat tots els recursos.

## Per aprofundir

- Investiga la clau `x-*` (YAML anchors) per evitar duplicar configuracio comuna.
- Prova a afegir un servei amb `scale: 3` per executar multiples instancies.
- Compara `docker compose` (v2, integrat) amb `docker-compose` (v1, antic).
- Llegeix sobre el "Compose Specification" (https://compose-spec.io/) per entendre totes les possibilitats.
