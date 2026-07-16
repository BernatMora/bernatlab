# 🚨 Recuperació d'emergència — Tailscale down a la RPi

> **Què fer si Tailscale es desconnecta i no pots accedir per SSH.**
>
> Aquest document està pensat per a una situació que es pot donar:
> has fet `sudo tailscale down` (o Tailscale ha fallat), i ara no
> pots accedir a la RPi per SSH perquè tot passava per Tailscale.

## Per què ha passat

La teva RPi (hostname `hortosona`, IP Tailscale `100.115.134.76`) s'ha
desconnectat de Tailscale. Com que al Windows fas `ssh bernat@100.115.134.76`,
i aquesta IP només funciona amb Tailscale, ara no pots entrar.

Les comandes SSH habituals (que **ara NO funcionen**):

```bash
ssh bernat@100.115.134.76      # IP Tailscale — NO funciona
ssh bernat@hortosona           # Nom amb MagicDNS — NO funciona
```

Per tornar a connectar-te, necessites **accés directe** a la RPi.

---

## 🕐 Procediment pas a pas

### 1. Prepara el material (5 min)

Necessites:

- **Monitor amb entrada HDMI** (un monitor d'ordinador o una tele)
- **Cable micro-HDMI a HDMI** (la RPi 4 té 2 ports micro-HDMI, el de l'esquerra marcat **HDMI0** és el principal)
- **Teclat USB** (qualsevol teclat USB estàndard)
- La RPi connectada a la pantalla i al corrent elèctric

Si no tens algun d'aquests elements, mira les **alternatives** al final.

### 2. Arrenca la RPi (1 min)

Connecta el corrent a la RPi. Hauries de veure:

- LED verd encès (activitat de la microSD)
- LED vermell encès (alimentació)
- A la pantalla: text d'arrencada de Debian, terminal de login

Si la RPi ja estava encesa i simplement vols accedir-hi, no cal resoldre — connecta el monitor i el teclat directament.

### 3. Entra a la terminal (1 min)

Quan vegis el prompt de login:

```
Debian GNU/Linux 13 hortosona tty1

hortosona login: bernat
Password: [la teva contrasenya]
```

Si tens un servidor gràfic (no hauries de tenir, però per si de cas),
premium `Ctrl+Alt+F1` per accedir a la terminal TTY.

### 4. Torna a engegar Tailscale (1 min)

Un cop dins, executa:

```bash
sudo tailscale up
```

Hauries de veure un missatge confirmant que Tailscale ha tornat:

```
Success.
```

Si tens MagicDNS actiu, et confirmarà que ha tornat a la xarxa.

### 5. Torna a accedir des del Windows (1 min)

Des de **PowerShell** al Windows:

```powershell
ssh bernat@100.115.134.76
# o:
ssh bernat@hortosona
```

Si et torna a demanar password, entra'l. Hauries d'estar dins.

### 6. Confirma que tot funciona (2 min)

Un cop dins, comprova:

```bash
# 1. Estatus de Tailscale
tailscale status

# 2. Portainer funciona?
curl -k -w "HTTP %{http_code} | %{time_total}s\n" \
  https://localhost:9443/ -o /dev/null --max-time 5

# 3. Tots els contenidors actius
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

Hauries de veure:
- Tailscale amb `hortosona` actiu
- HTTP 307 (redirect) al 9443
- 3-4 contenidors actius (homepage, uptime-kuma, portainer)

### 7. Neteja el contenidor hello-world (1 min)

Quan estiguis dins, neteja el contenidor residual:

```bash
docker rm laughing_northcutt
```

(El nom és aleatori, busca'l amb `docker ps -a` si no es diu exactament així.)

---

## 🔍 Investigar el motiu del timeout original

Quan hagis recuperat l'accés, val la pena entendre per què el Portainer donava timeout. Possibles causes:

### A. Problema de navegador (el més probable)

Si Portainer funciona via `curl` des de la RPi però no al navegador, és un problema de **caché del navegador**.

Prova:
1. Obre una **finestra d'incògnit** (`Ctrl+Shift+N` a Chrome/Edge).
2. Vés a https://100.115.134.76:9443
3. Si funciona → neteja la caché del navegador normal.

### B. Tailscale fent coses rares amb HTTPS

Prova el port alternatiu **9000** (HTTP, no HTTPS):

```
http://100.115.134.76:9000
```

Si el 9000 funciona però el 9443 no, és un problema específic del port HTTPS.

### C. Portainer penjat malgrat estar "Up"

Si el `curl` intern triga molt (>1 segon), pot ser que el procés dins del contenidor estigui penjat. Solució:

```bash
docker restart portainer
```

---

## 🔒 Prevenció per al futur

Aquesta situació no s'hauria de repetir. Un cop tinguis temps, fes això:

### 1. Configurar clau SSH al Windows (per entrar sense password)

Al Windows (PowerShell):

```powershell
# Generar clau
ssh-keygen -t ed25519

# Copiar-la a la RPi (entra amb password un cop)
type $env:USERPROFILE\.ssh\id_ed25519.pub | `
  ssh bernat@100.115.134.76 "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
```

A partir d'ara podràs entrar sense password.

### 2. Assignar IP local fixa a la RPi

A la RPi, edita `/etc/dhcpcd.conf` o configura una **reserva DHCP al router**.

```bash
sudo nano /etc/dhcpcd.conf
```

Afegeix:

```
interface eth0
static ip_address=192.168.1.50/24
static routers=192.168.1.1
static domain_name_servers=192.168.1.1 8.8.8.8
```

Després:

```bash
sudo systemctl restart dhcpcd
```

Així podràs accedir via `ssh bernat@192.168.1.50` sense Tailscale.

### 3. Documentar l'accés d'emergència

Un cop fet tot això, **no tornis a fer `sudo tailscale down`** sense tenir:
- Monitor + teclat preparats
- La IP local fixa apuntada
- Un pla B clar

---

## 🆘 Alternatives si no tens monitor + teclat

Si no tens accés a un monitor i un teclat:

### Opció 1: Router amb interfície web

Entra al router (normalment http://192.168.1.1) i busca la RPi a la llista de clients. Hauries de veure la seva IP local (per exemple `192.168.1.42`).

Després, des d'un altre PC de la xarxa:

```bash
ssh bernat@192.168.1.42
```

### Opció 2: App SSH al mòbil

Si tens el mòbil connectat a la mateixa WiFi:

1. Instal·la una app SSH (Termius, JuiceSSH, etc.).
2. Descobreix la IP de la RPi amb una app de xarxa (Fing, etc.).
3. Connecta't via SSH.

### Opció 3: Port sèrie UART (avançat)

Si tens un adaptador USB-sèrie (FTDI, CH340, etc.) i cables Dupont:

1. Connecta GND, TX, RX als pins GPIO de la RPi.
2. Usa Putty o similar a 115200 baud.
3. Accedeix a la consola sense xarxa.

Això és per a usuaris avançats.

### Opció 4: Apagar i encendre la RPi (no recomanat però funciona)

Si res més funciona:

1. Desendolla el corrent de la RPi.
2. Espera 30 segons.
3. Torna a endollar.
4. Connecta monitor + teclat abans que acabi d'arrencar.

La RPi arrencarà normalment, Tailscale intentarà reconnectar-se sol.

---

## 📞 Quan tornar a la RPi

Aquest procediment és per a **aquesta tarda** (quan arribis a casa i tinguis temps). Si tens cap problema durant el procediment, no entris en pànic — tens alternatives.

**L'objectiu principal és**: tornar a fer `sudo tailscale up` per recuperar l'accés normal. Tot el que està per sota d'això (netejar, investigar, prevenir) és opcional i es pot fer una altra tarda.

---

## 📝 Plantilla per actualitzar després

Quan hagis fet el procediment, pots afegir aquí què ha passat:

```markdown
## Data: [data]

### Què ha passat
- [Explica breument]

### Què he fet
- [Llista de passos que has seguit]

### Què he après
- [Conclusions]
```

---

**Última actualització:** 2026-07-15
