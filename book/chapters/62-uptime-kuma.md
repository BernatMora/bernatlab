# Capítol 62 — Uptime Kuma: el primer monitor

> *"Si no saps si el teu servidor està viu o mort, no el pots arreglar. El monitoratge és la base de tot."*

## 62.1 Què aprendràs

- Què és Uptime Kuma.
- Com instal·lar-lo amb Docker Compose.
- Com configurar els teus primers monitors.
- Com rebre alertes per Telegram i correu.
- Com monitorar la pròpia Raspberry.

## 62.2 Durada estimada

20-30 minuts.

## 62.3 Què és Uptime Kuma

**Uptime Kuma** és una eina de monitoratge self-hosted (l'allotges tu). Et permet:

- Fer ping a serveis (HTTP, TCP, ping ICMP, DNS, etc.).
- Veure l'estat en temps real.
- Rebre alertes quan alguna cosa falla.
- Veure gràfiques de latència i temps de resposta.
- Crear pàgines d'estat públiques.

Alternatives:

- **UptimeRobot** (cloud, gratuït fins a 50 monitors).
- **Healthchecks.io** (molt simple, basat en cron).
- **Prometheus + Alertmanager** (molt potent, però més complex — el veurem al cap 67).

Uptime Kuma és el **just mig**: potent però fàcil.

## 62.4 Instal·lació

Crea `~/homelab/compose/uptime-kuma.yml`:

```yaml
version: "3.8"

services:
  uptime-kuma:
    image: louislam/uptime-kuma:1
    container_name: uptime-kuma
    restart: unless-stopped
    ports:
      - "3001:3001"
    volumes:
      - ./data/uptime-kuma:/app/data
      - /var/run/docker.sock:/var/run/docker.sock:ro
```

Explicació:

- `louislam/uptime-kuma:1` és la imatge oficial. La tag `:1` segueix la darrera 1.x.
- Port 3001 (HTTP).
- Volum `./data/uptime-kuma` per persistir la configuració.
- `docker.sock` perquè Uptime Kuma pugui monitorar contenidors Docker directament.

Engega:

```bash
cd ~/homelab/compose
docker compose -f uptime-kuma.yml up -d
```

Obre `http://hortosona:3001` al navegador. La primera vegada et demanarà crear un compte d'administrador.

## 62.5 Configuració inicial

Un cop dins:

1. Crea el compte d'admin.
2. Tria el tema (clar o fosc).
3. Activa 2FA des de "Settings" → "General" → "2FA".

## 62.6 Crear el primer monitor

A la pantalla principal, fes clic a **"Add New Monitor"**.

Monitorem el **Portainer**:

- **Monitor Type**: HTTPS
- **Friendly Name**: Portainer
- **URL**: `https://localhost:9443`
- **Monitoring Interval**: 60 seconds
- **Retry**: 1
- **Request Timeout**: 10 seconds
- **Accepted Status Codes**: 200-299

Fes clic a **"Save"**. Ara Portainer apareix a la llista amb un punt verd (UP).

## 62.7 Què monitorar

Afegeix aquests monitors bàsics:

| Nom | Tipus | URL/Target |
|---|---|---|
| Portainer | HTTPS | https://localhost:9443 |
| Uptime Kuma | HTTP | http://localhost:3001 |
| Raspberry Pi (ping) | Ping | localhost |
| Grafana (futur) | HTTP | http://localhost:3000 |
| Mosquitto (futur) | TCP | localhost:1883 |
| InfluxDB (futur) | HTTP | http://localhost:8086 |

Per al ping, has de triar "Ping" com a tipus i posar `localhost` com a target.

## 62.8 Configurar alertes per Telegram

Això és el que realment val la pena: rebre alertes al mòbil quan alguna cosa falla.

Primer, necessites un **bot de Telegram** (si no el tens):

1. Obre Telegram, parla amb `@BotFather`.
2. Envia `/newbot`.
3. Segueix les instruccions. Et donarà un **token** (una cadena llarga tipus `1234567890:ABCdef...`).
4. Crea un grup amb tu i el bot.
5. Per obtenir el **chat_id**, obre `https://api.telegram.org/bot<TOKEN>/getUpdates` al navegador. Busca el `chat.id` del grup.

A Uptime Kuma:

1. Vés a **Settings** → **Notifications** → **Telegram**.
2. Activa.
3. Posa el **bot token** i el **chat ID**.
4. Fes clic a **"Test"**. Si tot va bé, rebràs un missatge al grup de Telegram.

Torna a **"Add New Monitor"** i configura les notificacions per aquest monitor (a la secció "Notifications" del formulari).

## 62.9 Configurar alertes per correu

Si vols rebre correus:

1. Settings → Notifications → Email (SMTP).
2. Configura el teu servidor SMTP. Si uses Gmail:
   - SMTP Host: `smtp.gmail.com`
   - Port: 587
   - Username: el teu correu.
   - Password: una **app password** de Google (no la teva contrasenya normal).
   - From i To: el teu correu.

Per obtenir una app password de Gmail:

1. Vés a https://myaccount.google.com/apppasswords.
2. Crea una nova "App password" per a "Mail / Uptime Kuma".
3. Google et donarà una contrasenya de 16 caràcters. Usa aquesta.

## 62.10 Monitorar la pròpia Raspberry

Volem saber si la RPi està viva. Per a això, monitora:

- **Ping** a localhost (o a la seva IP).
- **CPU** i **RAM** (no és directe a Uptime Kuma — cal un script).
- **Temperatura** (cal un script).

Per a CPU/RAM/temperatura, podem afegir un monitor HTTP que apunti a un petit servidor de mètriques. Però això ho farem al **Cap 67** (Prometheus). Per ara, el ping ja és bona cosa.

També podem monitorar **Uptime Kuma mateix** (un watchdog). Per fer-ho:

1. Crea un monitor de tipus HTTP a `http://localhost:3001`.
2. Si Uptime Kuma es cau, ell mateix no t'avisarà — però el monitor sí.

Això és estrany però útil: si Uptime Kuma es reinicia i funciona, rebràs una alerta de "Recovered".

## 62.11 Pàgina d'estat pública

Uptime Kuma permet crear una pàgina d'estat pública:

1. Settings → Status Page.
2. Crea una nova pàgina.
3. Afegeix els monitors que vols que siguin visibles.
4. Tria un nom (per exemple, "BernatLab Status").
5. Opcional: posa una contrasenya perquè només tu la puguis veure.

La pàgina estarà disponible a `http://hortosona:3001/status/bernatlab` o similar.

Això és útil si vols compartir amb algú l'estat del sistema sense donar accés a la consola d'admin.

## 62.12 Què fer quan arriba una alerta

Quan Uptime Kuma t'avisa per Telegram que un servei està caigut:

1. **No entris en pànic**. És normal que un servei caigui de tant en tant.
2. **Mira els logs**: a Portainer, selecciona el contenidor i mira els logs.
3. **Comprova si és transitori**: espera 5 minuts. Si torna sol, era un reinici de Docker o de la RPi.
4. **Si persisteix**: consulta el runbook pertinent (cap 68).
5. **Si no hi ha runbook**: consulta el cap 56 (diagnòstic).

## 62.13 Què ve després

Ja tens Docker, Portainer i Uptime Kuma. Al **Cap 63** muntarem la cadena de dades: **Mosquitto (MQTT)**, **InfluxDB** i **Grafana**. Això és el cor de l'hort.

## 62.14 Errors habituals

**Error 1: el contenidor no arrenca**.

Mira els logs:

```bash
docker logs uptime-kuma
```

Sovint és un conflicte de port o de volum.

**Error 2: Telegram no envia**.

Comprova que el token i el chat ID són correctes. Assegura't que el bot és membre del grup. Fes servir el botó "Test".

**Error 3: monitors falsos positius**.

Si la teva xarxa és inestable, rebràs alertes que no són reals. Augmenta l'interval de monitoratge o el "Retry" a 3 per evitar-ho.

**Error 4: pàgina d'estat inaccesible**.

Assegura't que el port 3001 és accessible. Si tens UFW, permet-ho per a la xarxa local.

## 62.15 Resum

Uptime Kuma és la teva primera línia de defensa: si un servei cau, t'avisa. Hem vist:

- Instal·lació amb Compose.
- Configuració de monitors.
- Alertes per Telegram i correu.
- Pàgina d'estat pública.

Al **Cap 63** muntarem la cadena de dades de l'hort.

## 62.16 Exercicis pràctics

1. Instal·la Uptime Kuma amb Compose.
2. Crea el compte d'admin i activa 2FA.
3. Crea 5 monitors (Portainer, Uptime Kuma, ping, i 2 més).
4. Configura alertes per Telegram.
5. Configura alertes per correu.
6. Crea una pàgina d'estat pública.
7. Documenta els monitors al `homelab/setup-log.md`.
