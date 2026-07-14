# Capítol 67 — Prometheus i alertes avançades

> *"Uptime Kuma et diu si un servei està viu o mort. Prometheus et diu com està de salut. La diferència és subtil però fonamental."*

## 67.1 Què aprendràs

- Què és Prometheus i per què serveix.
- Com instal·lar Prometheus + Node Exporter + cAdvisor + Alertmanager.
- Com crear mètriques personalitzades.
- Com configurar alertes intel·ligents.
- Com integrar-ho amb Telegram.
- Com visualitzar les mètriques a Grafana.

## 67.2 Durada estimada

1-1.5 hores.

## 67.3 Què és Prometheus

**Prometheus** és un sistema de monitoratge de mètriques (números) amb:

- **Pull**: ell mateix demana les mètriques als serveis cada X segons.
- **Series temporals**: emmagatzema cada mètrica amb un timestamp.
- **Alerting**: té el seu propi sistema d'alertes (Alertmanager).
- **Lenguatge de consultes**: PromQL, potent i flexible.

Combinat amb **Grafana** (que ja tens) tens una solució completa.

## 67.4 Arquitectura

```
[ Node Exporter ]   ──┐
[ cAdvisor ]        ──┤
[ Mosquitto exporter ]─┤──→ [ Prometheus ] ──→ [ Alertmanager ] ──→ [ Telegram ]
[ Custom exporter ]  ──┘                       ──→ [ Grafana ]
```

Cada component:

- **Node Exporter**: mètriques del sistema (CPU, RAM, disc, xarxa, temperatura).
- **cAdvisor**: mètriques dels contenidors Docker.
- **Mosquitto exporter**: mètriques del broker MQTT.
- **Custom exporter**: mètriques específiques (per exemple, l'estat del node LoRa).
- **Prometheus**: recull tot i emmagatzema.
- **Alertmanager**: gestiona les alertes.
- **Grafana**: visualitza.

## 67.5 Instal·lació

Crea `~/homelab/compose/prometheus.yml`:

```yaml
version: "3.8"

services:
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    restart: unless-stopped
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
      - ./prometheus/rules.yml:/etc/prometheus/rules.yml
      - ./data/prometheus:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--storage.tsdb.retention.time=30d'
    ports:
      - "9090:9090"

  alertmanager:
    image: prom/alertmanager:latest
    container_name: alertmanager
    restart: unless-stopped
    volumes:
      - ./prometheus/alertmanager.yml:/etc/alertmanager/alertmanager.yml
    command:
      - '--config.file=/etc/alertmanager/alertmanager.yml'
    ports:
      - "9093:9093"

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

Crea `~/homelab/compose/prometheus/prometheus.yml`:

```yaml
global:
  scrape_interval: 30s
  evaluation_interval: 30s

rule_files:
  - "rules.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets: ['alertmanager:9093']

scrape_configs:
  - job_name: prometheus
    static_configs:
      - targets: ['localhost:9090']

  - job_name: node
    static_configs:
      - targets: ['node-exporter:9100']

  - job_name: cadvisor
    static_configs:
      - targets: ['cadvisor:8080']
```

Crea `~/homelab/compose/prometheus/rules.yml`:

```yaml
groups:
  - name: bernatlab
    rules:
      - alert: HighCPUUsage
        expr: 100 - (avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 90
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "CPU alta a {{ $labels.instance }}"
          description: "CPU al {{ $value }}% durant més de 5 minuts."

      - alert: LowMemory
        expr: (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) * 100 < 10
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "RAM baixa a {{ $labels.instance }}"

      - alert: DiskFull
        expr: (node_filesystem_avail_bytes{fstype!="tmpfs"} / node_filesystem_size_bytes) * 100 < 10
        for: 10m
        labels:
          severity: critical
        annotations:
          summary: "Disc ple a {{ $labels.instance }}"

      - alert: ContainerDown
        expr: up{job=~"cadvisor|prometheus"} == 0
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Contenidor {{ $labels.instance }} caigut"
```

Crea `~/homelab/compose/prometheus/alertmanager.yml`:

```yaml
global:
  resolve_timeout: 5m

route:
  group_by: ['alertname', 'instance']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  receiver: 'telegram'

receivers:
  - name: 'telegram'
    webhook_configs:
      - url: 'http://alert-webhook:8080/alerts'
```

Crea `~/homelab/compose/alert-webhook/`:

```python
# app.py
import os, requests
from flask import Flask, request

app = Flask(__name__)

@app.route("/alerts", methods=["POST"])
def alerts():
    data = request.json
    for alert in data.get("alerts", []):
        status = alert.get("status", "unknown")
        emoji = "🔴" if status != "resolved" else "✅"
        text = alert.get("annotations", {}).get("summary", "")
        desc = alert.get("annotations", {}).get("description", "")
        msg = f"{emoji} {text}\n{desc}"
        requests.post(
            f"https://api.telegram.org/bot{os.environ['TELEGRAM_TOKEN']}/sendMessage",
            json={"chat_id": os.environ["TELEGRAM_CHAT_ID"], "text": msg},
        )
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
```

Engega:

```bash
cd ~/homelab/compose
docker compose -f prometheus.yml up -d
```

Afegeix el webhook al compose.

## 67.6 Verificar

- Prometheus UI: http://hortosona:9090
- Alertmanager UI: http://hortosona:9093
- Node Exporter: http://hortosona:9100/metrics

A Prometheus, vés a **Status** → **Targets** i comprova que tots els jobs estan "UP".

## 67.7 Connectar Grafana a Prometheus

A Grafana:

1. Connections → Data sources → Add data source.
2. Tria **Prometheus**.
3. URL: `http://prometheus:9090`.
4. Save & test.

Ara pots crear panells que combinen dades de Grafana (InfluxDB) i Prometheus (CPU, RAM, etc.).

## 67.8 Dashboard recomanat

Importa el dashboard oficial de Node Exporter:

1. Grafana → **+** → **Import**.
2. Enganxa l'ID `1860` (Node Exporter Full).
3. Tria el data source Prometheus.
4. Import.

Ara tens un dashboard complet amb CPU, RAM, disc, xarxa, processos, etc.

## 67.9 Provar les alertes

Per forçar una alerta, podem aturar un servei:

```bash
docker stop grafana
```

Espera 2-3 minuts. Hauries de rebre un missatge a Telegram: "Contenidor grafana caigut".

Torna a engegar:

```bash
docker start grafana
```

Rebràs "Resolved".

## 67.10 Mètriques personalitzades: l'estat del node LoRa

Podem exposar l'estat del node LoRa com a mètriques. Per exemple, un script Python que exposa "l'última vegada que el node ha enviat dades":

```python
# lora-exporter.py
from prometheus_client import start_http_server, Gauge
import paho.mqtt.client as mqtt
import time
import os

last_seen = Gauge('lora_node_last_seen_timestamp', 'Última vegada que el node ha enviat dades', ['node'])

def on_message(client, userdata, msg):
    import time
    last_seen.labels(node="hort1").set(time.time())

client = mqtt.Client()
client.username_pw_set("bernat", os.environ["MQTT_PASSWORD"])
client.connect("mosquitto", 1883, 60)
client.subscribe("sensors/#")
client.on_message = on_message

start_http_server(9119)
client.loop_forever()
```

Afegeix aquest servei al compose de Prometheus. Ara pots crear una alerta:

```yaml
- alert: LoRaNodeOffline
  expr: time() - lora_node_last_seen_timestamp{node="hort1"} > 3600
  for: 10m
  labels:
    severity: warning
  annotations:
    summary: "Node hort1 sense dades des de fa més d'1h"
```

## 67.11 Què ve després

Ja tens monitoratge complet. Al **Cap 68** aprendrem a fer **runbooks** per reaccionar ràpidament als incidents. Al **Cap 69** farem el **DRP** amb un test real.

## 67.12 Errors habituals

**Error 1: Prometheus no recull mètriques**.

Mira els targets a la UI. Si un job està "DOWN", comprova la URL i la xarxa.

**Error 2: les alertes no s'envien**.

Mira els logs d'Alertmanager. Comprova la configuració del webhook.

**Error 3: les alertes s'envien massa**.

Ajusta els llindars i els temps `for: 5m`. Sigues estricte.

## 67.13 Resum

Prometheus + Alertmanager és la combinació de monitoratge avançat més potent per a un homelab. Hem vist:

- Arquitectura completa.
- Instal·lació amb Compose.
- Regles d'alerta bàsiques.
- Integració amb Telegram.
- Mètriques personalitzades.
- Dashboard a Grafana.

## 67.14 Exercicis pràctics

1. Instal·la Prometheus + Alertmanager + Node Exporter + cAdvisor.
2. Verifica que els targets són "UP".
3. Importa el dashboard de Node Exporter (ID 1860).
4. Configura alertes per Telegram.
5. Crea una alerta personalitzada (per exemple, "Node LoRa offline").
6. Força una alerta aturant un servei.
7. Documenta la configuració.
