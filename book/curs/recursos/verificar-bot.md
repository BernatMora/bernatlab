# Comprovacio final del bot de Telegram

Tot sembla correcte:
- Servei actiu desde les 09:45:22
- Sense errors al log

## Comprovacio final: veure el log sencer

Per veure el log complet (no nomes 30 linies):

```bash
cat /home/bernat/hort-osona/hort-osona-iot/logs/telegram_bot.log
```

Aixo mostrara TOT el contingut del fitxer de log. Si encara hi ha errors de
"Conflict", els veuras aqui.

## Prova el bot des del mobil

1. Obre Telegram al mobil
2. Busca el teu bot (pel nom que li vas posar)
3. Envia-li un missatge qualsevol: "hola" o "/start"

Si respon, perfecte! Ja tens el bot funcionant.

## Si vols veure els logs en temps real

```bash
tail -f /home/bernat/hort-osona/hort-osona-iot/logs/telegram_bot.log
```

Aixo mostrara el log continuament. Ctrl+C per sortir.

## Comprovacio adicional: que el bot pot parlar amb Ollama

Des de la RPi:

```bash
# Comprova que Ollama segueix actiu
curl -s http://localhost:11434/

# Comprova que hi ha algun model
curl -s http://localhost:11434/api/tags
```

Si això retorna JSON amb models, Ollama funciona.

## Si el bot no respon

Mira el log:
```bash
tail -30 /home/bernat/hort-osona/hort-osona-iot/logs/telegram_bot.log
```

Si veus errors nous, enviam'els.
