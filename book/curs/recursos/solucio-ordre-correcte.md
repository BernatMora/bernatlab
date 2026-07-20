# Solucio correcta: primer aturar el servei, despres matar el proces

El proces es RELLANCA perque el servei systemd te `Restart=always`.
Cada vegada que el matem, el servei el torna a crear als 10 segons.
Es per això que veus un PID nou cada vegada (171620 -> 172704).

## L'ordre correcte

### 1. ATURA el servei systemd (ja no rellancara res)

```bash
sudo systemctl stop hort-osona-telegram
```

Aixo desactiva el servei. Despres el `Restart=always` ja no actua.

### 2. Espera 5 segons

```bash
sleep 5
```

### 3. Comprova que el servei esta parat

```bash
sudo systemctl status hort-osona-telegram
```

Ha de dir "inactive (dead)".

### 4. Ara sí, mata TOTS els procesos del bot

```bash
pkill -9 -f telegram_bot.py
sleep 3

# Comprova que no queda res
ps aux | grep telegram_bot | grep -v grep
# No ha de sortir res
```

Si encara hi ha un proces:

```bash
sudo kill -9 172704
sleep 3
ps aux | grep telegram_bot | grep -v grep
```

(o el PID que surti)

### 5. Espera 30 segons (IMPORTANT!)

```bash
echo "Esperant 30 segons perque Telegram alliberi la connexio..."
sleep 30
```

Aixo es CRUCIAL. Telegram triga a marcar la connexio com a tancada.
Si no esperes, quan tornis a iniciar el bot, Telegram el rebotara.

### 6. Comprova que tot esta net

```bash
ps aux | grep telegram | grep -v grep
sudo systemctl status hort-osona-telegram
```

Tots dos haurien destar "buits" o "inactive".

### 7. Engega el servei de nou

```bash
sudo systemctl start hort-osona-telegram
sleep 5
```

### 8. Comprova que funciona

```bash
sudo systemctl status hort-osona-telegram
tail -30 /home/bernat/hort-osona/hort-osona-iot/logs/telegram_bot.log
```

Ha de dir "active (running)" sense errors de Conflict.

### 9. Prova el bot des del mobil

Obre Telegram, busca el teu bot, envia-li un missatge.

---

## Si encara hi ha conflictes

Si despres de tot això encara surt l'error de Conflict, pot ser que hi hagi
UNA ALTRA MAQUINA amb el mateix token del bot.

Comprova:
```bash
tailscale status
```

Mira si tens altres maquines a la xarxa Tailscale. Si una daquestes tambe te
el bot, cal canviar el token o parar-lo a la maquina que no sha dusar.

