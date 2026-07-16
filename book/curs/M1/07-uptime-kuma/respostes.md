# Respostes — Capítol 7: Uptime Kuma

> Mira les respostes DESPRÉS d'haver fet el qüestionari.

## Pregunta 1: Què és Uptime Kuma?

**Resposta correcta**: Una eina self-hosted de monitoratge de serveis amb alertes.

**Explicació**: Uptime Kuma és una eina open-source que pots allotjar al teu servidor per vigilar serveis. Alternatives: UptimeRobot (cloud), Healthchecks.io, Statping, Monitoror. Kuma és la millor per a self-hosted per la seva simplicitat i potència.

## Pregunta 2: Port per defecte

**Resposta correcta**: 3001

**Explicació**: Uptime Kuma escolta al 3001 (HTTP) i 3002 (HTTPS). Al BernatLab exposem el 3001, accessible via Tailscale. Si vols HTTPS, caldria un reverse proxy (Traefik, Caddy, Nginx) — ho veurem en capítols posteriors.

## Pregunta 3: Monitor HTTP

**Resposta correcta**: HTTP(s)

**Explicació**: El tipus HTTP(s) comprova que una URL retorni un codi d'estat dins del rang acceptat (per defecte 200-299). És el tipus més usat perquè la majoria de serveis web exposen una URL.

## Pregunta 4: Canal d'alertes recomanat

**Resposta correcta**: Telegram

**Explicació**: Telegram és immediat (notificacions push al mòbil), gratuït, i fàcil d'automatitzar amb bots. SMS seria més fiable però de pagament. Email és menys immediat. Per a un homelab, Telegram és la millor opció.

## Pregunta 5: Primer pas per Telegram

**Resposta correcta**: Crear un bot amb @BotFather i obtenir el token.

**Explicació**: @BotFather és el bot oficial de Telegram per crear altres bots. Envia `/newbot` i segueix les instruccions. Et donarà un token que identifica el bot. Caldrà també el chat_id de l'usuari o grup que rebrà les alertes.

## Pregunta 6: Status Page

**Resposta correcta**: Una pàgina pública que mostra l'estat dels serveis monitorats.

**Explicació**: Les Status Pages serveixen per comunicar l'estat dels teus serveis a usuaris externs (família, amics, clients). Mostren ✅ UP, 🔴 DOWN, latència, uptime %. Al BernatLab, la pots compartir perquè la gent sàpiga si un servei concret és teu o és cosa seva.

## Pregunta 7: Freqüència recomanada

**Resposta correcta**: Entre 30 i 300 segons, segons la criticitat.

**Explicació**: 30s és molt sovint (pot generar molta càrrega si tens molts monitors). 300s (5 min) és poc sovint (podries trigar a saber d'una caiguda). 60-120s és el sweet spot. Serveis crítics: 30-60s. Serveis menys importants: 5 min.

## Pregunta 8: Avantatge del socket Docker

**Resposta correcta**: Permet monitors de tipus Docker Container que consulten l'estat dels contenidors.

**Explicació**: Muntant `/var/run/docker.sock`, Uptime Kuma pot parlar directament amb Docker i saber l'estat exacte de cada contenidor (running, exited, paused). Això és més fiable que fer un HTTP al port, perquè si el contenidor existeix però no respon, el socket ja et dóna info.

## Pregunta 9 (oberta): Quins serveis monitorar

**Resposta model**:

Al BernatLab actual, els serveis que monitoraria i el tipus de monitor serien:

**1. RPi hortosona (ping)**
- Tipus: **Ping** a `127.0.0.1`.
- Per què: si la RPi en si deixa de respondre, vols saber-ho. Un ping a localhost és un test bàsic de l'estat del sistema. Si falla, és un problema greu (kernel panico, OOM, fallada elèctrica).

**2. Portainer (HTTP 9000)**
- Tipus: **HTTP(s)** a `http://localhost:9000`.
- Per què: Portainer és el teu "quadre de comandaments". Si cau, no pots gestionar els altres serveis fàcilment. A més, si la interfície web respon, és bona senyal que Docker funciona.

**3. Whoami / servei web qualsevol (HTTP)**
- Tipus: **HTTP(s)** a `http://localhost:8080`.
- Per què: test genèric que el stack web (Nginx/qui sigui) funciona. Whoami retorna info de la petició, ideal per debug.

**4. SSH (TCP 22)**
- Tipus: **TCP port** a `127.0.0.1:22`.
- Per què: si SSH cau, et quedes fora de la RPi (a menys que tinguis Portainer o pantalla connectada). Vull saber immediatament si passa.

**5. DNS extern (HTTPS)**
- Tipus: **HTTP(s)** a `https://1.1.1.1`.
- Per què: test genèric de "tenim Internet?". Si falla, el problema és la xarxa, no els teus serveis. Ajudarà a discernir on és la fallada.

**6. Tailscale (HTTP)**
- Tipus: **HTTP(s)** a `http://100.115.134.76:9000` (Portainer via Tailscale).
- Per què: si l'accés remot via Tailscale falla, estàs aïllat. Un test periòdic et permet saber-ho.

**7. (Quan el tinguis) Homepage (HTTP 3010)**
- Tipus: **HTTP(s)** a `http://localhost:3010`.
- Per què: la porta d'entrada al BernatLab ha d'estar sempre viva.

**8. (Quan el tinguis) Cert SSL propi (HTTP)**
- Tipus: **HTTP(s)** a `https://elmeudomini.cat` + monitor de certificat.
- Per què: vols saber quan caduca el certificat SSL amb antelació.

La idea és cobrir tant els serveis individuals com la infraestructura subjacent (RPi, xarxa, Tailscale, Internet).

## Pregunta 10 (oberta): Alerta de Telegram quan Portainer cau

**Resposta model**:

Per configurar una alerta de Telegram que m'avisi quan Portainer cau:

**1. Preparar el bot a Telegram** (un sol cop):
- Al mòbil, obrir Telegram i buscar `@BotFather`.
- Enviar `/newbot`.
- Posar un nom amigable: `BernatLab Alerts`.
- Posar un username únic: `bernatlab_alerts_2026_bot` (ha d'acabar en `_bot`).
- BotFather em retorna un **token** llarg (p. ex. `6123456789:AAHxxxxxxxxxxxxxxxxxxxxxx`). Anoto aquest token en un lloc segur.
- Iniciar conversa amb el bot (cerca el seu username i prem "Iniciar" o envia `/start`).
- Per obtenir el meu **chat_id**: al navegador, obro `https://api.telegram.org/bot<TOKEN>/getUpdates`. Al JSON que retorna, veig `"chat":{"id":123456789, ...}`. Aquest `123456789` és el meu chat_id.

**2. Configurar la notificació a Uptime Kuma**:
- Accedeixo a `http://hortosona:3001`.
- Vaig a "Settings" > "Notifications".
- Clico "Setup Notification".
- Tipus: **Telegram**.
- Friendly Name: `Alerta Portainer`.
- Bot Token: enganxo el token del pas 1.
- Chat ID: enganxo el chat_id del pas 1.
- Clico "Test" — haig de rebre un missatge al Telegram tipus "Test successful".
- Si funciona, clico "Save".

**3. Crear el monitor de Portainer** (si no el tinc):
- "Add New Monitor".
- Type: HTTP(s).
- Name: `Portainer`.
- URL: `http://localhost:9000`.
- Interval: 60 segons.
- Retry: 3.
- Timeout: 5 segons.
- A "Notifications", afegeixo "Alerta Portainer".
- Configuro: "When down" + "When up" (per rebre tant la caiguda com la recuperació).
- Save.

**4. Com es dispara l'alerta?**
- Uptime Kuma fa una petició HTTP a `http://localhost:9000` cada 60 segons.
- Si 3 peticions consecutives fallen (Retry: 3), el monitor passa a DOWN.
- Uptime Kuma crida l'API de Telegram: `https://api.telegram.org/bot<TOKEN>/sendMessage` amb el chat_id i el missatge "Portainer is DOWN".
- Telegram envia una notificació push al meu mòbil.
- En qüestió de 60-180 segons des de la caiguda, rebo l'alerta.

**5. Quan el servei torna**:
- Uptime Kuma detecta que torna a respondre 200 OK.
- Envia "Portainer is UP" al Telegram.
- Tinc confirmació que el sistema s'ha recuperat.

**6. Ajustos recomanables**:
- Configurar retry count (per evitar falses alarmes per pèrdues puntuals de xarxa).
- Configurar "Resend notification every X minutes" si volem recordatoris.
- Configurar un segon canal (Email) per si Telegram falla.

## Què fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum, sobretot la part de Telegram.
- **3-4 encerts**: Repeteix l'exercici pas a pas.
- **0-2 encerts**: Repassem junts.

## Què fer si has encertat totes

- Passa al **Capítol 8** (Homepage).
