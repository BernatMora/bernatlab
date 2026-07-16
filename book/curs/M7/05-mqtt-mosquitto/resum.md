# Resum - Capitol 5: MQTT i Mosquitto

## La idea clau

**MQTT** (Message Queuing Telemetry Transport) es un protocol de missatgeria dissenyat el 1999 per Andy Stanford-Clark (IBM) i Arlen Nipper (Eurotech) per connectar sensors de pipelines de petroli via satel·lit. La seva bellesa es la **simplicitat**: nomes 2 tipus de missatges (PUBLISH i SUBSCRIBE), un broker central, i opcionalment QoS. **Mosquitto** es la implementacio de referencia, lleugera i apta per a RPi. A l'Hort Osona, Mosquitto es el cor de l'arquitectura.

## El model publish/subscribe

MQTT funciona amb un patro **pub/sub**. Hi ha dos rols:

- **Publisher** (publicador): envia missatges a un "topic" sense saber qui els llegira.
- **Subscriber** (subscriptor): es connecta al broker i diu "vull rebre tots els missatges del topic X".

El **broker** es l'intermediari que rep tots els missatges dels publishers i els distribueix als subscribers interessats. Es un **hub** central.

```
 Publisher A  --\
                  \
 Publisher B  ------> [ Broker MQTT ] ---> Subscriber X
                  /                       \
 Publisher C  --/                          Subscriber Y
```

Això es diferent del model HTTP client-server. En HTTP, el client **demanava** una pagina; en MQTT, el subscriber **escolta** i el broker **entrega**.

## Anatomia d'un missatge MQTT

Un missatge MQTT te:

- **Topic**: una cadena jerarquica separada per `/`. Ex: `hort-osona/miflora/1B32`.
- **Payload**: les dades, normalment en bytes. Pot ser text (JSON, CSV) o binari.
- **QoS**: nivell de servei (0, 1 o 2).
- **Retain**: boolea. Si es true, el broker guarda l'ultim missatge i l'entrega als nous subscribers.

Exemple de publicacio amb `mosquitto_pub`:

```bash
mosquitto_pub -h localhost -p 1883 -u hort-osona -P secretpass \
   -t "hort-osona/miflora/1B32" \
   -m '{"device":"miflora-1B32","soil_moisture":42,"soil_temp_c":18.5}' \
   -q 1 -r
```

- `-t` = topic
- `-m` = missatge
- `-q 1` = QoS 1 (almenys un cop)
- `-r` = retain (guardar l'ultim missatge)

## Wildcards: com subscriure's a molts topics

MQTT te dos comodins:

- `+` = un sol nivell. `hort-osona/miflora/+` escolta tots els sensors MiFlora.
- `#` = multiples nivells. `hort-osona/#` escolta tot el que penja de l'hort.

Exemple amb `mosquitto_sub`:

```bash
# Escolta tots els missatges
mosquitto_sub -h localhost -t "hort-osona/#" -v

# Escolta nomes MiFlora
mosquitto_sub -h localhost -t "hort-osona/miflora/+"

# Escolta totes les temperatures (BME i MiFlora)
mosquitto_sub -h localhost -t "hort-osona/+/+"
```

La `-v` mostra tambe el topic, util per depurar.

## QoS: els 3 nivells de servei

MQTT defineix 3 nivells de QoS (Quality of Service):

- **QoS 0**: "at most once" - el missatge es lliura una vegada o gens. Es el mes rapid i el que menys ample de banda gast. Usar per a telemetria no critica.
- **QoS 1**: "at least once" - el missatge es garanteix que arriba, pero pot arribar duplicat. Usar per a sensors normals.
- **QoS 2**: "exactly once" - el missatge arriba exactament un cop. Es el mes lent (4 round-trips). Usar nomes per a comandes critiques (e.g. obrir una electrovalvula).

A l'Hort Osona usem **QoS 1** per a la majoria de sensors i **QoS 2** per a comandes de reg.

## Last Will and Testament (LWT)

El LWT es un **missatge que el broker envia automaticament** si el client es desconnecta de forma abrupta. Serveix per saber si un sensor ha mort.

Exemple: el gateway RPi publica a `hort-osona/status/gateway/rpi1` un LWT amb payload `{"status":"offline"}`. Si la RPi cau, el broker publica aquest missatge a tothom que escolti `hort-osona/status/#`.

Això es **molt mes rapid** que fer pings. El broker detecta la caiguda en qüestio de segons (depen del `keepalive`).

```python
client = mqtt.Client("rpi1-gateway")
client.will_set(
    topic="hort-osona/status/gateway/rpi1",
    payload='{"status":"offline"}',
    qos=1,
    retain=True
)
```

## Retain: l'ultim valor esta sempre disponible

Si un publisher envia un missatge amb `retain=True`, el broker el guarda i l'entrega **automaticament** a qualsevol nou subscriber que es connecti al topic. Es com una "cache" de l'ultim valor.

Exemple: el sensor BME280 publica la temperatura actual amb retain. Si la PWA es connecta al broker i subscriu a `hort-osona/bme/hivernacle/temp`, rep immediatament la ultima lectura (no ha d'esperar 5 min al següent enviament).

Aixo es fonamental per a dashboards i visualitzacions reactives.

## Persistencia: missatges per a subscribers offline

Mosquitto te **buffer a disc** (configurable amb `persistence true` i `max_queued_messages`). Si un subscriber esta offline, els missatges nous es guarden i s'entreguen quan torni a connectar.

Limitacio: nomes funciona per a **clients amb sessio persistent** (`clean_session=False`). Si el client te `clean_session=True` (per defecte), no es guarden.

```python
# Sessio persistent: els missatges es guarden offline
client = mqtt.Client("dashboard", clean_session=False)
```

A l'Hort Osona, els dashboards Grafana usen `clean_session=False` per no perdre cap lectura quan es reinicien.

## Seguretat: autenticacio i TLS

Mosquitto te dues capes de seguretat:

1. **Autenticacio per usuari/password**: el mes basic. Es configura amb `password_file`.
2. **TLS/SSL**: encripta el transit i autentica el servidor. Port 8883 en lloc de 1883.

Exemple de configuracio TLS:

```conf
listener 8883
cafile /mosquitto/config/ca.crt
certfile /mosquitto/config/server.crt
keyfile /mosquitto/config/server.key
require_certificate true
```

A l'Hort Osona, **dins** de la xarxa local (192.168.1.x) usem nomes password (TLS es massa overhead per a una RPi). Pero si el broker es accessible des d'internet, **sempre** TLS.

## Comandes utils de mosquitto-clients

Les eines `mosquitto_pub` i `mosquitto_sub` son imprescindibles per depurar:

```bash
# Publicar un missatge de prova
mosquitto_pub -h localhost -p 1883 -u user -P pass \
   -t "test/topic" -m "hola" -q 1

# Subscriure's i veure tot
mosquitto_sub -h localhost -p 1883 -u user -P pass \
   -t "#" -v

# Subscriure's amb un missatge de benvinguda
mosquitto_sub -h localhost -t "test/topic" -v -W 30

# Publicar un missatge amb retain
mosquitto_pub -h localhost -t "status/hort" -m "OK" -r

# Llegir un missatge unic (no sub mode)
mosquitto_sub -h localhost -t "test/+" -C 1
```

## Instal·lacio de Mosquitto

A la RPi:

```bash
sudo apt update
sudo apt install mosquitto mosquitto-clients
sudo systemctl enable mosquitto
sudo systemctl start mosquitto
```

Crear un usuari:

```bash
sudo mosquitto_passwd -c /etc/mosquitto/passwd hort-osona
# Introdueix password dos cops
```

Configurar `/etc/mosquitto/mosquitto.conf`:

```conf
persistence true
persistence_location /var/lib/mosquitto/
log_dest file /var/log/mosquitto/mosquitto.log
listener 1883
allow_anonymous false
password_file /etc/mosquitto/passwd
```

Pero a l'Hort Osona, **preferim Docker** per facilitat de gestio (imatge oficial `eclipse-mosquitto:2`).

## Per que Mosquitto i no altres brokers

Alternatives a Mosquitto:

- **EMQX**: mes potent (milions de connexions), escrit en Erlang. Per a IoT industrial.
- **HiveMQ**: comercial, amb clustering i alta disponibilitat.
- **VerneMQ**: similar a EMQX, open source.
- **AWS IoT Core / Azure IoT Hub**: al núvol, cobren per missatge.
- **Home Assistant MQTT**: integracio especifica per a HA.

A l'Hort Osona usem **Mosquitto** perque:
- Es lleuger (unes 30 MB de RAM).
- Es estable i madur.
- Te bona documentacio.
- Es oficialment a l'Eclipse Foundation.
- Funciona perfecte amb Docker.

Si volguem escenar a 10.000 sensors o tenir alta disponibilitat, canviariem a EMQX. Per a un hort petit, Mosquitto es perfecte.

## Connexions amb altres capitols

- **M7 Cap 4** - L'arquitectura completa on MQTT es el bus central.
- **M7 Cap 6** - InfluxDB reb les dades via MQTT.
- **M7 Cap 7** - L'API també pot rebre missatges MQTT per actualitzar Redis.
- **M7 Cap 10** - Cas real: alerta de gelada basada en QoS 1.
