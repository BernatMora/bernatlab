# Exercici practic - Capitol 1: Que es un LLM

> 35-50 min · Sense necessitat de GPU

## Objectiu
Entendre de primera ma que vol dir "un LLM genera text paraula a paraula" fent una simulacio molt simple amb Python. No cal tenir Ollama ni cap model instal·lat: nomes el Python de sempre. A mes, farem proves amb el concepte d'al·lucinacio i finestra de context.

## Requisits

- Python 3.10 o superior disponible
- 35-50 minuts
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

## Pas 5: Simula una al·lucinacio (8 min)

Crea `hallucination_demo.py` per veure com un "model" inventaria respostes quan no te informacio:

```python
import random

# "Coneixement" limitat: nomes sap sobre gats
coneixement = {
    "gat": ["ronroneja", "menja peix", "dorm"],
    "gos": ["lladra", "menja ossos", "juga"],
}

def respondre(pregunta):
    paraules = pregunta.lower().split()
    for p in paraules:
        if p in coneixement:
            return f"Sobre {p}: {', '.join(coneixement[p])}."
    # Si no troba res, INVENTA (aixo es l'al·lucinacio)
    return f"El {random.choice(['gos', 'gat', 'ocell', 'peix'])} {random.choice(['vola', 'canta', 'neda', 'balla'])} per la nit."

# Provem preguntes
preguntes = [
    "Que sap un gat?",
    "Com es un unicorn?",
    "Que fan els dofins?",
    "Quin es el preu de la gasolina?",
]

for p in preguntes:
    print(f"P: {p}")
    print(f"R: {respondre(p)}\n")
```

Que observes? El model "respon" amb conviccio fins i tot quan no en sap res.

## Pas 6: Simula la finestra de context (7 min)

Crea `context_window.py`:

```python
# Simula un model amb finestra de context de 5 tokens
context = []

def afegir(text):
    global context
    context.append(text)
    # Finestra de 5: nomes recordem els ultims 5 missatges
    if len(context) > 5:
        context = context[-5:]

def estat():
    print(f"Context actual ({len(context)} missatges):")
    for i, m in enumerate(context):
        print(f"  {i+1}. {m}")
    print("-" * 40)

# Simulem una conversa llarga
for i in range(8):
    afegir(f"Missatge {i+1}: bla bla bla")
    estat()
```

Que passa amb els missatges 1, 2 i 3 quan el context arriba a 8? Es el mateix que li passa a un LLM real quan la conversa es fa llarga.

## Pas 7: Documenta les reflexions (10 min)

Crea un fitxer `reflexions.md` amb:

- La sortida de 5 execucions del Pas 3.
- Les teves respostes al Pas 5 i 6.
- Una analogia entre el teu script de 30 linies i un model real de 7B parametres.
- Quin dels tres experiments (generacio, al·lucinacio, context) t'ha semblat mes revelador?
- Quin impact te això en la teva manera de pensar quan usis un LLM real al BernatLab?

## Pas 8 (opcional): Compara amb un LLM real

Si ja tens Ollama instal·lat (capitol 2), pots fer aquesta comparativa:

```bash
ollama pull llama3.2:1b
```

```python
import ollama
pregunta = "Quants habitants te Vic?"
r = ollama.chat(model='llama3.2:1b', messages=[
    {'role': 'user', 'content': pregunta}
])
print(r['message']['content'])
```

Mira la resposta. Es exacta? Es propera? Compara-la amb la que donaria el teu "model" de manualitat. Que hi veus de comu?

## Validacio

Has acabat si:

- [ ] Has creat el directori i el fitxer `manual_llm.py`.
- [ ] L'has executat i has vist la sortida aleatoria.
- [ ] Has provat com a minim 2 modificacions del Pas 4.
- [ ] Has entès la simulacio d'al·lucinacio (Pas 5).
- [ ] Has vist com el context es "oblida" (Pas 6).
- [ ] Has escrit el fitxer `reflexions.md` amb conclusions personals.

## Per aprofundir

- Investiga quants parametres te `random.choice` vs un model real (Google "llama 3 parameters").
- Llegeix sobre el concepte de "temperature" en LLMs: es el parametre que controla l'aleatorietat.
- Mira el codi de `nanoGPT` de Karpathy (un LLM minimalista en ~300 linies de Python).
- Busca informacio sobre "logit bias" i "top-k sampling": com es controla la creativitat del model.

## Ves un pas mes enlla

**Repte avançat**: Escriu un script Python que simuli un model de TRIGRAMES (3 paraules) en lloc de BIGRAMES. Observa com la "memoria" augmenta i les frases tenen mes coherencia. Aquest experiment et donara intuicio de per que els models reals usen finestres de 4k-128k tokens: el context es el que fa que el text "tingui sentit" mes enlla de les dues ultimes paraules.
