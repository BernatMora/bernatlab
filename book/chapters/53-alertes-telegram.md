# Capítol 53 — Alertes intel·ligents amb Grafana i Telegram

> *"Una alerta que no actues és soroll. Una alerta que arriba quan toca, al canal adequat, és or."*

## 53.1 Què és una alerta útil

Una alerta útil té quatre propietats:

1. **Rellevant**: avisa d'un problema real, no d'una molèstia.
2. **Accionable**: saps què fer quan la reps.
3. **Puntual**: arriba quan toca, no més tard ni massa aviat.
4. **Al canal correcte**: crítiques a Telegram immediatament, informatives al correu en horari laboral.

Si una alerta no té aquestes quatre propietats, és soroll.

## 53.2 Tipus d'alertes

### Alertes de disponibilitat

- Un servei està caigut.
- Un contenidor ha deixat de respondre.
- La Raspberry no és accessible per SSH.

### Alertes de rendiment

- La CPU porta més de 30 minuts al 90%.
- El disc s'omplirà en menys de 24 h.
- La memòria lliure és inferior al 10%.

### Alertes de seguretat

- Més de 10 intents SSH fallits en 5 min.
- Un usuari ha accedit des d'una IP nova.
- Una alerta de fail2ban s'ha activat.

### Alertes de dades

- Un node LoRa no ha enviat dades en més d'1 hora.
- La còpia de seguretat no s'ha fet.
- InfluxDB té errors de consulta.

## 53.3 Alertmanager: el cervell de les alertes

**Alertmanager** (integrat a Prometheus) gestiona les alertes:

1. **Rep** les alertes de Prometheus.
2. **Agrupa** alertes relacionades.
3. **Silencia** alertes que saps que estan passant.
4. **Enruta** a canals diferents segons la severitat.
5. **Inhibeix** alertes que són conseqüència d'altres.

Configuració bàsica a `~/homelab/compose/prometheus/alertmanager.yml`:

```yaml
global:
  resolve_timeout: 5m

route:
  group_by: ['alertname', 'instance']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  receiver: 'telegram-critiques'
  routes:
    - match:
        severity: critical
      receiver: 'telegram-critiques'
    - match:
        severity: warning
      receiver: 'telegram-avís'

receivers:
  - name: 'telegram-critiques'
    webhook_configs:
      - url: 'http://alertmanager-webhook:8080/alerts/critical'

  - name: 'telegram-avís'
    webhook_configs:
      - url: 'http://alertmanager-webhook:8080/alerts/warning'

inhibit_rules:
  - source_match:
      severity: critical
    target_match:
      severity: warning
    equal: ['alertname', 'instance']
```

Afegeix Alertmanager al compose:

```yaml
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
    networks:
      - monitoring
```

## 53.4 Regles d'alerta a Prometheus

Crea `~/homelab/compose/prometheus/rules.yml`:

```yaml
groups:
  - name: bernatlab
    interval: 30s
    rules:
      # CPU alta durant 5 minuts
      - alert: HighCPUUsage
        expr: 100 - (avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 90
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "CPU alta a {{ $labels.instance }}"
          description: "CPU al {{ $value }}% durant més de 5 minuts."

      # RAM baixa
      - alert: LowMemory
        expr: (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) * 100 < 10
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "RAM baixa a {{ $labels.instance }}"
          description: "Només queda {{ $value }}% de RAM lliure."

      # Disc gairebé ple
      - alert: DiskFull
        expr: (node_filesystem_avail_bytes{fstype!="tmpfs"} / node_filesystem_size_bytes) * 100 < 10
        for: 10m
        labels:
          severity: critical
        annotations:
          summary: "Disc ple a {{ $labels.instance }}"
          description: "Només queda {{ $value }}% d'espai lliure."

      # Servei caigut (ping)
      - alert: ServiceDown
        expr: up{job="bernatlab-services"} == 0
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Servei {{ $labels.instance }} caigut"
          description: "El servei no respon a ping des de fa 2 minuts."

      # Temperatura alta
      - alert: HighTemperature
        expr: node_thermal_zone_temp > 75
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Temperatura alta: {{ $value }}°C"
          description: "La Raspberry està a {{ $value }}°C, considera netejar-la o millorar la ventilació."
```

Carrega les regles a `prometheus.yml`:

```yaml
rule_files:
  - "rules.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets: ['alertmanager:9093']
```

## 53.5 Crear el bot de Telegram

Per enviar alertes a Telegram:

1. Obre Telegram i parla amb **@BotFather**.
2. Envia `/newbot` i segueix les instruccions.
3. Guarda el **token** que et dóna (exemple: `1234567890:ABCdefGHI...`).
4. Crea un grup on el bot i tu sigueu membres.
5. Afegeix el bot al grup.
6. Obtenir el **chat_id** del grup: visita `https://api.telegram.org/bot<TOKEN>/getUpdates` i mira el `chat.id`.

## 53.6 Servei de webhook a Telegram

Crea un petit servei que rebi alertes d'Alertmanager i les enviï a Telegram. Crea `~/homelab/compose/alert-webhook/`:

**app.py**:

```python
import os
import json
import requests
from flask import Flask, request

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    })

@app.route("/alerts/critical", methods=["POST"])
def critical():
    data = request.json
    for alert in data.get("alerts", []):
        status = alert.get("status", "unknown")
        if status == "resolved":
            emoji = "✅"
            text = "RESOLT"
        else:
            emoji = "🔴"
            text = "ALERTA CRÍTICA"
        summary = alert.get("annotations", {}).get("summary", "Sense resum")
        description = alert.get("annotations", {}).get("description", "")
        message = f"{emoji} <b>{text}</b>\n\n{summary}\n{description}"
        send_telegram(message)
    return "OK", 200

@app.route("/alerts/warning", methods=["POST"])
def warning():
    data = request.json
    for alert in data.get("alerts", []):
        status = alert.get("status", "unknown")
        if status == "resolved":
            emoji = "✅"
            text = "RESOLT"
        else:
            emoji = "⚠️"
            text = "AVÍS"
        summary = alert.get("annotations", {}).get("summary", "")
        message = f"{emoji} <b>{text}</b>\n\n{summary}"
        send_telegram(message)
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
```

**Dockerfile**:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
RUN pip install flask requests gunicorn
COPY app.py .
CMD ["gunicorn", "-b", "0.0.0.0:8080", "-w", "2", "app:app"]
```

**requirements.txt**:

```
flask==3.0.0
requests==2.31.0
gunicorn==21.2.0
```

Crea `.env` (afegit a `.gitignore`):

```
TELEGRAM_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=-1001234567890
```

I actualitza el compose:

```yaml
  alertmanager-webhook:
    build: ./alert-webhook
    container_name: alertmanager-webhook
    restart: unless-stopped
    env_file:
      - ./alert-webhook/.env
    networks:
      - monitoring
```

## 53.7 Provar les alertes

Per forçar una alerta de prova:

1. Apaga un contenidor temporalment:

```bash
docker stop grafana
```

2. Espera 2-3 minuts.

3. Hauries de rebre una alerta a Telegram: "Servei caigut: grafana".

4. Torna a engegar:

```bash
docker start grafana
```

5. Rebràs una alerta "RESOLT".

## 53.8 Alertes intel·ligents

Algunes alertes són molt específiques i útils:

### Alerta: node LoRa no ha enviat dades en 1h

```yaml
- alert: LoRaNodeOffline
  expr: time() - max(temperature_last_seen{node="hort1"}) > 3600
  for: 10m
  labels:
    severity: warning
  annotations:
    summary: "Node LoRa hort1 sense dades des de fa 1h"
    description: "Comprova la bateria o la cobertura."
```

### Alerta: còpia de seguretat no s'ha fet

Pots usar Pushgateway per exposar l'edat de l'última còpia:

```bash
# Script que actualitza la mètrica
AGE=$(stat -c %Y /var/lib/bernatlab-backups/latest)
NOW=$(date +%s)
HOURS=$(( (NOW - AGE) / 3600 ))
echo "bernatlab_backup_age_hours $HOURS" | curl --data-binary @- \
    http://localhost:9091/metrics/job/backup
```

I la regla:

```yaml
- alert: BackupStale
  expr: bernatlab_backup_age_hours > 26
  for: 1h
  labels:
    severity: warning
  annotations:
    summary: "Còpia antiga: {{ $value }} hores"
```

### Alerta: certificat a punt de caducar

```yaml
- alert: CertificateExpiring
  expr: (ssl_cert_not_after - time()) / 86400 < 14
  for: 1h
  labels:
    severity: warning
  annotations:
    summary: "Certificat expira en menys de 14 dies"
```

Cal un exporter com **blackbox_exporter** o **ssl_exporter**.

## 53.9 Silenciació temporal

Quan saps que una cosa pot fallar (manteniment programat, canvis), pots silenciar alertes:

```bash
# Via amtool
amtool silence add --alertmanager=http://localhost:9093 \
    --comment="Manteniment programat" \
    --duration=2h \
    --match-label=alertname=HighCPUUsage
```

O via interfície web d'Alertmanager: http://localhost:9093.

## 53.10 Evitar el soroll

Si reps masses alertes, ajusta:

- **for**: augmenta el temps (per exemple, de 5m a 15m).
- **threshold**: ajusta el llindar (per exemple, de 90% a 95%).
- **group_by**: agrupa alertes relacionades.
- **repeat_interval**: augmenta l'interval de repetició.

## 53.11 Errors habituals

**Error 1: alertes que ningú llegeix**.

Si tens 50 alertes al dia, deixaràs de mirar-les. Sigues estricte amb què mereix una alerta.

**Error 2: alertes que es disparen massa**.

Si una alerta es dispara cada hora, no és útil. Ajusta el llindar.

**Error 3: no provar les alertes**.

Si no has provat mai l'alerta, no saps si funciona. Prova-les periòdicament.

**Error 4: no documentar què fer**.

Cada alerta hauria d'incloure què fer. Un runbook enllaçat a l'anotació.

## 53.12 Bones pràctiques

1. **Meningi's per cada alerta**: quina acció prendré?
2. **Severitat clara**: critical, warning, info.
3. **Anotacions útils**: resum + descripció + enllaç al runbook.
4. **Provar-les periòdicament**: força una alerta cada mes.
5. **Ajustar el soroll**: si una alerta no és útil, ajusta-la o elimina-la.
6. **Tenir un canal de "tot OK"**: rebre resolucions és igual d'útil que rebre alertes.

## 53.13 Resum

Les alertes són la part més important del monitoratge: t'avis quan alguna cosa va malament. Alertmanager + Telegram és una combinació potent i gratuïta. La clau és evitar el soroll i mantenir alertes accionables. Al proper capítol veurem els scripts de manteniment i actualitzacions.

## 53.14 Exercicis pràctics

1. Crea un bot de Telegram i obté el token.
2. Desplega Alertmanager i el servei de webhook.
3. Configura 5 regles d'alerta a Prometheus.
4. Prova les alertes aturant un servei.
5. Afegeix una alerta específica del teu cas (sensor, còpia, certificat).
6. Configura un silenci per a manteniment.
7. Documenta al README les alertes configurades.
