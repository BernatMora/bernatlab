# Qüestionari - Capitol 1: Contenidors avançats

> 10 preguntes · ~15 min

## Pregunta 1
Què és una capa (layer) en una imatge Docker?

- [ ] Un contenidor en execució
- [x] Un diff del sistema de fitxers creat per cada instruccio del Dockerfile
- [ ] Un volum persistent
- [ ] Una xarxa virtual

## Pregunta 2
Quina instrucció del Dockerfile crea una capa nova?

- [ ] CMD
- [ ] LABEL
- [x] RUN
- [ ] EXPOSE

## Pregunta 3
Per que es recomanen els multi-stage builds?

- [ ] Per fer les imatges mes colorfuls
- [x] Per obtenir imatges finals mes petites, sense eines de build
- [ ] Perque Docker ho exigeix
- [ ] Per poder fer mes d'un port exposed

## Pregunta 4
Quina es la diferencia entre `RUN` i `CMD`?

- [ ] Son sinonims
- [x] RUN executa durant el build; CMD es la comanda per defecte quan arranca el contenidor
- [ ] RUN nomes funciona a Windows
- [ ] CMD nomes funciona a Linux

## Pregunta 5
Quin avantatge te combinar diverses comandes en un sol `RUN`?

- [ ] Cap, es nomes estetica
- [x] Es redueix el nombre de capes i la mida final de la imatge
- [ ] Docker ho fa mes rapid sempre
- [ ] Permet usar mes memòria

## Pregunta 6
Per que es mala idea fer `FROM ubuntu:latest`?

- [ ] Perque Ubuntu no funciona a Docker
- [x] Perque 'latest' pot canviar i el teu build pot trencar-se mes endavant
- [ ] Perque Ubuntu te massa eines
- [ ] Perque gasta massa RAM

## Pregunta 7
Quina comanda llista les capes d'una imatge amb la seva mida?

- [ ] docker ps
- [ ] docker logs
- [x] docker history bernatlab-api:latest
- [ ] docker volume ls

## Pregunta 8
Que fa la instruccio `USER 1000` al final del Dockerfile?

- [ ] Canvia el port per defecte
- [x] Fa que el contenidor NO s'executi com a root
- [ ] Crea 1000 usuaris
- [ ] Activa el mode verbose

## Pregunta 9 (oberta)
Explica amb les teves paraules: quina diferència hi ha entre una imatge i un contenidor? Posa un exemple de la vida quotidiana si pots.

Pistes per respondre:
- Pensa en la imatge com una "recepta" o "plantilla".
- El contenidor es la "instancia viva" que executes.
- Pots tenir molts contenidors a partir de la mateixa imatge.

## Pregunta 10 (oberta)
Tens una aplicacio Python de 200 MB de dependencies pero el codi final nomes pesa 5 MB. Com ho faries per tenir una imatge Docker el mes petita possible? Explica el procés pas a pas.

Pistes per respondre:
- Parla dels multi-stage builds.
- Com usaries un fitxer `requirements.txt` per aprofitar la cache.
- Quin sistema base triaries (slim? alpine?).
- Esmenta el `.dockerignore`.
