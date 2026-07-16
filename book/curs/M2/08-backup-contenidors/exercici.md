# Exercici practic - Capitol 8: Backup de contenidors

> 40-60 min · Real al teu sistema

## Objectiu

Crear una estrategia de backup complerta per a contenidors Docker: backup de volums, dump de base de dades, automatitzacio amb cron, verificacio i còpia al núvol (simulada). Acabaras tenint un script que pots posar en marxa al BernatLab.

## Requisits

- Docker instal·lat
- Acces a un directori per emmagatzemar backups
- 40-60 minuts
- (Opcional) rclone configurat per a un núvol

## Pas 1: Prepara l'entorn de proves (5 min)

```bash
mkdir -p ~/backup-test/scripts
mkdir -p ~/backup-test/backups
cd ~/backup-test

# Arrenca una base de dades amb dades
docker run -d --name test-db -e POSTGRES_PASSWORD=test -e POSTGRES_DB=testdb postgres:16-alpine

# Espera que estigui llesta
sleep 5
docker exec test-db pg_isready -U postgres

# Crea dades de prova
docker exec test-db psql -U postgres -d testdb -c "CREATE TABLE proves (id SERIAL PRIMARY KEY, nom TEXT);"
docker exec test-db psql -U postgres -d testdb -c "INSERT INTO proves (nom) VALUES ('Bernat'), ('Maria'), ('Joan');"
docker exec test-db psql -U postgres -d testdb -c "SELECT * FROM proves;"
```

## Pas 2: Crea un volum amb dades (5 min)

```bash
# Crea un volum i un contenidor que l'usi
docker volume create dades-test
docker run -d --name test-vol -v dades-test:/app/data alpine sh -c "echo 'Foto 1' > /app/data/foto1.txt && echo 'Foto 2' > /app/data/foto2.txt && sleep 3600"
docker exec test-vol ls /app/data
```

## Pas 3: Script de backup basic (10 min)

Crea `~/backup-test/scripts/backup-basic.sh`:

```bash
#!/bin/bash
# backup-basic.sh
# Fa backup d'un volum i una base de dades

set -e

BACKUP_DIR=~/backup-test/backups
DATA=$(date +%F)
mkdir -p ${BACKUP_DIR}

echo "=== Inici del backup ${DATA} ==="

# 1. Backup del volum amb tar
echo "Backup del volum dades-test..."
docker run --rm \
  -v dades-test:/origen:ro \
  -v ${BACKUP_DIR}:/desti \
  alpine tar czf /desti/vol-dades-test-${DATA}.tar.gz -C /origen .

# 2. Dump de la base de dades
echo "Dump de la base de dades testdb..."
docker exec test-db pg_dump -U postgres testdb > ${BACKUP_DIR}/db-testdb-${DATA}.sql

# 3. Llista el que sha generat
ls -lh ${BACKUP_DIR}

echo "=== Backup finalitzat ==="
```

Fes-lo executable i executa'l:

```bash
chmod +x ~/backup-test/scripts/backup-basic.sh
~/backup-test/scripts/backup-basic.sh
```

## Pas 4: Restaurar el backup (10 min)

Ara simulem que tot sha perdut. Restaurem des del backup.

```bash
# 1. Elimina les dades originals
docker stop test-vol test-db
docker rm test-vol test-db
docker volume rm dades-test
docker volume prune -f

# 2. Comprova que sha perdut tot
ls ~/backup-test/backups  # nomes hauries de veure els .tar.gz

# 3. Crea de nou el volum i restaura'l
docker volume create dades-test
LATEST_VOL=$(ls -t ~/backup-test/backups/vol-dades-test-*.tar.gz | head -1)
docker run --rm \
  -v dades-test:/desti \
  -v ~/backup-test/backups:/backup \
  alpine tar xzf /backup/$(basename $LATEST_VOL) -C /desti

# 4. Verifica
docker run --rm -v dades-test:/data alpine ls /data
docker run --rm -v dades-test:/data alpine cat /data/foto1.txt
```

## Pas 5: Script de backup amb retencio i verificacio (15 min)

Afegeix una mica mes de sofisticacio: retencio (esborrar backups antics) i verificacio.

Crea `~/backup-test/scripts/backup-complet.sh`:

```bash
#!/bin/bash
# backup-complet.sh
# Backup amb retencio i verificacio

set -e

BACKUP_DIR=~/backup-test/backups
RETENTION_DAYS=7
DATA=$(date +%F)
mkdir -p ${BACKUP_DIR}

log() {
  echo "[$(date '+%F %T')] $@"
}

log "=== Inici del backup ${DATA} ==="

# 1. Backup del volum
log "Backup del volum dades-test..."
docker run --rm \
  -v dades-test:/origen:ro \
  -v ${BACKUP_DIR}:/desti \
  alpine tar czf /desti/vol-dades-test-${DATA}.tar.gz -C /origen .

# 2. Dump de la base de dades
log "Dump de la base de dades testdb..."
docker exec test-db pg_dump -U postgres testdb > ${BACKUP_DIR}/db-testdb-${DATA}.sql

# 3. Comprimir el SQL (estan en text pla)
gzip ${BACKUP_DIR}/db-testdb-${DATA}.sql

# 4. Verificar els fitxers de backup
log "Verificant backups..."
for fitxer in ${BACKUP_DIR}/vol-dades-test-${DATA}.tar.gz; do
  if tar tzf $fitxer > /dev/null 2>&1; then
    log "OK: $fitxer"
  else
    log "ERROR: $fitxer corrupte!"
    exit 1
  fi
done

if [ -f ${BACKUP_DIR}/db-testdb-${DATA}.sql.gz ]; then
  log "OK: db-testdb-${DATA}.sql.gz"
else
  log "ERROR: db SQL no creat"
  exit 1
fi

# 5. Esborrar backups antics
log "Esborrant backups antics (>${RETENTION_DAYS} dies)..."
find ${BACKUP_DIR} -type f -mtime +${RETENTION_DAYS} -delete

# 6. Llista final
log "Backups presents:"
ls -lh ${BACKUP_DIR}

log "=== Backup finalitzat amb exit ==="
```

```bash
chmod +x ~/backup-test/scripts/backup-complet.sh
~/backup-test/scripts/backup-complet.sh
```

## Pas 6: Automatitzar amb cron (5 min)

```bash
# Edita el crontab
crontab -e

# Afegeix aquesta linia al final:
# Cada nit a les 3 AM
0 3 * * * /home/pi/backup-test/scripts/backup-complet.sh >> /var/log/backup.log 2>&1
```

(Adapta la ruta del script al teu sistema: `pi` pot ser `iadmin` o un altre.)

Per provar, pots fer una entrada que s'executi cada minut (pero recorda treure-la despres!):

```cron
# PER PROVAR (esborra-ho despres)
* * * * * /home/pi/backup-test/scripts/backup-complet.sh >> /tmp/backup-test.log 2>&1
```

## Pas 7: Sincronitzacio al núvol (opcional) (10 min)

Si tens rclone configurat (Backblaze B2, S3, Google Drive, etc.):

```bash
# Sincronitzar el directori de backups
rclone sync ~/backup-test/backups b2:bernatlab-backups/

# Llista els fitxers al núvol
rclone ls b2:bernatlab-backups/
```

Si no tens rclone configurat, simplement simula amb una còpia a una altre ubicacio:

```bash
# Simula el núvol amb un altre directori
mkdir -p /tmp/nuvol-simulat
cp -r ~/backup-test/backups/* /tmp/nuvol-simulat/
ls -la /tmp/nuvol-simulat
```

## Pas 8: Neteja

```bash
# Atura i elimina els contenidors de prova
docker stop test-db
docker rm test-db
docker volume rm dades-test
docker volume prune -f

# Opcional: elimina el crontab de prova
crontab -e
# Esborra la linia que hem afegit

# Opcional: elimina els scripts i backups
# rm -rf ~/backup-test
```

## Validacio

Has acabat si:

- [ ] Has creat un script que fa backup d'un volum i una base de dades.
- [ ] Has restaurat amb exit un volum perdut.
- [ ] Has afegit retencio automatica al script.
- [ ] Has verificat que els fitxers de backup no son corruptes.
- [ ] Has configurat cron per executar el backup automaticament.
- [ ] Has fet una còpia al núvol o has simulat el procés.

## Per aprofundir

- Investiga **borgbackup** que fa backups incrementals amb desduplicacio i xifrat.
- Mira **restic** que es similar pero mes modern i suporta mes backends.
- Configura un monitor que t'avisi si el backup falla (manda un correu o missatge a Telegram).
- Practica un "disaster recovery" complet: perd la RPi i intenta recuperar tot nomes amb els backups.
