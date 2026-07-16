# Exercici practic - Capitol 5: MQTT i Mosquitto

> 30-45 min · Real a la RPi

## Objectiu

Muntar Mosquitto amb Docker, crear usuaris, practicar publicacio i subscripcio amb les eines `mosquitto_pub`/`mosquitto_sub`, i fer una aplicacio Python que publiqui i escolti amb QoS 1 i LWT.

## Requisits

- RPi amb Docker
- Python 3.10+
- 30-45 min

## Pas 1: Inicia Mosquitto amb Docker (5 min)

```bash
mkdir -p ~/hort-osona/mosquitto/{config,data,log}
cd ~/hort-osona/mosquitto

# Crea un password file amb dos usuaris
docker run --rm -it eclipse-mosquitto:2 \
   sh -c "mosquitto_passwd -c -b /tmp/passwd hort-osona secretpass && \
          mosquitto_passwd -b /tmp/passwd gateway gwpassword && \
          cat /tmp/passwd" > config/passwd
```

Crea `config/mosquitto.conf`:

```conf
persistence true
persistence_location /mosquitto/data/
log_dest stdout
log_type error
log_type warning
log_type notice

listener 1883
allow_anonymous false
password_file /mosquitto/config/passwd
```

Aixeca el contenidor:

```bash
cd ~/hort-osona
docker run -d --name hort-mosquitto \
   -p 1883:1883 \
   -v $PWD/mosquitto/config:/mosquitto/config \
   -v $PWD/mosquitto/data:/mosquitto/data \
   eclipse-mosquitto:2

docker logs hort-mosquitto
```

## Pas 2: Primer test amb mosquitto_pub/sub (5 min)

En una terminal, subscriu-te a tot:

```bash
mosquitto_sub -h localhost -p 1883 -u hort-osona -P secretpass \
   -t "hort-osona/#" -v
```

En una altra terminal, publica:

```bash
mosquitto_pub -h localhost -p 1883 -u hort-osona -P secretpass \
   -t "hort-osona/test/salutacio" \
   -m "Hola des del terminal!"
```

Hauries de veure el missatge a la primera terminal:

```
hort-osona/test/salutacio Hola des del terminal!
```

## Pas 3: Practica wildcards (5 min)

En una terminal:

```bash
mosquitto_sub -h localhost -p 1883 -u hort-osona -P secretpass \
   -t "hort-osona/miflora/+" -v
```

Publica uns quants missatges:

```bash
# Aquest l'hauries de veure
mosquitto_pub -h localhost -p 1883 -u hort-osona -P secretpass \
   -t "hort-osona/miflora/1B32" \
   -m '{"device":"miflora-1B32","soil_moisture":42}'

# Aquest NO l'hauries de veure (no comenca per hort-osona/miflora/)
mosquitto_pub -h localhost -p 1883 -u hort-osona -P secretpass \
   -t "hort-osona/bme/hivernacle" \
   -m '{"temp_c":25.0}'

# Aquest NO l'hauries de veure (te dos nivells)
mosquitto_pub -h localhost -p 1883 -u hort-osona -P secretpass \
   -t "hort-osona/miflora/1B32/extra" \
   -m "extra"
```

## Pas 4: Practica retain (5 min)

Publica un missatge amb retain:

```bash
mosquitto_pub -h localhost -p 1883 -u hort-osona -P secretpass \
   -t "hort-osona/status/hort" -m "OK" -r
```

Ara subscriu-te (encara que el missatge s'hagi publicat fa estona):

```bash
mosquitto_sub -h localhost -p 1883 -u hort-osona -P secretpass \
   -t "hort-osona/status/hort" -C 1 -v
# Hauries de rebre "OK" immediatament!
```

Aixo es molt util per a dashboards que volen l'ultim valor al connectar.

## Pas 5: Aplica Python amb QoS 1 i LWT (15 min)

Crea `~/hort-osona/scripts/test_mqtt.py`:

```python
#!/usr/bin/env python3
"""Client MQTT amb QoS 1, LWT i sessio persistent."""

import json
import time
import random
import logging
import signal
import sys
import paho.mqtt.client as mqtt

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s')
log = logging.getLogger(__name__)

BROKER = "localhost"
PORT = 1883
USER = "gateway"
PASS = "gwpassword"
CLIENT_ID = "test-gateway-01"

# Callbacks
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        log.info("Connectat al broker")
        # Subscriure a comandes
        client.subscribe("hort-osona/cmd/#", qos=1)
    else:
        log.error(f"Error connectant: rc={rc}")

def on_message(client, userdata, msg):
    log.info(f"Rebut [{msg.topic}] QoS={msg.qos} {msg.payload}")

def on_disconnect(client, userdata, rc):
    if rc != 0:
        log.warning(f"Desconnectat inesperadament: rc={rc}")

# Crea client
client = mqtt.Client(CLIENT_ID, clean_session=False)

# LWT: si el client cau, el broker publica aixo
client.will_set(
    topic=f"hort-osona/status/gateway/{CLIENT_ID}",
    payload=json.dumps({"status": "offline", "ts": time.time()}),
    qos=1,
    retain=True
)

client.username_pw_set(USER, PASS)
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

# Conecta
client.connect(BROKER, PORT, keepalive=60)
client.loop_start()

# Publica heartbeat cada 5 segons
try:
    for i in range(12):
        data = {
            "device": CLIENT_ID,
            "ts": time.time(),
            "soil_moisture": random.randint(30, 60),
            "soil_temp_c": round(15 + random.random() * 5, 1)
        }
        topic = f"hort-osona/miflora/{CLIENT_ID}"
        # Publica amb QoS 1 i retain
        info = client.publish(topic, json.dumps(data), qos=1, retain=True)
        info.wait_for_publish()
        log.info(f"Publicat #{i}: {data}")
        time.sleep(5)
except KeyboardInterrupt:
    log.info("Aturat per l'usuari")

# Publica LWT manual al desconnectar
client.publish(
    f"hort-osona/status/gateway/{CLIENT_ID}",
    json.dumps({"status": "intentional-disconnect"}),
    qos=1, retain=True
)
client.loop_stop()
client.disconnect()
```

Executa'l:

```bash
pip install paho-mqtt
python3 test_mqtt.py
```

En una altra terminal, subscriu-te:

```bash
mosquitto_sub -h localhost -p 1883 -u hort-osona -P secretpass \
   -t "hort-osona/#" -v
```

Hauries de veure el heartbeat i el LWT manual al final. Prova tambe de matar el proces amb `Ctrl+Z` i veuras com el broker publica el LWT automatic.

## Pas 6: Mesurar rendiment (5 min)

Volem saber quants missatges per segon pot gestionar el nostre broker:

```bash
# Instal·la mqttbench (eina de benchmarking)
pip install mqttbench

# Genera 1000 missatges a 10 msg/s
mqttbench -h localhost -p 1883 -u hort-osona -P secretpass \
   -t "hort-osona/bench/test" -c 1 -n 1000 -r 10
```

Una RPi 4 hauria d'aguantar **>1000 msg/s** amb Mosquitto. Si nomes arriba a 100 msg/s, alguna cosa va malament (potser la SD es lenta; amb SSD es molt mes rapid).

## Validacio

Has acabat si:

- [ ] Has aixecat Mosquitto amb Docker i un password file amb 2 usuaris.
- [ ] Has publicat i subscrit amb `mosquitto_pub`/`mosquitto_sub`.
- [ ] Has provat wildcards `+` i `#`.
- [ ] Has vist un missatge retain al subscriure't despres.
- [ ] Has executat el client Python amb QoS 1, LWT i retain.
- [ ] Has vist el LWT automatic al matar el proces.

## Per aprofundir

- Activa TLS amb un certificat autofirmat i canvia el port a 8883.
- Crea un bridge entre dos brokers Mosquitto (un local i un al núvol).
- Mesura el retard (latencia) amb `tc` o un test dirigit.
- Implementa ACLs per topic (nomes l'usuari X pot subscriure a hort-osona/cmd/#).
- Compara el rendiment de Mosquitto amb EMQX amb un test de carga.
