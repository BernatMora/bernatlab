# Qüestionari — Capitol 3: Backup de volums Docker

> 10 preguntes · ~15 min

## Pregunta 1
On emmagatzema Docker els volums natius per defecte?

- [ ] /home/pi/docker-volumes
- [x] /var/lib/docker/volumes
- [ ] /etc/docker/volumes
- [ ] Al núvol

## Pregunta 2
Quina es la diferencia entre un volum natiu i un bind mount?

- [ ] Son el mateix, noms diferents
- [x] Un volum natiu el gestiona Docker; un bind mount tu tries una ruta de l'amfitrio
- [ ] El bind mount nomes serveix per a Linux
- [ ] El volum natiu es mes lent

## Pregunta 3
Per que NO es recomana fer `tar` d'un directori de PostgreSQL mentre el servidor escriu?

- [ ] El fitxer resultant es massa gran
- [x] El backup pot quedar inconsistent (fitxers nous i vells barrejats)
- [ ] Es massa lent
- [ ] Docker no ho permet

## Pregunta 4
Quina ordre faries servir per fer un dump logic de PostgreSQL dins d'un contenidor?

- [ ] docker exec postgres backup
- [x] docker exec postgres pg_dump -U user database
- [ ] docker save postgres
- [ ] docker export postgres

## Pregunta 5
Quin metode NO atura el contenidor productiu per fer el backup?

- [ ] `docker stop` + `tar` + `docker start`
- [x] Muntar el volum en un contenidor temporal amb `docker run --rm`
- [ ] Apagar la RPi
- [ ] Fer `cp -r` mentre el contenidor corre

## Pregunta 6
Que vol dir "DR test" en el context de backups?

- [ ] Disaster Recovery test: provar que el backup es pot restaurar correctament
- [ ] Daily Restart test
- [ ] Docker Registry test
- [ ] Data Replication test

## Pregunta 7
Al BernatLab, on es guarden els fitxers de dades dels serveis?

- [ ] A dins dels contenidors (no persistent)
- [x] En bind mounts a /home/pi/bernatlab/
- [ ] A la microSD solament
- [ ] Al núvol unicament

## Pregunta 8
Quina eina NO es bona per fer backup consistent d'una base de dades?

- [ ] pg_dump per a PostgreSQL
- [x] Copiar els fitxers .db mentre el servidor escriu
- [ ] mysqldump per a MySQL
- [ ] influx backup per a InfluxDB

## Pregunta 9 (oberta)
Explica amb les teves paraules: per que es important provar de restaurar els backups periodicament, i que pot passar si nomes els crees pero mai els proves?

Pistes per respondre:
- Quin descobriment pots fer quan intentes restaurar un backup "trencat"?
- Quina diferencia hi ha entre "tinc backup" i "tinc un backup que funciona"?
- Amb quina freqUencia hauries de provar la restauracio?

## Pregunta 10 (oberta)
Al BernatLab tens Grafana, InfluxDB, Mosquitto, Nextcloud i PostgreSQL corrent en Docker. Dissenya un pla de backup: quina freqUencia per a cada un, quin metode (tar o dump), i on els guardes. Justifica cada decisio.

Pistes per respondre:
- Grafana: configuracio + dashboards. Son petits.
- InfluxDB: moltes lectures de sensors. Creixen rapid.
- Nextcloud: fitxers dels usuaris. Poden ser grans.
- PostgreSQL: dades estructurades. Cal consistencia.
