# Estat actual del projecte LoRa (Hort Osona)

> Última actualització: 2026-07-09

## Maquinari

### Node de camp (l'hort)
- **Heltec WiFi LoRa 32 V3** — ESP32-S3 + SX1262 + OLED integrada
- **Bateria Li-Po 3.7V** disponible
- **Sensor capacitiu d'humitat del sòl v1.2**
- **Sensor de temperatura DS18B20** impermeable

### Receptor (casa)
- **Raspberry Pi 4** amb **Waveshare LoRa HAT**
- Mòdul **E22-900T22S** (EBYTE, 868 MHz)
- Connexió per **UART** (no SPI)

## Configuració aconseguida

### Heltec (al Mac amb Arduino IDE)
- Port: `/dev/cu.usbserial-0001`
- Placa: WiFi LoRa 32(V3)
- Comunicació sèrie a 115200 baud
- OLED funciona
- Alimentació Vext funciona
- Programa de prova carregat correctament

### Raspberry Pi
- Accessible per SSH: `bernat@hortosona`
- UART habilitat: `enable_uart=1`
- Port sèrie: `/dev/serial0 -> /dev/ttyS0`
- Servei de consola sèrie: inactiu (correcte)
- Usuari `bernat` al grup `dialout`
- Selector del HAT: posició **B (Pi-LoRa)**
- Pins E22 en mode normal (M0=GND, M1=GND)

## Pendent

1. Soldar o connectar el sensor d'humitat a la Heltec
2. Llegir valors RAW amb sensor a l'aire, terra seca i terra humida
3. Calibrar la lectura en percentatge
4. Afegir el sensor DS18B20
5. Programar la Heltec per enviar dades per LoRa
6. Rebre dades al E22-900T22S de la RPi
7. Publicar a MQTT, InfluxDB, Grafana i Hort Osona

## Arquitectura
HORT Sensor humitat + DS18B20 ↓ Heltec WiFi LoRa 32 V3 ↓ LoRa 868 MHz ↓ CASA Waveshare E22-900T22S ↓ UART ↓ Raspberry Pi ↓ MQTT / Node-RED / InfluxDB / Grafana / Hort Osona
