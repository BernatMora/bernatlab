# Exercici practic - Capitol 4: Prompt engineering

> 35-50 min · Real amb Ollama

## Objectiu
Practicar les tecniques de prompt engineering mes importants: especificitat, role prompting, few-shot, chain of thought, i control de la sortida. Acabaras sabent com obtenir respostes mes utils del teu LLM local.

## Requisits

- Ollama instal·lat amb un model de 3B o mes
- Python amb `requests`
- 35-50 minuts

## Pas 1: Prepara l'entorn (3 min)

```bash
mkdir -p ~/bernatlab-exercicis/M4/04-prompts
cd ~/bernatlab-exercicis/M4/04-prompts
```

Crea `prompts.py` amb les funcions base:

```python
import requests

def preguntar(prompt, model='llama3.2:3b', system=None, temperature=0.7):
    messages = []
    if system:
        messages.append({'role': 'system', 'content': system})
    messages.append({'role': 'user', 'content': prompt})
    
    r = requests.post(
        'http://localhost:11434/api/chat',
        json={
            'model': model,
            'messages': messages,
            'stream': False,
            'options': {'temperature': temperature}
        }
    )
    return r.json()['message']['content']
```

## Pas 2: Compara un mal prompt amb un bon prompt (10 min)

Crea `comparar_prompts.py`:

```python
from prompts import preguntar

# MAL prompt
print("=== MAL PROMPT ===")
print(preguntar("Explica Docker."))

print("\n" + "="*60 + "\n")

# BON prompt
print("=== BON PROMPT ===")
print(preguntar(
    "Explica quines son les 3 diferencies principals entre Docker i una maquina virtual tradicional, "
    "adreçat a un administrador de sistemes amb 5 anys d'experiencia. Limita la resposta a 150 paraules. "
    "Escriu en catala."
))
```

Executa i observa la diferencia. El bon prompt ha de donar una resposta mes enfocada, mes especifica i mes util.

## Pas 3: Experimenta amb role prompting (8 min)

Crea `role_prompting.py`:

```python
from prompts import preguntar

pregunta = "Tinc errors intermitents amb el contenidor de Mosquitto. Que puc fer?"

# Sense rol
print("=== SENSE ROL ===")
print(preguntar(pregunta))

# Amb rol d'expert
print("\n=== AMB ROL EXPERT ===")
print(preguntar(
    pregunta,
    system="Ets un administrador de sistemes Linux senior amb 15 anys d'experiencia en homelabs. "
           "Especialista en MQTT, Docker i Raspberry Pi. Respon sempre en catala, amb exemples de comandes."
))

# Amb rol d'amic
print("\n=== AMB ROL D'AMIC ===")
print(preguntar(
    pregunta,
    system="Ets un company de feina simpatic que intenta ajudar. "
           "Parla en catala informal, sense tecnicismes excessius."
))
```

Que diferencies hi ha entre les tres respostes?

## Pas 4: Few-shot prompting (10 min)

Crea `few_shot.py`:

```python
from prompts import preguntar

# Zero-shot
print("=== ZERO-SHOT (classifica l'alerta) ===")
print(preguntar("Classifica aquesta alerta: 'CPU usage 95%'"))

# Few-shot
print("\n=== FEW-SHOT ===")
prompt_few_shot = """Classifica les alertes en INFO, WARNING o CRITICAL.

Exemples:
- 'Disk usage 60%' -> INFO
- 'Disk usage 85%' -> WARNING
- 'Disk usage 98%' -> CRITICAL
- 'Memory usage 45%' -> INFO
- 'Memory usage 80%' -> WARNING
- 'Service nginx down' -> CRITICAL

Classifica: 'CPU usage 95%'"""
print(preguntar(prompt_few_shot))
```

Que ha passat? El few-shot hauria de donar "CRITICAL" (CPU 95% es critic), pero el zero-shot potser ha donat una explicacio llarga i menys directa.

## Pas 5: Chain of thought (10 min)

Crea `chain_of_thought.py`:

```python
from prompts import preguntar

# Problema logic
problema = """Tinc 3 testos. Al primer hi ha 7 tomàquets. Al segon, el doble que al primer. 
Al tercer, la meitat que al segon. Si un ocell menja 2 tomàquets del segon test, 
quants tomàquets tinç en total?"""

# Sense chain of thought
print("=== SENSE CHAIN OF THOUGHT ===")
print(preguntar(problema))

# Amb chain of thought
print("\n=== AMB CHAIN OF THOUGHT ===")
print(preguntar(
    f"{problema}\n\nPensa pas a pas, mostrant cada calcul intermedi. "
    "Despres dona la resposta final."
))
```

El "amb chain of thought" hauria de mostrar: 7 + 14 + 7 = 28, menys 2 = 26 tomàquets. El "sense" pot donar una resposta rapida pero erronia.

## Pas 6: Control del format de sortida (8 min)

Crea `format_sortida.py`:

```python
from prompts import preguntar
import json

# Sortida en JSON estructurat
prompt_json = """Llista 3 avantatges i 3 inconvenients d'usar Docker en un homelab.
Respon EXCLUSIVAMENT amb JSON valid en aquest format:
{
  "avantages": ["av1", "av2", "av3"],
  "inconvenients": ["inc1", "inc2", "inc3"]
}
Nomes el JSON, sense texte adicional."""

print("=== JSON ESTRUCTURAT ===")
resposta = preguntar(prompt_json, temperature=0)
print(resposta)

# Intentem parsejar-lo
try:
    data = json.loads(resposta)
    print("\n[OK] JSON valid!")
    print(json.dumps(data, indent=2, ensure_ascii=False))
except json.JSONDecodeError as e:
    print(f"\n[ERROR] JSON invalid: {e}")
```

## Pas 7: Experimenta amb temperature (5 min)

Crea `temperature_test.py`:

```python
from prompts import preguntar

prompt = "Escriu una frase curta sobre l'horticultura."

for temp in [0.0, 0.5, 1.0]:
    print(f"\n=== TEMPERATURE {temp} ===")
    for i in range(3):
        print(f"  {i+1}. {preguntar(prompt, temperature=temp)}")
```

Que observes? Temperature 0 hauria de donar respostes identiques. Temperature 1 hauria de ser molt variat.

## Validacio

Has acabat si:

- [ ] Has vist la diferencia entre mal i bon prompt.
- [ ] Has practicat role prompting amb 3 rols diferents.
- [ ] Has usat few-shot per classificar alertes.
- [ ] Has provat chain of thought amb un problema logic.
- [ ] Has aconseguit una sortida en JSON valid.
- [ ] Has experimentat amb temperature.

## Per aprofundir

- Investiga "self-consistency": demanar al model N respostes i quedar-te amb la mes comuna.
- Llegeix sobre "ReAct prompting": alternar raonament i accions.
- Prova "negative prompting": dir-li al model que NO faci certes coses.
- Mira com fan servir prompts les eines populars: Aider, Cursor, Continue.

## Ves un pas mes enlla

**Repte avançat**: Crea una llibreria Python `bernatlab_prompts.py` amb prompts reusables per a les tasques comuns del BernatLab:
- `resumir_log(log_text)`
- `classificar_alerta(alerta_text)`
- `generar_script(descripcio, llenguatge)`
- `explicar_error(error_text)`
- `respondre_pregunta_hort(pregunta)`

Cada funcio ha de tenir un system prompt optimitzat per a la tasca. Despres, construeix un script que les faci servir totes en un menu interactiu.
