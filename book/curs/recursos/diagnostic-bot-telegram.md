# Comprovacions per entendre el bot de Telegram

Ja hem trobat el bot:
- Es un servei systemd (`/etc/systemd/system/hort-osona-telegram.service`)
- El codi esta a `/home/bernat/hort-osona/hort-osona-iot/telegram_bot.py`
- El log esta a `/home/bernat/hort-osona/hort-osona-iot/logs/telegram_bot.log`

Ara cal veure 4 coses:

## 1. La configuracio del servei systemd

```bash
cat /etc/systemd/system/hort-osona-telegram.service
```

## 2. El log del bot (ERROR EXACTE)

```bash
tail -50 /home/bernat/hort-osona/hort-osona-iot/logs/telegram_bot.log
```

## 3. La part del codi que parla amb Ollama

```bash
grep -n -A 3 -B 1 "ollama" /home/bernat/hort-osona/hort-osona-iot/telegram_bot.py
```

Aixo buscara totes les linies que contenen "ollama" amb 3 linies de context.

## 4. Verificar que el servei esta actiu

```bash
sudo systemctl status hort-osona-telegram
```

---

Quan tingui aquestes 4 sortides sabrem:
- Si el servei esta actiu
- L'error exacte al log
- A quina URL intenta conectar Ollama
- Si el problema es de xarxa, URL, o una altre cosa
