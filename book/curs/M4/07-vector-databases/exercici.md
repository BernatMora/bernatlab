# Exercici practic - Capitol 7: Vector databases

> 40-55 min · Real amb ChromaDB

## Objectiu
Instal·lar ChromaDB, indexar una col·leccio de documents, fer cerques per semblança, i entendre les limitacions. Acabaras sabent quan ChromaDB es suficient i quan cal una solucio mes potent.

## Requisits

- Python 3.10+
- Ollama amb model d'embeddings
- 40-55 minuts
- 500 MB de disc lliure

## Pas 1: Instal·la ChromaDB (3 min)

```bash
mkdir -p ~/bernatlab-exercicis/M4/07-vector-db
cd ~/bernatlab-exercicis/M4/07-vector-db

python3 -m venv venv
source venv/bin/activate

pip install chromadb ollama
```

Verifica:

```bash
python -c "import chromadb; print(chromadb.__version__)"
```

## Pas 2: Indexa una col·leccio de documents (10 min)

Crea `indexar.py`:

```python
import chromadb
import ollama

# Client persistent (guarda a disc)
client = chromadb.PersistentClient(path="./chroma_db")

# Crea o recupera la col·leccio
collection = client.get_or_create_collection(
    name="hort_osona",
    metadata={"hnsw:space": "cosine"}  # Usem cosinus
)

# Documents sobre l'hort
documents = [
    "Els tomàquets necessiten sol directe (6-8 hores diaries) i reg regular.",
    "Els enciams prefereixen temperatures fresques (15-20 graus) i reg diari.",
    "El sensor DS18B20 mesura la temperatura del sol amb precissio.",
    "La humitat optima del sol per a tomàquets es entre 60-80%.",
    "El reg automatic s'activa quan la humitat baixa del 30%.",
    "Les plantes aromatiques (basilica, orenga) son bones associacions amb tomàquets.",
    "Els pugons son plagues comunes que es combaten amb sabo potassic.",
    "L'adob verd (userda, trevol) millora l'estructura del sol.",
    "La sembra de primavera es fa despres de les ultimes glaçades (març-abril).",
    "La collita de tomàquets va de juliol a octubre.",
]

# Metadades associades
metadades = [
    {"categoria": "tomàquet", "epoca": "estiu"},
    {"categoria": "enciam", "epoca": "primavera"},
    {"categoria": "sensor", "epoca": "tot l'any"},
    {"categoria": "tomàquet", "epoca": "estiu"},
    {"categoria": "reg", "epoca": "tot l'any"},
    {"categoria": "associacio", "epoca": "estiu"},
    {"categoria": "plaga", "epoca": "estiu"},
    {"categoria": "adob", "epoca": "tardor"},
    {"categoria": "sembra", "epoca": "primavera"},
    {"categoria": "collita", "epoca": "tardor"},
]

# IDs unics
ids = [f"doc{i+1}" for i in range(len(documents))]

# Afegir a la col·leccio
collection.add(
    documents=documents,
    metadatas=metadades,
    ids=ids
)

print(f"Indexats {collection.count()} documents")
```

## Pas 3: Cerca per semblança (10 min)

Crea `cercar.py`:

```python
import chromadb

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection("hort_osona")

# Cerca simple
pregunta = "Com regar les plantes?"
resultats = collection.query(
    query_texts=[pregunta],
    n_results=3
)

print(f"Pregunta: {pregunta}\n")
print("Top 3 resultats:\n")
for i in range(len(resultats['documents'][0])):
    doc = resultats['documents'][0][i]
    dist = resultats['distances'][0][i]
    meta = resultats['metadatas'][0][i]
    print(f"{i+1}. (dist: {dist:.3f}, cat: {meta['categoria']})")
    print(f"   {doc}\n")
```

## Pas 4: Cerca amb filtres de metadades (10 min)

Crea `cercar_filtres.py`:

```python
import chromadb

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection("hort_osona")

# Cerca nomes documents de la categoria "tomàquet"
resultats = collection.query(
    query_texts=["consells per cultivar"],
    n_results=3,
    where={"categoria": "tomàquet"}  # Filtre
)

print("Resultats filtrats per categoria=Tomàquet:\n")
for i in range(len(resultats['documents'][0])):
    doc = resultats['documents'][0][i]
    meta = resultats['metadatas'][0][i]
    print(f"- ({meta['categoria']}) {doc}")

# Cerca amb multiples condicions
print("\nResultats amb categoria=Tomàquet o categoria=Enciam:\n")
resultats = collection.query(
    query_texts=[""],
    n_results=10,
    where={"$or": [
        {"categoria": "tomàquet"},
        {"categoria": "enciam"}
    ]}
)
for doc in resultats['documents'][0]:
    print(f"- {doc}")
```

## Pas 5: Actualitzar i eliminar documents (5 min)

Crea `modificar.py`:

```python
import chromadb

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection("hort_osona")

# Actualitzar un document existent
collection.update(
    ids=["doc1"],
    documents=["Els tomàquets necessiten sol directe i reg moderat, sense entollar."],
    metadatas=[{"categoria": "tomàquet", "epoca": "estiu", "actualitzat": "si"}]
)

# Afegir un document nou
collection.add(
    documents=["Les carxoques es planten a la tardor i es cullen a la primavera."],
    metadatas=[{"categoria": "carxofa", "epoca": "tardor"}],
    ids=["doc11"]
)

# Eliminar un document
collection.delete(ids=["doc11"])

print(f"Total actual: {collection.count()} documents")
```

## Pas 6: Benchmark amb mes volum (10 min)

Crea `benchmark.py`:

```python
import chromadb
import time
import random

client = chromadb.PersistentClient(path="./chroma_benchmark")
collection = client.get_or_create_collection("test_benchmark")

# Generem 10.000 documents aleatoris
print("Indexant 10.000 documents...")
docs = [f"Document numero {i}: text sobre tema {random.randint(1, 100)}" for i in range(10000)]
ids = [f"id{i}" for i in range(10000)]

inici = time.time()
collection.add(documents=docs, ids=ids)
print(f"Indexacio: {time.time() - inici:.2f}s")

# Benchmark de cerques
print("\nBenchmark de 100 cerques:")
latencies = []
for i in range(100):
    query = f"Cerca el document numero {random.randint(1, 10000)}"
    inici = time.time()
    resultats = collection.query(query_texts=[query], n_results=5)
    latencies.append(time.time() - inici)

print(f"Latencia mitjana: {sum(latencies)/len(latencies)*1000:.1f}ms")
print(f"Latencia max: {max(latencies)*1000:.1f}ms")
print(f"Latencia min: {min(latencies)*1000:.1f}ms")
```

## Pas 7: Comparacio amb cerca naive (10 min)

Crea `comparar.py`:

```python
import chromadb
import requests
import numpy as np
import time

# ChromaDB
client = chromadb.PersistentClient(path="./chroma_benchmark")
collection = client.get_collection("test_benchmark")

# Naive: calcular manualment
def embedding(text):
    r = requests.post('http://localhost:11434/api/embeddings',
                     json={'model': 'nomic-embed-text', 'prompt': text})
    return np.array(r.json()['embedding'])

def cos_sim(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Obtenim tots els embeddings (car pero just per comparar)
print("Carregant tots els embeddings...")
resultats = collection.get(include=['embeddings'])
embs = np.array(resultats['embeddings'])
print(f"Tinc {len(embs)} embeddings de {embs.shape[1]} dimensions")

# Cerca naive
query = "Document sobre el tema 42"
emb_q = embedding(query)

inici = time.time()
sims = [cos_sim(emb_q, e) for e in embs]
top_naive = np.argsort(sims)[-5:][::-1]
t_naive = time.time() - inici

# Cerca ChromaDB
inici = time.time()
resultats = collection.query(query_texts=[query], n_results=5)
t_chroma = time.time() - inici

print(f"\nCerca naive: {t_naive*1000:.1f}ms")
print(f"cerca ChromaDB: {t_chroma*1000:.1f}ms")
print(f"Speedup: {t_naive/t_chroma:.1f}x")
```

## Validacio

Has acabat si:

- [ ] Has instal·lat ChromaDB i Ollama.
- [ ] Has indexat una col·leccio de 10 documents.
- [ ] Has fet cerques per semblança.
- [ ] Has usat filtres per metadades.
- [ ] Has actualitzat i eliminat documents.
- [ ] Has fet un benchmark amb 10.000 documents.
- [ ] Has comparat ChromaDB amb cerca naive.

## Per aprofundir

- Investiga els index HNSW vs IVF vs Flat: avantatges i inconvenients.
- Prova de guardar la DB a una ruta diferent (volum Docker, particio SSD).
- Compara la velocitat de ChromaDB amb FAISS i LanceDB.
- Investiga com fer backups de la base de dades ChromaDB.

## Ves un pas mes enlla

**Repte avançat**: Construeix un sistema que:
1. Indexa tots els fitxers `.md` d'una carpeta recursivament.
2. Cada fitxer te metadades (path, data de modificacio, mida).
3. Permet cerques per text + filtres per data o path.
4. Es pot actualitzar nomes afegint/modificant els fitxers nous (no re-indexar tot).

Aixo es la base d'un sistema RAG real per a una base de coneixement.
