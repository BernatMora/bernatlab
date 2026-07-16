# Resum - Capitol 7: Backups segurs

## La idea clau

Un backup no es un luxe, es la diferencia entre un incident i una catastrofe. Pero un backup nomes es valid si es pot **restaurar**. I nomes es segur si esta **xifrat** i **fora del servidor**. Al BernatLab farem servir **Restic**: una eina moderna que fa copies incrementals, xifrades, deduplicades, i que es pot enviar a multiples destins (local, S3, SFTP, B2, etc.).

## La regla 3-2-1

La regla d'or dels backups es la **3-2-1**:

- **3** copies de les dades (l'original + 2 backups).
- **2** tipus de mitjans diferents (disc local + núvol, per exemple).
- **1** copia fora de casa (cloud, casa d'un amic, etc.).

Aquesta regla ens protegeix contra:

- Fallada de hardware (disc espatllat).
- Errors humans (esborrar un fitxer per error).
- Ransomware (atacant xifra les dades i demana rescat).
- Catastrofes naturals (incendi, inundacio).
- Robatori (entren a casa i s'enduen la RPi).

## Que cal backupejar al BernatLab

Depen de cada homelab, pero tipicament:

- **Bases de dades**: Postgres, InfluxDB, SQLite, MariaDB.
- **Volums Docker**: carpetes `/var/lib/docker/volumes/...`.
- **Configuracions**: `/etc/nginx`, `/etc/caddy`, `/opt/*/docker-compose.yml`, `.env`.
- **Secrets** (xifrats!): `.env`, claus SSH, configuracio de Tailscale.
- **Dades personals**: documents, fotos, configuracio de Home Assistant.
- **Repositoris Git locals**: Gitea, Gitness, etc.
- **Logs** (opcional): per forensic si hi ha un incident.

## Restic: l'eina que recomano

**Restic** es una eina de backup moderna i senzilla:

- **Xifratge**: AES-256, autenticacio amb contrasenya o fitxer de claus.
- **Incremental**: nomes copia el que ha canviat, estalvia espai.
- **Deduplicacio**: si un fitxer esta en diversos llocs, no el duplica.
- **Compressio**: opcional, estalvia ample de banda.
- **Multi-desti**: local, S3, SFTP, Backblaze B2, Azure, GCS, etc.
- **Open source**: llicencia BSD.
- **Scripts integrats**: nomes cal una comanda per fer un backup.

Instal·lacio:

```bash
sudo apt install restic
# o descarrega binari
wget https://github.com/restic/restic/releases/download/v0.16.4/restic_0.16.4_linux_arm64.bz2
```

## Primer backup amb Restic

Pas a pas:

```bash
# 1. Inicialitza un repositori (un desti per als backups)
export RESTIC_REPOSITORY=/var/backups/homelab
export RESTIC_PASSWORD="una_contrasenya_llarga_i_aleatoria"
restic init

# 2. Fes la primera copia
restic backup /opt/homelab /opt/gitea /etc/nginx

# 3. Comprova
restic snapshots
restic stats

# 4. Llista els fitxers d'un snapshot
restic ls latest

# 5. Restaura
restic restore latest --target /tmp/restore
```

Guarda la `RESTIC_PASSWORD` al vault (capitol 6) en un lloc segur. Si la perds, **no podràs restaurar mai**.

## Restic amb un desti remot (S3, B2, SFTP)

Backblaze B2 es una opcio molt assequible. Aqui un exemple amb SFTP a un altre servidor:

```bash
export RESTIC_REPOSITORY=sftp:user@backup.bernatlab.cat:/backups/restic
export RESTIC_PASSWORD="..."

# O amb S3 (AWS, Minio, Backblaze B2)
export RESTIC_REPOSITORY=s3:s3.amazonaws.com/bernatlab-backup
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
```

Restic soporta molts backends:

- `local`: directori local.
- `sftp`: servidor SFTP.
- `s3`: AWS S3 i compatibles.
- `b2`: Backblaze B2.
- `azure`: Azure Blob Storage.
- `gs`: Google Cloud Storage.
- `rclone`: qualsevol backend que suporti rclone.

## Politica de retencio

Restic permet definir quantes copies guardar:

```bash
restic forget \
  --keep-hourly 24 \
  --keep-daily 7 \
  --keep-weekly 4 \
  --keep-monthly 6 \
  --prune
```

Aixo mantindra:

- 24 copies de les ultimes hores.
- 7 copies diaries.
- 4 copies setmanals.
- 6 copies mensuals.

I esborra les mes antigues un cop superen els limits. **Recomanat per a homelab**.

## Automatitzacio amb cron o systemd

Un backup que no es automatic no es un backup. Crea un script:

```bash
#!/bin/bash
# /opt/homelab/scripts/backup.sh

set -a
source /opt/homelab/.env
set +a

restic backup /opt/homelab /opt/gitea /etc/nginx

restic forget \
  --keep-hourly 24 \
  --keep-daily 7 \
  --keep-weekly 4 \
  --keep-monthly 6 \
  --prune
```

```bash
chmod +x /opt/homelab/scripts/backup.sh
```

Programar amb cron:

```bash
# Cada dia a les 3 de la matinada
echo "0 3 * * * /opt/homelab/scripts/backup.sh >> /var/log/backup.log 2>&1" | sudo tee -a /etc/cron.d/backup
```

O amb systemd:

```ini
# /etc/systemd/system/backup.service
[Unit]
Description=Nightly backup with Restic

[Service]
Type=oneshot
EnvironmentFile=/opt/homelab/.env
ExecStart=/opt/homelab/scripts/backup.sh
```

```ini
# /etc/systemd/system/backup.timer
[Unit]
Description=Nightly backup timer

[Timer]
OnCalendar=*-*-* 03:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

```bash
sudo systemctl enable backup.timer
sudo systemctl start backup.timer
```

## Bones practiques

- **Automatitza SEMPRE**. No confiïs en la memoria.
- **Monitora els backups**: envia un correu o un webhook si fallen.
- **Prova la restauracio periodicament** (cada 3-6 mesos).
- **Xifratge obligatori**: mai un backup sense xifrar.
- **Multiples destins**: local + núvol.
- **Custodia de la clau**: si perds la clau de xifratge, **no pots recuperar res**.
- **Documenta la politica de retencio**.
- **Audita la mida**: si el backup creix sobtadament, pot ser un problema.

## Proves de restauracio

Un backup no es valid fins que no l'has restaurat. Crea un entorn de test:

```bash
# 1. Crea un entorn aillat
docker run -it --rm -v /tmp/restore:/restore alpine sh

# 2. Desde dins, copia el backup
restic restore latest --target /restore

# 3. Comprova que les dades son correctes
ls -la /restore
```

Fes aixo periodicament. Si trobes que la restauracio falla, tens un problema greu.

## Comandes utils

```bash
# Inicialitzar
restic init

# Fer backup
restic backup /path/a/backupejar

# Llistar snapshots
restic snapshots

# Veure fitxers d'un snapshot
restic ls latest
restic ls snapshot-id

# Estadistiques
restic stats

# Restaurar
restic restore latest --target /tmp/restore

# Esborrar snapshots antics
restic forget --keep-daily 7 --prune

# Comprovar integritat
restic check

# Mount (navegar el backup com un sistema de fitxers)
mkdir /mnt/restic
restic mount /mnt/restic
ls /mnt/restic/snapshots/
fusermount -u /mnt/restic
```

## Connexions amb altres capitols

- **M3 Cap 1-2** - Estrategia de backup i Restic: ja en tens els basics.
- **M2 Cap 8** - Backup de contenidors: com fer backup de volums Docker.
- **Cap 6 d'aquest modul** - Secrets: els secrets van als backups (xifrats).
- **Cap 8 d'aquest modul** - Monitoratge: alerta si el backup falla.

## Conclusio

Els backups son la **xarxa de seguretat** que et permet dormir tranquil. Sense ells, un fallo de hardware, un atac, o un error de comanda pot significar perdre mesos de dades. Restic + una bona politica de retencio + automatitzacio + proves de restauracio es el minim per estar protegit. Recorda: **un backup no es un backup fins que no l'has restaurat amb exit**.
