# Capítol 37 — RAG pas a pas: carregar les 76 fitxes d'hort a Ollama

> *"El RAG és la diferència entre una eina que respon coses generals i una eina que respon coses sobre el teu hort."*

## 37.1 Què és RAG (revisited)

Al Cap 36 vàrem veure els embeddings i les bases vectorials. Ara les connectem amb un model de llengua per crear un **RAG** (Retrieval-Augmented Generation, generació augmentada per recuperació): quan l'usuari fa una pregunta, primer busquem els fragments més rellevants als documents, i després donem aquests fragments al model com a context perquè generi una resposta.

Això és molt potent perquè:

- El model **no necessita saber** les respostes de memòria.
- Les respostes estan **basades en els teus documents**, no en dades generals.
- Pots **actualitzar els documents** sense re-entrenar el model.
- Les respostes poden **citar** els documents d'origen.

## 37.2 L'arquitectura d'un sistema RAG

```
[Usuari fa pregunta]
        │
        ▼
[Convertir pregunta en embedding]
        │
        ▼
[Cercar fragments similars a ChromaDB] ────► [Retorna top-k fragments]
        │                                              │
        │                                              ▼
        └─────────────────────► [Construir prompt amb:
                                  - System prompt
                                  - Pregunta original
                                  - Fragments recuperats
                                  - Instruccions de format]
                                                │
                                                ▼
                            [Enviar prompt al model d'Ollama]
                                                │
                                                ▼
                                    [Model genera resposta]
                                                │
                                                ▼
                                        [Retornar a l'usuari]
```

## 37.3 El primer RAG: versió mínima

Aquí tens un RAG complet en 30 línies de Python:

```python
#!/usr/bin/env python3
"""
rag_simple.py — Primer RAG per a Hort Osona.
Necessita: ollama (servidor corrent), chromadb, requests.
"""

import requests
import chromadb
from chromadb.utils import embedding_functions

# Configuració
MODEL_LLM = "gemma3:12b"
MODEL_EMBEDDING = "nomic-embed-text"
COLLECTION_NAME = "hort_osona"
N_FRAGMENTS = 4  # quants fragments recuperar

# Connexió a ChromaDB
ollama_ef = embedding_functions.OllamaEmbeddingFunction(
    model_name=MODEL_EMBEDDING,
    url="http://localhost:11434/api/embeddings"
)
client = chromadb.PersistentClient(path="./vectorstore")
collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    embedding_function=ollama_ef
)


def cerca(consulta: str, k: int = N_FRAGMENTS) -> list[str]:
    """Retorna els k fragments més rellevants per a la consulta."""
    resultats = collection.query(query_texts=[consulta], n_results=k)
    return resultats['documents'][0]


def genera_resposta(pregunta: str) -> str:
    """Genera una resposta basada en els fragments recuperats."""
    fragments = cerca(pregunta)
    context = "\n\n".join(
        f"[Fragment {i+1}]: {frag}" for i, frag in enumerate(fragments)
    )
    prompt = f"""Ets l'assistent Hort Osona. Respon en català, basant-te
només en la informació dels fragments següents. Si la informació no
és als fragments, digues "No tinc prou informació a les fitxes d'Hort
Osona per respondre aquesta pregunta."

FRAGMENTS D'HORT OSONA:
{context}

PREGUNTA: {pregunta}

RESPOSTA:"""

    # Crida a l'API d'Ollama
    r = requests.post("http://localhost:11434/api/generate", json={
        "model": MODEL_LLM,
        "prompt": prompt,
        "stream": False
    })
    return r.json()["response"]


if __name__ == "__main__":
    import sys
    pregunta = " ".join(sys.argv[1:]) or "Quan he de plantar carbasses?"
    print(f"\nPregunta: {pregunta}\n")
    print("Resposta:")
    print(genera_resposta(pregunta))
```

Prova'l:

```bash
python rag_simple.py "Com combatre el pugó?"
python rag_simple.py "Quan plantar tomàquets?"
```

## 37.4 Millorant el prompt

El prompt de l'apartat anterior és molt bàsic. Un millor prompt:

```python
PROMPT_TEMPLATE = """Ets l'assistent del projecte Hort Osona, un hort
ecològic a la comarca d'Osona (Catalunya). Tens accés a 76 fitxes de
cultius i 30+ guies d'horticultura.

INSTRUCCIONS:
1. Respon SEMPRE en català.
2. Basat-te NOMÉS en la informació dels fragments. Si no hi ha prou
   informació, digues "No ho sé amb les dades que tinc".
3. Sigues pràctic i directe. Evita frases com "En general..." o "És
   important...". Dona consells concrets.
4. Si la pregunta és sobre una planta concreta, esmenta la fitxa
   d'origen.
5. Si la pregunta és general, dona una resposta sintètica (5-10
   línies).
6. Si hi ha diverses opcions, enumera-les amb números.

FRAGMENTS D'HORT OSONA:
{context}

PREGUNTA: {pregunta}

RESPOSTA:"""
```

Aquest prompt força respostes útils i honestes.

## 37.5 Afegir cites als documents

Una millora important: retornar **quina fitxa ha donat la informació**. Això permet a l'usuari verificar i aprendre'n més.

```python
def cerca_amb_metadades(consulta: str, k: int = 4) -> list[dict]:
    resultats = collection.query(
        query_texts=[consulta],
        n_results=k
    )
    fragments = []
    for i in range(len(resultats['documents'][0])):
        fragments.append({
            "text": resultats['documents'][0][i],
            "font": resultats['metadatas'][0][i]['source'],
            "tema": resultats['metadatas'][0][i].get('tema', 'desconegut'),
            "distancia": resultats['distances'][0][i] if 'distances' in resultats else None
        })
    return fragments

def genera_resposta_amb_cites(pregunta: str) -> dict:
    fragments = cerca_amb_metadades(pregunta)
    context = "\n\n".join(
        f"[{f['tema']} | {f['font']}]: {f['text']}" for f in fragments
    )
    prompt = PROMPT_TEMPLATE.format(context=context, pregunta=pregunta)
    r = requests.post("http://localhost:11434/api/generate", json={
        "model": MODEL_LLM,
        "prompt": prompt,
        "stream": False
    })
    return {
        "resposta": r.json()["response"],
        "fonts": list(set(f['font'] for f in fragments)),
        "fragments": fragments
    }
```

Ara la resposta inclou quines fitxes ha usat.

## 37.6 Com gestionar fragments massa llargs

Quan recuperes 4-5 fragments, el context pot ser massa llarg per a un model petit. Solucions:

1. **Limitar la mida dels fragments** a l'hora d'indexar (ja ho fem al Cap 36).
2. **Resumir els fragments** amb el model abans de generar la resposta.
3. **Comprimir el context** tècniques com LongLLMLingua, Selective Context, LLMLingua.

Per al BernatLab, la solució 1 ja és bona. Si volem anar més enllà, la 2:

```python
def resum_fragments(fragments: list[str], pregunta: str) -> str:
    """Resum cada fragment en una frase, mantenint el relevant per a la pregunta."""
    resums = []
    for frag in fragments:
        prompt = f"Resum en una frase el següent text, mantenint la informació rellevant per a: '{pregunta}'.\n\nText: {frag}\n\nResum:"
        r = requests.post("http://localhost:11434/api/generate", json={
            "model": MODEL_LLM,
            "prompt": prompt,
            "stream": False
        })
        resums.append(r.json()["response"].strip())
    return "\n".join(f"- {r}" for r in resums)
```

Això fa una passada extra pel model, però redueix molt la mida del context final.

## 37.7 Com afegir metadades útils

Per a Hort Osona, les metadades importants són:

- **Temporada**: primavera, estiu, tardor, hivern.
- **Secció de l'hort**: tomateres, carabasseres, fruiters, compost, etc.
- **Tipus**: fitxa, guia, pla mensual, recepta.
- **Data**: quan s'ha escrit/actualitzat.

Si volem cerques més intel·ligents ("quines coses he de fer aquest mes?"), podem filtrar per temporada:

```python
def cerca_filtrada(consulta: str, temporada: str = None, k: int = 4) -> list:
    where = {"temporada": temporada} if temporada else None
    resultats = collection.query(
        query_texts=[consulta],
        n_results=k,
        where=where
    )
    return resultats['documents'][0]
```

Això permet respostes contextualitzades ("a l'estiu fes X, a l'hivern fes Y").

## 37.8 Com gestionar actualitzacions

Quan escrius una nova fitxa o actualitzes una de vella, cal:

1. **Re-indexar el document sencer** (esborrar els fragments antics i afegir els nous).
2. **Indexar només els canvis** (més eficient, però cal gestionar versions).

Un script de re-indexació per canvi:

```python
def reindexar_document(path: Path):
    """Re-indexa un sol document."""
    # Esborrar fragments antics
    tema = path.stem
    try:
        collection.delete(where={"tema": tema})
    except:
        pass

    # Llegir i fragmentar
    text = path.read_text(encoding="utf-8")
    fragments = fragmentar(text)

    # Afegir nous fragments
    for n, frag in enumerate(fragments):
        collection.add(
            documents=[frag],
            metadatas=[{
                "source": str(path.name),
                "fragment": n,
                "tema": tema
            }],
            ids=[f"{tema}-{n}"]
        )
```

I un script setmanal que comprova quins fitxers han canviat:

```python
import os
import time
from pathlib import Path

HORT_DIR = Path("/home/bernat/bernatlab/projects/hort-osona")
INDEX_FILE = Path(".indexed_files.txt")

# Carregar l'estat anterior
indexats = {}
if INDEX_FILE.exists():
    for line in INDEX_FILE.read_text().splitlines():
        if "," in line:
            f, mtime = line.split(",")
            indexats[f] = float(mtime)

# Comprovar canvis
nous_canvis = []
for md in HORT_DIR.rglob("*.md"):
    rel = str(md.relative_to(HORT_DIR))
    mtime = md.stat().st_mtime
    if rel not in indexats or mtime > indexats[rel]:
        nous_canvis.append(md)
        indexats[rel] = mtime

# Re-indexar
for md in nous_canvis:
    print(f"Re-indexant: {md.name}")
    reindexar_document(md)

# Guardar estat
INDEX_FILE.write_text("\n".join(f"{f},{m}" for f, m in indexats.items()))
```

## 37.9 Com avaluar la qualitat del RAG

Per saber si el teu RAG funciona bé, crea un **test set**:

```python
tests = [
    {
        "pregunta": "Quan plantar carbasses?",
        "resposta_esperada": "A la primavera, després de les últimes gelades",
        "fonts_esperades": ["fitxa-carbassa.md", "calendari-sembra.md"]
    },
    {
        "pregunta": "Com combatre el pugó?",
        "resposta_esperada": "Sabó potàssic, infusions d'all, afavorir marietes",
        "fonts_esperades": ["guia-plagues.md", "gestio-plagues.md"]
    },
    # ...
]

for t in tests:
    r = genera_resposta_amb_cites(t["pregunta"])
    correcte = t["fonts_esperades"][0] in r["fonts"]
    print(f"{'✓' if correcte else '✗'} {t['pregunta']}")
```

Si el RAG falla, ajusta:

- El model d'embeddings (prova'n un altre).
- La mida dels fragments.
- El nombre de fragments recuperats.
- El prompt del sistema.
- La qualitat dels documents d'origen.

## 37.10 Com passar a streaming

Per a respostes llargues, voldrem **streaming** (rebre la resposta a mesura que es genera, en comptes d'esperar tota la resposta):

```python
import json

def genera_stream(pregunta: str):
    fragments = cerca_amb_metadades(pregunta)
    context = "\n\n".join(f"[{f['font']}]: {f['text']}" for f in fragments)
    prompt = PROMPT_TEMPLATE.format(context=context, pregunta=pregunta)

    with requests.post(
        "http://localhost:11434/api/generate",
        json={"model": MODEL_LLM, "prompt": prompt, "stream": True},
        stream=True
    ) as r:
        for line in r.iter_lines():
            if line:
                data = json.loads(line)
                if "response" in data:
                    yield data["response"]
```

Ús:

```python
for chunk in genera_stream("Quan plantar carbasses?"):
    print(chunk, end="", flush=True)
print()
```

Això és el que farem servir al client web (Cap 38).

## 37.11 Errors habituals

**Error 1: el model no segueix les instruccions del prompt**.

Solució: fes servir un model més gran o reescriu el prompt més clar.

**Error 2: la cerca retorna fragments irrellevants**.

Solució: canvia el model d'embeddings, millora els documents, redueix k.

**Error 3: les respostes són molt llargues**.

Solució: afegeix "Respon en 3-5 línies" al prompt.

**Error 4: les respostes inventen informació**.

Solució: reforça el prompt amb "Si no saps, digues 'no ho sé'". Afegeix cites per verificar.

**Error 5: la base vectorial creix molt**.

Solució: fragmenta més fi (300-400 tokens) o redueix el nombre de documents.

## 37.12 Resum

Hem après a construir un RAG complet amb Ollama i ChromaDB: com recuperar fragments, com construir el prompt, com generar respostes amb cites, com gestionar actualitzacions, i com avaluar la qualitat. Al proper capítol construirem un client web senzill perquè puguis parlar amb l'assistent des del navegador.

## 37.13 Exercicis pràctics

1. Descarrega el codi de `rag_simple.py` i prova'l amb 5 preguntes.
2. Avalua la qualitat de les respostes.
3. Afegeix cites als documents.
4. Implementa streaming.
5. Crea un test set amb 10 preguntes i avalua el rendiment.
6. Ajusta el prompt per millorar les respostes.
7. Documenta al README la configuració del RAG, el model usat, i les mètriques.

Paraules clau: **RAG, retrieval-augmented generation, generació augmentada, fragments, top-k, context, prompt, system prompt, streaming, cites, fonts, metadades, ChromaDB, Ollama, embedding, on-premises, self-hosted, private AI, hort Osona, fitxes, guies, re-indexació, actualització, test set, avaluació, mètriques, recall, precision, MRR, reranking, re-ranking, rerank, cross-encoder, bi-encoder, hybrid search, BM25, filtratge, where, chunking, fragmentació, size, overlap, sliding window, semantic chunking, structured chunking, LongLLMLingua, LLMLingua, context compression, summarization, query expansion, HyDE, hypothetical document embeddings, multi-query, fusion, RAG-Fusion, agentic RAG, ReAct, self-RAG, corrective RAG, CRAG, advanced RAG, modular RAG, GraphRAG, knowledge graph**.
