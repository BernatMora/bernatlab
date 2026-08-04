# Idees - Energia

> Projectes denviar i monitoratge energetic: consum electric, panells solars, batteries, autonomia.

## Idees

### Monitor de consum electric per endoll

- **Dificultat**: Mitjana-alta
- **Cost**: ~25 EUR
- **Temps**: 4-5 h
- **Components**: ESP32 + sensor de corrent SCT-013 + pantalla OLED
- **Utilitat real**: Mesurar el consum dun endoll concret (nevera, rentadora, ...).
- **Coneixements**: Sensors analogics, calibratge, transformadors de corrent, **precaucions amb 230 V**.
- **Integracio**: Les dades es poden enviar via MQTT a InfluxDB i visualitzar a Grafana.

**⚠️ ATENCIO**: cal saber que estas fent amb 230 V. Consulta un electricista si tens dubtes.

### Monitor de batteries LiPo amb alerta

- **Dificultat**: Mitjana
- **Cost**: ~20 EUR
- **Temps**: 3-4 h
- **Components**: ESP32 + divisor de tensio + sensor de corrent INA219
- **Utilitat real**: Mesurar el voltatge i el corrent de batteries LiPo en temps real.
- **Coneixements**: ADC, divisors de tensio, sensors de corrent, calibratge.
- **Integracio**: Es pot alertar quan la bateria es baixa.

### Carregador solar per a petits dispositius

- **Dificultat**: Mitjana
- **Cost**: ~30 EUR
- **Temps**: 4-5 h
- **Components**: ESP32 + panell solar 5V + TP4056 + bateria 18650 + sensor de voltatge
- **Utilitat real**: Carregar un mobil o una ESP32 amb energia solar.
- **Coneixements**: Panells solars, carregadors de bateria, autonomia.
- **Integracio**: Es pot combinar amb qualsevol projecte que necessiti autonomia.

### Estacio autonomous amb panell solar

- **Dificultat**: Mitjana-alta
- **Cost**: ~50 EUR
- **Temps**: 6-8 h
- **Components**: ESP32 + panell solar + TP4056 + 18650 + sensor de voltatge + caixa impermeabilitzada
- **Utilitat real**: Sistema sensor complet que funciona amb energia solar.
- **Coneixements**: Panells solars, batteries, autonomia, deep-sleep.
- **Integracio**: Es pot combinar amb qualsevol projecte de sensors.
