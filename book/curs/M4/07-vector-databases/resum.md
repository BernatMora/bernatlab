# Resum - Capitol 7: Vector databases

## La idea clau

Quan fas RAG, necessites **emmagatzemar embeddings** i **cercar-hi rapid**. Això ho fan les **vector databases** (bases de dades de vectors). Son com bases de dades tradicionals, pero optimitzades per a **cerques per semblança** en lloc de cerques exactes.

## Per que serveixen

Una base de dades tradicional et fa cerques com `WHERE titol = 'poma'`. Perfecte per a text exacte. Pero si vols trobar "pomes" (plural), "Poma" (majuscules), o coses semblants, falla.

Una vector database fa una altre cosa: donat un vector (embedding), et retorna els **N vectors mes semblants**. Es a dir, et troba els conceptes relacionats, no pas els que coincideixen exactament.

Aixo es el que permet que el xat amb la teva base de coneixement trobi fragments **relevants** encara que les paraules exactes no coincideixin.

## ChromaDB - la mes facil

**ChromaDB** es la opcio que recomano per a un homelab perque:
- Es **gratis** i **open source**.
- Es **super facil** d'instal·lar (pip install chromadb).
- Guarda les dades a un **fitxer** local (no cal un servidor separat).
- Perfecta per a volums petits i mitjans (fins a uns 100.000 documents).

**Instal·lacio**:
```bash
pip install chromadb
```

**Us basic**:
```python
import chromadb

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="hort")

# Afegir documents
collection.add(
    documents=["El tomàquet s'ha de regar poc", "L'enciam vol molta aigua"],
    ids=["doc1", "doc2"]
)

# Cercar
results = collection.query(
    query_texts=["com regar el tomàquet"],
    n_results=2
)
print(results)
```

## Altres opcions

| Eina | Tipus | Pros | Contres |
|---|---|---|---|
| **ChromaDB** | Self-hosted | Fàcil, gratis, en un sol binari | No escala gaire |
| **FAISS** | Llibreria (Meta) | Molt ràpida, potent | Cal programar més |
| **LanceDB** | Self-hosted | Basada en Rust, moderna | Comunitat més petita |
| **Qdrant** | Self-hosted | Producció, escalable | Més complex de configurar |
| **Weaviate** | Self-hosted | Molt complet, GraphQL | Més complex |
| **Pinecone** | Cloud | Molt fàcil d'usar | No es local, pagament |

**La meva recomanacio**: 
- Per a un homelab: **ChromaDB** (perfecte).
- Si vols mes potència: **LanceDB** (modern, ràpid).
- Si vols produccio: **Qdrant** (escala bé).

## Embeddings a ChromaDB

Pots fer dues coses:
1. **Embedding automatic**: ChromaDB pot generar els embeddings sol (amb un model per defecte).
2. **Embedding extern**: tu els generes (amb Ollama, sentence-transformers, etc.) i els passes.

Per al cas del BernatLab amb Ollama, l'opcio 2 es la correcta. Et permet triar el model que vols i tenir control.

## Connexions amb altres capitols

- **M4 cap 5-6** - Que es RAG i com funcionen els embeddings.
- **M4 cap 8** - Implementacio completa amb Ollama + ChromaDB.
- **M3 cap 6** - InfluxDB es diferent (per a series temporals, no text).

## Errors habituals

- **No instal·lar el client HTTP** - ChromaDB pot correr com a servidor o com a llibreria. Per a scripts, usa la llibreria.
- **No persistir les dades** - Si no passes `path=`, les dades es perden al tancar.
- **Massa documents petits** - Si tens 1000 fragments de 50 paraules, ChromaDB no rendeix. Millor pocs fragments grans.
