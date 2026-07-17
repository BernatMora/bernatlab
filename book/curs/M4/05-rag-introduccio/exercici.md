# Exercici practic - Capitol 5: Que es RAG

> 40-55 min · Real al teu servidor

## Objectiu
Entendre el flux de RAG a ma: partir un document en chunks, calcular embeddings, i fer una cerca per semblança. Tot amb un script Python senzill per veure cada pas per separat.

## Requisits

- Python 3.10+
- Ollama instal·lat (per als embeddings)
- 40-55 minuts

## Pas 1: Prepara l'entorn (5 min)

```bash
mkdir -p ~/bernatlab-exercicis/M4/05-rag
cd ~/bernatlab-exercicis/M4/05-rag

python3 -m venv venv
source venv/bin/activate

pip install ollama numpy
```

## Pas 2: Crea un document de prova (5 min)

```bash
cat > hort_osona.md << 'EOF'
# Hort Osona - Manual de cultiu

## Tomàquets
Els tomàquets necessiten sol directe (6-8 hores diaries) i reg regular. 
Es planten a la primavera, despres de les ultimes glaçades. 
Varietats recomanades per a Osona: Montserrat, Poma, Cor de Bou.

## Enciams
Els enciams prefereixen temperatures fresques (15-20 graus). 
Es poden plantar tot l'any menys a l'estiu. 
Reg diari pero sense entollar.

## Sensors
- DS18B20: temperatura del sol
- DHT22: humitat i temperatura ambient
- Capacitive Soil Moisture: humitat del terra
- BME280: pressio atmosferica

## Reg automatic
El sistema de reg automatic s'activa quan la humitat del terra baixa del 30%. 
Es pot programar amb un timer o amb un sensor.
EOF

cat hort_osona.md
```

## Pas 3: Partim el document en chunks (10 min)

Crea `chunks.py`:

```python
import re

with open("hort_osona.md", "r") as f:
    text = f.read()

# Funcio simple de chunking: parteix per seccions (##)
def chunk_by_section(text):
    chunks = []
    sections = re.split(r'\n## ', text)
    for section in sections:
        if section.strip():
            section = section.replace('# Hort Osona - Manual de cultiu\n', '')
            section = '## ' + section if not section.startswith('##') else section
            chunks.append(section.strip())
    return chunks

chunks = chunk_by_section(text)
print(f"Total chunks: {len(chunks)}")
for i, c in enumerate(chunks):
    print(f"\n--- Chunk {i+1} ({len(c)} caracters) ---")
    print(c[:100] + "...")
```

Executa:

```bash
python chunks.py
```

## Pas 4: Calcular embeddings amb Ollama (10 min)

Instal·la un model d'embeddings:

```bash
ollama pull nomic-embed-text
```

Crea `embeddings.py`:

```python
import ollama
import numpy as np
from chunks import chunks

embeddings = []
for i, chunk in enumerate(chunks):
    response = ollama.embeddings(model='nomic-embed-text', prompt=chunk)
    emb = response['embedding']
    embeddings.append(np.array(emb))
    print(f"Chunk {i+1}: vector de {len(emb)} dimensions")

print(f"\nTotal: {len(embeddings)} vectors de {len(embeddings[0])} dimensions")
```

## Pas 5: Fer una cerca per semblança (10 min)

Crea `cerca.py`:

```python
import ollama
import numpy as np
from chunks import chunks
from embeddings import embeddings

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

pregunta = "Quin sensor faig servir per saber la temperatura del sol?"

emb_pregunta = np.array(ollama.embeddings(model='nomic-embed-text', prompt=pregunta)['embedding'])

sims = [cosine_similarity(emb_pregunta, emb) for emb in embeddings]

indexos = np.argsort(sims)[::-1]

print(f"Pregunta: {pregunta}\n")
print("Chunks ordenats per rellevancia:\n")
for i, idx in enumerate(indexos):
    print(f"{i+1}. Semblança: {sims[idx]:.4f}")
    print(f"   Chunk: {chunks[idx][:80]}...\n")

print("=" * 60)
print("Context per al LLM (els 2 millors chunks):")
print("=" * 60)
for idx in indexos[:2]:
    print(f"\n{chunks[idx]}\n")
```

## Pas 6: Munta el prompt final (5 min)

Crea `prompt_final.py`:

```python
import ollama
from chunks import chunks
from embeddings import embeddings
from cerca import cosine_similarity

pregunta = "Quin sensor faig servir per saber la temperatura del sol?"

emb_pregunta = np.array(ollama.embeddings(model='nomic-embed-text', prompt=pregunta)['embedding'])
sims = [cosine_similarity(emb_pregunta, emb) for emb in embeddings]
indexos = np.argsort(sims)[::-1]

context = "\n\n".join([chunks[idx] for idx in indexos[:2]])

prompt = f"""Respon la pregunta nomes basant-te en el contexte. Si no hi ha informacio, digues-ho.

CONTEXTE:
{context}

PREGUNTA: {pregunta}

RESPOSTA:"""

response = ollama.chat(model='llama3.2:3b', messages=[
    {'role': 'system', 'content': 'Ets un assistent que respon nomes amb la informacio del contexte. Respon en catala.'},
    {'role': 'user', 'content': prompt}
])

print(response['message']['content'])
```

## Pas 7: Avalua la qualitat del RAG (10 min)

Crea `evaluar.py`:

```python
import ollama
from chunks import chunks
from embeddings import embeddings
from cerca import cosine_similarity
import numpy as np

preguntes_test = [
    ("Quin sensor faig servir per saber la temperatura del sol?", "Sensors"),
    ("Com es el reg dels enciams?", "Enciams"),
    ("Quan es planten els tomàquets?", "Tomàquets"),
    ("Quina varietat de tomàquet es bona per Osona?", "Tomàquets"),
    ("Com funciona el reg automatic?", "Reg automatic"),
    ("Quin es el millor fertilitzant?", None),  # No hauria de trobar res
]

correctes = 0
total = 0

for pregunta, chunk_esperat in preguntes_test:
    if chunk_esperat is None:
        continue
    
    emb_pregunta = np.array(ollama.embeddings(model='nomic-embed-text', prompt=pregunta)['embedding'])
    sims = [cosine_similarity(emb_pregunta, emb) for emb in embeddings]
    millor_idx = np.argmax(sims)
    
    chunk_trobat = chunks[millor_idx][:50]
    match = chunk_esperat.lower() in chunks[millor_idx].lower()
    
    print(f"\nPregunta: {pregunta}")
    print(f"Esperat: {chunk_esperat}")
    print(f"Trobat:  {chunk_trobat}...")
    print(f"Correcte: {'SI' if match else 'NO'}")
    
    total += 1
    if match:
        correctes += 1

print(f"\n{'='*50}")
print(f"Resultat: {correctes}/{total} = {correctes/total*100:.0f}%")
```

## Validacio

Has acabat si:

- [ ] Has preparat l'entorn amb venv i dependencies.
- [ ] Has partit el document en chunks.
- [ ] Has calculat els embeddings.
- [ ] Has fet una cerca per semblança.
- [ ] Has completat el prompt RAG i el LLM ha respost correctament.
- [ ] Has avaluat la qualitat amb varies preguntes.

## Per aprofundir

- Prova altres preguntes: "Quan he de plantar tomàquets?", "Com funciona el reg automatic?".
- Investiga altres models d'embeddings: `mxbai-embed-large`, `all-minilm`.
- Prova amb un document mes llarg (100 pagines) i compara la velocitat.
- Experimenta amb diferents estrategies de chunking (per paragrafs, per frases, per finestra de N paraules).
- Investiga "re-ranking": un model que reordena els chunks per millor rellevancia.

## Ves un pas mes enlla

**Repte avançat**: Implementa un sistema RAG amb ChromaDB (en lloc de la teva base de dades casolana). ChromaDB es una base de dades de vectors optimitzada que:
- Persistent en fitxers.
- Cerca mes rapida.
- Permet metadades (filtrar per data, autor, etc.).

Aixo es el que veuras al capitol 7 (vector databases).
