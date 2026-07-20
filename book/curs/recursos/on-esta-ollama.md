# Trobar on esta el codi que parla amb Ollama

Si `telegram_bot.py` no te "ollama", pero el missatge dexistir "no es pot
connectar amb Ollama" ve doncs es que **un altre fitxer** conte el codi
que parla amb Ollama.

## 1. Buscar el text exacte a TOTS els fitxers

```bash
grep -rn "ollama\|Ollama\|OLLAMA" /home/bernat/hort-osona/hort-osona-iot/ --include="*.py" 2>/dev/null
```

Aixo buscara a TOTS els fitxers .py del projecte.

## 2. Buscar el missatge dexistir especific

El missatge que veus al mobil es:
"No es pot connectar amb Ollama. Assegura't que estigui actiu: ollama serve"

```bash
grep -rn "ollama serve\|no es pot connectar" /home/bernat/hort-osona/hort-osona-iot/ --include="*.py" 2>/dev/null
```

Aixo trobara el fitxer exacte on sha definit el missatge.

## 3. Segurament sera rag.py

El log ha mostrat que el bot te una variable `RAG script` que apunta a:
`/home/bernat/hort-osona/hort-osona-iot/rag.py`

Mirem aquest fitxer:

```bash
grep -n "ollama\|OLLAMA\|Ollama" /home/bernat/hort-osona/hort-osona-iot/rag.py | head -30
```

## 4. Provar directament rag.py

```bash
cd /home/bernat/hort-osona/hort-osona-iot
/home/bernat/hort-osona/hort-osona-iot/venv/bin/python rag.py --test 2>&1 | head -30
# O
/home/bernat/hort-osona/hort-osona-iot/venv/bin/python -c "
import sys
sys.path.insert(0, '/home/bernat/hort-osona/hort-osona-iot')
import rag
" 2>&1 | head -30
```

Aixo pot donar errors que mostren on esta el problema.
