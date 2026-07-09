# Capítol 45 — Còpies de seguretat amb restic i BorgBackup

> *"Si les teves dades existeixen en un sol lloc, no existeixen. Les còpies no són opcionals."*

## 45.1 Per què les còpies són crítiques

Un homelab sense còpies és un homelab que **viurà fins al primer incident**. I els incidents passen:

- **Disc dur falla** (molt probable amb microSD).
- **Esborrament accidental** (més probable del que voldríem).
- **Atac informàtic** (ransonware, intrusió).
- **Desastre natural** (aigua, foc, llamps).
- **Robatori** (portàtil, Raspberry).
- **Actualització que falla** (de vegades trenca coses).

La regla és clara: **3 còpies, 2 suports diferents, 1 fora de casa**. Això s'anomena la **regla 3-2-1**.

## 45.2 La regla 3-2-1

- **3 còpies**: la original més dues còpies.
- **2 suports diferents**: per exemple, disc local + núvol.
- **1 fora de casa**: per si hi ha un desastre local (incendi, inundació).

Per al BernatLab, una bona estratègia:

1. **Original**: a la Raspberry (microSD + possible SSD extern).
2. **Còpia local**: a un disc USB o NAS a casa.
3. **Còpia remota**: al núvol (Backblaze B2, Wasabi, AWS S3, Google Drive) o a casa d'un familiar.

## 45.3 Restic: l'eina moderna

**Restic** (restic.net) és la millor eina per a còpies de seguretat:

- **Xifrades** per disseny (AES-256).
- **Incrementals** (només canvis des de l'última còpia).
- **Comprimides** (estalvia espai).
- **Versionades** (pots recuperar versions antigues).
- **Ràpides** (gràcies a la deduplicació).
- **Multi-destí** (local, S3, B2, SFTP, etc.).
- **Scriptable** (perfecte per a cron).
- **Open source** (llicència BSD).

Instal·lació a la Raspberry:

```bash
sudo apt install restic
```

O a macOS:

```bash
brew install restic
```

## 45.4 Primeres còpies amb restic

### Inicialitzar el repositori

Un **repositori** restic és la ubicació on es desen les còpies. Pot ser:

- Una carpeta local.
- Un bucket S3 o compatible.
- Un servidor SFTP.

Per començar, una carpeta local:

```bash
mkdir -p /home/bernat/backups/bernatlab
restic init --repo /home/bernat/backups/bernatlab
```

Et demanarà una **contrasenya**. Guarda-la en un gestor de contrasenyes. Si la perds, les dades són irrecuperables.

### Fer la primera còpia

```bash
restic -r /home/bernat/backups/bernatlab backup \
    /home/bernat/homelab \
    /home/bernat/bernatlab \
    /var/lib/docker/volumes
```

Això copia les carpetes especificades. Trigarà una estona la primera vegada.

### Llistar còpies

```bash
restic -r /home/bernat/backups/bernatlab snapshots
```

Veuràs una llista de còpies amb IDs i dates.

### Recuperar una còpia

```bash
# Restaurar tota la còpia més recent
restic -r /home/bernat/backups/bernatlab restore latest --target /tmp/restored

# Restaurar una còpia específica
restic -r /home/bernat/backups/bernatlab restore abc1234 --target /tmp/restored

# Restaurar un sol fitxer
restic -r /home/bernat/backups/bernatlab restore latest \
    --target /tmp/restored \
    --include /home/bernat/homelab/compose/mosquitto/mosquitto.conf
```

## 45.5 Automatitzar amb cron

Per fer còpies diàries, crea un script:

```bash
#!/bin/bash
# backup_diari.sh - Còpia de seguretat diària amb restic

set -euo pipefail

# Configuració
export RESTIC_REPOSITORY="/home/bernat/backups/bernatlab"
export RESTIC_PASSWORD_FILE="$HOME/.restic-password"

# Què copiem
BACKUP_PATHS=(
    "$HOME/homelab"
    "$HOME/bernatlab"
    "/var/lib/docker/volumes"
    "/etc/docker"
    "/etc/nginx"
    "/etc/systemd"
    "$HOME/.bashrc"
    "$HOME/.ssh"
)

# Excloem
EXCLUDE_PATTERNS=(
    "--exclude=**/node_modules"
    "--exclude=**/.cache"
    "--exclude=**/tmp"
    "--exclude=**/__pycache__"
    "--exclude=**/venv"
    "--exclude=**/.venv"
)

# Fem la còpia
restic backup "${EXCLUDE_PATTERNS[@]}" "${BACKUP_PATHS[@]}"

# Neteja: conserva 7 diàries, 4 setmanals, 6 mensuals
restic forget \
    --keep-daily 7 \
    --keep-weekly 4 \
    --monthly 6 \
    --prune

echo "Backup complet: $(date)"
```

Fes-lo executable i afegix-lo a cron:

```bash
chmod +x ~/scripts/backup_diari.sh

# Cada dia a les 3 de la matinada
crontab -e
# Afegeix:
0 3 * * * /home/bernat/scripts/backup_diari.sh >> /var/log/restic.log 2>&1
```

## 45.6 Còpies al núvol

Per complir la regla 3-2-1, cal una còpia fora de casa. Les opcions:

### Backblaze B2

Backblaze B2 és molt econòmic ($0.005/GB/mes). Còpies segures:

```bash
# Inicialitzar el bucket
restic -r b2:bernatlab-backups:bernatlab init

# Fer còpia
restic -r b2:bernatlab-backups:bernatlab backup $HOME/bernatlab
```

Necessites les credencials de B2:

```bash
export B2_ACCOUNT_ID="..."
export B2_ACCOUNT_KEY="..."
```

### Wasabi

Wasabi és similar a S3 però més econòmic per emmagatzematge. Sense cost d'egress (sortida):

```bash
restic -r s3:https://s3.wasabisys.com/bernatlab-backups init
```

### AWS S3 Glacier

Si tens compte AWS, Glacier és molt econòmic però la recuperació és lenta. No recomanable per a ús quotidià.

### Google Drive (via rclone)

rclone (rclone.org) és una eina que munta qualsevol núvol com a sistema de fitxers. Combinat amb restic:

```bash
# Muntar Google Drive
rclone config  # configurar una vegada

# Usar rclone com a backend
restic -r rclone:gdrive:bernatlab-backups backup $HOME/bernatlab
```

Això és útil per a usuaris amb compte de Google.

## 45.7 BorgBackup: una alternativa

**BorgBackup** (borgbackup.org) és l'altre gran referent:

- Xifrat (AES-256, ChaCha20).
- Compressió (lz4, zstd, zlib, lzma).
- Deduplicació.
- Versionat.
- Multi-destí.
- Open source (BSD).

Diferències amb restic:

- **Borg** és més madur i estable, però menys actiu.
- **Restic** té més integracions al núvol (S3, B2, etc.).
- **Restic** té millor interfície per a la deduplicació entre còpies.

Per a un homelab, ambdós serveixen. Tria el que prefereixis.

### Borg bàsic

```bash
# Inicialitzar
borg init --encryption=repokey /home/bernat/backups/borg-repo

# Fer còpia
borg create --stats --progress \
    /home/bernat/backups/borg-repo::bernatlab-$(date +%Y%m%d) \
    $HOME/bernatlab

# Llistar
borg list /home/bernat/backups/borg-repo

# Recuperar
borg extract /home/bernat/backups/borg-repo::bernatlab-20260708
```

## 45.8 Què copiar

No tot s'ha de copiar. Cosa que sí:

- **/home/bernat/homelab** — Configuració del BernatLab.
- **/home/bernat/bernatlab** — El llibre tècnic.
- **/var/lib/docker/volumes** — Volums Docker (InfluxDB, Mosquitto, etc.).
- **/etc/docker** — Configuració Docker.
- **/etc/nginx** o **/etc/caddy** — Configuració del reverse proxy.
- **/etc/systemd** — Serveis personalitzats.
- **~/.bashrc, ~/.profile, ~/.ssh** — Configuració personal.

Cosa que NO:

- **/var/log** (logs, es regeneren).
- **/tmp** (temporals).
- **Caché** (es regenera).
- **node_modules, .venv** (es regeneren).
- **/proc, /sys** (virtuals).

## 45.9 Com xifrar les còpies

Restic i Borg ja xifren per defecte. Però la **contrasenya** és crítica:

1. **Guarda-la en un gestor de contrasenyes** (Bitwarden, KeePass).
2. **Imprimeix-la** en paper i guarda-la en un lloc segur (caixa forta).
3. **No la guardis mai** en el mateix lloc que les dades.

Si perds la contrasenya, **no hi ha manera de recuperar les dades**.

## 45.10 Còpies de la Raspberry

A la Raspberry, algunes coses addicionals:

### La microSD

Les microSD fallen. **Molt**. Per tant:

- Còpia setmanal de tota la microSD.
- Millor encara: usa una SSD externa per al sistema (Raspberry Pi Boot from USB).

Per fer una còpia de la microSD:

```bash
# Amb la Raspberry apagada
sudo dd if=/dev/mmcblk0 of=/home/bernat/backups/sd-card.img bs=4M status=progress
```

Això fa una còpia bit a bit. Comprèn-la amb gzip:

```bash
gzip /home/bernat/backups/sd-card.img
```

### Volums Docker

Els volums Docker sovint contenen les dades més importants (InfluxDB, Grafana, etc.). Assegura't d'incloure'ls:

```bash
# Trobar els volums
docker volume ls

# Còpia
restic backup /var/lib/docker/volumes/
```

Alternativament, fes còpia amb `docker exec` per a les dades vives:

```bash
# Per a InfluxDB
docker exec influxdb influx backup /tmp/backup
docker cp influxdb:/tmp/backup ./influxdb-backup
```

## 45.11 Provar les còpies

**Una còpia no provada no és una còpia**. Cada mes, dedica una hora a:

1. **Recuperar** una còpia en un entorn de test.
2. **Verificar** que els fitxers són correctes.
3. **Provar serveis** crítics (InfluxDB, Grafana, etc.).

Restic té una comanda per verificar la integritat:

```bash
restic -r /home/bernat/backups/bernatlab check
```

Borg té una similar:

```bash
borg check /home/bernat/backups/borg-repo
```

Si això falla, les dades estan corruptes i cal refer-les.

## 45.12 Còpies punt a punt: rsync

Per a còpies simples, sense versionat, **rsync** és l'eina clàssica:

```bash
rsync -avz --delete \
    /home/bernat/homelab/ \
    /mnt/usb-backup/homelab/
```

Avantatges: simple, ràpid, ben conegut.
Desavantatges: sense xifratge, sense versionat, sense compressió.

Per a una còpia de seguretat completa, usa restic o Borg. Rsync és per a sincronització.

## 45.13 Monitoratge de les còpies

Per saber que les còpies funcionen, monitora-les:

1. **Uptime Kuma** pot fer ping al repositori.
2. **Un script** que revisa l'edat de l'última còpia i alerta si és massa antiga.
3. **Codi de color**: el codi exit 0 = OK, != 0 = problema.

Exemple de script d'alerta:

```bash
#!/bin/bash
# check_backup.sh - Comprova que hi ha una còpia recent

REPO="/home/bernat/backups/bernatlab"
MAX_AGE_HOURS=26  # la còpia diària ha de ser de fa menys de 26h

# Trobar la còpia més recent
LATEST=$(restic -r "$REPO" snapshots --json | jq -r '.[0].time')

# Calcular l'edat
AGE_HOURS=$(( ($(date +%s) - $(date -d "$LATEST" +%s)) / 3600 ))

if [ $AGE_HOURS -gt $MAX_AGE_HOURS ]; then
    echo "ALERTA: còpia més antiga de $AGE_HOURS hores!"
    # Enviar alerta a Telegram
    curl -X POST "https://api.telegram.org/bot$TELEGRAM_TOKEN/sendMessage" \
        -d "chat_id=$CHAT_ID&text=⚠️ Backup BernatLab massa antic ($AGE_HOURS hores)"
    exit 1
fi

echo "Còpia OK ($AGE_HOURS hores)"
```

Afegeix-lo a Uptime Kuma o a cron cada matí.

## 45.14 Política de retenció

Quant de temps guardar cada còpia?

- **Diàries**: 7 (una setmana).
- **Setmanals**: 4 (un mes).
- **Mensuals**: 6 ( mig any).
- **Anuals**: 5 (5 anys).

Això és configurable a restic:

```bash
restic forget \
    --keep-daily 7 \
    --keep-weekly 4 \
    --keep-monthly 6 \
    --keep-yearly 5 \
    --prune
```

Això manté un historial raonable sense acumular infinitat de còpies.

## 45.15 Còpies de les dades de sensors

Les dades dels sensors LoRa (Mòdul 3) són especialment valuoses perquè representen **mesos o anys d'observació**. Cal còpia específica:

```bash
# Script específic per a InfluxDB
#!/bin/bash
BACKUP_DIR=/home/bernat/backups/influxdb
DATE=$(date +%Y%m%d)

mkdir -p "$BACKUP_DIR/$DATE"

# Còpia lògica amb influx
docker exec influxdb influx backup /tmp/backup
docker cp influxdb:/tmp/backup "$BACKUP_DIR/$DATE/"

# Comprimir
tar -czf "$BACKUP_DIR/$DATE.tar.gz" -C "$BACKUP_DIR" "$DATE"
rm -rf "$BACKUP_DIR/$DATE"
```

## 45.16 Resum

Les còpies de seguretat són la segona línia de defensa després de les ACLs. La regla 3-2-1 ens diu: 3 còpies, 2 suports, 1 fora de casa. Restic i BorgBackup són les millors eines modernes: xifrades, incrementals, versionades. Cal automatitzar-les amb cron, monitorar-les, i provar-les periòdicament. En el proper capítol veurem 2FA i gestió de secrets.

## 45.17 Exercicis pràctics

1. Instal·la restic a la Raspberry i al Mac.
2. Crea un repositori local.
3. Fes una primera còpia.
4. Escriu el script `backup_diari.sh`.
5. Configura una còpia al núvol (Backblaze B2 o Google Drive via rclone).
6. Configura la retenció.
7. Prova la recuperació en un directori temporal.
8. Afegeix el monitor d'Uptime Kuma.
9. Documenta al README l'estratègia de còpies.

Paraules clau: **còpia de seguretat, backup, restic, BorgBackup, rsync, 3-2-1, regla, restauració, recovery, xifratge, AES-256, ChaCha20, deduplicació, compressió, increment, snapshot, version, retenció, daily, weekly, monthly, yearly, prune, forget, check, verify, integritat, microSD, dd, S3, Backblaze B2, Wasabi, Glacier, rclone, Google Drive, OneDrive, Dropbox, SFTP, ssh, rsync.net, local, remot, fora de casa, off-site, BC, DR, business continuity, disaster recovery, RPO, RTO, RTA, RTA, còpia, original, còpia primària, còpia secundària, còpia terciària, cicle de vida, lifecycle, archival, retenció, GDPR, LOPDGDD, dret a l'oblit, esborrat, purga, retenció legal, conservació, normativa, compliance, auditoria, hash, checksum, sha256, MD5, integritat, fingerprint, signatura, GPG, PGP, encryption, key, passphrase, contrasenya, gestor, password manager, Bitwarden, KeePass, 1Password, automàtica, cron, systemd, timer, scheduler, monitoratge, alerting, Uptime Kuma, alerta, Telegram, exit code, log, error, recovery, prova, test, dry-run, simulate, scenario, playbook, runbook**.
