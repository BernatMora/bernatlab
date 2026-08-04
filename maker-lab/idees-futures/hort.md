# Idees - Hort

> Projectes relacionats amb lhort. **Atencio**: aquestes idees son per al laboratori maker, no per al projecte de lhort que ja tens (que te la seva propia infraestructura amb HELTEC WiFi LoRa 32 V3 i RPi 4). Si vols fer alguna cosa relacionada amb lhort real, consulta primer linventari daquell projecte.

## Idees

### Sensor de gelades amb alerta Telegram

- **Dificultat**: Baixa
- **Cost**: ~15 EUR
- **Temps**: 2-3 h
- **Components**: ESP32 + DS18B20 + buzzer
- **Utilitat real**: Avisar abans que es congelin les plantes.
- **Coneixements**: Sensors, deep-sleep, Wi-Fi, integracio amb Telegram.
- **Integracio**: Es pot integrar amb el sistema de lhort (RPi + MQTT) o funcionar independent amb Wi-Fi de casa.

### Reg automatic per temps amb bot de control

- **Dificultat**: Mitjana
- **Cost**: ~30 EUR
- **Temps**: 4-6 h
- **Components**: ESP32 + rele + bomba petita 12V + sensor dhumitat del sol
- **Utilitat real**: Regar tests o un petit hivernacle.
- **Coneixements**: Actuadors (rele), sensors, deep-sleep, automatitzacio.
- **Integracio**: Es pot connectar via MQTT al sistema de lhort.

### Estacio meteorologica compacta

- **Dificultat**: Mitjana
- **Cost**: ~25 EUR
- **Temps**: 4-5 h
- **Components**: ESP32 + DHT22 + BMP280 + LDR + placa solar petita + caixa impermeabilitzada
- **Utilitat real**: Mesurar temperatura, humitat, pressio i llum solar al pati/balco.
- **Coneixements**: Multi-sensor, I2C, deep-sleep, autonomia amb solar.
- **Integracio**: Es pot enviar via MQTT al Grafana de lhort.

### Pluviometre digital

- **Dificultat**: Mitjana
- **Cost**: ~20 EUR
- **Temps**: 3-4 h
- **Components**: ESP32 + sensor reed + comptador d'impulsos + petit embut
- **Utilitat real**: Mesurar la pluja al pati o hort.
- **Coneixements**: Interrupcions, comptatge, calibratge.
- **Integracio**: Es pot afegir al sistema de lhort via MQTT.

### Timelapse automatic del creixement de les plantes

- **Dificultat**: Mitjana-alta
- **Cost**: ~30 EUR
- **Temps**: 6-8 h
- **Components**: ESP32-CAM + servo per moure la camera + tarjeta SD
- **Utilitat real**: Capturar el creixement d'una planta al llarg de setmanes.
- **Coneixements**: Visio, servo, automatitzacio amb temporitzador.
- **Integracio**: Les fotos es poden pujar a una web (com ja fas amb Hort Osona).
