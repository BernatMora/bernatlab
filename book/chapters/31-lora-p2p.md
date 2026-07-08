# Capítol 31 — LoRa P2P amb SX1262: xarxes privades sense TTN

> *"Hi ha una altra manera de fer anar LoRa: sense servidor, sense TTN, sense ningú al mig. Dos mòduls parlen i punt. Més simple, menys potent, i de vegades exactament el que necessites."*

## 31.1 Quan té sentit LoRa P2P

Al capítol 25 vàrem veure l'arbre de decisió. LoRa P2P (punt a punt) té sentit quan:

- Tens un sol node i un sol receptor.
- Vols privacitat total (cap dada no passa per tercers).
- Estàs fent experiments amb la capa física.
- El volum de dades és tan petit que TTN no val la pena.

Per a Hort Osona no és la millor opció, però entenem que algunes situacions particulars la fan útil. Aquest capítol cobreix com fer-ho, amb exemples reals.

## 31.2 Què és LoRa P2P

En mode P2P, dos mòduls SX1262 es comuniquen directament. Sense gateway, sense network server. Tu defineixes:

- La freqüència (868.1 MHz, 868.3 MHz, etc.).
- El spreading factor (SF7-SF12).
- La amplada de banda (125, 250, 500 kHz).
- La potència de transmissió.
- El format del payload.
- Si hi ha ACK o no.
- Si hi ha xifrat o no.

Tot és a les teves mans. La llibreria **RadioLib** de jgromes és la millor eina per a P2P: moderna, ben documentada, suporta SX126x, SX127x, RFM9x.

## 31.3 Diferències amb LoRaWAN

| Característica | LoRaWAN | LoRa P2P |
|---|---|---|
| Network server | Necessari (TTN, ChirpStack) | No cal |
| Identificadors | DevEUI, AppEUI, AppKey | Cap (o propis) |
| Autenticació | Xifrada amb AppKey | Opcional, manual |
| Adreçament | DevAddr, multi-node | Cap (només 1 a 1) |
| Downlink | Estàndard | Manual, complicat |
| ADR | Automàtic | Manual |
| Consum de memòria | ~30-50 KB de codi | ~5-10 KB |
| Complexitat | Mitjana-alta | Baixa |

P2P és més simple, però tot el que abans feia el network server, ara ho has de fer tu.

## 31.4 Hardware: el que necessitem

Per a P2P, el hardware és exactament el mateix que per a LoRaWAN:

- Dos mòduls SX1262 (un com a node, un com a receptor).
- Un microcontrolador per a cada mòdul (ESP32, per exemple).
- Antenes 868 MHz.
- Alimentació.

La diferència és al software: amb P2P no cal TTN ni gateway.

## 31.5 Receptor: SX1262 connectat a la Raspberry

El receptor és un mòdul SX1262 connectat directament a la Raspberry per SPI. Hi ha diverses opcions:

### Opció 1: breakout board SX1262 + Raspberry

Connectem un breakout SX1262 als pins SPI de la Raspberry. Calen cables (no és tan net com un gateway SX1302).

### Opció 2: LoRa HAT per a Raspberry

Hi ha HATs per a Raspberry amb SX1262, com el Waveshare SX1262 LoRa HAT. Són barats (~15-25 €) i s'instal·len com un gateway però amb menys capacitats.

### Opció 3: USB LoRa dongle

Hi ha dongles USB amb SX1262 que es connecten a un port USB. Es comuniquen per serial. Molt còmode per a prototipatge.

Al BernatLab, recomanem l'opció 2 (HAT) per simplicitat. Si volem més versatilitat, l'opció 3 (USB dongle) és la més còmoda.

## 31.6 Codi del receptor en Python

A la Raspberry, un script Python que escolta els missatges P2P:

```python
#!/usr/bin/env python3
"""
receptor_lora_p2p.py
Rep missatges d'un node LoRa P2P amb SX1262 i els publica a MQTT.

Hardware: Waveshare SX1262 LoRa HAT a la Raspberry Pi 4.
"""

import json
import time
import struct
import paho.mqtt.client as mqtt
from datetime import datetime
from SX126x import SX126x

# Configuració LoRa
LORA_FREQ = 868100000  # 868.1 MHz
LORA_SF = 9            # Spreading Factor
LORA_BW = 125000       # 125 kHz
LORA_CR = 5            # Coding Rate 4/5
LORA_TX_POWER = 14     # dBm

# MQTT
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_USER = "lora-receptor"
MQTT_PASS = "password"
MQTT_TOPIC = "lora/hort/#"

# Inicialitzar el SX1262
lora = SX126x(
    freq_hz=LORA_FREQ,
    spreading_factor=LORA_SF,
    bandwidth=LORA_BW,
    coding_rate=LORA_CR,
    tx_power=LORA_TX_POWER,
)

# Inicialitzar MQTT
client = mqtt.Client()
client.username_pw_set(MQTT_USER, MQTT_PASS)
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()


def decode_payload(payload: bytes) -> dict:
    """
    Decodifica un payload CayenneLPP.

    Format esperat:
      - 0x67 0x01 [2 bytes]   : Temperatura (canal 1, valor × 10, signed)
      - 0x68 0x02 [2 bytes]   : Humitat (canal 2, valor × 2, unsigned)
      - 0x73 0x03 [2 bytes]   : Pressió (canal 3, valor × 10, unsigned)
    """
    decoded = {}
    i = 0
    while i < len(payload):
        if i + 1 >= len(payload):
            break
        tipo = payload[i]
        canal = payload[i + 1]
        i += 2
        if tipo == 0x67:  # Temperatura
            if i + 1 >= len(payload):
                break
            valor = struct.unpack(">h", payload[i:i + 2])[0]
            decoded["temperatura"] = valor / 10.0
            i += 2
        elif tipo == 0x68:  # Humitat
            if i + 1 >= len(payload):
                break
            valor = struct.unpack(">H", payload[i:i + 2])[0]
            decoded["humitat"] = valor / 2.0
            i += 2
        elif tipo == 0x73:  # Pressió
            if i + 1 >= len(payload):
                break
            valor = struct.unpack(">H", payload[i:i + 2])[0]
            decoded["pressio"] = valor / 10.0
            i += 2
        elif tipo == 0x75:  # Humitat del sòl
            if i >= len(payload):
                break
            decoded["humitat_sol"] = payload[i]
            i += 1
        else:
            # Tipus desconegut, aturar
            break
    return decoded


def publicar_a_mqtt(decoded: dict, rssi: int, snr: float):
    """Publica les dades decodificades al broker MQTT."""
    payload = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "rssi": rssi,
        "snr": snr,
        **decoded,
    }
    msg = json.dumps(payload)
    # Topic basat en el tipus de dada
    for key in decoded:
        topic = f"lora/hort/{key}"
        client.publish(topic, msg, retain=True)
    # També publiquem el payload complet
    client.publish("lora/hort/all", msg, retain=True)
    print(f"Publicat: {msg}")


def main():
    print(f"Receptor LoRa P2P a {LORA_FREQ/1e6} MHz, SF{LORA_SF}, BW {LORA_BW/1e3} kHz")
    print("Esperant transmissions...")

    while True:
        try:
            data, rssi, snr = lora.receive(timeout_ms=10000)
            if data:
                print(f"Rebut ({len(data)} bytes), RSSI={rssi}, SNR={snr}")
                decoded = decode_payload(data)
                if decoded:
                    publicar_a_mqtt(decoded, rssi, snr)
                else:
                    print(f"Payload no reconegut: {data.hex()}")
        except KeyboardInterrupt:
            print("\nAturant...")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(1)


if __name__ == "__main__":
    main()
```

Aquest codi:

- Inicialitza el SX1262 amb els paràmetres adequats.
- Escolta transmissions en bucle.
- Decodifica payloads CayenneLPP.
- Publica a MQTT per integrar-se amb la resta del BernatLab.

## 31.7 Codi del node en Arduino (ESP32 + SX1262)

El node és similar al que vam veure al capítol 29, però usant RadioLib i mode P2P:

```cpp
// BernatLab Hort Osona - Node LoRa P2P
// Hardware: Heltec LoRa 32 V3 + BME280
// Llibreria: RadioLib

#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>
#include <RadioLib.h>

// Pins per a la Heltec LoRa 32 V3
#define LORA_NSS  8
#define LORA_RST  12
#define LORA_DIO1 14
#define LORA_BUSY 13

// SX1262 amb RadioLib
SX1262 lora = new Module(LORA_NSS, LORA_DIO1, LORA_RST, LORA_BUSY);

// BME280
Adafruit_BME280 bme;

// Paràmetres P2P
#define LORA_FREQ     868.1
#define LORA_BW       125.0
#define LORA_SF       9
#define LORA_CR       5
#define LORA_TX_POWER 14

// Banderes
bool transmissio_OK = false;
volatile bool transmisio_completada = false;

void transmisio_completada_callback() {
    transmisio_completada = true;
}

void setup() {
    Serial.begin(115200);
    delay(2000);

    // Inicialitzar BME280
    if (!bme.begin(0x76) && !bme.begin(0x77)) {
        Serial.println(F("BME280 no trobat"));
        while (1) delay(1000);
    }

    // Inicialitzar SX1262 amb RadioLib
    Serial.print(F("Inicialitzant SX1262... "));
    int state = lora.begin();
    if (state != RADIOLIB_ERR_NONE) {
        Serial.print(F("Error: "));
        Serial.println(state);
        while (1) delay(1000);
    }
    Serial.println(F("OK"));

    // Configurar paràmetres
    lora.setFrequency(LORA_FREQ);
    lora.setSpreadingFactor(LORA_SF);
    lora.setBandwidth(LORA_BW);
    lora.setCodingRate(LORA_CR);
    lora.setOutputPower(LORA_TX_POWER);

    // Callback
    lora.setPacketSentAction(transmisio_completada_callback);
}

void loop() {
    // Llegir sensor
    float temperatura = bme.readTemperature();
    float humitat = bme.readHumidity();
    float pressio = bme.readPressure() / 100.0;

    // Codificar CayenneLPP
    uint8_t payload[16];
    int idx = 0;
    int16_t t10 = (int16_t)(temperatura * 10);
    payload[idx++] = 0x67;
    payload[idx++] = 0x01;
    payload[idx++] = (t10 >> 8) & 0xFF;
    payload[idx++] = t10 & 0xFF;
    uint16_t h2 = (uint16_t)(humitat * 2);
    payload[idx++] = 0x68;
    payload[idx++] = 0x02;
    payload[idx++] = (h2 >> 8) & 0xFF;
    payload[idx++] = h2 & 0xFF;
    uint16_t p10 = (uint16_t)(pressio * 10);
    payload[idx++] = 0x73;
    payload[idx++] = 0x03;
    payload[idx++] = (p10 >> 8) & 0xFF;
    payload[idx++] = p10 & 0xFF;

    // Transmetre
    Serial.print(F("Enviant... "));
    transmisio_completada = false;
    int state = lora.startTransmit(payload, idx);
    if (state != RADIOLIB_ERR_NONE) {
        Serial.print(F("Error: "));
        Serial.println(state);
    } else {
        // Esperar la transmissió
        unsigned long start = millis();
        while (!transmisio_completada && millis() - start < 5000) {
            lora.yield();
        }
        if (transmisio_completada) {
            Serial.println(F("OK"));
        } else {
            Serial.println(F("Timeout"));
        }
    }

    // Deep sleep 5 minuts
    Serial.println(F("Dormint..."));
    Serial.flush();
    esp_sleep_enable_timer_wakeup(5 * 60 * 1000000);
    esp_deep_sleep_start();
}
```

## 31.8 Avantatges i inconvenients del P2P

### Avantatges

- **Simplicitat**. No cal configurar TTN, no cal entendre DevEUI, AppEUI, etc.
- **Privacitat total**. Cap dada no surt del teu entorn.
- **Cost més baix**. No cal gateway SX1302 (més car), un SX1262 a la Raspberry n'hi ha prou.
- **Flexibilitat total**. Tu tries el format del payload, les capçaleres, el xifrat.

### Inconvenients

- **Escalabilitat limitada**. Dos mòduls, no més. Per a més, cal reimplementar la xarxa.
- **Sense roaming**. Si el node es mou, cal reconfigurar.
- **Sense ADR**. Cal optimitzar manualment.
- **Sense eines de monitoratge**. TTN ensenya gràfiques, RSSI, etc. En P2P, cal implementar-ho.
- **Cal gestionar errors**. En LoRaWAN, el NS desduplica i retransmet. En P2P, cal fer-ho manualment.

## 31.9 Com afegir reconeixement (ACK) en P2P

LoRaWAN té el seu mecanisme d'ACK. En P2P, podem implementar-lo manualment:

```cpp
// Al node: després de transmetre, escoltar un ACK durant 2 segons
lora.startTransmit(payload, idx);
// ... esperar la transmissió ...
// Escoltar un ACK durant RX1 (1s) i RX2 (2s)
String ack;
int state = lora.receive(ack, 0, 0, 2000);
if (state == RADIOLIB_ERR_NONE) {
    Serial.println("ACK rebut");
} else {
    Serial.println("Sense ACK, retransmetre");
}
```

Al receptor:

```python
# Quan rebem un missatge, enviem un ACK
def enviar_ack(received_payload):
    ack_payload = bytes([0xFF, 0x00, 0x01])  # Tipus ACK, longitud, OK
    lora.transmit(ack_payload)
```

Això afegeix complexitat, però permet saber si el missatge ha arribat.

## 31.10 Com xifrar en P2P

LoRaWAN xifra amb AES-128. En P2P, podem fer el mateix amb qualsevol llibreria AES:

```cpp
#include <mbedtls/aes.h>

uint8_t key[16] = { /* 16 bytes de clau */ };
uint8_t iv[16] = { /* IV aleatori */ };
uint8_t plaintext[16];
uint8_t ciphertext[16];

mbedtls_aes_context aes;
mbedtls_aes_setkey_enc(&aes, key, 128);
mbedtls_aes_crypt_cbc(&aes, MBEDTLS_AES_ENCRYPT, 16, iv, plaintext, ciphertext);
```

Però compte: en una xarxa P2P, la clau ha d'estar a tots dos extrems. Si volem canviar-la, cal reprogramar tots dos.

## 31.11 Què fer si volem molts nodes

P2P no escala. Si volem més de 2-3 nodes, les opcions són:

1. **P2P amb adreçament manual**: cada node té un ID, el receptor filtra per ID. Funciona per a uns pocs nodes.
2. **LoRaWAN amb ChirpStack autoallotjat**: la millor opció per a més de 2-3 nodes.
3. **Mesh amb Meshtastic**: una altra opció interessant, basada en LoRa, que permet mesh routing.

Per a Hort Osona, si volem créixer, **LoRaWAN amb TTN o ChirpStack** és la millor opció. P2P és per a situacions específiques.

## 31.12 Quan P2P és la millor opció

Algunes situacions on P2P és millor que LoRaWAN:

- **Hackatges ràpids**. Tens un node, vols transmetre, no tens temps de configurar TTN.
- **Educació**. Per aprendre LoRa a fons, res millor que un P2P.
- **Privacitat extrema**. Si no vols que cap dada passi per tercers.
- **Xarxes molt petites**. 1-2 nodes, no escalable.
- **Proves de camp**. Per validar la cobertura abans de muntar la xarxa completa.

## 31.13 Migració de P2P a LoRaWAN

Si comences amb P2P i vols migrar a LoRaWAN, la bona notícia és que **el hardware és el mateix**. Només cal canviar el software.

Concretament:

- El node P2P passa a executar LMIC o RadioLib en mode LoRaWAN.
- El receptor SX1262 a la Raspberry ja no cal; el gateway SX1302 s'hi connecta.
- Afegim un gateway LoRaWAN (Waveshare SX1302 HAT) a la Raspberry.
- Configurem TTN o ChirpStack.
- Adapta el payload a CayenneLPP (o JSON).

El temps de migració és d'unes hores, no pas setmanes.

## 31.14 Resum

En aquest capítol hem après què és LoRa P2P, quan té sentit, i com implementar-lo. Hem vist el codi del node (ESP32 + SX1262 + RadioLib) i del receptor (Python + SX1262 a la Raspberry). Hem après les limitacions d'aquesta arquitectura i quan és millor migrar a LoRaWAN. En el proper capítol veurem les proves de camp: com validar la cobertura, com calibrar el sistema, i com resoldre els problemes habituals.

## 31.15 Exercicis pràptics

1. Escriu el codi del node P2P amb RadioLib.
2. Escriu el codi del receptor en Python per a la Raspberry.
3. Prova la comunicació a 1 metre. Hauries de rebre el 100% dels missatges.
4. Prova a 50 metres en exterior.
5. Prova a 100 metres amb un obstacle al mig.
6. Mesura el RSSI a diferents distàncies.
7. Compara el rendiment de SF7 i SF12 a 100 metres.
8. Documenta al README els resultats de les proves.

Comandes útils:

```bash
# Receptor a la Raspberry
python3 ~/homelab/scripts/lora_p2p/receptor_lora_p2p.py

# Subscriure's a MQTT per veure les dades
mosquitto_sub -h 100.115.134.76 -t "lora/hort/#" -v -u bernat -P CONTRASENYA
```

Paraules clau: **LoRa P2P, point-to-point, RadioLib, SX1262, Python, receptor, ESP32, node, CayenneLPP, payload, xifrat, AES, ACK, retransmissió, adreçament, mesh, Meshtastic, RSSI, SNR, packet loss, time on air, EU868, SF7-SF12, BW125, Antena, ad-hoc, privat, xarxa privada, TTN alternatiu, ChirpStack**.