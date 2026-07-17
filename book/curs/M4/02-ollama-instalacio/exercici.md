# Exercici practic - Capitol 2: Instal·lar Ollama, primers passos

> 40-55 min · Real a la teva RPi o maquina local

## Objectiu
Instal·lar Ollama al teu entorn (RPi o Mac/PC), descarregar el teu primer model, xatejar-hi per terminal, i fer la primera crida a l'API REST. Acabaras sabent quin model triar per defecte al BernatLab.

## Requisits

- Maquina Linux, macOS o Windows amb acces a terminal
- Connexio a Internet
- 40-55 minuts
- Si es a la RPi: tenir 4 GB de RAM minim

## Pas 1: Instal·la Ollama (5 min)

A Linux:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

A macOS, pots fer-ho amb Homebrew:

```bash
brew install ollama
```

Verifica la versio:

```bash
ollama --version
# Hauria de mostrar 0.3.x o superior
```

## Pas 2: Comprova el servei (3 min)

Si estas a Linux amb systemd:

```bash
systemctl status ollama
# Hauria d'estar "active (running)"
```

Si vols iniciar-lo manualment:

```bash
ollama serve
```

A macOS, l'app s'inicia com a servei en segon pla quan la executes per primera vegada.

## Pas 3: Descarrega el teu primer model (5 min)

```bash
ollama pull llama3.2:1b
```

Aixo descarrega uns 1.3 GB. Si tens la RPi 4 amb 4 GB de RAM, aquest model es perfecte per començar.

Mira quins models tens descarregats:

```bash
ollama list
```

## Pas 4: Xateja per terminal (5 min)

```bash
ollama run llama3.2:1b
```

Un cop dins, escriu:

```
Explica'm en dues linies que es un LLM.
```

Despres:

```
Quin es el mejor [millor] servidor web per a homelab?
```

Per sortir:

```
/bye
```

## Pas 5: Cridar l'API REST (10 min)

L'API d'Ollama es la part que farem servir des dels scripts. Primer, comprova que escolta al port 11434:

```bash
curl http://localhost:11434/
# Hauria de retornar: "Ollama is running"
```

Ara la crida mes basica, generar text:

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2:1b",
  "prompt": "Explica que es Docker en una sola frase.",
  "stream": false
}'
```

Que torna? Un JSON amb `response` (el text generat) i metadades (`total_duration`, etc.).

## Pas 6: Crida desde Python (10 min)

Crea un fitxer `primer_script.py`:

```python
import requests

def preguntar(model, pregunta):
    r = requests.post(
        'http://localhost:11434/api/generate',
        json={
            'model': model,
            'prompt': pregunta,
            'stream': False
        }
    )
    return r.json()['response']

# Fem la primera pregunta
print(preguntar('llama3.2:1b', 'Que es una Raspberry Pi?'))
```

Si no tens `requests`:

```bash
pip install requests
```

Executa:

```bash
python3 primer_script.py
```

## Pas 7: Compara models (10 min)

Descarrega un model mes potent i compara:

```bash
ollama pull llama3.2:3b
```

Ara modifica el script per comparar temps i qualitat:

```python
import requests
import time

pregunta = "Escriu un paràgraf de 50 paraules sobre l'horticultura ecológica a Osona."

for model in ['llama3.2:1b', 'llama3.2:3b']:
    inici = time.time()
    r = requests.post(
        'http://localhost:11434/api/generate',
        json={'model': model, 'prompt': pregunta, 'stream': False}
    )
    durada = time.time() - inici
    text = r.json()['response']
    print(f"\n{'='*60}")
    print(f"Model: {model}")
    print(f"Durada: {durada:.2f}s")
    print(f"Resposta: {text}")
```

Que observes? Quin es mes rapid? Quin dona millor resposta?

## Pas 8: Neteja (5 min)

Si tens pocs espai:

```bash
# Mira quant ocupen els models
du -sh /usr/share/ollama/.ollama/models/*

# Esborra un model concret
ollama rm llama3.2:1b

# Llista els que queden
ollama list
```

## Validacio

Has acabat si:

- [ ] Has instal·lat Ollama correctament.
- [ ] Has descarregat almenys un model.
- [ ] Has xatejat per terminal.
- [ ] Has fet una crida a l'API REST amb curl.
- [ ] Has fet una crida desde Python.
- [ ] Has comparat dos models diferents.
- [ ] Has entès la diferencia de rendiment.

## Per aprofundir

- Prova `ollama run codellama` per generar codi Python.
- Investiga com canviar el directori de models amb `OLLAMA_MODELS`.
- Prova d'iniciar Ollama amb un altre port: `OLLAMA_HOST=0.0.0.0:8080 ollama serve`.
- Investiga el parametre `num_gpu` per descarregar part del model a la GPU.

## Ves un pas mes enlla

**Repte avançat**: Munta un petit script Python que actui com a assistent del BernatLab. Hauria de:
1. Carregar una llista de tasques possibles (revisar logs, generar script, explicar concepte).
2. Detectar quina tasca vols segons el prompt.
3. Cridar Ollama amb un system prompt adequat per a la tasca.
4. Retornar la resposta.

Aixo es el primer pas per construir un agent mes elaborat (capitols seguents).
