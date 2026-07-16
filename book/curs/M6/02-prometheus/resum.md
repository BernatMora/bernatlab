# Resum - Capitol 2: Prometheus

## La idea clau

Prometheus es una base de dades de series temporals (time series database) que recull metricas dels teus serveis a intervals regulars. Es el "cervell" del monitoratge: ell pregunta "com estas?" a cada servei, guarda la resposta amb marca de temps, i permet fer consultes com "quina ha estat la CPU mitjana de la RPi aquesta setmana?".

## Que es exactament una metrica?

Una metrica es un valor numeric associat a un instant de temps. Per exemple:

- `cpu_usage_percent{host="rpi", core="0"} 42.5 @ 1716000000`
- `memory_free_bytes 1530000000 @ 1716000000`
- `docker_container_up{name="homeassistant"} 1 @ 1716000000`

Prometheus guarda milers d'aquestes "mostres" i tu pots fer consultes tipus PromQL:

```promql
# CPU mitjana dels ultims 5 minuts
100 - (avg by(instance)(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# Contenidors caiguts
docker_container_up == 0
```

## L'arquitectura pull de Prometheus

A diferencia d'altres sistemes (que reben dades - "push"), Prometheus va a buscar-les ("pull"). Cada 15 segons (per defecte) Prometheus fa una peticio HTTP a un endpoint de cada servei. El servei nomes ha d'exposar les metricas en un format concret.

```
[Prometheus] --GET /metrics--> [Node Exporter a RPi]
[Prometheus] --GET /metrics--> [cAdvisor dins Docker]
[Prometheus] --GET /metrics--> [HA, InfluxDB, etc.]
```

Avantatges del model pull:
- Saps quins serveis estas monitorant (els que tens configurats).
- Si un servei cau, simplement deixa de respondre i ho veus.
- No cal que el servei sàpiga que Prometheus existeix.

Desavantatges:
- Els serveis han d'exposar un endpoint HTTP `/metrics`.
- Serveis dins de NAT/firewall son mes complicats.

## Els exporters

Un "exporter" es un petit programa que converteix l'estat intern d'un servei en metrices Prometheus. A la RPi del BernatLab en tindras uns quants:

- **node_exporter**: CPU, memoria, disc, xarxa, temperatura. El mes important.
- **cadvisor**: metricas dels contenidors Docker.
- **nginx_exporter**: peticions, errors, latencia del proxy invers.
- **blackbox_exporter**: probes HTTP, TCP, ICMP per veure si serveis externs responen.

Cada exporter es un petit contenidor o binaris que s'executa i exposa `/metrics`.

## Instal·lacio a la RPi

```yaml
# Afegeix al teu docker-compose.yml
services:
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    restart: unless-stopped
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
      - ./prometheus/data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.retention.time=30d'
      - '--storage.tsdb.retention.size=2GB'
    ports:
      - "9090:9090"

  node-exporter:
    image: prom/node-exporter:latest
    container_name: node-exporter
    restart: unless-stopped
    pid: host
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/rootfs:ro
    command:
      - '--path.procfs=/host/proc'
      - '--path.sysfs=/host/sys'
      - '--path.rootfs=/rootfs'
      - '--collector.filesystem.mount-points-exclude=^/(sys|proc|dev|host|etc)($$|/)'
    ports:
      - "9100:9100"

  cadvisor:
    image: gcr.io/cadvisor/cadvisor:latest
    container_name: cadvisor
    restart: unless-stopped
    privileged: true
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:ro
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
    ports:
      - "8080:8080"
```

`pid: host` al node-exporter es important: permet veure TOTS els processos del sistema, no nomes els del contenidor.

## Configuracio prometheus.yml

```yaml
# prometheus/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  # Prometheus mateix
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  # Metriques de la RPi (CPU, RAM, disc)
  - job_name: 'node'
    static_configs:
      - targets: ['node-exporter:9100']

  # Metriques dels contenidors Docker
  - job_name: 'cadvisor'
    static_configs:
      - targets: ['cadvisor:8080']

  # Home Assistant
  - job_name: 'homeassistant'
    static_configs:
      - targets: ['homeassistant:8123']
    metrics_path: /api/prometheus
    bearer_token_file: /run/secrets/ha_token

  # Altres serveis que exposin /metrics
  - job_name: 'nginx'
    static_configs:
      - targets: ['nginx-exporter:9113']
```

Despres de pujar els contenidors, accedeix a `http://IP_RPI:9090` i veuras la UI de Prometheus. A "Status" -> "Targets" pots veure si tots els serveis responen correctament (status "UP" en verd).

## PromQL: el llenguatge de consultes

PromQL es sorprenentment poderos. Alguns exemples utils:

```promql
# CPU per core
node_cpu_seconds_total{mode!="idle"}

# Memoria lliure en GB
node_memory_MemAvailable_bytes / 1024 / 1024 / 1024

# Espai en disc lliure
(node_filesystem_avail_bytes{mountpoint="/"} * 100) / node_filesystem_size_bytes{mountpoint="/"}

# Temperatura CPU (RPi)
node_thermal_zone_temp

# Contenidors corrent
container_last_seen{name=~".+"} - bool container_last_seen

# Taxa d'errors HTTP (5xx) per minut
rate(http_requests_total{status=~"5.."}[5m])
```

La gràcia de PromQL es que pots combinar metricas amb operadors matematics i funcions d'agregacio. Practica a `http://IP:9090/graph` escrivint consultes i veient el graf.

## Comandes basiques d'inspeccio

```bash
# Veure quantes series temporals tens
curl -s http://localhost:9090/api/v1/status/tsdb | jq

# Llista els jobs configurats
curl -s http://localhost:9090/api/v1/status/config | jq

# Comprovar si un target esta UP
curl -s http://localhost:9090/api/v1/targets | jq '.data.activeTargets[] | select(.labels.job=="node")'

# Forcar un scrape ara
curl -X POST http://localhost:9090/api/v1/admin/tsdb/snapshot
```

## Retencio i emmagatzematge

Per defecte Prometheus guarda 15 dies. A la RPi (amb SD/SSD limitat) volem ser conservadors:

```
--storage.tsdb.retention.time=30d
--storage.tsdb.retention.size=2GB
```

Aixo vol dir que mai passara de 2GB. Si veus que el disc s'omple, baixa el temps a 15 dies. Per anar mes enlla tenim Thanos o Cortex, pero per la RPi es massa.

## Limitacions de la RPi

A la Raspberry Pi has de vigilar:
- **No posis masses targets**: cada target son mes series i mes CPU.
- **`scrape_interval` mes alt**: 30s en lloc de 15s alleugereix la carrega.
- **Cardinality baixa**: no creis labels dinamics (com IDs unic) que exploten el nombre de series.
- **Recicla metricas velles**: la retencio curta evita que el disc s'ompli.

## Connexions amb altres capitols

- **M6 Cap 1** - L'arquitectura 24/7 on Prometheus es la capa d'observabilitat.
- **M6 Cap 3** - Grafana consumeix les dades de Prometheus per fer dashboards.
- **M6 Cap 4** - Alertmanager (part de Prometheus) s'encarrega d'enviar les alertes.
- **M2 Cap 9** - Monitoritzacio de contenidors amb cAdvisor que acabem de veure.
