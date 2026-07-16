# Exercici practic - Capitol 6: Embeddings

> 30-45 min · Real al teu servidor

## Objectiu

Practicar amb embeddings de veritat: generar-ne, comparar semblances, i entendre quan funcionen be i quan fallen. Acabaras veient com la "cerca per significat" es diferent de la "cerca per paraules".

## Requisits

- Ollama instal·lat
- 30-45 minuts
- ~1 GB d'espai per al model d'embeddings

## Pas 1: Instal·la un model d'embeddings (3 min)

```bash
ollama pull nomic-embed-text
```

Verifica que esta disponible:

```bash
ollama list
```

## Pas 2: Genera embeddings des de la terminal (5 min)

Prova amb text simple:

```bash
curl -s http://localhost:11434/api/embeddings -d '{
  "model": "nomic-embed-text",
  "prompt": "El gat dorm al sofà"
}' | python3 -c "import json,sys; d=json.load(sys.stdin); print('Dimensions:', len(d['embedding'])); print('Primers 5 valors:', d['embedding'][:5])"
```

Hauries de veure 768 dimensions i els primers 5 valors numerics.

## Pas 3: Compara semblances manualment (10 min)

Crea `proves.py`:

```python
import ollama
import numpy as np

def embedding(text):
    """Retorna l'embedding d'un text."""
    return np.array(ollama.embeddings(model='nomic-embed-text', prompt=text)['embedding'])

def cosine_similarity(a, b):
    """Calcula la semblança cosinus entre dos vectors."""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Proves: textos amb diferent grau de semblança
proves = [
    ("El gat dorm al sofà", "El moix està estirat al moble"),  # Molt semblant
    ("El gat dorm al sofà", "El gos juga al parc"),  # Poc semblant
    ("Avui plou a Vic", "Està fent mal temps a Osona"),  # Semblant
    ("Avui plou a Vic", "M'agrada el pernil"),  # Gens semblant
    ("Activa el reg automatic", "Engega el sistema d'aigua"),  # Semblant
    ("Activa el reg automatic", "Tanca la porta"),  # Gens semblant
]

for t1, t2 in proves:
    e1 = embedding(t1)
    e2 = embedding(t2)
    sim = cosine_similarity(e1, e2)
    print(f"Semblança: {sim:.3f}")
    print(f"  T1: {t1}")
    print(f"  T2: {t2}")
    print()
```

Executa:

```bash
python3 proves.py
```

Observa els valors. Coincideixen amb la teva intuicio?

## Pas 4: Cerca per significat vs cerca per paraules (10 min)

Crea `cerca_comparada.py`:

```python
import ollama
import numpy as np

def embedding(text):
    return np.array(ollama.embeddings(model='nomic-embed-text', prompt=text)['embedding'])

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Base de dades de l'Hort Osona
documents = [
    "El sensor DS18B20 mesura la temperatura del sol cada 5 minuts.",
    "El sistema de reg s'activa automaticament a les 7 del mati.",
    "La humitat relativa es manté entre el 60 i el 80 per cent.",
    "Cal podar els tomàquets cada dues setmanes durant l'estiu.",
    "El BME280 detecta canvis de pressio atmosferica.",
    "Els enciams necessiten temperatures fresques.",
    "El sensor DHT22 mesura temperatura i humitat ambiental.",
    "El reg automatic utilitza una electrovalvula de 12V.",
    "A la primavera es planten els primers tomàquets.",
    "La raspberry pi 4 controla tots els sensors i el reg."
]

# Precomputem tots els embeddings
print("Calculant embeddings de tots els documents...")
doc_embeddings = [embedding(doc) for doc in documents]
print(f"Fet. {len(doc_embeddings)} documents indexats.\n")

# Consultes de prova
consultes = [
    "Quin sensor fa servir per saber la calor?",
    "Com es controla l'aigua de l'hort?",
    "Quan he de plantar verdures?",
    "Quin ordinador fa anar tot plegat?",
]

for consulta in consultes:
    print(f"CONSULTA: {consulta}")
    print("-" * 60)
    q_emb = embedding(consulta)

    sims = [(cosine_similarity(q_emb, d_emb), i) for i, d_emb in enumerate(doc_embeddings)]
    sims.sort(reverse=True)

    for sim, idx in sims[:3]:
        print(f"  Semblança {sim:.3f}: {documents[idx]}")
    print()
```

Executa:

```bash
python3 cerca_comparada.py
```

Fixa't en com "Quin sensor fa servir per saber la calor?" troba documents que parlen de sensors de temperatura (DS18B20, DHT22) encara que la paraula "calor" no hi surti. Es la magia dels embeddings.

## Pas 5: Visualitza amb un heatmap simple (10 min)

Crea `visualitza.py`:

```python
import ollama
import numpy as np

def embedding(text):
    return np.array(ollama.embeddings(model='nomic-embed-text', prompt=text)['embedding'])

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Textos curts per visualitzar be
texts = [
    "el gat dorm",
    "el moix estirat",
    "el perro vigilant",
    "avui plou",
    "fa sol",
    "el sistema rega",
    "l'aigua cau",
    "el sensor mesura"
]

print("Calculant matriu de semblances...\n")
embeddings = [embedding(t) for t in texts]
n = len(texts)

# Imprimim una matriu
header = " " * 15 + "".join(f"{i:>6}" for i in range(n))
print(header)
print(" " * 15 + "-" * (6 * n))
for i in range(n):
    row = f"{i:>2} {texts[i][:12]:<12} |"
    for j in range(n):
        sim = cosine_similarity(embeddings[i], embeddings[j])
        row += f"{sim:>6.2f}"
    print(row)

print("\nInterpretacio:")
print("- Diagonal = 1.00 (semblança amb si mateix).")
print("- 0.7-0.9 = molt semblant.")
print("- 0.4-0.7 = relacionat.")
print("- 0.0-0.4 = diferent.")
```

Executa:

```bash
python3 visualitza.py
```

## Pas 6: Documenta conclusions (5 min)

Crea `book/curs/M4/06-embeddings/observacions.md` amb:

- Les semblances que has vist entre textos semblants i diferents.
- Un cas on els embeddings han sorprès (millor del que esperaves).
- Un cas on han fallat (pitjor del que esperaves).
- Conclusions: quan serves mes que la cerca per paraules?

## Validacio

Has acabat si:
- [ ] Has descarregat `nomic-embed-text`.
- [ ] Has generat embeddings des de la terminal.
- [ ] Has comprovat semblances amb text manual.
- [ ] Has fet una cerca per significat sobre una base de 10 documents.
- [ ] Has generat i entès la matriu de semblances.
- [ ] Has documentat les teves observacions.

## Per aprofundir

- Prova amb `mxbai-embed-large` (1024 dimensions) i compara la qualitat.
- Indexa tota la documentacio del BernatLab (el llibre complet) i fes una cerca.
- Prova frases negatives: "M'encanta el sistema de reg" vs "Odio el sistema de reg". Semblants o diferents?
- Investiga el concepte de "fine-tuning d'embeddings" per adaptar-los al teu domini.
