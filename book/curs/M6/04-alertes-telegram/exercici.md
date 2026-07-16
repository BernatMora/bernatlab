# Exercici practic - Capitol 4: Alertes amb Telegram

> 45-60 min · Real a la teva RPi

## Objectiu

Crear un bot de Telegram, configurar Alertmanager, i afegir regles d'alerta a Prometheus. Acabaras rebent un missatge al movil quan la teva RPi tingui un problema.

## Requisits

- RPi amb Prometheus i Grafana funcionant (capitols 2 i 3)
- Compte de Telegram al movil
- 45-60 minuts

## Pas 1: Crea el bot de Telegram (5 min)

1. Obre Telegram al movil
2. Busca `@BotFather` (verificat amb check blau)
3. Envia `/newbot`
4. Nom del bot: `BernatLab Alerts`
5. Username: `bernatlab_alerts_XXX_bot` (canvia les XXX per algo unic)
6. Guarda el token que et dona (sembla `123456789:ABCdef...`)

Crea un grup anomenat "BernatLab Alertes" i afegeix el bot. Tambe pots simplement afegir el bot al teu xat privat.

## Pas 2: Obte el chat_id (3 min)

Envia qualsevol missatge al grup o al bot. Despres obre al navegador:

```
https://api.telegram.org/bot<EL_TEU_TOKEN>/getUpdates
```

Busca al JSON el camp `chat.id`. Per un grup sera un numero negatiu (per exemple `-123456789`). Guarda'l.

## Pas 3: Instal·la Alertmanager (10 min)

Crea el fitxer de configuracio:

```bash
mkdir -p ~/bernatlab/alertmanager
nano ~/bernatlab/alertmanager/alertmanager.yml
```

Enganxa (substituint el token i el chat_id):

```yaml
global:
  resolve_timeout: 5m

route:
  receiver: 'telegram-bernatlab'
  group_by: ['alertname', 'instance']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h

receivers:
  - name: 'telegram-bernatlab'
    telegram_configs:
      - bot_token: 'POSA_EL_TELEGRAM_BOT_TOKEN_AQUI'
        chat_id: POSA_EL_CHAT_ID_AQUI
        parse_mode: 'Markdown'
        message: |
          🚨 *{{ .GroupLabels.alertname }}*
          {{ .CommonAnnotations.summary }}
          
          *Severitat*: {{ .CommonLabels.severity }}
          *Instancia*: {{ .CommonLabels.instance }}
          *Valor*: {{ $value }}
```

Afegeix al `docker-compose.yml`:

```yaml
  alertmanager:
    image: prom/alertmanager:latest
    container_name: alertmanager
    restart: unless-stopped
    user: "0:0"
    volumes:
      - ./alertmanager/alertmanager.yml:/etc/alertmanager/alertmanager.yml
    command:
      - '--config.file=/etc/alertmanager/alertmanager.yml'
      - '--storage.path=/alertmanager'
    ports:
      - "9093:9093"
```

```bash
cd ~/bernatlab
docker compose up -d alertmanager
```

Accedeix a `http://IP:9093` per veure la UI.

## Pas 4: Crea regles d'alerta a Prometheus (10 min)

```bash
mkdir -p ~/bernatlab/prometheus/rules
nano ~/bernatlab/prometheus/rules/bernatlab.yml
```

```yaml
groups:
  - name: bernatlab_sistema
    interval: 30s
    rules:
      - alert: CPUAlta
        expr: 100 - (avg by(instance)(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "CPU alta a {{ $labels.instance }}"
          description: "CPU al {{ $value }}% durant 5 minuts"

      - alert: MemoriaBaixa
        expr: (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) * 100 < 15
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Memoria baixa a {{ $labels.instance }}"
          description: "Nomes queden {{ $value }}% de memoria"

      - alert: DiscPle
        expr: (node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"}) * 100 < 10
        for: 10m
        labels:
          severity: critical
        annotations:
          summary: "Disc ple a {{ $labels.instance }}"
          description: "Nomes queden {{ $value }}% d'espai"

      - alert: TemperaturaAlta
        expr: node_thermal_zone_temp > 75
        for: 3m
        labels:
          severity: warning
        annotations:
          summary: "Temperatura alta a {{ $labels.instance }}"
          description: "CPU a {{ $value }} graus"

      - alert: RPiDown
        expr: up{job="node"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "RPi no respon"
          description: "Node Exporter no respon desde fa 1 minut"
```

## Pas 5: Activa les regles i Alertmanager a Prometheus (5 min)

Edita `prometheus/prometheus.yml` i afegeix:

```yaml
rule_files:
  - "rules/bernatlab.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets: ['alertmanager:9093']
```

```bash
docker compose restart prometheus
```

Comprova a `http://IP:9090/rules` que les regles s'han carregat.

## Pas 6: Prova que funciona forçant una alerta (15 min)

Crea una alerta artificial fent pujar la CPU:

```bash
# En una terminal SSH
yes > /dev/null &
# Espera 6 minuts
```

Despres de 5 minuts la regla "CPUAlta" hauria de disparar. Comprova:
- A `http://IP:9090/alerts` veuras l'alerta en estat "FIRING"
- A `http://IP:9093` veuras l'alerta agrupada
- Al teu Telegram hauries de rebre el missatge!

Per netejar:

```bash
killall yes
```

L'alerta passara a "RESOLVED" als pocs minuts i rebràs un altre missatge.

## Validacio

Has acabat si:

- [ ] Has creat el bot amb BotFather i tens el token.
- [ ] Alertmanager esta corrent al port 9093.
- [ ] Prometheus carrega les 5 regles del fitxer bernatlab.yml.
- [ ] Has forçat una alerta artificial i has rebut el missatge a Telegram.
- [ ] Has rebut el missatge "Resolved" quan tot torna a la normalitat.
- [ ] Has configurat el teu grup/chat amb el bot.

## Per aprofundir

- Afegeix inhibit rules per silenciar les warning quan hi ha una critica.
- Configura un canal d'email paral·lel per a coses critiques.
- Crea una alerta de "Watchdog" que s'envia cada 24h per confirmar que el sistema funciona.
- Investiga Pushover per alertes critiques amb so fort.
