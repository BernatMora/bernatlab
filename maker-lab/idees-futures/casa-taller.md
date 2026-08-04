# Idees - Casa i taller

> Projectes per a la casa o el taller: control dendolls, sensors de moviment, alarmes, automatitzacions.

## Idees

### Control dendolls Wi-Fi amb MQTT

- **Dificultat**: Mitjana
- **Cost**: ~15 EUR
- **Temps**: 3-4 h
- **Components**: ESP32 + modul rele 5V + caixa
- **Utilitat real**: Encendre i apagar llums o electrodomestics des del mobil.
- **Coneixements**: Wi-Fi, MQTT, control de carregues amb rele, **precaucions amb 230 V**.
- **Integracio**: Integrable amb Home Assistant i la RPi del BernatLab.

**⚠️ ATENCIO**: nomes per a endolls amb carregues segures (llums, carregadors). Per a carregues d'alta potència (radiadors, forns), cal un electricista.

### Sensor de moviment PIR amb alerta

- **Dificultat**: Baixa
- **Cost**: ~10 EUR
- **Temps**: 2 h
- **Components**: ESP32 + sensor PIR HC-SR501 + buzzer
- **Utilitat real**: Detectar moviment a una entrada o passadis.
- **Coneixements**: Sensors digitals, interrumptes, alertes.
- **Integracio**: Es pot afegir a un sistema dalarma local.

### Monitor de consum electric per endoll

- **Dificultat**: Mitjana-alta
- **Cost**: ~20 EUR
- **Temps**: 4-5 h
- **Components**: ESP32 + sensor de corrent SCT-013 + pantalla OLED
- **Utilitat real**: Mesurar el consum dun endoll concret (nevera, rentadora, ...).
- **Coneixements**: Sensors analogics, calibratge, transformadors de corrent, **precaucions amb 230 V**.
- **Integracio**: Les dades es poden enviar via MQTT a InfluxDB i visualitzar a Grafana.

**⚠️ ATENCIO**: cal saber que estas fent amb 230 V. Consulta un electricista si tens dubtes.

### Estacio meteorologica interior amb pantalla

- **Dificultat**: Baixa-mitjana
- **Cost**: ~20 EUR
- **Temps**: 3-4 h
- **Components**: ESP32 + DHT22 + BMP280 + OLED 0,96"
- **Utilitat real**: Mostrar temperatura, humitat i pressio a la sala destar.
- **Coneixements**: I2C, multi-sensor, pantalles OLED.
- **Integracio**: Es pot accedir via web per consultar des del mobil.

### Porta serial oberta al timbre

- **Dificultat**: Mitjana
- **Cost**: ~15 EUR
- **Temps**: 3-4 h
- **Components**: ESP32 + sensor magnetic + buzzer + RPi amb Telegram
- **Utilitat real**: Detectar quan sobri una porta i avisar al mobil.
- **Coneixements**: Interrupcions, sensors, integracio amb Telegram.
- **Integracio**: Es pot afegir a un sistema dalarma mes gran.
