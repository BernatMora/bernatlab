# Exercici practic - Capitol 6: Embeddings

> 35-50 min · Real amb Ollama

## Objectiu
Calcular embeddings de diferents textos amb Ollama, comparar semblances, entendre les limitacions. Acabaras sabent quan un embedding es "bo" i quan falla.

## Requisits

- Ollama amb `nomic-embed-text` instal·lat
- Python amb `requests` i `numpy`
- 35-50 minuts

## Pas 1: Prepara l'entorn (3 min)

```bash
mkdir -p ~/bernatlab-exercicis/M4/06-embeddings
cd ~/bernatlab-exercicis/M4/06-embeddings

python3 -m venv venv
source venv/bin/activate

pip install requests numpy
```

Assegura't que tens el model:

```bash
ollama pull nomic-embed-text
```

## Pas 2: Primer embedding (5 min)

Crea `primer_embedding.py`:

```python
import requests
import numpy as np

def embedding(text, model='nomic-embed-text'):
    r = requests.post(
        'http://localhost:11434/api/embeddings',
        json={'model': model, 'prompt': text}
    )
    return np.array(r.json()['embedding'])

text = "El gat menja peix"
emb = embedding(text)
print(f"Text: {text}")
print(f"Embedding shape: {emb.shape}")
print(f"Primeres 10 dimensions: {emb[:10]}")
print(f"Norma (longitud): {np.linalg.norm(emb):.4f}")
```

Observa: tens un vector de 768 dimensions. La norma sol ser propera a 1 (els models normalitzen).

## Pas 3: Compara semblances entre frases (10 min)

Crea `semblances.py`:

```python
import requests
import numpy as np

def embedding(text):
    r = requests.post(
        'http://localhost:11434/api/embeddings',
        json={'model': 'nomic-embed-text', 'prompt': text}
    )
    return np.array(r.json()['embedding'])

def cos_sim(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

frases = [
    "El gat menja peix",
    "El moix menja peix",  # Sinonim (moix = gat en catala)
    "El gos menja ossos",
    "L'avio vola pel cel",
    "M'agrada menjar sushi",
    "Plou a bots i barrals",
]

# Calcular tots els embeddings
embs = [embedding(f) for f in frases]

# Matriu de semblances
print("Matriu de semblances cosinus:\n")
print("          ", "  ".join([f"{i+1:4d}" for i in range(len(frases))]))
for i, f1 in enumerate(frases):
    sims = [cos_sim(embs[i], embs[j]) for j in range(len(frases))]
    print(f"Frase {i+1:2d}: " + "  ".join([f"{s:5.2f}" for s in sims]))

print("\nDetalls per parelles interessants:")
print(f"'Gat menja peix' vs 'Moix menja peix': {cos_sim(embs[0], embs[1]):.3f}")
print(f"'Gat menja peix' vs 'Gos menja ossos': {cos_sim(embs[0], embs[2]):.3f}")
print(f"'Gat menja peix' vs 'Plou a bots i barrals': {cos_sim(embs[0], embs[5]):.3f}")
```

Que observes? Les frases sinonimes haurien de tenir semblança >0.8. Les no relacionades, <0.4.

## Pas 4: Cerca els mes semblants (10 min)

Crea `cerca_topk.py`:

```python
import requests
import numpy as np

def embedding(text):
    r = requests.post('http://localhost:11434/api/embeddings',
                     json={'model': 'nomic-embed-text', 'prompt': text})
    return np.array(r.json()['embedding'])

def cos_sim(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Base de dades de documents
documents = {
    'doc1': 'Com plantar tomàquets a l\'hort: cal sol directe i reg moderat.',
    'doc2': 'El reg automatic s\'activa quan la humitat baixa del 30%.',
    'doc3': 'Els enciams es planten a la primavera i tardor.',
    'doc4': 'Les plagues mes comunes son els pugons i l\'aranya roja.',
    'doc5': 'Un sensor DS18B20 mesura la temperatura del sol.',
    'doc6': 'La fotosintesi es el proces per el qual les plantes fan sucre.',
    'doc7': 'Com fer compost: barreja restes de fruita i verdura.',
    'doc8': 'L\'adob verd millora l\'estructura del sol.',
}

# Pregunta de l'usuari
pregunta = "Com regar les plantes?"
emb_pregunta = embedding(pregunta)

# Calcular semblances amb tots els documents
sims = []
for doc_id, doc_text in documents.items():
    emb_doc = embedding(doc_text)
    sim = cos_sim(emb_pregunta, emb_doc)
    sims.append((doc_id, doc_text, sim))

# Ordenar per semblança
sims.sort(key=lambda x: x[2], reverse=True)

print(f"Pregunta: {pregunta}\n")
print("Top 5 documents mes rellevants:\n")
for i, (doc_id, doc_text, sim) in enumerate(sims[:5]):
    print(f"{i+1}. {doc_id} (sim: {sim:.3f})")
    print(f"   {doc_text}\n")
```

## Pas 5: Compara dos models d'embeddings (10 min)

Crea `compara_models.py`:

```bash
ollama pull mxbai-embed-large
```

```python
import requests
import numpy as np

def embedding(text, model='nomic-embed-text'):
    r = requests.post('http://localhost:11434/api/embeddings',
                     json={'model': model, 'prompt': text})
    return np.array(r.json()['embedding'])

def cos_sim(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

text1 = "El gat menja peix"
text2 = "El moix menja peix"

# Test amb dos models
for model in ['nomic-embed-text', 'mxbai-embed-large']:
    e1 = embedding(text1, model)
    e2 = embedding(text2, model)
    sim = cos_sim(e1, e2)
    print(f"{model}: shape={e1.shape}, sim={sim:.4f}")

# Important: embeddings de models diferents NO es poden mesclar!
e1_nomic = embedding(text1, 'nomic-embed-text')
e1_mxbai = embedding(text1, 'mxbai-embed-large')
print(f"\nMateix text, models diferents: sim={cos_sim(e1_nomic, e1_mxbai):.3f}")
print("(Hauria de ser proper a 0 o aleatori, no ~0.9)")
```

## Pas 6: Embeddings sobre el BernatLab (10 min)

Crea `bernatlab_test.py`:

```python
import requests
import numpy as np

def embedding(text):
    r = requests.post('http://localhost:11434/api/embeddings',
                     json={'model': 'nomic-embed-text', 'prompt': text})
    return np.array(r.json()['embedding'])

def cos_sim(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Fragments d'un runbook del BernatLab
fragments = [
    "Si el contenidor de Mosquitto no arranca, comprova els logs amb 'docker logs mqtt'",
    "Per actualitzar InfluxDB: docker compose pull && docker compose up -d",
    "L'API de l'hort escolta al port 8000 i retorna dades JSON",
    "El backup es fa diariament a les 3 de la matinada amb borgbackup",
    "Si Grafana mostra 'no data', comprova que InfluxDB te la base de dades 'hort'",
]

# Pregunta
pregunta = "Com reiniciar el servei de missatgeria?"
emb_pregunta = embedding(pregunta)

# Calcular semblances
sims = [(cos_sim(emb_pregunta, embedding(f)), f) for f in fragments]
sims.sort(reverse=True)

print(f"Pregunta: {pregunta}\n")
for sim, frag in sims:
    print(f"  {sim:.3f}: {frag}")
```

## Validacio

Has acabat si:

- [ ] Has calculat el teu primer embedding.
- [ ] Has vist la matriu de semblances entre frases.
- [ ] Has implementat cerca top-k sobre una base de dades.
- [ ] Has comparat dos models d'embeddings.
- [ ] Has provat amb contingut real del BernatLab.

## Per aprofundir

- Investiga la diferencia entre embeddings normalitzats i no normalitzats.
- Prova "matryoshka embeddings": un model que pot donar embeddings de diferents mides.
- Investiga "instruction-tuned embeddings": models que entenen instruccions a la query.
- Compara la velocitat de calcul entre diferents models.

## Ves un pas mes enlla

**Repte avançat**: Construeix un petit "detector de temes" que:
1. Calculi embeddings de tots els correus rebuts en un mes.
2. Faci clustering (k-means) per agrupar correus similars.
3. Per cada grup, calculi l'embedding promig (centroide).
4. Et mostri els 5 temes mes frequents del mes.

Aixo es la base d'un sistema d'analisi de correu automatic, molt util per a qualsevol negoci o homelab.
