# El meu primer dia amb la Raspberry Pi

> Guia practica per posar en marxa un servidor personal BernatLab en una tarda. De RPi acabada de comprar fins a tenir serveis funcionant.

## Que necessites

### Maquinari (~200 EUR total)

- Raspberry Pi 4 Model B (4 GB RAM) — ~70 EUR
- Targeta microSD 32 GB Clase 10 — ~10 EUR
- Alimentador USB-C 5V/3A oficial — ~12 EUR
- Carcasa amb dissipadors — ~10 EUR
- Cable Ethernet Cat 6 (1-2 m) — ~5 EUR
- Monitor + cable micro-HDMI (per a la primera configuracio) — opcional si tens accés per SSH
- Teclat + ratoli USB — opcional per a la primera configuracio

### Programari

- **Raspberry Pi Imager** (des de https://www.raspberrypi.com/software/)
- **SSH client** (PowerShell a Windows ja en te un)
- **Tailscale** (al final de la guia)

## Temps estimat

| Fase | Durada | Dificultat |
|---|---|---|
| 1. Flashejar la microSD | 10 min | Facil |
| 2. Primera arrencada | 10 min | Facil |
| 3. Configurar xarxa | 15 min | Facil |
| 4. Actualitzacio inicial | 20 min | Facil |
| 5. Instal·lar Docker | 10 min | Mitjana |
| 6. Instal·lar Portainer | 10 min | Facil |
| 7. Instal·lar Uptime Kuma | 5 min | Facil |
| 8. Instal·lar Homepage | 5 min | Facil |
| 9. Configurar Tailscale | 15 min | Mitjana |
| 10. Verificar-ho tot | 10 min | Facil |
| **TOTAL** | **~2 hores** | **Facil-Mitjana** |

---

## Fase 1: Flashejar la microSD (10 min)

### A. Descarrega Raspberry Pi Imager

1. Ves a https://www.raspberrypi.com/software/
2. Descarrega la versio per al teu sistema (Windows / Mac / Linux).
3. Instal·la'l.

### B. Selecciona el sistema operatiu

1. Obre Raspberry Pi Imager.
2. Click a **"Choose OS"**.
3. Tria **"Raspberry Pi OS (other)"** → **"Raspberry Pi OS Lite (64-bit)"**.
   - "Lite" perque no volem escriptor ni navegador.
   - "64-bit" perque la RPi 4 ho suporta.

### C. Selecciona la targeta

1. Click a **"Choose Storage"**.
2. Tria la teva targeta microSD.

### D. Preconfigura (important!)

Click a la **icona de la rodeta** (o prem `Ctrl+Shift+X`):

1. **Hostname**: `hortosona` (o el que vulguis, pero consistent).
2. **Enable SSH**: activa.
3. **Set username and password**: posa `bernat` i una **contrasenya forta** (despres la canviaras).
4. **Configure wireless**: pots posar-la ometre si fas servir Ethernet.
5. **Set locale settings**: posa el teu fus horari.
6. **Enable telemetry**: NO.
7. Click **SAVE**.

### E. Escriu

1. Click **"WRITE"**.
2. Espera 5-10 minuts.
3. Quan acabi, treu la targeta.

---

## Fase 2: Primera arrencada (10 min)

### A. Insereix la microSD a la RPi

1. Apaga la RPi.
2. Insereix la microSD.
3. Connecta el cable Ethernet al router.
4. Connecta el monitor i teclat (només per a la primera arrencada).
5. Endolla l'alimentacio.

### B. Arrenca

1. La RPi arrencara en 30-60 segons.
2. Hauries de veure un login a la consola.
3. Entra com `bernat` amb la contrasenya.

### C. Comprova la xarxa

```bash
ip a
```

Hauries de veure `eth0` amb una IP del tipus `192.168.1.X`.

---

## Fase 3: Configurar xarxa (15 min)

### A. IP fixa al router (recomanat)

1. Entra al router (normalment http://192.168.1.1).
2. Busca la seccio **DHCP** o **Address Reservation**.
3. Reserva la IP actual de la RPi (per exemple, `192.168.1.100`).
4. D'aquesta manera, la RPi sempre tindra la mateixa IP a la teva xarxa local.

### B. Verificar

```bash
ping 8.8.8.8
ping google.com
```

Si funciona, tens internet. Si no:
- Comprova el cable Ethernet.
- Comprova la configuracio del router.

### C. SSH des del teu PC

Ara pots treure el monitor i treballar només per SSH:

**Des de Windows PowerShell**:
```powershell
ssh bernat@192.168.1.100
```

Si funciona, ja tens el primer pas fet!

---

## Fase 4: Actualitzacio inicial (20 min)

### A. Actualitza el sistema

```bash
sudo apt update
sudo apt upgrade -y
sudo apt autoremove -y
```

Pot trigar 5-15 minuts.

### B. Instal·la eines basiques

```bash
sudo apt install -y curl wget git nano htop vim net-tools
```

### C. Configura el hostname (si no ho has fet a l'imager)

```bash
sudo hostnamectl set-hostname hortosona
```

Edita `/etc/hosts`:
```bash
sudo nano /etc/hosts
```

Canvia la linia amb `127.0.1.1` per:
```
127.0.1.1 hortosona
```

Guarda amb `Ctrl+O`, `Enter`, `Ctrl+X`.

### D. Reinicia

```bash
sudo reboot
```

---

## Fase 5: Instal·lar Docker (10 min)

### A. Script oficial

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
rm get-docker.sh
```

### B. Afegeix el teu usuari al grup docker

```bash
sudo usermod -aG docker bernat
```

**Important**: tanca la sessio SSH i torna a entrar perque el canvi tingui efecte:
```bash
exit
ssh bernat@192.168.1.100
```

### C. Verifica

```bash
docker --version
docker run hello-world
```

Si veus el missatge "Hello from Docker!", funciona.

### D. Instal·la Docker Compose

Ja ve amb Docker modern, pero verifica:
```bash
docker compose version
```

---

## Fase 6: Instal·lar Portainer (10 min)

### A. Crea un volum per les dades

```bash
docker volume create portainer_data
```

### B. Arrenca Portainer

```bash
docker run -d -p 9000:9000 -p 9443:9443 \
  --name portainer \
  --restart=always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data \
  portainer/portainer-ce:latest
```

### C. Configura

1. Obre el navegador: https://192.168.1.100:9443
2. Crea un compte d'administrador (la primera vegada).
3. Selecciona **"Get Started"** amb el Docker local.

Ara ja tens un panell per gestionar tots els teus contenidors!

---

## Fase 7: Instal·lar Uptime Kuma (5 min)

### A. Crea el directori

```bash
mkdir -p /home/bernat/homelab/uptime-kuma
cd /home/bernat/homelab/uptime-kuma
```

### B. Crea el docker-compose.yml

```bash
cat > docker-compose.yml << 'EOF'
services:
  uptime-kuma:
    image: louislam/uptime-kuma:1
    container_name: uptime-kuma
    restart: always
    ports:
      - 3001:3001
    volumes:
      - uptime-kuma:/app/data

volumes:
  uptime-kuma:
EOF
```

### C. Arrenca

```bash
docker compose up -d
```

### D. Configura

1. Obre: http://192.168.1.100:3001
2. Crea un compte.
3. Afegeix monitors:
   - **Portainer**: `https://192.168.1.100:9443` (cada minut)
   - **Homepage** (quan estigui): http://192.168.1.100:3000
   - **Hort Osona** (web publica): https://bernatmora.github.io/hort-osona/
   - **BernatLab** (web publica): https://bernatmora.github.io/bernatlab/

---

## Fase 8: Instal·lar Homepage (5 min)

### A. Crea el directori

```bash
mkdir -p /home/bernat/homelab/homepage
cd /home/bernat/homelab/homepage
```

### B. Crea el docker-compose.yml

```bash
cat > docker-compose.yml << 'EOF'
services:
  homepage:
    image: ghcr.io/gethomepage/homepage:latest
    container_name: homepage
    restart: always
    ports:
      - 3000:3000
    volumes:
      - ./config:/app/config
      - /var/run/docker.sock:/var/run/docker.sock:ro
    environment:
      - HOMEPAGE_ALLOWED_HOSTS=192.168.1.100,hortosona.local
EOF
```

### C. Crea la configuracio inicial

```bash
mkdir -p config/services
cat > config/services.yaml << 'EOF'
---
- Portainer:
    - Container: portainer
      Description: Gestor de contenidors
      URL: https://192.168.1.100:9443
      Icon: portainer

- Uptime Kuma:
    - Container: uptime-kuma
      Description: Monitoritzacio
      URL: http://192.168.1.100:3001
      Icon: uptime-kuma

- BernatLab:
    - Web publica del projecte
      URL: https://bernatmora.github.io/bernatlab/
      Icon: github

- Hort Osona:
    - Web publica de lhort
      URL: https://bernatmora.github.io/hort-osona/
      Icon: leaf
EOF

cat > config/widgets.yaml << 'EOF'
---
- search:
    provider: custom
    url: https://www.google.com/search

- resources:
    cpu: true
    memory: true
    disk: /
EOF

cat > config/settings.yaml << 'EOF'
---
title: BernatLab
background:
  opacity: 50
theme: dark
color: slate
EOF
```

### D. Arrenca

```bash
docker compose up -d
```

### E. Verifica

Obre: http://192.168.1.100:3000

Hauries de veure el teu panell personalitzat.

---

## Fase 9: Configurar Tailscale (15 min)

### A. Instal·la Tailscale

```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
```

Et donara un enllaç per autenticar-te. Segueix-lo.

### B. Comprova la IP Tailscale

```bash
tailscale ip -4
```

Hauries de veure una IP del tipus `100.X.Y.Z`. **Aquesta es la teva IP Tailscale** (anota-la).

### C. Verifica l'accés extern

Des del teu PC:
```powershell
ssh bernat@100.X.Y.Z
```

Si funciona, ja pots accedir a la RPi des de qualsevol lloc amb Tailscale.

### D. Configura MagicDNS

Tailscale ja ve amb MagicDNS activat per defecte. Pots accedir amb `ssh bernat@hortosona` des de qualsevol node Tailscale.

---

## Fase 10: Verificar-ho tot (10 min)

### A. Comprova que tot esta corrent

```bash
docker ps
```

Hauries de veure 3 contenidors actius:
- portainer
- uptime-kuma
- homepage

### B. Comprova la xarxa

```bash
curl -k https://localhost:9443/api/status
curl http://localhost:3001
curl http://localhost:3000
```

Tots han de respondre.

### C. Accedeix des del navegador

| Servei | URL local | URL Tailscale |
|---|---|---|
| Portainer | https://192.168.1.100:9443 | https://100.X.Y.Z:9443 |
| Uptime Kuma | http://192.168.1.100:3001 | http://100.X.Y.Z:3001 |
| Homepage | http://192.168.1.100:3000 | http://100.X.Y.Z:3000 |

### D. Configura alertes a Uptime Kuma

1. Ves a Uptime Kuma → Settings → Notifications.
2. Afegeix **Telegram** (veure documentacio oficial).
3. Configura una alerta per quan qualsevol servei caigui.

---

## Que fer despres?

### Dia 1 (avui):
- Tot lo anterior.
- Familiaritzar-te amb cada eina.

### Dia 2 (dema):
- Configurar **SSH amb claus** (M8 cap 1).
- Configurar el **perfil SSH** al teu PC (M8 cap 3).
- **Backup** de la configuracio de la RPi.

### Dia 3 (mes tard):
- **Node-RED** per a automatitzacions.
- **Grafana + Prometheus** per a visualitzacio.
- **MQTT (Mosquitto)** per als sensors.

### Mes endavant:
- **LoRa SX1262** per als sensors llunyans.
- **InfluxDB** per emmagatzemar series temporals.
- **Ollama** per a IA local.

---

## Solucio de problemes

### Si SSH no connecta

1. Comprova que la RPi te IP (`ip a`).
2. Comprova que el firewall permet SSH (`sudo ufw status`).
3. Comprova que SSH esta actiu (`sudo systemctl status ssh`).

### Si Docker no arrenca

1. Comprova els logs (`sudo journalctl -u docker`).
2. Comprova que tens memoria suficient (`free -h`).
3. Reinstalla (`sudo apt reinstall docker.io`).

### Si un port esta ocupat

1. Comprova qui l'ocupa (`sudo netstat -tlnp | grep PORT`).
2. Canvia el port al `docker-compose.yml`.

### Si Tailscale no autentica

1. Verifica que tens internet a la RPi.
2. Torna a provar (`sudo tailscale up`).
3. Si segueix fallant, surt (`sudo tailscale down`) i torna a entrar.

---

## Recursos adicionals

- **Curs del BernatLab**: https://bernatmora.github.io/bernatlab/book/curs/
- **Llibre del BernatLab**: https://bernatmora.github.io/bernatlab/
- **Glossari**: https://bernatmora.github.io/bernatlab/book/glossari.html
- **Hort Osona**: https://bernatmora.github.io/hort-osona/
- **Runbook Tailscale recovery**: https://github.com/BernatMora/bernatlab/blob/main/book/curs/recursos/recuperacio-emergencia-tailscale.md

---

> *Guia redactada per Hermes, el copilot del BernatLab. Adaptada a la RPi de l'usuari Bernat Mora, configurada a hortosona amb Debian 13 Lite.*
