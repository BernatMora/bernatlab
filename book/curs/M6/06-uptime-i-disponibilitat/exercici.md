# Exercici practic - Capitol 6: Uptime i disponibilitat

> 30-45 min · Real a la teva RPi

## Objectiu

Instal·lar Uptime Kuma, configurar monitors per als teus serveis principals, crear una status page publica, i configurar alertes a Telegram. Acabaras tenint una visio externa de l'estat del BernatLab.

## Requisits

- RPi amb Docker funcionant
- 20-30 minuts

## Pas 1: Afegeix Uptime Kuma al docker-compose (5 min)

```bash
cd ~/bernatlab
mkdir -p uptime-kuma/data
```

Edita `docker-compose.yml`:

```yaml
  uptime-kuma:
    image: louislam/uptime-kuma:latest
    container_name: uptime-kuma
    restart: unless-stopped
    volumes:
      - ./uptime-kuma/data:/app/data
    ports:
      - "3001:3001"
```

```bash
docker compose up -d uptime-kuma
docker ps | grep uptime-kuma
```

## Pas 2: Configura el compte admin (3 min)

Accedeix a `http://IP_RPI:3001`. El primer cop et demanara:
- Username: `admin`
- Password: una bona contrasenya
- Guarda-la!

## Pas 3: Crea els monitors basics (15 min)

A la UI, "Add New Monitor" per cada un:

**Monitor 1 - Router**
- Tipus: Ping
- Hostname: `192.168.1.1` (la IP del teu router)
- Heartbeat: 60s
- Retries: 3

**Monitor 2 - DNS Google**
- Tipus: DNS
- Hostname: `google.com`
- Heartbeat: 60s
- Retries: 3

**Monitor 3 - Internet**
- Tipus: HTTP(s)
- URL: `https://www.google.com`
- Heartbeat: 60s
- Retries: 3
- Accepts self-signed: no

**Monitor 4 - Grafana**
- Tipus: HTTP(s)
- URL: `http://192.168.1.50:3000`
- Heartbeat: 60s
- Retries: 3

**Monitor 5 - Prometheus**
- Tipus: HTTP(s)
- URL: `http://192.168.1.50:9090`
- Heartbeat: 60s
- Retries: 3

**Monitor 6 - Home Assistant**
- Tipus: HTTP(s)
- URL: `http://192.168.1.50:8123`
- Heartbeat: 60s
- Retries: 3

**Monitor 7 - SSH (TCP)**
- Tipus: Port (TCP)
- Hostname: `192.168.1.50`
- Port: 22
- Heartbeat: 60s
- Retries: 3

Substitueix `192.168.1.50` per la IP de la teva RPi.

## Pas 4: Configura alerta a Telegram (5 min)

A "Settings" -> "Notifications" -> "Setup Notification":
1. Tipus: Telegram
2. Bot Token: el token del cap 4
3. Chat ID: el chat ID del cap 4
4. "Test" - hauries de rebre un missatge
5. "Save"

## Pas 5: Crea una status page publica (10 min)

A "Status Page" -> "New Status Page":
1. Name: `BernatLab`
2. Slug: `bernatlab`
3. Title: `Serveis del BernatLab`
4. Description: `Estat dels serveis de la Raspberry Pi de casa`
5. Theme: light o dark (al teu gust)
6. Show Certificate Expiry: ON
7. Add monitors: selecciona els 7 anteriors
8. Save

Ara tens una URL publica a `http://IP_RPI:3001/status/bernatlab` accessible per tothom a la teva xarxa.

## Pas 6: Configura un monitor "push" per backups (5 min)

Aquest tipus de monitor funciona al reves: TU li envies un senyal quan fas una tasca. Si no arriba el senyal, vol dir que la tasca ha fallat.

1. "Add New Monitor"
2. Tipus: Push
3. Push URL: et donara una URL tipus `https://uptime-kuma/api/push/XXXXX?status=up&msg=OK`
4. Heartbeat: 86400 (24h)
5. Retries: 1
6. Save

Ara al teu script de backups, afegeix al final:

```bash
curl -s "https://uptime-kuma/api/push/XXXXX?status=up&msg=Backup+OK" > /dev/null
```

Si el backup falla:

```bash
curl -s "https://uptime-kuma/api/push/XXXXX?status=down&msg=Backup+FAILED" > /dev/null
```

Uptime Kuma avisara si passa mes de 24h sense rebre senyal.

## Validacio

Has acabat si:

- [ ] Uptime Kuma esta corrent al port 3001.
- [ ] Has creat almenys 5 monitors basics.
- [ ] Has configurat l'alerta de Telegram i has rebut un missatge de test.
- [ ] Has creat una status page publica.
- [ ] Has configurat un monitor push per backups.

## Per aprofundir

- Configura un monitor HTTP amb "keyword" per comprovar contingut.
- Afegeix monitors per serveis externs que usis (API de meteo, etc.).
- Configura un monitor extern real (UptimeRobot gratuit) per tenir un segon ull.
- Exporta la llista de monitors com a JSON per tenir backup.
