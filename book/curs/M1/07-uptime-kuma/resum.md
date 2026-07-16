# Resum — Capítol 7: Uptime Kuma

## La idea clau

Un homelab sense monitoratge és com un cotxe sense quadre de comandament: no saps quina velocitat fas, quanta benzina et queda, o si el motor s'ha escalfat. **Uptime Kuma** és el "quadre de comandament" del BernatLab: una eina que vigila si els teus serveis estan vius, mesura el temps de resposta, i t'avisa per Telegram (o altres canals) quan algo cau. S'hi accedeix via `http://hortosona:3001`.

## Què és Uptime Kuma?

Uptime Kuma és una aplicació web de monitoratge self-hosted (l'allotges tu). Fa una cosa i la fa bé: **vigilar serveis i alertar quan fallen**. Està feta amb Node.js + Vue.js, i mantinguda per una comunitat activa (molt popular a GitHub, ~60k estrelles).

Tipus de monitors que suporta:

- **HTTP(s)**: comprova que una URL retorni 200 OK.
- **Ping**: ICMP echo (clàssic ping).
- **TCP port**: comprova que un port estigui obert.
- **DNS**: consulta un registre DNS.
- **Docker**: monitoritza contenidors directament (consulta l'API Docker).
- **Push**: el servei envia "I'm alive" periòdicament.
- **SQL/Mongo/Redis/Postgres**: connexions a bases de dades.
- **Certificat SSL**: vigila quan caduca el certificat.
- I molts més...

## Per què l'usem al BernatLab

- **Saber ràpid si algo ha caigut** (sense esperar que ho noti un visitant).
- **Mesurar uptime**: quin % del temps ha estat cada servei actiu?
- **Detectar degradació**: latència creixent pot indicar un problema.
- **Rebre alertes** al mòbil (Telegram) quan passa alguna cosa.
- **Visualitzar tendències**: gràfiques de disponibilitat, temps de resposta.
- **Pàgina pública d'estat** (status page) per compartir amb família/amics.

Per a un homelab de 4-10 serveis, Uptime Kuma és la solució ideal: lleugera, senzilla, gratuïta, self-hosted.

## Instal·lació al BernatLab

```yaml
# Afegir a ~/homelab/docker/docker-compose.yml
services:
  uptime-kuma:
    image: louislam/uptime-kuma:latest
    container_name: uptime-kuma
    ports:
      - "3001:3001"
    volumes:
      - uptime_data:/app/data
      - /var/run/docker.sock:/var/run/docker.sock  # per monitorar contenidors
    restart: unless-stopped

volumes:
  uptime_data:
```

```bash
cd ~/homelab/docker
docker compose up -d uptime-kuma
```

Accedeix a `http://hortosona:3001`, crea l'usuari admin, i ja hi ets.

## Configuració dels primers monitors

Un cop dins, ves a "Add New Monitor" i configura:

### Monitor 1: Ping a la pròpia RPi

- **Type**: Ping
- **Name**: RPi hortosona (ping)
- **Hostname**: `127.0.0.1` o `hortosona`
- **Interval**: 60 segons
- **Retry**: 3
- **Timeout**: 5 segons

### Monitor 2: Portainer (HTTP)

- **Type**: HTTP(s)
- **Name**: Portainer
- **URL**: `http://hortosona:9000`
- **Interval**: 60s
- **Accepted status codes**: 200-299
- **Save**

### Monitor 3: Connexió a Internet

- **Type**: HTTP(s)
- **Name**: Internet (Cloudflare DNS)
- **URL**: `https://1.1.1.1`
- **Interval**: 5 min
- **Save**

Si volem monitors per a tots els serveis de l'homelab, una bona llista inicial:

- RPi (ping)
- Portainer (HTTP 9000)
- Homepage (HTTP 3010)
- SSH (TCP 22)
- DNS extern (Cloudflare 1.1.1.1)
- GitHub (HTTPS api.github.com)
- La teva pàgina web personal (si en tens)

## Alertes: configurar Telegram

Les alertes són la part crítica. Sense alertes, el monitoratge és inútil. Telegram és el canal més fàcil al BernatLab.

### Crear el bot de Telegram

1. Parla amb `@BotFather` a Telegram.
2. Envia `/newbot`, posa-li un nom (p. ex. "BernatLab Alerts") i un username (p. ex. `bernatlab_alerts_bot`).
3. BotFather et donarà un **token** (un string llarg tipus `123456789:ABCdefGHI...`). Guarda'l.
4. Afegeix el bot a un grup o inicia una conversa privada amb ell.
5. Per obtenir el teu **chat_id**: visita `https://api.telegram.org/bot<TOKEN>/getUpdates` i mira el camp `chat.id`.

### Configurar Uptime Kuma

1. A Uptime Kuma, vés a "Settings" > "Notifications".
2. Clica "Setup Notification".
3. **Type**: Telegram.
4. **Bot Token**: el token del pas anterior.
5. **Chat ID**: el teu chat_id.
6. Prova amb "Test" — hauries de rebre un missatge al Telegram.
7. Desa.

Ara, quan un monitor caigui, rebràs un missatge al mòbil en qüestió de minuts.

## Altres canals d'alerta

Uptime Kuma suporta molts altres canals:

- **Email** (SMTP, menys immediat).
- **Discord** (webhook).
- **Slack** (webhook).
- **Microsoft Teams**.
- **Pushover** (app de pagament per a alertes).
- **Gotify** (self-hosted).
- **Webhook** genèric (per integrar amb qualsevol cosa).

Al BernatLab, Telegram + Email de backup és la combinació recomanada.

## Status Page pública

Una de les funcionalitats més maques: pots crear una **status page** pública (o privada) que mostra l'estat de tots els teus serveis:

- Vés a "Status Pages" > "New Status Page".
- Nom: "BernatLab Status".
- Slug: `bernatlab` (URL: `http://hortosona:3001/status/bernatlab`).
- Tria quins monitors vols mostrar.
- Tema: clar o fosc.
- Desa i comparteix l'enllaç amb família/amics.

Si ells accedeixen i veuen "✅ Operatiu", saben que tot va bé. Si veuen "🔴 Caigut", ja saben que no és cosa seva.

## Correlació amb Portainer

Si tens el socket Docker muntat (`/var/run/docker.sock`), pots afegir monitors de tipus "Docker Container" i Uptime Kuma et dirà si un contenidor concret està running. Combinat amb Portainer, tens:

- **Portainer**: operacions manuals, visualització, gestió.
- **Uptime Kuma**: vigilància passiva + alertes automàtiques.

## Connexions amb altres capítols

- **Cap 5-6** — Uptime Kuma és un contenidor Docker monitorant altres contenidors.
- **Cap 8** — Homepage mostrarà l'estat del BernatLab amb un widget d'Uptime Kuma.
- **Cap 22** — Monitoratge avançat (Prometheus + Grafana) per a mètriques profundes.
- **Cap 23** — Alertes externes i pàgines de status avançades.

Ja saps quan un servei cau. Ara toca posar un bon "lloc d'entrada" visual a tot plegat.
