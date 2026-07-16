# Exercici practic - Capitol 3: Protocol LoRa (SX1262 868 MHz)

> 40-60 min · Real amb hardware LoRa o simulacio

## Objectiu

Muntar un node LoRa amb un ESP32 + SX1262, enviar una lectura de temperatura cada minut, i rebre-la a la RPi gateway. Acabaras amb una transmissio radio real.

## Requisits

- 1x ESP32 (Wemos D1 R32, NodeMCU-32S, o similar)
- 1x modul SX1262 (Waveshare, Lilygo, o beaglebone amb SPI)
- 1x antena SMA 868 MHz (~8 cm)
- 1x RPi amb Python 3.10+ (per al gateway)
- 1x sensor BME280 opcional (per a dades reals)
- 40-60 min

## Pas 1: Connecta el SX1262 a l'ESP32 (10 min)

Cablejat tipic (SPI):

| SX1262 | ESP32 |
|--------|-------|
| VCC    | 3.3V  |
| GND    | GND   |
| SCK    | GPIO 18 |
| MISO   | GPIO 19 |
| MOSI   | GPIO 23 |
| CS     | GPIO  5 |
| RST    | GPIO 14 |
| BUSY   | GPIO 26 |
| DIO1   | GPIO 33 |

Si uses la placa Lilygo LoRa32, tot ja ve integrat. Nomes cal connectar l'antena SMA (molt important fer-ho ABANS d'encendre per no cremar el radio).

## Pas 2: Configura el PlatformIO (10 min)

Si no tens PlatformIO, instal·la'l a VS Code. Crea un nou projecte ESP32:

```bash
mkdir -p ~/proves-lora/node1
cd ~/proves-lora/node1
pio init --board esp32dev
```

Edita `platformio.ini`:

```ini
[env:esp32dev]
platform = espressif32
board = esp32dev
framework = arduino
lib_deps =
    jgromes/RadioLib@^6.0.0
    adafruit/Adafruit BME280 Library@^2.2.0
monitor_speed = 115200
```

## Pas 3: Escriu el codi del node (15 min)

Edita `src/main.cpp`:

```cpp
#include <Arduino.h>
#include <RadioLib.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>

// Pins per Lilygo LoRa32 (ajusta si uses altre placa)
#define LORA_CS    5
#define LORA_RST   14
#define LORA_DIO1  33
#define LORA_BUSY  26

SX1262 radio = new Module(LORA_CS, LORA_RST, LORA_DIO1, LORA_BUSY);
Adafruit_BME280 bme;

uint16_t seq = 0;

void setup() {
  Serial.begin(115200);
  delay(2000);

  // Inicia BME280
  if (!bme.begin(0x76)) {
    Serial.println("BME280 no trobat");
  }

  // Inicia LoRa
  Serial.print("Iniciant radio... ");
  int state = radio.begin(
    868.0,    // freq MHz
    125.0,    // BW kHz
    9,        // SF
    5,        // CR
    0x12,     // sync word
    14,       // TX power dBm
    8,        // preamble
    1.6,      // TCXO voltage (1.6V per SX1262)
    false     // use TCXO
  );
  if (state != RADIOLIB_ERR_NONE) {
    Serial.print("Error: ");
    Serial.println(state);
    while (true);
  }
  Serial.println("OK");
}

void loop() {
  // Llegeix sensor
  float temp = bme.readTemperature();
  float hum = bme.readHumidity();

  // Prepara payload
  char payload[64];
  snprintf(payload, sizeof(payload),
           "{\"dev\":\"node1\",\"seq\":%u,\"t\":%.1f,\"h\":%.1f}",
           seq++, temp, hum);

  Serial.print("Enviant: ");
  Serial.println(payload);

  int state = radio.transmit(payload);
  if (state == RADIOLIB_ERR_NONE) {
    Serial.println("Enviat correctament");
  } else {
    Serial.print("Error: ");
    Serial.println(state);
  }

  // Espera 1 min
  delay(60000);
}
```

Compila i puja:

```bash
pio run -t upload
pio device monitor
```

## Pas 4: Munta el receptor a la RPi (15 min)

Connecta un altre SX1262 a la RPi (o usa una RPi amb la Waveshare HAT per LoRa). Pins:

| SX1262 | RPi |
|--------|-----|
| VCC    | 3.3V (pin 1) |
| GND    | GND (pin 6) |
| SCK    | GPIO 11 (pin 23) |
| MISO   | GPIO 9  (pin 21) |
| MOSI   | GPIO 10 (pin 19) |
| CS     | GPIO 8  (pin 24) |
| RST    | GPIO 25 (pin 22) |
| BUSY   | GPIO 24 (pin 18) |
| DIO1   | GPIO 23 (pin 16) |

Activa SPI:

```bash
sudo raspi-config
# -> Interface Options -> SPI -> Yes
sudo reboot
```

Instal·la les dependencies:

```bash
sudo apt install python3-pip
pip install paho-mqtt spidev RPi.GPIO
pip install pySX126x
```

Crea `gateway_lora.py`:

```python
#!/usr/bin/env python3
"""Gateway LoRa a la RPi. Rep paquets i els publica a MQTT."""

import json
import time
import logging
import paho.mqtt.client as mqtt
from sx126x import SX126x

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s')
log = logging.getLogger(__name__)

# Inicia radio
radio = SX126x(spi_bus=0, spi_cs=0,
               reset_pin=25, busy_pin=24, dio1_pin=23)
state = radio.begin(868.0, 125.0, 9, 5, 0x12, 14)
if state != 0:
    raise RuntimeError(f"Radio init error: {state}")
radio.set_rx(continuous=True)
log.info("Radio iniciat. Escoltant...")

# MQTT
mqtt_client = mqtt.Client("lora-gateway")
mqtt_client.connect("localhost", 1883)

while True:
    msg, err = radio.receive(timeout=5000)
    if err == 0 and msg:
        try:
            data = json.loads(msg)
            data["rssi"] = radio.getRSSI()
            data["snr"] = radio.getSNR()
            data["gateway_ts"] = time.time()

            topic = f"hort-osona/lora/{data.get('dev', 'unknown')}"
            mqtt_client.publish(topic, json.dumps(data), qos=1)
            log.info(f"Rebut: {data}")
        except json.JSONDecodeError:
            log.warning(f"Payload no es JSON: {msg}")
        except Exception as e:
            log.error(f"Error processant: {e}")
    elif err != 0 and err != -2:  # -2 = timeout
        log.warning(f"Radio error: {err}")
```

## Pas 5: Prova el sistema (5 min)

En una terminal a la RPi:

```bash
sudo python3 gateway_lora.py
```

En una altra terminal:

```bash
mosquitto_sub -h localhost -t "hort-osona/lora/#" -v
```

Despres a l'ESP32, obre el monitor serie. Hauries de veure cada minut:

```
Enviant: {"dev":"node1","seq":42,"t":21.3,"h":58.0}
Enviat correctament
```

I a la RPi:

```
[2026-04-12 11:00:00] Rebut: {'dev': 'node1', 'seq': 42, 't': 21.3, ...}
```

Si no reps res:

1. Verifica que l'antena esta connectada.
2. Comprova que el sync word (`0x12`) es igual als dos costats.
3. Prova SF=7 o SF=8 (mes permis).
4. Apropa els dos dispositius a 1 metre.

## Pas 6: Mesura l'abast (10 min)

Si tot funciona, podem fer proves d'abast:

```bash
# A l'ESP32, canvia el delay a 5 segons per fer proves rapid
# delay(5000);

# Surt al carrer amb l'ESP32 i un powerbank
# A cada 50 m, mira si la RPi reb el missatge
```

Apunta a quina distancia es perd. Hauries d'arribar a 500 m - 1 km amb bona antena en visio directa.

## Validacio

Has acabat si:

- [ ] Has connectat el SX1262 a l'ESP32 i a la RPi amb l'antena SMA.
- [ ] El node ESP32 envia un missatge JSON cada minut.
- [ ] La RPi rep el missatge i el publica a MQTT.
- [ ] Veus el payload amb `mosquitto_sub`.
- [ ] Has fet una prova d'abast i sapigueres a quants metres arriba.

## Per aprofundir

- Implementa ACK: que el gateway contesti i el node reintent si no reb resposta.
- Afegeix un watchdog al node: si no reb ACK, retransmet amb SF mes alt.
- Investiga LoRaWAN amb The Things Network (TTN) si vols mes robustesa.
- Compara SF7, SF9, SF12 en diferents condicions.
- Connecta el node a un panell solar per fer-lo totalment autonomous.
