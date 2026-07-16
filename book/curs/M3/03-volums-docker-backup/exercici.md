# Exercici practic — Capitol 3: Backup de volums Docker

> 30-40 min · Real al teu sistema

## Objectiu

Practicar el backup i la restauracio d'un volum Docker real. Farem servir un contenidor de **PostgreSQL** com a exemple perque ensenya tant la copia de fitxers (volum) com el dump logic (consistent).

## Requisits

- Tailscale actiu
- Connexio SSH a la RPi
- Docker funcionant
- 30-40 minuts

## Pas 1: Crea un contenidor de prova (5 min)

```bash
# Crea un volum i un contenidor postgres de prova
docker volume create pg-prova

docker run -d --name pg-prova \
  -e POSTGRES_PASSWORD=prova123 \
  -e POSTGRES_DB=hivernacle \
  -v pg-prova:/var/lib/postgresql/data \
  postgres:16-alpine

# Espera 10 segons que arrenqui
sleep 10

# Comprova que esta funcionant
docker ps | grep pg-prova
```

## Pas 2: Omple'l amb dades (5 min)

```bash
# Crea una taula i insereix dades
docker exec -it pg-prova psql -U postgres -d hivernacle -c "
  CREATE TABLE sensors (
    id SERIAL PRIMARY KEY,
    nom TEXT,
    valor REAL,
    ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  );
  INSERT INTO sensors (nom, valor) VALUES
    ('temperatura', 22.5),
    ('humitat', 65.0),
    ('llum', 850.0);
"

# Comprova
docker exec -it pg-prova psql -U postgres -d hivernacle -c "SELECT * FROM sensors;"
# Hauries de veure 3 files
```

## Pas 3: Fes un dump logic (10 min)

```bash
# Crea el directori de backups
mkdir -p /home/pi/bernatlab/backups/prova

# Dump consistent
docker exec pg-prova pg_dump -U postgres hivernacle | \
  gzip > /home/pi/bernatlab/backups/prova/hivernacle-$(date +%Y%m%d).sql.gz

# Comprova
ls -lh /home/pi/bernatlab/backups/prova/
# Hauries de veure hivernacle-YYYYMMDD.sql.gz

# Mostra les primeres linies
zcat /home/pi/bernatlab/backups/prova/hivernacle-*.sql.gz | head -30
```

## Pas 4: Fes una copia del volum amb tar (5 min)

```bash
# Aquesta NO es la manera correcta, pero serveix per veure com es fa
docker stop pg-prova

# Crea un tar del volum
sudo tar -czf /home/pi/bernatlab/backups/prova/volum-pg-$(date +%Y%m%d).tar.gz \
  /var/lib/docker/volumes/pg-prova/_data/

ls -lh /home/pi/bernatlab/backups/prova/

# Torna a aixecar
docker start pg-prova
```

## Pas 5: Simula un desastre (5 min)

```bash
# Esborra el contenidor i el volum (DESASTRE!)
docker rm -f pg-prova
docker volume rm pg-prova

# Comprova que tot ha desaparegut
docker ps -a | grep pg-prova
docker volume ls | grep pg-prova
# No hauries de veure res

# Les dades de sensors ja no existeixen
```

## Pas 6: Restaura des del dump (10 min)

```bash
# Crea un volum nou i un contenidor
docker volume create pg-prova-restaurat

docker run -d --name pg-restaurat \
  -e POSTGRES_PASSWORD=prova123 \
  -e POSTGRES_DB=hivernacle \
  -v pg-prova-restaurat:/var/lib/postgresql/data \
  postgres:16-alpine

sleep 10

# Restaura el dump
zcat /home/pi/bernatlab/backups/prova/hivernacle-*.sql.gz | \
  docker exec -i pg-restaurat psql -U postgres -d hivernacle

# Comprova
docker exec -it pg-restaurat psql -U postgres -d hivernacle -c "SELECT * FROM sensors;"
# Hauries de tornar a veure les 3 files originals!
```

## Pas 7: Neteja

```bash
docker stop pg-restaurat
docker rm pg-restaurat
docker volume rm pg-prova-restaurat
```

## Validacio

Has acabat si:

- [ ] Has creat un contenidor PostgreSQL amb dades reals.
- [ ] Has fet un dump consistent amb `pg_dump | gzip`.
- [ ] Has entès per que el `tar` directe es perillos per a BD actives.
- [ ] Has "perdut" el contenidor i el volum a propòsit.
- [ ] Has restaurat el dump en un contenidor nou i has vist les dades originals.
- [ ] Has après la diferencia entre "tinc backup" i "tinc un backup que funciona".

## Per aprofundir

- Prova de fer el mateix amb un **bind mount** en lloc d'un volum natiu.
- Investiga `docker exec pg-prova pg_dumpall` per fer backup de TOTES les BD.
- Prova de programar el backup amb cron (veure cap 7).
- Compara l'espai que ocupa el `.sql.gz` (dump) vs el `.tar.gz` (volum).
