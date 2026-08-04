# Idees - Seguretat

> Projectes de seguretat i monitoratge: alarmes locals, sensors dapertura, cameras, notificacions.

## Idees

### Alarma local per a porta doberta

- **Dificultat**: Baixa
- **Cost**: ~15 EUR
- **Temps**: 2-3 h
- **Components**: ESP32 + sensor magnetic dobertura + buzzer + bateria
- **Utilitat real**: Alarma si una porta es queda oberta mes de X minuts.
- **Coneixements**: Sensors, timers, logica condicional.
- **Integracio**: Es pot conectar via Wi-Fi a la RPi per enviar una alerta Telegram.

### Detector de presencia amb PIR i camera

- **Dificultat**: Mitjana-alta
- **Cost**: ~50 EUR
- **Temps**: 6-8 h
- **Components**: ESP32-CAM + sensor PIR + caixa + targeta SD
- **Utilitat real**: Quan detecta moviment, fa una foto i la guarda o envia.
- **Coneixements**: Visio, sensors, I/O, gestio dimatges.
- **Integracio**: Les fotos es poden pujar a la RPi per veure-les des del mobil.

### Camara espia amb timelapse

- **Dificultat**: Mitjana
- **Cost**: ~30 EUR
- **Temps**: 4-5 h
- **Components**: ESP32-CAM + bateria + caixa
- **Utilitat real**: Fer fotos cada N minuts per monitorar un espai.
- **Coneixements**: Timers, visio, autonomia amb bateria.
- **Integracio**: Es pot conectar via Wi-Fi a la RPi per desar les fotos a una carpeta compartida.

### Sensor de vibracio per a finestres

- **Dificultat**: Baixa-mitjana
- **Cost**: ~15 EUR
- **Temps**: 2-3 h
- **Components**: ESP32 + sensor de vibracio SW-420 + buzzer
- **Utilitat real**: Detectar intents de trencar una finestra.
- **Coneixements**: Sensors, interrumptes, calibratge de sensibilitat.
- **Integracio**: Es pot afegir a un sistema dalarma mes gran.

### Alarma per a la nevera (porta oberta)

- **Dificultat**: Baixa
- **Cost**: ~10 EUR
- **Temps**: 1-2 h
- **Components**: ESP32 + sensor magnetic + buzzer
- **Utilitat real**: Avisar si la porta de la nevera sha quedat oberta.
- **Coneixements**: Sensors, timers, logica condicional.
- **Integracio**: Es pot conectar a la RPi per avisarte al mobil.

### Sistema dalarma modular amb MQTT

- **Dificultat**: Alta
- **Cost**: ~80 EUR
- **Temps**: 10-15 h
- **Components**: Multiples ESP32 amb sensors (PIR, magnetico, vibracio) + RPi amb Home Assistant
- **Utilitat real**: Alarma completa modular amb notificacions al mobil.
- **Coneixements**: MQTT, Home Assistant, multi-node, automatitzacions.
- **Integracio**: Integracio completa amb el sistema existent del BernatLab.
