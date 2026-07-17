# Exercici practic - Capitol 8: RAG - implementacio completa

> 50-65 min · Real al teu servidor

## Objectiu
Construir un sistema RAG complet, de cap a cap, que respongui preguntes sobre la base de coneixement de l'Hort Osona. Es l'exercici mes important del modul.

## Requisits

- Python 3.10+
- Ollama amb `nomic-embed-text` i `llama3.2:3b`
- ChromaDB instal·lat
- 50-65 minuts

## Pas 1: Prepara el projecte (5 min)

```bash
mkdir -p ~/bernatlab-exercicis/M4/08-rag-complet
cd ~/bernatlab-exercicis/M4/08-rag-complet

python3 -m venv venv
source venv/bin/activate

pip install chromadb ollama
```

## Pas 2: Crea una base de coneixement (10 min)

Crea la carpeta de documents:

```bash
mkdir -p documents
cat > documents/01-tomatecs.md << 'EOF'
# Tomàquets a l'Hort Osona

## Sembrament
Els tomàquets es sembren en semiller a l'interior al febrer-març. Es trasplanten a l'exterior a partir de mitjans d'abril, quan ja no hi ha risc de glaçades.

## Reg
Necessiten reg regular pero sense entollar. Es recomana reg per degoteig. La frequencia depen del temps, pero en general 2-3 cops per setmana a l'estiu.

## Varietats
Per a Osona (900m d'altitud), les varietats que millor funcionen son:
- Montserrat: tradicional, bona per a amanir.
- Poma: dolça, ideal per a nens.
- Cor de Bou: gran, per a farcir.
EOF

cat > documents/02-enciams.md << 'EOF'
# Enciams a l'Hort Osona

## Sembrament
Es poden sembrar tot l'any menys a l'estiu (juliol-agost). Les varietats d'estiu (tipus iceberg) son mes resistents a la calor.

## Reg
Reg diari pero sense entollar. Els enciams son sensibles a la sequera pero tambe al'exces d'aigua.

## Recol·leccio
30-60 dies despres del sembrament. Es poden tallar les fulles externes deixant el cor per rebrotar.
EOF

cat > documents/03-sensors.md << 'EOF'
# Sensors de l'Hort Osona

## DS18B20
Mesura la temperatura del sol a 5cm de profunditat. Protocol 1-Wire. Precisio: 0.5 graus. Connexio GPIO 4.

## DHT22
Mesura humitat i temperatura ambient. Protocol digital. Precisio: 2-5% humitat, 0.5 graus temperatura. Connexio GPIO 17.

## Capacitive Soil Moisture
Mesura la humitat del terra. Sortida analogica. Calibrar entre 0-100%. Connexio GPIO amb ADC (MCP3008).
EOF
```

## Pas 3: Script d'indexacio (15 min)

Crea `indexar.py`:

```python
import chromadb
import ollama
from pathlib import Path

def carregar_documents(base_path):
    """Carrega tots els .md d'una carpeta."""
    docs = []
    for md_file in Path(base_path).rglob("*.md"):
        content = md_file.read_text(encoding='utf-8')
        docs.append({
            'path': str(md_file),
            'content': content,
            'filename': md_file.name,
        })
    return docs

def chunk_text(text, chunk_size=500, overlap=50):
    """Parteix el text en chunks amb overlap."""
    # Primer separem per paragrafs
    paragrafs = text.split('\n\n')
    chunks = []
    chunk_actual = ""
    
    for paragraf in paragrafs:
        if len(chunk_actual) + len(paragraf) <= chunk_size:
            chunk_actual += "\n\n" + paragraf if chunk_actual else paragraf
        else:
            if chunk_actual:
                chunks.append(chunk_actual.strip())
            chunk_actual = paragraf
    
    if chunk_actual:
        chunks.append(chunk_actual.strip())
    
    return chunks

def obtenir_embedding(text):
    """Calcula embedding amb Ollama."""
    r = ollama.embeddings(model='nomic-embed-text', prompt=text)
    return r['embedding']

# Carregar documents
print("Carregant documents...")
docs = carregar_documents('./documents')
print(f"Trobats {len(docs)} documents")

# Chunking
print("Fent chunking...")
tots_chunks = []
tots_ids = []
tots_metadades = []
for doc in docs:
    chunks = chunk_text(doc['content'])
    for i, chunk in enumerate(chunks):
        chunk_id = f"{doc['filename']}_{i}"
        tots_chunks.append(chunk)
        tots_ids.append(chunk_id)
        tots_metadades.append({
            'path': doc['path'],
            'filename': doc['filename'],
            'chunk_index': i,
        })

print(f"Total chunks: {len(tots_chunks)}")

# Inicialitzar ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(
    name="hort_osona",
    metadata={"hnsw:space": "cosine"}
)

# Netejar si ja existia
try:
    collection.delete(where={})
except:
    pass

# Calcular embeddings i afegir
print("Calculant embeddings i indexant...")
for i, (chunk, chunk_id, metadata) in enumerate(zip(tots_chunks, tots_ids, tots_metadades)):
    embedding = obtenir_embedding(chunk)
    collection.add(
        documents=[chunk],
        embeddings=[embedding],
        ids=[chunk_id],
        metadatas=[metadata]
    )
    if (i+1) % 10 == 0:
        print(f"  Indexats {i+1}/{len(tots_chunks)} chunks")

print(f"\nFet! {collection.count()} chunks indexats")
```

## Pas 4: Script de consulta (10 min)

Crea `consultar.py`:

```python
import chromadb
import ollama

def obtenir_embedding(text):
    r = ollama.embeddings(model='nomic-embed-text', prompt=text)
    return r['embedding']

def cercar_chunks(pregunta, n=3):
    """Cerca els N chunks mes rellevants."""
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_collection("hort_osona")
    
    embedding = obtenir_embedding(pregunta)
    resultats = collection.query(
        query_embeddings=[embedding],
        n_results=n
    )
    return resultats

def generar_resposta(pregunta, chunks):
    """Genera resposta amb el LLM."""
    context = "\n\n---\n\n".join(chunks)
    
    prompt = f"""Ets un assistent expert en horticultura a Osona (Catalunya).
Respon la pregunta basant-te nomes en el contexte proporcionat.
Si no tens prou informacio, digues-ho honestament.
Respon en catala, amb concisio (max 200 paraules).

CONTEXTE:
{context}

PREGUNTA: {pregunta}

RESPOSTA:"""
    
    r = ollama.chat(
        model='llama3.2:3b',
        messages=[
            {'role': 'system', 'content': 'Ets un expert en horticultura. Respon sempre en catala.'},
            {'role': 'user', 'content': prompt}
        ]
    )
    return r['message']['content']

def preguntar(pregunta):
    """Funcio principal: pregunta -> resposta."""
    print(f"\nPregunta: {pregunta}")
    print("-" * 60)
    
    # 1. Cercar chunks
    resultats = cercar_chunks(pregunta, n=3)
    chunks = resultats['documents'][0]
    print(f"Trobats {len(chunks)} chunks rellevants")
    
    # 2. Mostrar contexte
    print("\nContext recuperat:")
    for i, chunk in enumerate(chunks):
        print(f"  [{i+1}] {chunk[:100]}...")
    
    # 3. Generar resposta
    print("\nGenerant resposta...")
    resposta = generar_resposta(pregunta, chunks)
    print(f"\nResposta:\n{resposta}")
    return resposta

if __name__ == '__main__':
    # Exemples de preguntes
    preguntes = [
        "Quan he de plantar tomàquets?",
        "Com es el reg dels enciams?",
        "Quin sensor mesura la humitat del terra?",
        "Quina varietat de tomàquet es dolça?",
    ]
    
    for p in preguntes:
        preguntar(p)
        print("\n" + "="*60)
```

## Pas 5: Avaluacio qualitativa (10 min)

Crea `evaluar.py`:

```python
import json
from consultar import preguntar

# Test cases amb respostes esperades
tests = [
    {
        "pregunta": "Quan es planten els tomàquets?",
        "ha_de_contenir": ["abril", "trasplanten"],
        "no_ha_de_contenir": ["hivern", "gener"]
    },
    {
        "pregunta": "Quin sensor mesura la humitat del terra?",
        "ha_de_contenir": ["Capacitive", "Soil"],
        "no_ha_de_contenir": ["DHT22", "DS18B20"]
    },
    {
        "pregunta": "Com es reguen els enciams?",
        "ha_de_contenir": ["diari"],
        "no_ha_de_contenir": ["setmanal"]
    },
]

print("Avaluant qualitat del RAG...\n")
correctes = 0
for test in tests:
    print(f"Pregunta: {test['pregunta']}")
    resposta = preguntar(test['pregunta'])
    print(f"\nValidant...")
    
    # Comprovar contingut
    te_correcte = all(p in resposta for p in test['ha_de_contenir'])
    no_incorrecte = all(p not in resposta for p in test['no_ha_de_contenir'])
    
    if te_correcte and no_incorrecte:
        print("[OK] Resposta valida\n")
        correctes += 1
    else:
        print(f"[FAIL] Falten: {test['ha_de_contenir']}")
        print(f"       Hi ha incorrectes: {test['no_ha_de_contenir']}\n")
    print("-" * 60)

print(f"\nResultat final: {correctes}/{len(tests)} = {correctes/len(tests)*100:.0f}%")
```

## Pas 6: Optimitzacio - chunking millorat (10 min)

Crea `indexar_v2.py` amb chunking per seccions:

```python
import chromadb
import ollama
import re
from pathlib import Path

def carregar_documents(base_path):
    docs = []
    for md_file in Path(base_path).rglob("*.md"):
        docs.append({
            'path': str(md_file),
            'content': md_file.read_text(encoding='utf-8'),
            'filename': md_file.name,
        })
    return docs

def chunk_per_seccio(text):
    """Parteix per seccions (H2, H3)."""
    # Separem per H2 (##)
    seccions = re.split(r'\n## ', text)
    chunks = []
    for seccio in seccions:
        seccio = seccio.strip()
        if not seccio:
            continue
        # Si la seccio es massa llarga (>1500 chars), la parteixo per paragrafs
        if len(seccio) > 1500:
            paragrafs = seccio.split('\n\n')
            chunk_actual = ""
            for p in paragrafs:
                if len(chunk_actual) + len(p) <= 800:
                    chunk_actual += "\n\n" + p if chunk_actual else p
                else:
                    if chunk_actual:
                        chunks.append(chunk_actual.strip())
                    chunk_actual = p
            if chunk_actual:
                chunks.append(chunk_actual.strip())
        else:
            chunks.append(seccio)
    return chunks

# Carregar i indexar amb el nou chunking
docs = carregar_documents('./documents')

client = chromadb.PersistentClient(path="./chroma_db_v2")
collection = client.get_or_create_collection(
    name="hort_osona",
    metadata={"hnsw:space": "cosine"}
)

try:
    collection.delete(where={})
except:
    pass

for doc in docs:
    chunks = chunk_per_seccio(doc['content'])
    for i, chunk in enumerate(chunks):
        emb = ollama.embeddings(model='nomic-embed-text', prompt=chunk)['embedding']
        collection.add(
            documents=[chunk],
            embeddings=[emb],
            ids=[f"{doc['filename']}_{i}"],
            metadatas=[{'path': doc['path'], 'filename': doc['filename']}]
        )

print(f"Indexats {collection.count()} chunks amb chunking per seccions")
```

## Pas 7: Compara les dues versions (10 min)

Crea `comparar_versions.py`:

```python
import chromadb

client1 = chromadb.PersistentClient(path="./chroma_db")
client2 = chromadb.PersistentClient(path="./chroma_db_v2")
col1 = client1.get_collection("hort_osona")
col2 = client2.get_collection("hort_osona")

preguntes = [
    "Quan es planten els tomàquets?",
    "Quin sensor faig servir per la humitat?",
    "Com es el reg dels enciams?",
]

for pregunta in preguntes:
    print(f"\n{'='*60}\n{pregunta}\n{'='*60}")
    
    print("\n--- V1 (chunking per paragrafs) ---")
    r1 = col1.query(query_texts=[pregunta], n_results=2)
    for doc in r1['documents'][0]:
        print(f"  - {doc[:80]}...")
    
    print("\n--- V2 (chunking per seccions) ---")
    r2 = col2.query(query_texts=[pregunta], n_results=2)
    for doc in r2['documents'][0]:
        print(f"  - {doc[:80]}...")
```

## Validacio

Has acabat si:

- [ ] Has indexat els 3 documents sobre l'Hort Osona.
- [ ] Has fet el sistema RAG complet que respon preguntes.
- [ ] Has avaluat la qualitat amb tests.
- [ ] Has provat chunking per paragrafs vs per seccions.
- [ ] Has vist la diferencia entre les dues estrategies.

## Per aprofundir

- Investiga "hybrid search": combinar cerca vectorial amb BM25 (paraules clau).
- Prova "HyDE" (Hypothetical Document Embeddings): generar una resposta hipotetica i usar-la per cercar.
- Compara el cost de re-indexar nomes el document nou vs tota la col·leccio.
- Investiga "metadata filtering": filtrar per data, tipus, etc.

## Ves un pas mes enlla

**Repte avançat**: Afegeix un sistema de feedback al RAG. Despres de cada resposta, l'usuari pot dir si era bona o dolenta. Guarda aquest feedback. Usa'l per:
1. Detectar quan el sistema falla.
2. Re-entrenar el sistema (re-prioritzar chunks).
3. Avisar quan calgui re-indexar (molts feedbacks negatius).

Aixo es la base d'un sistema RAG que millora amb l'us.
