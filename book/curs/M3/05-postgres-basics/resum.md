# Resum — Capitol 5: PostgreSQL basic

## La idea clau

Quan les dades creixen massa per a SQLite (GB, milions de files, molts usuaris) o necessites consultes serioses amb JOINs i agregacions complexes, toca pujar a una base de dades **client-servidor**. Al BernatLab la meva eleccio es **PostgreSQL**: es la BD open source mes potent del mon, gratuita, estable, i amb una qualitat de codi envejable. Per a l'hort IoT, la faig servir per a inventari de plantes, historial de collites, dades meteorologiques agregades, i qualsevol cosa que tingui volums superiors a uns 100 MB.

## Que es PostgreSQL?

PostgreSQL (o "Postgres" pels amics) es una base de dades **relacional** client-servidor que existeix des de 1996. Caracteristiques principals:

- **Open source** (llcencia PostgreSQL, similar a BSD).
- **ACID** estricte per defecte.
- **SQL estandard** + extensions (JSON, GIS, full text search).
- **Concurrencia**: milers de connexions simultanies.
- **Volum**: gestiona sense problemes BD de centenars de GB.
- **Replicacio**: master-slave, streaming, logica.

## Quan usar PostgreSQL (i quan no)

PostgreSQL es la millor opcio quan:

- Les dades superen ~1 GB.
- Tens multiples aplicacions/usuaris accedint alhora.
- Necessites JOINs complexes o agregacions pesades.
- Cal compliment ACID estricte (transaccions financeres, inventari).
- Vols replicacio o alta disponibilitat.

NO es necessari quan:

- Tens menys de 100 MB de dades (**SQLite** es millor).
- Les dades son series temporals massives (**InfluxDB** es millor).
- Nomes un sol proces hi escriu.

## Instal·lacio al BernatLab

Al BernatLab corre en un contenidor Docker amb la imatge oficial `postgres:16-alpine`:

```yaml
services:
  postgres:
    image: postgres:16-alpine
    container_name: bernatlab-postgres
    restart: unless-stopped
    environment:
      POSTGRES_USER: bernatlab
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: bernatlab
    volumes:
      - /home/pi/bernatlab/postgres/data:/var/lib/postgresql/data
    ports:
      - "127.0.0.1:5432:5432"
```

## Comandes basiques

```bash
# Connectar-se (via docker exec)
docker exec -it bernatlab-postgres psql -U bernatlab -d bernatlab

# Dins de psql:
\l              # llistar BD
\dt             # llistar taules
\d+ sensors     # descriure una taula
\du             # llistar usuaris
\h SELECT       # ajuda sobre una ordre SQL
\q              # sortir

# Crear una BD nova
CREATE DATABASE hivernacle;
\c hivernacle

# Crear una taula
CREATE TABLE sensors (
  id SERIAL PRIMARY KEY,
  nom TEXT NOT NULL,
  valor REAL NOT NULL,
  ts TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

# Inserir
INSERT INTO sensors (nom, valor) VALUES
  ('temperatura', 22.5),
  ('humitat', 65.0);

# Consultar
SELECT * FROM sensors;
SELECT nom, AVG(valor) FROM sensors GROUP BY nom;
```

## Tipus de dades utils

- **INTEGER, BIGSERIAL**: enters.
- **TEXT, VARCHAR(n)**: cadenes.
- **REAL, DOUBLE PRECISION**: decimals.
- **BOOLEAN**: cert/fals.
- **TIMESTAMPTZ**: data + hora amb zona horaria (sempre usa aquest!).
- **JSONB**: JSON binari, indexable.
- **UUID**: identificadors unics universals.
- **INET, CIDR**: adreces IP.

## Backup consistent: pg_dump

Mai facis `tar` d'un directori de Postgres actiu. Usa sempre `pg_dump`:

```bash
# D'una sola BD
docker exec bernatlab-postgres pg_dump -U bernatlab bernatlab | \
  gzip > backup-$(date +%Y%m%d).sql.gz

# De TOTES les BD
docker exec bernatlab-postgres pg_dumpall -U postgres | \
  gzip > backup-all-$(date +%Y%m%d).sql.gz

# Restaurar
zcat backup-20250615.sql.gz | \
  docker exec -i bernatlab-postgres psql -U bernatlab -d bernatlab
```

## Diferencies claus amb SQLite

| Caracteristica | SQLite | PostgreSQL |
|---|---|---|
| Tipus | Embeguda (un .db) | Client-servidor |
| Volum recomanat | <1 GB | GB a TB |
| Concurrencia | 1 escriptura | Milers |
| SQL | Subconjunt | Estandard + extensions |
| Tipus propis | 5 basics | 40+ |
| Replicacio | No | Si |
| Autenticacio | Cap | Usuaris, rols, permisos |

## Connexions amb altres capítols

- **Cap 3** — Com fer backup consistent amb pg_dump.
- **Cap 4** — Quan SQLite es millor opcio.
- **Cap 6** — InfluxDB per a dades de sensors massives.
- **Cap 7** — Com accedir a Postgres des d'apps Node/Python.
