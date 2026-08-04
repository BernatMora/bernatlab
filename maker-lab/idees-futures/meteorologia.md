# Idees - Meteorologia

> Projectes destacio meteorologica personal: sensors ambientals, sensors de vent, pluviometria, radiacio solar.

## Idees

### Estacio meteorologica compacta amb BME280

- **Dificultat**: Baixa-mitjana
- **Cost**: ~25 EUR
- **Temps**: 3-4 h
- **Components**: ESP32 + BME280 (temperatura, humitat, pressio) + caixa impermeabilitzada
- **Utilitat real**: Estacio meteorologica personal al balco o pati.
- **Coneixements**: I2C, multi-sensor, deep-sleep, autonomia.
- **Integracio**: Es pot enviar via MQTT al sistema del BernatLab.

### Estacio amb sensor de vent i pluja

- **Dificultat**: Mitjana-alta
- **Cost**: ~50 EUR
- **Temps**: 6-8 h
- **Components**: ESP32 + anemometre + pluviometre + caixa
- **Utilitat real**: Mesurar vent i pluja a temps real.
- **Coneixements**: Interrupcions, comptatge, sensors, calibratge.
- **Integracio**: Es pot afegir a lestacio compacta.

### Alerta de gelada basada en temperatura

- **Dificultat**: Baixa
- **Cost**: ~15 EUR
- **Temps**: 2-3 h
- **Components**: ESP32 + DS18B20 + buzzer + bateria
- **Utilitat real**: Avisar quan la temperatura baixa per sota de 2 graus.
- **Coneixements**: Sensors, deep-sleep, alertes.
- **Integracio**: Es pot enviar via Telegram.

### Sensor de radiacio solar per a panells

- **Dificultat**: Mitjana
- **Cost**: ~25 EUR
- **Temps**: 3-4 h
- **Components**: ESP32 + sensor de radiacio solar (piranometre basic) + ADC extern
- **Utilitat real**: Mesurar la radiacio solar per optimitzar la collocacio de panells.
- **Coneixements**: ADC, sensors analogics, calibratge.
- **Integracio**: Es pot desar a InfluxDB i visualitzar a Grafana.

### Sensor de qualitat de l'aire (PM2.5 + CO2)

- **Dificultat**: Mitjana-alta
- **Cost**: ~50 EUR
- **Temps**: 6-8 h
- **Components**: ESP32 + sensor PMS5003 (PM2.5/PM10) + sensor MH-Z19 (CO2)
- **Utilitat real**: Mesurar la qualitat de laire a linterior o lexterior.
- **Coneixements**: UART, sensors avançats, calibratge.
- **Integracio**: Es pot integrar a un sistema domotic.
