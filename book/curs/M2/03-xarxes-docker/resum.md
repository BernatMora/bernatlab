# Resum - Capitol 3: Xarxes Docker

## La idea clau

Cada contenidor Docker te la seva propia interficie de xarxa aillada. Per que es puguin comunicar entre ells i amb el mon exterior, Docker te un sistema de **xarxes virtuals** que es creen i es gestionen amb comandes simples. Sense entendre les xarxes, no pots muntar cap servei decent.

## Per que calen xarxes

Quan executes un contenidor, per defecte queda aillat de tot. Si tens tres serveis (un web, una API, una base de dades), necessites que:

- La base de dades sigui accessible nomes des de l'API (no des de fora).
- L'API sigui accessible des del web (i nomes des del web).
- El web sigui accessible des del navegador (des de fora).

Les xarxes Docker resolen això amb **segmentacio i DNS automatic**.

## Tipus de xarxes

Docker te quatre drivers de xarxa principals:

### 1. Bridge (per defecte)

La xarxa mes comuna. Crea un bridge virtual (com un switch) dins l'amfitrio. Els contenidors que hi son connectats es comuniquen entre ells i tenen acces a l'exterior via NAT.

```bash
# Xarxa bridge per defecte
docker run --name web nginx

# Xarxa bridge custom (recomanada)
docker network create xarxa-meva
docker run --network xarxa-meva --name api node
docker run --network xarxa-meva --name db postgres
```

Els contenidors a la **mateixa xarxa bridge** es poden resoldre per nom (DNS automatic). Aixo es_or_d_or: pots fer `db:5432` i Docker ho resol a la IP correcta.

### 2. Host

El contenidor **comparteix la pila de xarxa de l'amfitrio**. No te la seva pròpia IP aillada. Es rapidissim perque no hi ha virtualitzacio, pero es menys segur.

```bash
docker run --network host nginx
# Ara nginx escolta directament al port 80 de l'amfitrio
```

Cas d'us: serveis que necessiten molt rendiment de xarxa (DNS resolvers, balancejadors), o quan vols evitar conflictes de ports.

### 3. None

El contenidor **no te xarxa**. Esta completament aillat. Es per a tasques molt especials (processar fitxers sense tocar xarxa, proves de seguretat).

```bash
docker run --network none alpine
```

### 4. Overlay

Xarxa que **s'esten entre multiples hosts Docker** (Swarm o Swarm mode). Es la base per a orquestracio. Al BernatLab amb una sola RPi, no la usem.

```bash
docker network create --driver overlay xarxa-multi-host
```

## DNS automatic

Aixo es potser la part mes important. Si tens dos contenidors a la mateixa xarxa bridge custom (`api` i `db`), el contenidor `api` pot fer `ping db` o conectar a `postgres://db:5432` i Docker ho resol a la IP correcta.

Si els poses a la xarxa bridge per defecte (`bridge`), nomes es veuen per IP, no per nom. Per això **mai** no posis els serveis productius a la xarxa per defecte.

## Port mapping

Com accedeix el mon exterior als teus serveis? Amb `-p` (publish):

```bash
# Mapar port 80 del contenidor al 8080 de l'amfitrio
docker run -p 8080:80 nginx

# Especificar IP
docker run -p 127.0.0.1:8080:80 nginx

# Deixar Docker triar el port de l'amfitrio
docker run -p 80 nginx
```

Quan visites `http://raspberry.local:8080`, el trafic va al port 8080 de l'amfitrio, Docker el redirigeix al port 80 del contenidor.

## Cas practic: app web + base de dades

```bash
# 1. Crear la xarxa
docker network create app-net

# 2. Arrencar la base de dades
docker run -d --name db \
  --network app-net \
  -e POSTGRES_PASSWORD=secret \
  postgres:16

# 3. Arrencar l'app web
docker run -d --name web \
  --network app-net \
  -p 8080:80 \
  -e DATABASE_URL=postgres://db:5432/mydb \
  meva-app:latest

# 4. Inspeccionar la xarxa
docker network inspect app-net
```

Fixat com `web` pot conectar a `db:5432` nomes per nom, sense saber la IP. Si la base de dades es reinicia i canvia d'IP, tot continua funcionant.

## Inspeccio de xarxes

```bash
# Llistar xarxes
docker network ls

# Inspeccionar una xarxa (contenidors connectats, subxarxa, gateway)
docker network inspect app-net

# Connectar un contenidor existent a una xarxa
docker network connect app-net contenidor-existent

# Desconnectar
docker network disconnect app-net contenidor

# Esborrar xarxa (nomes si no te contenidors actius)
docker network rm app-net
```

## Xarxes a Docker Compose

Compose simplifica molt la vida. Crea una xarxa per defecte per a l'stack:

```yaml
version: "3.8"
services:
  web:
    image: nginx
    ports:
      - "8080:80"
  api:
    image: node
    networks:
      - backend
  db:
    image: postgres
    networks:
      - backend
networks:
  backend:
    driver: bridge
```

Els serveis `api` i `db` es comuniquen nomes per la xarxa `backend` (no exposada a fora). `web` esta a la xarxa per defecte i pot rebre trafic extern. Si vols mes segmentacio, pots crear mes xarxes.

## Connexions amb altres capitols

- **M2 Cap 2** - Les xarxes son "l'altre costat" dels volums: comparteixen dades vs comparteixen comunicacio.
- **M2 Cap 4** - Compose crea xarxes automaticament.
- **M2 Cap 5** - Els registres es connecten a xarxes privades.
- **M2 Cap 6** - Xarxes aillades es un dels mecanismes de seguretat.
- **M2 Cap 10** - Les xarxes overlay son la base de l'orquestracio.
