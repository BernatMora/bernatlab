# Idees - IA local

> Projectes amb inteligencia artificial local: veu, visio, assistants, integracio amb Ollama.

## Idees

### Assistent de veu local amb wake word

- **Dificultat**: Alta
- **Cost**: ~50 EUR
- **Temps**: 12-15 h
- **Components**: ESP32-S3 + microfon I2S + altaveu + caixa
- **Utilitat real**: Dispositiu que escolta una paraula clau i respon a ordres.
- **Coneixements**: Veu, I2S, processament de senyal, wake word, integracio amb Ollama.
- **Integracio**: Es pot conectar a la RPi que te Ollama instal·lat.

### Classificador de sons ambient

- **Dificultat**: Alta
- **Cost**: ~40 EUR
- **Temps**: 10-12 h
- **Components**: ESP32-S3 + microfon I2S + TensorFlow Lite Micro
- **Utilitat real**: Detectar tipus de sons (vidre trencat, alarma, plorant, ...).
- **Coneixements**: ML embegut, processament de senyal, TensorFlow Lite.
- **Integracio**: Es pot enviar via MQTT les alertes al sistema.

### Detecccio de plagues amb visio

- **Dificultat**: Alta
- **Cost**: ~40 EUR
- **Temps**: 10-15 h
- **Components**: ESP32-CAM + TensorFlow Lite Micro + caixa
- **Utilitat real**: Detectar plagues o malalties a les plantes amb visio.
- **Coneixements**: ML embegut, visio per computador, agricultura.
- **Integracio**: Es pot integrar al sistema de lhort.

### Assistent local per consultes de cultiu

- **Dificultat**: Mitjana
- **Cost**: ~30 EUR
- **Temps**: 6-8 h
- **Components**: ESP32 + pantalla OLED + polsadors + RPi amb Ollama
- **Utilitat real**: Dispositiu a lhort que envia consultes a Ollama sobre plagues o cultiu.
- **Coneixements**: Wi-Fi, HTTP, integracio amb Ollama, RAG.
- **Integracio**: Integracio completa amb el sistema del BernatLab.

### Control per veu de llums i endolls

- **Dificultat**: Mitjana-alta
- **Cost**: ~50 EUR
- **Temps**: 8-10 h
- **Components**: ESP32-S3 + microfon I2S + moduls rele
- **Utilitat real**: Controlar les llums de casa amb la veu.
- **Coneixements**: Veu, MQTT, Home Assistant, integracio.
- **Integracio**: Integracio completa amb Home Assistant.

### Sistema de reconeixement facial basic

- **Dificultat**: Alta
- **Cost**: ~40 EUR
- **Temps**: 12-15 h
- **Components**: ESP32-S3 + camera + TensorFlow Lite Micro
- **Utilitat real**: Dispositiu que reconeix les persones autoritzades.
- **Coneixements**: ML embegut, visio per computador, seguretat.
- **Integracio**: Es pot integrar a un sistema dalarma.
