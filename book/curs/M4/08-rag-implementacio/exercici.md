# Exercici practic - Capitol 8: RAG - implementacio completa

> 45-60 min - RPi amb Ollama

## Objectiu

Muntar un pipeline RAG complet de cap a peus: carregar documents, fragmentarlos, generar embeddings, indexarlos, i respondre preguntes.

## Requisits

- Ollama funcionant amb el model `nomic-embed-text` i `llama3.2` (o similar)
- ChromaDB instal·lat
- Python 3.11
- 5-10 fitxers .md de prova (pots crear-ne alguns sobre l'hort)

## Pas 1: Preparar documents de prova (10 min)

Crea una carpeta amb 5-10 fitxers `.md` curts sobre horticultura:

```bash
mkdir -p ~/rag-test/docs
cd ~/rag-test/docs

# Crear 5 fitxers d'exemple
cat > tomàquet.md << 'EOF'
# El tomàquet
El tomàquet (Solanum lycopersicum) es cultiva a l'estiu. Vol sol directe i reg moderat. Es sembra entre març i maig. Les plagues mes comuns son el mildiu i la mosca blanca. Es bona companyia de la mongeta i l'alfàbrega. S'ha de regar al mati, mai al vespre.
EOF

cat > enciam.md << 'EOF'
# L'enciam
L'enciam (Lactuca sativa) es una verdura de fulla. Es cultiva tot l'any excepte l'estiu mes fort. Vol reg frequent pero no xuclar. Es sembra cada 3 setmanes per collita esglaonada. Plagues: llimacs i pugons. Companyia bona amb la pastanaga i el rave.
EOF

cat > carbassa.md << 'EOF'
# La carbassa
La carbassa (Cucurbita maxima) vol molt d'espai i sol. Es sembra a la primavera un cop passades les gelades. Reg abundant pero espaiat. Es cull a la tardor. Plagues: aranya roja i pugons. Es bona companyia del blat de moro.
EOF

cat > mongeta.md << 'EOF'
# La mongeta
La mongeta (Phaseolus vulgaris) fixa nitrogen al sol. Es sembra a la primavera. Volsol i reg moderat. Es cull entre juliol i octubre. Plagues: coleopters. Bona companyia del tomàquet i la pastanaga. Millor no plantar amb ceba o all.
EOF

cat > calçot.md << 'EOF'
# El calçot
El calçot (Allium cepa) es un tipus de ceba. Es sembra a la tardor. Es calça (cobrir la base) a l'estiu per blanquejar. Es cull entre gener i març. Vol reg moderat. Plagues: mosca de la ceba. Es menja a la calcotada.
EOF
```

## Pas 2: Script d'indexacio complet (15 min)

Crea `indexar.py`:

```python
import chromadb
import requests
from pathlib import Path

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="hort")

def get_embedding(text, model="nomic-embed-text"):
    r = requests.post(
        "http://localhost:11434/api/embeddings",
        json={"model": model, "prompt": text}
    )
    return r.json()['embedding']

def chunk_text(text, size=300, overlap=50):
    words = text.split()
    return [' '.join(words[i:i+size])
            for i in range(0, len(words), size - overlap)]

# Carregar i indexar
doc_id = 0
for md_file in Path("./docs").glob("*.md"):
    content = md_file.read_text(encoding='utf-8')
    chunks = chunk_text(content)
    for chunk in chunks:
        emb = get_embedding(chunk)
        collection.add(
            embeddings=[emb],
            documents=[chunk],
            metadatas=[{"source": md_file.name}],
            ids=[f"doc_{doc_id}"]
        )
        doc_id += 1
    print(f"  Indexat {md_file.name}: {len(chunks)} fragments")

print(f"\nTotal: {doc_id} fragments indexats a ChromaDB")
```

Executa:
```bash
cd ~/rag-test
python indexar.py
```

## Pas 3: Script de consulta (15 min)

Crea `consultar.py`:

```python
import chromadb
import requests

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection(name="hort")

def get_embedding(text, model="nomic-embed-text"):
    r = requests.post(
        "http://localhost:11434/api/embeddings",
        json={"model": model, "prompt": text}
    )
    return r.json()['embedding']

def ask(question, k=3):
    # 1. Embedding de la pregunta
    q_emb = get_embedding(question)
    # 2. Cerca
    results = collection.query(
        query_embeddings=[q_emb],
        n_results=k
    )
    # 3. Preparar contexte
    context = "\n\n".join(results['documents'][0])
    fonts = [m['source'] for m in results['metadatas'][0]]
    # 4. Prompt al LLM
    prompt = f"""Respon en catala nomes amb el contexte donat. Si no saps, digues-ho.

Context:
{context}

Pregunta: {question}
Resposta:"""
    # 5. Generar
    r = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama3.2", "prompt": prompt, "stream": False}
    )
    return r.json()['response'], fonts

# Proves
preguntes = [
    "Com he de regar el tomàquet?",
    "Quan es sembra l'enciam?",
    "Quines plagues te la carbassa?",
    "Que puc plantar al costat de la mongeta?"
]

for p in preguntes:
    print(f"\nQ: {p}")
    resposta, fonts = ask(p)
    print(f"R: {resposta}")
    print(f"Fonts: {fonts}")
```

Executa:
```bash
python consultar.py
```

## Pas 4: Afinar el prompt (10 min)

Observa les respostes. Prova a:
- Afegir "Sigues concis, max 2-3 frases" al prompt.
- Canviar k=5 i veure si canvia la resposta.
- Canviar la instruccio del prompt per ser mes estricte ("Cita nomes informacio del contexte").

## Validacio

Has acabat si:
- [ ] Tinc 5 documents .md creats
- [ ] L'script d'indexacio ha funcionat i mostra el total
- [ ] L'script de consulta respon 4 preguntes correctament
- [ ] Les respostes inclouen informacio especifica dels documents (no generals)
- [ ] He provat almenys una optimitzacio de prompt

## Per aprofundir

- Prova amb una col·lecció mes gran (50+ documents).
- Afegeix un sistema de cites: "Segons el document X...".
- Guarda un log de les preguntes i respostes per avaluar qualitat.
- Implementa streaming de la resposta (pas a pas).
