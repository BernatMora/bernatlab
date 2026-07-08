# Capítol 22 — Operativa: còpies, alertes, escalat

> *"Un sistema en producció no es diferencia d'un prototip pel que fa, sinó pel que passa quan alguna cosa falla."*

## 22.1 Què hem construït

En aquest mòdul hem afegit al BernatLab:

- **Mosquitto**: broker MQTT amb autenticació i ACLs.
- **InfluxDB**: base de dades de sèries temporals.
- **Telegraf**: agent de recollida de dades.
- **Node-RED**: eina de programació visual.
- **Grafana**: visualització.
- **API FastAPI**: servei REST per a clients externs.
- **Cloudflare Tunnel**: exposició segura de l'API.
- **Integració amb la web Hort Osona**.

Tot plegat, **sis serveis nous** i una integració amb una web pública. El sistema, ara com ara, és força complex. I com més complex, més important és la operativa diària.

En aquest capítol veurem les tasques que hem de fer regularment per mantenir el sistema sa: còpies de seguretat, monitoratge avançat, gestió de la retenció, i quan caldrà considerar pujar de hardware.

## 22.2 Còpies de seguretat

La regla d'or: **si no podem restaurar el sistema en una hora, no estem preparats**.

Què hem de copiar?

### Dades d'InfluxDB

InfluxDB conté tota la història de mesures. Si la perdem, perdem tot el coneixement acumulat sobre l'hort.

Còpia amb la CLI d'InfluxDB:

```bash
influx backup /home/bernat/homelab/backup/influxdb-$(date +%F) \
  --bucket hort-osona \
  --org bernatlab \
  --token TOKEN
```

Aquesta ordre crea una còpia completa del bucket. Per restaurar:

```bash
influx restore /home/bernat/homelab/backup/influxdb-2026-XX-XX \
  --bucket hort-osona \
  --org bernatlab \
  --token TOKEN
```

Compte: les còpies es fan amb el servei **aturat** per garantir la consistència.

### Configuracions

Tots els fitxers de configuració viuen a `/home/bernat/homelab/stacks/`, que ja està versionat amb Git. Tanmateix, podem fer còpies addicionals:

- `telegraf.conf`
- `mosquitto.conf`, `passwordfile`, `aclfile`
- `nodered/flows.json`
- `grafana/dashboards/*.json`
- `api/.env`

### Volums de dades

Els volums de dades contenen:

- InfluxDB: les dades històriques (ja cobert per la còpia d'InfluxDB).
- Grafana: dashboards, alertes, configuracions.
- Node-RED: fluxos.
- Mosquitto: missatges retained.

Per a còpies completes, podem aturar tots els serveis i copiar `/home/bernat/homelab/data/` sencer.

### Freqüència

- **Diàriament**: còpia d'InfluxDB.
- **Setmanalment**: còpia de les configuracions no versionades.
- **Mensualment**: còpia completa del sistema, emmagatzemada fora de la Raspberry.

### On guardar les còpies

Tres opcions:

1. **Un altre disc de la Raspberry**: ràpid, però no protegeix contra fallada de hardware.
2. **Un PC de la xarxa**: bona opció, amb `rsync` o `scp`.
3. **El núvol**: la millor opció per a còpies de seguretat de veritat. Backblaze B2, Mega.nz, o un repositori Git privat.

Al BernatLab, farem còpies al núvol amb un script que combina `influx backup` amb `rclone` (que suporta múltiples proveïdors de núvol).

## 22.3 Retenció de dades

InfluxDB ens permet definir **polítiques de retenció** per a cada bucket. Al Capítol 15 ja vàrem parlar d'això, però ara veurem com gestionar-ho de forma dinàmica.

### Estratègia de retenció

Al BernatLab, fem servir tres buckets:

- **hort-osona** (1 any): dades originals, alta resolució.
- **hort-osona-1h** (5 anys): dades agregades a resolució horària.
- **hort-osona-1d** (10 anys): dades agregades a resolució diària.

Les agregacions les fan **tasks** periòdiques que calculen la mitjana, màxim i mínim per a finestres temporals.

### Quanta memòria/disc ocupa?

Podem estimar:

- 10 sensors × 5 mesures cadascun × 1 punt per minut × 60 minuts × 24 hores × 365 dies = **262 milions de punts per any**.
- Cada punt ocupa uns 100 bytes amb índexs.
- Total: uns **26 GB per any**.

Això és molt per a una microSD de 32 GB. Per això cal:

- **Reduir la freqüència de publicació** si no necessitem 1 punt per minut.
- **Agregar dades** en buckets separats.
- **Usar un SSD USB** (pròximament).

### Monitoratge de l'ús de disc

Un script que ens avisa quan el disc s'omple:

```bash
#!/bin/bash
# comprovar_espai.sh
US=$$(df -h / | tail -1 | awk '{print $5}' | sed 's/%//')$$
if [ $US -gt 80 ]; then
    curl -X POST "https://api.telegram.org/bot$BOT_TOKEN/sendMessage" \
        -d "chat_id=$CHAT_ID" \
        -d "text=⚠️ Disc del BernatLab al ${US}% d'ús"
fi
```

Podem programar aquest script amb `cron` perquè s'executi cada dia.

## 22.4 Monitoratge avançat

Uptime Kuma ens avisa quan un servei cau. Però podem anar més enllà:

### Monitorar mètriques internes

Cada servei pot exposar mètriques que Uptime Kuma pot consultar:

- **InfluxDB**: té un endpoint `/metrics` en format Prometheus.
- **Node-RED**: pot exposar mètriques amb un node personalitzat.
- **Grafana**: té el seu propi sistema d'alertes.
- **API**: podem afegir un endpoint `/metrics` amb prometheus_client.

Això ens permet monitorar coses com:

- Quantes consultes per segon rep l'API.
- Quanta memòria consumeix Node-RED.
- Quantes insercions per segon fa Telegraf.

### Alertes de capacitat

A més dels serveis caiguts, podem alertar quan:

- El disc supera el 80 % d'ús.
- La RAM supera el 90 % d'ús.
- La CPU supera el 80 % durant més de 5 minuts.
- La temperatura de la CPU supera els 70 °C.

Això es pot fer amb un script que consulti `/proc` i enviï alertes per Telegram.

### Alertes de dades

També podem alertar quan les dades no arriben:

- Cap publicació MQTT durant 10 minuts → possible problema de xarxa o de sensors.
- InfluxDB no ha rebut cap punt en 30 minuts → problema amb Telegraf.
- Un sensor concret porta més d'1 hora sense publicar → possible bateria esgotada.

Aquestes alertes les podem configurar a Node-RED o Grafana.

## 22.5 Logs centralitzats

Quan tenim molts serveis, revisar logs pot ser un mal de cap. Una solució és centralitzar-los.

### Opció simple: volums compartits

Tots els serveis escriuen els seus logs a `/home/bernat/homelab/logs/`, organitzat per servei:

```yaml
volumes:
  - /home/bernat/homelab/logs/mosquitto:/mosquitto/log
  - /home/bernat/homelab/logs/influxdb:/var/log/influxdb
  - /home/bernat/homelab/logs/grafana:/var/log/grafana
```

Podem revisar-los tots amb `tail -f` o eines com `lnav`.

### Opció avançada: Loki

**Loki** és un sistema de logs centralitzat, similar a Prometheus però per a logs. Grafana s'hi integra nativament.

Però això és potser excessiu per a un homelab. Per ara, els volums compartits són suficients.

## 22.6 Actualitzacions

Mantenir el sistema actualitzat és fonamental, però cada actualització és un risc.

### Estratègia

1. **Llegir les notes de versió** abans d'actualitzar res.
2. **Fer una còpia de seguretat** abans d'actualitzar.
3. **Actualitzar un servei a la vegada**.
4. **Provar** que tot funciona.
5. **Si alguna cosa falla**, poder tornar enrere.

### Procediment estàndard

```bash
cd /home/bernat/homelab/stacks/iot
docker compose pull
docker compose up -d
# Esperar 5 minuts
docker compose ps
docker compose logs --tail=50
```

Si tot és correcte, podem continuar amb el següent servei.

### Quan NO actualitzar

- Si el sistema està en ple funcionament i no tenim temps per depurar.
- Si les notes de versió mencionen canvis que poden trencar la configuració.
- Si tenim poc espai de disc per fer còpies.

## 22.7 Rendiment: quan cal pujar de hardware

Amb 4 GB de RAM i una microSD, el BernatLab té un sostell. Quan el sistema creix, pot ser que:

- InfluxDB es torna lent.
- Grafana trigui massa a carregar.
- Els contenidors es reiniciïn per manca de memòria.
- La microSD s'ompli ràpidament.

### Quan cal més RAM

Si veiem `killed` als logs (Linux mata processos quan no hi ha prou RAM), és hora d'ampliar. Les solucions:

- **Passar a 8 GB de RAM** (la Raspberry Pi 4 admet fins a 8 GB).
- **Afegir swap a un SSD USB** (per crear "RAM virtual" en un disc).

### Quan cal un SSD

La microSD és el coll d'ampolla per a bases de dades. Si InfluxDB va lent i tenim moltes dades, és hora de moure les dades a un SSD.

La Raspberry Pi 4 pot arrencar des d'un SSD USB. El procediment:

1. Connectar el SSD a un port USB 3.0.
2. Instal·lar Raspberry Pi OS al SSD (o copiar la microSD).
3. Configurar la BIOS per arrencar des d'USB.
4. Moure les dades.

Això és un projecte per si sol, però és al full de ruta del BernatLab.

### Quan cal un segon servidor

Si arribem al punt que la Raspberry no dona per a més, podem considerar:

- Una Raspberry Pi 5 (més potent, ~120 €).
- Un mini PC amb Intel N100 (~200 €).
- Un servidor dedicat al núvol (VPS).

Per ara, amb la Raspberry 4 i un SSD, podem arribar força lluny.

## 22.8 Seguretat contínua

La seguretat no és un estat, és un procés. Cal revisar periòdicament:

### Auditar accessos

- Qui s'ha connectat per SSH? (`journalctl -u ssh --since "1 month ago"`)
- Quins clients MQTT s'han connectat? (Logs de Mosquitto)
- Quins accessos a l'API s'han fet? (Logs de l'API)

### Auditar tokens

- Tots els tokens d'InfluxDB són necessaris?
- Les API keys s'usen, o estan abandonades?
- Hi ha credencials al codi que s'haurien de moure al `.env`?

### Auditar ports

```bash
ss -tulpn
```

Quins ports tenim oberts? Tots són necessaris? Algú ha afegit un servei que no toca?

### Auditar permisos

- Els usuaris tenen només els permisos que necessiten?
- Hi ha fitxers amb permisos massa oberts? (`chmod 777` és sempre sospitós)

### Auditar actualitzacions

- Tots els serveis estan a l'última versió?
- Hi ha vulnerabilitats conegudes? (`docker scan` o `trivy`)

## 22.9 Documentació contínua

Cada canvi al sistema ha de quedar documentat. Al BernatLab, tenim:

- **README.md**: descripció general, com començar.
- **CHANGELOG.md**: registre cronològic de canvis.
- **docs/**: documentació addicional per temes.
- **Git**: historial de canvis a la configuració.
- **Aquest manual**: el coneixement aprofundit.

Quan fem un canvi important, hem d'actualitzar el `CHANGELOG.md`:

```markdown
# CHANGELOG — BernatLab

## 2026-08-15
- Afegit sensor BME280 a la zona de pebrots
- Configurat monitor d'Uptime Kuma per a l'API
- Actualitzat InfluxDB a 2.7.5

## 2026-08-01
- Integració amb la web Hort Osona completa
- Publicació del dashboard de Grafana
```

## 22.10 Procediments davant d'incidents

Quan alguna cosa falla, hem de tenir un protocol clar:

### Pas 1: detectar

Uptime Kuma ens avisa per Telegram.

### Pas 2: identificar

Quin servei falla? Què diuen els logs?

```bash
docker compose logs servei
```

### Pas 3: contenir

Si el servei no es recupera amb un reinici, podem aturar-lo temporalment per evitar danys:

```bash
docker compose stop servei
```

### Pas 4: resoldre

Buscar la solució: llegir documentació, buscar a Internet, provar.

### Pas 5: recuperar

Tornar a aixecar el servei:

```bash
docker compose up -d servei
```

### Pas 6: aprendre

Un cop resolt, escriure al CHANGELOG què ha passat i com s'ha resolt. Si cal, afegir un monitor per detectar-ho abans la pròxima vegada.

## 22.11 Quan rebre ajuda

A vegades, tot i els nostres esforços, no podem resoldre un problema. En aquests casos:

- **Documentació oficial**: la primera parada.
- **Forums i comunitats**: Reddit, StackOverflow, fòrums específics.
- **GitHub Issues**: si el problema és d'un servei específic, potser ja està reportat.
- **ChatGPT, Claude, altres IAs**: eines útils per a depurar.

I, per descomptat, **jo (Hermes)** soc aquí per ajudar-te amb el BernatLab quan calgui.

## 22.12 Full de ruta operativa

Aquí tens una llista de tasques operatives que hauries de fer regularment:

### Diàriament

- [ ] Comprovar Uptime Kuma (o rebre les alertes per Telegram).
- [ ] Mirar si hi ha alertes de sensors inactius.

### Setmanalment

- [ ] Còpia de seguretat d'InfluxDB.
- [ ] Revisar els logs dels serveis.
- [ ] Comprovar l'ús de disc i memòria.
- [ ] Actualitzar contenidors si n'hi ha de nous.

### Mensualment

- [ ] Còpia de seguretat completa al núvol.
- [ ] Auditar accessos i tokens.
- [ ] Revisar el CHANGELOG i actualitzar-lo si cal.
- [ ] Comprovar l'estat del hardware (temperatura, salut de la microSD/SSD).

### Anualment

- [ ] Planificar actualitzacions de hardware.
- [ ] Revisar l'arquitectura del sistema i simplificar si cal.
- [ ] Fer un balanç: què ha funcionat, què no.

## 22.13 Reflexió final

Hem cobert molta terra en aquest mòdul. Hem passat d'un servidor amb tres serveis bàsics a un sistema complet de captura, emmagatzemament, processament, visualització i exposició de dades d'un hort. Això és una fita important.

Però recorda: la millor tecnologia és la que s'usa. No té sentit tenir el sistema més sofisticat del món si després no el mirem, no l'entenem, no l'aprofiten. Un sistema senzill que funciona és infinitament millor que un sistema complex que abandonem.

Si en algun moment el BernatLab es torna massa complicat de mantenir, **simplifica**. Lleva el que no usis. Documenta el que conservis. Fes que cada peça compti.

## 22.14 Resum

Hem après les tasques operatives essencials per mantenir el BernatLab sa: còpies de seguretat, retenció de dades, monitoratge avançat, logs centralitzats, actualitzacions, rendiment, seguretat contínua, documentació, i procediments davant d'incidents. Hem vist quan cal pujar de hardware i hem establert una full de ruta operativa diària, setmanal, mensual i anual. En el proper mòdul (M3) tractarem la part de ràdio: sensors LoRa SX1262, xarxes de llarg abast, i la integració amb el sistema MQTT. En el M4 parlarem d'IA local amb Ollama i RAG sobre les dades.

## 22.15 Exercicis pràctics

1. Escriu un script `backup.sh` que faci còpia d'InfluxDB i la pugi al núvol amb rclone.
2. Programa aquest script amb `cron` perquè s'executi cada dia a les 3:00 AM.
3. Configura un monitor a Uptime Kuma per a l'API i per a Grafana.
4. Mira l'ús de disc actual: `df -h`. Quant queda lliure? Quant ocupa InfluxDB?
5. Escriu al CHANGELOG un resum de tot el que hem fet en aquest mòdul.
6. Planifica una auditoria de seguretat: quins tokens, quins usuaris, quins ports.
7. Documenta al README del projecte el procediment davant d'incidents.
8. Fes una còpia de seguretat completa del sistema i guarda-la fora de la Raspberry.

Comandes útils:
```bash
# Còpia d'InfluxDB
influx backup /backup/influxdb-$(date +%F) --token TOKEN

# Ús de disc
df -h
du -sh /home/bernat/homelab/data/*

# Monitorar serveis
docker ps
docker stats --no-stream

# Veure logs
docker compose logs -f --tail=100

# Auditoria
ss -tulpn
journalctl -u ssh --since "1 month ago"
```

Paraules clau: **operativa, còpia de seguretat, backup, retenció, monitoratge, alertes, logs, actualitzacions, rendiment, RAM, SSD, seguretat, auditar, tokens, ports, permisos, documentació, CHANGELOG, incidents, procediment, full de ruta, operativa diària, operativa setmanal, operativa mensual, operativa anual, simplificar, sistema, BernatLab, sensors, dades, hort, Mòdul 3, Mòdul 4, LoRa, IA, Ollama, RAG, cron, rclone, Uptime Kuma, Telegram, df, docker stats, journalctl, ss, talls, hardware, microSD, Raspberry Pi 5, N100, VPS**.
