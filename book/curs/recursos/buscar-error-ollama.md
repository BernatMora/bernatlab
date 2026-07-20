# Buscar l'error real d'Ollama

Ara veig que el bot de Telegram FUNCIONA (accepta missatges, envia respostes).
Per tant, l'error d'Ollama ha d'estar al log pero pot ser:

1. Nivell INFO no mostra errors de Ollama
2. L'error sha produit pero no sha desat al log
3. L'error sha produit en una execucio anterior (potser amb un altre model)

## Comprovacio 1: Buscar errors al log

```bash
# Errors especifics d'Ollama
grep -i "ollama\|error\|exception\|traceback" /home/bernat/hort-osona/hort-osona-iot/logs/telegram_bot.log | tail -30

# O tots els warnings
grep -i "warn" /home/bernat/hort-osona/hort-osona-iot/logs/telegram_bot.log | tail -30
```

## Comprovacio 2: Augmentar el nivell de log

Edita el .env i canvia el nivell:

```bash
# Canvia aquesta linia
LOG_LEVEL=INFO

# Per aquesta altra
LOG_LEVEL=DEBUG
```

Despres reinicia el servei:

```bash
sudo systemctl restart hort-osona-telegram
```

I envia un missatge al bot. Despres mira el log:

```bash
tail -100 /home/bernat/hort-osona/hort-osona-iot/logs/telegram_bot.log
```

## Comprovacio 3: Prova directa a Ollama amb el model

El log mostra que tens 2 models:
- gemma3:1b (~815 MB)
- phi3:mini (~2.1 GB)

El .env posa OLLAMA_MODEL=gemma3:1b.

Prova aquest model directament:

```bash
curl -s http://localhost:11434/api/generate -d '{
  "model": "gemma3:1b",
  "prompt": "Hola",
  "stream": false
}' | head -50
```

Si retorna JSON amb "response", el model funciona.

## Comprovacio 4: Mira el codi del bot

Aquestes linies del .env son importants:
- OLLAMA_HOST=http://localhost:11434
- OLLAMA_MODEL=gemma3:1b
- RPI_API_URL=http://hortpi.local:8000  <-- aquesta URL potser no existeix

Per veure com el bot utilitza aquestes variables:

```bash
grep -n "OLLAMA\|ollama" /home/bernat/hort-osona/hort-osona-iot/telegram_bot.py | head -20
grep -n "RPI_API" /home/bernat/hort-osona/hort-osona-iot/telegram_bot.py | head -10
```

## Comprovacio 5: Prova un test

Al .env tens la variable RPI_API_URL=http://hortpi.local:8000.
Aixo vol dir que el bot tambe intenta conectar a la RPi per a sensors.
Si hortpi.local no existeix, tambe podria donar error.

Comprova:
```bash
# Existeix hortpi.local?
ping -c 2 hortpi.local

# Si no, cal canviar la URL o desactivar aquesta part
```

## Solucio rapida: si el model es massa petit

gemma3:1b te nomes 1B parametres. Es MOLT petit i pot tenir limitacions.
Prova amb phi3:mini que es mes potent:

```bash
# Canvia al .env
nano /home/bernat/hort-osona/hort-osona-iot/.env
# Substitueix OLLAMA_MODEL=gemma3:1b per OLLAMA_MODEL=phi3:mini
# Despres Ctrl+O, Enter, Ctrl+X

# Reinicia
sudo systemctl restart hort-osona-telegram
```

Pero abans de tot, **comparteix l'error exacte** que veus.
Si no el veus al log, posa el log a DEBUG i torna-ho a provar.
