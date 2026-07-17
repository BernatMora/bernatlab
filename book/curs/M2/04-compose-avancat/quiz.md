# Qüestionari - Capitol 4: Compose avançat

> 15 preguntes · ~20 min

## Pregunta 1
Quin es l'objectiu principal dels perfils a Docker Compose?

- [ ] Canviar la versio de Docker
- [x] Definir serveis opcionals que nomes s'activen en certes situacions (dev, prod, debug)
- [ ] Accelerar el build
- [ ] Reduir la mida de les imatges

## Pregunta 2
Quina dependencia garanteix que el servei B esperi a que el servei A estigui "sa" (no nomes iniciat)?

- [ ] depends_on:
- [x] depends_on: condition: service_healthy
- [ ] links:
- [ ] networks:

## Pregunta 3
Que fa `extends` a un fitxer Compose?

- [ ] Connecta serveis a mes xarxes
- [x] Hereta configuracio d'un altre servei (base) per evitar duplicar-la
- [ ] Converteix un volum en xarxa
- [ ] Activa el mode verbose

## Pregunta 4
Quin es el format correcte per definir un perfil?

- [ ] profile: dev
- [x] profiles: [dev, debug]
- [ ] config: dev
- [ ] env: dev

## Pregunta 5
Com s'activen els serveis amb perfil?

- [ ] Sempre automaticament
- [x] Amb `docker compose --profile dev up`
- [ ] Només cal posar el nom del perfil
- [ ] Cal editar el fitxer .env

## Pregunta 6
Quina diferencia hi ha entre `docker compose up -d` i `docker compose up`?

- [ ] -d nomes funciona en Linux
- [x] -d deixa els serveis en segon pla (detached); sense -d es veuen els logs
- [ ] Sense -d no arrenca res
- [ ] -d es mes rapid

## Pregunta 7
Quina comanda mostra els logs de tots els serveis alhora?

- [ ] docker compose show
- [x] docker compose logs -f
- [ ] docker compose tail
- [ ] docker compose -l

## Pregunta 8
Que permet la clau `secrets` a un servei?

- [ ] Crea usuaris nous
- [x] Injectar fitxers sensibles (contrasenyes, claus) sense posar-los al fitxer compose
- [ ] Activa el xifrat
- [ ] Connecta a un servidor de secrets extern

## Pregunta 9 (oberta)
Explica amb les teves paraules: per que es una bona practica tenir perfils separats per a "dev" i "prod" en una app amb Docker Compose? Posa un exemple concret.

Pistes per respondre:
- En dev vols eines com phpMyAdmin, debugging, hot reload.
- En prod vols el minim, sense eines de dev exposades.
- Quins serveis tindries nomes en dev?

## Pregunta 10 (oberta)
Imagina que tens una app amb 4 serveis: web, api, db, cache. Tots son essencials. Com escriuries el fitxer `docker-compose.yml`? Tingues en compte: xarxa aillada per a db i cache, port mapping nomes per a web, volums per a db i cache, ordre d'arrencada correcte (db primer, despres cache, despres api, despres web).

Pistes per respondre:
- Quantes xarxes necessites?
- Quins volums nomes?
- Com expresses l'ordre d'arrencada?

## Pregunta 11 (oberta)
Per que creus que Docker Compose ha introduit els perfils en lloc de simplement tenir un fitxer `.yml` per a cada entorn? Quins avantatges te tenir un sol fitxer amb perfils respecte a tenir-ne tres de separats?

Pistes per respondre:
- Un sol fitxer evita duplicar serveis comuns (la base de dades, la xarxa).
- Es mes facil de revisar amb un `diff` quin canvi hi ha entre entorns.
- Per que pot ser problematic tenir la configuracio de prod en un fitxer separat que pot divergir?

## Pregunta 12 (oberta)
Quina relacio hi ha entre els healthchecks i el `depends_on: condition: service_healthy`? Per que no n'hi ha prou amb `depends_on` tot sol? Dona un exemple del BernatLab on la diferencia es importanta.

Pistes per respondre:
- Un servei pot estar "iniciat" pero no "llest" (per exemple, una base de dades que encara esta fent recovery).
- Si el backend es connecta massa aviat, falla.
- Que passaria amb un Nextcloud que espera MariaDB pero aquesta encara no ha acabat d'inicialitzar?

## Pregunta 13 (oberta)
Imagina que el teu company et diu: "el docker-compose.yml es un fitxer de configuracio, no cal posar-hi comentaris". Argumenta per que aixo es una mala practica, especialment al BernatLab on probablement nomes treballes tu pero vols recordar per que vas prendre cada decisio d'aqui 6 mesos.

Pistes per respondre:
- Que passa quan tornes al fitxer despres d'un any?
- Els comentaris expliquen el "per que", no nomes el "que".
- Un bon `docker-compose.yml` es documentacio viva.
- Exemple: per que aquest servei te `cap_drop: ALL`? Vale la pena un comentari.

## Pregunta 14 (oberta)
Aplica els conceptes del capitol al cas concret del BernatLab amb l'stack de monitoritzacio: Prometheus, Grafana, cAdvisor, node-exporter i Uptime Kuma. Escriu mentalment un `docker-compose.yml` que: usi perfils per separar eines opcionals (Grafana nomes en dev?), defineixi una xarxa comuna, munti volums per a la persistencia de Prometheus i Grafana, i configuri un ordre d'arrencada correcte.

Pistes per respondre:
- Quins serveis son essencials i quins opcionals?
- Que passa si Prometheus arranca abans que els altres? No passa res perque ell fa "scrape" periodicament.
- Comprova: Grafana depen de Prometheus? Si.

## Pregunta 15 (oberta)
Quines consequencies te per a la seguretat i la mantenibilitat posar totes les variables d'entorn al fitxer `docker-compose.yml` en lloc d'usar un `.env` separat o els `secrets`? Al BernatLab, quina estrategia tries per gestionar credencials de bases de dades, tokens d'API, etc?

Pistes per respondre:
- Si el compose es puja a Git (inclús privat), les contrasenyes queden exposades.
- Els `.env` es poden posar al `.gitignore` i carregar-se nomes en runtime.
- Els `secrets` (amb fitxers) son encara millors: xifrats, permisos estrictes.
- Trade-off: complexitat vs seguretat.
