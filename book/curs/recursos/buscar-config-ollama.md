# Diagnostic: el bot sha donat un missatge especific

L'error exacte que veus al mobil es:

    Error: No es pot connectar amb Ollama.
    Assegura't que estigui actiu: ollama serve

Aixo vol dir que el codi del bot te un try/except que quan falla la
connexio a Ollama envia aquest missatge.

Pero Ollama JA funciona (curl http://localhost:11434 retorna "Ollama is running").
Per tant el problema es que **el bot esta buscant Ollama a un lloc diferent**.

## Possibles causes

1. **OLLAMA_HOST al .env apunta a un altre lloc**
   - El .env diu: OLLAMA_HOST=http://localhost:11434
   - Si esta mal escrit (typo), el bot busca un altre IP

2. **El bot no carrega el .env correctament**
   - Si el bot no llegeix el .env, OLLAMA_HOST pot ser buit o tenir
     un valor per defecte diferent

3. **Ollama nomes escolta a una IP especifica**
   - Si OLLAMA_HOST nomes escolta a 127.0.0.1, OK per a localhost
   - Pero si el bot esta en un altre contexte (chroot, container, etc.)
     pot no veure 127.0.0.1

4. **El model no existeix o no sha carregat**
   - OLLAMA_MODEL=gemma3:1b (aixo shauria de funcionar)

## Comprovacions

### 1. Comprova que el bot pot arribar a Ollama

Des de la RPi (no des del bot), fes una prova amb el model:

```bash
curl -s http://localhost:11434/api/generate -d '{
  "model": "gemma3:1b",
  "prompt": "Hola",
  "stream": false
}' | head -50
```

Si retorna JSON amb "response", Ollama funciona.

### 2. Comprova com el codi carrega les variables

Aquesta es la part mes important. Mira el codi:

```bash
grep -n -B 2 -A 5 "OLLAMA_HOST\|ollama" /home/bernat/hort-osona/hort-osona-iot/telegram_bot.py | head -50
```

Volem veure:
- On llegeix OLLAMA_HOST (amb os.getenv? amb dotenv?)
- A quina URL intenta conectar
- Si te un try/except que captura l'error

### 3. Comprova el modul dotenv

```bash
# Comprova que el modul python-dotenv esta instal·lat
/home/bernat/hort-osona/hort-osona-iot/venv/bin/pip list | grep -i dotenv
```

Si no esta, el .env no es carrega.

### 4. Comprova que python pot llegir el .env

Crea un test rapid:

```bash
cd /home/bernat/hort-osona/hort-osona-iot
/home/bernat/hort-osona/hort-osona-iot/venv/bin/python -c "
import os
from dotenv import load_dotenv
load_dotenv()
print('OLLAMA_HOST:', os.getenv('OLLAMA_HOST'))
print('OLLAMA_MODEL:', os.getenv('OLLAMA_MODEL'))
print('TELEGRAM_BOT_TOKEN:', 'OK' if os.getenv('TELEGRAM_BOT_TOKEN') else 'BUIT')
"
```

Si OLLAMA_HOST surt buit o diferent de http://localhost:11434, tens el problema.

## Solucio temporal: llançar Ollama explicitament

Si vols intentar una cosa directa:

```bash
# Comprova que Ollama esta realment escoltant
ss -tlnp | grep 11434

# Hauria de sortir:
# LISTEN  0  4096  0.0.0.0:11434  ...
# o
# LISTEN  0  4096  127.0.0.1:11434  ...

# Si nomes escolta a 127.0.0.1 (localhost), esta be per a connexions locals
# Si volem que escolti a 0.0.0.0 (totes les IPs):
sudo systemctl edit ollama
# Afegeix:
# [Service]
# Environment="OLLAMA_HOST=0.0.0.0:11434"
# Ctrl+O, Enter, Ctrl+X
sudo systemctl daemon-reload
sudo systemctl restart ollama
```

## El mes probable

El problema es al **.env** o al **carregament de variables**. Comparteix la sortida
de les 4 comprovacions i sabrem exactament on esta el problema.
