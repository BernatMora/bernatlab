# Resum - Capitol 5: Logs centralitzats

## La idea clau

Els logs son el "diari de bord" del sistema. Tot el que passa, queda escrit. Pero si tens 5 contenidors, mes el sistema operatiu, mes journald, mes sshd... acabes amb logs dispersos per 10 fitxers i contenidors diferents. Els logs centralitzats els uneixen tots en un sol lloc on els pots buscar, filtrar i visualitzar.

## Que es un log?

Un log es una linia de text amb un instant de temps i un missatge. Exemples:

```
2026-05-12T14:32:11 rpi kernel: [12345.678] usb 1-1: new high-speed USB device
2026-05-12T14:32:15 homeassistant ERROR: Connection refused to influxdb
2026-05-12T14:32:18 grafana INFO: dashboard loaded by user admin
```

Cada linia te un **timestamp**, una **font** (qui l'escriu), un **nivell** (INFO, WARNING, ERROR) i un **missatge** lliure.

## On son els logs a una RPi amb Docker?

Tenim tres llocs principals:

1. **journald**: el sistema systemd guarda els logs del sistema aqui.
2. **Fitxers de log tradicionals**: `/var/log/syslog`, `/var/log/auth.log`, etc.
3. **Logs de Docker**: cada contenidor te el seu log accessible amb `docker logs`.

```bash
# Veure logs d'un contenidor
docker logs homeassistant --tail 100

# Veure logs en temps real
docker logs -f grafana

# Logs del sistema
journalctl -u docker --since "1 hour ago"

# Tots els logs del sistema en directe
journalctl -f
```

## Per que centralitzar?

Buscar en 10 llocs diferents es molt inefficient. Centralitzar vol dir:

- **Un sol lloc** on buscar (una UI web, una eina CLI).
- **Filtratge potent**: per data, per servei, per nivell, per text.
- **Correlacio**: veure QUIN esdeveniment precedeix un error.
- **Retencio configurable**: vols 7 dies? 30? 1 any?
- **Alertes sobre logs**: "avisame si surt l'error XYZ mes de 10 cops per hora".

## Opcions de stack de logs

Hi ha tres opcions principals, de menys a mes complexe:

### Opcio 1: journald + logrotate (la mes simple)

A la RPi pots viure be nomes amb journald + logrotate si tens pocs serveis. La limitacio es que no hi ha una UI web amigable - cal fer `journalctl` per terminal.

### Opcio 2: Grafana Loki + Promtail (recomanada)

Loki es el "Prometheus dels logs". No indexa el contingut (aixo el fa rapid i lleuger) sino que etiqueta cada log amb labels. Es busca amb una especie de SQL: `{job="docker"} |= "error"`.

- **Loki**: el magatzem de logs. Equivalent a Prometheus pero per logs.
- **Promtail**: l'agent que envia els logs a Loki. Llegeix fitxers o journald i els envia.
- **Grafana**: la UI per visualitzar-los (ja el tens del cap 3).

### Opcio 3: ELK Stack (la mes completa pero pesada)

Elasticsearch + Logstash + Kibana. Es l'estandard industrial pero massa per una RPi:

- Elasticsearch sol necessita 2-4 GB de RAM.
- Logstash es potent pero complicat de configurar.
- Kibana es la UI pero te mil opcions.

A una RPi, ELK es massa. Si vols el mateix tipus d'experiencia, **Grafana Loki es la opcio**.

## Instal·lacio de Grafana Loki

```yaml
# Afegeix al docker-compose.yml
  loki:
    image: grafana/loki:latest
    container_name: loki
    restart: unless-stopped
    user: "0:0"
    volumes:
      - ./loki/data:/loki
      - ./loki/loki-config.yml:/etc/loki/local-config.yaml
    command: -config.file=/etc/loki/local-config.yaml
    ports:
      - "3100:3100"

  promtail:
    image: grafana/promtail:latest
    container_name: promtail
    restart: unless-stopped
    user: "0:0"
    volumes:
      - ./promtail/promtail-config.yml:/etc/promtail/config.yml
      - /var/log:/var/log:ro
      - /var/lib/docker/containers:/var/lib/docker/containers:ro
      - /run/docker.sock:/run/docker.sock:ro
    command: -config.file=/etc/promtail/config.yml
```

## Configuracio de Loki

```yaml
# loki/loki-config.yml
auth_enabled: false

server:
  http_listen_port: 3100

common:
  instance_addr: 127.0.0.1
  path_prefix: /loki
  storage:
    filesystem:
      chunks_directory: /loki/chunks
      rules_directory: /loki/rules
  replication_factor: 1
  ring:
    kvstore:
      store: inmemory

schema_config:
  configs:
    - from: 2024-01-01
      store: tsdb
      object_store: filesystem
      schema: v13
      index:
        prefix: index_
        period: 24h

limits_config:
  retention_period: 30d
  ingestion_rate_mb: 10
  ingestion_burst_size_mb: 20

ruler:
  storage:
    type: local
    local:
      directory: /loki/rules
```

Aixo configura Loki per guardar els logs a `/loki` durant 30 dies i limitar l'ingressio a 10 MB/s (suficient per una RPi).

## Configuracio de Promtail

```yaml
# promtail/promtail-config.yml
server:
  http_listen_port: 9080

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://loki:3100/loki/api/v1/push

scrape_configs:
  # Logs de Docker
  - job_name: docker
    docker_sd_configs:
      - host: unix:///var/run/docker.sock
        refresh_interval: 5s
    relabel_configs:
      - source_labels: ['__meta_docker_container_name']
        target_label: 'container'
        regex: '/(.*)'
      - source_labels: ['__meta_docker_container_log_stream']
        target_label: 'stream'
      - source_labels: ['__meta_docker_compose_service']
        target_label: 'service'

  # Logs del sistema (journald)
  - job_name: journal
    journal:
      max_age: 12h
      labels:
        job: systemd
    relabel_configs:
      - source_labels: ['__journal__systemd_unit']
        target_label: 'unit'

  # Logs dels fitxers tradicionals
  - job_name: syslog
    static_configs:
      - targets: [localhost]
        labels:
          job: syslog
          __path__: /var/log/*.log
```

Promtail llegeix els logs de Docker (via socket), de journald, i dels fitxers de `/var/log`. Els envia a Loki amb labels per identificar la font.

## Visualitzar a Grafana

A Grafana:

1. "Connections" -> "Data sources" -> "Add data source" -> "Loki"
2. URL: `http://loki:3100`
3. Guarda i testeja

Ara tens dos datasources: Prometheus (metricas) i Loki (logs). A qualsevol dashboard pots afegir un panell de tipus "Logs" i fer consultes tipus:

```logql
# Tots els errors de Home Assistant les ultimes 24h
{container="homeassistant"} |= "error" | json | line_format "{{.message}}"

# Logs de grafana amb nivell ERROR
{container="grafana"} |= "ERROR"

# Logs de sshd (intents fallits d'autenticacio)
{unit="sshd.service"} |= "Failed password"

# Logs del kernel
{unit="kernel"} |~ "usb|error"
```

LogQL (el llenguatge de Loki) es mes simple que PromQL. `|=` vol dir "conté el text", `!=` es "no conté", `|~` es regex.

## Rotacio de logs a la RPi

Encara que Loki centralitza, els fitxers de log tradicionals (`/var/log/*.log`) poden créixer i omplir el disc. Cal logrotate:

```bash
# /etc/logrotate.d/bernatlab
/var/log/bernatlab-health.log {
    daily
    rotate 7
    compress
    missingok
    notifempty
    create 0640 root root
    postrotate
        # Opcional: enviar senyal al proces perque re-obri el fitxer
    endscript
}
```

Aixo rota el fitxer cada dia, guarda 7 copies, i les comprimeix. Logrotate ve pre-instal·lat a Raspberry Pi OS pero pot necessitar una mica de configuracio.

## journald: configuracio de retencio

Per defecte journald pot créixer fins a 4 GB o mes. Cal limitar-ho:

```bash
sudo nano /etc/systemd/journald.conf
```

```ini
[Journal]
SystemMaxUse=200M
SystemKeepFree=1G
SystemMaxFileSize=20M
MaxRetentionSec=2week
```

Despres:

```bash
sudo systemctl restart systemd-journald
```

Aixo limita el journal a 200 MB, neteja per deixar 1 GB lliure, i nomes guarda 2 setmanes.

## Comandes utils

```bash
# Cerca logs per paraula clau
journalctl -u docker | grep -i error

# Logs del ultim reboot
journalctl -b -1

# Logs entre dues dates
journalctl --since "2026-05-01" --until "2026-05-12"

# Coneix el tamany del journal
journalctl --disk-usage

# Forçar neteja del journal
sudo journalctl --vacuum-size=100M
sudo journalctl --vacuum-time=7d

# Estadistiques de Loki via API
curl -s http://localhost:3100/metrics | grep loki_
```

## Bones practiques

- **No posis informacio sensible als logs**: claus API, contrasenyes, tokens. Filtra'ls abans.
- **Usa nivells**: DEBUG, INFO, WARNING, ERROR. Tots els serveis els suporten.
- **Estructura els missatges**: usa JSON quan puguis. Es mes facil de parsejar.
- **No t'obsessions amb tots els logs**: comença amb els 2-3 serveis mes importants.

## Connexions amb altres capitols

- **M2 Cap 8** - Backups: tambe hauries de fer backup dels logs importants.
- **M6 Cap 3** - Grafana tambe serveix per visualitzar logs (via Loki).
- **M3 Cap 7** - Gestio de fitxers, on parlem de retencio.
