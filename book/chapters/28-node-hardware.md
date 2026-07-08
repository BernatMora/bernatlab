# Capítol 28 — El node: ESP32 + SX1262, hardware i esquemes

> *"Un node LoRa és la combinació d'un cervell, uns sentits i una veu. El cervell és l'ESP32, els sentits són els sensors, i la veu és el SX1262."*

## 28.1 Què necessita un node

Un node LoRaWAN al camp ha de tenir:

1. **Un microcontrolador** per llegir sensors i prendre decisions.
2. **Un mòdul ràdio LoRa** per transmetre les dades.
3. **Un sensor o sensors** (temperatura, humitat, sòl, etc.).
4. **Una antena** per transmetre.
5. **Alimentació** (bateria, placa solar, USB, etc.).
6. **Una caixa estanca** per a ús a l'exterior.

Això és molt semblant al que ja coneixem de qualsevol sistema encastat (sistema encastat = sistema informàtic integrat en un altre producte). La diferència és que la transmissió és per ràdio, no per Wi-Fi o Bluetooth.

## 28.2 Per què ESP32

L'**ESP32** és la millor opció per a un node LoRa perquè:

- **Barat**: ~3-5 € una placa de desenvolupament amb Wi-Fi i Bluetooth integrats.
- **Potent**: dual-core 240 MHz, 520 KB de RAM, suficient per a la majoria de tasques.
- **Comunitat enorme**: llibreries per a gairebé tot, tutorials, fòrums.
- **Baix consum**: ~80 mA actiu, ~10 µA en deep sleep.
- **Moltes plaques amb LoRa integrat**: Heltec LoRa 32, TTGO LoRa, LILYGO T-Beam, etc.

Alternatives:

- **Raspberry Pi Pico + SX1262**: bona opció, però menys exemples LoRa.
- **STM32 + SX1262**: molt baix consum, però més complex de programar.
- **Arduino Nano + SX1262**: barat, però poca memòria per a la pila LoRaWAN.

## 28.3 Plaques ESP32 amb LoRa integrat

Aquestes plaques combinen ESP32 + SX1262 + antena + (sovint) pantalla OLED i connector de bateria. Són la millor opció per començar:

### Heltec LoRa 32 V3

- **ESP32-S3FN8** (dual-core 240 MHz, 8 MB flash, 512 KB RAM, 384 KB ROM).
- **SX1262** LoRa transceiver.
- **Pantalla OLED** de 0,96" (128×64).
- **Connector per a bateria LiPo** (amb circuit de càrrega).
- **Antena** externa amb IPEX/U.FL connector.
- **Preu**: ~25 €.

### TTGO LoRa (T-Beam, T-HiGrow, etc.)

Similar a Heltec, sovint amb GPS afegit en el cas del T-Beam. Una mica més cara (~30 €) però més opcions.

### LILYGO T3S3 / T-Deck

Plaques noves amb pantalles de color, millor consum, suport per a LoRaWAN i Meshtastic.

### Plaques "nues" (mòdul separat)

Si volem més flexibilitat, podem comprar:

- Un **ESP32-DevKit** estàndard (~5 €).
- Un **mòdul SX1262 breakout board** (~10 €).
- Cablejat manual (jumper wires, protoboard, o PCB).

Aquesta opció és més feina però permet personalitzar al 100 % la disposició.

## 28.4 Sensors

Depenent del que vulguem mesurar:

### BME280

- **Mesura**: temperatura, humitat, pressió.
- **Interfície**: I2C o SPI.
- **Precisió**: ±0.4 °C, ±3 % HR, ±1 hPa.
- **Preu**: ~3-5 €.
- **Ús**: un dels més comuns per a estacions meteorològiques.

### SHT31

- **Mesura**: temperatura, humitat.
- **Interfície**: I2C.
- **Precisió**: ±0.3 °C, ±2 % HR.
- **Preu**: ~3-5 €.

### DHT22 / AM2302

- **Mesura**: temperatura, humitat.
- **Interfície**: GPIO digital.
- **Precisió**: ±0.5 °C, ±2-5 % HR.
- **Preu**: ~2-3 €.
- **Ús**: molt popular, però menys precís i menys fiable que el BME280.

### Sensor d'humitat del sòl capacitiu

- **Mesura**: humitat del sòl (%).
- **Interfície**: analògica (0-3.3 V) o digital.
- **Preu**: ~1-3 €.
- **Ús**: clau per a Hort Osona.

### Sensor de llum (LDR o BH1750)

- **LDR** (Light Dependent Resistor): resistència variable segons la llum. Analògica, molt barata, però poc precisa.
- **BH1750**: digital, mesura lux. Més car (~2 €) però precís.

### Pluja (pluviòmetre)

Pluviòmetre tipus balancí: genera un impuls cada 0.2 mm de pluja. Es connecta a un pin d'interrupció de l'ESP32.

### Pressió (si no tenim BME280)

BMP280: pressió + temperatura (sense humitat). Més barat que BME280.

## 28.5 Connexió SX1262 a ESP32

Si usem una placa amb tot integrat (Heltec, TTGO), les connexions ja estan fetes. Si usem un mòdul separat, cal connectar:

| SX1262 | ESP32 | Funció |
|---|---|---|
| VCC | 3.3V | Alimentació (compte: 3.3V, no 5V) |
| GND | GND | Terra |
| SCK | GPIO 18 | SPI Clock |
| MISO | GPIO 19 | SPI MISO |
| MOSI | GPIO 23 | SPI MOSI |
| NSS / CS | GPIO 5 | Chip Select |
| RST | GPIO 14 | Reset |
| DIO1 | GPIO 26 | Interrupció |
| BUSY | GPIO 27 | Busy (opcional) |

Aquests pins són els valors per defecte a la majoria de llibreries. Es poden canviar per software.

## 28.6 Esquema elèctric

Per a una versió amb ESP32-DevKit + SX1262 breakout + BME280:

```
ESP32          SX1262
  3.3V  -------  VCC
  GND   -------  GND
  GPIO18-------  SCK
  GPIO19-------  MISO
  GPIO23-------  MOSI
  GPIO5 -------  NSS
  GPIO14-------  RST
  GPIO26-------  DIO1
  GPIO27-------  BUSY

ESP32          BME280
  3.3V  -------  VCC
  GND   -------  GND
  GPIO21-------  SDA  (I2C Data)
  GPIO22-------  SCL  (I2C Clock)
```

Això és el bàsic. Si volem afegir un sensor d'humitat del sòl, connectem el seu pin analògic (AO) a un pin ADC de l'ESP32 (per exemple, GPIO34).

## 28.7 Alimentació

Per a ús al camp, tenim diverses opcions:

### Bateria LiPo + placa solar

- **Bateria**: 3.7V LiPo 18650 (3000-3500 mAh) o LiPo petita.
- **Placa solar**: 5-6V, 1-2W.
- **Carregador**: TP4056 o integrat a la placa (Heltec ja en porta).
- **Autonomia**: amb bones pràctiques, mesos o anys.

### USB

- **Font**: carregador de mòbil, 5V 1A.
- **Ús**: interior, prototipatge, proves.

### 4 piles AA

- **Voltatge**: 4 × 1.5V = 6V (necessitem un regulador a 3.3V o 5V).
- **Capacitat**: ~2500-3000 mAh.
- **Ús**: per a proves a l'hort a curt termini.

### Bateria fixa (12V, tipus bateria de cotxe o solar)

- Per a instal·lacions permanents amb consum moderat.

### Optimització de consum

Per allargar la vida de la bateria:

- **Deep sleep** entre transmissions: l'ESP32 consumeix ~10 µA en deep sleep.
- **Transmetre poc sovint**: cada 5-15 minuts és un bon equilibri.
- **Usar SF baixos** quan sigui possible: menys temps de transmissió.
- **Llegir sensors només quan calgui**: durant el deep sleep, no caldrà.
- **Apagar perifèrics no usats**: Wi-Fi, Bluetooth, etc.

## 28.8 Caixa estanca

Per a ús a l'exterior, necessitem una **caixa estanca IP65 o superior**. Opcions:

- **Caixa de plàstic ABS**: barata, fàcil de perforar, IP65 si està ben tancada.
- **Caixa d'alumini**: més cara, més robusta, millor dissipació de calor.
- **Caixa de polièster reforçat amb fibra de vidre**: per a instal·lacions professionals.

A la caixa, cal:

- **Forats per a l'antena**: segellat amb cautxú o silicona.
- **Forats per al sensor d'humitat del sòl**: perquè el sensor sobresurti.
- **Ventilació**: per evitar condensació a l'interior. Una mena de filtre Gore-Tex ajuda.
- **Accés per a la bateria**: per poder-la canviar.

## 28.9 Posada en marxa

Quan tinguem tot el hardware:

1. **Soldar o connectar** l'antena al mòdul SX1262 (o a la placa).
2. **Carregar el codi** a l'ESP32 (veure capítol 29).
3. **Configurar DevEUI, AppEUI, AppKey** amb els valors generats per TTN.
4. **Verificar** que el node es connecta a la xarxa (veure monitor serie).
5. **Posar-lo a la caixa** estanca.
6. **Muntar-lo al camp** amb bona posició per a l'antena.

## 28.10 Proves inicials

Abans de posar el node al camp, cal validar:

1. **El node arrenca correctament**: LED encén, missatge al port sèrie.
2. **L'antena està connectada**: sense antena, podem cremar el mòdul!
3. **El node es connecta a la xarxa LoRaWAN**: veure missatges "JOINED" al log.
4. **El node transmet dades**: veure els uplink a la consola de TTN.
5. **Les dades són correctes**: temperatura, humitat, etc., en els rangs esperats.
6. **El deep sleep funciona**: deixar-lo una nit, comprovar que la bateria dura.

## 28.11 Errors habituals

**Error 1: antena no connectada**. Símptoma: el mòdul es queda "penjat" o es crema. Solució: SEMPRE connectar l'antena abans d'encendre.

**Error 2: tensió d'alimentació incorrecta**. Símptoma: el node es reinicia aleatòriament, o no arrenca. Solució: verificar que la font d'alimentació és 3.3V (per al SX1262) i prou potent (almenys 500 mA).

**Error 3: pins SPI mal connectats**. Símptoma: el node no es comunica amb el SX1262. Solució: verificar les connexions amb un multímetre.

**Error 4: deep sleep massa profund**. Símptoma: el node no es desperta. Solució: verificar que la interrupció DIO1 està ben connectada.

**Error 5: freqüència incorrecta**. Símptoma: el node transmet, però el gateway no el sent. Solució: verificar que el node està configurat per a EU868 (no US915 o AS923).

## 28.12 Resum

En aquest capítol hem vist el hardware del node LoRa: ESP32 + SX1262 + sensors, amb l'esquema elèctric, les opcions d'alimentació, la caixa estanca, i els passos de posada en marxa. Hem après quins sensors són útils per a Hort Osona i com connectar-los. En el proper capítol programarem el node: codi per a ESP32 amb la llibreria LMIC o RadioLib, transmissió de dades en format CayenneLPP, deep sleep, i bones pràctiques de consum.

## 28.13 Exercicis pràctics

1. Compra una placa ESP32 amb LoRa (Heltec LoRa 32 V3 recomanada).
2. Compra un sensor BME280.
3. Munta el circuit a una protoboard.
4. Connecta l'antena.
5. Carrega un codi d'exemple que llegeixi el BME280 i mostri les dades pel port sèrie.
6. Mesura el consum de corrent amb un multímetre.
7. Implementa deep sleep i mesura el consum en sleep.
8. Documenta al README el hardware del node, els pins, i el consum.

Paraules clau: **ESP32, ESP32-S3, SX1262, Heltec LoRa 32, TTGO LoRa, LILYGO T-Beam, T-Deck, sensor, BME280, SHT31, DHT22, humitat del sòl, LDR, BH1750, pluja, pluviòmetre, balancí, pinout, SPI, I2C, GPIO, ADC, 3.3V, alimentació, LiPo, 18650, TP4056, placa solar, deep sleep, baix consum, caixa estanca, IP65, ABS, alumini, antena, IPEX, U.FL, SMA, soldar, multímetre, consum, mA, µA, deep sleep, watchdog, RTOS, Arduino, ESP-IDF, MicroPython, PlatformIO, IDE, sketch, port sèrie, monitor, debug, ESP-Prog, ESPtool, flashing, firmware, bootloader, partition table, OTA, update, deep sleep wake-up, GPIO wake-up, timer wake-up, sensor reading, I2C scanning, SPI initialization, GPIO configuration, interrupt, ISR, callback, millis(), micros(), delay, Scheduler, FreeRTOS, task, queue, semaphore, mutex, ESP_LOG, ets_printf, log levels, error handling, watchdog timer, brown-out detector, ESP32-C3, ESP32-S2, ESP32-S3, ESP32-C6, variants, deep sleep modes, RTC memory, ULP, coprocessor, ULP wake-up, ext0, ext1, touch wake-up, ulp wake-up, gpio wake-up, timer wake-up, Wi-Fi, Bluetooth, BLE, ESP-NOW, LoRa, SX1276, SX1278, SX1262, SX1268, RFM95, RFM96, RF69, HopeRF, Ai-Thinker, Ra-02, Semtech, modulation, OOK, FSK, GFSK, MSK, GMSK, LoRa, FSK, OOK, packet, radio, antenna, impedance matching, balun, SAW filter, low-pass filter, matching network, RF path, ground plane, EMI, RFI, EMC, compliance, ETSI, FCC, modular approval, regulatory, certification, IP rating, IP65, IP67, IP68, IP69K, UV resistance, temperature range, operating temperature, storage temperature, humidity, condensation, venting, Gore-Tex, vent plug, desiccant, silica gel, anti-condensation heater, condensation prevention, self-heating, solar heating, heat dissipation, thermal management, sun exposure, black box, white box, UV-stabilized, weatherproof, weather-resistant, outdoor enclosure, junction box, ABS enclosure, polycarbonate enclosure, fiberglass enclosure, stainless steel enclosure, aluminum enclosure, mounting bracket, pole mount, wall mount, ground mount, mast mount, weatherhead, cable gland, strain relief, IP68 cable gland, cable entry, sealing, silicone sealant, hot melt glue, epoxy, potting, conformal coating, PCB protection, marine-grade, salt-spray resistant, anti-corrosion, anodized, powder-coated, paint, primer, mounting hardware, U-bolts, hose clamps, screws, anchors, washers, nuts, security screws, tamper-proof, locking, key, lock, hasp, padlock, security, theft prevention, vandalism, lockable enclosure, locking mechanism, latch, clasp, hinge, gasket, O-ring, rubber gasket, foam gasket, IP-rated, IP65, IP66, IP67, IP68, IP69K, NEMA 4, NEMA 4X, NEMA 6, NEMA 6P, outdoor, indoor, indoor/outdoor, dry location, wet location, damp location, hazardous location, Class I Div 1, Class I Div 2, explosion-proof, intrinsically safe, IS, Ex, ATEX, IECEx, hazardous area, gas group, dust group, temperature class, T1, T2, T3, T4, T5, T6, T-class, surface temperature, maximum temperature, ignition temperature, flammable, combustible, hazardous materials, industrial environment, marine environment, coastal environment, salt water, salt spray, corrosion, rust, oxidation, galvanic corrosion, dissimilar metals, electrolytic, electrical isolation, barrier, isolation, insulation, weatherhead, drip loop, cable loop, condensation drain, weep hole, drainage, ventilation, breather, vent plug, Gore-Tex, Goretex, GORE-TEX, expanded PTFE, ePTFE, hydrophobic, oleophobic, breathable, IP-rated vent, screw-in vent, push-in vent, adhesive vent**.
