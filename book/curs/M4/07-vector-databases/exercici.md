# Exercici practic - Capitol 7: Vector databases

> 30-45 min - RPi amb Ollama

## Objectiu

Instal·lar ChromaDB, indexar documents d'exemple, i fer les primeres cerques.

## Requisits

- Ollama ja funcionant
- Python 3.11 amb pip
- 30-45 min

## Pas 1: Instal·lar ChromaDB (5 min)

```bash
# Crear un entorn virtual per evitar conflictes
mkdir -p ~/chroma-test
cd ~/chroma-test
python3 -m venv venv
source venv/bin/activate

# Instal·lar
pip install chromadb requests
```

## Pas 2: Crear una base de dades de prova (15 min)

Crea `test_chroma.py`:

```python
import chromadb

client = chromadb.PersistentClient(path="./test_db")
collection = client.get_or_create_collection(name="test")

# Afegir alguns documents
collection.add(
    documents=[
        "El tomàquet s'ha de regar 2-3 cops per setmana",
        "L'enciam vol reg frequent, cada 1-2 dies",
        "La carbassa es cultiva a l'estiu, calor i sol",
        "El formatge es fa amb llet",
    ],
    ids=["doc1", "doc2", "doc3", "doc4"]
)

print("Documents afegits:", collection.count())
```

Executa:
```bash
python test_chroma.py
```

## Pas 3: Fer una cerca (5 min)

```python
# Continua amb aquest script
results = collection.query(
    query_texts=["com regar"],
    n_results=2
)
print("Resultats:", results)
```

Hauries de veure els 2 documents mes rellevants sobre regar.

## Pas 4: Usar embeddings d'Ollama (15 min)

Crea `ollama_chroma.py`:

```python
import chromadb
import requests

client = chromadb.PersistentClient(path="./ollama_db")
collection = client.get_or_create_collection(name="ollama-test")

def get_embedding(text):
    r = requests.post(
        "http://localhost:11434/api/embeddings",
        json={"model": "nomic-embed-text", "prompt": text}
    )
    return r.json()['embedding']

# Indexar amb embeddings d'Ollama
docs = [
    "El tomàquet vol poc reg pero profund",
    "L'enciam vol reg frequent i superficial",
    "La carbassa aguanta la sequera pero dona mes fruit amb aigua",
]

embeddings = [get_embedding(d) for d in docs]
collection.add(
    embeddings=embeddings,
    documents=docs,
    ids=["t1", "t2", "t3"]
)

# Cercar
q = "Com he de regar el meu hort?"
q_emb = get_embedding(q)
results = collection.query(query_embeddings=[q_emb], n_results=2)
print("Pregunta:", q)
print("Resultats:", results['documents'][0])
```

## Validacio

Has acabat si:
- [ ] ChromaDB instal·lat
- [ ] Primera base de dades creada
- [ ] Cerques basics funcionen
- [ ] Integracio amb Ollama funciona

## Per aprofundir

- Prova amb mes documents (100+) i mira el rendiment.
- Experimenta amb diferents mides de chunk.
- Prova altres models d'embeddings a Ollama.
