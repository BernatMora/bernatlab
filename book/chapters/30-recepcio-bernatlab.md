# Capítol 30 — Recepció al BernatLab: de TTN a InfluxDB

> *"El node ha transmès, el gateway ha escoltat, TTN ha desxifrat. Ara falta la part que ens interessa: que les dades aterrin al Grafana i a la web."*

## 30.1 El pipeline complet

Quan un node LoRaWAN transmet, les dades fan el següent camí:

```
[NODES]  ──── LoRa 868 MHz ────►  [GATEWAY]  ── Internet ──►  [TTN]  ── MQTT ──►  [Mosquitto]
                                                                                       │
                                                                                       ▼
                                                                                  [Telegraf]
                                                                                       │
                                                                                       ▼
                                                                                  [InfluxDB]
                                                                                       │
                                                                                       ▼
                                                                                  [Grafana]
                                                                                       │
                                                                                       ▼
                                                                               [Web Hort Osona]
                                                                                  (via API)
```

Aquest pipeline ja el coneixem del Mòdul 2, però ara veurem els detalls específics per a dades LoRa.

## 30.2 El que rep Mosquitto

Quan TTN ha desxifrat el payload d'un node, el publica al broker MQTT. El missatge té aquesta estructura JSON:

```json
{
  "end_device_ids": {
    "device_id": "eui-70b3d57ed004f1ce",
    "application_ids": {
      "application_id": "hort-osona-bernat"
    },
    "dev_eui": "70B3D57ED004F1CE",
    "join_eui": "0000000000000000"
  },
  "received_at": "2026-07-08T12:34:56.789Z",
  "uplink_message": {
    "f_port": 2,
    "f_cnt": 42,
    "frm_payload": "GAEABbYBmAu4",
    "decoded_payload": {
      "temperatura": 25.5,
      "humitat": 91,
      "pressio": 1013
    },
    "rx_metadata": [{
      "gateway_ids": {
        "gateway_id": "raspi-hortosona-gw"
      },
      "rssi": -67,
      "snr": 9.5
    }],
    "settings": {
      "data_rate": {
        "lora": {
          "bandwidth": 125000,
          "spreading_factor": 9
        }
      },
      "frequency": "868100000"
    }
  }
}
```

Com veiem, **el payload decodificat ja ve en JSON** (gràcies al payload formatter que hem configurat a TTN). També tenim metadades útils: RSSI, SNR, data rate, etc.

## 30.3 Subscriure's manualment per veure-ho

Per veure els missatges en directe, ens podem subscriure al broker:

```bash
mosquitto_sub -h 100.115.134.76 -t "v3/#" -v -u bernat -P CONTRASENYA
```

Això ensenya tots els missatges que arriben. Si veiem alguna cosa, vol dir que TTN s'està connectant correctament al nostre broker.

## 30.4 Configurar Telegraf per rebre dades LoRa

Ara ve la part interessant: configurar Telegraf perquè consumeixi els missatges de TTN i els escrigui a InfluxDB.

A `/home/bernat/homelab/compose/iot/telegraf.conf`:

```toml
[agent]
  interval = "30s"
  flush_interval = "30s"

# Input: escoltem MQTT per missatges de TTN
[[inputs.mqtt_consumer]]
  servers = ["tcp://mosquitto:1883"]
  username = "telegraf"
  password = "${MQTT_PASSWORD}"
  client_id = "telegraf-ttn-bridge"
  topics = ["v3/+/@/devices/+/up"]
  data_format = "json"
  json_time_key = "received_at"
  json_time_format = "2006-01-02T15:04:05Z"
  tag_keys = ["device_id", "application_id", "dev_eui"]

  # Tag a partir d'una ruta JSON: el data rate i el SF
  [[inputs.mqtt_consumer.json_fields]]
    path = "uplink_message.settings.data_rate.lora.spreading_factor"
    name = "spreading_factor"
    type = "integer"
  [[inputs.mqtt_consumer.json_fields]]
    path = "uplink_message.settings.data_rate.lora.bandwidth"
    name = "bandwidth"
    type = "integer"
  [[inputs.mqtt_consumer.json_fields]]
    path = "uplink_message.rx_metadata[0].rssi"
    name = "rssi"
    type = "integer"
  [[inputs.mqtt_consumer.json_fields]]
    path = "uplink_message.rx_metadata[0].snr"
    name = "snr"
    type = "float"
  [[inputs.mqtt_consumer.json_fields]]
    path = "uplink_message.f_cnt"
    name = "fcnt"
    type = "integer"

  # Camps de la payload (cayenne LPP ja desxifrat per TTN)
  [[inputs.mqtt_consumer.json_fields]]
    path = "uplink_message.decoded_payload.temperatura"
    name = "temperatura"
    type = "float"
  [[inputs.mqtt_consumer.json_fields]]
    path = "uplink_message.decoded_payload.humitat"
    name = "humitat"
    type = "float"
  [[inputs.mqtt_consumer.json_fields]]
    path = "uplink_message.decoded_payload.pressio"
    name = "pressio"
    type = "float"
  [[inputs.mqtt_consumer.json_fields]]
    path = "uplink_message.decoded_payload.humitat_sol"
    name = "humitat_sol"
    type = "float"
  [[inputs.mqtt_consumer.json_fields]]
    path = "uplink_message.decoded_payload.lux"
    name = "lux"
    type = "integer"
  [[inputs.mqtt_consumer.json_fields]]
    path = "uplink_message.decoded_payload.voltatge_bateria"
    name = "voltatge_bateria"
    type = "float"

# Output: InfluxDB v2
[[outputs.influxdb_v2]]
  urls = ["http://influxdb:8086"]
  token = "${INFLUX_TOKEN}"
  org = "bernatlab"
  bucket = "hort-osona"
  timeout = "10s"
  content_encoding = "gzip"
  # Mesura comuna per a tots els punts
  measurement = "sensor_lora"
```

Aquesta configuració:

- Escolta tots els missatges de TTN (`v3/+/@/devices/+/up`).
- Extreu els tags: device_id, application_id, dev_eui.
- Extreu les metadades: SF, BW, RSSI, SNR, frame counter.
- Extreu les dades: temperatura, humitat, pressió, etc.
- Usa el temps de `received_at` de TTN com a timestamp.
- Escriu a InfluxDB al bucket `hort-osona`, amb mesura `sensor_lora`.

## 30.5 Verificar que Telegraf rep dades

Podem mirar els logs:

```bash
docker compose logs -f telegraf
```

Si tot funciona, veurem línies com:

```
2026-07-08T12:34:56Z I! Loaded inputs: mqtt_consumer
2026-07-08T12:34:56Z I! Loaded outputs: influxdb_v2
2026-07-08T12:34:56Z I! [agent] Start: agent started
```

I quan arribi una transmissió, veurem l'escriptura a InfluxDB.

També podem consultar directament a InfluxDB:

```bash
influx query '
from(bucket: "hort-osona")
  |> range(start: -1h)
  |> filter(fn: (r) => r._measurement == "sensor_lora")
  |> filter(fn: (r) => r._field == "temperatura")
' --org bernatlab --token TOKEN
```

Si veiem dades, tot funciona.

## 30.6 Configurar Grafana

A Grafana (que ja tenim configurat al M2), creem o importem un dashboard específic per a sensors LoRa.

Un dashboard bàsic tindria:

1. **Panell "Temperatura per zona"**: gràfica de línies, últimes 24 h.
2. **Panell "Humitat per zona"**: similar.
3. **Panell "Humitat del sòl"**: gràfica específica.
4. **Panell "RSSI / SNR"**: gràfiques de qualitat del senyal.
5. **Panell "Bateria"**: gràfica del voltatge de la bateria.
6. **Panell "Estat del node"**: taula amb l'últim valor, RSSI, SNR, etc.
7. **Alerta visual**: si la temperatura baixa de 2 °C, el panell es posa vermell.

Crear el dashboard és similar al que vam fer al Mòdul 2 (Capítol 19). Aquí només afegim les dades específiques de LoRa.

## 30.7 Alertes amb Grafana

A més de les alertes visuals, podem configurar alertes reals:

- **Temperatura massa baixa** (gelada imminent): alerta per Telegram.
- **Bateria baixa**: alerta per Telegram.
- **Node inactiu**: si no hem rebut cap uplink en 30 minuts, alerta.
- **RSSI massa baix**: indica que alguna cosa ha canviat al camp.

Aquestes alertes les creem a Grafana → Alerting → Alert rules.

## 30.8 Configurar Node-RED per processar

A Node-RED, podem afegir fluxos específics per a LoRa:

- **Flux 1: filtre de qualitat**. Si RSSI < -110 dBm, alerta.
- **Flux 2: detecció de gelada**. Si temperatura < 2 °C, alerta per Telegram.
- **Flux 3: reg automàtic**. Si humitat del sòl < 30 % durant 30 min, enviar comanda a la vàlvula de reg.
- **Flux 4: resum diari**. Cada matí, enviar un resum a Telegram amb les últimes lectures.

Ja tenim Node-RED instal·lat (M2, Capítol 17), només cal afegir els fluxos nous.

## 30.9 Exemple de flux Node-RED per alerta de gelada

Un flux senzill a Node-RED que escolta els missatges de TTN i alerta si la temperatura baixa de 2 °C:

1. **Node `mqtt in`**: subscriu a `v3/+/@/devices/+/up`.
2. **Node `function`**: filtra els missatges amb temperatura < 2 °C.
3. **Node `telegram sender`**: envia l'alerta.

Codi del node function:

```javascript
// Filtrar missatges amb temperatura baixa
const payload = msg.payload;

if (!payload.uplink_message || !payload.uplink_message.decoded_payload) {
    return null;
}

const temp = payload.uplink_message.decoded_payload.temperatura;
if (typeof temp !== 'number' || temp >= 2) {
    return null;
}

const deviceId = payload.end_device_ids.device_id;
const rssi = payload.uplink_message.rx_metadata[0]?.rssi || 'N/A';

msg.payload = `❄️ ALERTA GELADA\n\nNode: ${deviceId}\nTemperatura: ${temp}°C\nRSSI: ${rssi} dBm\nHora: ${new Date().toISOString()}`;
return msg;
```

Aquest flux ja s'encarrega de la detecció i l'alerta.

## 30.10 Publicar a la web Hort Osona

Per integrar les dades LoRa a la web pública, l'API FastAPI (M2, Capítol 20) ja està preparada. Només cal afegir endpoints específics per a sensors LoRa:

```python
@router.get("/lora/zones", response_model=list[str])
def llistar_zones_lora():
    """Llista les zones (devices) amb sensors LoRa actius."""
    query = '''
    import "influxdata/influxdb/schema"
    schema.tagValues(bucket: "hort-osona", tag: "device_id")
    '''
    result = query_api.query(query)
    return [table.values[0] for table in result]


@router.get("/lora/{device_id}/latest")
def ultimes_dades_lora(device_id: str):
    """Retorna les últimes dades d'un sensor LoRa."""
    query = f'''
    from(bucket: "hort-osona")
      |> range(start: -1h)
      |> filter(fn: (r) => r._measurement == "sensor_lora")
      |> filter(fn: (r) => r.device_id == "{device_id}")
      |> last()
    '''
    # ... processar el resultat i retornar JSON
```

La web Hort Osona pot consumir aquests endpoints per mostrar dades en temps quasi-real.

## 30.11 Còpies de seguretat de les dades LoRa

Les dades dels sensors LoRa són valuoses (representen mesos d'observació). Per tant, cal fer-ne còpia de seguretat:

- **InfluxDB**: la còpia regular d'InfluxDB (M2, Capítol 22) ja inclou aquestes dades.
- **TTN**: TTN ja en té còpia al núvol (gratuït).
- **Local**: podem exportar les dades periòdicament amb una tasca programada.

## 30.12 Monitoratge del pipeline complet

Per saber que tot funciona, monitorarem:

1. **Concentratord**: monitor HTTP al port 3001 (M3, Capítol 27).
2. **Mosquitto**: monitor TCP al port 1883 (M2, Capítol 13).
3. **Telegraf**: monitor HTTP al port 8086 (no té interfície web, però podem fer un `docker ps`).
4. **InfluxDB**: monitor HTTP al port 8086 (amb `/health`).
5. **Grafana**: monitor HTTP al port 3000.

A Uptime Kuma, afegim tots aquests monitors. Si algun falla, alerta per Telegram.

## 30.13 Proves d'integració

Quan tot estigui en marxa, validarem el pipeline amb una prova end-to-end:

1. **Node transmet**: veure al log del node "Packet transmitted".
2. **Gateway rep**: veure a la consola de TTN l'uplink.
3. **TTN publica a MQTT**: veure el missatge amb `mosquitto_sub`.
4. **Telegraf escriu a InfluxDB**: veure la dada amb `influx query`.
5. **Grafana mostra**: veure la gràfica actualitzada.
6. **Web pública**: veure la dada al frontend d'Hort Osona.
7. **Node-RED alerta**: si la temperatura és baixa, rebre un missatge a Telegram.

Si tot això funciona, tenim el pipeline complet.

## 30.14 Resum

En aquest capítol hem après a connectar el pipeline LoRa amb la resta del BernatLab. Hem vist com configurar Telegraf per rebre els missatges de TTN via MQTT, com guardar les dades a InfluxDB, com visualitzar-les a Grafana, com processar-les amb Node-RED, i com exposar-les a través de l'API per a la web pública. Hem après a monitorar tot el pipeline amb Uptime Kuma. En el proper capítol veurem el cas alternatiu: LoRa P2P amb SX1262, sense LoRaWAN ni TTN, útil per a un sol node o per a xarxes privades.

## 30.15 Exercicis pràctics

1. Desplega la nova configuració de Telegraf per rebre dades de TTN.
2. Configura el payload formatter CayenneLPP a la consola de TTN.
3. Configura la integració MQTT a TTN apuntant al broker del BernatLab.
4. Verifica que les dades arriben a InfluxDB amb `influx query`.
5. Crea un panell a Grafana per visualitzar la temperatura d'un node.
6. Crea una alerta de Grafana per temperatura baixa.
7. Afegeix un flux a Node-RED que processi les dades LoRa.
8. Afegeix un monitor a Uptime Kuma per al gateway LoRa.
9. Documenta al README el pipeline complet amb un esquema.

Paraules clau: **TTN, The Things Stack, MQTT, Mosquitto, Telegraf, InfluxDB, Grafana, Node-RED, FastAPI, API, web pública, CayenneLPP, payload formatter, decoder, telemetry, uplink, downlink, RSSI, SNR, frame counter, FCnt, FPort, data rate, spreading factor, bandwidth, time on air, EU868, frequency plan, channels, duty cycle, ADR, device EUI, application EUI, join, OTAA, ABP, session, dev nonce, join nonce, XSS, integració, broker, Mosquitto, publicador, subscriptor, wildcard, v3/, application_id, device_id, end device, application, gateway, concentratord, packet forwarder, server address, EU1, NAM1, AU1, AS923, US915, region, RSSI, SNR, signal quality, monitoring, alerting, Uptime Kuma, Telegram, alert rules, dashboard, panel, gauge, time series, bar chart, table, threshold, alert visual, alert real, contact point, alert evaluation, alert manager, Prometheus, alertmanager, InfluxDB, line protocol, bucket, org, retention, schema, measurements, tags, fields, time series database, TSDB, continuous query, task, aggregate, mean, max, min, last, range filter, tag filter, field filter, group by, window, windowPeriod, timeRangeStart, timeRangeStop, query, InfluxQL, Flux, query builder, Data Explorer, task scheduler, cron, InfluxDB API, InfluxDB CLI, influx command, influx query, influx write, influx bucket, influx auth, influx task, backup, restore, retention policy, downsampling, performance, index, TSI, time series index, cardinality, series cardinality, tag cardinality, series limit, query performance, Flux performance, query optimization, predicate pushdown, predicate, pushdown, caching, query cache, partition, shard, shard duration, shard group, retention enforcement, drop, series, expired series, series expiry, query history, query log, debug, info, error, warning, structured logging, JSON logging, log destination, stderr, stdout, file, syslog, journald, network, log shipping, Loki, Grafana Loki, log aggregation, log query, logQL, alerts, recording rules, alert rules, hot, warm, cold, tier, storage, S3, GCS, Azure, local, disk, memory, RAM, heap, OOM, out of memory, garbage collection, GC, performance, latency, throughput, write throughput, read throughput, queries per second, points per second, series per second, ingestion, ingestion rate, cardinality budget, cardinality, tag values, tag keys, schema, schema exploration, schema management, schema design, tag design, field design, data model, time series data model, time series best practices, naming conventions, tag naming, field naming, measurement naming, bucket naming, retention, downsampling, aggregation, continuous query, Flux task, scheduled task, cron task, InfluxDB tasks, task runs, task history, task options, task configuration, task management, task monitoring, task alerts**.
