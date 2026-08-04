# Capítol 52 — Monitoratge avançat amb Grafana i Prometheus

> *"Si no pots mesurar-ho, no pots millorar-ho. Si no pots veure-ho, no saps què falla."*

## 52.1 Què és el monitoratge

**Monitorar** un sistema significa **recollir mètriques contínuament** per entendre què passa. Al BernatLab, això es fa amb tres eines clau:

- **Prometheus**: recull mètriques (números) dels serveis.
- **Grafana**: visualitza les mètriques en gràfiques i panells.
- **Alertmanager**: gestiona les alertes basades en les mètriques.

Aquesta combinació s'anomena **stack PGE** (Prometheus, Grafana, Exporters).

## 52.2 Com funciona Prometheus

Prometheus funciona amb un model **pull** (empènyer vs estirar):

1. Prometheus **demana** mètriques a cada servei cada pocs segons.
2. Els serveis exposen les mètriques a `/metrics` en format text.
3. Prometheus les emmagatzema a la seva base de dades.
4. Grafana les consulta i les dibuixa.

Exemple de mètriques d'un contenidor:

```
# HELP container_cpu_usage_seconds_total CPU usat pel contenidor
# TYPE container_cpu_usage_seconds_total counter
container_cpu_usage_seconds_total{name="grafana"} 12.5

# HELP container_memory_usage_bytes Memòria usada pel contenidor
# TYPE container_memory_usage_bytes gauge
container_memory_usage_bytes{name="grafana"} 52428800
```

## 52.3 Instal·lació de Prometheus

### A la Raspberry amb Docker Compose

Crea `~/homelab/compose/monitoring.yml`:

```yaml
version: "3.8"

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
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/usr/share/prometheus/console_libraries'
      - '--web.console.templates=/usr/share/prometheus/consoles'
    ports:
      - "9090:9090"
    networks:
      - monitoring

  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    restart: unless-stopped
    depends_on:
      - prometheus
    volumes:
      - ./grafana/data:/var/lib/grafana
      - ./grafana/provisioning:/etc/grafana/provisioning
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
      - GF_USERS_ALLOW_SIGN_UP=false
    ports:
      - "3000:3000"
    networks:
      - monitoring

networks:
  monitoring:
    driver: bridge
```

Crea els volums:

```bash
mkdir -p ~/homelab/compose/prometheus/data
mkdir -p ~/homelab/compose/grafana/data
mkdir -p ~/homelab/compose/grafana/provisioning/datasources
mkdir -p ~/homelab/compose/grafana/provisioning/dashboards
```

## 52.4 Configuració de Prometheus

Crea `~/homelab/compose/prometheus/prometheus.yml`:

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s
  external_labels:
    monitor: bernatlab

scrape_configs:
  # El propi Prometheus
  - job_name: prometheus
    static_configs:
      - targets: ['localhost:9090']

  # Node Exporter (mètriques de la Raspberry)
  - job_name: node
    static_configs:
      - targets: ['node-exporter:9100']

  # cAdvisor (mètriques de Docker)
  - job_name: cadvisor
    static_configs:
      - targets: ['cadvisor:8080']

  # Altres serveis HTTP
  - job_name: bernatlab-services
    metrics_path: /metrics
    static_configs:
      - targets:
        - 'mosquitto:9001'
        - 'influxdb:8086'
        - 'uptime-kuma:3001'
```

Afegeix `node-exporter` i `cadvisor` al compose:

```yaml
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
    networks:
      - monitoring

  cadvisor:
    image: gcr.io/cadvisor/cadvisor:latest
    container_name: cadvisor
    restart: unless-stopped
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:ro
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
      - /dev/disk/:/dev/disk:ro
    privileged: true
    networks:
      - monitoring
```

Engega-ho tot:

```bash
cd ~/homelab/compose
docker compose -f monitoring.yml up -d
```

## 52.5 Com accedir-hi

- **Prometheus**: http://100.x.y.z:9090
- **Grafana**: http://100.x.y.z:3000

A Grafana, el primer accés et demanarà contrasenya. L'has definit al compose.

## 52.6 Configurar Grafana

### Afegir Prometheus com a font de dades

Crea `~/homelab/compose/grafana/provisioning/datasources/prometheus.yml`:

```yaml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    editable: true
```

Grafana carregarà automàticament aquesta configuració.

### Crear un dashboard bàsic

Al panell, fes clic a **+** → **Dashboard** → **Add visualization**.

Exemple de panell "Ús de CPU de la Raspberry":

- **Data source**: Prometheus
- **Metric**: `100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)`
- **Visualization**: Time series
- **Title**: CPU Raspberry (%)

Això et mostrarà una gràfica en temps real de l'ús de CPU.

## 52.7 Mètriques útils per al BernatLab

### Sistema (Node Exporter)

- **CPU**: `rate(node_cpu_seconds_total[5m])`
- **RAM**: `node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes`
- **Disc**: `(node_filesystem_size_bytes - node_filesystem_avail_bytes) / node_filesystem_size_bytes`
- **Xarxa**: `rate(node_network_receive_bytes_total[5m])`
- **Temperatura**: `node_thermal_zone_temp` (si tens el sensor)

### Docker (cAdvisor)

- **CPU per contenidor**: `rate(container_cpu_usage_seconds_total[5m])`
- **RAM per contenidor**: `container_memory_usage_bytes`
- **Xarxa per contenidor**: `rate(container_network_receive_bytes_total[5m])`

### Mosquitto (mètriques natives)

- **Missatges publicats**: `mosquitto_messages_published_total`
- **Missatges rebuts**: `mosquitto_messages_received_total`
- **Connexions actives**: `mosquitto_clients_connected`

## 52.8 Dashboards prefabricats

Grafana té una comunitat amb milers de dashboards. Per trobar-los:

1. Vés a https://grafana.com/grafana/dashboards.
2. Busca "Node Exporter Full" (ID: 1860).
3. Copia l'ID.
4. A Grafana: **+** → **Import** → enganxa l'ID.

Altres dashboards útils:

- **Docker Container Monitoring** (ID: 893): mètriques dels contenidors.
- **Prometheus Stats** (ID: 2): mètriques del propi Prometheus.
- **Mosquitto** (ID: 11587): mètriques MQTT.

## 52.9 Retenció de dades

Per defecte, Prometheus guarda les dades 15 dies. Per canviar-ho:

```bash
docker compose -f monitoring.yml down
# Afegeix a la comanda de prometheus:
- '--storage.tsdb.retention.time=30d'
docker compose -f monitoring.yml up -d
```

Això guarda 30 dies. Més dies = més espai en disc.

## 52.10 Què fer amb les dades

Un cop tens gràfiques, pots:

- **Detectar patrons**: la CPU puja cada dia a les 15h? Probablement una tasca programada.
- **Identificar pics**: la RAM s'ha disparat a les 3 de la matinada? Alguna cosa consumeix molt.
- **Comparar períodes**: aquest mes vs. el mes passat.
- **Predir necessitats**: si el creixement de dades és X%/mes, quan s'omplirà el disc?

## 52.11 Compartir dashboards

Grafana permet exportar i compartir dashboards:

1. **Exportar JSON**: a la configuració del dashboard, **Share** → **Export** → **Save to file**.
2. **Importar JSON**: **+** → **Import** → puja el fitxer.
3. **Compartir URL**: **Share** → **Link**. Qualsevol amb la URL pot veure (si és a la mateixa xarxa).

## 52.12 Limitacions de Prometheus

Prometheus és excel·lent, però té limitacions:

- **Només numèrics**: no emmagatzema logs ni traces.
- **No escal·la horitzontalment** (per a moltes dades, cal Cortex, Thanos, o Mimir).
- **No té UI per a alertes avançades** (cal Alertmanager).
- **No és bo per a alta cardinalitat** (moltes etiquetes úniques).

Per al BernatLab, és perfecte. Per a una empresa, caldrien eines més potents.

## 52.13 Com estendre el monitoratge

Quan vulguis afegir més mètriques:

1. **Afegeix exporters**: serveis que exposen mètriques en format Prometheus.
2. **Usa pushgateway**: per a mètriques de treballs curts (cron, scripts).
3. **Configura alertes**: per a mètriques crítiques.
4. **Integra amb Telegram**: per a notificacions.

## 52.14 Què NO monitorar

No totes les mètriques aporten valor:

- **Mètriques que no canvien mai**: inútils.
- **Mètriques massa granulars**: generen molt emmagatzematge sense benefici.
- **Mètriques que no pots actuar**: si no hi ha res a fer, no cal saber-ho.

La regla: **si no saps quina acció prendràs quan vegis aquesta mètrica, no la monitoris**.

## 52.15 Resum

El monitoratge és la base de l'operativa. Prometheus recull, Grafana visualitza, i tu pots prendre decisions. Al BernatLab, amb Node Exporter + cAdvisor + exporters dels serveis tens visibilitat completa. Al proper capítol veurem com configurar alertes per Telegram.

## 52.16 Exercicis pràctics

1. Desplega Prometheus i Grafana a la Raspberry.
2. Configura Node Exporter i cAdvisor.
3. Importa el dashboard "Node Exporter Full".
4. Crea un panell personalitzat de CPU per contenidor.
5. Afegeix mètriques de Mosquitto.
6. Exporta un dashboard i comparteix-lo.
7. Configura la retenció a 30 dies.
8. Documenta al README els URLs de Prometheus i Grafana.
