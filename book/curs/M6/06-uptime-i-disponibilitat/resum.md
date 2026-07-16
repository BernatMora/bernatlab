# Resum - Capitol 6: Uptime i disponibilitat

## La idea clau

Podem tenir tota la monitoritzacio interna que volguem (Prometheus, Grafana, Loki), pero si la RPi queda penjada o el router es reinicia, els nostres monitors tampoc funcionen. Cal un **monitor extern** que vigili els nostres serveis des de FORA, independent de la nostra infraestructura. Es com tenir un segon ull que mira des de fora.

## Que es un SLA?

SLA = Service Level Agreement. Es un compromis sobre la disponibilitat. Els mes comuns:

- **99%** ("two nines"): 3.65 dies d'inactivitat per any
- **99.9%** ("three nines"): 8.76 hores d'inactivitat per any
- **99.99%** ("four nines"): 52.6 minuts d'inactivitat per any
- **99.999%** ("five nines"): 5.26 minuts d'inactivitat per any

Per un servidor casola, aspirar a 99.9% es raonable. Això vol dir que el sistema pot estar caigut menys de 9 hores l'any. Per una RPi, perdre el WiFi del router o que marxi la llum ja son 30 minuts, per tant la realitat es mes propera a 99.5%.

## Que es el temps d'uptime?

**Uptime** es el percentatge de temps que un servei ha estat disponible. Es calcula com:

```
uptime = (temps_total - temps_caigut) / temps_total * 100
```

Exemple: un servei cau 5 minuts al dia durant una setmana = 35 minuts de downtime setmanal = (35 / (7*24*60)) * 100 = 0.35% de downtime = **99.65% d'uptime**.

## Per que cal un monitor EXTERN

Si nomes monitors des de dins, tens dos problemes:

1. **El monitor cau amb el sistema**: si la RPi es penja, el monitor tambe. No t'assabentes de res.
2. **No detecta fallades de xarxa**: si el router es reinicia, la RPi esta be pero no es accessible. Des de dins, no ho saps.

Un monitor extern corre en un altre lloc (cloud, casa d'un amic) i mira la teva RPi des de fora. Es l'unic que pot dir "la teva RPi no es accesible des d'internet".

## Uptime Kuma: el monitor del BernatLab

Uptime Kuma es una eina open source auto-allotjada ("self-hosted") que permet monitorar serveis HTTP, TCP, ping, DNS, etc. Es l'alternativa a Pingdom, UptimeRobot, etc. pero GRATIS i a casa teva.

Avantatges respecte serveis cloud:
- **Gratis i privat**: totes les dades a casa teva.
- **Sense limits artificials**: monitors il·limitats, verificacions cada 30s.
- **Multiples tipus de probes**: HTTP(S), TCP, ping, DNS, MQTT, etc.
- **UI bonica**: web amb status page publicable.
- **Alertes integrades**: Telegram, email, Discord, etc.

Desavantatges:
- **Si la teva RPi cau, Uptime Kuma tambe** (si esta a la mateixa RPi).
- **Cal un segon lloc**: per tenir monitor realment extern, cal posar Uptime Kuma en una altre maquina o al cloud.

## Instal·lacio d'Uptime Kuma

```yaml
# Afegeix al docker-compose.yml
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
cd ~/bernatlab
mkdir -p uptime-kuma/data
docker compose up -d uptime-kuma
```

Accedeix a `http://IP_RPI:3001`. El primer cop et demanara crear un compte admin.

## Configurar els monitors basics

A la UI d'Uptime Kuma:

1. **"Add New Monitor"**
2. **Tipus**: HTTP(s)
3. **URL**: `http://192.168.1.50:8123` (la teva RPi o un servei)
4. **Heartbeat interval**: 60 segons (cada quan comprova)
5. **Retries**: 3 (quantes vegades falla abans de marcar DOWN)
6. **Save**

Repeteix per cada servei important:

- **Grafana**: `http://192.168.1.50:3000`
- **Prometheus**: `http://192.168.1.50:9090`
- **Home Assistant**: `http://192.168.1.50:8123`
- **Loki**: `http://192.168.1.50:3100`
- **Router**: tipus "Ping", IP `192.168.1.1`
- **DNS**: tipus "DNS", domini `google.com`
- **Internet**: tipus "HTTP(s)", URL `https://www.google.com`

## Status page publica

Uptime Kuma pot generar una **status page** publica amb l'estat de tots els teus serveis. Es ideal per compartir amb familia o per tenir en una pestanya del navegador.

A "Status Page" -> "New Status Page":
1. Dona un nom: "BernatLab"
2. Tria un slug: `bernatlab`
3. Títol: "Serveis del BernatLab"
4. Descripcio: "Estat dels serveis de la Raspberry Pi de casa"
5. Tema: clar o fosc
6. Afegeix els monitors que vols mostrar
7. Guarda

Ara pots accedir a `http://IP_RPI:3001/status/bernatlab` i veuras una pagina public amb l'estat.

## Alertes integrades

Uptime Kuma ja te integracio amb Telegram (i molts altres):

1. "Settings" -> "Notifications"
2. "Setup Notification" -> tria "Telegram"
3. Bot Token: el mateix d'abans
4. Chat ID: el mateix d'abans
5. "Test" per verificar
6. "Save"

Pots configurar:
- **Quins monitors avisen**: nomes els criticals, o tots.
- **Quan avisen**: nomes quan cauen, o tambe quan es recuperen.
- **Cada quan avisen**: nomes un cop o cada X minuts.

## Alternativa al monitor EXTERN: serveis cloud

Si vols un monitor REALMENT extern, tens opcions gratuites:

- **UptimeRobot** (free tier: 50 monitors, comprovacio cada 5 min): facil, fiable.
- **Cronitor** (free tier limitat): mes tecnic.
- **Healthchecks.io** (free tier: 20 monitors): per cron jobs.
- **Better Stack** (free tier limitat): nomes pagat.
- **Hetrixtools** (free tier: 15 monitors): una mica mes tecnic.

Configuracio tipica: un monitor HTTP a `http://IP_PUBLICA_RPI:8123` (el port d'HA) que comprova cada 5 min. Si falla 2 cops seguits, avisa.

## Probes importants a configurar

A mes dels monitors basics, hi ha probes que val la pena tenir:

- **HTTP amb keyword**: comprova que la pagina conté un text esperat. Per exemple, el dashboard d'HA ha de contenir "Home Assistant".
- **HTTP amb JSON i jq**: comprova que un endpoint retorna el JSON esperat.
- **TCP**: comprova que un port esta obert (per serveis que no son HTTP).
- **DNS**: comprova que un domini resol correctament.
- **Push**: tu envies un senyal periodicament. Si no arriba, vol dir que el teu job ha fallat. Ideal per backups.

## Mesurar el teu uptime real

Uptime Kuma ja calcula l'uptime per monitor:

- **Last 24 hours**: el percentatge de les ultimes 24h.
- **Last 7 days**, **30 days**, **365 days**: mes periodes llargs.

Aixo es MOLT valuos perque et permet veure tendencies. Si el teu uptime baixa setmana a setmana, tens un problema emergent. Si nomes es baixa en una setmana concreta, va ser un incident puntual.

## Connexions amb altres capitols

- **M6 Cap 1** - Arquitectura 24/7: el monitor extern es la capa d'observabilitat externa.
- **M6 Cap 4** - Alertes: Uptime Kuma pot enviar alertes a Telegram directament.
- **M2 Cap 9** - Monitoritzacio interna vs externa.
