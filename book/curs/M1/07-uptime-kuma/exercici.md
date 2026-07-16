# Exercici pràctic — Capítol 7: Uptime Kuma

> 45-60 min · Real al teu sistema

## Objectiu
Posar en marxa Uptime Kuma, configurar els primers monitors dels teus serveis, i activar alertes per Telegram. Acabaràs amb un sistema que t'avisa al mòbil quan alguna cosa falla.

## Requisits
- Docker instal·lat i corrent
- Tailscale actiu
- Telegram instal·lat al mòbil
- 45-60 minuts

## Pas 1: Afegeix Uptime Kuma al compose (10 min)

Edita `~/homelab/docker/docker-compose.yml`:

```yaml
version: "3.9"

services:
  portainer:
    image: portainer/portainer-ce:latest
    container_name: portainer
    ports:
      - "9000:9000"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - portainer_data:/data
    restart: unless-stopped

  uptime-kuma:
    image: louislam/uptime-kuma:latest
    container_name: uptime-kuma
    ports:
      - "3001:3001"
    volumes:
      - uptime_data:/app/data
      - /var/run/docker.sock:/var/run/docker.sock
    restart: unless-stopped

  whoami:
    image: traefik/whoami
    container_name: whoami
    ports:
      - "8080:80"
    restart: unless-stopped

volumes:
  portainer_data:
  uptime_data:
```

```bash
cd ~/homelab/docker
docker compose up -d
docker compose ps
```

## Pas 2: Configuració inicial (5 min)

1. Obre `http://hortosona:3001`.
2. Crea l'usuari admin.
3. Ja ets al dashboard.

## Pas 3: Crea els primers monitors (15 min)

Vés a "Add New Monitor" per cadascun:

**Monitor 1: RPi ping**
- Type: Ping
- Name: `RPi hortosona`
- Hostname: `127.0.0.1`
- Interval: 60s
- Save

**Monitor 2: Portainer**
- Type: HTTP(s)
- Name: `Portainer`
- URL: `http://localhost:9000`
- Interval: 60s
- Save

**Monitor 3: Whoami**
- Type: HTTP(s)
- Name: `Whoami`
- URL: `http://localhost:8080`
- Interval: 60s
- Save

**Monitor 4: SSH port**
- Type: Port (TCP)
- Name: `SSH`
- Hostname: `127.0.0.1`
- Port: `22`
- Interval: 60s
- Save

**Monitor 5: Internet**
- Type: HTTP(s)
- Name: `Internet (Cloudflare)`
- URL: `https://1.1.1.1`
- Interval: 5 min
- Save

Després de 2-3 minuts hauries de veure tots els monitors amb check verd (UP).

## Pas 4: Crea el bot de Telegram (10 min)

1. Al mòbil, obre Telegram.
2. Busca `@BotFather`.
3. Envia `/newbot`.
4. Nom: `BernatLab Alerts`.
5. Username: `bernatlab_alerts_$(date +%s)_bot` (que sigui únic).
6. Guarda el **token** que et dóna (format: `1234567890:ABC...`).
7. Inicia conversa amb el teu bot (cerca'l per username i prem "Iniciar").
8. Per obtenir el teu chat_id, obre al navegador:
   `https://api.telegram.org/bot<EL_TEU_TOKEN>/getUpdates`
   Hauries de veure un JSON amb el teu `chat.id` (un número).
9. Anota el token i el chat_id.

## Pas 5: Configura l'alerta a Uptime Kuma (10 min)

1. A Uptime Kuma, vés a "Settings" > "Notifications".
2. Clica "Setup Notification".
3. **Type**: Telegram.
4. **Friendly Name**: `Telegram Bernat`.
5. **Bot Token**: enganxa el token.
6. **Chat ID**: enganxa el chat_id.
7. Clica "Test" — has de rebre un missatge al Telegram.
8. Desa.

## Pas 6: Connecta les alertes als monitors (5 min)

1. Edita el monitor "Portainer".
2. Clica "Notifications" (o "Setup Notification" al monitor).
3. Tria "Telegram Bernat".
4. Configura: "When the monitor goes down" + "When the monitor goes back up".
5. Repeteix per a "Whoami", "SSH", i algun altre.

## Pas 7: Prova l'alerta (10 min)

1. Para un servei: `docker stop whoami`.
2. Espera ~60 segons (interval del monitor).
3. Hauries de rebre una alerta de Telegram: "Whoami is DOWN".
4. Torna a aixecar: `docker start whoami`.
5. Espera ~60 segons.
6. Alerta: "Whoami is UP".

## Pas 8: Crea una Status Page (5 min)

1. Vés a "Status Pages" > "New Status Page".
2. Name: `BernatLab Status`.
3. Slug: `bernatlab`.
4. Description: `Estat dels serveis del BernatLab`.
5. Public: yes.
6. Afegeix tots els monitors.
7. Desa i obre `http://hortosona:3001/status/bernatlab`.

## Validació

Has acabat si:
- [ ] Uptime Kuma corre a `http://hortosona:3001`.
- [ ] Tens almenys 5 monitors actius.
- [ ] Has creat un bot de Telegram i tens el token + chat_id.
- [ ] Has configurat l'alerta de Telegram a Uptime Kuma.
- [ ] Has provat l'alerta parant i reiniciant un contenidor.
- [ ] Has creat una Status Page pública.
- [ ] Has documentat a `book/curs/M1/07-uptime-kuma/diari.md`.

## Per aprofundir

- Configura monitor de certificat SSL per a un domini propi.
- Afegeix un monitor de tipus "Push" per a scripts que s'executen periòdicament.
- Configura un segon canal d'alertes (Email) com a backup.
- Investiga la "Maintenance" per silenciar alertes durant finestres de manteniment.
