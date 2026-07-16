# Resum - Capitol 4: Alertes amb Telegram

## La idea clau

Tenir un dashboard bonic no serveix de res si no mires la pantalla. El sistema 24/7 ha de ser PROACTIU: t'ha d'avisar QUAN alguna cosa va malament, no esperar que tu miris. Telegram es perfecte per aixo perque el portem al movil sempre, es gratis, i permet crear bots i grups amb pocs passos.

## Per que Telegram i no altres?

Podriem usar email, SMS, Slack, Discord o webhooks. Telegram es la millor opcio per la RPi casolana perque:

- **Sempre el portem al movil**: l'alerta arriba a la butxatera.
- **Gratis i sense limits**: Telegram no cobra per missatges (fins a 30/segon per bot).
- **API senzilla**: pots enviar un missatge amb una sola crida HTTP.
- **Grups**: pots tenir un grup "BernatLab Alertes" amb tu i la teva parella, on el bot publica.
- **Markdown i botons**: pots enviar missatges rics amb links als dashboards.
- **Sense registre complicat**: nomes cal un numero de telefon.

L'email te el problema que arriba al "Promotions" o "Spam" i no el mires. SMS costa diners. Slack/Discord cal configurar un workspace.

## Anatomia d'una alerta

Una alerta te quatre parts:

1. **Condicio**: QUAN passa alguna cosa. P.ex. "CPU > 80% durant 5 minuts".
2. **Avaluacio**: cada quan es comprova. Cada 30 segons a Alertmanager.
3. **Destinacio**: ON s'envia. Telegram, email, etc.
4. **Missatge**: QUE es diu. Text amb dades de l'incident.

Tambe te cicles de vida:

- **Inactive**: tot be, no s'envia res.
- **Pending**: la condicio es compleix pero encara no ha durat el temps minim.
- **Firing**: la condicio s'ha mantingut prou temps, s'envia l'alerta.
- **Resolved**: la condicio ha tornat a la normalitat, s'envia "recuperat".

## Alertmanager: el carter de Prometheus

Alertmanager es un servei independent que rep les alertes de Prometheus, les agrupa, silencia, i envia al canal que toqui. Es separa de Prometheus per una bona raio: si Prometheus reinicia, Alertmanager recorda quines alertes estan actives i no t'espameja.

```yaml
# Afegeix al docker-compose.yml
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

## Crear el bot de Telegram

1. Obre Telegram i busca `@BotFather`
2. Envia `/newbot`
3. Dona un nom (per exemple "BernatLab Alerts")
4. Dona un username unic (acabant en `bot`, per exemple `bernatlab_alerts_bot`)
5. Rebràs un **token** tipus `1234567890:ABCdef...`. **Guarda'l be!**

Per obtenir el chat_id:

1. Afegeix el bot a un grup nou anomenat "BernatLab Alertes" (o usa el teu xat privat)
2. Envia qualsevol missatge al grup
3. Visita `https://api.telegram.org/bot<TOKEN>/getUpdates` al navegador
4. Busca el `chat.id` (pot ser negatiu per grups, positiu per usuaris)
5. Guarda'l tambe

## Configuracio d'Alertmanager

```yaml
# alertmanager/alertmanager.yml
global:
  resolve_timeout: 5m

route:
  receiver: 'telegram-bernatlab'
  group_by: ['alertname', 'instance']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  routes:
    - match:
        severity: 'critical'
      receiver: 'telegram-bernatlab'
    - match:
        severity: 'warning'
      receiver: 'telegram-bernatlab'

receivers:
  - name: 'telegram-bernatlab'
    telegram_configs:
      - bot_token: 'EL_TELEGRAM_BOT_TOKEN'
        chat_id: EL_CHAT_ID
        parse_mode: 'Markdown'
        message: |
          🚨 *{{ .GroupLabels.alertname }}*
          {{ .CommonAnnotations.summary }}
          
          *Severitat*: {{ .CommonLabels.severity }}
          *Instancia*: {{ .CommonLabels.instance }}
          *Valor*: {{ .CommonAnnotations.value }}
          
          {{ .CommonAnnotations.description }}

inhibit_rules:
  - source_match:
      severity: 'critical'
    target_match:
      severity: 'warning'
    equal: ['alertname', 'instance']
```

La clau `inhibit_rules` fa que si ja hi ha una alerta critica, no t'espameja amb les warning del mateix servei.

## Regles d'alerta a Prometheus

Les regles es defineixen a un fitxer separat i es carreguen desde `prometheus.yml`:

```yaml
# prometheus/rules/bernatlab.yml
groups:
  - name: bernatlab_sistema
    interval: 30s
    rules:
      # CPU alta
      - alert: CPUAlta
        expr: 100 - (avg by(instance)(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "CPU alta a {{ $labels.instance }}"
          description: "CPU al {{ $value }}% durant 5 minuts"
          value: "{{ $value }}%"

      # Memoria baixa
      - alert: MemoriaBaixa
        expr: (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) * 100 < 15
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Memoria baixa a {{ $labels.instance }}"
          description: "Nomes queden {{ $value }}% de memoria"

      # Disc ple
      - alert: DiscPle
        expr: (node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"}) * 100 < 10
        for: 10m
        labels:
          severity: critical
        annotations:
          summary: "Disc ple a {{ $labels.instance }}"
          description: "Nomes queden {{ $value }}% d'espai"

      # Temperatura alta
      - alert: TemperaturaAlta
        expr: node_thermal_zone_temp > 75
        for: 3m
        labels:
          severity: warning
        annotations:
          summary: "Temperatura alta a {{ $labels.instance }}"
          description: "CPU a {{ $value }} graus"

      # RPi no accesible
      - alert: RPiDown
        expr: up{job="node"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "RPi no respon"
          description: "Node Exporter no respon desde fa 1 minut"

      # Contenidor caigut
      - alert: ContenidorCaigut
        expr: absent(container_last_seen{name="homeassistant"})
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Contenidor {{ $labels.name }} no esta corrent"
          description: "El contenidor fa mes de 2 minuts que no reporta"
```

I a `prometheus.yml` afegeix:

```yaml
rule_files:
  - "rules/bernatlab.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets: ['alertmanager:9093']
```

Despres:

```bash
docker compose restart prometheus alertmanager
```

## Bones practiques d'alertes

- **No t'espamegis**: si tens 20 alertes cada hora, acabaras ignorant-les totes. Millor 5 alertes MOLT significatives.
- **Usa `for:`**: la condicio ha d'estar activa un temps minim (5-10 min) abans d'avisar. Evita falses alarmes per pics puntuals.
- **Descripcions utils**: no posis nomes "CPU alta". Posa "CPU al 95% a rpi-bernatlab desde les 14:32".
- **Links als dashboards**: inclou un link al dashboard de Grafana perque amb un click puguis veure el context.
- **Inhibit rules**: si un node esta caigut, no cal avisar de que els seus contenidors tambe.
- **Resolve_timeout**: quan tot torna a la normalitat, s'envia un missatge "Resolved". Sense això no saps si s'ha arreglat.

## Alertes per SMS o telefonada

Per a coses CRITIQUES (incendi, intrusio, pujada de temperatura extrema), pot ser bona idea rebre una telefonada automatica. Eines per fer-ho:

- **Twilio**: API de telefonada/SMS, te un free tier limitat.
- **Alertmanager + twilio**: hi ha integracions no oficials.
- **Grafana + twilio**: tambe es pot fer.
- **Pushover**: app de pagament (5 EUR) que permet notificacions critiques amb so fort.

Aixo nomes per a les 2-3 coses MES importants (la casa esta cremant, la RPi te 50 °C).

## Silenci temporal (silences)

Quan estàs treballant en la RPi i toques coses, no vols rebre alertes constants. Alertmanager permet silenciar temporalment:

1. Accedeix a `http://IP:9093`
2. Clica "New Silence"
3. Tria el match (per exemple, totes les alertes de `instance=rpi-bernatlab`)
4. Posa durada (per exemple, 1 hora)
5. Clica "Create"

Durant aquesta hora no rebras missatges nous pero l'estat segueix guardant-se.

## Connexions amb altres capitols

- **M6 Cap 2** - Prometheus recull les metricas.
- **M6 Cap 3** - Grafana mostra l'estat pero no avisa (alerta proactiva).
- **M6 Cap 6** - Uptime Kuma tambe pot enviar alertes a Telegram directament.
- **M6 Cap 9** - Troubleshooting: quan arriba una alerta, cal saber actuar.
