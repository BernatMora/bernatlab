# Qüestionari - Capitol 2: Volums persistents

> 10 preguntes · ~15 min

## Pregunta 1
Que passa amb les dades d'un contenidor quan fas `docker rm`?

- [ ] Es guarden automaticament al núvol
- [x] Es perden, perque la capa escribible s'elimina amb el contenidor
- [ ] Queden al registre de Docker
- [ ] Es mouen a un volum temporal

## Pregunta 2
Quin tipus de volum es recomana per defecte per a dades de servei (per exemple una base de dades)?

- [ ] Bind mount
- [x] Volum nomenat
- [ ] tmpfs
- [ ] Cap, Docker ja ho gestiona

## Pregunta 3
A on viuen els volums nomenats per defecte a l'amfitrio?

- [x] A /var/lib/docker/volumes/
- [ ] A /home/pi/volums/
- [ ] Dins el contenidor
- [ ] Al Docker Hub

## Pregunta 4
Quina es la principal diferencia entre un volum nomenat i un bind mount?

- [ ] Cap, son el mateix
- [x] El volum nomenat el gestiona Docker; el bind mount munta una ruta concreta de l'amfitrio
- [ ] El bind mount es nomes per a Linux
- [ ] El volum nomenat nomes funciona amb Compose

## Pregunta 5
Quan usaries un tmpfs mount?

- [ ] Per guardar una base de dades
- [x] Per a dades temporals que vols nomes en RAM (caches, secrets)
- [ ] Per compartir fitxers entre dos contenidors
- [ ] Per accedir al sistema de fitxers de l'amfitrio

## Pregunta 6
Quina comanda llista tots els volums del sistema?

- [ ] docker ps
- [x] docker volume ls
- [ ] docker images
- [ ] docker network ls

## Pregunta 7
Quina d'aquestes opcions munta un bind mount correctament?

- [ ] docker run -v volum:/data nginx
- [x] docker run -v /home/pi/photos:/app/photos nginx
- [ ] docker run --volume-bind /data nginx
- [ ] docker run --tmpfs /data nginx

## Pregunta 8
Que fa la comanda `docker volume prune`?

- [ ] Crea un volum nou
- [ ] Fa un backup de tots els volums
- [x] Esborra tots els volums que no estan en us per cap contenidor
- [ ] Reinicia el servei de volums

## Pregunta 9 (oberta)
Explica amb les teves paraules: per que un contenidor es volatil i quina consequencia practica te si no fas servir volums? Dona un exemple concret del BernatLab.

Pistes per respondre:
- Pensa en la capa escribible que s'elimina amb el contenidor.
- Que passaria si reinicies la RPi i tens un Nextcloud amb tot alli dins?
- Com afecta a una base de dades PostgreSQL?

## Pregunta 10 (oberta)
Tens un servidor de fotos (Immich o PhotoPrism) al BernatLab. Vols que les fotos originals estiguin a la RPi, pero que el contenidor les pugui llegir i indexar. A mes, vols que la base de dades (que es petita) es pugui fer backup facilment. Quin tipus de volum triaries per a cada cas i per que?

Pistes per respondre:
- Les fotos originals: bind mount o volum nomenat? Per que?
- La base de dades: volum nomenat? Per que?
- Pensa en com faries el backup de cada un.
