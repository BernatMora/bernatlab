# Resum - Capitol 8: Backup de contenidors

## La idea clau

Si tens un servei en produccio (Nextcloud, base de dades, wiki), necessites **backups**. Sense backup, qualsevol fallada (un disc que es mor, una actualitzacio que trenca algo, un atac de ransomware) et pot fer perdre totes les dades. La bona noticia es que Docker facilita els backups perque tot es fitxers.

## Regla 3-2-1

La regla daurada dels backups:

- **3 copies** de les dades (l'original + 2 backups)
- **2 suports diferents** (per exemple, SD + disc USB extern, o SD + núvol)
- **1 fora de la maquina** (per exemple, en un núvol o un servidor remot)

Al BernatLab: les dades viuen a la RPi (original). Backup 1: un disc SSD USB muntat a la mateixa RPi. Backup 2: una sincronitzacio a un núvol (Backblaze B2, S3, etc.).

## Que cal fer backup

Tot el que **no es pot tornar a generar**:

1. **Volums Docker** (les dades que hi son dins: base de dades, fitxers pujats, configuracio).
2. **Configuracio** (fitxers `docker-compose.yml`, `.env`, configuracions de cada servei).
3. **Secrets** (contrasenyes, claus - **xifrats**!).
4. **Imatges personalitzades** (si n'has construit alguna).

El que **NO** cal fer backup:
- Les imatges de Docker Hub (es poden tornar a baixar).
- El sistema operatiu (es pot reinstal·lar i Docker es pot tornar a instal·lar).

## Estratègies de backup

### 1. Backup de volums (la mes important)

Els volums son carpetes a `/var/lib/docker/volumes/`. Per fer-ne backup, usem un **contenidor temporal** que munta el volum i l'empaqueta:

```bash
# Backup d'un volum nomenat
docker run --rm \
  -v dades-meves:/origen:ro \
  -v ~/backups:/desti \
  alpine tar czf /desti/dades-meves-$(date +%F).tar.gz -C /origen .

# Restaurar
docker volume create dades-meves-restaurades
docker run --rm \
  -v dades-meves-restaurades:/desti \
  -v ~/backups:/origen \
  alpine tar xzf /origen/dades-meves-2024-01-15.tar.gz -C /desti
```

### 2. Backup de base de dades

Hi ha eines especifiques per a cada base de dades:

```bash
# PostgreSQL
docker exec postgres-container pg_dump -U user dbname > backup.sql

# MySQL / MariaDB
docker exec mariadb-container mysqldump -u root -p dbname > backup.sql

# MongoDB
docker exec mongo-container mongodump --archive > backup.archive
```

Important: el backup ha d'incloure **totes** les dades, no nomes l'esquema. Les eines de dump ho fan.

### 3. Backup de fitxers de configuracio

Simplement copiar els fitxers:

```bash
# Backup del directori de compose
tar czf config-backup.tar.gz /home/pi/bernatlab/

# Important: xifrar si hi ha secrets!
gpg --symmetric --cipher-algo AES256 config-backup.tar.gz
```

### 4. Backup incremental

Si tens 100 GB de dades, fer-ne backup sencer cada dia es costos. Usa **rsync** amb `--link-dest` per fer copies dures incrementals:

```bash
# Primer backup: sencer
rsync -a /home/pi/dades/ /backup/daily.0/

# Segon backup: nomes els canvis (link-dest)
rsync -a --link-dest=/backup/daily.0 /home/pi/dades/ /backup/daily.1/
```

O usa una eina dedicada: **borgbackup**, **restic**, **duplicity**.

### 5. Backup al núvol

Pots sincronitzar al núvol amb eines com:

- **rclone**: suporta S3, Google Drive, Backblaze B2, OneDrive, etc.
- **restic**: suporta diversos backends.
- **aws-cli** o **b2-cli**: especific per a un núvol.

```bash
# Amb rclone
rclone sync /backup/daily.0 b2:bernatlab-backup/

# Amb restic
restic -r b2:bernatlab-backup:/ backup /home/pi/dades
```

## Automatitzacio amb cron

Els backups manuals son perillosos perque **t'oblides**. Automatitza'ls amb `cron`:

```bash
# Editar el crontab
crontab -e

# Afegir una feina que fa backup cada nit a les 3 AM
0 3 * * * /home/pi/scripts/backup-volums.sh >> /var/log/backup.log 2>&1
```

Exemple de script:

```bash
#!/bin/bash
# backup-volums.sh

BACKUP_DIR=/home/pi/backups
DATA=$(date +%F)
RETENTION=7  # dies

# Backup de cada volum
for volum in nextcloud-data mariadb-data; do
  docker run --rm \
    -v ${volum}:/origen:ro \
    -v ${BACKUP_DIR}:/desti \
    alpine tar czf /desti/${volum}-${DATA}.tar.gz -C /origen .
done

# Backup de la base de dades
docker exec mariadb-container mysqldump -u root -p"${DB_PASS}" nextcloud > ${BACKUP_DIR}/nextcloud-db-${DATA}.sql

# Esborrar backups antics
find ${BACKUP_DIR} -type f -mtime +${RETENTION} -delete
```

## Verificar els backups

Un backup que no s'ha verificat **no es un backup**. Pots tenir un script trencat que "fa backup" pero que no esta fent res correctament.

```bash
# Verificar que un .tar.gz no esta corrupte
tar tzf backup.tar.gz > /dev/null && echo "OK" || echo "CORRUPT!"

# Restaurar a un directori temporal i comprovar
mkdir /tmp/test-restore
tar xzf backup.tar.gz -C /tmp/test-restore
ls -la /tmp/test-restore/
diff -r /tmp/test-restore /origen/
```

## Emmagatzematge de backups

- **Local** (disc SSD USB): rapid pero si la casa crema, tot es perd.
- **Núvol** (Backblaze B2, Wasabi, S3): segur pero mes lent.
- **Extern** (disc USB guardat a una altra ubicacio): segur pero cal record de portar-lo.

La millor estrategia: combinacio. Un backup local (rapid) + un al núvol (segur).

## Xifrat

Si els teus backups contenen dades sensibles (que casi sempre), **xifra'ls**:

```bash
# Xifrar amb GPG
gpg --symmetric --cipher-algo AES256 backup.tar.gz

# Es necessita una passphrase. No la perdis!

# Desxifrar
gpg -d backup.tar.gz.gpg > backup.tar.gz
```

O usa una eina que xifra per defecte com **restic** o **borgbackup**.

## Connexions amb altres capitols

- **M2 Cap 1** - Les imatges es poden tornar a descarregar, pero les teves pròpies es poden perdre.
- **M2 Cap 2** - Els volums son el que cal fer backup.
- **M2 Cap 5** - Els registres privats son part del backup.
- **M2 Cap 7** - Sempre fer backup abans d'actualitzar.
