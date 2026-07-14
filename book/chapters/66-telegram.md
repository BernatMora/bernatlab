# Capítol 66 — Bot de Telegram: alertes al mòbil

> *"Rebre una alerta al mòbil quan passa alguna cosa a l'hort, en temps real, és el salt entre un sistema que recull dades i un sistema que et cuida."*

## 66.1 Què aprendràs

- Com crear un bot de Telegram.
- Com obtenir el chat_id.
- Com enviar missatges des de la RPi.
- Com configurar alertes automàtiques des de Node-RED.
- Com combinar-ho amb Uptime Kuma.
- Bones pràctiques per a bots de Telegram.

## 66.2 Durada estimada

30-45 minuts.

## 66.3 Per què Telegram

Telegram és ideal per a alertes perquè:

- **Gratuït** per a bots.
- **API oberta** i ben documentada.
- **Grups** amb múltiples membres (perfecte per compartir l'estat amb família).
- **Markdown** i **HTML** als missatges.
- **Sense límit** pràctic de missatges.
- **Multiplataforma**: iOS, Android, web, desktop.

Alternatives:

- **Signal**: més segur però l'API per a bots és menys popular.
- **Discord**: similar però pensat per a comunitats.
- **Pushover, Pushbullet, Ntfy**: serveis específics per a notificacions.
- **SMS**: car i no xifrat.

Telegram és la millor elecció per a un homelab personal.

## 66.4 Crear el bot

Al teu mòbil o web de Telegram:

1. Cerca **@BotFather**.
2. Inicia conversa.
3. Envia `/newbot`.
4. Tria un nom (per exemple, "BernatLab Bot").
5. Tria un username (ha d'acabar en `bot`, per exemple, "bernatlab_alerts_bot").
6. Rebràs un **token**. Guarda'l al gestor de contrasenyes.

Exemple de token: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz123456`.

## 66.5 Crear el grup

1. Crea un grup a Telegram anomenat "BernatLab" (o com vulguis).
2. Afegeix el bot al grup.
3. Per obtenir el **chat_id** del grup:
   - Com a admin, obre `https://api.telegram.org/bot<TOKEN>/getUpdates`.
   - Cerca el `chat.id` del grup (un número negatiu, ex: `-1001234567890`).
   - Guarda'l al gestor.

## 66.6 El primer missatge des de la RPi

Des de la Raspberry, prova:

```bash
curl -X POST "https://api.telegram.org/bot<TOKEN>/sendMessage" \
    -d "chat_id=<CHAT_ID>" \
    -d "text=Hola des del BernatLab!"
```

Si tot va bé, rebràs el missatge al grup.

## 66.7 Com automatitzar des de la RPi

Crea un petit script Python que envia missatges:

Crea `~/homelab/scripts/telegram-notify.py`:

```python
#!/usr/bin/env python3
"""Envia un missatge a Telegram."""
import os
import sys
import requests

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

if not TOKEN or not CHAT_ID:
    print("Falten TELEGRAM_TOKEN o TELEGRAM_CHAT_ID", file=sys.stderr)
    sys.exit(1)

if len(sys.argv) < 2:
    print("Ús: telegram-notify.py <missatge>", file=sys.stderr)
    sys.exit(1)

text = " ".join(sys.argv[1:])

r = requests.post(
    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
    json={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"},
    timeout=10,
)
r.raise_for_status()
print("Enviat.")
```

Crea `~/homelab/secrets/telegram.env`:

```
TELEGRAM_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=-1001234567890
```

Fes-lo executable:

```bash
chmod +x ~/homelab/scripts/telegram-notify.py
```

Prova'l:

```bash
source ~/homelab/secrets/telegram.env
~/homelab/scripts/telegram-notify.py "Prova de Telegram"
```

## 66.8 Integrar amb Uptime Kuma

Recordes el **Cap 62**? Uptime Kuma ja permet enviar alertes per Telegram. Si ho vas configurar, ja ho tens.

Si no, ara és el moment. A Uptime Kuma:

1. Settings → Notifications → Telegram.
2. Activa.
3. Posa el bot token.
4. Posa el chat_id.
5. Fes clic a "Test".
6. Aplica a tots els monitors que vulguis.

## 66.9 Integrar amb Node-RED

A Node-RED, podem afegir un node de Telegram:

1. **Manage palette** → Install → busca `node-red-contrib-telegrambot`.
2. Després d'instal·lar, tindràs nodes `telegram bot`, `telegram sender`, `telegram receiver`, `telegram command`, `telegram event`.
3. Configura el bot:
   - **Bot username**: el que vas triar.
   - **Bot token**: el token.
4. Usa el node `telegram sender` per enviar missatges.

Exemple: una automatització que envia una alerta quan la temperatura baixa de 5°C.

1. Node `mqtt in` a `sensors/hort1/temperatura`.
2. Node `function` que filtra temperatures baixes.
3. Node `telegram sender` configurat amb el bot.
4. Connecta'ls.

Deploy. Prova publicant una temperatura baixa a MQTT. Rebràs un missatge al grup de Telegram.

## 66.10 Com enviar missatges amb format

Telegram accepta HTML i Markdown. Pots fer missatges bonics:

```python
text = """
<b>⚠️ Alerta BernatLab</b>

<b>Node:</b> hort1
<b>Sensor:</b> temperatura
<b>Valor:</b> 2.3°C
<b>Llindar:</b> 5°C
<b>Missatge:</b> Risc de gelada!
"""
```

Per usar HTML, posa `parse_mode=HTML` a la crida a l'API.

Per Markdown, `parse_mode=MarkdownV2`.

## 66.11 Comandes del bot

Pots fer que el bot respongui a comandes. Per exemple, `/status` retorna l'estat dels serveis.

A Node-RED, amb el node `telegram command`:

1. Configura `/status` com a command.
2. Connecta'l a un node `function` que construeixi el missatge.
3. Connecta'l a un node `telegram sender`.

Ara quan algú escrigui `/status` al grup, rebrà l'estat actual.

## 66.12 Bones pràctiques

1. **Un sol grup per a tot**. No creïs 10 grups.
2. **No saturis**. Limita les alertes a les importants.
3. **Usa emojis** per identificar ràpidament la severitat: 🔴 critical, ⚠️ warning, ℹ️ info.
4. **Inclou l'acció a prendre**. No només "s'ha trencat X", sinó "s'ha trencat X, fer Y per arreglar-ho".
5. **Limita el volum**. Si reps 100 missatges al dia, ja no els llegeixes.
6. **No comparteixis el token**. És com una contrasenya.

## 66.13 Què ve després

Ja tens alertes al mòbil. Al **Cap 67** afegirem **Prometheus + Alertmanager** per a monitoratge avançat, i al **Cap 68** aprendrem a fer **runbooks** per als incidents.

## 66.14 Errors habituals

**Error 1: el bot no envia res**.

Comprova el token i el chat_id. Mira els logs de Node-RED o del script Python.

**Error 2: el bot és al grup però no rep missatges**.

Això passa si el grup té "anti-spam" molt estricte. Assegura't que el bot té permís per llegir i enviar.

**Error 3: el missatge s'envia però no el reps**.

Comprova que tens notificacions actives per a aquest grup al teu mòbil.

**Error 4: format HTML invàlid**.

Si el missatge té un `<` sense tancar, Telegram el rebutja. Escapa caràcters especials.

## 66.15 Resum

Telegram és la manera més còmoda de rebre alertes del BernatLab. Hem vist:

- Crear el bot.
- Configurar el grup.
- Enviar missatges des de la RPi.
- Integrar amb Uptime Kuma.
- Integrar amb Node-RED.
- Comandes interactives.

## 66.16 Exercicis pràctics

1. Crea el bot de Telegram.
2. Crea el grup i afegeix-hi el bot.
3. Envia un missatge des de la RPi amb `curl`.
4. Configura Uptime Kuma per enviar alertes al grup.
5. Configura Node-RED per enviar alertes quan la temperatura baixa de 5°C.
6. Afegeix una comanda `/status` al bot.
7. Documenta la configuració al `homelab/setup-log.md`.
