# Capítol 29 — Programació del node: ESP32 + LoRaWAN

> *"Programar un node LoRa és programació de sistemes encastats amb un extra: el temps d'aire és car i la bateria és finita. Cada byte compta."*

## 29.1 Què ha de fer el codi del node

Un node LoRaWAN complet ha de:

1. **Inicialitzar** el hardware (SPI per al SX1262, I2C per als sensors).
2. **Connectar-se a la xarxa LoRaWAN** (procediment de join OTAA).
3. **Llegir els sensors** periòdicament.
4. **Codificar les dades** en un payload binari (CayenneLPP recomanat).
5. **Transmetre** el payload via LoRaWAN.
6. **Entrar en deep sleep** fins a la propera transmissió.
7. **Despertar** i repetir.

Això, en codi, són 100-200 línies d'Arduino o MicroPython. Més del que sembla, menys del que sembla.

## 29.2 Quina llibreria: LMIC o RadioLib

Hi ha diverses llibreries per a LoRaWAN en ESP32:

### MCCI LoRaWAN LMIC (recomanada per a LoRaWAN)

- La versió moderna de la clàssica LMIC d'IBM.
- Molt estable, ben mantinguda.
- Suporta ESP32, ESP8266, STM32, etc.
- API basada en callbacks (pot ser una mica confosa al principi).

### RadioLib

- Llibreria moderna que suporta **LoRaWAN, LoRa P2P, FSK, OOK**, etc.
- API més neta que LMIC.
- Suporta moltes plaques i xips (SX126x, SX127x, RFM9x).
- Ideal si volem fer P2P i LoRaWAN amb la mateixa llibreria.

### Altres

- **arduino-lmic**: la clàssica, menys mantinguda.
- **TinyLoRa**: minimalista, per a nodes molt petits.
- **Heltec examples**: específics per a les plaques Heltec.

Recomanació: per a LoRaWAN amb ESP32, **MCCI LMIC** o **RadioLib**. Per a P2P, **RadioLib**.

## 29.3 Configuració de l'entorn Arduino

Si no tens l'entorn Arduino preparat:

1. **Instal·la Arduino IDE** (https://www.arduino.cc/en/software) o **PlatformIO** (integrat a VSCode).
2. **Afegeix el suport per a ESP32**:
   - Arduino IDE: a `File → Preferences`, afegeix l'URL `https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json` a "Additional Board Manager URLs".
   - Instal·la "esp32" des del Board Manager.
3. **Instal·la les llibreries necessàries** des del Library Manager:
   - **MCCI LoRaWAN LMIC library** (per a LoRaWAN).
   - **RadioLib** (alternativa).
   - **Adafruit BME280 Library** (per al sensor).
   - **Adafruit Unified Sensor** (dependència).

## 29.4 Exemple complet: codi per a Heltec LoRa 32 V3 amb BME280

Aquí tens un programa complet que llegeix un BME280 i transmet cada 5 minuts via LoRaWAN:

```cpp
// BernatLab Hort Osona - Node LoRaWAN
// Hardware: Heltec LoRa 32 V3 + BME280
// Llibreria: MCCI LoRaWAN LMIC
// Llicència: CC-BY-SA

#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>
#include <lmic.h>
#include <hal/hal.h>
#include <SPI.h>

// Identificadors LoRaWAN (substituir pels teus propis!)
static const u1_t PROGMEM DEVEUI[8] = { 0x70, 0xB3, 0xD5, 0x7E, 0xD0, 0x04, 0xF1, 0xCE };
static const u1_t PROGMEM APPEUI[8] = { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 };
static const u1_t PROGMEM APPKEY[16] = {
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
};

// Pins per a la Heltec LoRa 32 V3
#define PIN_LMIC_NSS  8
#define PIN_LMIC_RST  12
#define PIN_LMIC_DIO0 14
#define PIN_LMIC_DIO1 35
#define PIN_LMIC_DIO2 34

// BME280 (I2C per defecte a la Heltec)
#define SEALEVELPRESSURE_HPA (1013.25)
Adafruit_BME280 bme;

// Configuració de l'objectiu (TTN)
static const u4_t NETID = 0x13;  // TTN
static const u1_t NWKSKEY[16] = { 0 };  // No cal per a OTAA
static const u1_t APPSKEY[16] = { 0 };  // No cal per a OTAA
static const u4_t DEVADDR = 0;          // No cal per a OTAA
static const u1_t FREQ_CHNL_HOP = 0;    // desactivat (TTN gestiona)
static const u2_t FREQ_HZ_MIN = 868100000;
static const u2_t FREQ_HZ_MAX = 868500000;

const lmic_pinmap lmic_pins = {
    .nss = PIN_LMIC_NSS,
    .rxtx = LMIC_UNUSED_PIN,
    .rst = PIN_LMIC_RST,
    .dio = {PIN_LMIC_DIO0, PIN_LMIC_DIO1, PIN_LMIC_DIO2},
};

// Callbacks de LMIC
void onJoinFailed() {
    Serial.println(F("Join failed"));
}

void onJoinSuccess() {
    Serial.println(F("Join success!"));
    LMIC_setLinkCheckMode(1);
}

void onTransmitted() {
    Serial.println(F("Packet transmitted"));
}

// Tasca periòdica
osjob_t sendjob;

void do_send(osjob_t* j) {
    if (LMIC.opmode & OP_TXRXPEND) {
        Serial.println(F("OP_TXRXPEND, skip"));
    } else {
        // Llegir el sensor
        float temperatura = bme.readTemperature();
        float humitat = bme.readHumidity();
        float pressio = bme.readPressure() / 100.0F;  // Pa → hPa

        // Construir el payload CayenneLPP
        uint8_t payload[16];
        int idx = 0;
        // Temperatura (canal 1, valor × 10)
        int16_t t10 = (int16_t)(temperatura * 10);
        payload[idx++] = 0x67;  // Tipus: temperatura
        payload[idx++] = 0x01;  // Canal: 1
        payload[idx++] = (t10 >> 8) & 0xFF;
        payload[idx++] = t10 & 0xFF;
        // Humitat (canal 2, valor × 2)
        uint16_t h2 = (uint16_t)(humitat * 2);
        payload[idx++] = 0x68;  // Tipus: humitat
        payload[idx++] = 0x02;  // Canal: 2
        payload[idx++] = (h2 >> 8) & 0xFF;
        payload[idx++] = h2 & 0xFF;
        // Pressió (canal 3, valor en hPa × 10)
        uint16_t p10 = (uint16_t)(pressio * 10);
        payload[idx++] = 0x73;  // Tipus: pressió baromètrica
        payload[idx++] = 0x03;  // Canal: 3
        payload[idx++] = (p10 >> 8) & 0xFF;
        payload[idx++] = p10 & 0xFF;
        // Voltatge de la bateria (canal 4)
        // ... llegir amb analogRead() i afegir

        // Preparar i enviar
        LMIC_setTxData2(1, payload, idx, 0);
        Serial.print(F("Enviats "));
        Serial.print(idx);
        Serial.println(F(" bytes"));
    }
    // Programar la propera transmissió en 5 minuts
    os_setTimedCallback(&sendjob, os_getTime() + sec2osticks(300), do_send);
}

void setup() {
    Serial.begin(115200);
    delay(2000);  // Donar temps a que el port sèrie estigui llest

    // Inicialitzar el BME280
    if (!bme.begin(0x76)) {
        if (!bme.begin(0x77)) {
            Serial.println(F("BME280 no trobat!"));
            while (1) delay(1000);
        }
    }
    Serial.println(F("BME280 OK"));

    // Inicialitzar LMIC
    os_init();
    LMIC_reset();
    LMIC_setClockError(MAX_CLOCK_ERROR * 10 / 100);  // Tolerar 10% d'error

    // Configurar DevEUI, AppEUI, AppKey
    LMIC_setSession(0x13, DEVEUI, NWKSKEY, APPSKEY);
    LMIC_startJoin();

    // Programar la primera transmissió
    do_send(nullptr);
}

void loop() {
    os_runloop_once();
}
```

Aquest codi és llarg però estructurat. Repassem les parts importants.

## 29.5 Estructura del codi

El codi es compon de:

1. **Inclusions**: les llibreries.
2. **Identificadors LoRaWAN**: DevEUI, AppEUI, AppKey.
3. **Configuració de pins**: definits segons la placa.
4. **Inicialització del sensor**: BME280 en el nostre cas.
5. **Inicialització de LMIC**: clau per a LoRaWAN.
6. **Callback de transmissió**: `do_send` que llegeix, codifica, i envia.
7. **Setup**: inicialitza tot i programa la primera transmissió.
8. **Loop**: el bucle principal d'esdeveniments de LMIC.

## 29.6 CayenneLPP: detalls pràctics

CayenneLPP és el format recomanat per la seva eficiència. Cada dada és:

- 1 byte: **tipus** (0x67 = temperatura, 0x68 = humitat, etc.).
- 1 byte: **canal** (1-255, identifica quin sensor).
- N bytes: **valor** (1-4 bytes segons el tipus).

A la web de CayenneLPP hi ha la llista completa de tipus: https://developers.mydevices.com/cayenne/docs/cayenne-lpp/

Per als nostres sensors:

- **Temperatura (0x67)**: 2 bytes, signed 16-bit, valor × 10. Rang: -3276.7 a +3276.7 °C.
- **Humitat (0x68)**: 2 bytes, unsigned 16-bit, valor × 2. Rang: 0-100 %.
- **Pressió (0x73)**: 2 bytes, unsigned 16-bit, valor × 10. Rang: 0-6553.5 hPa.
- **Llum (0x65)**: 2 bytes, unsigned 16-bit, valor × 1. Rang: 0-65535 lux.
- **Humitat del sòl (0x75)**: 1 byte, unsigned 8-bit, valor × 1. Rang: 0-100 %.
- **Voltatge de bateria (0x74)**: 2 bytes, unsigned 16-bit, valor × 100. Rang: 0-655.35 V.

## 29.7 El procediment de join OTAA

Quan l'ESP32 arrenca, LMIC fa el procediment de join OTAA automàticament. El procediment és:

1. Genera un **DevNonce** aleatori.
2. Envia un **Join Request** a un canal aleatori de 868 MHz.
3. Escolta el **Join Accept** a RX1 (1 segon després) o RX2 (2 segons).
4. Si rep el Join Accept, deriva les claus de sessió (NwkSKey, AppSKey) i el DevAddr.
5. Si no, espera 30 segons i torna a provar.

El join pot trigar uns segons a completar-se. Mentrestant, el node no pot transmetre dades. Això és normal.

A la consola de TTN, podem veure els join requests a la pàgina del node, secció "Live data".

## 29.8 Deep sleep: la clau de la bateria

Per a ús amb piles, el deep sleep és fonamental. L'ESP32 pot entrar en deep sleep i consumir només ~10 µA. Es desperta amb:

- **Temporitzador**: cada X segons/minuts.
- **Interrupció externa**: canvi d'estat d'un pin (per exemple, un polsador).
- **Touchpad**: toc a un pin capacitiu.
- **ULP**: coprocessador que pot fer lectures simples.

Codi per entrar en deep sleep 5 minuts:

```cpp
esp_sleep_enable_timer_wakeup(5 * 60 * 1000000);  // 5 minuts en µs
esp_deep_sleep_start();
```

En el nostre cas, podem estructurar el programa així:

```cpp
void loop() {
    // Primer cop: setup() ja ha programat do_send()
    // do_send() transmet i després entra en deep sleep
}

// Modificar do_send() per entrar en deep sleep al final:
void do_send(osjob_t* j) {
    // ... llegir, codificar, transmetre ...
    Serial.println(F("Anant a dormir..."));
    Serial.flush();
    esp_sleep_enable_timer_wakeup(5 * 60 * 1000000);
    esp_deep_sleep_start();
}
```

Així, el cicle és: arrencada → join → llegir → transmetre → dormir 5 min → despertar → llegir → transmetre → dormir → ...

A la pràctica, l'ESP32 triga ~1-2 segons a despertar-se des de deep sleep, fer el join (que potser ja està fet, sinó fer-lo), llegir sensors, transmetre, i tornar a dormir. La majoria del temps, **el node està dormint**.

## 29.9 Bona gestió de la bateria

Algunes pràctiques:

- **Llegir el voltatge de la bateria** periòdicament i enviar-lo com a dada addicional.
- **Usar el màxim SF possible** quan el node dorm (per a transmissions ràpides).
- **Configurar l'ADR activat** (el NS optimitzarà els paràmetres).
- **Desactivar Wi-Fi i Bluetooth** si no es fan servir (ja ve per defecte en la majoria de llibreries).
- **Usar el mode de baix consum del SX1262** (es desactiva sol quan no transmet).
- **Evitar transmissions amb errors** (reintentar inútilment).

## 29.10 Logs i debug

Durant el desenvolupament, és important tenir bons logs:

```cpp
#define LMIC_DEBUG_LEVEL 1  // 0 = silenci, 1 = normal, 2 = molt
```

Això ensenya missatges interns de LMIC, útil per veure el procés de join, l'estat de les transmissions, etc.

També podem afegir un **LED** que indiqui l'estat:

```cpp
// LED parpelleja durant el join
// LED fix quan el join és complet
// LED parpelleja durant la transmissió
```

Per a depuració més avançada, podem afegir un **botó** que forci una transmissió immediata.

## 29.11 Primera càrrega del codi

Per carregar el codi a l'ESP32:

1. **Connectar l'ESP32** al PC per USB.
2. **Seleccionar la placa** a l'Arduino IDE: `Tools → Board → ESP32 Dev Module` (o `Heltec LoRa 32` si tens aquesta opció).
3. **Seleccionar el port**: `Tools → Port → COMx` (Windows) o `/dev/ttyUSBx` (Linux).
4. **Pujar el codi**: `Sketch → Upload`.
5. **Obrir el monitor sèrie**: `Tools → Serial Monitor` a 115200 baud.

Veurem els missatges del node: arrencada, intent de join, transmissió, etc.

## 29.12 Primera transmissió exitosa

Quan tot funciona, veurem a la consola de TTN:

1. A la pàgina del node, secció "Live data":
   - "Join request" → "Join accept"
   - Un uplink amb el payload

2. A la pàgina del gateway:
   - Un uplink rebut amb RSSI, SNR, etc.

3. A la integració MQTT:
   - Un missatge JSON al broker.

Si tot això passa, tenim un node LoRaWAN funcional!

## 29.13 Adaptació a altres sensors

Per afegir un sensor nou (per exemple, un sensor d'humitat del sòl), el codi canvia poc:

```cpp
// Definir el pin
#define SOIL_PIN 34

// A do_send():
int soilValue = analogRead(SOIL_PIN);
float soilPercent = map(soilValue, 0, 4095, 100, 0);  // Invertir: 0 = sec, 4095 = mullat
// O una corba de calibratge millor:
// float soilPercent = 100.0 * (4095 - soilValue) / 4095.0;

// Codificar CayenneLPP (canal 4)
uint8_t soil = (uint8_t)soilPercent;
payload[idx++] = 0x75;  // Tipus: humitat del sòl
payload[idx++] = 0x04;  // Canal: 4
payload[idx++] = soil;
```

I afegir-lo al payload formatter de TTN:

```javascript
case 0x75:  // Humitat del sòl
    var soil = input.bytes[i++];
    decoded.humitat_sol = soil;
    break;
```

## 29.14 Versió amb MicroPython

Si prefereixes MicroPython a Arduino, la sintaxi canvia però la lògica és similar. La llibreria LoRaWAN en MicroPython no és tan madura com en C, però per a prototips funciona.

Exemple amb MicroPython i una Heltec LoRa 32 V3:

```python
from machine import Pin, I2C, deepsleep
import time
import bme280
import ujson

# Pins
PIN_SS = 8
PIN_RST = 12
PIN_DIO0 = 14

# Inicialitzar BME280
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
bme = bme280.BME280(i2c=i2c)

# Inicialitzar LoRa (amb radio library específica de MicroPython)
# ... (cal instal·lar la llibreria de MicroPython per a SX126x)

while True:
    temperatura, pressio, humitat = bme.read_compensated_data()
    temperatura = temperatura / 100
    humitat = humitat / 1024
    pressio = pressio / 25600

    # Codificar CayenneLPP
    payload = bytes([
        0x67, 0x01,  # Temperatura canal 1
        (int(temperatura * 10) >> 8) & 0xFF, int(temperatura * 10) & 0xFF,
        0x68, 0x02,  # Humitat canal 2
        (int(humitat * 2) >> 8) & 0xFF, int(humitat * 2) & 0xFF,
        0x73, 0x03,  # Pressió canal 3
        (int(pressio * 10) >> 8) & 0xFF, int(pressio * 10) & 0xFF,
    ])

    # Transmetre
    lora.send(payload)

    # Deep sleep 5 minuts
    deepsleep(5 * 60 * 1000)
```

La versió Arduino és més madura i recomanada per a producció. MicroPython és bona per a prototipatge ràpid.

## 29.15 Errors habituals

**Error 1: identificadors incorrectes**. Símptoma: el join falla constantment. Solució: verificar DevEUI, AppEUI, AppKey.

**Error 2: pins incorrectes**. Símptoma: el SX1262 no es comunica. Solució: verificar els pins segons la placa.

**Error 3: no configurar la regió**. Símptoma: el node transmet però el gateway no el sent. Solució: afegir `LMIC_setRegion(LMIC_region_eu868)` (o similar per a la teva regió).

**Error 4: consum excessiu**. Símptoma: la bateria dura poc. Solució: entrar en deep sleep correctament, desactivar Wi-Fi i Bluetooth.

**Error 5: payload massa gran**. Símptoma: transmissió falla o es retarda. Solució: CayenneLPP compacte, no enviar JSON.

## 29.16 Resum

En aquest capítol hem après a programar un node LoRaWAN amb ESP32 i la llibreria MCCI LMIC. Hem vist el codi complet d'un node que llegeix BME280 i transmet cada 5 minuts en format CayenneLPP. Hem après a configurar el deep sleep per a baix consum, a gestionar la bateria, i a fer el debug amb logs. En el proper capítol veurem com rebre aquestes dades al BernatLab: TTN → Mosquitto → Telegraf → InfluxDB, i com visualitzar-les a Grafana.

## 29.17 Exercicis pràctics

1. Munta un circuit amb Heltec LoRa 32 V3 + BME280.
2. Instal·la Arduino IDE i les llibreries (LMIC, Adafruit BME280).
3. Configura el codi amb els TEUS DevEUI, AppEUI, AppKey.
4. Carrega el codi a l'ESP32.
5. Mira el monitor sèrie. Hauries de veure "Join success!" en uns segons.
6. A la consola de TTN, comprova que el node apareix com a "Connected".
7. Espera 5 minuts. Hauries de veure un uplink a "Live data".
8. Prova d'afegir un sensor d'humitat del sòl al codi.
9. Mesura el consum de corrent en deep sleep amb un multímetre.
10. Documenta al README el procés de flashing i el consum.

Paraules clau: **programació, codi, Arduino, ESP32, Heltec LoRa 32, LMIC, MCCI, RadioLib, CayenneLPP, payload, deep sleep, esp_sleep_enable, esp_deep_sleep, RTC, RAM persistent, timer wake-up, GPIO wake-up, deep sleep modes, ULP, coprocessador, sensor reading, I2C, SPI, GPIO, ADC, DAC, PWM, timer, interrupt, ISR, callback, FreeRTOS, task, queue, semaphore, mutex, ESP-IDF, Arduino framework, sketch, upload, monitor sèrie, port sèrie, COM, ttyUSB, baud, 115200, log, debug, LMIC_DEBUG_LEVEL, OTAA, ABP, DevEUI, AppEUI, AppKey, NWKSKEY, APPSKEY, DevAddr, DevNonce, join procedure, EU868, regió, data rate, SF, BW, TX power, ack, confirmed, unconfirmed, downlink, RX1, RX2, BME280, temperatura, humitat, pressió, sensor, I2C address, 0x76, 0x77, deep sleep wake-up, timer wake-up, low power, low energy, mAh, bateria, LiPo, 18650, TP4056, charging, battery voltage, ADC, analogRead, voltage divider, MOSFET, fuel gauge, INA219, INA260, coulomb counter, battery health, charge cycle, deep discharge, over-discharge, undervoltage, low battery, power management, sleep current, active current, average current, deep sleep current, wake-up time, boot time, startup time, frequency, clock, ESP32 clock, crystal, oscillator, RTC, real-time clock, external RTC, DS3231, PCF8523, time sync, NTP, time server, time protocol, timestamp, log timestamp, debug log, Serial.println, sprintf, format string, buffer, overflow, memory, heap, stack, fragmentation, watchdog, brown-out, panic, error handling, exception, fault, GDB, JTAG, debug, OCD, ESP-Prog, ESPtool, esptool.py, flash tool, firmware, bootloader, partition table, OTA, update over the air, FOTA, firmware update, secure boot, flash encryption, NVS, preferences, ESP32 preferences, LittleFS, SPIFFS, file system, SD card, microSD, data logging, local storage, send to server, queue, batch, retransmission, reliable, MQTT-SN, CoAP, LwM2M, lightweight, IoT protocol, application protocol, network protocol, transport protocol, MAC protocol, modulation, spreading, coding, error correction, FEC, interleaving, whitening, channel coding, source coding, compression, encryption, AES, CCM, integrity, MAC, message authentication, replay attack, sequence number, frame counter, MIC, message integrity code, frame integrity, data integrity, OTAA, ABP, session key, network key, application key, root key, join key, NwkKey, AppKey, MCKE, multicast key, multicast, group, multicast setup, FUOTA, firmware update over the air, multicast firmware update, class B, class C, downlink, RX1, RX2, receive window, RX1 delay, RX2 delay, dwell time, maximum payload, dwell time limitation, EU868 dwell time, ETSI EN 300 220, regional parameters, LoRaWAN regional parameters, RP001, RP002, LoRaWAN specification, LoRaWAN 1.0, LoRaWAN 1.0.2, LoRaWAN 1.0.3, LoRaWAN 1.0.4, LoRaWAN 1.1, MAC specification, regional parameters document, Lora Alliance, TS001, TS002, TS003, TS004, TS005, TS006, TS007, TS008, TS009, TS010, TS011, LoRaWAN L2 specification, layer 2, MAC layer, physical layer, PHY layer, application layer, application server, network server, join server, application session, network session, session context, MAC commands, fopts, FOpts, FOptsLen, FCtrl, frame control, frame header, FPort, FRMPayload, payload, MIC, message integrity check, B0, B1, B2, encryption, decryption, AES-128, AES-CMAC, CMAC, MIC calculation, MIC verification, packet validation, packet filtering, deduplication, desduplicació, replay protection, replay attack, frame counter, FCnt, FCntUp, FCntDown, frm_payload_size, payload size, maximum payload size, dwell time, time on air, airtime, transmission time, duty cycle, EU868 duty cycle, 1% duty cycle, 0.1% duty cycle, 10% duty cycle, sub-banda, 868.0-868.6, 868.7-869.2, 869.4-869.65, ETSI, ERC Recommendation 70-03, EN 300 220, ETSI EN 300 220-1, ETSI EN 300 220-2, regulator, telecom regulator, bandwidth, 125 kHz, 250 kHz, 500 kHz, channel, 868.1, 868.3, 868.5, 867.1, 867.3, 867.5, 867.7, 867.9, frequency plan, EU868 frequency plan, RX2 channel, RX2 data rate, default RX2, network server RX2, second receive window, RX2 frequency, RX2 DR, RX2 SF, RX2 BW, RX1 channel, RX1 DR, RX1 SF, RX1 BW, RX1 data rate, RX1 delay, receive delay, transmission timing, hop limit, MAC command, ADR, ADR bit, ADRACKReq, ADRACKCnt, LinkADRReq, LinkADRAns, DutyCycleReq, DutyCycleAns, RXParamSetupReq, RXParamSetupAns, DevStatusReq, DevStatusAns, NewChannelReq, NewChannelAns, RXTimingSetupReq, RXTimingSetupAns, Class B, ping slot, beacon, BCN, beacon frequency, beacon period, ping slot period, multicast, MCKS, multicast address, group address, FUOTA, fragmentation, file fragmentation, fragIndex, fragCount, MIC, integrity check, signed fragment, signature, EUI-64, EUI-48, dev nonce, join nonce, AppNonce, DevNonce, JoinNonce, LoRaWAN 1.0, LoRaWAN 1.1, LoRaWAN 1.0.4, LoRaWAN 1.0.3, LoRaWAN 1.0.2, application root key, root key, application key, network key, NwkKey, SNwkSIntKey, FNwkSIntKey, NwkSEncKey, AppSKey, root key, derivation, session key derivation, key derivation, KDF, key derivation function, session context, session state, security context, join server, network server, application server, separated AS, separated NS, separated JS, server architecture, distributed, monolithic, integrated, key management, key rotation, root key rotation, secure element, secure storage, hardware secure element, ATECC608, ATECC608A, secure element, ECC, elliptic curve, ECDSA, ECDH, signature, verification, secure boot, secure firmware, hardware root of trust, immutable bootloader, signed firmware, firmware signature, secure firmware update, FOTA, FUOTA, secure FOTA**.
