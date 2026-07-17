# Xuleta de comandes del curs del BernatLab

> Totes les comandes que apareixen als 77 capitols del curs, organitzades per categoria.

## Docker i contenidors

```
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```
```
docker images
```
```
docker volume ls
```
```
docker network ls
```
```
[enganxa la sortida de docker ps]
```
```
│  │9443 │  │3001 │  │3000  │ │     Docker
```
```
echo "Contenidors actius: $(docker ps -q | wc -l)"
```
```
5. Serveis i contenidors Docker
```
```
mkdir -p homelab/{docker,config,notes,scripts,logs,backups}
```
```
echo "Contenidors actius: $(docker ps -q 2>/dev/null | wc -l)"
```
```
mkdir docker              # Crea carpeta
```
```
curl -fsSL https://get.docker.com -o get-docker.sh
```
```
sudo sh get-docker.sh
```
```
sudo usermod -aG docker bernat
```
```
newgrp docker
```
```
docker --version
```
```
docker compose version
```
```
docker run hello-world
```
```
docker run -d --name prova-nginx -p 8080:80 nginx:alpine
```
```
docker ps
```
```
docker exec -it prova-nginx sh
```
```
docker logs prova-nginx
```
```
docker logs -f prova-nginx  # Ctrl+C per sortir
```
```
docker stats prova-nginx
```
```
docker stop prova-nginx
```
```
docker rm prova-nginx
```
```
docker volume create dades-prova
```
```
docker run -d --name writer -v dades-prova:/dades alpine sh -c "while true; do date >> /dades/log.txt; sleep 5; done"
```
```
docker exec writer cat /dades/log.txt
```
```
docker volume inspect dades-prova | grep Mountpoint
```

## Git

```
git config --global user.name "Bernat Mora"
```
```
git config --global user.email "bernat@hortosona.local"
```
```
git config --global init.defaultBranch main
```
```
git config --global core.editor nano
```
```
git init
```
```
git status
```
```
git add .
```
```
git diff scripts/info-rpi.sh
```
```
git add scripts/info-rpi.sh
```
```
git commit -m "Afegeix script info-rpi.sh per veure estat del sistema"
```
```
git diff
```
```
git branch experiment-rpi-zero
```
```
git checkout experiment-rpi-zero
```
```
git commit -m "Afegeix versio del kernel a info-rpi.sh"
```
```
git log --oneline --all
```
```
git checkout main
```
```
git merge experiment-rpi-zero
```
```
git branch -d experiment-rpi-zero
```
```
git diff --staged
```
```
git add config/homepage/services.yaml
```
```
git commit -m "Afegeix PiHole al servei de xarxa"
```
```
git push origin main
```
```
git log
```
```
git log --oneline
```
```
git log --graph --oneline --all
```
```
git show <commit-hash>
```
```
git revert <commit-hash>      # crea un commit que desfà
```
```
git reset --hard <commit-hash>  # PERILLÓS: esborra commits
```
```
git checkout -- fitxer.txt     # descartar canvis locals
```
```
git branch                          # llista
```

## SSH

```
ssh bernat@hortosona
```
```
ssh bernat@100.115.134.76
```
```
lscpu | head -20
```
```
sudo journalctl -u ssh --since "1 hour ago" | tail -20
```
```
sudo journalctl -u ssh -f
```
```
sudo journalctl -u ssh | grep -c "Failed"
```
```
sudo systemctl restart ssh         # reinicia el servei SSH
```
```
sudo systemctl status ssh        # estat d'un servei
```
```
sudo systemctl start ssh         # arrenca'l
```
```
sudo systemctl stop ssh          # para'l
```
```
sudo systemctl restart ssh       # reinicia'l
```
```
sudo systemctl enable ssh        # arrenca automàticament en boot
```
```
sudo systemctl disable ssh       # NO arrenqui en boot
```
```
sudo journalctl -u ssh --since today    # logs d'un servei des d'avui
```
```
sudo journalctl -u ssh -f               # segueix els logs en temps real (tail -f)
```
```
ssh-keygen -t ed25519 -C "bernat@portatil-2026"
```
```
ssh-keygen -lf ~/.ssh/id_ed25519.pub
```
```
type $env:USERPROFILE\.ssh\id_ed25519.pub | ssh bernat@hortosona "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
```
```
cat ~/.ssh/id_ed25519.pub | ssh bernat@hortosona "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
```
```
ssh hortosona "echo funciona; uptime"
```
```
sudo nano /etc/ssh/sshd_config
```
```
sudo sshd -t
```
```
ssh bernat@hortosona "echo agent funciona"
```
```
ssh -L 9999:localhost:9000 bernat@hortosona -N
```
```
ssh bernat@192.168.1.50
```
```
ssh-keygen -t ed25519 -C "bernat@portatil"
```
```
- ssh bernat@hortosona
```
```
- Configuracio SSH amb claus
```
```
- SSH (22) - accés remot
```
```
rsync -avz --delete -e ssh "$ORIGEN" "$DESTI"
```

## Linux i sistema

```
cat /etc/os-release | head -5
```
```
ip -4 addr show | grep inet
```
```
cat /sys/firmware/devicetree/base/model
```
```
cat /proc/cpuinfo | grep Serial
```
```
cat /proc/cpuinfo | grep Revision
```
```
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq 2>/dev/null
```
```
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_max_freq
```
```
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
```
```
dmidecode -t memory 2>/dev/null | head -10 || cat /proc/meminfo | head -5
```
```
mount | grep "on / "
```
```
sudo hdparm -Tt /dev/mmcblk0
```
```
cat /sys/class/thermal/thermal_zone0/temp | awk '{print $1/1000 "C"}'
```
```
sudo ethtool eth0 | grep Speed
```
```
sudo apt install -y stress
```
```
echo "CPU freq: $(cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq)"
```
```
echo "RAM lliure: $(free -h | grep Mem | awk '{print $4}')"
```
```
4. systemd (primer procés, PID 1)
```
```
cd ~
```
```
ls -la homelab/
```
```
tree homelab/ 2>/dev/null || find homelab/ -type d
```
```
cd homelab
```
```
cat README.md
```
```
cd ..
```
```
cd /home/bernat/homelab
```
```
cd ~/homelab/scripts
```
```
ls -l hola.sh
```
```
chmod +x hola.sh
```
```
chmod 600 secret.txt
```
```
ls -l secret.txt
```
```
chmod 770 ~/homelab/compartit
```

## Xarxa

```
- Tailscale: [sí/no]
```
```
│       Tailscale       │   ← VPN privada,
```
```
ip addr show
```
```
tailscale ip -4 2>/dev/null
```
```
stress --cpu 4 --timeout 60
```
```
echo "IP Tailscale: $(tailscale ip -4 2>/dev/null || echo 'Tailscale no actiu')"
```
```
less /var/log/kern.log          # log del kernel
```
```
tailscale status 2>/dev/null || echo "No instal·lat"
```
```
curl -fsSL https://tailscale.com/install.sh | sh
```
```
tailscale ip -4
```
```
tailscale status
```
```
tailscale.exe status
```
```
ping 100.115.134.76
```
```
ping hortosona
```
```
ping 100.115.134.76         # a ella mateixa
```
```
ping 8.8.8.8                # a Internet (DNS de Google)
```
```
curl -I https://google.com  # test HTTPS
```
```
curl http://localhost:8080
```
```
curl http://localhost:8082
```
```
curl http://localhost:8083
```
```
curl http://localhost:8080   # whoami
```
```
curl http://localhost:8084
```
```
RUN apk add --no-cache curl
```
```
echo "IP del contenidor: $(hostname -i 2>/dev/null || echo 'desconeguda')"
```
```
curl http://hortosona:8080
```
```
- IP Tailscale: 100.115.134.76
```
```
3. Instal·lar Tailscale
```
```
Tailscale. MagicDNS, configuracio automatica, gratuit fins a 100 dispositius.
```
```
4. Configura Tailscale
```
```
**Decisio**: Tailscale.
```

## Monitoritzacio

```
uptime -p
```
```
- Uptime Kuma: [sí/no]
```
```
- Uptime: [de uptime -p]
```
```
- Monitors Uptime Kuma actius: [X de Y verds]
```
```
echo "Uptime: $(uptime -p)"
```
```
uptime:
```
```
image: louislam/uptime-kuma:latest
```
```
container_name: uptime-kuma
```
```
- uptime_data:/app/data
```
```
uptime_data:
```
```
uptime-kuma:
```
```
- Uptime Kuma:
```
```
icon: uptime-kuma
```
```
uptime: true
```
```
uptimekuma:
```
```
nano ~/homelab/config/homepage/uptimekuma.yaml
```
```
type: uptime-kuma
```
```
url: http://uptime-kuma:3001
```
```
- Grafana:
```
```
icon: grafana
```
```
- Uptime Kuma (port 3001): http://hortosona:3001
```
```
- Serveis: Portainer, Uptime Kuma, Homepage, Whoami
```
```
│   └── uptime-kuma/       (configuració, opcional)
```
```
- [Uptime Kuma](http://hortosona:3001)
```
```
- Status Page pública a Uptime Kuma
```
```
- Uptime Kuma (3001) - monitoratge
```
```
4. Grafana (M4) - per visualitzar dades
```
```
Hi ha 4 sectors amb sensors. Vull veure les dades a Grafana.
```
```
|Grafana |
```
```
[Portainer 9000] [Uptime Kuma 3001] [File Browser 8082]
```

## MQTT

```
│  │Dockr│  │Tails│  │MQTT  │ │   ← Infra
```
```
| MQTT  +-->+InfluxDB|
```
```
--include /home/pi/bernatlab/configs/mosquitto.conf
```
```
"""Servei que llegeix MiFlora i publica a MQTT cada 15 min."""
```
```
import paho.mqtt.client as mqtt
```
```
c = mqtt.Client("miflora-gateway", clean_session=False)
```
```
c.username_pw_set(CFG["mqtt"]["user"], CFG["mqtt"]["pass"])
```
```
c.connect(CFG["mqtt"]["host"], CFG["mqtt"]["port"], 60)
```
```
mqtt_client = build_client()
```
```
mqtt_client.publish(topic, payload, qos=1)
```
```
mqtt:
```
```
mosquitto_sub -h localhost -t "hort-osona/miflora/#" -v
```
```
After=network.target bluetooth.target mosquitto.service
```
```
Wants=mosquitto.service
```
```
client = mqtt.Client("miflora-gateway")
```
```
mqtt_client = mqtt.Client("lora-gateway")
```
```
mqtt_client.connect("localhost", 1883)
```
```
mqtt_client.publish(topic, json.dumps(data), qos=1)
```
```
mosquitto_sub -h localhost -t "hort-osona/lora/#" -v
```
```
import json, paho.mqtt.client as mqtt
```
```
mosquitto/
```
```
mosquitto.conf
```
```
mqtt_to_influxdb.py
```
```
persistence_location /mosquitto/data/
```
```
password_file /mosquitto/config/passwd
```
```
sh -c "mosquitto_passwd -c -b /tmp/passwd hort-osona secretpass"
```
```
mosquitto:
```
```
image: eclipse-mosquitto:2
```
```
container_name: hort-mosquitto
```
```
- ./mosquitto/config:/mosquitto/config
```

## Backups

```
rsync -a /home/pi/dades/ /backup/daily.0/
```
```
rsync -a --link-dest=/backup/daily.0 /home/pi/dades/ /backup/daily.1/
```
```
restic -r b2:bernatlab-backup:/ backup /home/pi/dades
```
```
restic version
```
```
mkdir -p /tmp/prova-restic/dades
```
```
mkdir -p /tmp/prova-restic/repo
```
```
export RESTIC_PASSWORD="prova-1234-bona"
```
```
restic -r /tmp/prova-restic/repo init
```
```
restic -r /tmp/prova-restic/repo backup /tmp/prova-restic/dades
```
```
restic -r /tmp/prova-restic/repo snapshots
```
```
echo "Nou fitxer" > /tmp/prova-restic/dades/nou-1.txt
```
```
mkdir -p /tmp/prova-restic/restaurat
```
```
restic -r /tmp/prova-restic/repo restore latest \
```
```
--target /tmp/prova-restic/restaurat \
```
```
--include /tmp/prova-restic/dades/gran-1.bin
```
```
echo "iteracio $i - $(date)" > /tmp/prova-restic/dades/iteracio-$i.txt
```
```
restic -r /tmp/prova-restic/repo backup /tmp/prova-restic/dades > /dev/null
```
```
restic -r /tmp/prova-restic/repo forget --keep-daily 3 --prune
```
```
restic -r /mnt/ssd-backup/bernatlab init
```
```
restic -r /mnt/ssd-backup/bernatlab backup \
```
```
restic -r /mnt/ssd-backup/bernatlab snapshots
```
```
restic -r /mnt/ssd-backup/bernatlab restore latest \
```
```
restic -r /mnt/ssd-backup/bernatlab forget \
```
```
rsync -av --delete /home/pi/dades/ /mnt/ssd-backup/dades/
```
```
rsync -avn /home/pi/bernatlab/proves/sync/origen/ /home/pi/bernatlab/proves/sync/desti/
```
```
rsync -av /home/pi/bernatlab/proves/sync/origen/ /home/pi/bernatlab/proves/sync/desti/
```
```
rsync -av --delete /home/pi/bernatlab/proves/sync/origen/ /home/pi/bernatlab/proves/sync/desti/
```
```
rsync -av /origen/ /desti/
```
```
rsync -av --delete /home/pi/bernatlab/ /mnt/ssd-backup/bernatlab/
```
```
rsync -avn --delete /home/pi/bernatlab/ /mnt/ssd-backup/bernatlab/
```

## Seguretat

```
- Homepage (port 3010): http://hortosona:3010
```
```
- Homepage (3010) - dashboard
```
```
[Homepage 3010]
```
```
trivy image nginx:alpine
```
```
trivy image --severity HIGH,CRITICAL nginx:alpine
```
```
gpg --symmetric --cipher-algo AES256 config-backup.tar.gz
```
```
gpg --symmetric --cipher-algo AES256 backup.tar.gz
```
```
gpg -d backup.tar.gz.gpg > backup.tar.gz
```
```
CONTAINER   CPU %   MEM USAGE / LIMIT   MEM %   NET I/O           BLOCK I/O   PIDS
```
```
age --version
```
```
gpg --version
```
```
age -r "$PUBKEY" -o secrets.txt.age secrets.txt
```
```
age -d -i age-key.txt -o secrets-restored.txt secrets.txt.age
```
```
age -p -o notes.age notes.txt
```
```
age -d -o notes-restored.txt notes.age
```
```
echo "un altre secret" > gpg-test.txt
```
```
gpg --symmetric --batch --passphrase "test-2025" -o gpg-test.txt.gpg gpg-test.txt
```
```
file gpg-test.txt.gpg
```
```
gpg --batch --passphrase "test-2025" -o gpg-restored.txt gpg-test.txt.gpg
```
```
age -r "$PUBKEY" -o "$FITXER.age" "$FITXER"
```
```
gpg --full-generate-key
```
```
gpg --list-keys
```
```
gpg --decrypt fitxer.txt.gpg > fitxer.txt
```
```
gpg --symmetric fitxer.txt
```
```
age -r age1ql3z7hjy54pw3hyww5ayyfg7zqgvc7w3j2elw8zmrj2vn5... \
```
```
-o secrets.txt.age secrets.txt
```
```
age -d -i key.txt -o secrets-restored.txt secrets.txt.age
```
```
age -p -o secrets.txt.age secrets.txt
```
```
age -d -o secrets-restored.txt secrets.txt.age
```
```
Critica: "Molt bon llibre, l'he gaudit"
```

## Intel·ligencia artificial

```
mkdir -p ~/bernatlab-exercicis/M4/01-llm
```
```
python3 manual_llm.py
```
```
ollama --version
```
```
Environment="OLLAMA_MODELS=/mnt/dades/ollama-models"
```
```
ollama list
```
```
ollama pull llama3.2:1b
```
```
ollama pull llama3.2:3b
```
```
ollama run llama3.2:1b
```
```
Environment="OLLAMA_HOST=0.0.0.0:11434"
```
```
Environment="OLLAMA_KEEP_ALIVE=10m"
```
```
ollama pull gemma2:2b
```
```
ollama pull phi3:mini
```
```
Mar 15 20:15:00 rpi ollama[3456]: [GIN] 2024/03/15 20:15:00 | 200 |    1.2s |  127.0.0.1 | POST     "/api/generate"
```
```
ollama pull nomic-embed-text
```
```
import ollama
```
```
embeddings = []
```
```
response = ollama.embeddings(model='nomic-embed-text', prompt=chunk)
```
```
emb = response['embedding']
```
```
embeddings.append(np.array(emb))
```
```
print(f"\nTotal: {len(embeddings)} vectors de {len(embeddings[0])} dimensions")
```
```
python embeddings.py
```
```
from embeddings import embeddings
```
```
emb_pregunta = np.array(ollama.embeddings(model='nomic-embed-text', prompt=pregunta)['embedding'])
```
```
sims = [cosine_similarity(emb_pregunta, emb) for emb in embeddings]
```
```
response = ollama.chat(model='llama3.2:3b', messages=[
```
```
Documents -> Chunks -> Embeddings -> Vector DB
```
```
Pregunta -> Embedding -> Cerca a Vector DB -> Top-K chunks
```
```
Pregunta + Chunks rellevants -> LLM -> Resposta
```
```
}' | python3 -c "import json,sys; d=json.load(sys.stdin); print('Dimensions:', len(d['embedding'])); print('Primers 5 valors:', d['embedding'][:5])"
```
```
def embedding(text):
```

## Sensors i hort

```
- Temperatura CPU: [de vcgencmd]
```
```
- Temperatura sota càrrega: [de l'apartat 5]
```
```
sensors 2>/dev/null || echo "Paquet lm-sensors no instal·lat"
```
```
echo "Temperatura: $(vcgencmd measure_temp)"
```
```
echo "Temperatura: $(vcgencmd measure_temp 2>/dev/null)"
```
```
- [ ] Comprar sensor temperatura hort
```
```
- Raspberry Pi Zero per posar al camp com a gateway LoRa.
```
```
- 4 sensors LoRa de temperatura + humitat.
```
```
| Sensors  +---->+ Gateway+--+  | ChirpStack|
```
```
| LoRa     |     | LoRa   |  |  | (broker)  |
```
```
- [ ] M5 - Tinc sensors al camp
```
```
M5 (IoT) ............... LoRaWAN, sensors, Hort Osona
```
```
CREATE TABLE sensors (
```
```
INSERT INTO sensors (nom, valor) VALUES
```
```
('temperatura', 22.5),
```
```
('humitat', 65.0),
```
```
CREATE INDEX idx_sensor_ts ON sensors(sensor, ts);
```
```
INSERT INTO sensors (sensor, valor) VALUES
```
```
('temperatura', 23.0),
```
```
('humitat', 64.0);
```
```
SELECT * FROM sensors;
```
```
SELECT * FROM sensors WHERE sensor = 'temperatura';
```
```
SELECT sensor, AVG(valor) FROM sensors GROUP BY sensor;
```
```
SELECT COUNT(*) FROM sensors;
```
```
FROM sensors
```
```
sqlite3 /home/pi/bernatlab/proves/hivernacle.db "SELECT COUNT(*) FROM sensors;"
```
```
"INSERT INTO sensors (sensor, valor) VALUES (?, ?)",
```
```
('temperatura', 22.7)
```
```
SELECT * FROM sensors
```
```
WHERE sensor = 'temperatura'
```

## Altres

```
uname -a
```
```
df -h /
```
```
free -h
```
```
vcgencmd measure_temp 2>/dev/null || echo "No tens vcgencmd"
```
```
htop
```
```
yes > /dev/null &
```
```
vcgencmd measure_temp
```
```
killall yes
```
```
- IP: [100.115.134.76]
```
```
- Puc entrar per SSH: [sí/no]
```
```
- Mètode (clau vs contrasenya): [què uso]
```
```
- Homepage: [sí/no]
```
```
- Portainer: [sí/no]
```
```
- SO: [la sortida de /etc/os-release]
```
```
- Nucli: [la sortida de uname -a]
```
```
- Disc lliure: [de df -h]
```
```
- RAM lliure: [de free -h]
```
```
- Monitors que fallen: [quina i per què]
```
```
[Cosa que no funcioni, coses que vegis estranyes, etc.]
```
```
┌─────────────────────────────────────────────────────────┐
```
```
│                      Internet                            │
```
```
└────────────────────────┬────────────────────────────────┘
```
```
│
```
```
▼
```
```
┌──────────────────────┐
```
```
│   (100.x.x.x IPs)     │     sense obrir
```
```
│                       │     ports al router
```
```
└──────────┬───────────┘
```
```
┌──────────────────────────────┐
```
```
│   Raspberry Pi 4 (4 GB RAM)  │
```
