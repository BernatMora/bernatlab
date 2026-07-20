# Qüestionari - Capitol 1: Contenidors avançats

> 15 preguntes · ~20 min

## Pregunta 1
Que es una capa (layer) en una imatge Docker?

- [ ] Un contenidor en execucio
- [x] Un diff del sistema de fitxers creat per cada instruccio del Dockerfile
- [ ] Un volum persistent
- [ ] Una xarxa virtual

## Pregunta 2
Quina instruccio del Dockerfile crea una capa nova?

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
- [ ] Permet usar mes memoria

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
Explica amb les teves paraules: quina diferencia hi ha entre una imatge i un contenidor? Posa un exemple de la vida quotidiana si pots.

Pistes per respondre:
- Pensa en la imatge com una "recepta" o "plantilla".
- El contenidor es la "instancia viva" que executes.
- Pots tenir molts contenidors a partir de la mateixa imatge.

## Pregunta 10 (oberta)
Tens una aplicacio Python de 200 MB de dependencies pero el codi final nomes pesa 5 MB. Com ho faries per tenir una imatge Docker el mes petita possible? Explica el proces pas a pas.

Pistes per respondre:
- Parla dels multi-stage builds.
- Com usaries un fitxer `requirements.txt` per aprofitar la cache.
- Quin sistema base triaries (slim? alpine?).
- Esmenta el `.dockerignore`.

## Pregunta 11 (oberta)
Per que creus que Docker emmagatzema les capes en cache i les reutilitza entre builds? Com canvia això la teva manera d'escriure un Dockerfile quan preveus que tocaras el codi sovint?

Pistes per respondre:
- Que passa si toques nomes el codi font pero les dependencies no canvien?
- Per que es important copiar primer el fitxer de dependencies abans que la resta del codi?
- Aixo aplica al cas del BernatLab amb una app que iteres cada setmana?

## Pregunta 12 (oberta)
Quina relacio hi ha entre la mida d'una imatge i la velocitat de desplegament? Si tens el BernatLab amb una RPi a 100.x.y.z i vols actualitzar serveis rapidament, per que importa tenir imatges petites?

Pistes per respondre:
- Temps de descarrega de la imatge nova.
- Espai ocupat a la microSD/SSD.
- Temps d'arrencada del contenidor.
- Cost de memoria RAM en temps d'execucio.

## Pregunta 13 (oberta)
Imagina que el teu company de feina et diu: "el Docker es magic, jo només faig `docker run` i tot funciona". Explica-li amb les teves paraules quines coses passen per sota que ell no veu, usant el concepte de capes i el de sistema de fitxers en copy-on-write.

Pistes per respondre:
- Que es una imatge i que es un contenidor.
- Que vol dir "copy-on-write".
- Per que dos contenidors de la mateixa imatge no es molesten entre ells.

## Pregunta 14 (oberta)
Aplica el concepte de multi-stage build al cas concret del BernatLab: tens un servei Python (FastAPI) que depèn de `pandas` i `numpy` (llibreries molt pesades). Escriu mentalment un Dockerfile amb dos stages i explica cada bloc: que posaries al primer FROM, que al segon, i quins fitxers copiaries entre ells.

Pistes per respondre:
- Primer stage: imatge completa amb compiladors.
- Segon stage: imatge minima nomes amb runtime Python.
- Com passes les dependencies instal·lades del primer al segon.
- Per que `pandas` necessita compilacio pero en runtime nomes cal el `.so` final.

## Pregunta 15 (oberta)
Quines consequencies pratiques te per al BernatLab triar `alpine` versus `debian-slim` com a imatge base? Pensa en compatibilitat de llibreries, mida final, temps de build i seguretat. Argumenta una recomanacio final.

Pistes per respondre:
- Alpine te musl en lloc de glibc: quines llibreries ho pateixen?
- Debian-slim te moltes mes llibreries preinstal·lades pero pesa mes.
- Temps de build: Alpine pot trigar mes per la compilacio de dependencies natives.
- Seguretat: menys superficie d'atac a Alpine.
