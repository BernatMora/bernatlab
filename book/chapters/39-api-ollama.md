# Capítol 39 — API d'Ollama: integrar la IA amb el BernatLab

> *"Ollama al Mac, el BernatLab a la Raspberry. Si parlen entre ells, tens un sistema que pot raonar sobre les dades del teu hort sense sortir de casa."*

## 39.1 L'API d'Ollama

Ollama exposa una **API HTTP local** (a `http://localhost:11434`) que permet:

- Generar respostes (`/api/generate`).
- Mantenir converses amb historial (`/api/chat`).
- Generar embeddings (`/api/embeddings`).
- Llistar models (`/api/tags`).
- Aturar/reprendre models (`/api/ps`, `/api/load`, `/api/unload`).

També és **compatible amb l'API d'OpenAI**, així que qualsevol eina que funcioni amb OpenAI funciona amb Ollama (canviant la URL base).

Això obre la porta a integrar Ollama amb tot el que ja tenim al BernatLab: FastAPI, Node-RED, scripts Python, Telegram bots, etc.

## 39.2 Configurar Ollama per accedir des de la xarxa

Per defecte, Ollama escolta a `localhost:11434`. Per permetre connexions des d'altres dispositius:

```bash
# Atura Ollama
pkill ollama

# Re-arrenca escoltant a totes les interfícies
OLLAMA_HOST=0.0.0.0:11434 ollama serve &
```

Per fer-ho persistent, edita la configuració del servei launchd (macOS):

```xml
<key>EnvironmentVariables</key>
<dict>
    <key>OLLAMA_HOST</key>
    <string>0.0.0.0:11434</string>
</dict>
```

Verifica des d'un altre dispositiu:

```bash
curl http://<mac-tailscale-ip>:11434/api/tags
```

Hauries de veure la llista de models.

## 39.3 Endpoints essencials

### Llistar models disponibles

```bash
curl http://localhost:11434/api/tags
```

Resposta:

```json
{
  "models": [
    {
      "name": "gemma3:12b",
      "size": 8149502976,
      "modified_at": "2026-07-08T10:30:00Z"
    }
  ]
}
```

### Generar una resposta (no streaming)

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "gemma3:12b",
  "prompt": "Quan plantar tomàquets?",
  "stream": false
}'
```

Resposta:

```json
{
  "model": "gemma3:12b",
  "response": "Els tomàquets es planten a la primavera...",
  "done": true,
  "context": [123, 456, 789, ...],
  "total_duration": 5234567890,
  "load_duration": 1234567890,
  "prompt_eval_count": 12,
  "eval_count": 87
}
```

### Generar amb streaming

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "gemma3:12b",
  "prompt": "Explica el compostatge",
  "stream": true
}'
```

Resposta: cada línia és un JSON amb un tros de la resposta. Acaba amb `"done": true`.

### Chat amb historial

```bash
curl http://localhost:11434/api/chat -d '{
  "model": "gemma3:12b",
  "messages": [
    {"role": "user", "content": "Hola"},
    {"role": "assistant", "content": "Hola! Com puc ajudar-te?"},
    {"role": "user", "content": "Quan plantar carbasses?"}
  ],
  "stream": false
}'
```

Això manté el context de la conversa.

### Generar embeddings

```bash
curl http://localhost:11434/api/embeddings -d '{
  "model": "nomic-embed-text",
  "prompt": "El tomàquet prefereix sòl ben drenat"
}'
```

Resposta: un vector de 768 números.

## 39.4 Compatibilitat amb OpenAI

L'endpoint `http://localhost:11434/v1/chat/completions` és compatible amb l'API d'OpenAI. Això vol dir que qualsevol eina que usi OpenAI pot usar Ollama simplement canviant la URL base:

```python
# Abans amb OpenAI:
import openai
client = openai.OpenAI(api_key="sk-...")
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hola"}]
)

# Ara amb Ollama (canvi mínim):
import openai
client = openai.OpenAI(
    api_key="ollama",  # qualsevol valor, no es valida
    base_url="http://localhost:11434/v1"
)
response = client.chat.completions.create(
    model="gemma3:12b",
    messages=[{"role": "user", "content": "Hola"}]
)
```

Això permet usar eines com:
- **LangChain** (framework per construir aplicacions amb LLMs).
- **LlamaIndex** (framework especialitzat en RAG).
- **Open WebUI** (interfície web similar a ChatGPT).
- **AnythingLLM** (una altra interfície).

## 39.5 Integració amb la Raspberry

A la Raspberry, podem fer consultes a Ollama al Mac via Tailscale. Un script Python:

```python
#!/usr/bin/env python3
"""
consulta_hort.py — Script per fer consultes a Ollama des de la Raspberry.
"""

import requests
import sys

OLLAMA_URL = "http://100.x.y.z:11434"  # Mac Tailscale IP
MODEL = "gemma3:12b"


def pregunta(text: str) -> str:
    """Envia una pregunta a Ollama i retorna la resposta."""
    r = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model": MODEL,
            "prompt": text,
            "stream": False
        },
        timeout=60
    )
    r.raise_for_status()
    return r.json()["response"]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Ús: consulta_hort.py 'la teva pregunta'")
        sys.exit(1)
    q = " ".join(sys.argv[1:])
    print(f"Pregunta: {q}\n")
    print(f"Resposta: {pregunta(q)}")
```

Ús:

```bash
python3 consulta_hort.py "Quan he de plantar carbasses a Osona?"
```

## 39.6 Integració amb Node-RED

Node-RED té nodes per cridar HTTP. Un flux per rebre alertes de sensors i consultar Ollama:

```
[MQTT subscriber: hort/sensors/#]
        │
        ▼
[Function: construir prompt amb dades del sensor]
        │
        ▼
[HTTP request: POST a Ollama]
        │
        ▼
[Function: formatar resposta]
        │
        ▼
[Telegram: enviar alerta]
```

Exemple del node function que construeix el prompt:

```javascript
// Rep un missatge MQTT amb dades del sensor
const sensorData = msg.payload;

const prompt = `Ets l'assistent de l'hort. Acabo de rebre les següents dades
d'un sensor a l'hort:

${JSON.stringify(sensorData, null, 2)}

Analitza aquestes dades i, si hi ha alguna cosa que requereixi atenció
(temperatura extrema, humitat del sòl massa baixa, bateria baixa),
dona'm una alerta curta en català. Si tot és normal, digue'm "Tot correcte".

Resposta (màxim 3 línies):`;

msg.payload = prompt;
return msg;
```

## 39.7 Integració amb el bot de Telegram

Tens un bot de Telegram al BernatLab (M2). Pots afegir una comanda `/hort` que consulta Ollama:

```python
# Dins del teu bot de Telegram (python-telegram-bot)
async def hort(update, context):
    """Respon a la comanda /hort amb una consulta a Ollama."""
    if not context.args:
        await update.message.reply_text(
            "Ús: /hort la teva pregunta sobre l'hort"
        )
        return

    pregunta = " ".join(context.args)
    await context.bot.send_chat_action(
        update.effective_chat.id, "typing"
    )

    try:
        resposta = pregunta_ollama(pregunta)
        await update.message.reply_text(resposta, parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")
```

Ara pots fer `/hort Quan plantar tomàquets?` des del mòbil.

## 39.8 Integració amb FastAPI (BernatLab API)

L'API FastAPI del M2 (Cap 20) pot tenir un nou endpoint que consulta Ollama:

```python
# A l'API del BernatLab
from fastapi import APIRouter
import httpx

router = APIRouter()

OLLAMA_URL = "http://100.x.y.z:11434"  # Mac Tailscale

@router.get("/hort/preguntar")
async def hort_preguntar(q: str):
    """Consulta l'assistent Hort Osona."""
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(
            f"{OLLAMA_URL}/api/generate",
            json={"model": "gemma3:12b", "prompt": q, "stream": False}
        )
        return r.json()
```

Ara la web pública d'Hort Osona pot tenir un quadre de preguntes que crida aquest endpoint.

## 39.9 Com gestionar la càrrega

Ollama pot gestionar una sola petició a la vegada bé, però si tens moltes peticions simultànies, cal:

1. **Posar un timeout**. Si la resposta triga més de 60 segons, cancel·la.
2. **Posar una cua**. Usa Redis o RabbitMQ per serialitzar les peticions.
3. **Limitar les peticions concurrents**. Usa un middleware al backend.
4. **Servir el model més petit per a tasques fàcils**. Tenir 2-3 models i triar el adequat.

Exemple de cua simple amb Python:

```python
import asyncio
from collections import deque

class OllamaQueue:
    def __init__(self):
        self.cua = deque()
        self.busy = False

    async def processa(self, prompt: str) -> str:
        future = asyncio.Future()
        self.cua.append((prompt, future))
        await self._buidar()
        return await future

    async def _buidar(self):
        if self.busy or not self.cua:
            return
        self.busy = True
        while self.cua:
            prompt, future = self.cua.popleft()
            try:
                resultat = await self._trucar_ollama(prompt)
                future.set_result(resultat)
            except Exception as e:
                future.set_exception(e)
        self.busy = False
```

## 39.10 Monitoratge de l'API

Per saber com va l'API, podem afegir:

1. **Logs**: totes les peticions amb temps de resposta.
2. **Mètriques**: nombre de peticions, latència, errors.
3. **Alertes**: si el model no respon, o si la latència és massa alta.

Exemple amb un middleware de FastAPI:

```python
import time
from fastapi import Request

@app.middleware("http")
async def timing(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    print(f"{request.method} {request.url.path}: {duration:.2f}s")
    return response
```

I un panell a Uptime Kuma per veure si l'API està viva:

```bash
# Afegir a Uptime Kuma
curl -X POST http://localhost:3001/api/monitors \
  -H "Content-Type: application/json" \
  -d '{"name": "Ollama API", "url": "http://mac:11434/api/tags", "interval": 60}'
```

## 39.11 Seguretat de l'API

L'API d'Ollama **no té autenticació** per defecte. Si l'exposes a la xarxa, algú podria:

- Usar el teu Mac per a inferència (consumint CPU/RAM).
- Enviar prompts maliciosos.
- Saturar el sistema.

Per protegir-la:

1. **Tallafocs al Mac**: permet només la xarxa Tailscale.
2. **Reverse proxy amb Nginx/Caddy** i autenticació bàsica.
3. **API key** personalitzada: modifica Ollama per afegir un header d'autenticació.

Una solució senzilla amb Caddy:

```caddyfile
# /etc/caddy/Caddyfile
ollama.bernat.local {
    basicauth {
        bernat $2a$14$...  # hash bcrypt
    }
    reverse_proxy localhost:11434
}
```

Ara cal usuari i contrasenya per accedir.

## 39.12 Backup i recuperació

Quan tens un sistema que depèn d'Ollama, és bona pràctica:

1. **Guardar els models** amb regularitat: les descàrregues ocupen molt, però si les perds, cal esperar hores a tornar-les a descarregar.
2. **Guardar la base vectorial** (ChromaDB): una còpia de seguretat setmanal.
3. **Guardar l'historial de converses**: si en tens.
4. **Guardar les configuracions**: Modelfiles, scripts, etc.

Un script de backup:

```bash
#!/bin/bash
# backup_ollama.sh
BACKUP_DIR="/Users/bernat/backups/ollama"
DATE=$(date +%Y%m%d)

mkdir -p "$BACKUP_DIR/$DATE"

# Models
cp -r ~/.ollama "$BACKUP_DIR/$DATE/"

# Base vectorial
cp -r ~/bernatlab/asistent/vectorstore "$BACKUP_DIR/$DATE/"

# Configuració
cp ~/Library/LaunchAgents/com.bernat.asistent.plist "$BACKUP_DIR/$DATE/"

echo "Backup fet a $BACKUP_DIR/$DATE"
```

Executar amb cron o launchd.

## 39.13 Resum

Hem après a fer accessible l'API d'Ollama des de la xarxa, a integrar-la amb la Raspberry, Node-RED, el bot de Telegram, i l'API del BernatLab. Hem vist com gestionar la càrrega, monitorar, securitzar, i fer còpies de seguretat. Al proper capítol afegirem veu: li parlarem a l'assistent en lloc d'escriure.

## 39.14 Exercicis pràctics

1. Configura Ollama per escoltar a `0.0.0.0:11434`.
2. Verifica que la Raspberry pot accedir-hi via Tailscale.
3. Crea el script `consulta_hort.py` i prova'l.
4. Afegeix un node HTTP a Node-RED que consulti Ollama.
5. Afegeix una comanda `/hort` al bot de Telegram.
6. Afegeix un endpoint `/hort/preguntar` a l'API FastAPI.
7. Configura Uptime Kuma per monitorar l'API.
8. Fes un backup programat d'Ollama i la base vectorial.

Paraules clau: **API, HTTP, REST, Ollama, localhost, 11434, Tailscale, 100.x.y.z, OpenAI compatibility, /v1, /api/generate, /api/chat, /api/embeddings, /api/tags, streaming, JSON, pydantic, FastAPI, uvicorn, async, httpx, timeout, cua, queue, rate limit, autenticació, basicauth, Caddy, Nginx, seguretat, tallafocs, firewall, monitoratge, Uptime Kuma, alerting, backup, recuperació, restore, snapshot, launchd, servei, dimoni, plist, RunAtLoad, KeepAlive, integració, Node-RED, Telegram, Python, script, CLI, command-line, asyncio, future, deque, prometheus, grafana, observabilitat, mètriques, logs, latència, throughput, peticions per segon, RPS, error rate, time series, panell, alert, contact point**.
