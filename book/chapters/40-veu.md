# Capítol 40 — Veu: parlar a l'assistent en lloc d'escriure

> *"Quan tens les mans plenes de terra i el cap ple de preguntes, l'últim que vols és teclejar. Li parles, et contesta. Màgia."*

## 40.1 Per què veu a Hort Osona

A l'hort, les mans estan ocupades (pala, planter, regadora). El mòbil pot estar brut. Però la veu sempre és disponible. Per això, la integració de veu és especialment valuosa per a consultes ràpides mentre treballes.

Casos d'ús reals:

- Estàs trasplantant tomàquets i vols saber la distància exacta. Li preguntes, et contesta.
- Vius una plaga sobtada i vols consell immediat. Li parles, reps la resposta.
- Estàs collint i vols saber si ja estan al punt. Li ensenyes la foto (multimodal), et diu.

## 40.2 Stack tecnològic

Per a la veu, usarem:

- **Whisper** (OpenAI) per a **STT** (Speech-to-Text, transcripció de veu a text). Versió local, multilingüe, excel·lent en català.
- **Piper** o **XTTS** per a **TTS** (Text-to-Speech, síntesi de veu). Sintetitza veu a partir de text. Opcions locals, en diversos idiomes.
- **FastAPI** com a backend (reutilitzem el del Cap 38).
- **Web Audio API** al frontend per gravar àudio del micròfon.

Tot local, sense enviar res al núvol.

## 40.3 Instal·lar Whisper

Whisper és la millor opció per a transcripció. Versió local amb Python:

```bash
# Opció 1: faster-whisper (recomanada, més ràpida)
pip install faster-whisper

# Opció 2: openai-whisper (oficial)
pip install openai-whisper
```

`faster-whisper` és ~4x més ràpida i consumeix menys memòria. Recomanada.

Descarrega un model:

```python
from faster_whisper import WhisperModel

# Models disponibles: tiny, base, small, medium, large-v3
# - tiny: 39M paràmetres, ~75 MB, molt ràpid, baixa qualitat
# - base: 74M, ~140 MB, ràpid, qualitat acceptable
# - small: 244M, ~460 MB, equilibrat
# - medium: 769M, ~1.5 GB, bona qualitat
# - large-v3: 1.5 GB, ~3 GB, millor qualitat, multilingüe

model = WhisperModel("large-v3", device="cpu", compute_type="int8")
```

## 40.4 Ús bàsic de Whisper

```python
from faster_whisper import WhisperModel

model = WhisperModel("large-v3", device="cpu", compute_type="int8")

# Transcriure un fitxer d'àudio
segments, info = model.transcribe("audio.wav", language="ca")

print(f"Idioma detectat: {info.language} (probabilitat: {info.language_probability:.2f})")
print(f"Durada: {info.duration:.1f}s")
print()

for segment in segments:
    print(f"[{segment.start:.1f}s - {segment.end:.1f}s] {segment.text}")
```

Whisper detecta automàticament l'idioma, però pots forçar-lo amb `language="ca"`.

## 40.5 Capturar àudio del navegador

Al frontend, podem capturar àudio del micròfon amb la **Web Audio API** + **MediaRecorder**:

```javascript
async function gravarAudio() {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const recorder = new MediaRecorder(stream);
    const chunks = [];

    recorder.ondataavailable = e => chunks.push(e.data);
    recorder.onstop = async () => {
        const blob = new Blob(chunks, { type: 'audio/webm' });
        const formData = new FormData();
        formData.append('audio', blob, 'gravar.webm');

        const response = await fetch('/api/transcriure', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        console.log('Transcripció:', data.text);
    };

    recorder.start();
    // Aturar després de 5 segons (o quan l'usuari cliqui un botó)
    setTimeout(() => recorder.stop(), 5000);
}
```

El botó pot ser:

```html
<button id="record">🎤 Parleu (5s)</button>
```

## 40.6 Endpoint FastAPI per transcriure

Al backend, afegim:

```python
from fastapi import UploadFile, File
from faster_whisper import WhisperModel
import tempfile
import os

# Inicialitzar el model un sol cop
whisper_model = WhisperModel("large-v3", device="cpu", compute_type="int8")

@app.post("/api/transcriure")
async def transcriure(audio: UploadFile = File(...)):
    """Rep un àudio i retorna la transcripció."""
    # Guardar l'àudio temporalment
    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as f:
        content = await audio.read()
        f.write(content)
        tmp_path = f.name

    try:
        # Transcriure
        segments, info = whisper_model.transcribe(tmp_path, language="ca")
        text = " ".join(s.text for s in segments)
        return {
            "text": text,
            "idioma": info.language,
            "probabilitat": info.language_probability
        }
    finally:
        os.unlink(tmp_path)
```

Ara el frontend pot enviar l'àudio gravat i rebre la transcripció.

## 40.7 Integració amb el RAG

Combinem transcripció + RAG:

```python
@app.post("/api/veu-preguntar")
async def veu_preguntar(audio: UploadFile = File(...)):
    """Rep àudio, transcriu, fa consulta RAG, retorna resposta en text."""
    # 1. Transcriure
    text = await _transcriure(audio)

    # 2. Fer la consulta al RAG
    resposta = rag.ask(text['text'])

    return {
        "pregunta_transcrita": text['text'],
        "resposta": resposta['resposta'],
        "fonts": resposta['fonts']
    }
```

I podem afegir síntesi de veu a la resposta:

```python
@app.post("/api/veu-preguntar-audio")
async def veu_preguntar_audio(audio: UploadFile = File(...)):
    """Mateix que veu-preguntar, però retorna la resposta en àudio."""
    text = await _transcriure(audio)
    resposta = rag.ask(text['text'])

    # Sintetitzar la resposta a veu
    audio_path = await _sintetitzar(resposta['resposta'])

    return FileResponse(
        audio_path,
        media_type="audio/mpeg",
        headers={
            "X-Pregunta": text['text'],
            "X-Fonts": ",".join(resposta['fonts'])
        }
    )
```

## 40.8 Síntesi de veu amb Piper

**Piper** és un sistema de síntesi de veu local, lleuger i amb bona qualitat. Suporta català.

### Instal·lació

```bash
pip install piper-tts
```

Descarrega un model de veu en català:

```bash
# Descarregar model de veu (exemple)
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/ca/ca_ES/voice.json
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/ca/ca_ES/voice.onnx
```

### Ús

```python
from piper import PiperVoice
import wave

voice = PiperVoice.load("ca_ES/voice.onnx", "ca_ES/voice.json")
text = "Hola, soc l'assistent Hort Osona. Com puc ajudar-te?"

with wave.open("resposta.wav", "wb") as f:
    voice.synthesize(text, f)
```

## 40.9 Síntesi alternativa: XTTS

**XTTS** (Coqui) permet clonar veus amb només 6 segons d'àudio. Recomanat si vols que l'assistent parli amb la teva veu o la d'un familiar.

```bash
pip install TTS
```

```python
from TTS.api import TTS

tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)
tts.tts_to_file(
    text="Hola, benvingut al teu hort",
    file_path="resposta.wav",
    speaker_wav="la_meva_veu.wav",  # 6 segons de la teva veu
    language="ca"
)
```

## 40.10 Alternativa simple: Web Speech API

Si no vols instal·lar res al backend, pots fer servir la **Web Speech API** del navegador:

```javascript
// Reconèixer veu (STT)
const recognition = new webkitSpeechRecognition();
recognition.lang = 'ca-ES';
recognition.continuous = false;

recognition.onresult = (event) => {
    const text = event.results[0][0].transcript;
    console.log('Transcripció:', text);
};

recognition.start();

// Sintetitzar veu (TTS)
const utterance = new SpeechSynthesisUtterance("Hola món");
utterance.lang = 'ca-ES';
utterance.rate = 1.0;
speechSynthesis.speak(utterance);
```

Avantatges: zero instal·lació, funciona al navegador.
Inconvenients: depèn del navegador, no sempre català de qualitat, no és privat (Google processa).

Recomanació: usa Web Speech API per començar, i migra a Whisper + Piper quan vulguis més qualitat o privadesa total.

## 40.11 Optimitzar el reconeixement de veu

Whisper és bo, però podem millorar-lo:

1. **Forçar idioma**: `language="ca"` evita que provi altres idiomes.
2. **Detectar silenci**: parar la gravació quan hi ha 2 segons de silenci.
3. **Filtrar soroll**: aplicar un filtre de reducció de soroll abans de transcriure.
4. **Usar el model adequat**: `small` o `medium` per a velocitat, `large-v3` per a qualitat.
5. **Ajustar la mida del vocabulari**: passa una llista de termes esperats (noms de plantes) per millorar el reconeixement.

Exemple de llista de termes:

```python
from faster_whisper import WhisperModel

model = WhisperModel("large-v3", device="cpu", compute_type="int8")

segments, info = model.transcribe(
    "audio.webm",
    language="ca",
    initial_prompt="carbassa, tomaquet, enciam, mongeta, ceba, all, porro, "
                   "bleda, espinac, rave, meló, pebrot, col, escarola, "
                   "alfàbrega, menta, romaní, farigola, orenga, sajolida, "
                   "api, carabassa, patata, pastanaga, compota, purins, "
                   "adob, compost, fem, humus, reg, ascla, aixada, trasplantar"
)
```

Això ajuda Whisper a reconèixer correctament els termes específics d'horticultura.

## 40.12 Com crear una interfície completa de veu

Combinem-ho tot en una interfície usable:

```html
<div id="voice-control">
    <button id="record-btn" class="big-btn">🎤</button>
    <div id="status-veu">Prem per parlar</div>
    <div id="transcripcio"></div>
    <div id="resposta"></div>
</div>
```

```javascript
const recordBtn = document.getElementById('record-btn');
const statusVeu = document.getElementById('status-veu');
let gravant = false;
let mediaRecorder = null;
let chunks = [];

recordBtn.addEventListener('click', async () => {
    if (!gravant) {
        // Començar a gravar
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        chunks = [];
        mediaRecorder.ondataavailable = e => chunks.push(e.data);
        mediaRecorder.onstop = enviarAudio;
        mediaRecorder.start();
        gravant = true;
        recordBtn.textContent = '⏹';
        statusVeu.textContent = 'Escoltant...';
    } else {
        // Aturar
        mediaRecorder.stop();
        gravant = false;
        recordBtn.textContent = '🎤';
        statusVeu.textContent = 'Processant...';
    }
});

async function enviarAudio() {
    const blob = new Blob(chunks, { type: 'audio/webm' });
    const formData = new FormData();
    formData.append('audio', blob, 'gravar.webm');

    try {
        const response = await fetch('/api/veu-preguntar', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        document.getElementById('transcripcio').textContent =
            'Tú: ' + data.pregunta_transcrita;
        document.getElementById('resposta').textContent =
            'Assistent: ' + data.resposta;
        statusVeu.textContent = 'Fet';
    } catch (e) {
        statusVeu.textContent = 'Error: ' + e.message;
    }
}
```

## 40.13 Privadesa de la veu

La veu és una dada **especialment sensible**: conté biometria, emocions, salut. Per això:

1. **No enviar al núvol**. Whisper local + Piper local.
2. **Xifrar l'àudio** si l'emmagatzemes.
3. **Esborrar després d'ús**. No cal guardar totes les gravacions.
4. **Permetre l'opt-out**. L'usuari ha de poder desactivar la veu.

Això és important no només per privadesa, sinó per **complir normatives** (GDPR, LOPDGDD a Espanya).

## 40.14 Veu offline al mòbil

Si vols que el client web funcioni **offline** al mòbil (a l'hort sense cobertura):

1. **PWA** (Progressive Web App, aplicació web que es comporta com a app nativa): converteix el client en una "app" que es pot instal·lar.
2. **Service Worker** (script que permet que la web funcioni offline): permet cachejar recursos.
3. **Whisper al mòbil**: hi ha versions (Whisper.cpp, Whisper Android).

La PWA és la solució més pràctica. Pots instal·lar el client web al mòbil amb "Add to Home Screen" i funciona com una app.

## 40.15 Resum

Hem après a afegir veu a l'assistent Hort Osona: transcripció amb Whisper, síntesi amb Piper o Web Speech API, integració amb el RAG, i una interfície usable. Hem vist com optimitzar el reconeixement, gestionar la privadesa, i preparar el client per a ús offline. Al proper capítol veurem les bones pràctiques de privadesa i seguretat per a sistemes d'IA local.

## 40.16 Exercicis pràctics

1. Instal·la faster-whisper al Mac.
2. Descarrega el model `large-v3` (o `small` si tens poca RAM).
3. Grava un àudio de prova amb el mòbil i transcriu-lo.
4. Afegeix l'endpoint `/api/transcriure` al backend del Cap 38.
5. Crea una interfície amb botó de micròfon.
6. Afegeix síntesi de veu amb Piper o Web Speech API.
7. Combina transcripció + RAG + síntesi en un sol endpoint.
8. Fes proves amb termes específics d'horticultura.

Paraules clau: **veu, STT, TTS, speech-to-text, text-to-speech, Whisper, faster-whisper, Piper, XTTS, Coqui, àudio, gravació, micròfon, MediaRecorder, Web Audio API, Web Speech API, SpeechRecognition, SpeechSynthesis, frontend, mic permission, getUserMedia, FormData, multipart, blob, webm, mp3, wav, format, codificació, privacy, GDPR, LOPDGDD, biometria, opt-out, offline, PWA, Service Worker, install, Add to Home Screen, manifest, model de veu, clonar veu, veu sintètica, idioma, català, ca-ES, optimització, transcripció, vocabulari, initial_prompt, hotwords, language detection, vad, voice activity detection, silenci, gravació, 5 segons, parlar, escoltar, streaming audio, WebSocket, àudio, format, opus, codec, compressió, qualitat, sample rate, 16kHz, 44.1kHz, micròfon, noise reduction, filtre, pre-processament, post-processament, diacritics, accent, dialecte, pronunciació**.
