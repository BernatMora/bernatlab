# Exercici practic - Capitol 3: Triar el model adequat

> 45-60 min · Real a la teva maquina

## Objectiu
Comparar diferents models d'Ollama en termes de velocitat, qualitat i mida. Crearas una taula de referencia que t'ajudara a triar el millor model per a cada tasca al BernatLab.

## Requisits

- Ollama ja instal·lat (capitol 2)
- 4 GB de RAM minim (millor si son 8 GB o mes)
- 45-60 minuts
- Espai en disc: 5-10 GB lliures per als models

## Pas 1: Descarrega 3-4 models diferents (10 min)

Triem un ventall de mides:

```bash
ollama pull llama3.2:1b       # ~1.3 GB, model petit
ollama pull llama3.2:3b       # ~2.0 GB, sweet spot
ollama pull phi3:mini         # ~2.3 GB, optimitzat per raonament
ollama pull gemma2:2b         # ~1.6 GB, alternativa de Google
```

Si tens 8 GB de RAM, tambe pots provar:

```bash
ollama pull mistral:7b        # ~4.1 GB, mes potent pero mes exigent
```

## Pas 2: Crea un benchmark de velocitat (10 min)

Crea `benchmark.py`:

```python
import requests
import time
import json

def benchmark_model(model, prompt, n_runs=3):
    """Executa el prompt N vegades i calcula la mitjana de temps."""
    durades = []
    for i in range(n_runs):
        inici = time.time()
        r = requests.post(
            'http://localhost:11434/api/generate',
            json={'model': model, 'prompt': prompt, 'stream': False}
        )
        durada = time.time() - inici
        durades.append(durada)
        # Comptem tokens generats
        data = r.json()
        tokens = data.get('eval_count', 0)
        tps = tokens / durada if durada > 0 else 0
        print(f"  Run {i+1}: {durada:.2f}s, {tokens} tokens, {tps:.1f} t/s")
    return {
        'model': model,
        'avg_time': sum(durades) / len(durades),
        'min_time': min(durades),
        'max_time': max(durades),
    }

prompt = """Explica el concepte de xarxa neuronal en 5 linies, 
amb un exemple concret. Escriu nomes el text, sense intro."""

models = ['llama3.2:1b', 'llama3.2:3b', 'phi3:mini', 'gemma2:2b']

resultats = []
for model in models:
    print(f"\nBenchmarking {model}...")
    try:
        r = benchmark_model(model, prompt)
        resultats.append(r)
    except Exception as e:
        print(f"Error amb {model}: {e}")

print("\n" + "="*60)
print("RESUM:")
for r in resultats:
    print(f"{r['model']:20s} mitjana: {r['avg_time']:.2f}s")
```

## Pas 3: Avalua la qualitat de les respostes (15 min)

Crea `quality_test.py`:

```python
import requests

# Preguntes dissenyades per avaluar diferents capacitats
preguntes = {
    'basica': "Quants planetes te el sistema solar?",
    'raonament': "Si tinc 3 pomes i en dono la meitat al meu germa, quantes em queden? Explica el calcul.",
    'catala': "Explica en catala que es l'agricultura regenerativa en 2-3 frases.",
    'codi': "Escriu una funcio Python que calculi la mitjana d'una llista de numeros. Nomes el codi, sense explicacio.",
    'creativitat': "Escriu una descripcio poetica d'un hort al capvespre. 4-5 linies.",
}

models_a_provar = ['llama3.2:1b', 'llama3.2:3b', 'phi3:mini']

for model in models_a_provar:
    print(f"\n{'='*60}")
    print(f"MODEL: {model}")
    print('='*60)
    for categoria, pregunta in preguntes.items():
        r = requests.post(
            'http://localhost:11434/api/generate',
            json={'model': model, 'prompt': pregunta, 'stream': False}
        )
        resposta = r.json()['response']
        print(f"\n[{categoria.upper()}]")
        print(f"Q: {pregunta}")
        print(f"R: {resposta[:400]}{'...' if len(resposta) > 400 else ''}")
```

Executa i guarda les sortides. Despres, puntua cada resposta de l'1 al 5 en qualitat.

## Pas 4: Prova la quantitzacio en practica (10 min)

Descarrega una versio especifica en quantitzacio mes alta:

```bash
ollama pull llama3.2:3b-instruct-q8_0
```

Compara'l amb el `llama3.2:3b` normal (que es Q4). Fes servir el mateix prompt i mira:

- Mida descarregada: `ollama list`
- Velocitat: el benchmark
- Qualitat: un parell de preguntes representatives

Que observes? La diferencia Q4 vs Q8 es notable?

## Pas 5: Compara amb tasques especifiques del BernatLab (10 min)

Crea `bernatlab_test.py`:

```python
import requests

# Tasques que farem servir al BernatLab
tasques = [
    ("Resum curt", "Resumeix aquesta linia de log: '2025-01-15 10:23:45 ERROR [mqtt] connection refused to 192.168.1.100:1883'"),
    ("Generar script", "Escriu un script bash que comprovi si el servei nginx esta actiu, i si no, l'inici. Nomes el codi."),
    ("Explicar error", "Explica què vol dir aquest error de Docker: 'bind: address already in use'"),
    ("Catala tecnic", "Descriu en catala com funciona el protocol MQTT en 3-4 frases."),
]

for model in ['llama3.2:1b', 'llama3.2:3b', 'phi3:mini']:
    print(f"\n{'='*60}\nMODEL: {model}\n{'='*60}")
    for nom, prompt in tasques:
        r = requests.post(
            'http://localhost:11434/api/generate',
            json={'model': model, 'prompt': prompt, 'stream': False}
        )
        print(f"\n[{nom}]")
        print(r.json()['response'][:300])
```

## Pas 6: Construeix la teva taula de decisio (5 min)

Crea `README.md` amb les conclusions:

```markdown
# Taula de models al BernatLab

## El meu hardware
- [escriu el teu hardware: RPi 4, 4GB RAM, SSD de 256GB]

## Resultats del benchmark

| Model | Mida | Velocitat | Qualitat | Preu memoria | Recomanat per |
|---|---|---|---|---|---|
| llama3.2:1b | 1.3 GB | 30 t/s | Basica | 1.2 GB | Tasques simples |
| llama3.2:3b | 2.0 GB | 12 t/s | Bona | 2.5 GB | Sweet spot |
| phi3:mini | 2.3 GB | 10 t/s | Excel·lent raonament | 3.0 GB | Analisi |
| gemma2:2b | 1.6 GB | 18 t/s | Bona | 1.8 GB | Alternativa |

## Conclusions
- El model que fare servir per defecte sera: [...]
- Per a tasques critiques fare servir: [...]
- Els models que esborrare: [...]
```

## Validacio

Has acabat si:

- [ ] Has descarregat 3-4 models diferents.
- [ ] Has fet el benchmark de velocitat.
- [ ] Has avaluat la qualitat amb preguntes variades.
- [ ] Has comparat Q4 vs Q8 (opcional).
- [ ] Has provat amb tasques reals del BernatLab.
- [ ] Has construit la teva taula de decisio.

## Per aprofundir

- Investiga els benchmarks oficials: LMSYS Chatbot Arena, Open LLM Leaderboard.
- Prova altres models menys coneguts: `qwen2.5:3b`, `gemma2:9b` (si tens RAM).
- Compara el consum de RAM amb `htop` o `docker stats` mentre el model treballa.
- Investiga "speculative decoding": una tecnica per accelerar models petits.

## Ves un pas mes enlla

**Repte avançat**: Implementa un petit "router" de models. Es un script que:
1. Rep una consulta amb la categoria de tasca.
2. Tria automaticament el model mes adequat (rapid per a resums, potent per a raonament).
3. Fa la crida i retorna la resposta.

Aixo es el primer pas per construir un sistema multi-model al BernatLab.
