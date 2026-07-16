# Resum - Capitol 4: Compose avançat

## La idea clau

Docker Compose es la manera **declarativa** de definir aplicacions multi-contenidor. Amb un sol fitxer `docker-compose.yml` pots descriure serveis, xarxes, volums i secrets, i Docker els gestiona tots junts. Pero a mes dels basics, hi ha funcionalitats que et fan la vida molt mes facil: perfils, dependencies, extends i secrets.

## Recordatori rapid: que es Compose

Si ja ho saps (capitol 5 del M1), pots saltar. Si no:

```yaml
version: "3.9"
services:
  web:
    image: nginx
    ports:
      - "8080:80"
  db:
    image: postgres
    environment:
      - POSTGRES_PASSWORD=secret
```

Amb `docker compose up -d` tens tota l'app corrent. Amb `docker compose down` l'atures. Magic.

## Perfils: serveis opcionals

Els perfils permeten definir serveis que **nomes s'activen quan vols**. El cas mes clar: eines de desenvolupament.

```yaml
services:
  web:
    image: nginx
    profiles: [prod, dev]  # sempre actiu

  db:
    image: postgres
    profiles: [prod, dev]  # sempre actiu

  phpmyadmin:
    image: phpmyadmin
    profiles: [dev]  # nomes en dev!
```

Com usar-ho:

```bash
# Prod: nomes web i db
docker compose --profile prod up -d

# Dev: tot
docker compose --profile dev up -d

# Per defecte (sense --profile): nomes serveis sense perfil
docker compose up -d
```

Aixo es genial per tenir un sol fitxer compose que serveix per a dev i prod, sense duplicar res.

## Dependencies i ordre d'arrencada

Si tens serveis que depenen d'altres, vols que s'arrenguin en ordre correcte. `depends_on` faixo:

```yaml
services:
  api:
    image: myapi
    depends_on:
      - db  # nomes espera que db iniciï

  web:
    image: nginx
    depends_on:
      - api  # espera que api iniciï
```

Pero atencio: `depends_on` nomes espera que el contenidor **inicii**, no que estigui **llest** per rebre connexions. Per aixo s'afegeix `condition`:

```yaml
services:
  api:
    image: myapi
    depends_on:
      db:
        condition: service_healthy  # espera que db estigui "healthy"

  db:
    image: postgres
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 10s
      timeout: 3s
      retries: 5
```

Amb aixo, Docker no arrenca `api` fins que `db` passa el seu `healthcheck`. Es el que necessites per a una base de dades.

## Healthchecks

Defines una comanda que Docker executa periodicament. Si retorna exit code 0, el servei esta "healthy":

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost/health"]
  interval: 30s
  timeout: 5s
  retries: 3
  start_period: 10s  # temps inicial abans de començar a comprovar
```

Opcions per al `test`:
- `["CMD", "comanda", "args"]` (forma llarga)
- `["CMD-SHELL", "comanda"]` (executa amb shell)
- `NONE` (desactivar)

## Extends: heretar configuracio

Si tens molts serveis amb configuracio comuna, `extends` et permet heretar:

```yaml
# docker-compose.base.yml
services:
  app-base:
    environment:
      - LOG_LEVEL=info
      - TZ=Europe/Madrid
    user: "1000:1000"
    restart: unless-stopped

# docker-compose.yml
services:
  api:
    extends:
      file: docker-compose.base.yml
      service: app-base
    image: myapi
    command: ["python", "main.py"]

  worker:
    extends:
      file: docker-compose.base.yml
      service: app-base
    image: myapi
    command: ["python", "worker.py"]
```

Aixi, `api` i `worker` hereten l'entorn i el user de `app-base`. Si vols canviar LOG_LEVEL a tots dos, canvies nomes al base.

## Secrets: credentials segurs

Mai posis passwords al fitxer compose en text pla. Usa secrets:

```yaml
services:
  db:
    image: postgres
    environment:
      - POSTGRES_PASSWORD_FILE=/run/secrets/db_password
    secrets:
      - db_password

secrets:
  db_password:
    file: ./secrets/db_password.txt
```

Docker munta el fitxer a `/run/secrets/db_password` dins el contenidor. L'aplicacio llegeix el fitxer en lloc d'usar la variable d'entorn directa. Es mes segur perque el secret no apareix a `docker inspect`.

## Variables d'entorn i .env

Pots definir variables en un fitxer `.env`:

```bash
# .env
DB_PASSWORD=supersecret
API_PORT=8080
```

I usar-les al compose:

```yaml
services:
  db:
    environment:
      - POSTGRES_PASSWORD=${DB_PASSWORD}
```

Important: mai facis commit del `.env` amb passwords reals. Usa `.env.example` com a plantilla.

## Comandes utils

```bash
# Validar la sintaxi sense executar
docker compose config

# Veure els serveis que s'arrengin
docker compose ps

# Logs
docker compose logs -f              # tots
docker compose logs -f api          # nomes un
docker compose logs --tail 100 api  # ultim 100 linies

# Executar una comanda dins un servei
docker compose exec api sh

# Reiniciar un servei
docker compose restart api

# Escalar (multiples instancies)
docker compose up -d --scale api=3
```

## Connexions amb altres capitols

- **M1 Cap 5** - Els basics de Compose ja els coneixes.
- **M2 Cap 1** - Els multi-stage builds serveixen per tenir imatges mes petites per a Compose.
- **M2 Cap 2** - Els volums es defineixen al compose declarativament.
- **M2 Cap 3** - Les xarxes custom es poden definir al compose.
- **M2 Cap 5** - Compose pot pujar imatges a registres privats.
- **M2 Cap 7** - Les dependencies son la base de les actualitzacions rolling.
