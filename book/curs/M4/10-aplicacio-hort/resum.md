# Resum - Capitol 10: Aplicacio a Hort Osona

## La idea clau

Aquest ultim capitol del modul aplica **tot el que hem vist** al cas real del projecte **Hort Osona**: un sistema de consulta a la base de coneixement de l'hort amb IA local, 100% privat.

## El sistema complet

Ara que tens Ollama, embeddings, ChromaDB, i el pipeline RAG, **pots muntar el teu propi assistent horticola** que:
- Coneix les 76 fitxes de cultiu d'Hort Osona.
- Coneix el calendari de sembra, plagues, associacions.
- Respon preguntes en catala.
- Es queda al teu servidor - res surt de casa.

## L'arquitectura

```
┌─────────────────────────────────────┐
│  RPi (hortosona)                    │
├─────────────────────────────────────┤
│                                     │
│  ┌─────────────┐   ┌────────────┐  │
│  │  Open WebUI │ ←→ │   Ollama   │  │
│  │  (frontend) │   │  (LLM)     │  │
│  └──────┬──────┘   └────────────┘  │
│         │                           │
│         ↓                           │
│  ┌─────────────┐                   │
│  │  ChromaDB   │ ← (vector store) │
│  │  (hort-osona)│                  │
│  └─────────────┘                   │
│         ↑                           │
│         │                           │
│  ┌─────────────┐                   │
│  │   Script    │ (indexa documents)│
│  │  d'indexació│                   │
│  └─────────────┘                   │
│                                     │
└─────────────────────────────────────┘
```

## Pas 1: Preparar la base de coneixement

Tots els fitxers d'Hort Osona son a `https://github.com/BernatMora/hort-osona/`. Cal clonar-lo:

```bash
cd /home/bernat
git clone https://github.com/BernatMora/hort-osona.git
```

Ara tens 80+ documents en catala sobre horticultura.

## Pas 2: Indexar els documents

Crea un script `indexar_hort.py`:

```python
import chromadb
import requests
from pathlib import Path

# Conectar a ChromaDB
client = chromadb.PersistentClient(path="./hort_db")
collection = client.get_or_create_collection(name="hort-osona")

def get_embedding(text):
    r = requests.post(
        "http://localhost:11434/api/embeddings",
        json={"model": "nomic-embed-text", "prompt": text}
    )
    return r.json()['embedding']

def chunk_text(text, size=500, overlap=50):
    words = text.split()
    return [' '.join(words[i:i+size])
            for i in range(0, len(words), size - overlap)]

# Carregar tots els .md
hort_path = Path("/home/bernat/hort-osona")
docs_carregats = 0
for md_file in hort_path.rglob("*.md"):
    content = md_file.read_text(encoding='utf-8')
    chunks = chunk_text(content)
    for chunk in chunks:
        if len(chunk) < 50:  # Saltar fragments massa petits
            continue
        emb = get_embedding(chunk)
        collection.add(
            embeddings=[emb],
            documents=[chunk],
            metadatas=[{"source": str(md_file.relative_to(hort_path))}],
            ids=[f"{md_file.name}_{docs_carregats}"]
        )
        docs_carregats += 1
    print(f"  {md_file.name}: {len(chunks)} fragments")

print(f"\nTotal: {docs_carregats} fragments indexats")
```

## Pas 3: Crear l'API de consulta

Crea `consultar_hort.py`:

```python
import chromadb
import requests

client = chromadb.PersistentClient(path="./hort_db")
collection = client.get_collection(name="hort-osona")

def get_embedding(text):
    r = requests.post(
        "http://localhost:11434/api/embeddings",
        json={"model": "nomic-embed-text", "prompt": text}
    )
    return r.json()['embedding']

def ask_hort(question, k=5):
    """Respon una pregunta sobre l'hort."""
    # 1. Buscar fragments rellevants
    q_emb = get_embedding(question)
    results = collection.query(
        query_embeddings=[q_emb],
        n_results=k
    )
    context = '\n\n'.join(results['documents'][0])
    sources = [m['source'] for m in results['metadatas'][0]]
    # 2. Preparar prompt
    prompt = f"""Ets un expert en horticultura ecològica a Osona.
Respon la pregunta NOMÉS amb la informació del context.
Si no saps, digues-ho.

Context:
{context}

Pregunta: {question}
Resposta (en català):"""
    # 3. Generar resposta
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3.2", "prompt": prompt, "stream": False}
    )
    return {
        "answer": response.json()['response'],
        "sources": sources
    }
```

## Pas 4: Integrar amb Open WebUI (opcional)

Si tens Open WebUI instal·lat, pots connectar-hi el RAG.

A Open WebUI:
1. Ves a **Settings** > **Connections**.
2. Afegeix una nova **OpenAI API connection**.
3. URL: `http://localhost:11434/v1`
4. Model: `llama3.2`

Ara pots xatejar amb el LLM directament des d'Open WebUI. Per al RAG, cal una extensio (potser mes complex).

## Proves que pots fer

Un cop tot funcioni, prova:
- "Com es planta el tomàquet a Osona?"
- "Quines plagues pateix l'enciam al juliol?"
- "Quan s'ha de sembrar la carbassa?"
- "Quines plantes son bones companyes de la mongeta?"

Si tot va be, el sistema et respondra amb informacio **especifica** d'Hort Osona, no pas informacio generica.

## Limitacions

- **Qualitat dels embeddings** depen del model. `nomic-embed-text` es bo pero no perfecte.
- **Qualitat del LLM** depen del model. `llama3.2` es bo, pero `mistral` o `gemma` poden ser millors per a catala.
- **Velocitat** depen del hardware. La RPi es lenta per a models grans.
- **Cobertura** depen dels documents indexats. Si un tema no es a Hort Osona, no es pot respondre.

## Connexions

- **M4 caps 1-9** - Tots els conceptes.
- **M4 cap 8** - Implementacio RAG.
- **M3 cap 10** - Visualitzacio amb Grafana.
- **M5 del llibre** - Seguretat de l'API.

## El futur

Aixo es nomes el principi. Al BernatLab pots:
- Afegir mes documents automaticament.
- Crear una **interficie web** personalitzada.
- Connectar amb **Telegram** per consultar des del mobil.
- Fer que el sistema **aprengui** de les respostes bones (feedback).
