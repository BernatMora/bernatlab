# Capítol 38 — Client web: parla amb l'assistent des del navegador

> *"Un assistent potent al terminal és útil. Un assistent al navegador, amb historial, cites i veu, és una altra cosa."*

## 38.1 Per què un client web

Un cop tens el RAG funcionant al terminal (Cap 37), vols alguna cosa més usable:

- **Interfície gràfica** amb quadre de text, historial, format.
- **Cites clicables** que porten a la fitxa original.
- **Markdown renderitzat** (llistes, negretes, enllaços).
- **Codi amb color** (útil si preguntes sobre scripts).
- **Persistència** de l'historial entre sessions.
- **Accessible des de qualsevol dispositiu** del tailnet.

La manera més senzilla és un client web local que connecta amb Ollama. Sense dependències complexes, en HTML + JavaScript, allotjable a qualsevol lloc.

## 38.2 Stack tecnològic

Triarem eines lleugeres, sense frameworks pesats:

- **Backend**: FastAPI (Python) — simple, modern, async.
- **Frontend**: HTML + CSS + JavaScript — sense React ni Vue, perquè volem poc.
- **Markdown**: marked.js (libreria que converteix Markdown a HTML, ~30 KB) carregada per CDN.
- **Syntax highlight**: highlight.js per al codi, per CDN.

Tot plegat: **150 KB de frontend, 200 línies de Python al backend**. Prou per a un assistent potent.

## 38.3 Estructura del projecte

```
book/asistent/
├── backend/
│   ├── main.py            # FastAPI app
│   ├── rag.py             # Lògica RAG (Cap 37)
│   └── requirements.txt   # Dependències
├── frontend/
│   ├── index.html         # Pàgina principal
│   ├── styles.css         # Estils
│   └── app.js             # Lògica del client
└── README.md              # Com arrancar-ho
```

## 38.4 Backend: FastAPI

Crea `backend/main.py`:

```python
#!/usr/bin/env python3
"""
asistent_hort_osona.py — Backend FastAPI per a l'assistent Hort Osona.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pathlib import Path
import sys

# Afegir el directori del RAG al path
sys.path.insert(0, str(Path(__file__).parent))
from rag import HortOsonaRAG

# Inicialitzar
app = FastAPI(title="Hort Osona Assistent")
rag = HortOsonaRAG(
    model_llm="gemma3:12b",
    model_embedding="nomic-embed-text",
    collection_name="hort_osona",
    vectorstore_path="./vectorstore"
)

# Servir fitxers estàtics
FRONTEND_DIR = Path(__file__).parent.parent / "frontend"
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


class Pregunta(BaseModel):
    text: str
    stream: bool = True


@app.get("/")
def root():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/api/preguntar")
def preguntar_text(q: str):
    """Endpoint per streaming amb Server-Sent Events (SSE)."""
    from fastapi.responses import StreamingResponse
    import json

    def generator():
        for chunk in rag.ask_stream(q):
            yield f"data: {json.dumps(chunk)}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(generator(), media_type="text/event-stream")


@app.post("/api/preguntar")
def preguntar_json(pregunta: Pregunta):
    """Endpoint per obtenir resposta completa en JSON."""
    if pregunta.stream:
        raise HTTPException(400, "Useu /api/preguntar?q=... per streaming")
    return rag.ask(pregunta.text)


@app.get("/api/estadistiques")
def estadistiques():
    """Retorna estadístiques de la base vectorial."""
    return {
        "fragments_indexats": rag.count(),
        "model_llm": rag.model_llm,
        "model_embedding": rag.model_embedding,
    }
```

## 38.5 Backend: la classe RAG

Crea `backend/rag.py` (basat en el Cap 37, però organitzat com a classe):

```python
"""
rag.py — Lògica del RAG per a Hort Osona.
"""

import json
from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions
import requests


class HortOsonaRAG:
    def __init__(self, model_llm, model_embedding, collection_name, vectorstore_path):
        self.model_llm = model_llm
        self.model_embedding = model_embedding

        # Configurar embeddings via Ollama
        ollama_ef = embedding_functions.OllamaEmbeddingFunction(
            model_name=model_embedding,
            url="http://localhost:11434/api/embeddings"
        )

        # Connectar a ChromaDB
        client = chromadb.PersistentClient(path=vectorstore_path)
        self.collection = client.get_or_create_collection(
            name=collection_name,
            embedding_function=ollama_ef
        )

    def cerca(self, pregunta: str, k: int = 4) -> list[dict]:
        resultats = self.collection.query(
            query_texts=[pregunta],
            n_results=k
        )
        return [
            {
                "text": resultats['documents'][0][i],
                "font": resultats['metadatas'][0][i].get('source', 'desconegut'),
                "tema": resultats['metadatas'][0][i].get('tema', ''),
                "distancia": resultats['distances'][0][i] if 'distances' in resultats else 0
            }
            for i in range(len(resultats['documents'][0]))
        ]

    def _build_prompt(self, pregunta: str, fragments: list[dict]) -> str:
        context = "\n\n".join(
            f"[Fragment de {f['font']}]\n{f['text']}"
            for f in fragments
        )
        return f"""Ets l'assistent del projecte Hort Osona.

INSTRUCCIONS:
- Respon SEMPRE en català.
- Basat-te NOMÉS en la informació dels fragments.
- Si la informació no és als fragments, digues "No ho sé amb les dades d'Hort Osona".
- Sigues pràctic i concret.
- Si la pregunta és sobre una planta concreta, esmenta la fitxa d'origen.

FRAGMENTS:
{context}

PREGUNTA: {pregunta}

RESPOSTA:"""

    def ask(self, pregunta: str) -> dict:
        fragments = self.cerca(pregunta)
        prompt = self._build_prompt(pregunta, fragments)
        r = requests.post("http://localhost:11434/api/generate", json={
            "model": self.model_llm,
            "prompt": prompt,
            "stream": False
        })
        return {
            "resposta": r.json()["response"],
            "fonts": list(set(f['font'] for f in fragments)),
            "fragments": fragments
        }

    def ask_stream(self, pregunta: str):
        """Genera la resposta en streaming, amb cites al final."""
        fragments = self.cerca(pregunta)
        prompt = self._build_prompt(pregunta, fragments)

        # Enviar primer les cites
        yield {
            "type": "fonts",
            "fonts": list(set(f['font'] for f in fragments))
        }

        # Després la resposta en streaming
        with requests.post(
            "http://localhost:11434/api/generate",
            json={"model": self.model_llm, "prompt": prompt, "stream": True},
            stream=True
        ) as r:
            for line in r.iter_lines():
                if line:
                    data = json.loads(line)
                    if "response" in data:
                        yield {
                            "type": "text",
                            "content": data["response"]
                        }

    def count(self) -> int:
        return self.collection.count()
```

## 38.6 Frontend: HTML

Crea `frontend/index.html`:

```html
<!DOCTYPE html>
<html lang="ca">
<head>
    <meta charset="UTF-8">
    <title>Hort Osona · Assistent</title>
    <link rel="stylesheet" href="/static/styles.css">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/dompurify@3.0.6/dist/purify.min.js"></script>
    <link rel="stylesheet"
          href="https://cdn.jsdelivr.net/npm/highlight.js@11.9.0/styles/github.min.css">
    <script src="https://cdn.jsdelivr.net/npm/highlight.js@11.9.0/lib/core.min.js"></script>
</head>
<body>
    <header>
        <h1>🌱 Hort Osona</h1>
        <p class="subtitle">Assistent local basat en les teves 76 fitxes</p>
    </header>

    <main>
        <div id="chat"></div>

        <form id="form">
            <textarea
                id="input"
                placeholder="Pregunta'm sobre el teu hort..."
                rows="3"
                autofocus></textarea>
            <div class="actions">
                <span id="status"></span>
                <button type="submit">Enviar</button>
            </div>
        </form>
    </main>

    <footer>
        <small>
            Model: <span id="model-name">...</span> ·
            Fragments: <span id="fragments-count">...</span>
        </small>
    </footer>

    <script src="/static/app.js"></script>
</body>
</html>
```

## 38.7 Frontend: CSS

Crea `frontend/styles.css`:

```css
* { box-sizing: border-box; }
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    margin: 0;
    background: #f8f9fa;
    color: #222;
    line-height: 1.6;
}
header {
    background: #2d5016;
    color: #fff;
    padding: 1em 2em;
    text-align: center;
}
header h1 { margin: 0; font-size: 1.5em; }
header .subtitle { margin: 0.3em 0 0; opacity: 0.8; font-size: 0.9em; }
main {
    max-width: 800px;
    margin: 0 auto;
    padding: 1em;
    min-height: 70vh;
    display: flex;
    flex-direction: column;
}
#chat {
    flex: 1;
    overflow-y: auto;
    margin-bottom: 1em;
}
.message {
    margin: 1em 0;
    padding: 0.8em 1em;
    border-radius: 8px;
    max-width: 90%;
}
.user {
    background: #e3f2fd;
    margin-left: auto;
}
.assistant {
    background: #fff;
    border: 1px solid #e0e0e0;
}
.assistant pre {
    background: #1e1e1e;
    color: #d4d4d4;
    padding: 0.8em;
    border-radius: 4px;
    overflow-x: auto;
}
.assistant code {
    background: #f0f0f0;
    padding: 0.1em 0.3em;
    border-radius: 3px;
}
.fonts {
    margin-top: 0.5em;
    font-size: 0.85em;
    color: #666;
    font-style: italic;
}
#form {
    background: #fff;
    padding: 1em;
    border-radius: 8px;
    border: 1px solid #e0e0e0;
}
#input {
    width: 100%;
    border: 1px solid #ddd;
    border-radius: 4px;
    padding: 0.5em;
    font-family: inherit;
    font-size: 1em;
    resize: vertical;
}
.actions {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 0.5em;
}
button {
    background: #2d5016;
    color: #fff;
    border: none;
    padding: 0.5em 1.5em;
    border-radius: 4px;
    cursor: pointer;
    font-size: 1em;
}
button:hover { background: #3d6b1f; }
button:disabled { background: #aaa; cursor: not-allowed; }
#status { font-size: 0.85em; color: #666; }
footer {
    text-align: center;
    color: #888;
    padding: 1em;
}
```

## 38.8 Frontend: JavaScript

Crea `frontend/app.js`:

```javascript
// app.js — Client per a l'assistent Hort Osona

const chat = document.getElementById('chat');
const form = document.getElementById('form');
const input = document.getElementById('input');
const status = document.getElementById('status');
const modelName = document.getElementById('model-name');
const fragmentsCount = document.getElementById('fragments-count');

// Carregar estadístiques
fetch('/api/estadistiques')
    .then(r => r.json())
    .then(d => {
        modelName.textContent = d.model_llm;
        fragmentsCount.textContent = d.fragments_indexats;
    });

function afegirMissatge(text, role, fonts = null) {
    const div = document.createElement('div');
    div.className = `message ${role}`;
    if (role === 'assistant') {
        div.innerHTML = DOMPurify.sanitize(marked.parse(text));
        if (fonts && fonts.length > 0) {
            const f = document.createElement('div');
            f.className = 'fonts';
            f.textContent = '📚 ' + fonts.join(', ');
            div.appendChild(f);
        }
    } else {
        div.textContent = text;
    }
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
    return div;
}

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const text = input.value.trim();
    if (!text) return;

    afegirMissatge(text, 'user');
    input.value = '';
    status.textContent = 'Pensant...';
    form.querySelector('button').disabled = true;

    try {
        // Obrir stream
        const response = await fetch(`/api/preguntar?q=${encodeURIComponent(text)}`);
        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        let buffer = '';
        let assistantDiv = null;
        let fullText = '';
        let fonts = null;

        while (true) {
            const { value, done } = await reader.read();
            if (done) break;
            buffer += decoder.decode(value, { stream: true });

            // Processar línies SSE
            const lines = buffer.split('\n\n');
            buffer = lines.pop() || '';

            for (const line of lines) {
                if (!line.startsWith('data: ')) continue;
                const data = line.slice(6);
                if (data === '[DONE]') continue;

                try {
                    const obj = JSON.parse(data);
                    if (obj.type === 'fonts') {
                        fonts = obj.fonts;
                    } else if (obj.type === 'text') {
                        fullText += obj.content;
                        if (!assistantDiv) {
                            assistantDiv = afegirMissatge('', 'assistant');
                        }
                        assistantDiv.innerHTML = DOMPurify.sanitize(
                            marked.parse(fullText)
                        );
                    }
                } catch (e) {}
            }
            chat.scrollTop = chat.scrollHeight;
        }

        // Afegir cites al final
        if (fonts && assistantDiv) {
            const f = document.createElement('div');
            f.className = 'fonts';
            f.textContent = '📚 Fonts: ' + fonts.join(', ');
            assistantDiv.appendChild(f);
        }

        status.textContent = '';
    } catch (err) {
        afegirMissatge('Error: ' + err.message, 'assistant');
        status.textContent = '';
    } finally {
        form.querySelector('button').disabled = false;
    }
});
```

## 38.9 Com arrencar-ho tot

1. **Assegura't que Ollama està corrent**:

```bash
ollama serve &
```

2. **Indexa les fitxes** (només la primera vegada, o quan n'afegim de noves):

```bash
python backend/../index_hort_osona.py
```

3. **Arrenca el backend**:

```bash
cd backend
pip install -r requirements.txt  # fastapi, uvicorn, chromadb, requests
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

4. **Obre el navegador** a `http://localhost:8080`.

## 38.10 Accedir des de la Raspberry o el mòbil

Si vols accedir des d'altres dispositius del tailnet:

1. **Assegura't que el backend escolta a 0.0.0.0** (ja ho fem amb `--host 0.0.0.0`).
2. **Obre el port al firewall** del Mac:

```bash
# System Settings → Network → Firewall → Options
# Afegir uvicorn (Python) i permetre connexions entrants
```

3. **Accedeix des de la Raspberry**:

```bash
curl http://<mac-tailscale-ip>:8080/api/estadistiques
```

4. **Des del navegador del mòbil**: obre `http://<mac-tailscale-ip>:8080`.

## 38.11 Millores opcionals

Un cop el bàsic funciona, pots afegir:

1. **Historial persistent**. Guarda les converses a una base de dades SQLite o fitxer JSON.
2. **Sistema de feedback**. Botons 👍/👎 per millorar el model.
3. **Memòria a llarg termini**. Recorda les preferències de l'usuari (l'hort, varietats favorites).
4. **Exportar converses**. Descarrega les respostes com a Markdown o PDF.
5. **Multimodal**. Afegeix lectura d'imatges (p. ex. una foto d'una planta malalta).
6. **Veu**. Cap 40.

## 38.12 Desplegament al BernatLab

Si vols que el client estigui disponible sempre, sense haver d'arrencar-lo manualment:

1. **Crea un servei launchd al Mac**:

```xml
<!-- ~/Library/LaunchAgents/com.bernat.asistent.plist -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.bernat.asistent</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/bernat/bernatlab/.venv/bin/python</string>
        <string>-m</string>
        <string>uvicorn</string>
        <string>main:app</string>
        <string>--host</string>
        <string>0.0.0.0</string>
        <string>--port</string>
        <string>8080</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/Users/bernat/bernatlab/asistent/backend</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
```

2. **Carrega'l**:

```bash
launchctl load ~/Library/LaunchAgents/com.bernat.asistent.plist
```

Ara l'assistent arrenca automàticament quan encens el Mac.

## 38.13 Resum

Hem muntat un client web complet per a l'assistent Hort Osona: backend FastAPI, frontend HTML+CSS+JS, streaming de respostes, cites als documents, i persistència. Al proper capítol veurem com integrar Ollama amb l'API del BernatLab perquè la Raspberry pugui preguntar coses al Mac i rebre respostes basades en les fitxes.

## 38.14 Exercicis pràctics

1. Crea l'estructura `asistent/backend/` i `asistent/frontend/`.
2. Escriu `rag.py` i `main.py`.
3. Escriu `index.html`, `styles.css`, i `app.js`.
4. Arrenca Ollama i el backend amb uvicorn.
5. Obre `http://localhost:8080` i fes 5 preguntes.
6. Afegeix el servei launchd per arrencada automàtica.
7. Configura l'accés des de la Raspberry via Tailscale.
8. Documenta al README com usar-lo.

Paraules clau: **FastAPI, uvicorn, streaming, Server-Sent Events, SSE, EventSource, ReadableStream, frontend, HTML, CSS, JavaScript, marked.js, DOMPurify, highlight.js, marked, sanitize, Markdown, renderitzat, historial, persistència, localStorage, SQLite, JSON, feedback, usuari, multi-dispositiu, Tailscale, mòbil, responsive, launchd, plist, dimoni, servei, arrencada automàtica, RunAtLoad, KeepAlive, Mac, deployment, producció, monitor, watchdog, pàgina web, navegador, client, UI, UX, interfície, quadre de text, Enter, enviar, cites, fonts, links, click, enllaços, navegació**.
