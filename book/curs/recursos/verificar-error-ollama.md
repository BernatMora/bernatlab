# Comprovacio: veure l'error real d'Ollama

Ara que el bot esta corrent des de fa estona, l'error d'Ollama JA hauria
dapareixer al log. Cal veure'l.

## Pas 1: Mira el log sencer (no nomes 30 linies)

```bash
cat /home/bernat/hort-osona/hort-osona-iot/logs/telegram_bot.log
```

Copia TOT el que surti, pero sobretot:
- Linies amb "Error" o "ERROR"
- Linies amb "ollama" o "Ollama"
- Linies amb "Connection" o "connect"
- Qualsevol excepcio (Traceback)

## Pas 2: Si el log es massa llarg, busca l'error

```bash
# Ultimes 100 linies
tail -100 /home/bernat/hort-osona/hort-osona-iot/logs/telegram_bot.log

# O les linies amb error
grep -i "error\|ollama\|connect\|fail" /home/bernat/hort-osona/hort-osona-iot/logs/telegram_bot.log | tail -30
```

## Pas 3: Verificar que el bot pot arribar a Ollama

```bash
# Des de la RPi
curl -s http://localhost:11434/api/tags
# Ha de tornar JSON amb els models

# Prova tambe amb 127.0.0.1
curl -s http://127.0.0.1:11434/api/tags
```

Si aixo funciona, el problema NO es de xarxa sino del codi del bot.

## Pas 4: On busca el bot a Ollama?

Aixo cal mirar-ho al codi o a la configuracio:

```bash
# Mira el fitxer .env
cat /home/bernat/hort-osona/hort-osona-iot/.env

# Cerca on sha configurat Ollama al codi
grep -rn "ollama\|OLLAMA" /home/bernat/hort-osona/hort-osona-iot/*.py
grep -rn "ollama\|OLLAMA" /home/bernat/hort-osona/hort-osona-iot/config/ 2>/dev/null
```

## Les causes mes probables

1. **URL incorrecta** al .env o al codi
   - Si posa `localhost:11434` hauria de funcionar
   - Si posa `ollama:11434` nomes funciona si es contenidor Docker
   - Si posa una altra cosa, cal canviar-la

2. **Ollama nomes escolta a localhost**
   - Comprova: `ss -tlnp | grep 11434`
   - Si nomes escolta a 127.0.0.1, OK per a bot local
   - Si volem acces extern, cal canviar OLLAMA_HOST

3. **No hi ha cap model descarregat**
   - Comprova: `curl http://localhost:11434/api/tags`
   - Si retorna llista buida, cal descarregar: `ollama pull llama3.2:3b`

4. **El codi del bot te un error de sintaxi o logica**
   - Mira la part que parla amb Ollama
   - Prova una crida directa a l'API

## Prova directa a Ollama

```bash
# Prova basic
curl -s http://localhost:11434/api/generate -d '{
  "model": "llama3.2:3b",
  "prompt": "Hola",
  "stream": false
}'
```

Si retorna text JSON, Ollama funciona perfectament.
Si dona error, l'error es da Ollama (no pas del bot).
