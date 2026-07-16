# Qüestionari - Capitol 4: Compose avançat

> 10 preguntes · ~15 min

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
