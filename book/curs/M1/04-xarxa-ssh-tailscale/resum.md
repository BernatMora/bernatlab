# Resum — Capítol 4: Xarxa, SSH i Tailscale

## La idea clau

Un homelab sense accés remot és un trasto inútil. Al BernatLab necessitem poder entrar a la Raspberry Pi (hostname `hortosona`, Debian 13) des de qualsevol lloc: des del portàtil de sobretaula, des del mòbil, des d'un WiFi de cafeteria. Per fer-ho combinem **SSH** (per accedir a la terminal) i **Tailscale** (per fer-ho de forma segura sense tocar el router).

## Conceptes de xarxa que necessites

**Adreça IP**: identificador numèric de cada dispositiu a la xarxa. La RPi té una IP local (típicament `192.168.1.X`) i una IP Tailscale (`100.x.y.z`).

**Port**: número associat a un servei. És com l'extensió telefònica:
- `22` — SSH
- `80` — HTTP
- `443` — HTTPS
- `9000` — Portainer
- `3001` — Uptime Kuma

Un servidor web escolta al port 80, SSH al 22, etc.

**DNS** (Domain Name System): tradueix noms fàcils (`hortosona.local`, `google.com`) a IPs (`192.168.1.50`, `142.250.190.46`).

**NAT i port forwarding**: a casa teva, el router té una IP pública i els teus dispositius tenen IPs privades. Per accedir des de fora caldria obrir ports al router (perillós). Tailscale ho evita creant una xarxa privada virtual (VPN) que evita el router.

## SSH: la porta d'entrada

SSH (Secure Shell) és el protocol estàndard per accedir a una terminal remota de forma xifrada. Per defecte escolta al port 22.

Connexió bàsica (amb contrasenya):

```bash
ssh bernat@hortosona
# o per IP
ssh bernat@100.x.y.z
ssh bernat@192.168.1.50
```

La primera vegada et pregunta si confies en la fingerprint de la clau del servidor. Escriu `yes`. Després et demana la contrasenya.

**Sortir de la sessió**: `exit` o `Ctrl+D`.

## Claus SSH: sense contrasenya (i més segur)

Les claus SSH són dos fitxers: una **privada** (la guardes al teu portàtil, com una master key) i una **pública** (la copies al servidor, com un pany). Són millors que la contrasenya perquè:
- No es poden endevinar (són de 4096 bits).
- No es poden robar per força bruta.
- Permeten automatitzar còpies de seguretat.

Generar-les al teu portàtil (Windows amb PowerShell o WSL):

```bash
ssh-keygen -t ed25519 -C "bernat@portatil"
# Desa a C:\Users\usuari\.ssh\id_ed25519 (Windows)
# o ~/.ssh/id_ed25519 (Linux/Mac)
```

Copiar la clau pública al servidor (obert al port 22):

```bash
# Amb Windows 10+:
type $env:USERPROFILE\.ssh\id_ed25519.pub | ssh bernat@hortosona "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"

# Amb Linux/Mac:
ssh-copy-id bernat@hortosona
```

A partir d'ara, `ssh bernat@hortosona` entra sense contrasenya.

## Fitxer de configuració SSH

Per no haver de recordar IPs, crea/edita `~/.ssh/config` (al teu portàtil):

```
Host hortosona
    HostName 100.x.y.z
    User bernat
    IdentityFile ~/.ssh/id_ed25519

Host rpi
    HostName hortosona
    User bernat
```

Ara pots fer `ssh hortosona` o `ssh rpi` directament.

## Tailscale: la xarxa màgica

**Tailscale** és una VPN basada en WireGuard que crea una xarxa privada entre els teus dispositius sense tocar el router. Cada dispositiu té una IP `100.X.Y.Z` única.

Instal·lar a la RPi:

```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
# Et donarà un enllaç per autenticar-te al navegador
sudo tailscale status   # veure l'estat i les IPs assignades
```

La IP Tailscale de la teva RPi és `100.x.y.z`. Pots accedir-hi des de qualsevol dels teus dispositius Tailscale, siguis on siguis al món.

Avantatges:
- **Sense port forwarding**: no cal tocar el router.
- **Xifrat d'extrem a extrem**: WireGuard és modern i segur.
- **MagicDNS**: pots accedir amb el nom de la màquina (`ssh bernat@hortosona`) sense recordar la IP.
- **Gratis fins a 100 dispositius**: més que suficient per un homelab.

## MagicDNS

Un cop tens Tailscale actiu, pots fer `ssh bernat@hortosona` en lloc de `ssh bernat@100.x.y.z`. Tailscale resol automàticament el nom a la IP correcta.

Si vols noms personalitzats (`rpi`, `nas`, `nasbernat`...), configura "MagicDNS names" al panell de Tailscale o simplement funciona amb els hostnames dels dispositius.

## SSH amb clau + Tailscale = combo perfecte

Combinant les dues coses:
- Des del portàtil, sense Tailscale, només pots entrar a la RPi si sou a la mateixa WiFi.
- Amb Tailscale, hi entres des de qualsevol lloc del món amb `ssh bernat@hortosona` (sense contrasenya si has posat clau).
- I tot el tràfic va xifrat, ni tan sols el router de la teva xarxa ho pot veure.

## Comandes útils

```bash
# Veure la teva IP Tailscale
tailscale ip -4

# Llistar tots els dispositius de la xarxa Tailscale
tailscale status

# Compartir un servei amb un amic (temporal)
sudo tailscale serve 3000    # comparteix Portainer temporalment

# Test de xarxa des de la RPi
ping 100.x.y.z         # a ella mateixa
ping 8.8.8.8                # a Internet (DNS de Google)
curl -I https://google.com  # test HTTPS
```

## Connexions amb altres capítols

- **Cap 3** — Ordres de terminal que executarem per SSH.
- **Cap 5** — Docker exposarà serveis a ports que accedirem via Tailscale.
- **Cap 6** — Portainer al port 9000, accessible per `http://hortosona:9000`.
- **Cap 7** — Uptime Kuma al port 3001, accessible igual.
- **Cap 8** — Homepage al port 3010, el punt d'entrada gràfic.
- **Cap 22** — Monitoratge remot amb aquesta combinació.

Amb SSH i Tailscale, tens la base de tot. Ara toca posar-hi serveis a sobre.
