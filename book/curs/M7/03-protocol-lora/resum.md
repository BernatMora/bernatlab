# Resum - Capitol 3: Protocol LoRa (SX1262 868 MHz)

## La idea clau

**LoRa** (Long Range) es un modulacio de radio dissenyada per enviar **pocs bytes a molta distancia** consumint **molt poca energia**. Es la tecnologia ideal per sensors de camp que estan lluny del gateway: un sensor LoRa amb pila pot durar 5 anys enviant dades cada 15 minuts a 5 km de distancia. A l'Hort Osona l'usem per cobrir els sectors mes allunyats (l'era de les carxoferes, el camp de cereals) on el BLE del MiFlora no arriba.

## Que es LoRa i que no es

LoRa es **unicament la capa fisica** (la modulacio de radio). No es la xarxa completa. Per sobre de LoRa tens:

- **LoRaWAN**: el protocol de xarxa (com el 4G per LoRa). Te gateways, servidors, AppKeys, etc.
- **LoRa punto a punto (P2P)**: nomes LoRa, sense xarxa. Dos dispositius parlen directament.

A l'Hort Osona fem servir **LoRa P2P** perque nomes tenim 4-5 sensors i no cal la complexitat de LoRaWAN. Es mes simple i mes barat.

```
Sensor amb SX1262  <- 868 MHz ->  Gateway amb SX1262
   (RPi o ESP32)                       (RPi central)
```

## Especificacions del SX1262 868 MHz

El modul **SX1262IMLTRT** de Semtech es el radio mes utilizat actualment. Es el successor del SX1276 i te millor consum i abast. Es connecta per **SPI** a un microcontrolador (ESP32, RPi, STM32).

Caracteristiques:

- **Frequencia**: 868 MHz (Europa) o 915 MHz (EUA). A Catalunya 868.
- **Modulacio**: LoRa (CSS - Chirp Spread Spectrum).
- **Potencia TX**: fins a +22 dBm (~158 mW). A Europa, limit legal a +14 dBm (25 mW) per no necessitar llicencia.
- **Sensibilitat RX**: fins a -148 dBm (aixo es el que dona l'abast de km).
- **Consum TX**: ~100 mA a +14 dBm. Consum RX: ~5 mA. Repos: <1 µA.
- **Aire data rate**: 0.3 a 50 kbps segons el **spreading factor** (SF7 a SF12).

A mes el SX1262 inclou un **paquet engine** que gestiona CRC, whitening i encriptacio basica. Ideal per a qui vol fer P2P sense preocupar-se de la capa fisica.

## LoRa vs altres tecnologies

| Tecnologia | Abast  | Consum TX | Consum RX | Preu radio | Us a hort |
|-----------|--------|-----------|-----------|------------|-----------|
| BLE       | 10-20m | 15 mA     | 15 mA     | 4€         | Sensors propers |
| WiFi      | 50 m   | 250 mA    | 100 mA    | 5€         | Gateway, no sensors |
| Zigbee    | 100 m  | 30 mA     | 30 mA     | 4€         | Xarxes mesh |
| LoRa      | 5 km   | 100 mA    | 5 mA      | 5€         | Sensors lluny |
| Cellular  | km     | 300 mA    | 100 mA    | 20€        | Sense cobertura WiFi |

LoRa **brilla** quan necessites mes de 100 m i la pila ha de durar mesos o anys. Si el sensor esta a 5 metres de la RPi, BLE es millor. Si esta a 2 km i nomes envies 10 bytes cada 15 min, LoRa es perfecte.

## Spreading Factor: la clau de l'abast

El **SF (Spreading Factor)** es el parametre que controla el trade-off entre abast i velocitat. Va de SF7 (rapid, curt abast) a SF12 (lent, llarg abast).

| SF  | Bitrate | Temps a 10 bytes | Abast relatiu |
|-----|---------|------------------|---------------|
| SF7 | 5.5 kbps | 50 ms           | 1x            |
| SF8 | 3.1 kbps | 100 ms          | 1.3x          |
| SF9 | 1.8 kbps | 200 ms          | 1.7x          |
| SF10| 0.98 kbps| 400 ms          | 2.2x          |
| SF11| 0.44 kbps| 800 ms          | 2.8x          |
| SF12| 0.25 kbps| 1600 ms         | 3.5x           |

A l'Hort Osona usem **SF9** que dona ~1 km d'abast amb bona fiabilitat. SF12 es massa lent i SF7 massa curt.

## Bandwidth i Coding Rate

Dos parametres mes que afecten l'abast:

- **Bandwidth (BW)**: ample de banda del canal. Com mes estret (125 kHz, 250 kHz, 500 kHz), mes sensible pero menys capacitat. Usem 125 kHz.
- **Coding Rate (CR)**: correccio d'errors. CR4/5 (1 bit de paritat cada 4) a CR4/8 (3 bits de paritat). Usem CR4/5.

Aquests parametre es configuren als dos extrems i han de coincidir. Si poses SF12 al sensor i SF7 al gateway, no es parlen.

## Hardware: el modul i la antena

El SX1262 ve en plaques com:

- **Waveshare SX1262 LoRa Node** (~12€): ESP32 + SX1262 + antena SMA. Ideal per a sensors.
- **Dragino LoRa Shield** (~20€): per Arduino.
- **RAK3172** (~10€): modul petit, nomes LoRa, per integrar.
- **Lilygo LoRa32** (~25€): ESP32 + SX1262 + OLED + bateria. Tot en un.

L'antena es **critica**. Una antena mal apuntada o massa curta redueix l'abast a la meitat. Usar:

- Antena SMA 868 MHz de 1/4 d'ona (~8.6 cm) - la mes comuna.
- Antena exterior amb cable coaxial si el gateway es a dins un edifici.
- Antena colineal o Yagi per abast maxim (>5 km).

## Exemple: llegir un sensor i enviar per LoRa

Exemple en C++ per ESP32 + SX1262 usant la llibreria RadioLib:

```cpp
#include <RadioLib.h>

// SX1262 te 5 pins: SCK, MISO, MOSI, CS, BUSY, RESET, DIO1
SX1262 radio = new Module(SS, RST, DIO1, BUSY);

void setup() {
  Serial.begin(115200);
  // freq=868.0 MHz, BW=125 kHz, SF=9, CR=4/5, TX=14 dBm
  int state = radio.begin(868.0, 125.0, 9, 5, 0x12, 14);
  if (state != RADIOLIB_ERR_NONE) {
    Serial.print("Error iniciant radio: ");
    Serial.println(state);
    while (true);
  }
}

void loop() {
  // Llegeix sensor (BME280)
  float temp = bme.readTemperature();
  float hum = bme.readHumidity();
  
  // Codifica com a text
  char payload[32];
  snprintf(payload, sizeof(payload), "T=%.1f H=%.1f", temp, hum);
  
  // Envia
  int state = radio.transmit(payload);
  if (state == RADIOLIB_ERR_NONE) {
    Serial.print("Enviat: ");
    Serial.println(payload);
  } else {
    Serial.print("Error enviant: ");
    Serial.println(state);
  }
  
  // Deep sleep 15 min per estalviar pila
  esp_sleep_enable_timer_wakeup(15 * 60 * 1000000ULL);
  esp_deep_sleep_start();
}
```

## Receptor LoRa a la RPi

A l'Hort Osona tenim una RPi al centre de l'hort amb un SX1262 connectat per SPI. Un petit script Python llegeix els missatges i els publica a MQTT:

```python
# receptor simple amb pySX126x (llibreria Python per SX1261/SX1262)
from sx126x import SX126x
import json, paho.mqtt.client as mqtt
from datetime import datetime

radio = SX126x(spi_bus=0, spi_cs=0, reset_pin=25, busy_pin=24, dio1_pin=23)
radio.begin(868.0, 125.0, 9, 5, 0x12, 14)

mqtt_client = mqtt.Client("lora-gateway")
mqtt_client.connect("localhost", 1883)

while True:
    msg, err = radio.receive(timeout=10000)  # 10s
    if msg:
        try:
            data = json.loads(msg)
            data["ts"] = datetime.utcnow().isoformat() + "Z"
            data["rssi"] = radio.getRSSI()
            data["snr"] = radio.getSNR()
            topic = f"hort-osona/lora/{data['device']}"
            mqtt_client.publish(topic, json.dumps(data), qos=1)
        except Exception as e:
            print(f"Error: {e}")
```

## Avantatges reals per a un hort

LoRa es la **tecnologia idonia** per a horts perque:

1. **Cobertura**: arriba a sectors que el BLE no cobreix (300 m, 1 km, 5 km).
2. **Autonomia**: amb 2 piles AA, un sensor LoRa dura 2-3 anys enviant cada 15 min.
3. **Robustesa**: travessa arbres, cases, fins i tot petits turons.
4. **Sense infraestructura**: no cal WiFi, no cal cobertura cellular. Només un gateway.
5. **Legal**: 868 MHz es banda ISM lliure a Europa. No pagues quota.
6. **Barat**: 10€ per node, 20€ per gateway.

A l'Hort Osona tenim un gateway al centre i 4 nodes: un a l'era de les carxoferes (800 m), un al camp de cereals (1.2 km), un al pou (400 m), un al magatzem (300 m). Cap altre tecnologia ens donava aquesta cobertura per aquest preu.

## Limitacions i inconvenients

- **Limite de duty cycle**: a 868 MHz nomes pots transmetre l'1% del temps. Si transmetes 1 s, has d'esperar 99 s.
- **Banda estreta**: 125 kHz BW = pocs kbps. NO serveix per video, ni per moltes dades.
- **Sensibilitat a interferencies**: si hi ha molts altres dispositius a 868 MHz, baixa el rendiment.
- **Configurar SF i BW iguals**: si un node te SF7 i l'altre SF12, no es parlen.
- **No es IP**: no tens adreces IP, no pots enviar paquets arbitraris. Has de codificar el que envies.
- **Sense ACK garantit**: LoRaWAN te ACK, P2P no. Has de fer la teva propia gestio de retries.

## Connexions amb altres capitols

- **M7 Cap 2** - El MiFlora usa BLE; LoRa es per a sensors mes llunyans.
- **M7 Cap 4** - L'arquitectura integra MiFlora i LoRa en un sol pipeline.
- **M7 Cap 5** - Tots dos acaben publicant a MQTT igual.
- **M7 Cap 7** - L'API pot oferir dades de sensors BLE i LoRa unificats.
