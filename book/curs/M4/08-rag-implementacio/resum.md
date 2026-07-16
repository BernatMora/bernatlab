# Resum - Capitol 8: RAG - implementacio completa

## La idea clau

Aquest capitol posa totes les peces juntes: **com fer un sistema RAG complet** que respongui preguntes sobre la teva base de coneixement d'Hort Osona. Es el capitol mes practic del modul.

## El pipeline

```
Pregunta de l'usuari
    ↓
1. Generar embedding de la pregunta (Ollama)
    ↓
2. Cercar els 5 fragments mes semblants (ChromaDB)
    ↓
3. Preparar el prompt amb el context trobat
    ↓
4. Enviar al LLM (Ollama)
    ↓
5. Retornar la resposta
```

Cada pas es un ingredient. Si en falles un, el plat no surt be.

## Pas a pas amb codi

### 1. Carregar els documents

```python
from pathlib import Path

def load_documents(base_path):
    """Carrega tots els .md d'una carpeta."""
    docs = []
    for md_file in Path(base_path).rglob("*.md"):
        content = md_file.read_text(encoding='utf-8')
        docs.append({
            'path': str(md_file),
            'content': content,
        })
    return docs

docs = load_documents('./hort-osona')
print(f"Carregats {len(docs)} documents")
```

### 2. Dividir en fragments (chunking)

Els documents son massa llargs per passar-los al LLM. Cal dividir-los:

```python
def chunk_text(text, chunk_size=500, overlap=50):
    """Divideix el text en fragments de chunk_size paraules."""
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

# Aplicar a tots els documents
all_chunks = []
for doc in docs:
    for chunk in chunk_text(doc['content']):
        all_chunks.append(chunk)
print(f"Total chunks: {len(all_chunks)}")
```

### 3. Generar els embeddings

```python
import requests
import json

def get_embedding(text, model="nomic-embed-text"):
    """Obté l'embedding d'un text via Ollama API."""
    response = requests.post(
        "http://localhost:11434/api/embeddings",
        json={"model": model, "prompt": text}
    )
    return response.json()['embedding']

# Generar embedding per a cada chunk
for i, chunk in enumerate(all_chunks):
    emb = get_embedding(chunk)
    # Guardar a ChromaDB (pas següent)
```

### 4. Emmagatzemar a ChromaDB

```python
import chromadb
import uuid

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="hort")

for i, chunk in enumerate(all_chunks):
    emb = get_embedding(chunk)
    collection.add(
        embeddings=[emb],
        documents=[chunk],
        ids=[str(uuid.uuid4())]
    )
```

### 5. Cercar i generar

```python
def ask_rag(question, k=5):
    """Respon una pregunta usant RAG."""
    # 1. Embedding de la pregunta
    q_emb = get_embedding(question)
    # 2. Cercar els fragments mes semblants
    results = collection.query(
        query_embeddings=[q_emb],
        n_results=k
    )
    context = '\n\n'.join(results['documents'][0])
    # 3. Preparar el prompt
    prompt = f"""Respon aquesta pregunta usant nomes el context proporcionat.
Si no trobes la resposta al context, digues-ho.

Context:
{context}

Pregunta: {question}
Resposta:"""
    # 4. Enviar al LLM
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()['response']

# Us
resposta = ask_rag("Com he de regar els tomàquets?")
print(resposta)
```

## Optimitzacions

### Chunk size

- **Massa petit** (100 paraules): massa fragments, el LLM es perd.
- **Massa gran** (2000 paraules): el LLM no hi cap tot.
- **Sweet spot**: 300-800 paraules.

### k (nombre de fragments a retornar)

- k=1: nomes el mes semblant (perdut informacio).
- k=10: masses fragments (el LLM es confon).
- k=3-5: bon equilibri.

### Re-ranking

Per a mes precisio, pots fer una **segona cerca** entre els fragments ja trobats. Pero es complex - no cal per a un homelab.

## Connexions

- **M4 cap 5-7** - Tots els conceptes previos.
- **M4 cap 9** - Privadesa: tot corre local.
- **M4 cap 10** - Aplicacio a Hort Osona (cas concret).

## Errors habituals

- **No persistir ChromaDB** - Si no passes `path=`, les dades es perden.
- **Embedding del LLM equivocat** - Usa sempre el mateix model per embeddings i cerca.
- **Prompt massa llarg** - Si el context es massa gran, el LLM triga o falla. Limita a 3-5 fragments.
- **No gestionar errors** - Si Ollama no respon, el sistema peta. Afegeix try/except.
