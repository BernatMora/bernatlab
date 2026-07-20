# Solucio: "Conflict: terminated by other getUpdates"

L'error NO es de Ollama. Es que hi ha DUES instancies del bot de Telegram
correguent alhora i Telegram nomes permet UNA.

Aixo passa quan:
- El servei systemd esta actiu + un altre proces manual
- El servei sha reiniciat rapid i l'anterior no ha alliberat la connexio
- Hi ha una altre maquina amb el mateix token del bot

## Solucio (executar a la RPi)

### 1. Mata TOTS els processos del bot

```bash
# Mata tots els processos de telegram_bot.py
pkill -9 -f telegram_bot.py

# Espera 5 segons
sleep 5

# Comprova que no queda cap
ps aux | grep telegram_bot
# Hauries de veure nomes el grep, no cap python
```

### 2. Espera 30 segons (important!)

```bash
echo "Esperant 30 segons perque Telegram alliberi la connexio..."
sleep 30
```

Aixo es perque Telegram triga una mica a marcar la connexio com a tancada.

### 3. Comprova que no hi ha cap altre proces

```bash
ps aux | grep telegram | grep -v grep
```

Si no surt res, perfecte. Si surt algun proces, mata'l.

### 4. Reinicia el servei

```bash
sudo systemctl restart hort-osona-telegram
```

### 5. Comprova que funciona

```bash
sudo systemctl status hort-osona-telegram
```

Ha de dir "active (running)" sense errors nous.

Mira tambe el log:
```bash
tail -30 /home/bernat/hort-osona/hort-osona-iot/logs/telegram_bot.log
```

Si tot ha anat be, ja no veuras l'error de "Conflict".

### 6. Prova el bot des del mobil

Obre Telegram, busca el teu bot, envia-li un missatge com "hola" o "/start".
Si respon, perfecte.

## Si l'error persisteix

Pot ser que hi hagi un segon bot amb el mateix token en una altra maquina.
Comprova:

```bash
# A la RPi
ps aux | grep -i telegram
# Des del teu PC
Get-Process | Where-Object {\$_.CommandLine -like "*telegram*"}
# O tambe pots buscar a la xarxa amb Tailscale
tailscale status
```

Si veus un altre bot en una altre maquina, cal matar-lo o canviar el token
(amb @BotFather a Telegram).

## Sobre Ollama

Quan el bot estigui funcionant correctament, ja podra parlar amb Ollama.
L'error que veus al log es nomes de Telegram, no pas d'Ollama.
El bot ni tan sols arriba a provar de conectar a Ollama perque Telegram
el para abans.
