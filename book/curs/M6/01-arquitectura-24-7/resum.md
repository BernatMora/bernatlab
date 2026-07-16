# Resum - Capitol 1: Arquitectura 24/7

## La idea clau

Un servidor casola (la teva Raspberry Pi del BernatLab) no es un servidor profesional amb doble font d'alimentacio, discos en RAID i un datacenter refrigerat. Pero volem que funcioni "sempre" - o almenys que sabem quan falla. Operativa 24/7 vol dir que tens les eines per detectar, reaccionar i recuperar. No es que mai caigui, es que quan cau te n'adones rapid i el tornes a aixecar.

## Que significa realment "24/7"?

No es lo mateix tenir un servidor encès que tenir un servidor operatiu. Un servei 24/7 ha de complir quatre condicions basiques:

- **Disponible**: la RPi esta encesa, el contenidor esta corrent, el port esta obert.
- **Observable**: tens alguna manera de saber si funciona (ping, dashboard, alerta).
- **Recuperable**: quan cau, el pots tornar a aixecar automaticament o amb un sol pas.
- **Mantengut**: el sistema s'actualitza, es neteja i no acaba morint ple de brossa al cap de 6 mesos.

Si nomes compleixes la primera, tens un servidor "ences", no un servidor "24/7".

## Per que es diferent a la RPi?

La Raspberry Pi es fantastica pero te limitacions importants que cal entendre:

- **MicroSD**: es un punt unic de fallada. Les escriptures constants la maten. Cal moure logs i volums a un disc USB o SSD.
- **Alimentacio**: una pujada de tensio i la RPi es reinicia. Una font bona (5V/3A minim) es vital.
- **Temperatura**: sense dissipador, a l'estiu throttling i rendiment baix. A partir de 80 graus comences a perdre CPU.
- **Xarxa**: si el router es reinicia, la RPi pot perdre la IP fixa. Cal DHCP reservation o IP estatica.
- **Sense IPMI/BMC**: en un servidor professional tens una consola remota. Aqui nomes tens SSH (si arriba) o acces fisic.

## Capes d'arquitectura 24/7

Pensa en el sistema com a capes apilades. Si la capa de baix falla, la de sobre cau pero pots recuperar nomes la de baix:

1. **Capa fisica**: RPi, alimentacio, microSD, xarxa, temperatura.
2. **Capa sistema operatiu**: Raspberry Pi OS, actualitzacions, serveis basics (ssh, cron).
3. **Capa contenidors**: Docker/Portainer, imatges, volums, xarxes.
4. **Capa aplicacio**: els serveis del BernatLab (Home Assistant, InfluxDB, Grafana, etc.).
5. **Capa observabilitat**: Prometheus, Grafana, Uptime Kuma - tot el que t'ajuda a VEURE.
6. **Capa alerta**: Telegram, email - el que t'avisa QUAN alguna cosa falla.
7. **Capa manteniment**: backups, neteja, actualitzacions - el que MANTI el sistema sa.

Cada te els seus propis monitors i cada te la seva propia forma de recuperar-se.

## Health checks basicos

Abans de posar cap eina fancy, comença per lo basic. Un script que comprovi les coses vitals:

```bash
#!/bin/bash
# /opt/bernatlab/healthcheck.sh
echo "=== Health check $(date) ==="

# RPi viu?
uptime

# Temperatura (critic a l'estiu)
vcgencmd measure_temp

# Espai en disc
df -h /

# Memoria
free -h

# Serveis clau corrent?
systemctl is-active docker
systemctl is-active ssh

# Contenidors BernatLab
docker ps --format "table {{.Names}}\t{{.Status}}" | grep -E "homeassistant|grafana|influxdb"
```

Executa-ho cada 5 minuts amb cron i guarda la sortida a un fitxer. D'aqui a uns dies tindras un mini-monitor gratis.

## Watchdog: la xarxa de seguretat

Linux te un **watchdog** que pot reiniciar automaticament la RPi si el kernel penja. Es configura amb un sol fitxer:

```bash
# Instal·la el paquet
sudo apt install watchdog

# Activa el dimoni
sudo systemctl enable watchdog
sudo systemctl start watchdog

# Configuracio basica
sudo nano /etc/watchdog.conf
```

Edita `/etc/watchdog.conf` i descomenta (o afegeix):

```
watchdog-device = /dev/watchdog
max-load-1 = 24
watchdog-timeout = 15
```

Amb aixo, si la carrega del sistema passa de 24 (24 processos bloquejats) o el sistema es queda penjat, el watchdog reiniciara la RPi. Es brutal pero efectiu. Millor un reinici automatic que un servidor penjat per sempre.

## Reinici automatic de serveis

systemd ja reinicia els seus serveis si cauen, pero Docker no. Per fer-ho, configura els teus contenidors amb `restart: always` al docker-compose:

```yaml
services:
  homeassistant:
    image: homeassistant/home-assistant:stable
    restart: always
    # ...
```

Aixi quan el contenidor peta, Docker el torna a aixecar. Si la RPi es reinicia, tambe. Es la minima expressio de "24/7".

## Connexions amb altres capitols

- **M2 Cap 9** - Monitoritzacio de contenidors (el primer pas cap a 24/7).
- **M2 Cap 8** - Backups: sense ells, 24/7 vol dir "24/7 fins que perds tot").
- **M2 Cap 7** - Actualitzacio de contenidors: com fer-ho sense deixar el sistema caigut.
- **M3 Cap 1** - Estrategia de backup: complementa la recuperacio automatica.
- **M8 Cap 7** - Runbooks basics: com documentar que fer quan alguna cosa falla.
