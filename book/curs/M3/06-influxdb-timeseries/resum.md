# Resum — Capitol 6: InfluxDB per a dades de sensors

## La idea clau

Quan tens sensors que generen lectures cada segon, cada minut o cada hora, durant mesos o anys, les dades creixen rapidissim. Un sol sensor pot generar **5 milions de files/any**. Amb 10 sensors son 50 milions. Amb 50 sensors, 250 milions. Això es el mon de les **series temporals** (time series), i les bases de dades tradicionals (SQLite, PostgreSQL) no estan dissenyades per aixo.

**InfluxDB** es una base de dades **específica per a series temporals** (TSDB). Esta optimitzada exactament per a aquest cas: escriptures massives, consultes per rangs temporals, agregacions per finestres de temps, i politiques de retencio automatiques. Al BernatLab la faig servir per emmagatzemar totes les lectures dels sensors de l'hort: temperatura, humitat, llum, pH del sol, nivell d'aigua del diposit, etc.

## Que es una serie temporal?

Una serie temporal es simplement una secuencia de punts de dades **indexats per temps**. Exemples:

- Temperatura cada minut: 22.5, 22.7, 22.6, 22.8, 22.7, ...
- Preu d'una accio cada segon: 100.5, 100.7, 100.6, ...
- Visites a una web cada hora: 152, 168, 143, ...

Aquestes dades comparteixen uns patrons:

- **Escriptura masiva**: cada interval de temps s'afegeix una nova lectura.
- **Lectura agregada**: poques vegades vols una sola fila; sempre vols agregacions (mitjana per hora, maxim del dia, etc.).
- **Retencio limitada**: les dades molt antigues deixen de ser rellevants.
- **Consultes per rang temporal**: "dona'm les lectures entre el 15 i 20 de juny".

Les BD tradicionals (SQL) poden gestionar-ho, pero no estan optimitzades: les escriptures son lentes, les agregacions costan, i l'espai es dispara. Les TSDB (Time Series Databases) com InfluxDB ho resolen amb **estructures especialitzades**.

## Que es InfluxDB?

**InfluxDB** es una TSDB open source (pero el creador va crear una empresa i hi ha una versio cloud comercial). Caracteristiques:

- **Optimitzada per a series temporals**: emmagatzema les dades en blocs comprimits per temps.
- **Llenguatge propi**: Flux (semblant a SQL pero orientat a series).
- **Retencio automatica**: pots dir "esborra tot el que tingui mes de 2 anys" i ho fa automaticament.
- **Consultes continues**: consultes que s'executen periodicament i guarden el resultat.
- **Downsampling automatic**: "guarda les lectures originals 30 dies, despres nomes les agregades cada hora durant 5 anys".
- **HTTP API**: enviar dades es tan facil com fer una peticio POST.

## InfluxDB v1 vs v2

Hi ha dues versions que coexisteixen:

- **v1.x**: la "classica", mes simple, amb una sola base de dades i un usuari admin. Bona per a homelabs petits.
- **v2.x**: la nova, amb organitzacio, buckets, tokens, millor rendiment. Pero mes complexa de configurar.

Al BernatLab vaig començar amb v2 pero he tornat a v1 perque es mes simple per al meu cas. Si comences de zero, recomano **v2** perque es el futur.

## Quan usar InfluxDB

InfluxDB es la millor opcio quan:

- Tens **moltes lectures** (>10k/segon o >1M/dia).
- Les dades son **series temporals** (indexades per temps).
- Necessites **agregacions per finestres** (mitjana per hora, maxim per dia).
- Volem **politiques de retencio** automatic (esborrar dades antigues).
- Necessites **downsample** (resumir dades antigues a intervals mes grans).

NO es adequada quan:

- Tens **poques dades** (SQLite o Postgres van be).
- Les dades **no son series temporals** (un inventari, una llista de clients).
- Necessites **transaccions complexes** o JOINs (millor Postgres).

## Instal·lacio al BernatLab

```yaml
services:
  influxdb:
    image: influxdb:2.7-alpine
    container_name: bernatlab-influxdb
    restart: unless-stopped
    environment:
      DOCKER_INFLUXDB_INIT_MODE: setup
      DOCKER_INFLUXDB_INIT_USERNAME: bernatlab
      DOCKER_INFLUXDB_INIT_PASSWORD: ${INFLUXDB_PASSWORD}
      DOCKER_INFLUXDB_INIT_ORG: bernatlab
      DOCKER_INFLUXDB_INIT_BUCKET: hort
      DOCKER_INFLUXDB_INIT_RETENTION: 90d
    volumes:
      - /home/pi/bernatlab/influxdb/data:/var/lib/influxdb2
      - /home/pi/bernatlab/influxdb/config:/etc/influxdb2
    ports:
      - "127.0.0.1:8086:8086"
```

## Comandes basiques amb influx CLI

```bash
# Dintre del contenidor
docker exec -it bernatlab-influxdb influx

# Llistar buckets
SHOW BUCKETS

# Seleccionar el bucket
USE bernatlab_hort

# Escriure una lectura (sintaxi v1)
INSERT temperatura,sensor=t1 value=22.5

# Consultar
SELECT * FROM temperatura WHERE time > now() - 1h
```

Per a v2, l'eina es la **influx CLI** des de fora del contenidor.

## Model de dades

A InfluxDB cada "taula" es un **measurement** (com `temperatura`). Cada fila te:

- **time**: timestamp (sempre).
- **fields**: els valors (temperatura, humitat, etc.).
- **tags**: metadades indexades (sensor, ubicacio, etc.).

Exemple:

```bash
INSERT temperatura,sensor=t1,ubicacio=hivernacle value=22.5,humitat=65
#                  ^tags               ^fields
```

Els tags son indexats (rapids de cercar), els fields no.

## Consultes amb Flux (v2)

```flux
// Ultimes 24 hores de temperatura
from(bucket: "hort")
  |> range(start: -24h)
  |> filter(fn: (r) => r._measurement == "temperatura")
  |> mean()

// Mitjana per hora els darrers 7 dies
from(bucket: "hort")
  |> range(start: -7d)
  |> filter(fn: (r) => r._measurement == "temperatura")
  |> aggregateWindow(every: 1h, fn: mean, createEmpty: false)
  |> yield(name: "mitjana")
```

## Com fer backup d'InfluxDB

```bash
# Backup d'una base de dades
docker exec bernatlab-influxdb influx backup /tmp/backup

# Restaurar
docker exec -i bernatlab-influxdb influx restore /tmp/backup
```

Per a v2, hi ha l'ordre `influx backup` i `influx restore`. Son consistents.

## Retencio automatica

A InfluxDB pots configurar **retention policies**:

- `hort_raw`: 30 dies, totes les lectures.
- `hort_1h`: 1 any, agregades per hora.
- `hort_1d`: 5 anys, agregades per dia.

InfluxDB esborra automaticament les dades mes antigues del periode. No cal netejar mai manualment.

## Connexions amb altres capítols

- **Cap 1** — Les lectures dels sensors son dades critiques que cal backupejar.
- **Cap 3** — Com fer backup dels volums d'InfluxDB.
- **Cap 4** — Diferencies amb SQLite.
- **Cap 5** — Diferencies amb PostgreSQL.
- **Cap 10** — Grafana consumeix dades d'InfluxDB per fer grafics.
