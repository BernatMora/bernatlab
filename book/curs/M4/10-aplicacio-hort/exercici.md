# Exercici practic - Capitol 10: Aplicacio a Hort Osona

> 45-60 min - RPi amb Ollama

## Objectiu

Muntar el sistema Hort Osona complet: clonar el repo, indexar els documents, i fer consultes reals sobre l'hort.

## Requisits

- RPi amb Ollama funcionant
- ChromaDB i requests instal·lats
- 1-2 GB d'espai lliure al disc
- 45-60 min

## Pas 1: Clonar Hort Osona (5 min)

```bash
cd ~
git clone https://github.com/BernatMora/hort-osona.git
cd hort-osona
ls
# Hauries de veure ~80 fitxers .md
```

Compta quants fitxers hi ha:

```bash
find . -name "*.md" | wc -l
```

Mira un parell de fitxers per entendre l'estructura:

```bash
cat tomàquet.md  # o el primer que trobis
```

## Pas 2: Crear l'script d'indexacio (15 min)

Crea `indexar_hort.py` a la carpeta `hort-osona`:

```python
import chromadb
import requests
from pathlib import Path

client = chromadb.PersistentClient(path="./hort_db")
collection = client.get_or_create_collection(name="hort-osona")

def get_embedding(text, model="nomic-embed-text"):
    r = requests.post(
        "http://localhost:11434/api/embeddings",
        json={"model": model, "prompt": text}
    )
    return r.json()['embedding']

def chunk_text(text, size=500, overlap=50):
    words = text.split()
    return [' '.join(words[i:i+size])
            for i in range(0, len(words), size - overlap)]

# Indexar tots els .md
doc_id = 0
hort_path = Path(".")
for md_file in hort_path.rglob("*.md"):
    content = md_file.read_text(encoding='utf-8')
    chunks = chunk_text(content)
    for chunk in chunks:
        if len(chunk) < 50:
            continue
        emb = get_embedding(chunk)
        collection.add(
            embeddings=[emb],
            documents=[chunk],
            metadatas=[{"source": str(md_file.relative_to(hort_path))}],
            ids=[f"{md_file.name}_{doc_id}"]
        )
        doc_id += 1
    print(f"  {md_file.name}: {len(chunks)} fragments")

print(f"\nTotal: {doc_id} fragments indexats")
```

Executa (pot trigar 10-30 min a la RPi):

```bash
cd ~/hort-osona
python indexar_hort.py
```

## Pas 3: Crear l'script de consulta (15 min)

Crea `consultar_hort.py`:

```python
import chromadb
import requests

client = chromadb.PersistentClient(path="./hort_db")
collection = client.get_collection(name="hort-osona")

def get_embedding(text, model="nomic-embed-text"):
    r = requests.post(
        "http://localhost:11434/api/embeddings",
        json={"model": model, "prompt": text}
    )
    return r.json()['embedding']

def ask_hort(question, k=5):
    # 1. Embedding de la pregunta
    q_emb = get_embedding(question)
    # 2. Cerca
    results = collection.query(
        query_embeddings=[q_emb],
        n_results=k
    )
    context = "\n\n".join(results['documents'][0])
    fonts = [m['source'] for m in results['metadatas'][0]]
    # 3. Prompt
    prompt = f"""Ets un expert en horticultura ecologica a Osona.
Respon la pregunta Nomes amb la informacio del context.
Si no saps, digues-ho.

Context:
{context}

Pregunta: {question}
Resposta (en catala):"""
    # 4. Generar
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3.2", "prompt": prompt, "stream": False}
    )
    return response.json()['response'], fonts

if __name__ == "__main__":
    while True:
        q = input("\nPregunta (o 'sortir'): ")
        if q.lower() == 'sortir':
            break
        resposta, fonts = ask_hort(q)
        print(f"\nResposta: {resposta}")
        print(f"\nFonts: {set(fonts)}")
```

## Pas 4: Fer les proves suggerides (15 min)

Executa i prova aquestes preguntes:

```bash
python consultar_hort.py
```

Prova:
- "Com es planta el tomàquet a Osona?"
- "Quines plagues pateix l'enciam al juliol?"
- "Quan s'ha de sembrar la carbassa?"
- "Quines plantes son bones companyes de la mongeta?"
- "Com es fa la rotacio de cultius?"

Observa:
- Les respostes son especifiques d'Hort Osona o son generals?
- Les fonts son els fitxers correctes?
- El catala es correcte?

## Pas 5 (opcional): Integrar amb Open WebUI (15 min)

Si tens Open WebUI instal·lat:

1. Ves a Settings > Connections.
2. Afegeix OpenAI API connection.
3. URL: `http://localhost:11434/v1`
4. Model: `llama3.2`

Ara pots xatejar amb el LLM des d'Open WebUI. Per a RAG amb contexte, cal un treball extra (extensions o custom).

## Validacio

Has acabat si:
- [ ] He clonat el repo d'Hort Osona
- [ ] L'indexacio ha acabat amb exit (X>0 fragments)
- [ ] El script de consulta respon preguntes especifiques
- [ ] Les respostes inclouen informacio dels fitxers d'Hort Osona
- [ ] He provat almenys 4 preguntes diferents

## Per aprofundir

- Afegir un sistema de cites: "Segons el document X...".
- Connectar amb Telegram per consultar des del mobil.
- Crear una interficie web propia amb Flask o Streamlit.
- Fer que el sistema aprengui de les respostes bones (feedback).
- Re-indexar periodicament quan s'afegeixen nous fitxers.
