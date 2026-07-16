# Respostes — Capitol 3: Backup de volums Docker

> Mira les respostes DESPRES d'haver fet el qüestionari.

## Pregunta 1: On son els volums natius?

**Resposta correcta**: /var/lib/docker/volumes.

**Explicacio**: Docker emmagatzema els volums natius a `/var/lib/docker/volumes/<nom>/_data/`. Es poden llistar amb `docker volume ls` i inspeccionar amb `docker volume inspect <nom>`. A la RPi amb bind mounts (com al BernatLab), les dades solen estar a `/home/pi/...` i NO a `/var/lib/docker/volumes/...`.

---

## Pregunta 2: Volum natiu vs bind mount

**Resposta correcta**: Un volum natiu el gestiona Docker; un bind mount tu tries una ruta de l'amfitrio.

**Explicacio**:
- **Volum natiu** (`volumes: - mi-volum:/path`): Docker tria on guardar-lo, normalment a `/var/lib/docker/volumes/`. Tu només coneixes el nom.
- **Bind mount** (`volumes: - /home/pi/dades:/path`): tu tries exactament quina carpeta de l'amfitrio es munta al contenidor. Es mes transparent i mes facil de navegar/backup.

---

## Pregunta 3: Per que `tar` no es segur per a BD actives?

**Resposta correcta**: El backup pot quedar inconsistent (fitxers nous i vells barrejats).

**Explicacio**: Quan la base de dades esta escrivint, els fitxers de dades estan en estat inconsistent: una taula pot tenir les dades noves pero l'index encara apunta a l'estat antic. Si fas `tar` en aquest moment, captures una "instantania" incoherent. Al restaurar, la BD pot no arrencar o retornar dades corruptes. La solucio es fer un **dump logic** (pg_dump, mysqldump) que llegeix les dades de manera consistent independentment de l'estat dels fitxers.

---

## Pregunta 4: Dump de PostgreSQL en contenidor

**Resposta correcta**: `docker exec postgres pg_dump -U user database`.

**Explicacio**: `pg_dump` es l'eina estandard de PostgreSQL per fer backups logics. L'ordre completa sol ser:
```
docker exec postgres pg_dump -U bernatlab bernatlab | gzip > backup.sql.gz
```
El `|` redirigeix la sortida a gzip, que la comprimeix al vol. El resultat es un fitxer SQL comprimit que es pot restaurar amb `psql -f` o amb `cat | psql`.

---

## Pregunta 5: Metode que NO atura el contenidor

**Resposta correcta**: Muntar el volum en un contenidor temporal amb `docker run --rm`.

**Explicacio**: 
```bash
docker run --rm \
  -v grafana-data:/source:ro \
  -v /tmp/backup:/backup \
  alpine tar -czf /backup/grafana.tar.gz -C /source .
```
El contenidor original (grafana) continua funcionant. nomes aixequem un contenidor temporal que munta el volum (nomes lectura) i el comprimeix. Es ideal per backups sense temps d'aturada, pero nomes funciona amb volums natius.

---

## Pregunta 6: Que es un DR test?

**Resposta correcta**: Disaster Recovery test: provar que el backup es pot restaurar correctament.

**Explicacio**: Un DR test es la prova periodica de restauracio. Consisteix en agafar un backup, intentar restaurar-lo, i verificar que les dades son correctes. Serveix per descobrir problemes abans que sigui massa tard: el fitxer esta corrupte, falta una dependencia, el format ha canviat, etc. Al BernatLab faig un DR test un cop al trimestre com a minim.

---

## Pregunta 7: On es guarden les dades al BernatLab?

**Resposta correcta**: En bind mounts a /home/pi/bernatlab/.

**Explicacio**: Tots els serveis productius del BernatLab usen bind mounts:
- `/home/pi/bernatlab/grafana` -> Grafana
- `/home/pi/bernatlab/postgres` -> PostgreSQL  
- `/home/pi/bernatlab/nextcloud` -> Nextcloud
- etc.

Aixo permet navegar per `/home/pi/bernatlab/` i veure totes les dades, fer backup amb `tar` o `rsync` igual que qualsevol altre directori, i saber sempre on son les coses.

---

## Pregunta 8: NO es bona per fer backup de BD

**Resposta correcta**: Copiar els .db mentre el servidor escriu.

**Explicacio**: Aixo es exactament el que NO s'ha de fer. Els fitxers de la base de dades (WAL logs, taules, indexs) estan en estat inconsistent durant les escriptures. Copiar-los garanteix un backup trencat. SEMPRE s'ha d'usar l'eina de dump nativa: `pg_dump`, `mysqldump`, `sqlite3 .dump`, `influx backup`, etc.

---

## Pregunta 9 (oberta): Importancia del DR test

**Resposta model**:

Fer un backup nomes te sentit si es pot restaurar. Si nomes crees backups pero mai els proves, estas vivint en una il·lusio: el dia que necessitis restaurar, descobriraes que el fitxer esta corrupte, que el format ha canviat, que falta una dependencia, o que simplement no saps COM fer-ho.

Al BernatLab vaig descobrir fa dos anys que el meu backup de Nextcloud estava **buit**. Resulta que el bind mount havia canviat de ruta amb una actualitzacio de Docker Compose, i el backup automatic feia mesos que copiava un directori buit. Si ho hagues necessitat, hauria estat un desastre. Pero gracies a un DR test rutinari, ho vaig descobrir i vaig poder corregir la configuracio.

**Regla practica**: fes un DR test **un cop al trimestre** com a minim. Tria un dia (pot ser el primer diumenge de cada trimestre), agafa un backup, intenta restaurar-lo en un entorn aillat, i verifica les dades. Documenta el que ha funcionat i el que no. Si fallen coses, corregeix el sistema de backup abans que sigui massa tard.

**Conclusio**: un backup no provat es com un paraigua foradat. Sembla que serveix, pero el dia de la tempesta t'adones que no.

---

## Pregunta 10 (oberta): Pla de backup pel BernatLab

**Resposta model**:

| Servei | Tipus de dada | FreqUencia | Metode | Desti |
|---|---|---|---|---|
| Grafana | Configuracio + dashboards | Setmanal | `tar` del bind mount | SSD local + Backblaze B2 |
| InfluxDB | Lectures de sensors (creix) | Cada 6 hores | `influx backup` | SSD local + B2 |
| Mosquitto | Config + usuaris MQTT | Setmanal | `tar` | SSD + B2 |
| Nextcloud | Fitxers d'usuari (grans) | Cada dia | `rsync` al SSD, despres a B2 | SSD + B2 |
| PostgreSQL | Dades estructurades | Cada dia | `pg_dump | gzip` | SSD + B2 |

**Justificacio**:

- **Grafana**: son fitxers petits (~10 MB). Setmanal es suficient perque els dashboards canvien poc. Backup amb `tar` esta be perque no es una BD activa en el moment del backup (Grafana ho permet, pero millor aturar-lo uns segons per consistencia).

- **InfluxDB**: creix rapidament amb cada lectura de sensor. Faig backup cada 6 hores perque perdre 6 h de lectures es acceptable, pero perdre 24 h no. Uso `influx backup` que es l'eina consistent.

- **Mosquitto**: nomes config + usuaris. Setmanal. Es un fitxer .conf i un .passwd que ocupen kilobytes.

- **Nextcloud**: els fitxers d'usuari poden ser grans (fotos de l'hort, documents). Backup diari amb rsync es eficient perque rsync nomes copia el que ha canviat.

- **PostgreSQL**: les dades mes critiques (recollides, configuracio, etc.). Backup diari amb `pg_dump | gzip` que garanteix consistencia. Comprimeixo perque els SQL plans poden ser grans.

Tots van a parar a `/home/pi/bernatlab/backups/` i despres restic els puja al Backblaze B2 amb la politica `keep-daily 7, keep-weekly 4, keep-monthly 6`.

---

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum.
- **3-4 encerts**: Rellegeix el capitol amb atencio, sobretot la seccio de backups consistents.
- **0-2 encerts**: Repassem junts el capitol. Es la base per als proxims 7 capitols del modul M3.

## Que fer si has encertat totes

- Passa al **Capitol 4** (SQLite).
- O fes l'**exercici practic** amb un Postgres real per consolidar.
