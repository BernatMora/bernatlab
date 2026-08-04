# Capitol 70 - Bernat Maker Lab: afegir nova maquinaria al laboratori

> *"Un homelab no es nomes servidors. Es tambe la maquina que donas forma amb les teves mans."*

## 70.1 Que es el Bernat Maker Lab

El **Bernat Maker Lab** es la part del projecte dedicada a **aprendre electronics, programacio de microcontroladors i disseny de dispositius propis** amb plaques com l'ESP32, l'ESP8266, l'Arduino, la Raspberry Pi Pico i similars.

Es diferencia del BernatLab "classic" (servidors, Docker, IA) en que aqui el focus es:

- **Aprendre fent** - cada capitol acaba amb un projecte que funciona.
- **Construit per tu** - el codi, els esquemes i les decisions son teus, no pas presets d'un fabricant.
- **Local-first** - la regla es que tot funcioni a la teva xarxa local, sense dependre del nuvol.
- **Documentat com un llibre** - cada projecte es converteix en un capitol del curs, amb resum, quiz, exercici i respostes.

Aquest capitol es la **porta d'entrada** al Maker Lab dins del llibre. La part practica esta al **curs M9** (resum + quiz + exercici + respostes) i la part operativa (codi, esquemes, decisions) viu a la carpeta `maker-lab/` del repositori.

## 70.2 Per que un laboratori maker a mes del servidor

Tres motius:

1. **Aprendre electronics** - un servidor es software. Un microcontrolador es hardware + software. Les dues cares s'aprenen.
2. **Construir coses noves** - sensors, llums, alarmes, panells interactius, robots petits, instruments musicals, ... tot el que pots imaginar i muntar amb una placa de 5 EUR i un manat de components.
3. **Descobrir limitacions** - un servidor pot fer moltes coses, pero mai mouras un motor, llegiras un sensor d'humitat del sol o encendras un LED a 50 metres amb ells. Els microcontroladors si.

## 70.3 Que tens a la taula (inventari inicial)

| Component | Quantitat | On |
|---|---|---|
| ESP32 DevKit v1 (xip ESP32-WROOM-32) | 2 | Kit basic (~10-14 EUR) |
| LED 5 mm assortits | 10-20 | Kit basic |
| Resistencies 1/4 W assortides (10 ohm a 1 M ohm) | 600 | Kit basic |
| Polsadors / micro-switches | 5-10 | Kit basic |
| Potenciometre 10 k ohm | 3 | Kit basic |
| Protoboard 830 punts | 1 | Kit basic |
| Cables Dupont (M-M, M-F, F-F) | 40+40+40 | Kit basic |
| Buzzer actiu 5 V + buzzer passiu | 1+1 | Kit basic |
| Transistor NPN 2N2222 (o S8050) | 5 | Kit basic |
| DHT22 (temperatura + humitat aire) | 1 | Kit basic |
| DS18B20 amb sonda metal·lica 1 m | 1 | Kit basic |
| Fotoresistencia (LDR) GL55 | 1 | Kit basic |
| Sensor d'humitat del sol capacitiu v1.2 | 1 | Kit basic |
| Modul rele 5 V (1 canal, optoacoblador) | 1 | Kit basic |
| Pantalla OLED 0,96" I2C (SSD1306) | 1 | Kit basic |
| Servomotor SG90 (9 g) | 1-2 | Kit basic |
| Conversor de nivell logic 3,3 V <-> 5 V | 1 | Kit basic |
| Multimete digital basic | 1 | **Obligatori** comprar (~10-15 EUR) |

**Pressupost total del laboratori:** uns 35-50 EUR (kit + multimete).

**Important:** cap d'aquestes peces es compartida amb el projecte de l'hort. L'hort te la seva propia infraestructura (HELTEC WiFi LoRa 32 V3, RPi 4, etc.). Al Maker Lab comencem des de zero.

## 70.4 Els 5 nivells d'aprenentatge

El laboratori s'organitza en 5 nivells progressius. Cada nivell acaba amb un projecte que funciona abans de passar al seguent.

### Nivell 1 - Fonaments

- Que es un microcontrolador i com es diferencia d'un PC.
- Que es un GPIO i com es fan servir.
- Com muntar un circuit a la protoboard.
- Com programar i carregar un firmware a l'ESP32.
- Comandes basiques: `pinMode`, `digitalWrite`, `digitalRead`, `delay`.
- **Projecte final:** encendre un LED amb un programa (Blink) i des d'una pagina web.

### Nivell 2 - Sensors i actuadors

- Lectura de sensors basics (temperatura, humitat, llum).
- Sortides analogiques amb PWM.
- Busos I2C, SPI, UART.
- Us de transistors i relays per a carregues petites.
- **Projecte final:** llegir un sensor ambient (DHT22 o DS18B20) i mostrar-lo a una pagina web amb grfica.

### Nivell 3 - Comunicacions

- Wi-Fi i Bluetooth de l'ESP32.
- MQTT (aixo ja esta explicat al cap 12 del M2 del llibre - s'hi connecta).
- HTTP i APIs.
- ESP-NOW per comunicar ESP32 entre elles sense router.
- LoRa per a llarg abast (aixo tambe esta al M3 del llibre).
- **Projecte final:** dues ESP32 que es comuniquen via MQTT a traves d'un broker.

### Nivell 4 - Aplicacions completes

- Integracio amb la Raspberry Pi (ja explicat al M2 del llibre).
- Base de dades de series temporals (InfluxDB, ja explicat al M2).
- Grafana o un panell web propi.
- Alertes.
- Actualitzacio remota del firmware.
- **Projecte final:** sistema sensor complet amb panell web accessible des del mobil.

### Nivell 5 - Sistemes intelligents

- Analisi de dades.
- Detecccio d'anomalies.
- Visio artificial amb ESP32-CAM.
- Control per veu.
- IA local (Ollama, ja explicat al M4 del llibre).
- Automatitzacions basades en context.
- **Projecte final:** un sistema que prengui decisions a partir de les dades dels sensors.

## 70.5 Els 5 primers projectes (P0 a P4)

Aquest son els projectes **inicials** del laboratori. P0 esta desenvolupat al curs M9. P1-P4 s'aniran afegint a mesura que els facis servir.

| Codi | Nom | Nivell | Durada |
|---|---|---|---|
| **P0** | Blink + LED via web | 1 | 1-2 h |
| **P1** | Termometre amb pagina web | 2 | 2-3 h |
| **P2** | Dos ESP32 amb polsador i LED creuat | 2 | 3-4 h |
| **P3** | MQTT entre ESP32 i Raspberry Pi | 3 | 4-5 h |
| **P4** | Panell web propi a la Raspberry | 4 | 6-8 h |

## 70.6 Arquitectura del sistema

```
+--------------------------------------------------+
|                  Xarxa local                      |
|                                                   |
|   +-------------+         +-------------------+   |
|   |  ESP32 #1   |         |   ESP32 #2        |   |
|   |  P0/P1/P2   |         |   P2 (cross-LED)  |   |
|   |  (LED,      |         |                   |   |
|   |   sensor)   |         |                   |   |
|   +-----+-------+         +---------+---------+   |
|         | Wi-Fi                     | Wi-Fi       |
|         |                           |             |
|         +-------------+-------------+             |
|                       |                           |
|                       v                           |
|              +-----------------+                  |
|              |   Raspberry Pi  |                  |
|              |   4 (o PC)      |                  |
|              |  +------------+ |                  |
|              |  | Broker     | |                  |
|              |  | MQTT       | |                  |
|              |  +------------+ |                  |
|              |  | InfluxDB   | |                  |
|              |  +------------+ |                  |
|              |  | Panell web | |                  |
|              |  +------------+ |                  |
|              +--------+--------+                  |
|                       |                           |
+-----------------------+---------------------------+
                        |
                        v
                +---------------+
                |   iPhone /    |
                |   PC client   |
                +---------------+
```

**Regles d'or:**

- L'**ESP32** es el node de camp: llegeix sensors, mou actuadors, decideix coses rapides. No hi posem la logica de negoci.
- La **Raspberry Pi** es el cervell local: broker, base de dades, panell web, possibles automatismes complexos.
- L'**iPhone / PC** es la interficie humana.
- **Tot funciona local**. El nuvol es opcional.

## 70.7 Eines de programacio

| Eina | Pros | Contres |
|---|---|---|
| **Arduino IDE** | Senzill, molta documentacio, llibreries per a tot. | Editor basic, projectes grans es fan pesats. |
| **PlatformIO (VSCode)** | Professional, integracio amb Git, gestor de dependencies. | Mes complex d'entrar-hi. |
| **MicroPython** | Python en lloc de C++, iteracio rapidissima. | Menys exemples, mes limitat en algunes coses. |
| **ESPHome** | Integracio directa amb Home Assistant, molt practic. | Menys flexible, lligat a un ecosistema. |
| **C++ amb ESP-IDF** | Maxim control, optimitzacio extrema. | Molt mes complex. |

**Recomanacio inicial:** Arduino IDE. Es la porta mes suau. Es podra canviar a PlatformIO quan els projectes siguin grans.

## 70.8 Seguretat electrica (la part mes important)

Mai oblidis aquestes regles:

1. **Mai connectis 230 V directament a l'ESP32** ni a cap GPIO. Un sol error pot cremar la placa o electrocutar-te.
2. **Mai connectis 5 V a un GPIO de l'ESP32** - es 3,3 V. Usa un conversor de nivell logic si cal.
3. **Sempre una resistencia en serie amb un LED** - 220-330 ohm es l'estandard.
4. **Desconnecta l'ESP32 abans de canviar el circuit** - evita curtcircuits.
5. **Per a carregues de 230 V** usa moduls de rele amb optoacobladors i, si tens dubtes, consulta un electricista qualificat.
6. **Mai treballis amb 230 V si estas sol** o mullat o distret.
7. **Un multimete es obligatori**, no opcional. Sense ell, no pots saber quines tensions i corrents tens al circuit.

## 70.9 Connexions amb altres parts del BernatLab

- **Curs M9 (Bernat Maker Lab)** - aqui es on viuen els capitols practics amb resum, quiz, exercici i respostes.
- **Cap 12 (MQTT des de zero)** - el protocol que farem servir a P3.
- **Cap 15 (InfluxDB)** - la base de dades de series temporals per a P3 i P4.
- **Cap 20 (API publica)** - com fer el panell web propi per a P4.
- **Cap 23-32 (M3 del llibre - LoRa)** - per quan vulguis fer nodes a llarga distancia.

## 70.10 Per on començar

1. **Llegeix el resum del capitol M9.1** (Blink + LED via web) a `book/curs/M9/01-blink-i-led-via-web/resum.md`.
2. **Fes el questionari** per validar que ho has entes.
3. **Fes l'exercici practic** - munta el circuit, flasheja la placa, obre la pagina web.
4. **Fes una captura de pantalla** del resultat.
5. **Quan tot funcioni**, ja tens P0 fet. Passa a P1.
