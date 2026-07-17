# Exercici practic - Capitol 10: Aplicacio a Hort Osona

> 50-70 min · Real al teu servidor

## Objectiu
Muntar el sistema d'IA complet per a l'Hort Osona: clonar la base de coneixement, indexar-la, configurar Open WebUI, i provar el sistema. Es l'exercici final del modul.

## Requisits

- RPi o servidor amb Ollama
- 50-70 minuts
- 10 GB d'espai lliure
- Conexio a Internet

## Pas 1: Clonar la base de coneixement (5 min)

```bash
mkdir -p ~/hort-osona
cd ~/hort-osona

git clone https://github.com/BernatMora/hort-osona.git
cd hort-osona

ls
# Hauries de veure ~80 fitxers .md
```

Mira alguns dels fitxers per entendre l'estructura:

```bash
ls | head -20
cat fitxa-tomatecs.md  # o el que hi hagi
```

## Pas 2: Preparar l'entorn Python (5 min)

```bash
mkdir -p ~/bernatlab-exercicis/M4/10-hort-osona
cd ~/bernatlab-exercicis/M4/10-hort-osona

python3 -m venv venv
source venv/bin/activate

pip install chromadb ollama
```

Assegura't que tens Ollama i un model d'embeddings:

```bash
ollama pull nomic-embed-text
ollama pull llama3.2:3b
```

## Pas 3: Script d'indexacio (15 min)

Crea `indexar_hort.py`:

```python
import chromadb
import ollama
from pathlib import Path
import time

def carregar_documents(base_path):
    """Carrega tots els .md de l'Hort Osona."""
    docs = []
    for md_file in Path(base_path).rglob("*.md"):
        content = md_file.read_text(encoding='utf-8')
        # Ignorar fitxers massa petits (titols, indexos)
        if len(content) < 100:
            continue
        docs.append({
            'path': str(md_file.relative_to(base_path)),
            'content': content,
            'filename': md_file.name,
        })
    return docs

def chunk_per_seccio(text, max_chunk=800):
    """Parteix per seccions (##, ###)."""
    import re
    seccions = re.split(r'\n##? ', text)
    chunks = []
    for seccio in seccions:
        seccio = seccio.strip()
        if not seccio or len(seccio) < 50:
            continue
        if len(seccio) > max_chunk:
            # Parteixo per paragrafs
            paragrafs = seccio.split('\n\n')
            actual = ""
            for p in paragrafs:
                if len(actual) + len(p) <= max_chunk:
                    actual += "\n\n" + p if actual else p
                else:
                    if actual:
                        chunks.append(actual.strip())
                    actual = p
            if actual:
                chunks.append(actual.strip())
        else:
            chunks.append(seccio)
    return chunks

# Indexar
print("Carregant documents de l'Hort Osona...")
base_path = Path.home() / 'hort-osona' / 'hort-osona'
docs = carregar_documents(base_path)
print(f"Trobats {len(docs)} documents")

print("\nFent chunking...")
tots_chunks = []
metadades = []
ids = []
for doc in docs:
    chunks = chunk_per_seccio(doc['content'])
    for i, chunk in enumerate(chunks):
        tots_chunks.append(chunk)
        ids.append(f"{doc['filename']}_{i}")
        metadades.append({
            'path': doc['path'],
            'filename': doc['filename'],
            'chunk_index': i,
        })

print(f"Total chunks: {len(tots_chunks)}")

# Inicialitzar ChromaDB
print("\nInicialitzant ChromaDB...")
client = chromadb.PersistentClient(path="./hort_chroma_db")
collection = client.get_or_create_collection(
    name="hort_osona",
    metadata={"hnsw:space": "cosine"}
)

# Netejar si ja existia
try:
    existing = collection.count()
    if existing > 0:
        print(f"Col·leccio ja te {existing} chunks. Esborrant...")
        collection.delete(where={})
except Exception as e:
    print(f"Netegant: {e}")

# Calcular embeddings
print(f"\nCalculant {len(tots_chunks)} embeddings (pot trigar uns minuts)...")
inici = time.time()
batch_size = 50

for i in range(0, len(tots_chunks), batch_size):
    batch_chunks = tots_chunks[i:i+batch_size]
    batch_ids = ids[i:i+batch_size]
    batch_metas = metadades[i:i+batch_size]
    
    embeddings = []
    for chunk in batch_chunks:
        emb = ollama.embeddings(model='nomic-embed-text', prompt=chunk)['embedding']
        embeddings.append(emb)
    
    collection.add(
        documents=batch_chunks,
        embeddings=embeddings,
        ids=batch_ids,
        metadatas=batch_metas
    )
    
    if (i+batch_size) % 100 == 0 or (i+batch_size) >= len(tots_chunks):
        print(f"  {min(i+batch_size, len(tots_chunks))}/{len(tots_chunks)} chunks indexats")

durada = time.time() - inici
print(f"\nIndexacio completada en {durada/60:.1f} minuts")
print(f"Total chunks a la DB: {collection.count()}")
```

Executa'l:

```bash
python indexar_hort.py
```

## Pas 4: Script de consulta (10 min)

Crea `consultar_hort.py`:

```python
import chromadb
import ollama

def obtenir_embedding(text):
    return ollama.embeddings(model='nomic-embed-text', prompt=text)['embedding']

def cercar(pregunta, n=4):
    client = chromadb.PersistentClient(path="./hort_chroma_db")
    collection = client.get_collection("hort_osona")
    
    emb = obtenir_embedding(pregunta)
    resultats = collection.query(
        query_embeddings=[emb],
        n_results=n
    )
    return resultats

def respondre(pregunta, temperatura=0.3):
    """Consulta + resposta amb citacions."""
    resultats = cercar(pregunta, n=4)
    chunks = resultats['documents'][0]
    fontes = resultats['metadatas'][0]
    
    # Preparar contexte
    context = "\n\n---\n\n".join([
        f"[{f['filename']}]\n{c}" 
        for c, f in zip(chunks, fontes)
    ])
    
    # Generar resposta
    prompt = f"""Ets un expert en horticultura a Osona (Catalunya).
Respon la pregunta basant-te nomes en la informacio proporcionada.
Si no tens la informacio, digues-ho honestament.
Respon en catala, amb concisio (max 250 paraules).
Cita les fonts quan sigui rellevant.

DOCUMENTS DE REFERENCIA:
{context}

PREGUNTA: {pregunta}

RESPOSTA:"""
    
    r = ollama.chat(
        model='llama3.2:3b',
        messages=[
            {'role': 'system', 'content': 'Ets un expert pagès d\'Osona amb 30 anys d\'experiencia. Coneixes totes les plantes, tecniques i tradicions locals. Respon en catala.'},
            {'role': 'user', 'content': prompt}
        ],
        options={'temperature': temperatura}
    )
    
    return r['message']['content'], chunks, fontes

# Proves
if __name__ == '__main__':
    preguntes = [
        "Quan he de plantar tomàquets?",
        "Com es el reg dels enciams?",
        "Tinc plagues de pugons, que puc fer?",
        "Quin sensor mesura la humitat del terra?",
        "Quines associacions son bones amb les tomaqueres?",
    ]
    
    for p in preguntes:
        print(f"\n{'='*60}")
        print(f"PREGUNTA: {p}")
        print('='*60)
        resposta, chunks, fontes = respondre(p)
        print(f"\nRESPOSTA:\n{resposta}")
        print(f"\nFONTS: {', '.join(set(f['filename'] for f in fontes))}")
```

## Pas 5: Instal·lar Open WebUI (10 min)

```bash
docker run -d --name open-webui \
  --network host \
  -v open-webui-data:/app/backend/data \
  -e OLLAMA_BASE_URL=http://127.0.0.1:11434 \
  --restart always \
  ghcr.io/open-webui/open-webui:main
```

Comprova:

```bash
docker ps | grep open-webui
```

Ara obre un navegador a `http://localhost:8080`. Si no tens navegador a la RPi, obre desde el teu PC (assegurant-te que la RPi es accessible).

## Pas 6: Configurar el sistema de RAG a Open WebUI (10 min)

A Open WebUI:
1. Crea un compte d'admin.
2. Ves a "Workspace" -> "Knowledge".
3. Afegeix una nova coleccio: "Hort Osona".
4. Apunta a la base ChromaDB existent.
5. Configura el prompt del sistema per al model d'hort.

## Pas 7: Avaluacio final (10 min)

Crea `evaluar_final.py`:

```python
from consultar_hort import respondre

# 20 preguntes representatives amb respostes esperades
test = [
    ("Quan plantar tomàquets?", ["abril", "maig"]),
    ("Reg dels enciams?", ["diari"]),
    ("Plagues de tomàquets?", ["pugons"]),
    ("Humitat del terra?", ["capacitive", "sensor"]),
    ("Temperatura del sol?", ["DS18B20"]),
    ("Quan collir?", ["juliol", "octubre"]),
    ("Compost?", ["restes", "orgànic"]),
    ("Adob verd?", ["userda", "trevol"]),
    ("Sol directe tomàquets?", ["6", "8", "hores"]),
    ("Varietats Osona?", ["Montserrat", "Poma"]),
]

correctes = 0
for pregunta, paraules_clau in test:
    resposta, _, _ = respondre(pregunta)
    
    # Comprovar si conte almenys una paraula clau
    te_clau = any(p.lower() in resposta.lower() for p in paraules_clau)
    
    if te_clau:
        correctes += 1
        print(f"[OK]  {pregunta}")
    else:
        print(f"[FAIL] {pregunta}")
        print(f"   Paraules esperades: {paraules_clau}")
        print(f"   Resposta: {resposta[:150]}...")

print(f"\nResultat: {correctes}/{len(test)} = {correctes/len(test)*100:.0f}%")
```

## Validacio

Has acabat si:

- [ ] Has clonat la base de coneixement de l'Hort Osona.
- [ ] Has indexat els 80+ documents.
- [ ] Has provat el sistema amb 5+ preguntes representatives.
- [ ] Has instal·lat Open WebUI.
- [ ] Has configurat el RAG al frontend.
- [ ] Has fet una avaluacio final amb un test de 10 preguntes.

## Per aprofundir

- Investiga "RAG agents": sistemes que poden fer mes d'una cerca per pregunta.
- Prova "function calling": que el LLM pugui cridar eines externes (calendari, sensors).
- Implementa un sistema de feedback: l'usuari puntua les respostes.
- Crea una "personalitat" especifica per al sistema: to, longitud, formalitat.

## Ves un pas mes enlla

**Repte avançat**: Implementa un sistema que integri **dades en temps real**:
1. Connecta el sistema a InfluxDB (lectures de sensors).
2. Permet preguntes com "com esta la humitat del terra ara?".
3. Combina RAG (documents) + query a BD (dades) en una sola resposta.
4. Usa "function calling" per decidir quin tipus de consulta fer.

Aixo es un sistema "agentic" que combina coneixement historic amb dades actuals.
