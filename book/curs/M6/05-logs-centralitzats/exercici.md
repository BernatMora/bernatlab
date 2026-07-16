# Exercici practic - Capitol 5: Logs centralitzats

> 45-60 min · Real a la teva RPi

## Objectiu

Instal·lar Loki i Promtail, connectar-los a Grafana, i aprendre a buscar en els logs. Tambe configuraras logrotate i journald perque no omplin el disc. Acabaras tenint un sol lloc on buscar TOTS els logs del BernatLab.

## Requisits

- RPi amb Grafana ja funcionant (capitol 3)
- 500 MB d'espai lliure adicionals
- 45-60 minuts

## Pas 1: Prepara l'estructura de carpetes (5 min)

```bash
cd ~/bernatlab
mkdir -p loki/data
mkdir -p promtail
```

## Pas 2: Crea la configuracio de Loki (5 min)

```bash
nano loki/loki-config.yml
```

Enganxa:

```yaml
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
```

## Pas 3: Crea la configuracio de Promtail (5 min)

```bash
nano promtail/promtail-config.yml
```

Enganxa:

```yaml
server:
  http_listen_port: 9080

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://loki:3100/loki/api/v1/push

scrape_configs:
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

  - job_name: journal
    journal:
      max_age: 12h
      labels:
        job: systemd
    relabel_configs:
      - source_labels: ['__journal__systemd_unit']
        target_label: 'unit'
```

## Pas 4: Afegeix Loki i Promtail al docker-compose (10 min)

Edita `docker-compose.yml`:

```yaml
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

```bash
docker compose up -d loki promtail
docker ps | grep -E "loki|promtail"
```

## Pas 5: Connecta Loki a Grafana (5 min)

A la UI de Grafana:
1. "Connections" -> "Data sources" -> "Add data source" -> "Loki"
2. URL: `http://loki:3100`
3. Guarda i testeja

## Pas 6: Fes les primeres consultes LogQL (15 min)

A Grafana, ves a "Explore" -> tria Loki com a font. Prova aquestes consultes:

```logql
# Tots els logs del sistema
{job="systemd"}

# Logs de Docker en general
{job="docker"}

# Logs d'un contenidor concret
{container="homeassistant"}

# Errors a Home Assistant
{container="homeassistant"} |= "error"

# Logs de sshd amb errors
{unit="sshd.service"} |= "Failed"

# Warnings a grafana
{container="grafana"} |~ "warn|error"

# Logs dels ultims 30 minuts amb un text concret
{container="homeassistant"} |= "influxdb" [30m]

# Comptar el nombre de linies amb error
count_over_time({container="homeassistant"} |= "error" [1h])
```

Per cada consulta, canvia el periode temporal a la dreta (Last 5m, 15m, 1h, etc.).

## Pas 7: Limita la mida del journald (5 min)

```bash
sudo nano /etc/systemd/journald.conf
```

Descomenta o afegeix:

```ini
[Journal]
SystemMaxUse=200M
SystemKeepFree=1G
SystemMaxFileSize=20M
MaxRetentionSec=2week
```

```bash
sudo systemctl restart systemd-journald
journalctl --disk-usage
```

Hauries de veure menys de 200 MB ocupats.

## Pas 8: Configura logrotate pel log de salut (5 min)

```bash
sudo nano /etc/logrotate.d/bernatlab
```

Enganxa:

```
/var/log/bernatlab-health.log {
    daily
    rotate 7
    compress
    missingok
    notifempty
    create 0640 root root
}
```

```bash
sudo logrotate -d /etc/logrotate.d/bernatlab
```

La opcio `-d` es "dry run" - mostra que faria sense executar res. Si tot es correcte, treu el `-d`.

## Validacio

Has acabat si:

- [ ] Loki i Promtail corren com a contenidors.
- [ ] Has afegit Loki com a data source a Grafana.
- [ ] Pots veure logs dels teus contenidors a Grafana Explore.
- [ ] Has fet almenys 5 consultes LogQL amb resultats.
- [ ] Has limitat la mida del journald a 200 MB.
- [ ] Has creat la configuracio de logrotate pel teu log.

## Per aprofundir

- Crea un panell "Logs" dins d'un dashboard Grafana amb les consultes que mes uses.
- Configura una alerta Loki: avisar si surten mes de 100 errors per hora.
- Investiga la integracio Loki + Tempo per traces distribuits.
- Prova a exportar logs antics a object storage abans que s'esborrin.
