# Exercici practic - Capitol 1: Arquitectura 24/7

> 30-45 min · Real a la teva RPi

## Objectiu

Posar les bases d'un sistema 24/7: crear un script de healthcheck, configurar el watchdog de Linux, i assegurar que els teus contenidors es reinicien automaticament. Acabaras amb una RPi que es recupera sola de les fallades mes basics.

## Requisits

- RPi amb Raspberry Pi OS
- Acces root (sudo)
- Almenys un contenidor BernatLab corrent

## Pas 1: Crea el script de healthcheck (10 min)

```bash
sudo mkdir -p /opt/bernatlab
sudo nano /opt/bernatlab/healthcheck.sh
```

Enganxa aquest contingut:

```bash
#!/bin/bash
# /opt/bernatlab/healthcheck.sh
# Comprovacions basiques del sistema BernatLab

LOG=/var/log/bernatlab-health.log
DATE=$(date '+%Y-%m-%d %H:%M:%S')

echo "=== Health check $DATE ===" >> $LOG

# 1. Sistema viu
echo "[Uptime]" >> $LOG
uptime >> $LOG

# 2. Temperatura (avisar si > 70 graus)
TEMP=$(vcgencmd measure_temp | grep -o '[0-9]*\.[0-9]*')
echo "[Temp] ${TEMP}C" >> $LOG
if (( $(echo "$TEMP > 70" | bc -l) )); then
    echo "WARN: temperatura alta" >> $LOG
fi

# 3. Espai en disc (avisar si < 10% lliure)
DISK_FREE=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
echo "[Disk] ${DISK_FREE}% usat" >> $LOG
if [ $DISK_FREE -gt 90 ]; then
    echo "WARN: poc espai en disc" >> $LOG
fi

# 4. Memoria
echo "[Memory]" >> $LOG
free -h >> $LOG

# 5. Serveis basics
echo "[Services]" >> $LOG
for svc in docker ssh cron; do
    STATUS=$(systemctl is-active $svc)
    echo "  $svc: $STATUS" >> $LOG
done

# 6. Contenidors BernatLab
echo "[Containers]" >> $LOG
docker ps --format "  {{.Names}}: {{.Status}}" >> $LOG 2>&1

echo "---" >> $LOG
```

Fes-lo executable i prova:

```bash
sudo chmod +x /opt/bernatlab/healthcheck.sh
sudo /opt/bernatlab/healthcheck.sh
sudo tail -20 /var/log/bernatlab-health.log
```

## Pas 2: Programa el healthcheck cada 5 minuts (5 min)

```bash
sudo crontab -e
```

Afegeix aquesta línia:

```
*/5 * * * * /opt/bernatlab/healthcheck.sh
```

Espera 5 minuts i comprova que el log creix:

```bash
sudo wc -l /var/log/bernatlab-health.log
```

## Pas 3: Configura el reinici automatic als contenidors (5 min)

Mira quins dels teus contenidors NO tenen restart automatic:

```bash
docker ps --format "table {{.Names}}\t{{.Status}}" 
```

Si tens un docker-compose, edita'l i afegeix `restart: always` (o `unless-stopped`) a cada servei. Despres:

```bash
cd ~/bernatlab
docker compose up -d
```

Si vols aplicar-ho a un contenidor ja existent sense tocar el compose:

```bash
docker update --restart=always NOM_CONTENIDOR
```

## Pas 4: Instal·la i configura el watchdog (10 min)

```bash
sudo apt update
sudo apt install -y watchdog

sudo nano /etc/watchdog.conf
```

Descomenta o afegeix aquestes línies:

```
watchdog-device = /dev/watchdog
max-load-1 = 24
watchdog-timeout = 15
min-memory = 1
watchdog-timeout = 15
```

Activa el servei:

```bash
sudo systemctl enable watchdog
sudo systemctl start watchdog
sudo systemctl status watchdog
```

Comprova que el dispositiu existeix:

```bash
ls -l /dev/watchdog
```

Si `/dev/watchdog` no existeix, has d'activar el watchdog al config.txt:

```bash
sudo nano /boot/config.txt
# Afegeix:
dtparam=watchdog=on
sudo reboot
```

## Pas 5: Simula una fallada i comprova la recuperacio (10 min)

Comprova que els teus contenidors es reinicien sols:

```bash
# Atura un contenidor
docker stop homeassistant
sleep 5
docker ps  # Hauria de tornar a estar "Up"
```

Mira el log del healthcheck:

```bash
sudo tail -30 /var/log/bernatlab-health.log
```

Hauries de veure el moment en que el contenidor estava caigut.

## Pas 6: Documenta la teva arquitectura (5 min)

Crea un fitxer `ARQUITECTURA.md` a `/opt/bernatlab/`:

```bash
sudo nano /opt/bernatlab/ARQUITECTURA.md
```

Descriu:
- Quins serveis tens corrent i per que
- On es guarden les dades
- Quin es el procediment de recuperacio si la RPi es reinicia
- Qui te acces (IP, usuaris)

## Validacio

Has acabat si:

- [ ] Tens el script `/opt/bernatlab/healthcheck.sh` funcionant.
- [ ] El cron l'executa cada 5 minuts i el log creix.
- [ ] Tots els teus contenidors tenen `restart: always` o `unless-stopped`.
- [ ] El watchdog de Linux esta actiu i configurat.
- [ ] Has provat que un contenidor es reinicia sol.
- [ ] Tens un document `ARQUITECTURA.md` basic.

## Per aprofundir

- Configura logrotate per `/var/log/bernatlab-health.log` (sino creixera infinit).
- Investiga què passa si el watchdog es dispara moltes vegades seguides.
- Prova `monit` com a alternativa mes amigable al watchdog.
- Mira si la teva RPi suporta `dtparam=watchdog=on` (algunes versions antigues no).
