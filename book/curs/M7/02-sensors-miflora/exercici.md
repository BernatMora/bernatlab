# Exercici practic - Capitol 2: Sensors Xiaomi MiFlora

> 30-45 min · Real a la RPi amb un MiFlora

## Objectiu

Connectar un sensor MiFlora a la RPi, llegir les seves dades cada 15 minuts i publicar-les a un broker MQTT. Acabaras amb un servei funcionant que pots deixar corrent.

## Requisits

- Raspberry Pi amb Python 3.10+
- Un sensor MiFlora amb pila nova
- La RPi ha de tenir BLE (Pi 3+, Pi 4, Pi Zero 2W, o dongle USB)
- 30-45 minuts

## Pas 1: Verifica el Bluetooth (5 min)

Assegura't que la RPi te BLE. Comprova-ho:

```bash
# Instal·la les eines si cal
sudo apt install bluetooth bluez bluez-tools

# Comprova el servei
sudo systemctl status bluetooth

# Escaneja dispositius BLE propers
sudo hcitool lescan
```

Deuries veure alguna cosa aixi:

```
C4:7C:8D:65:1B:32 (unknown)
C4:7C:8D:65:1B:32 Flower care
```

Apreta Ctrl+C despres de 8 segons. Apunta la MAC del teu MiFlora: sera del tipus `C4:7C:8D:xx:xx:xx`.

## Pas 2: Instal·la les dependencies (5 min)

Crea un entorn virtual per al projecte (bona praxis):

```bash
mkdir -p ~/hort-osona/services/miflora
cd ~/hort-osona/services/miflora
python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install miflora paho-mqtt pyyaml
```

Comprova que `miflora` funciona:

```bash
python3 -c "from miflora.miflora_poller import MiFloraPoller; print('OK')"
```

## Pas 3: Primer test del sensor (10 min)

Crea un fitxer `test_miflora.py`:

```python
import sys
from miflora.miflora_poller import MiFloraPoller
from btlewrap.bluepy import BluepyBackend

if len(sys.argv) < 2:
    print("Us: python3 test_miflora.py <MAC>")
    sys.exit(1)

mac = sys.argv[1]
poller = MiFloraPoller(mac=mac, backend=BluepyBackend)

print(f"Llegint MiFlora {mac}...")
data = poller.parameter_value(MiFloraPoller.SERVICE_DATA)
moisture, temp, ec, light, battery = data
fw = poller.firmware_version()
print(f"Firmware: {fw}")
print(f"Humitat soll: {moisture}%")
print(f"Temp soll: {temp}°C")
print(f"EC: {ec} µS/cm")
print(f"Llum: {light} lux")
print(f"Bateria: {battery}%")
```

Executa'l amb la MAC del teu sensor:

```bash
sudo python3 test_miflora.py C4:7C:8D:65:1B:32
```

Necessites `sudo` per accedir a l'adapter BLE. Si et molesta, pots afegir el teu usuari al grup `bluetooth`:

```bash
sudo usermod -aG bluetooth $USER
# Tanca sessio i torna a entrar
```

## Pas 4: Crea el servei continu (15 min)

Ara el fitxer principal `miflora_service.py`:

```python
#!/usr/bin/env python3
"""Servei que llegeix MiFlora i publica a MQTT cada 15 min."""

import json
import time
import logging
from datetime import datetime, timezone
import yaml

from miflora.miflora_poller import MiFloraPoller
from btlewrap.bluepy import BluepyBackend
import paho.mqtt.client as mqtt

# Carrega configuracio
with open("config.yaml") as f:
    CFG = yaml.safe_load(f)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s')
log = logging.getLogger(__name__)


def build_client():
    c = mqtt.Client("miflora-gateway", clean_session=False)
    c.username_pw_set(CFG["mqtt"]["user"], CFG["mqtt"]["pass"])
    c.connect(CFG["mqtt"]["host"], CFG["mqtt"]["port"], 60)
    return c


def read_sensor(mac):
    """Llegeix un MiFlora. Torna un dict o None si falla."""
    poller = MiFloraPoller(mac=mac, backend=BluepyBackend)
    try:
        data = poller.parameter_value(MiFloraPoller.SERVICE_DATA)
        moisture, temp, ec, light, battery = data
        return {
            "device": f"miflora-{mac[-5:].replace(':','')}",
            "mac": mac,
            "ts": datetime.now(timezone.utc).isoformat(),
            "soil_moisture": moisture,
            "soil_temp_c": temp,
            "ec_us_cm": ec,
            "lux": light,
            "battery": battery
        }
    except Exception as e:
        log.error(f"Error llegint {mac}: {e}")
        return None


def main():
    mqtt_client = build_client()
    sensors = CFG["sensors"]
    freq_s = CFG["frequency_s"]

    log.info(f"Iniciat amb {len(sensors)} sensors, freq {freq_s}s")

    while True:
        for mac in sensors:
            data = read_sensor(mac)
            if data:
                topic = f"hort-osona/miflora/{data['device']}"
                payload = json.dumps(data)
                mqtt_client.publish(topic, payload, qos=1)
                log.info(f"Publicat {topic}: moisture={data['soil_moisture']}%")
            time.sleep(5)  # pausa entre sensors per no col·lapsar BLE
        time.sleep(freq_s)


if __name__ == "__main__":
    main()
```

I el `config.yaml`:

```yaml
mqtt:
  host: "localhost"
  port: 1883
  user: "hort-osona"
  pass: "secret"

sensors:
  - "C4:7C:8D:65:1B:32"  # toma-cherry
  - "C4:7C:8D:65:1B:33"  # pebrot-italia
  - "C4:7C:8D:65:1B:34"  # enciam

frequency_s: 900
```

## Pas 5: Prova el servei (5 min)

En una terminal:

```bash
source .venv/bin/activate
sudo python3 miflora_service.py
```

Hauries de veure cada 15 min:

```
[2026-04-12 10:00:03] Publicat hort-osona/miflora/miflora-1B32: moisture=42%
[2026-04-12 10:00:09] Publicat hort-osona/miflora/miflora-1B33: moisture=38%
[2026-04-12 10:00:15] Publicat hort-osona/miflora/miflora-1B34: moisture=55%
```

En una altra terminal, comprova amb `mosquitto_sub` (veure cap 5):

```bash
mosquitto_sub -h localhost -t "hort-osona/miflora/#" -v
```

Si veus els missatges, tot funciona!

## Pas 6: Fer-lo correr com a dimoni (5 min)

Volem que arrenqui automaticament quan engeguem la RPi. Crea `/etc/systemd/system/hort-miflora.service`:

```ini
[Unit]
Description=Hort Osona - MiFlora gateway
After=network.target bluetooth.target mosquitto.service
Wants=mosquitto.service

[Service]
Type=simple
User=root
WorkingDirectory=/home/pi/hort-osona/services/miflora
ExecStart=/home/pi/hort-osona/services/miflora/.venv/bin/python miflora_service.py
Restart=on-failure
RestartSec=30

[Install]
WantedBy=multi-user.target
```

Activa'l:

```bash
sudo systemctl daemon-reload
sudo systemctl enable hort-miflora.service
sudo systemctl start hort-miflora.service
sudo systemctl status hort-miflora.service
```

## Validacio

Has acabat si:

- [ ] Has descobert la MAC del teu MiFlora amb `hcitool lescan`.
- [ ] Has llegit el sensor amb `test_miflora.py` i has vist les 4 lectures.
- [ ] El servei publicant cada 15 min a MQTT funciona.
- [ ] Has vist els missatges amb `mosquitto_sub`.
- [ ] El servei systemd esta actiu i arrenca al boot.

## Per aprofundir

- Connecta 2-3 sensors i mira com afecta el temps de bucle.
- Afegeix retry logic quan la lectura falla (sols passa un 2% de les vegades).
- Investiga com guardar les dades a InfluxDB directament (veure cap 6).
- Prova a canviar la freq a 60 s i mira la mida de la base de dades.
- Mira el projecte `homeassistant-mitemp_bt` per alternatives.
