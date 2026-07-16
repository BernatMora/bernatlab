# Exercici practic - Capitol 7: Backups segurs

> 30-45 min · Real al teu sistema

## Objectiu

Configurar Restic per fer backups automatics del BernatLab amb una politica de retencio, un desti extern, i una prova de restauracio. Acabaras amb un sistema de backups robust que pots confiar.

## Requisits

- Acces a la RPi amb sudo
- Un compte de Backblaze B2, AWS S3, o un altre servidor per SFTP (opcional)
- 30-45 minuts

## Pas 1: Inventaria que cal backupejar (5 min)

```bash
# Quines coses tens al sistema?
ls -la /opt
ls -la /var/lib/docker/volumes/

# Quins serveis?
docker ps --format '{{.Names}}:{{.Image}}'

# Configuracio del sistema
ls /etc/nginx/ 2>/dev/null
ls /etc/caddy/ 2>/dev/null
ls /etc/ssh/

# Bases de dades
docker exec gitea-postgres psql -U gitea -c '\l' 2>/dev/null
```

Anota tot el que vols protegir.

## Pas 2: Instal·la Restic (5 min)

```bash
sudo apt install restic
restic version
```

## Pas 3: Inicialitza el repositori (10 min)

Tria un desti. Per simplicitat comencem amb local (despres afegirem un núvol):

```bash
# Crea el directori
sudo mkdir -p /var/backups/homelab
sudo chown bernat:bernat /var/backups/homelab

# Genera una contrasenya forta
export RESTIC_PASSWORD=$(openssl rand -base64 32)
echo "Guarda aquesta clau al vault: $RESTIC_PASSWORD"

# Inicialitza el repositori
export RESTIC_REPOSITORY=/var/backups/homelab
restic init
```

**IMPORTANT**: guarda la `RESTIC_PASSWORD` al vault (capitol 6). Si la perds, no podràs restaurar mai.

## Pas 4: Fes el primer backup (5 min)

```bash
# Backup d'exemple (ajusta els paths al teu cas)
restic backup /opt/homelab /opt/gitea /etc/nginx

# Comprova
restic snapshots
# Hauries de veure: latest, ...

# Estadistiques
restic stats
```

## Pas 5: Configura la politica de retencio (5 min)

```bash
restic forget \
  --keep-hourly 24 \
  --keep-daily 7 \
  --keep-weekly 4 \
  --keep-monthly 6 \
  --prune
```

Comprova que s'han aplicat:

```bash
restic snapshots
# Hauries de veure multiples snapshots
```

## Pas 6: Crea el script d'automatitzacio (10 min)

```bash
mkdir -p /opt/homelab/scripts
nano /opt/homelab/scripts/backup.sh
```

Contingut:

```bash
#!/bin/bash
set -e

# Carrega variables d'entorn (RESTIC_PASSWORD, RESTIC_REPOSITORY)
set -a
source /opt/homelab/.env
set +a

echo "=== Inici del backup: $(date) ==="

# Backup
restic backup /opt/homelab /opt/gitea /etc/nginx /etc/caddy

# Retencio
restic forget \
  --keep-hourly 24 \
  --keep-daily 7 \
  --keep-weekly 4 \
  --keep-monthly 6 \
  --prune

echo "=== Backup finalitzat: $(date) ==="

# Notificacio per correu (opcional)
# mail -s "Backup exit" bernat@bernatlab.cat < /var/log/backup.log
```

```bash
chmod +x /opt/homelab/scripts/backup.sh
```

## Pas 7: Programa amb cron o systemd (5 min)

Opcio A: cron (simple)

```bash
echo "0 3 * * * /opt/homelab/scripts/backup.sh >> /var/log/backup.log 2>&1" | sudo tee /etc/cron.d/backup
```

Opcio B: systemd (mes net)

```bash
sudo nano /etc/systemd/system/backup.service
```

```ini
[Unit]
Description=Nightly backup with Restic

[Service]
Type=oneshot
EnvironmentFile=/opt/homelab/.env
ExecStart=/opt/homelab/scripts/backup.sh
```

```bash
sudo nano /etc/systemd/system/backup.timer
```

```ini
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
sudo systemctl list-timers | grep backup
```

## Pas 8: Afegeix un desti al núvol (opcional, 5 min)

Si tens Backblaze B2 o AWS S3, configura un segon repositori:

```bash
# Inicialitza el segon repositori
export RESTIC_REPOSITORY=s3:s3.eu-central-003.backblazeb2.com/bernatlab-backup
export AWS_ACCESS_KEY_ID=...
export AWS_SECRET_ACCESS_KEY=...
restic init

# Fes-hi backup tambe
restic backup /opt/homelab

# O configura el script per fer-ho a tots dos
```

Modifica el script per fer doble backup:

```bash
# Backup local
export RESTIC_REPOSITORY=/var/backups/homelab
restic backup /opt/homelab

# Backup núvol
export RESTIC_REPOSITORY=s3:s3.eu-central-003.backblazeb2.com/bernatlab-backup
restic backup /opt/homelab
```

## Pas 9: Prova la restauracio (5 min)

Importantissim: verifica que el backup es pot restaurar.

```bash
# Crea un directori temporal
mkdir -p /tmp/restore-test

# Restaura
restic restore latest --target /tmp/restore-test

# Comprova
ls -la /tmp/restore-test/opt/homelab/

# Neteja
rm -rf /tmp/restore-test
```

## Pas 10: Documenta (5 min)

Al fitxer `inventari-seguretat.md`, afegeix una seccio "Backups" amb:

- Que es backupeja.
- On es guarden els backups (local, núvol).
- La politica de retencio.
- Quan es fan (programacio).
- Com restaurar.
- Quan es va fer l'ultima prova de restauracio.

## Validacio

- [ ] Restic esta instal·lat.
- [ ] Has inicialitzat un repositori.
- [ ] Has fet un primer backup.
- [ ] La politica de retencio esta configurada.
- [ ] El backup esta automatitzat (cron o systemd).
- [ ] Has provat la restauracio amb exit.
- [ ] (Opcional) Tens un segon desti al núvol.

## Per aprofundir

- Configura **monitoratge** amb Prometheus o Healthchecks.io per saber quan falla.
- Prova **Restic Web** o **Restic Browser** per una interficie grafica.
- Afegeix **rclone** com a backend per accedir a mes núvols.
- Documenta un **runbook de restauracio** pas a pas per si cal fer-ho en calent.
