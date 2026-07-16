# Exercici practic - Capitol 1: Que es un LLM

> 20-30 min · Sense necessitat de GPU

## Objectiu

Entendre de primera ma que vol dir "un LLM genera text paraula a paraula" fent una simulacio molt simple amb Python. No cal tenir Ollama ni cap model instal·lat: nomes el Python de sempre.

## Requisits

- Python 3.10 o superior disponible
- 20-30 minuts
- Cap dependència externa

## Pas 1: Crea el directori de treball (2 min)

```bash
mkdir -p ~/bernatlab-exercicis/M4/01-llm
cd ~/bernatlab-exercicis/M4/01-llm
```

## Pas 2: Escriu un "model" de manualitat (5 min)

Crea un fitxer `manual_llm.py`. Aquest script NO es un LLM real, pero imita el seu comportament basic: tria la paraula seguent a partir de la frequencia en un text d'entrenament.

```python
import random
from collections import defaultdict

# "Entrenament": un text curt que farem servir com a corpus
corpus = """
el gat beu llet el gos menja ossos el gat menja peix
el gos beu aigua el gat dorm el gos juga el gat juga
""".lower().split()

# Construim un model de bigrames (parelles de paraules)
bigrams = defaultdict(list)
for i in range(len(corpus) - 1):
    bigrams[corpus[i]].append(corpus[i + 1])

def generar(paraula_inicial, longitud=10):
    paraula = paraula_inicial
    resultat = [paraula]
    for _ in range(longitud):
        candidates = bigrams.get(paraula, [])
        if not candidates:
            break
        paraula = random.choice(candidates)
        resultat.append(paraula)
    return " ".join(resultat)

# Generem 5 frases
for i in range(5):
    print(generar("el", 6))
```

## Pas 3: Executa'l (3 min)

```bash
python3 manual_llm.py
```

Observa la sortida. Veus com cada vegada surt una frase diferent? Es la "no-determinacio" dels LLMs reals: mateixa entrada, possibles sortides diferents.

## Pas 4: Experimenta (10 min)

Prova modificacions per entendre com es comporta:

- Canvia el corpus per un text mes llarg (un paràgraf d'un llibre, per exemple).
- Substitueix `random.choice` per `max` (sempre la paraula mes frequent). Que passa?
- Afegeix una llavor fixa al principi: `random.seed(42)`. Que canvia?
- Compara la sortida amb un corpus de 5 paraules vs 50. Que observes?

## Pas 5: Reflexiona (5 min)

Contesta mentalment (o al README que crearas al pas 6):

- Aquest "model" enten el que diu? Per que no?
- Que passaria si el corpus fos Wikipedia sencera? Milloraria la qualitat?
- Quina analogia hi ha amb un LLM real de 7B parametres?

## Pas 6: Documenta (5 min)

Crea un fitxer `reflexions.md` amb:

- La sortida de 5 execucions del Pas 3.
- Les teves respostes al Pas 5.
- Una analogia entre el teu script de 30 linies i un model real de 7B parametres.

## Validacio

Has acabat si:
- [ ] Has creat el directori i el fitxer `manual_llm.py`.
- [ ] L'has executat i has vist la sortida aleatoria.
- [ ] Has provat com a minim 2 modificacions del Pas 4.
- [ ] Has escrit el fitxer `reflexions.md`.

## Per aprofundir

- Investiga quants parametres te `random.choice` vs un model real (Google "llama 3 parameters").
- Llegeix sobre el concepte de "temperature" en LLMs: es el parametre que controla l'aleatorietat.
- Mira el codi de `nanoGPT` de Karpathy (un LLM minimalista en ~300 linies de Python).
