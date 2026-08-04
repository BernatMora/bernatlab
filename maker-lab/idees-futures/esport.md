# Idees - Esport

> Projectes per a esport i activitats a laire lliure: sensors de moviment, GPS, telemetria, dispositius per a bicicleta, trail o kitesurf.

## Idees

### Velocimetre i cadenciometre per a bicicleta

- **Dificultat**: Mitjana
- **Cost**: ~25 EUR
- **Temps**: 4-5 h
- **Components**: ESP32 + sensor magnetic de roda + imant + pantalla OLED
- **Utilitat real**: Mesurar velocitat instantania i cadencia de pedaleig.
- **Coneixements**: Interrupcions, comptatge, calibratge.
- **Integracio**: Es pot desar a una SD i baixar les dades al PC.

### GPS tracker per a trail running

- **Dificultat**: Mitjana-alta
- **Cost**: ~40 EUR
- **Temps**: 6-8 h
- **Components**: ESP32 + modul GPS NEO-6M + targeta SD + bateria LiPo
- **Utilitat real**: Registrar el recorregut durant una cursa o sortida.
- **Coneixements**: UART, GPS, emmagatzematge, autonomia amb bateria.
- **Integracio**: Les dades es poden convertir a GPX i visualitzar a OSM o Google Earth.

### Dispositiu de telemetria per a kitesurf

- **Dificultat**: Alta
- **Cost**: ~50 EUR
- **Temps**: 8-10 h
- **Components**: ESP32 + IMU MPU9250 (accelerometre + giroscopi + magnetometre) + SD
- **Utilitat real**: Mesurar la inclinacio del pal, les forres G i la velocitat.
- **Coneixements**: I2C, IMU, processament de senyal, fusio sensorial.
- **Integracio**: Es pot conectar via BLE a un mobil per veure les dades en temps real.

### Analitzador de salts i temps de vol

- **Dificultat**: Mitjana
- **Cost**: ~30 EUR
- **Temps**: 4-5 h
- **Components**: ESP32 + accelerometre LIS3DH + buzzer + bateria
- **Utilitat real**: Mesurar laltura dun salt i el temps de vol.
- **Coneixements**: I2C, processament de senyal, calibratge.
- **Integracio**: Es pot conectar a un mobil via BLE per veure lestadistica.

### Dispositiu anti-oblit per a casc de bici

- **Dificultat**: Mitjana
- **Cost**: ~25 EUR
- **Temps**: 4-5 h
- **Components**: ESP32 + accelerometre + buzzer + bateria
- **Utilitat real**: Avisar-te si has deixat el casc a algun lloc.
- **Coneixements**: I2C, deep-sleep, BLE, logica destat.
- **Integracio**: Es pot conectar al mobil per rebre alertes quan allunyas.
