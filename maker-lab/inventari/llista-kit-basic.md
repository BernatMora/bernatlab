# Llista detallada del kit basic recomanat

Aquesta es la llista exhaustiva del material que hauria de contenir el kit basic que compris per al Bernat Maker Lab. Busca a Amazon o AliExpress un **"Kit ESP32 amb sensors"** o **"Kit Arduino amb sensors"** amb valoracio >= 4,5 estrelles que inclogui el maxim d'aquesta llista.

## Per que aquesta llista

Esta dissenyada per cobrir els **5 nivells d'aprenentatge** del laboratori amb un sol kit (~25 EUR), sense necessitat de comprar mes coses fins a P3 o P4.

## Electronica basica (Nivell 1)

| Component | Quantitat | Per a que et servira |
|---|---|---|
| LEDs 5 mm assortits (vermell, groc, verd, blau) | 10-20 uts | P0, senyals, aprendre GPIO |
| Resistencies 1/4 W assortides (10 ohm a 1 M ohm) - kit 600 uts | 1 | Protegir LEDs, pull-up, pull-down, divisor de tensio |
| Polsadors / micro-switches | 5-10 uts | Entrades digitals, interrumptes, debouncing |
| Potenciometre 10 k ohm | 3 uts | Entrada analogica, control de brill |
| Protoboard 830 punts | 1 | Muntar circuits sense soldar |
| Cables Dupont M-M, M-F, F-F (kit 40+40+40) | 1 | Connexions a protoboard |
| Buzzer actiu 5 V i buzzer passiu | 1+1 | Audio, alarmes, melodies |
| Transistor NPN 2N2222 (o S8050) | 5 uts | Commutar carregues petites, entendre transistors |

## Sensors (Nivell 2)

| Component | Quantitat | Per a que et servira |
|---|---|---|
| **DHT22** (temperatura + humitat aire) - millor que DHT11 | 1 | Primer sensor daire. Calibrat decent. |
| **DS18B20** amb sonda metal·lica 1 m | 1 | Temperatura a distancia, bus 1-Wire, 1 sol pin per a molts sensors |
| **Fotoresistencia (LDR) GL55** | 1 | Mesurar llum, despertador solar, alarma |
| **Sensor d'humitat del sol capacitiu** v1.2 | 1 | Plantes, tests, hivernacles petits |
| Modul rele 5 V (1 canal, optoacoblador) | 1 | Primer pas cap a actuadors. Mai 230 V directe a l'ESP32! |

## Altres

| Component | Quantitat | Per a que et servira |
|---|---|---|
| Pantalla OLED 0,96" I2C (SSD1306) | 1 | Mostrar dades sense PC - molt satisfactori |
| Servomotor SG90 (9 g) | 1-2 | Primer motor, aprendre PWM, projectes mechanics senzills |
| Conversor de nivell logic 3,3 V ↔ 5 V (bidireccional, 4 canals) | 1 | Quan necessitis connectar coses a 5 V de forma segura |
| Brides, estoig, caixa plastica petita | 1 | Protegir la placa i organitzar cables |

## Marques recomanades (orientatives)

A Amazon.es solen aparixer aquests kits amb bona valoracio (canvien sovint):

- "Kit ESP32 amb sensors" - 22-28 EUR
- "Kit Arduino amb sensors" (comptabilitat amb ESP32) - 20-25 EUR
- "Kit basic electronica 830 punts" - 15-20 EUR

Important: **compra 2 plaques ESP32 DevKit v1 per separat** (~5-7 EUR cadascuna) si el kit nomes en porta una. Et caldran per a P2 i P3.

## Coses a NO comprar encara

- ESP32-S3 (~10-15 EUR) - per a projectes de visio (P5+).
- ESP32-CAM (~8-12 EUR) - per a visio artificial.
- ESP8266 (~4-6 EUR) - alternativa mes barata a lESP32 pero sense BLE.
- Pantalla tactil (~15-25 EUR) - per a projectes de HMI.
- Sensors cars (BME280, BMP280, etc.) - per a mesura precisa (P3+).
- Motors pas a pas, drivers - per a projectes mechanics grans.

---

*Ultima actualitzacio: 3 dagost del 2026.*
