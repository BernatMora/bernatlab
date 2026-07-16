# Resum - Capitol 2: Sensors Xiaomi MiFlora

## La idea clau

El **Xiaomi MiFlora (HHCCJCY10)** es un sensor bluetooth que es clava al test i et diu si la planta te set, te calor, te nutrients i te llum. Es petit (~5 cm), te pila de botó que dura un any, i val uns 10-15€. Es el sensor favorit dels horts urbans perque es **no-invasiu** (no cal cablejat) i **barat** (10 plantes = 100€). A l'Hort Osona en tenim 6 repartits entre els sectors productius.

## Que es el MiFlora i que mesura

El sensor es un tub de plastic blanc amb quatre sensors dins i una pila CR2032. Cada 5-10 minuts transmet per BLE (Bluetooth Low Energy) un paquet amb quatre lectures:

- **Soil moisture** (%) - humitat del substrat
- **Soil temperature** (°C) - temperatura del soll
- **EC / Fertility** (µS/cm) - conductivitat, proxy de nutrients
- **Light** (lux) - lluminositat

I a mes dades internes com el nivell de bateria i el temps desde l'ultim reset.

```
  +----------------------------+
  |  MiFlora HHCCJCY10         |
  |  - Soil moisture: 42%      |
  |  - Soil temp: 18.3°C       |
  |  - EC: 820 µS/cm           |
  |  - Light: 18.000 lux       |
  |  - Battery: 87%            |
  +----------------------------+
         |
         | BLE 4.0+ (advertising)
         |
         v
    Raspberry Pi (gateway)
```

## Per que BLE i no WiFi o Zigbee

El MiFlora usa **Bluetooth Low Energy (BLE)** per raons d'estalvi energetic. La pila CR2032 aguanta un any transmetent cada pocs minuts. Si fos WiFi, la pila duraria dies. Zigbee tambe es bona opcio pero el MiFlora no ho soporta de serie.

L'inconvenient es que **la RPi ha d'estar a prop** (10-20 metres) per rebre els advertisements. Si el test es a 50 metres, no arriba. Solucions:

- Multiples RPi com a gateways repartides per l'hort
- Repetidors BLE (ex. ESP32 que reenvien per WiFi o LoRa)
- Nodo central amb antena BLE externa (antena direccional a 2.4 GHz)

## Integracio a la RPi: el projecte miflora-mqtt

Hi ha diverses maneres d'integrar el MiFlora. La mes utilitzada a l'Hort Osona es la llibreria Python `miflora` combinada amb `paho-mqtt`:

```bash
pip install miflora paho-mqtt
```

Exemple de script Python que llegeix un MiFlora i el publica a MQTT:

```python
from miflora.miflora_poller import MiFloraPoller
from btlewrap.bluepy import BluepyBackend
import paho.mqtt.client as mqtt
import json
from datetime import datetime

# MAC del sensor (a l'etiqueta)
SENSOR_MAC = "C4:7C:8D:65:1B:32"

def llegir_i_publicar():
    poller = MiFloraPoller(
        mac=SENSOR_MAC,
        backend=BluepyBackend
    )
    try:
        data = poller.parameter_value(MiFloraPoller.FIRMWARE_VERSION)
        fw = int(data.split('.')[0])

        if fw < 3:
            # Versio antiga, un sol bloc
            payload = poller.parameter_value(MiFloraPoller.SERVICE_DATA)
        else:
            # Versio nova, amb broadcast
            payload = poller.parameter_value(MiFloraPoller.SERVICE_DATA)

        moisture, temp, ec, light, battery = payload

        msg = {
            "device": f"miflora-{SENSOR_MAC[-5:].replace(':','')}",
            "ts": datetime.utcnow().isoformat() + "Z",
            "soil_moisture": moisture,
            "soil_temp_c": temp,
            "ec_us_cm": ec,
            "lux": light,
            "battery": battery
        }
        client = mqtt.Client("miflora-gateway")
        client.connect("localhost", 1883)
        client.publish(
            f"hort-osona/miflora/{SENSOR_MAC[-5:].replace(':','')}",
            json.dumps(msg),
            qos=1
        )
        client.disconnect()
    except Exception as e:
        print(f"Error llegint {SENSOR_MAC}: {e}")

if __name__ == "__main__":
    while True:
        llegir_i_publicar()
        time.sleep(900)  # cada 15 min
```

## Descoberta dels sensors

La primera vegada has de descobrir les MAC dels sensors. Un cop els tens emparellats, la MAC es estable:

```bash
sudo hcitool lescan
# Escaneja 8 segons i llista els BLE visibles:
# C4:7C:8D:65:1B:32 miflora
# C4:7C:8D:65:1B:33 miflora
# C4:7C:8D:65:1B:34 miflora
```

Apunta les MAC en un paper i al fitxer `~/hort-osona/config/dades.yaml` (veure cap 1).

## Decodificacio del advertisement BLE

Si vols entendre que passa per sota, el MiFlora envia un "service data" amb un format propietari de Xiaomi. La llibreria `miflora` ja el descodifica, pero si vols fer-ho tu en C o en un microcontrolador, aqui tens el format (versio >=3):

```
Offset  Longitud  Camp
0       1         firma (0x71 per MiFlora)
1       2         seq counter
3       1         soil moisture (%)
4       2         soil temp (decagrees, signed, LE)
6       2         EC (µS/cm, unsigned, LE)
8       4         light (lux, uint32 LE)
12      1         battery (%)
13      1         firmware version
```

Exemple en Python pur (sense `miflora`):

```python
import struct
data = bytes.fromhex("7122033412a80300784f00b50100")
moisture = data[3]
temp_raw = struct.unpack('<h', data[4:6])[0]
temp = temp_raw / 10.0
ec = struct.unpack('<H', data[6:8])[0]
light = struct.unpack('<I', data[8:12])[0]
battery = data[12]
# moisture=52, temp=47.4??, ec=216, light=20380, battery=181??
```

Atencio: el format canvia entre firmwares 2.x i 3.x. Millor usar la llibreria.

## Bona praxis: cura del sensor

El MiFlora te una pila CR2032 i un sensor d'humitat capacitiu. Algunes cures:

- **No el submergeixis** en aigua, nomes al substrat humit.
- **Treu-lo** abans d'un transplantament (es trenca facil).
- **Ressona** la pila cada any (la llibreria t'avisa amb `battery < 20%`).
- **Evita sol directe** sobre el tub, pot escalfar el sensor i donar lectures erronies.

A l'Hort Osona el que fem es canviar la pila cada 12 mesos preventivament, i tenim 2 sensors de recanvi per si un es trenca.

## Limitacions conegudes

- **Alcance limitat**: 10-20 m amb un adapter BLE USB normal. Mes amb antena externa.
- **Lent per arrancar**: triga 2-3 segons a connectar-se i llegir. Si tens 10 sensors, el bucle trigues 20-30 segons.
- **No es apte per sòl molt argilós**: la lectura es menys fiable en argila pura. En substrat universal va molt be.
- **No te datalogger intern**: si la RPi no esta, no guarda res. Si vols historial garantit, posa un ESP32 amb SD.

## Alternatives al MiFlora

Si el MiFlora no et convenç, hi ha alternatives:

| Sensor       | Preu | Protocol | Pros               | Contres             |
|--------------|------|----------|--------------------|---------------------|
| MiFlora      | 12€  | BLE      | Barat, fiable      | No datalogger       |
| Xiaomi HHCC  | 12€  | BLE      | Igual a MiFlora    | -                   |
| Sonkirn 3in1 | 8€   | BLE      | Mes barat          | Menys precís        |
| ESP32+soil   | 5€   | WiFi     | Totalment DIY      | Has de soldar       |
| Atlas EZO    | 30€  | I2C      | Professional       | Cal cablejar        |
| Sensoterra   | 100€ | LoRa     | Llarg abast, soll  | Car, professional    |

A l'Hort Osona ens quedem amb MiFlora pel preu i la simplicitat.

## Connexions amb altres capitols

- **M7 Cap 1** - Les dades que captura el MiFlora son les "de soll".
- **M7 Cap 3** - Si vols mes abast, pots combinar MiFlora amb LoRa.
- **M7 Cap 5** - Les dades del MiFlora es publiquen a MQTT.
- **M7 Cap 10** - Cas real: detectar reg excessiu mirant EC.
