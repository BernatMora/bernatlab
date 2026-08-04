# Idees - Cameras i visio

> Projectes amb cameras i visio per computador: ESP32-CAM, deteccio de moviment, timelapses.

## Idees

### Camara IP local amb ESP32-CAM

- **Dificultat**: Baixa-mitjana
- **Cost**: ~15 EUR
- **Temps**: 3-4 h
- **Components**: ESP32-CAM + targeta SD + font dalimentacio
- **Utilitat real**: Stream de video a la xarxa local, accessible des del mobil.
- **Coneixements**: Visio, Wi-Fi, streaming, configuracio de xarxa.
- **Integracio**: Es pot visualitzar des del panell web del BernatLab.

### Timelapse de la posta de sol

- **Dificultat**: Mitjana
- **Cost**: ~20 EUR
- **Temps**: 4-5 h
- **Components**: ESP32-CAM + caixa impermeabilitzada + font dalimentacio
- **Utilitat real**: Capturar una posta de sol cada N segons i muntar un timelapse.
- **Coneixements**: Visio, timers, gestio dimatges.
- **Integracio**: Les fotos es poden muntar a un video automaticament.

### Detector de moviment amb ESP32-CAM

- **Dificultat**: Mitjana
- **Cost**: ~20 EUR
- **Temps**: 4-5 h
- **Components**: ESP32-CAM + sensor PIR + targeta SD
- **Utilitat real**: Quan detecta moviment, fa una foto i la desa.
- **Coneixements**: Visio, sensors, I/O, gestio dimatges.
- **Integracio**: Es pot integrar a un sistema dalarma.

### Porta-retrats digital amb ESP32-CAM

- **Dificultat**: Mitjana
- **Cost**: ~40 EUR
- **Temps**: 6-8 h
- **Components**: ESP32-CAM + pantalla TFT + caixa impresa en 3D
- **Utilitat real**: Mostrar fotos que canvien cada X temps.
- **Coneixements**: Visio, pantalles, gestio dimatges, disseny industrial.
- **Integracio**: Es pot actualizar via Wi-Fi.

### Escaneig 3D basic amb ESP32-CAM i servo

- **Dificultat**: Alta
- **Cost**: ~30 EUR
- **Temps**: 10-15 h
- **Components**: ESP32-CAM + 2 servos + estructura mecanica
- **Utilitat real**: Escaneig 3D basic dun objecte petit.
- **Coneixements**: Visio, servos, triangulacio, processament dimatges.
- **Integracio**: Es pot conectar a un PC per processar les imatges.

### Deteccio dobjectes amb TensorFlow Lite Micro

- **Dificultat**: Alta
- **Cost**: ~30 EUR
- **Temps**: 12-15 h
- **Components**: ESP32-S3 (te mes memoria) + camera
- **Utilitat real**: Detectar objectes en temps real a la vora del dispositiu.
- **Coneixements**: ML embegut, TensorFlow Lite, visio per computador.
- **Integracio**: Es pot enviar via MQTT les deteccions al sistema del BernatLab.
