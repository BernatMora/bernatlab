# Capítol 65 — El node LoRa al camp

> *"Aquest capítol és on l'hort es connecta de veritat. Fins ara tenies un servidor; ara tens un sistema que escolta el que passa al camp."*

## 65.1 Què aprendràs

- Quin hardware necessites per al node LoRa.
- Com muntar el node (ESP32 + SX1262 + sensors).
- Com programar-lo per publicar dades a MQTT.
- Com rebre les dades a la Raspberry.
- Com veure les primeres dades reals a Grafana.

## 65.2 Durada estimada

2-3 hores (comptant proves).

## 65.3 Quin hardware

Per al node del camp:

- **ESP32-WROOM-32** (la placa de microcontrol·lador): 5 €.
- **Mòdul SX1262 868 MHz** (la ràdio LoRa): 10 €.
- **Antena 868 MHz** amb connector IPEX/U.FL: 3 €.
- **Sensor BME280** (temperatura, humitat, pressió): 5 €.
- **Sensor d'humitat del sòl capacitiu**: 3 €.
- **Cable Dupont** (per connectar tot): 5 €.
- **Caixa estanca IP65**: 5 €.
- **Bateria 18650 + carregador TP4056**: 8 €.
- **Placa solar 6V 1W** (opcional): 8 €.

**Total: ~50 € per node.**

Si ja tens un gateway LoRaWAN (Dragino LPS8, RAK7258, etc.), el node serà més simple — parla directament amb TTN, no necessita un gateway local.

## 65.4 Decidir: LoRaWAN o P2P

Al **Cap 25** ja vam decidir això. Recordatori breu:

- **LoRaWAN + TTN**: el node parla amb un gateway, TTN redirigeix a un servidor (el teu, via MQTT). Molt escalable, però depens d'un servei extern.
- **LoRa P2P**: dos mòduls SX1262 parlen directament. No hi ha servidor intermedi. Més simple, però menys escalable.

Per a un homelab amb un sol node, **P2P és més simple** — no necessites TTN ni un gateway, només dos SX1262. Però **LoRaWAN + un gateway Dragino LPS8** és més robust.

Aquest capítol assumeix **LoRaWAN amb un gateway local**. Si vols P2P, els canvis són petits (mira el Cap 31).

## 65.5 Muntar el gateway (si no el tens)

El gateway és un dispositiu que escolta els nodes LoRa i envia les dades a un servidor. El model més popular per a homelab és el **Dragino LPS8**.

Per muntar-lo:

1. Connecta'l al router via Ethernet.
2. Connecta'l a l'antena (port SMA).
3. Endolla'l.
4. Accedeix a la interfície web (per defecte, http://192.168.1.77).
5. Configura'l per parlar amb TTN o amb el teu servidor local.

Al cap 27 explicàvem com configurar el gateway amb concentratord. Si tens dubtes, mira'l.

## 65.6 Muntar el node

Connexions de l'ESP32 al SX1262 (SPI):

| ESP32 | SX1262 |
|---|---|
| 3.3V | VCC |
| GND | GND |
| GPIO 5 | SCK |
| GPIO 27 | MISO |
| GPIO 2 | MOSI |
| GPIO 4 | NSS (CS) |
| GPIO 14 | RST |
| GPIO 26 | DIO1 |
| GPIO 33 | BUSY |

I els sensors:

| ESP32 | BME280 | Humitat sòl |
|---|---|---|
| 3.3V | VCC | VCC |
| GND | GND | GND |
| GPIO 21 (SDA) | SDA | - |
| GPIO 22 (SCL) | SCL | - |
| GPIO 34 (ADC) | - | AOUT |

Això és la part elèctrica. Ara ve la programació.

## 65.7 Programar el node

Usa **Arduino IDE** o **PlatformIO** per programar l'ESP32. Jo recomano PlatformIO (integrat a VS Code) per la seva potència.

Crea un nou projecte "ESP32 + LoRa + BME280".

**Llibreries necessàries** (via PlatformIO):

```ini
lib_deps =
    sandeepmistry/LoRa@^0.8.0
    adafruit/Adafruit BME280 Library@^2.2.4
    bblanchon/ArduinoJson@^7.0.0
```

**Codi bàsic**:

```cpp
#include <SPI.h>
#include <LoRa.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>

#define SS_PIN    4
#define RST_PIN   14
#define DIO0_PIN  26

Adafruit_BME280 bme;

int counter = 0;

void setup() {
    Serial.begin(115200);

    // Setup LoRa
    LoRa.setPins(SS_PIN, RST_PIN, DIO0_PIN);
    if (!LoRa.begin(868E6)) {
        Serial.println("Error iniciant LoRa");
        while (1);
    }
    LoRa.setSpreadingFactor(7);
    LoRa.setSignalBandwidth(125E3);
    LoRa.setTxPower(14);

    // Setup BME280
    if (!bme.begin(0x76)) {
        Serial.println("Error iniciant BME280");
        while (1);
    }
}

void loop() {
    // Llegeix sensors
    float temperatura = bme.readTemperature();
    float humitat = bme.readHumidity();
    float pressio = bme.readPressure() / 100.0;

    // Llegeix humitat del sòl (0-4095, menor = més humit)
    int soilRaw = analogRead(34);
    float soilPercent = map(soilRaw, 0, 4095, 100, 0);  // invertir

    // Crea el payload
    String payload = "{";
    payload += "\"node\":\"hort1\",";
    payload += "\"counter\":" + String(counter) + ",";
    payload += "\"temperatura\":" + String(temperatura, 1) + ",";
    payload += "\"humitat\":" + String(humitat, 1) + ",";
    payload += "\"pressio\":" + String(pressio, 1) + ",";
    payload += "\"soil\":" + String(soilPercent, 1);
    payload += "}";

    // Envia via LoRa
    LoRa.beginPacket();
    LoRa.print(payload);
    LoRa.endPacket();

    Serial.println("Enviat: " + payload);
    counter++;

    // Espera 5 minuts
    delay(300000);
}
```

Pujem el codi a l'ESP32.

## 65.8 Receptar les dades a la Raspberry

Al gateway Dragino, configura el "Packet Forwarder" per enviar les dades a un servidor local:

1. Accedeix a la interfície web del gateway.
2. Configura el servidor primari com a `localhost` (o la IP de la RPi si el gateway és un altre dispositiu).
3. Configura el port 1700 (per defecte del packet forwarder).

A la Raspberry, hem de tenir un servei que escolti el port 1700 i enviï les dades a MQTT. Una opció és **ChirpStack** (molt potent però complex), o **golismero** (molt simple).

Alternativa: usa **TTN** com a intermediari. El gateway envia a TTN, i TTN redirigeix a un servidor MQTT (que pot ser la teva RPi).

## 65.9 Configurar TTN (mètode recomanat)

**The Things Network** (TTN) és gratuït per a ús personal. Configurar-lo:

1. Crea un compte a https://www.thethingsnetwork.org.
2. Crea una **Application**.
3. Crea un **End device** dins l'aplicació:
   - Manufacturer: el teu (o selecciona el perfil correcte).
   - DevEUI, AppEUI, AppKey: els que tingui el teu node (o genera'ls automàticament).
4. Configura el **Payload formatter** (Uplink) per desxifrar CayenneLPP o el teu format JSON.
5. Configura l'**integració MQTT**:
   - Default endpoint.
   - Porta 1883.
   - Username i password: els de Mosquitto (però TTN ha de poder accedir — cal exposar Mosquitto, cosa que NO recomanem per seguretat).

**Alternativa més segura**: usa TTN per desar les dades, i un script a la RPi que les vagi a buscar periòdicament via l'API de TTN (no via MQTT directe).

## 65.10 Receptar amb un script Python local

Si vols evitar TTN, pots tenir un script Python a la RPi que escolti el port 1700:

Crea `~/homelab/scripts/lora-listener.py`:

```python
import socket
import json
import paho.mqtt.client as mqtt
import os

# Configuració
TTN_MQTT_USER = "bernat"
TTN_MQTT_PASSWORD = os.environ["MQTT_PASSWORD"]
MQTT_BROKER = "localhost"
MQTT_PORT = 1883

# Client MQTT
client = mqtt.Client()
client.username_pw_set(TTN_MQTT_USER, TTN_MQTT_PASSWORD)
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Socket per escoltar el gateway
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 1700))

print("Escoltant al port 1700...")

while True:
    data, addr = sock.recvfrom(4096)
    # Parseja el protocol TTN Packet Forwarder
    # (Aquí va una mica de feina per deserialitzar el format)
    # Publica a MQTT
    payload = {"raw": data.hex()}
    client.publish("lora/gateway/raw", json.dumps(payload))
```

Aquest script és esquemàtic — caldria implementar correctament el protocol del packet forwarder. En la pràctica, és molt més fàcil usar TTN.

## 65.11 Veure les primeres dades a Grafana

Un cop el node envia, el gateway rep, TTN redirigeix, i la teva cadena MQTT → InfluxDB → Grafana ja té les dades.

Si tot està connectat:

1. Publica una dada de prova (o espera que el node enviï).
2. Mira els logs de Mosquitto: `docker logs mosquitto`.
3. Mira els logs de Telegraf: `docker logs telegraf`.
4. A Grafana, crea una gràfica nova amb `SELECT mean("temperatura") FROM "mqtt_consumer" WHERE node = 'hort1'`.

Si veus una línia a la gràfica, **tot funciona**. El teu hort ara és al núvol.

## 65.12 Bateria i durada

Si el node funciona amb bateria, el consum és crític. Optimitzacions:

- **Deep sleep** entre transmissions (ESP32 consumeix 10 µA en sleep).
- Transmetre cada 5-15 minuts en lloc de cada minut.
- Usar SF7 (ràpida, menys temps d'aire).
- Reduir la potència de transmissió al mínim necessari.

Codi per afegir deep sleep:

```cpp
#include <esp_sleep.h>

void loop() {
    // Llegeix sensors
    // Envia dades
    Serial.println("Anant a dormir 5 minuts");
    esp_sleep_enable_timer_wakeup(300 * 1000000);
    esp_deep_sleep_start();
}
```

Així l'ESP32 es desperta cada 5 minuts, llegeix sensors, envia, i torna a dormir. La bateria pot durar setmanes o mesos.

## 65.13 Què ve després

Ja tens el node LoRa enviant dades reals des del camp. Al **Cap 66** afegirem un **bot de Telegram** per rebre alertes al mòbil.

## 65.14 Errors habituals

**Error 1: el node no es connecta al gateway**.

Comprova:

- Clau d'aplicació (AppKey) correcta.
- Freqüència correcta (868 MHz a Europa).
- El node està dins del rang del gateway.
- La DevEUI és correcta a TTN.

**Error 2: les dades arriben però no es veuen a Grafana**.

Comprova:

- Telegraf està escoltant el topic correcte.
- InfluxDB està rebent dades (botó "Query" a InfluxDB UI).
- La query de Grafana té el bon nom de mesura (`mqtt_consumer` per defecte).

**Error 3: el node es queda sense bateria ràpid**.

Augmenta l'interval de transmissió, activa deep sleep, redueix la potència de transmissió.

**Error 4: senyals dèbils (RSSI baix)**.

Afegeix una antena millor, canvia la ubicació del node, augmenta SF (a costa de més temps d'aire i consum).

## 65.15 Resum

Ara tens el node LoRa enviant dades reals a través de TTS → Mosquitto → Telegraf → InfluxDB → Grafana. La cadena completa funciona. A partir d'aquí, el que pots fer és infinit:

- Afegir més nodes.
- Afegir més sensors (vent, pluja, radiació solar).
- Fer automatitzacions a Node-RED basades en les dades.
- Afegir alertes quan els valors surtin dels llindars.

## 65.16 Exercicis pràctics

1. Munta el node (ESP32 + SX1262 + sensors).
2. Programa'l amb el codi bàsic.
3. Configura el gateway (o usa TTN).
4. Configura Telegraf per escoltar `lora/+/+`.
5. Crea un panell a Grafana amb les dades.
6. Activa deep sleep al node.
7. Col·loca el node a l'hort (o al balcó) i espera 24 h.
8. Documenta la configuració al `homelab/setup-log.md`.
