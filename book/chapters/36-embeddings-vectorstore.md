# Capítol 36 — Embeddings i bases vectorials: com la IA troba el que busques

> *"Si cerques per paraules exactes, trobaràs documents amb aquestes paraules. Si cerques per significat, trobaràs documents que parlen del que vols saber, encara que no usin les mateixes paraules."*

## 36.1 El problema: la cerca per paraules clau no és prou

Imagina que tens les 76 fitxes d'hort i un dia vols saber **"què fer quan els tomàquets tenen taques grogues a les fulles"**. Si cerques a mà:

- "tomaques taca groga fulla" — pot ser que trobis poques coses perquè el text pot dir "fulles groguenques", "clorosi", "deficiència de nitrogen", etc.
- Necessitaries llegir cada fitxa, una per una.

El que voldries és: "troba'm els paràgrafs que parlen d'això, encara que no usin les mateixes paraules". Això és el que fan els **embeddings** i les **bases vectorials**.

## 36.2 Què és un embedding

Un **embedding** (en català, **representació vectorial** o **incrustació**) és una manera de convertir text en una llista de números (un vector) que captura el **significat** del text.

Per exemple:

- "El gos borda" → [0.12, -0.34, 0.78, ..., 0.45] (384 o 1024 o 4096 números)
- "El ca lladra" → [0.11, -0.33, 0.79, ..., 0.46] (molt similar!)
- "Avui plou" → [0.87, 0.23, -0.45, ..., -0.12] (molt diferent)

Això és màgia matemàtica: frases amb significat similar tenen vectors propers. Frases amb significat diferent tenen vectors allunyats.

Aquesta propietat es mesura amb la **similaritat del cosinus** (cosine similarity, mètrica que mesura l'angle entre dos vectors: 1.0 = idèntic, 0.0 = orthogonal, -1.0 = oposat). Dos textos que parlen del mateix tindran una similaritat alta (>0.8). Dos textos no relacionats tindran una similaritat baixa (<0.3).

## 36.3 Com es crea un embedding

Hi ha models entrenats específicament per a aquesta tasca. Els més coneguts:

- **OpenAI text-embedding-3-small/large** (al núvol, pagament).
- **BGE** (BAAI, gratuït, molt bo).
- **E5** (Microsoft, gratuït, multilingüe).
- **mE5** (multilingüe, inclou català).
- **Nomic Embed** (obert, bona qualitat).
- **Ollama** (sí, Ollama també pot generar embeddings!).

A Ollama:

```bash
# Descarrega un model d'embeddings
ollama pull nomic-embed-text

# Genera l'embedding d'un text
curl http://localhost:11434/api/embeddings -d '{
  "model": "nomic-embed-text",
  "prompt": "El gos borda fort"
}'
```

Això retorna un vector de 768 números. Cadascun captura algun aspecte del significat.

## 36.4 Què és una base vectorial

Una **base vectorial** (vector store, vector database) és un sistema que:

1. **Emmagatzema** milions de vectors associats a fragments de text.
2. **Cerca ràpidament** els vectors més similars a una consulta.

Les bases vectorials més conegudes:

- **ChromaDB** — la més fàcil d'usar, ideal per començar.
- **FAISS** (Facebook) — molt ràpida, per a molts vectors.
- **LanceDB** — moderna, eficient, bona per a hobby.
- **Qdrant** — servidor complet, escalable.
- **Milvus** — solucions professionals, molt ràpid.
- **Pinecone** — al núvol, pagament.

Per al BernatLab, recomano **ChromaDB** o **LanceDB** per simplicitat. Si volem alguna cosa més professional, **Qdrant**.

## 36.5 ChromaDB: el primer pas

ChromaDB és la base vectorial més fàcil d'utilitzar. S'instal·la amb pip i funciona localment.

### Instal·lació

```bash
pip install chromadb
```

### Ús bàsic en Python

```python
import chromadb

# Inicialitzar (per defecte emmagatzema a ~/.chromadb)
client = chromadb.PersistentClient(path="./vectorstore")

# Crear o obtenir una col·lecció
collection = client.get_or_create_collection(name="hort_osona")

# Afegir documents
collection.add(
    documents=[
        "El tomàquet de Penedès prefereix sòls ben drenats i assolellats.",
        "Les carbasses necessiten molt espai, almenys 2 m² per planta.",
        "El mildiu és un fong que apareix amb humitat alta."
    ],
    metadatas=[
        {"source": "fitxa-tomaque.md", "tema": "tomàquet"},
        {"source": "fitxa-carbassa.md", "tema": "carbassa"},
        {"source": "guia-plagues.md", "tema": "malalties"}
    ],
    ids=["doc1", "doc2", "doc3"]
)

# Cercar per similitud
results = collection.query(
    query_texts=["Quan he de plantar carbasses?"],
    n_results=2
)

# Mostrar els resultats
for doc, meta in zip(results['documents'][0], results['metadatas'][0]):
    print(f"  {meta['source']}: {doc}")
```

La cerca retorna els 2 documents més similars a la pregunta, ordenats per rellevància.

## 36.6 Com funciona la cerca per similitud

Quan fas una consulta:

1. **Converteix la consulta en un vector** usant el mateix model d'embeddings.
2. **Calcula la distància** entre el vector de la consulta i tots els vectors emmagatzemats.
3. **Retorna els k més propers** (k=2 a l'exemple anterior).

Això és extremadament ràpid: per a 10.000 vectors, la cerca triga menys d'un segon.

## 36.7 Com fragmentar els documents

Un embedding té una mida màxima (normalment 512-2048 tokens, és a dir, unitats de text que el model processa, aproximadament 1 token = 0.75 paraules en català). Si tens un document de 5.000 tokens, no pots fer-ne un sol embedding. Cal **fragmentar** (chunking) en parts més petites.

Estratègies comunes de fragmentació:

1. **Per mida fixa**. Trossos de 500 tokens amb solapament de 50. Senzill i efectiu.

2. **Per paràgrafs o seccions**. Cada secció del document és un chunk. Mantén la coherència.

3. **Semàntica**. Parteix on hi ha canvis de tema. Més sofisticat.

4. **Per estructures Markdown**. Capçaleres, llistes, blocs de codi. Molt adequat per a llibres tècnics.

Per al BernatLab, recomano **per mida fixa (500 tokens) amb solapament (50 tokens)**. Senzill i funciona bé.

## 36.8 Ús pràctic: indexar les 76 fitxes d'hort

Un script per indexar totes les fitxes:

```python
#!/usr/bin/env python3
"""
index_hort_osona.py
Indexa tots els fitxers Markdown de Hort Osona a ChromaDB.
"""

import os
from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions

# Configuració
HORT_DIR = Path("/home/bernat/bernatlab/projects/hort-osona")
VECTORSTORE_DIR = "./vectorstore"
COLLECTION_NAME = "hort_osona"

# Model d'embeddings — cal que estigui a Ollama
ollama_ef = embedding_functions.OllamaEmbeddingFunction(
    model_name="nomic-embed-text",
    url="http://localhost:11434/api/embeddings"
)

# Inicialitzar ChromaDB
client = chromadb.PersistentClient(path=VECTORSTORE_DIR)
collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    embedding_function=ollama_ef
)

# Funció per fragmentar un document
def fragmentar(text, mida=500, solapament=50):
    """Fragmenta text en trossos amb solapament."""
    paraules = text.split()
    fragments = []
    i = 0
    while i < len(paraules):
        fragment = " ".join(paraules[i:i+mida])
        fragments.append(fragment)
        i += mida - solapament
    return fragments

# Indexar tots els .md
idx = 0
for md_file in HORT_DIR.rglob("*.md"):
    if md_file.name.startswith("."):
        continue
    text = md_file.read_text(encoding="utf-8")
    fragments = fragmentar(text)
    for n, frag in enumerate(fragments):
        collection.add(
            documents=[frag],
            metadatas=[{
                "source": str(md_file.relative_to(HORT_DIR)),
                "fragment": n,
                "tema": md_file.stem
            }],
            ids=[f"{md_file.stem}-{n}"]
        )
        idx += 1
    print(f"  Indexat: {md_file.name} ({len(fragments)} fragments)")

print(f"\nTotal: {idx} fragments indexats a ChromaDB")
```

Executa'l una vegada, i ja tens les 76 fitxes (i totes les guies) en una base vectorial.

## 36.9 Com escollir el model d'embeddings

No tots els models d'embeddings són igual de bons. Al 2026, els millors per a text multilingüe (inclòs català) són:

| Model | Mida | Qualitat | Català | Velocitat |
|---|---|---|---|---|
| **nomic-embed-text** | 274 MB | Excel·lent | Bona | Molt ràpid |
| **mxbai-embed-large** | 670 MB | Excel·lent | Bona | Ràpid |
| **bge-m3** | 2.3 GB | Excel·lent | Molt bona | Mitjà |
| **multilingual-e5-large** | 2.2 GB | Excel·lent | Molt bona | Mitjà |
| **snowflake-arctic-embed** | 1.2 GB | Molt bona | Bona | Ràpid |

Recomanació per al BernatLab: `nomic-embed-text` per defecte. Si vols més qualitat, `bge-m3` o `multilingual-e5-large`.

## 36.10 Com avaluar la qualitat de la cerca

Per validar que la cerca funciona bé:

1. **Crea un test set**: 10-20 preguntes amb les respostes esperades (quins documents haurien d'aparèixer).
2. **Executa cada pregunta** i mira els resultats.
3. **Calcula mètriques**:
   - **Recall@K** (quants documents rellevants apareixen entre els K primers resultats).
   - **MRR** (Mean Reciprocal Rank, rang mitjà del primer document rellevant).
4. **Ajusta**: si els resultats són dolents, canvia de model d'embeddings, ajusta la mida dels fragments, o afegeix metadades.

Per a Hort Osona, les primeres 10 preguntes bones serien:

1. "Quan plantar tomàquets a Osona?"
2. "Com combatre el pugó?"
3. "Quines associacions de cultius funcionen?"
4. "Com fer compost casolà?"
5. "Quan collir les carbasses?"
6. "Quin reg necessita l'enciam?"
7. "Com sembrar pèsols?"
8. "Quines plagues ataquen la patata?"
9. "Com protegir les plantes de la gelada?"
10. "Quan fer la poda dels fruiters?"

Si el sistema retorna les fitxes correctes per a totes 10, tens una bona base.

## 36.11 Com actualitzar la base vectorial

Quan afegeixis nous documents a Hort Osona (una nova fitxa, una guia actualitzada), cal re-indexar. Opcions:

1. **Re-indexar tot sencer**. Lent però segur.
2. **Indexar només els nous**. Ràpid, però cal gestionar els fragments antics.
3. **Sistema d'actualització automàtic**. Un script que mira els canvis amb `git pull` i re-indexa el que cal.

Recomanació per al BernatLab: un script setmanal via cron que comprova si hi ha canvis i re-indexa només el que cal.

## 36.12 Emmagatzematge i persistència

La base vectorial s'ha de desar a algun lloc:

- **Local al Mac**: `~/.chromadb` o `./vectorstore`. Fàcil però cal còpia de seguretat.
- **A la Raspberry**: si vols compartir amb altres dispositius.
- **A GitHub**: NO! Els fitxers de la base vectorial ocupen molt i canvien sovint.

Recomanació: **local al Mac, amb còpia a la Raspberry via Tailscale si vols accedir-hi des d'allà**. No versionis la base vectorial a Git.

## 36.13 Com moure la base vectorial a la Raspberry

Si vols accedir a la base vectorial des de la Raspberry, pots:

1. **Muntar la carpeta** via NFS o SMB (compartir carpetes per xarxa).
2. **Usar SSHFS** (muntar carpetes remotes com si fossin locals).
3. **Exportar/importar** periòdicament (un script que fa `cp`).

L'opció més neta per a un homelab és SSHFS:

```bash
# A la Raspberry
sshfs bernat@<mac-tailscale-ip>:/Users/bernat/vectorstore /home/bernat/vectorstore
```

Ara `/home/bernat/vectorstore` és la mateixa carpeta que al Mac.

## 36.14 Resum

Hem après què són els embeddings, com representen el significat del text com a vectors numèrics, com funcionen les bases vectorials, i com indexar els documents d'Hort Osona amb ChromaDB. Al proper capítol muntarem el sistema RAG complet: quan l'usuari fa una pregunta, buscarem els fragments més rellevants i els donarem al model de llengua perquè generi una resposta basada en ells.

## 36.15 Exercicis pràctics

1. Instal·la ChromaDB al teu Mac: `pip install chromadb`.
2. Descarrega `nomic-embed-text` a Ollama.
3. Executa l'script d'exemple amb 3-5 documents i comprova que la cerca funciona.
4. Adapta l'script `index_hort_osona.py` al teu cas.
5. Crea 10 preguntes de test i avalua la qualitat de la cerca.
6. Compara `nomic-embed-text` amb `bge-m3` (si tens temps).
7. Documenta al README la mida de la base vectorial, el model d'embeddings, i les mètriques obtingudes.

Paraules clau: **embedding, vector, representació vectorial, incrustació, similaritat, cosinus, cosine similarity, distància euclidiana, dot product, base vectorial, vector store, vector database, ChromaDB, FAISS, LanceDB, Qdrant, Milvus, Pinecone, fragmentació, chunking, solapament, overlap, n_results, recall, MRR, mètriques, test set, ground truth, embeddings multilingüe, nomic, bge, e5, mxbai, arctic, multilingual, semàntica, cerca semàntica, cerca per paraules clau, search, full-text search, FTS, BM25, híbrida, reranking, cross-encoder, bi-encoder, contrastive learning, sentence-transformers, Hugging Face, Ollama embedding, API embedding, persistència, SSHFS, NFS, còpia de seguretat, vectorstore, col·lecció, document, fragment, metadata, filtratge, filter, where, where_document, similarity threshold, top-k**.
