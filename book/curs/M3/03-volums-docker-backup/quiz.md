# Qüestionari - Capitol 3: Backup de volums Docker

> 15 preguntes · ~20 min

## Pregunta 1
On emmagatzema Docker els volums natius per defecte?

- [ ] /home/pi/docker-volumes
- [x] /var/lib/docker/volumes
- [ ] /etc/docker/volumes
- [ ] Al núvol

## Pregunta 2
Quina es la diferencia entre un volum natiu i un bind mount?

- [ ] Son el mateix, noms diferents
- [x] Un volum natiu el gestiona Docker; un bind mount tu tries una ruta de lamfitrio
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

- [x] Disaster Recovery test: provar que el backup es pot restaurar correctament
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
- Amb quina frequencia hauries de provar la restauracio?

## Pregunta 10 (oberta)
Al BernatLab tens Grafana, InfluxDB, Mosquitto, Nextcloud i PostgreSQL corrent en Docker. Dissenya un pla de backup: quina frequencia per a cada un, quin metode (tar o dump), i on els guardes. Justifica cada decisio.

Pistes per respondre:
- Grafana: configuracio + dashboards. Son petits.
- InfluxDB: moltes lectures de sensors. Creixen rapid.
- Nextcloud: fitxers dels usuaris. Poden ser grans.
- PostgreSQL: dades estructurades. Cal consistencia.

## Pregunta 11 (oberta)
Per que creus que Docker va triar tenir volums nomenats en lloc de que tot fossin bind mounts? Com afecta a la teva estrategia de backup aquesta decisio al BernatLab?

Pistes per respondre:
- Els volums nomenats viuen a /var/lib/docker/volumes/, camins llargs i críptics.
- Els bind mounts son mes fàcils de recordar i copiar.
- Docker vol abstraccio pero alhora practicitat.
- Trade-off: portabilitat vs simplicitat.

## Pregunta 12 (oberta)
Quina relacio hi ha entre el metode de backup (tar, dump logic, snapshot) i la consistencia de les dades restaurades? Quan es acceptable cada metode al BernatLab? Dona exemples concrets.

Pistes per respondre:
- tar en calent: risc de corrupcio.
- pg_dump: sempre consistent, pero nomes BD.
- Snapshot del filesystem: consistent pero cal parar.
- Per a cada servei, quin metode te sentit?

## Pregunta 13 (oberta)
Imagina que el teu company et diu: "estic fent backup amb `cp -r` de la carpeta de Nextcloud cada dia, ja esta be". Argumenta per que aixo te riscos al BernatLab i proposa una alternativa mes robusta.

Pistes per respondre:
- Fitxers parcials si Nextcloud esta escrivint.
- No es un backup amb versionat.
- Si Nextcloud es corromp, el backup tambe (es una copia identica).
- Proposta: restic amb versionat o snapshot amb contenidor aturat.

## Pregunta 14 (oberta)
Aplica el concepte de backup de volums al cas concret del BernatLab amb l'hort IoT. Tinc InfluxDB amb 2 anys de lectures, Grafana amb 15 dashboards, Mosquitto amb configuracio i un broker MQTT. Dissenya un script de backup periodic que automatitzi el procés i que pugui restaurar en cas d'error.

Pistes per respondre:
- InfluxDB: usar `influx backup` (consistent).
- Grafana: exportar dashboards via API o copiar el volum.
- Mosquitto: copia de la configuracio (text, petita).
- On guardar cada backup?

## Pregunta 15 (oberta)
Quines consequencies te per a la recuperacio davant desastres (DR) no tenir un test periodic de restauracio al BernatLab? Argumenta amb exemples reals de quan un backup "existent" no serveix per res.

Pistes per respondre:
- Backup corrupte que no es detecta fins al moment de restaurar.
- Format de backup canviat per una actualitzacio.
- Permissos canviats que impedeixen la lectura.
- Clau de xifrat perduda.
- El cost d'un test de restauracio vs el cost d'un desastre real.
