# Exercici practic — Capitol 5: PostgreSQL basic

> 40-50 min · Real al teu sistema

## Objectiu

Instal·lar PostgreSQL amb Docker, crear una base de dades per a l'hort, inserir dades, practicar consultes i fer un backup amb `pg_dump`.

## Requisits

- Tailscale actiu
- Connexio SSH a la RPi
- Docker funcionant
- 40-50 minuts

## Pas 1: Aixeca PostgreSQL en Docker (5 min)

```bash
mkdir -p /home/pi/bernatlab/postgres/data

docker run -d --name bernatlab-postgres \
  -e POSTGRES_USER=bernatlab \
  -e POSTGRES_PASSWORD=prova1234 \
  -e POSTGRES_DB=bernatlab \
  -v /home/pi/bernatlab/postgres/data:/var/lib/postgresql/data \
  postgres:16-alpine

sleep 10
docker ps | grep bernatlab-postgres
# Hauries de veure el contenidor bernatlab-postgres actiu
```

## Pas 2: Connecta't amb psql (5 min)

```bash
# Connectar-se via docker exec
docker exec -it bernatlab-postgres psql -U bernatlab -d bernatlab

# Dins de psql:
\conninfo
\l              # llistar BD
\du             # llistar usuaris
\q              # sortir
```

## Pas 3: Crea l'esquema de l'hort (10 min)

```bash
# Torna a entrar i crea les taules
docker exec -i bernatlab-postgres psql -U bernatlab -d bernatlab <<EOF
CREATE TABLE plantes (
  id SERIAL PRIMARY KEY,
  nom TEXT NOT NULL,
  varietat TEXT,
  plantat DATE NOT NULL,
  ubicacio TEXT
);

CREATE TABLE lectures (
  id BIGSERIAL PRIMARY KEY,
  planta_id INT REFERENCES plantes(id),
  sensor TEXT NOT NULL,
  valor REAL NOT NULL,
  ts TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_lectures_ts ON lectures(ts);
CREATE INDEX idx_lectures_sensor ON lectures(sensor, ts);

\dt
\d+ lectures
EOF
```

## Pas 4: Insereix dades de prova (10 min)

```bash
docker exec -i bernatlab-postgres psql -U bernatlab -d bernatlab <<EOF
INSERT INTO plantes (nom, varietat, plantat, ubicacio) VALUES
  ('Tomàquet', 'Pera', '2025-04-15', 'Bancal 1'),
  ('Enciam', 'Meravella', '2025-05-01', 'Bancal 2'),
  ('Carbassa', 'Cacahuet', '2025-05-10', 'Bancal 3');

-- Genera 1000 lectures aleatories
INSERT INTO lectures (planta_id, sensor, valor)
SELECT 
  (random() * 2 + 1)::int,
  s.sensor,
  (random() * 30 + 15)::real
FROM generate_series(1, 1000) g
CROSS JOIN (VALUES ('temperatura'), ('humitat')) AS s(sensor);

SELECT COUNT(*) FROM lectures;
EOF
# Hauries de veure 2000 (1000 per sensor)
```

## Pas 5: Consultes avançades (5 min)

```bash
docker exec -it bernatlab-postgres psql -U bernatlab -d bernatlab

-- Mitjana per planta i sensor
SELECT p.nom, l.sensor, AVG(l.valor)
FROM lectures l
JOIN plantes p ON l.planta_id = p.id
GROUP BY p.nom, l.sensor
ORDER BY p.nom, l.sensor;

-- Mitjana per hora
SELECT 
  date_trunc('hour', ts) AS hora,
  sensor,
  AVG(valor) AS mitjana
FROM lectures
GROUP BY hora, sensor
ORDER BY hora DESC
LIMIT 5;

-- Ultimes 10 lectures
SELECT * FROM lectures ORDER BY ts DESC LIMIT 10;

\q
```

## Pas 6: Backup amb pg_dump (5 min)

```bash
mkdir -p /home/pi/bernatlab/backups/postgres

# Dump consistent comprimit
docker exec bernatlab-postgres pg_dump -U bernatlab bernatlab | \
  gzip > /home/pi/bernatlab/backups/postgres/bernatlab-$(date +%Y%m%d).sql.gz

ls -lh /home/pi/bernatlab/backups/postgres/
# Hauries de veure el .sql.gz

# Comprova
zcat /home/pi/bernatlab/backups/postgres/bernatlab-*.sql.gz | head -20
```

## Pas 7: Restaurar (opcional, 5 min)

```bash
# Aixo es nomes per practicar. NO ho facis amb dades productives sense voler.

# Esborra les taules
docker exec -i bernatlab-postgres psql -U bernatlab -d bernatlab \
  -c "DROP TABLE IF EXISTS lectures, plantes;"

# Restaura
zcat /home/pi/bernatlab/backups/postgres/bernatlab-*.sql.gz | \
  docker exec -i bernatlab-postgres psql -U bernatlab -d bernatlab

# Comprova
docker exec bernatlab-postgres psql -U bernatlab -d bernatlab -c "SELECT COUNT(*) FROM lectures;"
# Hauries de veure 2000
```

## Validacio

Has acabat si:

- [ ] Has aixecat PostgreSQL amb Docker.
- [ ] T'has connectat amb `psql`.
- [ ] Has creat l'esquema de l'hort (plantes + lectures).
- [ ] Has inserit 2000 lectures amb `generate_series`.
- [ ] Has fet consultes amb JOIN i agregacions.
- [ ] Has fet un backup amb `pg_dump | gzip`.
- [ ] Has restaurat el backup en proves.

## Per aprofundir

- Practica transaccions amb `BEGIN; UPDATE plantes ...; ROLLBACK;`.
- Investiga com configurar `pg_hba.conf` per permetre connexions externes amb TLS.
- Prova de crear una vista per a una consulta frequent: `CREATE VIEW lectures_diaries AS SELECT ...`
- Compara el rendiment fent 100.000 insercions amb `COPY` vs `INSERT` individual.
- Investiga `EXPLAIN ANALYZE SELECT ...` per entendre el pla d'execucio.
