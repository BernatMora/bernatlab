# Solucio reforçada: matar el proces del bot

Veig que el `pkill -9 -f telegram_bot.py` NO ha funcionat.
Aixo pasa perque el filtre no es prou ampli o el proces esta protegit.

## Prova 1: Matar per PID directament

```bash
# Mata el proces especific pel seu PID
sudo kill -9 171620

# Espera 3 segons
sleep 3

# Comprova
ps aux | grep telegram_bot | grep -v grep
```

Si no funciona:

## Prova 2: Matar amb sudo

```bash
# A vegades cal sudo
sudo kill -9 171620
sleep 3
ps aux | grep telegram_bot | grep -v grep
```

Si encara no funciona:

## Prova 3: Matar tots els python del usuari bernat

```bash
# Compte: nomes fes-ho si tens clar que nomes corre el bot
pkill -9 -u bernat python
sleep 3
ps aux | grep python | grep -v grep
```

## Prova 4: Usar el nom complet del proces

```bash
pkill -9 -f "hort-osona-iot/telegram_bot.py"
sleep 3
ps aux | grep -i "telegram_bot" | grep -v grep
```

## Quan NO quedi cap proces

```bash
# Confirma que no hi ha res
ps aux | grep -i telegram | grep -v grep
# Ha de quedar buit

# Espera 30 segons
echo "Esperant 30 segons..."
sleep 30

# Ara reinicia el servei
sudo systemctl restart hort-osona-telegram
sleep 5

# Comprova
sudo systemctl status hort-osona-telegram

# Mira el log
tail -20 /home/bernat/hort-osona/hort-osona-iot/logs/telegram_bot.log
```

## Si res funciona

L'ultima opcio es reiniciar la RPi:

```bash
sudo reboot
```

Aixo matara TOTS els processos. Pero espera 2-3 minuts
perque la RPi torni a estar disponible per Tailscale.
