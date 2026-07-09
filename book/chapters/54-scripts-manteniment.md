# Capítol 54 — Scripts de manteniment i actualitzacions

> *"Si ho has de fer més de dues vegades, automatitza-ho. Si ho has de fer cada setmana, programa-ho."*

## 54.1 Què automatitzar

Al BernatLab, les tasques repetitives que cal automatitzar són:

- **Actualitzacions del sistema**: apt update + apt upgrade.
- **Actualitzacions de contenidors**: docker compose pull + up.
- **Còpies de seguretat**: restic backup.
- **Neteja**: esborrar logs antics, imatges obsoletes.
- **Rotació de logs**: logrotate.
- **Monitoratge**: alertes, comprovacions periòdiques.
- **Certificats**: renovació automàtica.

## 54.2 Estructura de scripts

Crea una estructura clara:

```
~/homelab/scripts/
├── update-system.sh         # Actualitza el SO
├── update-containers.sh     # Actualitza contenidors
├── backup-daily.sh          # Còpia diària
├── cleanup.sh               # Neteja
├── health-check.sh          # Comprovació de salut
├── restart-failed.sh        # Reiniciar contenidors caiguts
├── cert-renew.sh            # Renovació de certificats
└── lib/
    ├── colors.sh            # Codis de color
    └── notify.sh            # Funcions de notificació
```

Tots els scripts han de ser:

- **Idempotents**: es poden executar múltiples vegades sense efectes secundaris.
- **Amb logging**: registren què fan.
- **Amb notificació**: avisen si falla.
- **Amb cleanup**: netegen recursos temporals.

## 54.3 Plantilla de script

```bash
#!/bin/bash
#
# update-system.sh - Actualitza el sistema operatiu
#
# Ús: ./update-system.sh [--auto]
#
# Opcions:
#   --auto    No demana confirmació

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Funcions
log() { echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $*"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $*"; }
err() { echo -e "${RED}[ERROR]${NC} $*" >&2; }

# Comprovació de root
if [ "$(id -u)" -ne 0 ]; then
    err "Aquest script necessita privilegis de root"
    exit 1
fi

# Paràmetres
AUTO=false
[ "${1:-}" == "--auto" ] && AUTO=true

# Lògica
log "Actualitzant la llista de paquets..."
apt update

log "Comprovant què s'ha d'actualitzar..."
UPDATES=$(apt list --upgradable 2>/dev/null | wc -l)
if [ "$UPDATES" -le 1 ]; then
    log "No hi ha actualitzacions pendents."
    exit 0
fi

log "$UPDATES paquets per actualitzar."
if [ "$AUTO" = false ]; then
    read -p "Continuar? (s/N) " -n 1 -r
    echo
    [[ ! $REPLY =~ ^[Ss]$ ]] && exit 0
fi

log "Actualitzant paquets..."
apt upgrade -y

log "Esborrant paquets obsolets..."
apt autoremove -y

log "Fet!"
```

## 54.4 Script d'actualització de contenidors

`update-containers.sh`:

```bash
#!/bin/bash
set -euo pipefail

cd ~/homelab/compose

for compose_file in *.yml; do
    log "Actualitzant $compose_file"
    docker compose -f "$compose_file" pull
    docker compose -f "$compose_file" up -d
done

log "Esborrant imatges antigues..."
docker image prune -f
```

## 54.5 Script de comprovació de salut

`health-check.sh`:

```bash
#!/bin/bash
set -euo pipefail

HEALTHY=0
UNHEALTHY=0
SERVICES=(
    "portainer:9443"
    "uptime-kuma:3001"
    "homepage:3000"
    "grafana:3000"
    "prometheus:9090"
)

for service in "${SERVICES[@]}"; do
    name="${service%:*}"
    port="${service#*:}"
    if curl -s -o /dev/null -w "%{http_code}" \
        --connect-timeout 3 \
        "http://localhost:$port" | grep -q "^[2-4]"; then
        log "✓ $name"
        ((HEALTHY++)) || true
    else
        err "✗ $name"
        ((UNHEALTHY++)) || true
    fi
done

log "Resultat: $HEALTHY sans, $UNHEALTHY amb problemes"

# Notificar si hi ha problemes
if [ $UNHEALTHY -gt 0 ]; then
    send_telegram "⚠️ BernatLab: $UNHEALTHY serveis no responen"
fi
```

## 54.6 Reiniciar contenidors caiguts

`restart-failed.sh`:

```bash
#!/bin/bash
set -euo pipefail

# Trobar contenidors en estat exited
FAILED=$(docker ps -a --filter "status=exited" --format "{{.Names}}")

if [ -z "$FAILED" ]; then
    log "Cap contenidor caigut."
    exit 0
fi

for container in $FAILED; do
    log "Reiniciant $container..."
    docker restart "$container"
done

send_telegram "🔄 BernatLab: contenidors reiniciats: $FAILED"
```

## 54.7 Neteja periòdica

`cleanup.sh`:

```bash
#!/bin/bash
set -euo pipefail

log "Esborrant imatges dangling..."
docker image prune -f

log "Esborrant volums no utilitzats..."
docker volume prune -f

log "Esborrant xarxes no utilitzades..."
docker network prune -f

log "Esborrant contenidors aturats..."
docker container prune -f

log "Esborrant logs antics (>30 dies)..."
find /var/log -name "*.gz" -mtime +30 -delete
find /var/log -name "*.log.*" -mtime +30 -delete

log "Esborrant còpies de seguretat antigues..."
# Si tens un script de neteja de restic, crida'l
~/homelab/scripts/lib/notify.sh "🧹 BernatLab: neteja setmanal completada"
```

## 54.8 Renovació de certificats

Si uses Caddy, els certificats es renoven sols. Si uses Let's Encrypt amb certbot:

`cert-renew.sh`:

```bash
#!/bin/bash
set -euo pipefail

log "Renovant certificats..."
certbot renew --quiet

log "Recarregant nginx/Caddy..."
docker exec caddy caddy reload 2>/dev/null || systemctl reload nginx

log "Certificats renovats."
```

## 54.9 Ús de cron

Edita `crontab -e` (com a root):

```bash
# Actualització del sistema, diumenge a les 3 AM
0 3 * * 0 /home/bernat/homelab/scripts/update-system.sh --auto >> /var/log/bernatlab-update.log 2>&1

# Actualització de contenidors, dilluns a les 3 AM
0 3 * * 1 /home/bernat/homelab/scripts/update-containers.sh >> /var/log/bernatlab-update.log 2>&1

# Còpia de seguretat, cada dia a les 2 AM
0 2 * * * /home/bernat/homelab/scripts/backup-daily.sh >> /var/log/bernatlab-backup.log 2>&1

# Health check, cada 5 minuts
*/5 * * * * /home/bernat/homelab/scripts/health-check.sh >> /var/log/bernatlab-health.log 2>&1

# Reiniciar contenidors caiguts, cada hora
0 * * * * /home/bernat/homelab/scripts/restart-failed.sh >> /var/log/bernatlab-restart.log 2>&1

# Neteja, dissabte a les 4 AM
0 4 * * 6 /home/bernat/homelab/scripts/cleanup.sh >> /var/log/bernatlab-cleanup.log 2>&1

# Renovació de certificats, dilluns a les 4 AM
0 4 * * 1 /home/bernat/homelab/scripts/cert-renew.sh >> /var/log/bernatlab-cert.log 2>&1
```

## 54.10 Ús de systemd timers (alternativa a cron)

Systemd timers són més moderns i tenen més funcionalitat:

**`/etc/systemd/system/bernatlab-backup.service`**:

```ini
[Unit]
Description=Còpia de seguretat BernatLab
Wants=bernatlab-backup.timer

[Service]
Type=oneshot
ExecStart=/home/bernat/homelab/scripts/backup-daily.sh
User=bernat
```

**`/etc/systemd/system/bernatlab-backup.timer`**:

```ini
[Unit]
Description=Programació còpia BernatLab

[Timer]
OnCalendar=*-*-* 02:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

Activar:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now bernatlab-backup.timer
```

Avantatges de systemd timers:

- Es poden veure amb `systemctl list-timers`.
- Tenen logging integrat (`journalctl`).
- Dependències entre serveis.
- Més fàcils de testejar.

## 54.11 Notificacions

Tots els scripts poden enviar missatges a Telegram. Crea `lib/notify.sh`:

```bash
#!/bin/bash
# notify.sh - Envia missatges a Telegram

# Carregar variables del .env
if [ -f ~/homelab/.env ]; then
    source ~/homelab/.env
fi

: "${TELEGRAM_TOKEN:?Necessites definir TELEGRAM_TOKEN}"
: "${TELEGRAM_CHAT_ID:?Necessites definir TELEGRAM_CHAT_ID}"

send_telegram() {
    local message="$1"
    curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendMessage" \
        -d chat_id="$TELEGRAM_CHAT_ID" \
        -d text="$message" \
        -d parse_mode=HTML \
        > /dev/null
}
```

Afegeix als altres scripts:

```bash
source ~/homelab/scripts/lib/notify.sh
send_telegram "✅ BernatLab: còpia completada"
```

## 54.12 Monitoratge de cron

Si vols saber que el cron s'executa:

```bash
# Health check que comprova els logs
if ! grep -q "$(date '+%Y-%m-%d')" /var/log/bernatlab-backup.log; then
    send_telegram "⚠️ Còpia no s'ha executat avui"
fi
```

## 54.13 Lockfile: evitar execucions simultànies

Si un script pot trigar molt, vols evitar que s'executi dues vegades:

```bash
LOCKFILE=/tmp/bernatlab-backup.lock

if [ -e "$LOCKFILE" ]; then
    err "Ja hi ha una execució en curs"
    exit 1
fi
trap 'rm -f "$LOCKFILE"' EXIT
touch "$LOCKFILE"

# ... la teva lògica aquí ...
```

## 54.14 Comprovació de resultats

Un bon script retorna un codi de sortida:

- **0**: èxit.
- **1**: error genèric.
- **2**: error d'arguments.
- **3**: error de permisos.

I usa `set -euo pipefail` per fallar ràpid en errors.

## 54.15 Errors habituals

**Error 1: scripts que fallen silenciosament**.

Sense `set -e`, els errors es poden perdre. Usa-lo sempre.

**Error 2: scripts que deixen l'estat inconsistent**.

Si el script falla a meitat, hauria de netejar. Usa `trap`.

**Error 3: no provar els scripts abans de programar-los**.

Prova'ls manualment abans de posar-los a cron.

**Error 4: massa automatització**.

No automatitzis coses que passes un cop. Perd més temps configurant que no pas fent-ho.

## 54.16 Resum

Els scripts de manteniment són la base de l'operativa. Plantilles clares, idempotència, logging, notificacions, lockfiles. Cron o systemd timers per programar-los. Telegram per rebre alertes. En el proper capítol veurem els runbooks, que són la cara humana d'aquesta automatització.

## 54.17 Exercicis pràctics

1. Crea l'estructura `~/homelab/scripts/`.
2. Escriu un script d'actualització del sistema.
3. Programa'l amb cron o systemd timer.
4. Afegeix notificacions a Telegram.
5. Crea un health check que s'executi cada 5 min.
6. Documenta els scripts al README.
7. Fes una prova amb un script que simuli un error.
