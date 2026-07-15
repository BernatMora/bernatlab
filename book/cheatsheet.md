# BernatLab · Chuleta de comandes

Chuleta ràpida amb les 303 comandes més útils
extretes dels 7 mòduls del manual. Útil per imprimir o per tenir a mà
quan treballes a la RPi.

Versió web amb cerca i botons de copiar: [`book/cheatsheet.html`](./cheatsheet.html)

---

## Altres (25 comandes)

```│   Usuari bernat · SSH · tallafoc UFW opcional                │```
_Fonaments · Cap 1_

```sudo systemctl enable docker```
_Fonaments · Cap 2_

```sudo systemctl start docker```
_Fonaments · Cap 2_

```sudo systemctl stop docker```
_Fonaments · Cap 2_

```sudo systemctl restart docker```
_Fonaments · Cap 2_

```├── var/        → dades variables (logs, bases de dades, cues)```
_Fonaments · Cap 3_

```│   └── log/    → logs del sistema```
_Fonaments · Cap 3_

```chmod u+x script.sh      # afegeix execució al propietari```
_Fonaments · Cap 3_

```sudo apt install paquet          # instal·la un paquet```
_Fonaments · Cap 3_

```sudo apt remove paquet           # elimina un paquet```
_Fonaments · Cap 3_

```sudo apt autoremove              # elimina dependències innecessàries```
_Fonaments · Cap 3_

```ps aux                 # tots els processos```
_Fonaments · Cap 3_

```ps aux | grep docker    # processos que contenen "docker"```
_Fonaments · Cap 3_

```sudo apt install htop```
_Fonaments · Cap 3_

```└── docs/                        # documentació addicional```
_Fonaments · Cap 3_

```uptime                 # temps encès, càrrega```
_Fonaments · Cap 3_

```ps aux, htop, kill```
_Fonaments · Cap 3_

```sudo ufw status```
_Fonaments · Cap 4_

```sudo apt install ufw```
_Fonaments · Cap 4_

```sudo ufw default deny incoming```
_Fonaments · Cap 4_

```sudo ufw default allow outgoing```
_Fonaments · Cap 4_

```sudo ufw allow ssh```
_Fonaments · Cap 4_

```sudo ufw allow 9443/tcp    # Portainer```
_Fonaments · Cap 4_

```sudo ufw allow 3001/tcp    # Uptime Kuma```
_Fonaments · Cap 4_

```sudo ufw allow 3000/tcp    # Homepage```
_Fonaments · Cap 4_

## Cron (1 comandes)

```crontab -e```
_Seguretat · Cap 45_

## Còpies de seguretat (25 comandes)

```sudo apt install restic```
_Seguretat · Cap 45_

```brew install restic```
_Seguretat · Cap 45_

```restic init --repo /home/bernat/backups/bernatlab```
_Seguretat · Cap 45_

```restic -r /home/bernat/backups/bernatlab backup \```
_Seguretat · Cap 45_

```restic -r /home/bernat/backups/bernatlab snapshots```
_Seguretat · Cap 45_

```restic -r /home/bernat/backups/bernatlab restore latest --target /tmp/restored```
_Seguretat · Cap 45_

```restic -r /home/bernat/backups/bernatlab restore abc1234 --target /tmp/restored```
_Seguretat · Cap 45_

```restic -r /home/bernat/backups/bernatlab restore latest \```
_Seguretat · Cap 45_

```export RESTIC_REPOSITORY="/home/bernat/backups/bernatlab"```
_Seguretat · Cap 45_

```export RESTIC_PASSWORD_FILE="$HOME/.restic-password"```
_Seguretat · Cap 45_

```restic backup "${EXCLUDE_PATTERNS[@]}" "${BACKUP_PATHS[@]}"```
_Seguretat · Cap 45_

```restic forget \```
_Seguretat · Cap 45_

```0 3 * * * /home/bernat/scripts/backup_diari.sh >> /var/log/restic.log 2>&1```
_Seguretat · Cap 45_

```restic -r b2:bernatlab-backups:bernatlab init```
_Seguretat · Cap 45_

```restic -r b2:bernatlab-backups:bernatlab backup $HOME/bernatlab```
_Seguretat · Cap 45_

```restic -r s3:https://s3.wasabisys.com/bernatlab-backups init```
_Seguretat · Cap 45_

```restic -r rclone:gdrive:bernatlab-backups backup $HOME/bernatlab```
_Seguretat · Cap 45_

```restic backup /var/lib/docker/volumes/```
_Seguretat · Cap 45_

```restic -r /home/bernat/backups/bernatlab check```
_Seguretat · Cap 45_

```LATEST=$(restic -r "$REPO" snapshots --json | jq -r '.[0].time')```
_Seguretat · Cap 45_

```restic -r /mnt/usb/backups/bernatlab restore latest \```
_Seguretat · Cap 50_

```restic init --repo /home/bernat/backups```
_Hort Osona en acció · Cap 60_

```restic --repo /home/bernat/backups backup \```
_Hort Osona en acció · Cap 60_

```restic --repo /home/bernat/backups snapshots```
_Hort Osona en acció · Cap 60_

```restic -r ~/backups/bernatlab snapshots```
_Hort Osona en acció · Cap 69_

## Còpies i imatges (20 comandes)

```git add .```
_Fonaments · Cap 9_

```git remote add origin git@github.com:bernatmora/bernatlab.git```
_Fonaments · Cap 9_

```git remote add origin URL```
_Fonaments · Cap 9_

```git add directe.html css/directe.css js/directe.js sw.js```
_Dades operatives · Cap 21_

```BACKUP_DIR="/Users/bernat/backups/ollama"```
_IA local · Cap 39_

```sudo /usr/libexec/ApplicationFirewall/socketfilterfw --add /Applications/Ollama.app```
_IA local · Cap 41_

```mkdir -p /home/bernat/backups/bernatlab```
_Seguretat · Cap 45_

```borg init --encryption=repokey /home/bernat/backups/borg-repo```
_Seguretat · Cap 45_

```/home/bernat/backups/borg-repo::bernatlab-$(date +%Y%m%d) \```
_Seguretat · Cap 45_

```borg list /home/bernat/backups/borg-repo```
_Seguretat · Cap 45_

```borg extract /home/bernat/backups/borg-repo::bernatlab-20260708```
_Seguretat · Cap 45_

```sudo dd if=/dev/mmcblk0 of=/home/bernat/backups/sd-card.img bs=4M status=progress```
_Seguretat · Cap 45_

```gzip /home/bernat/backups/sd-card.img```
_Seguretat · Cap 45_

```borg check /home/bernat/backups/borg-repo```
_Seguretat · Cap 45_

```REPO="/home/bernat/backups/bernatlab"```
_Seguretat · Cap 45_

```AGE=$(stat -c %Y /var/lib/bernatlab-backups/latest)```
_Operativa 24/7 · Cap 53_

```- alert: BackupStale```
_Operativa 24/7 · Cap 53_

```ExecStart=/home/bernat/homelab/scripts/backup-daily.sh```
_Operativa 24/7 · Cap 54_

```sudo systemctl enable --now bernatlab-backup.timer```
_Operativa 24/7 · Cap 54_

```mkdir -p /home/bernat/backups```
_Hort Osona en acció · Cap 60_

## Docker (25 comandes)

```│   └── Docker Compose (fitxers a /home/bernat/homelab)         │```
_Fonaments · Cap 1_

```find / -name "docker-compose.yml"  # buscar un fitxer```
_Fonaments · Cap 3_

```├── docker-compose.yml           # definició principal de serveis```
_Fonaments · Cap 3_

```├── stacks/                      # sub-piles de compose```
_Fonaments · Cap 3_

```sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin```
_Fonaments · Cap 5_

```docker run hello-world```
_Fonaments · Cap 5_

```docker images                       # llista imatges locals```
_Fonaments · Cap 5_

```docker pull imatge:tag              # descarrega una imatge```
_Fonaments · Cap 5_

```docker rmi imatge                   # esborra una imatge```
_Fonaments · Cap 5_

```docker image prune                  # esborra imatges no usades```
_Fonaments · Cap 5_

```docker image prune -a               # esborra TOTES les imatges no usades```
_Fonaments · Cap 5_

```docker ps                           # contenidors actius```
_Fonaments · Cap 5_

```docker ps -a                        # tots els contenidors (inclosos aturats)```
_Fonaments · Cap 5_

```docker run -d --name web nginx      # crea i arrenca un contenidor```
_Fonaments · Cap 5_

```docker start nom                    # arrenca un contenidor existent```
_Fonaments · Cap 5_

```docker stop nom                     # atura un contenidor```
_Fonaments · Cap 5_

```docker restart nom                  # reinicia```
_Fonaments · Cap 5_

```docker rm nom                       # esborra un contenidor aturat```
_Fonaments · Cap 5_

```docker rm -f nom                    # forçar esborrat```
_Fonaments · Cap 5_

```docker logs nom                     # mostra logs```
_Fonaments · Cap 5_

```docker logs -f nom                  # logs en directe```
_Fonaments · Cap 5_

```docker exec -it nom bash            # obre una consola dins del contenidor```
_Fonaments · Cap 5_

```docker stats                        # ús de recursos en temps real```
_Fonaments · Cap 5_

```docker volume ls                    # llista volums```
_Fonaments · Cap 5_

```docker volume create nom            # crea un volum```
_Fonaments · Cap 5_

## Fitxers i editors (6 comandes)

```nano /etc/sudoers```
_Fonaments · Cap 3_

```nano, systemctl, journalctl```
_Fonaments · Cap 3_

```nano /home/bernat/homelab/data/homepage/services.yaml```
_Fonaments · Cap 9_

```nano services.yaml```
_Fonaments · Cap 9_

```cat ~/.ssh/bernatlab.pub | ssh bernat@hortosona "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"```
_Hort Osona en acció · Cap 60_

```nano ~/.ssh/config```
_Hort Osona en acció · Cap 60_

## Git (4 comandes)

```Homepage és la porta d'entrada visual al BernatLab. Ens permet organitzar tots els nostres serveis en una sola pàgina, amb informació en temps real. La configuració és totalment basada en fitxers, cosa que ens permet versionar-la amb Git. El socket de Docker, en mode lectura, ens permet accedir a informació dels contenidors. `HOMEPAGE_ALLOWED_HOSTS` és una de les variables clau per evitar errors. En el proper capítol veurem com versionar tota aquesta feina amb Git i com mantenir una bona documentació.```
_Fonaments · Cap 8_

```git pull```
_Fonaments · Cap 9_

```git init, git status, git add, git commit```
_Fonaments · Cap 9_

```git push, git pull```
_Fonaments · Cap 9_

## Grafana (25 comandes)

```│   ├── monitoring/              # Uptime Kuma, Grafana, etc.```
_Fonaments · Cap 3_

```git commit -m "Afegeix targeta Grafana a Homepage"```
_Fonaments · Cap 9_

```user grafana```
_Dades operatives · Cap 13_

```grafana:```
_Dades operatives · Cap 19_

```image: grafana/grafana:11.0```
_Dades operatives · Cap 19_

```container_name: grafana```
_Dades operatives · Cap 19_

```- /home/bernat/homelab/data/grafana:/var/lib/grafana```
_Dades operatives · Cap 19_

```- GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_ADMIN_PASSWORD}```
_Dades operatives · Cap 19_

```- /home/bernat/homelab/logs/grafana:/var/log/grafana```
_Dades operatives · Cap 22_

```├── Grafana (visualització)```
_LoRa · Cap 23_

```[Grafana]```
_LoRa · Cap 30_

```grafana/loki:2.9.0```
_Seguretat · Cap 49_

```grafana/promtail:2.9.0```
_Seguretat · Cap 49_

```container_cpu_usage_seconds_total{name="grafana"} 12.5```
_Operativa 24/7 · Cap 52_

```container_memory_usage_bytes{name="grafana"} 52428800```
_Operativa 24/7 · Cap 52_

```image: grafana/grafana:latest```
_Operativa 24/7 · Cap 52_

```- ./grafana/data:/var/lib/grafana```
_Operativa 24/7 · Cap 52_

```- ./grafana/provisioning:/etc/grafana/provisioning```
_Operativa 24/7 · Cap 52_

```- GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}```
_Operativa 24/7 · Cap 52_

```"grafana:3000"```
_Operativa 24/7 · Cap 54_

```grafana-data:```
_Operativa 24/7 · Cap 57_

```device: /mnt/ssd/grafana```
_Operativa 24/7 · Cap 57_

```│   ├── grafana.yml```
_Hort Osona en acció · Cap 61_

```[ Grafana ]    ← panell web amb gràfiques```
_Hort Osona en acció · Cap 63_

```- ./data/grafana:/var/lib/grafana```
_Hort Osona en acció · Cap 63_

## InfluxDB (25 comandes)

```│   ├── data/                    # InfluxDB, PostgreSQL, etc.```
_Fonaments · Cap 3_

```│   ├── monitoring/   → grafana, influxdb```
_Fonaments · Cap 6_

```influxdb:```
_Dades operatives · Cap 15_

```image: influxdb:2.7```
_Dades operatives · Cap 15_

```container_name: influxdb```
_Dades operatives · Cap 15_

```- /home/bernat/homelab/data/influxdb:/var/lib/influxdb2```
_Dades operatives · Cap 15_

```- /home/bernat/homelab/data/influxdb/config:/etc/influxdb2```
_Dades operatives · Cap 15_

```- DOCKER_INFLUXDB_INIT_MODE=setup```
_Dades operatives · Cap 15_

```- DOCKER_INFLUXDB_INIT_USERNAME=bernat```
_Dades operatives · Cap 15_

```- DOCKER_INFLUXDB_INIT_PASSWORD=ELMEUPASSWORD```
_Dades operatives · Cap 15_

```- DOCKER_INFLUXDB_INIT_ORG=bernatlab```
_Dades operatives · Cap 15_

```- DOCKER_INFLUXDB_INIT_BUCKET=hort-osona```
_Dades operatives · Cap 15_

```- DOCKER_INFLUXDB_INIT_RETENTION=8760h  # 1 any```
_Dades operatives · Cap 15_

```- DOCKER_INFLUXDB_INIT_ADMIN_TOKEN=ELMEUTOKENINICIAL```
_Dades operatives · Cap 15_

```from influxdb_client import InfluxDBClient```
_Dades operatives · Cap 15_

```from influxdb_client.client.write_api import SYNCHRONOUS```
_Dades operatives · Cap 15_

```client = InfluxDBClient(```
_Dades operatives · Cap 15_

```INFLUXD_BOLT_PATH=/var/lib/influxdb2/influxd.bolt```
_Dades operatives · Cap 15_

```INFLUXD_ENGINE_PATH=/var/lib/influxdb2/engine```
_Dades operatives · Cap 15_

```INFLUXD_QUERY_MEMORY_BYTES=536870912   # 512 MB```
_Dades operatives · Cap 15_

```INFLUXD_QUERY_MAX_BUCKETS=20```
_Dades operatives · Cap 15_

```influx backup /path/al/backup \```
_Dades operatives · Cap 15_

```influx restore /path/al/backup \```
_Dades operatives · Cap 15_

```influx backup /home/bernat/homelab/backup/influxdb-$(date +%F)```
_Dades operatives · Cap 15_

```influx bucket list --org bernatlab --token ELMEUTOKEN```
_Dades operatives · Cap 15_

## LoRa i sensors (3 comandes)

```Network Server (TTN o autoallotjat)```
_LoRa · Cap 23_

```│   ├── Sí → LoRaWAN (amb TTN o ChirpStack)```
_LoRa · Cap 25_

```client.publish("lora/gateway/raw", json.dumps(payload))```
_Hort Osona en acció · Cap 65_

## MQTT (25 comandes)

```│       ├── [pròxims: File Browser, Node-RED, Mosquitto, ...]   │```
_Fonaments · Cap 1_

```│   ├── iot/                     # Mosquitto, Node-RED, etc.```
_Fonaments · Cap 3_

```│   ├── iot/          → mosquitto, node-red```
_Fonaments · Cap 6_

```mosquitto_pub -h broker.local -t sensors/zona1/temperatura \```
_Dades operatives · Cap 12_

```mosquitto_pub -h 100.115.134.76 -t test -m "hola"```
_Dades operatives · Cap 12_

```mosquitto_sub -h 100.115.134.76 -t "sensors/#" -v```
_Dades operatives · Cap 12_

```mosquitto_pub -h BROKER -t TOPIC -m MISSATGE```
_Dades operatives · Cap 12_

```mosquitto_sub -h BROKER -t TOPIC -v```
_Dades operatives · Cap 12_

```mosquitto_pub -h BROKER -t TOPIC -m MISSATGE -q 1 -r```
_Dades operatives · Cap 12_

```│       ├── mosquitto.conf```
_Dades operatives · Cap 13_

```└── mosquitto/    (volum persistent)```
_Dades operatives · Cap 13_

```mosquitto:```
_Dades operatives · Cap 13_

```image: eclipse-mosquitto:2.0```
_Dades operatives · Cap 13_

```container_name: mosquitto```
_Dades operatives · Cap 13_

```- ./mosquitto.conf:/mosquitto/config/mosquitto.conf:ro```
_Dades operatives · Cap 13_

```- ./passwordfile:/mosquitto/config/passwordfile:ro```
_Dades operatives · Cap 13_

```- ./aclfile:/mosquitto/config/aclfile:ro```
_Dades operatives · Cap 13_

```- /home/bernat/homelab/data/mosquitto:/mosquitto/data```
_Dades operatives · Cap 13_

```- /home/bernat/homelab/data/mosquitto/log:/mosquitto/log```
_Dades operatives · Cap 13_

```persistence_location /mosquitto/data/```
_Dades operatives · Cap 13_

```log_dest file /mosquitto/log/mosquitto.log```
_Dades operatives · Cap 13_

```password_file /mosquitto/config/passwordfile```
_Dades operatives · Cap 13_

```acl_file /mosquitto/config/aclfile```
_Dades operatives · Cap 13_

```mosquitto_passwd -c passwordfile USUARI```
_Dades operatives · Cap 13_

```mosquitto_passwd -b passwordfile USUARI CONTRASENYA```
_Dades operatives · Cap 13_

## Paquets (apt) (6 comandes)

```apt update && apt upgrade```
_Fonaments · Cap 3_

```apt install, apt remove```
_Fonaments · Cap 3_

```apt install mosquitto-clients```
_Dades operatives · Cap 12_

```apt update```
_Operativa 24/7 · Cap 54_

```apt upgrade -y```
_Operativa 24/7 · Cap 54_

```apt autoremove -y```
_Operativa 24/7 · Cap 54_

## Prometheus (21 comandes)

```prometheus:```
_Operativa 24/7 · Cap 52_

```image: prom/prometheus:latest```
_Operativa 24/7 · Cap 52_

```container_name: prometheus```
_Operativa 24/7 · Cap 52_

```- ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml```
_Operativa 24/7 · Cap 52_

```- ./prometheus/data:/prometheus```
_Operativa 24/7 · Cap 52_

```- '--config.file=/etc/prometheus/prometheus.yml'```
_Operativa 24/7 · Cap 52_

```- '--storage.tsdb.path=/prometheus'```
_Operativa 24/7 · Cap 52_

```- '--web.console.libraries=/usr/share/prometheus/console_libraries'```
_Operativa 24/7 · Cap 52_

```- '--web.console.templates=/usr/share/prometheus/consoles'```
_Operativa 24/7 · Cap 52_

```- prometheus```
_Operativa 24/7 · Cap 52_

```- job_name: prometheus```
_Operativa 24/7 · Cap 52_

```- name: Prometheus```
_Operativa 24/7 · Cap 52_

```type: prometheus```
_Operativa 24/7 · Cap 52_

```url: http://prometheus:9090```
_Operativa 24/7 · Cap 52_

```- ./prometheus/alertmanager.yml:/etc/alertmanager/alertmanager.yml```
_Operativa 24/7 · Cap 53_

```amtool silence add --alertmanager=http://localhost:9093 \```
_Operativa 24/7 · Cap 53_

```"prometheus:9090"```
_Operativa 24/7 · Cap 54_

```- ./prometheus/rules.yml:/etc/prometheus/rules.yml```
_Hort Osona en acció · Cap 67_

```- ./data/prometheus:/prometheus```
_Hort Osona en acció · Cap 67_

```expr: up{job=~"cadvisor|prometheus"} == 0```
_Hort Osona en acció · Cap 67_

```from prometheus_client import start_http_server, Gauge```
_Hort Osona en acció · Cap 67_

## Python (7 comandes)

```pip install chromadb```
_IA local · Cap 36_

```pip install -r requirements.txt  # fastapi, uvicorn, chromadb, requests```
_IA local · Cap 38_

```pip install faster-whisper```
_IA local · Cap 40_

```pip install openai-whisper```
_IA local · Cap 40_

```pip install piper-tts```
_IA local · Cap 40_

```pip install TTS```
_IA local · Cap 40_

```pip install gitleaks```
_Seguretat · Cap 46_

## SSH i accés remot (20 comandes)

```ssh bernat@100.115.134.76```
_Fonaments · Cap 1_

```ssh-keygen -t ed25519 -C "bernat@bernatlab"```
_Fonaments · Cap 4_

```ssh-copy-id bernat@100.115.134.76```
_Fonaments · Cap 4_

```ssh bernat@hortosona```
_Fonaments · Cap 4_

```ssh -i ~/.ssh/id_ed25519 bernat@100.115.134.76```
_Fonaments · Cap 4_

```ssh-keygen -t ed25519```
_Fonaments · Cap 4_

```ssh-copy-id bernat@hortosona```
_Fonaments · Cap 4_

```ssh-keygen -t ed25519 -C "bernat@bernat-mbp" -f ~/.ssh/bernatlab```
_Seguretat · Cap 46_

```ssh-copy-id -i ~/.ssh/bernatlab.pub bernat@hortosona```
_Seguretat · Cap 46_

```sudo systemctl restart sshd```
_Seguretat · Cap 46_

```ssh-add ~/.ssh/bernatlab```
_Seguretat · Cap 46_

```sudo systemctl edit sshd```
_Seguretat · Cap 47_

```ExecStart=/usr/sbin/sshd -D -i -e -f /etc/ssh/sshd_config```
_Seguretat · Cap 47_

```sudo fail2ban-client status sshd```
_Seguretat · Cap 47_

```sudo fail2ban-client set sshd unbanip 1.2.3.4```
_Seguretat · Cap 47_

```sudo fail2ban-client set sshd banip 1.2.3.4```
_Seguretat · Cap 47_

```journalctl -u sshd```
_Seguretat · Cap 49_

```journalctl -u sshd -n 100```
_Operativa 24/7 · Cap 56_

```ssh -i ~/.ssh/bernatlab bernat@hortosona```
_Hort Osona en acció · Cap 60_

```ssh-add --apple-use-keychain ~/.ssh/bernatlab```
_Hort Osona en acció · Cap 60_

## Seguretat i tallafocs (7 comandes)

```sudo apt install fail2ban```
_Seguretat · Cap 47_

```sudo systemctl status fail2ban```
_Seguretat · Cap 47_

```sudo fail2ban-client status```
_Seguretat · Cap 47_

```sudo tail -f /var/log/fail2ban.log```
_Seguretat · Cap 47_

```description: "Més de 10 intents fallits en 5 minuts. IP bloquejada per fail2ban."```
_Seguretat · Cap 49_

```sudo nano /etc/fail2ban/jail.local```
_Hort Osona en acció · Cap 60_

```sudo systemctl restart fail2ban```
_Hort Osona en acció · Cap 60_

## Tailscale (5 comandes)

```sudo ufw allow in on tailscale0  # permet tot des de Tailscale```
_Seguretat · Cap 47_

```sudo ufw allow in on tailscale0 to any port 22```
_Seguretat · Cap 47_

```sudo ufw allow in on tailscale0 to any port 9443  # Portainer```
_Seguretat · Cap 47_

```sudo ufw allow in on tailscale0 to any port 3000  # Homepage```
_Seguretat · Cap 47_

```sudo ufw allow in on tailscale0 to any port 3001  # Uptime Kuma```
_Seguretat · Cap 47_

## Telegram (4 comandes)

```url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"```
_Operativa 24/7 · Cap 53_

```send_telegram "⚠️ Còpia no s'ha executat avui"```
_Operativa 24/7 · Cap 54_

```f"https://api.telegram.org/bot{TOKEN}/sendMessage",```
_Hort Osona en acció · Cap 66_

```f"https://api.telegram.org/bot{os.environ['TELEGRAM_TOKEN']}/sendMessage",```
_Hort Osona en acció · Cap 67_

## Xarxa (curl, wget) (24 comandes)

```curl -fsSL https://tailscale.com/install.sh | sh```
_Fonaments · Cap 4_

```curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg```
_Fonaments · Cap 5_

```curl -i -XPOST "http://100.115.134.76:8086/api/v2/write?org=bernatlab&bucket=hort-osona" \```
_Dades operatives · Cap 15_

```curl -H "X-API-Key: CLAU" http://100.115.134.76:8000/zones```
_Dades operatives · Cap 20_

```curl -H "X-API-Key: CLAU" http://100.115.134.76:8000/zones/zona-tomateres/latest```
_Dades operatives · Cap 20_

```curl -H "X-API-Key: CLAU" https://api.bernatlab.cat/zones```
_Dades operatives · Cap 21_

```curl -X POST "https://api.telegram.org/bot$BOT_TOKEN/sendMessage" \```
_Dades operatives · Cap 22_

```curl -s http://100.115.134.76:3001/ | grep -q "concentratord" && echo "Gateway OK" || echo "Gateway FALL"```
_LoRa · Cap 32_

```curl -fsSL https://ollama.com/install.sh | sh```
_IA local · Cap 34_

```curl http://localhost:11434/api/generate -d '{```
_IA local · Cap 34_

```curl http://<mac-tailscale-ip>:11434/api/tags```
_IA local · Cap 34_

```curl http://localhost:11434/api/embeddings -d '{```
_IA local · Cap 36_

```curl http://<mac-tailscale-ip>:8080/api/estadistiques```
_IA local · Cap 38_

```curl http://localhost:11434/api/tags```
_IA local · Cap 39_

```curl http://localhost:11434/api/chat -d '{```
_IA local · Cap 39_

```curl -X POST http://localhost:3001/api/monitors \```
_IA local · Cap 39_

```wget https://huggingface.co/rhasspy/piper-voices/resolve/main/ca/ca_ES/voice.json```
_IA local · Cap 40_

```wget https://huggingface.co/rhasspy/piper-voices/resolve/main/ca/ca_ES/voice.onnx```
_IA local · Cap 40_

```curl http://100.115.134.76:8080```
_Seguretat · Cap 44_

```curl -X POST "https://api.telegram.org/bot$TELEGRAM_TOKEN/sendMessage" \```
_Seguretat · Cap 45_

```curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendMessage" \```
_Operativa 24/7 · Cap 54_

```curl http://localhost:<port>```
_Operativa 24/7 · Cap 56_

```curl -fsSL https://get.docker.com -o get-docker.sh```
_Hort Osona en acció · Cap 61_

```curl -X POST "https://api.telegram.org/bot<TOKEN>/sendMessage" \```
_Hort Osona en acció · Cap 66_

## systemd (25 comandes)

```systemctl status docker```
_Fonaments · Cap 2_

```systemctl list-units --type=service --state=running```
_Fonaments · Cap 2_

```systemctl status servei          # estat detallat```
_Fonaments · Cap 3_

```systemctl start servei           # iniciar```
_Fonaments · Cap 3_

```systemctl stop servei            # aturar```
_Fonaments · Cap 3_

```systemctl restart servei         # reiniciar```
_Fonaments · Cap 3_

```systemctl reload servei          # recarregar config sense parar```
_Fonaments · Cap 3_

```systemctl enable servei          # arrencar a l'inici```
_Fonaments · Cap 3_

```systemctl disable servei         # no arrencar a l'inici```
_Fonaments · Cap 3_

```systemctl is-active servei       # actiu? (yes/no)```
_Fonaments · Cap 3_

```systemctl is-enabled servei      # habilitat? (yes/no)```
_Fonaments · Cap 3_

```systemctl list-unit-files --type=service```
_Fonaments · Cap 3_

```journalctl -u servei                  # tots els logs```
_Fonaments · Cap 3_

```journalctl -u servei -f               # en directe (follow)```
_Fonaments · Cap 3_

```journalctl -u servei --since "1 hour ago"```
_Fonaments · Cap 3_

```journalctl -u servei --since today```
_Fonaments · Cap 3_

```journalctl -xe           # últims missatges amb explicacions```
_Fonaments · Cap 3_

```journalctl --since "1 hour ago"```
_Fonaments · Cap 3_

```journalctl -xe```
_Fonaments · Cap 3_

```systemctl status servei```
_Fonaments · Cap 3_

```systemctl restart servei```
_Fonaments · Cap 3_

```journalctl -u ssh --since "1 month ago"```
_Dades operatives · Cap 22_

```journalctl --since today```
_Seguretat · Cap 49_

```journalctl -p err```
_Seguretat · Cap 49_

```journalctl -f```
_Seguretat · Cap 49_
