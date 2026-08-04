# ADR 0001 - Microcontrolador inicial: ESP32 DevKit v1

> **Estat**: Acceptada · **Data**: 2026-08-03 · **Autor**: Bernat + Hermes

## Context

Volem començar el Bernat Maker Lab amb una primera placa de microcontrolador que ens permeti:

- Aprendre els fonaments (Nivell 1: GPIO, digitalRead/Write, PWM).
- Fer projectes amb sensors i actuadors (Nivell 2).
- Connectar-nos a la xarxa local (Nivell 3: Wi-Fi, MQTT, HTTP).
- No gastar gaire (5-10 EUR per placa).
- Tenir abundant documentacio i exemples a la comunitat.

## Alternatives considerades

| Alternativa | Preu | Pros | Contres |
|---|---|---|---|
| **ESP32 DevKit v1 (HiLetgo / DOIT)** | 5-7 EUR | Wi-Fi+BLE integrats, 30 pins, abundant documentacio, llibreries per a tot. | Requereix driver CH340 a Windows (no es problema). |
| Arduino Uno R3 | 8-10 EUR | Classic, molt simple, bona per a Nivell 1. | No te Wi-Fi, cal comprar shield separat (~15-20 EUR). |
| ESP8266 NodeMCU | 4-6 EUR | Mes barat que lESP32, tambe te Wi-Fi. | Menys pins, menys memoria, sense BLE, menys futur. |
| Raspberry Pi Pico W | 6-8 EUR | Molt barat, bona documentacio. | Menys mainstream que lESP32 per a IoT. |
| ESP32-S3 DevKit | 10-15 EUR | Mes potent que lESP32 classic, mes memoria. | Massa per a Nivell 1, cal esperar. |
| ESP32-CAM | 8-12 EUR | Te camera integrada, ideal per a visio. | Pocs GPIO disponibles, no es bona primera placa. |

## Decisio

**Comencem amb 2 × ESP32 DevKit v1** (xip ESP32-WROOM-32, 4 MB flash, 30 pins, USB micro-B amb CH340 o CP2102).

## Raonament

1. **Cobertura maxima del curriculum**: lESP32 cobreix el Nivell 1 (GPIO, PWM), Nivell 2 (I2C, SPI, UART, sensors), Nivell 3 (Wi-Fi, BLE) i part del Nivell 5 (BLE per a aplicacions locals).
2. **Millor relacio qualitat/preu**: 5-7 EUR per una placa amb Wi-Fi+BLE es imbatible.
3. **Comunitat i exemples**: tots els tutorials, examples de codi i llibreries del món IoT estan fets per a lESP32.
4. **Futur**: quan vulguem fer projectes mes especialitzats (LoRa, visio, tactil), podem afegir altres plaques com a ampliacions - lESP32 basic segueix sent util.
5. **2 unitats ens permeten fer P2** (comunicacio entre dues plaques) i tenir recanvi si es crema una.

## Conseqüencies

- Cal instal·lar el driver CH340 a Windows (o el CP2102 si la placa en duu).
- Cal usar Arduino IDE (o PlatformIO) amb el paquet d'Espressif.
- Les plaques comparteixen pins i funcions: podem traslladar projectes entre elles facilment.
- El preu de les plaques es independent del projecte de lhort (que ja te HELTEC WiFi LoRa 32 V3).

## Notes operatives

- Mai connectis 5 V a un GPIO (es 3,3 V). Usa un conversor de nivell logic si cal.
- Mai connectis res als pins GPIO6-11 (estan lligats a la memoria flash).
- Usa sempre una resistencia de 220-330 ohm en serie amb els LEDs.

## Properes decisions

- ADR 0002 - Llenguatge inicial: Arduino IDE o PlatformIO o MicroPython.
- ADR 0003 - Patron de capitols del Maker Lab dins del BernatLab.
