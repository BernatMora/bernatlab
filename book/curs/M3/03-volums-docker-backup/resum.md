# Resum — Capitol 3: Backup de volums Docker

## La idea clau

Al BernatLab quasi totes les dades viuen dins de **contenidors Docker**: Grafana te els seus dashboards, InfluxDB te les lectures de sensors, Mosquitto te la configuracio del broker MQTT, Nextcloud te els fitxers dels usuaris. Si no fas backup dels volums d'aquests contenidors, quan la RPi mori o la SD es corrompi, perds **totes** les dades. I no estem parlant d'unes hores de feina per reinstalar: estem parlant de **mesos o anys de dades perdudes**.

La bona noticia es que fer backup dels volums Docker es relativament senzill un cop entens la diferencia entre **volums nadius** (gestiona Docker) i **bind mounts** (els gestionas tu). Els dos es poden backupejar, pero el metode canvia lleugerament.

## On son les dades dins Docker?

Docker emmagatzema les dades dels seus contenidors de dues maneres:

### Volums nadius (volumes)

Docker els gestiona a `/var/lib/docker/volumes/`. Son directoris que Docker crea i manté. Exemple:

```yaml
volumes:
  - grafana-data:/var/lib/grafana
```

Aqui `grafana-data` es el nom del volum. Esta a `/var/lib/docker/volumes/grafana-data/_data`. Docker en te un registre intern i es pot gestionar amb `docker volume ls`.

**Avantatges**: Docker els pot moure entre contenidors, fer backup amb un sol comando, i netejar-los facilment.
**Desavantatges**: estan dins de la jerarquia de Docker, una mica menys "transparents".

### Bind mounts

Tu especifiques una ruta de l'amfitrio (la RPi). Exemple:

```yaml
volumes:
  - /home/pi/bernatlab/grafana:/var/lib/grafana
```

Aqui el directori de la RPi `/home/pi/bernatlab/grafana` es munta dins del contenidor. Tu hi pots accedir directament sense passar per Docker.

**Avantatges**: transparents, pots navegar-hi amb un `ls` normal, i es poden backupejar amb rsync.
**Desavantatges**: la responsabilitat de backups es teva.

## Quin metode fer servir al BernatLab?

Al BernatLab faig servir **bind mounts** per quasi tot. Son mes transparents, puc navegar per `/home/pi/bernatlab/...` i veure exactament quines dades tinc. A mes a mes, els backup amb rsync/restic son trivials: son simplement fitxers en un directori.

Nomes faig servir volums natius per a casos molt especifics on el rendiment es critic (per exemple, la base de dades d'InfluxDB te mes rendiment amb un volum natiu que amb un bind mount a la SD).

## Com fer backup d'un volum Docker

### Metode 1: Aturar el contenidor i copiar el directori

El metode mes directe:

```bash
# Aturar el contenidor
docker stop grafana

# Fer un tar del directori de dades
sudo tar -czf backup-grafana-$(date +%Y%m%d).tar.gz \
  /var/lib/docker/volumes/grafana-data/_data/

# Tornar a aixecar el contenidor
docker start grafana
```

**Pros**: simple, funciona sempre.
**Contres**: el contenidor esta aturat uns segons (pot ser problema en produccio).

### Metode 2: Usar un contenidor temporal

Si el volum es natiu, pots muntar-lo en un contenidor temporal:

```bash
docker run --rm \
  -v grafana-data:/source:ro \
  -v /tmp/backup:/backup \
  alpine tar -czf /backup/grafana-$(date +%Y%m%d).tar.gz -C /source .
```

Aixo munta el volum `grafana-data` (nomes lectura) i el comprimeix dins de `/tmp/backup` de l'amfitrio. El contenidor temporal s'esborra automaticament quan acaba.

**Pros**: el contenidor productiu no s'atura.
**Contres**: nomes serveix per a volums nadius, no per a bind mounts.

### Metode 3: Usar un tool especialitzat

Hi ha eines com **docker-volume-backup** (un script Python) que automatitzen tot plegat. Pero al BernatLab, el metode mes net es fer-ho a ma amb `tar` + un cron.

## Backups consistents de bases de dades

Aquí rau la trampa. Si fas `tar` d'un directori de PostgreSQL mentre el servidor esta escrivint, el backup pot quedar **inconsistent**: alguns fitxers de dades nous, alguns vells, i cap manera de recuperar-los.

La solucio es fer un **dump logic** (no copiar fitxers) abans de fer el backup:

```bash
# Per a PostgreSQL
docker exec postgres pg_dump -U bernatlab bernatlab | \
  gzip > /home/pi/bernatlab/backups/postgres-$(date +%Y%m%d).sql.gz

# Per a MySQL/MariaDB
docker exec mysql mysqldump -u root -p$MYSQL_ROOT_PASSWORD bernatlab | \
  gzip > /home/pi/bernatlab/backups/mysql-$(date +%Y%m%d).sql.gz
```

Aixo extreu les dades en format SQL comprimit, garantint consistència. Despres ja pots fer `tar` del directori si vols, pero el dump es la teva "veritat" per restaurar.

Per a **InfluxDB** i **SQLite** (que veurem als capitols seguents) hi ha mecanismes similars.

## Estrategia al BernatLab

Al BernatLab tinc un script `/home/pi/bernatlab/scripts/backup-volums.sh` que:

1. Fa un `pg_dump` de PostgreSQL comprimit.
2. Fa un dump d'InfluxDB.
3. Fa un `tar` dels bind mounts importants (Grafana, Mosquitto, Nextcloud).
4. Guarda tot a `/home/pi/bernatlab/backups/`.
5. Deixa que restic s'encarregui de copiar-ho al núvol.

Aixo s'executa cada nit a les 2 de la matinada amb un cron.

## Restauracio

Restaurar es la part mes important. Si no proves mai de restaurar, el teu backup no serveix per a res. Periodicament (un cop al mes) hauries de:

1. Agafar un backup recent.
2. Aixecar un contenidor de prova amb ell.
3. Verificar que les dades son correctes.
4. Esborrar el contenidor de prova.

Aixo es el **DR test** (Disaster Recovery test). Es tediós pero salva vides.

## Connexions amb altres capítols

- **Cap 1** — Per què cal un pla 3-2-1 abans de pensar en volums.
- **Cap 2** — L'eina restic s'aplica a aquest cap per automatitzar els backups.
- **Cap 4** — Com fer backup consistent de SQLite.
- **Cap 5** — Com fer backup consistent de PostgreSQL.
- **Cap 6** — Com fer backup consistent d'InfluxDB.
- **Cap 7** — Automatitzacio amb cron i scripts.
