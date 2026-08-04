# Capítol 60 — Sistema base segur

> *"La diferència entre un servidor vulnerable i un de segur és, sovint, una hora de feina. Aquest capítol és aquesta hora."*

## 60.1 Què aprendràs

Al final d'aquest capítol tindràs:

- Autenticació per **clau SSH** (sense contrasenya).
- **Contrasenya desactivada** per SSH (només clau).
- **Tailscale** instal·lat i configurat.
- Accés a la RPi des de qualsevol lloc del món via Tailscale.
- **2FA** per a SSH (opcional, però recomanat).
- Les primeres mesures de **hardening** aplicades.

Aquest és el capítol on el teu servidor passa de "joguina" a "infraestructura". Tot el que hi ha aquí és **defensa en profunditat** (recorda el **Cap 43**, filosofia de seguretat).

## 60.2 Durada estimada

- Amb experiència: 30-45 min.
- Primer cop: 1-1.5 hores (comptant la generació de claus).

## 60.3 Abans de començar

Assegura't que:

- Estàs connectat a la RPi per SSH.
- Tens accés a un altre terminal (el del teu ordinador, per generar les claus).
- Tens **dos dispositius preparats**: la RPi i el teu ordinador.

Si tens problemes durant el capítol, recorda que **no has de tancar la sessió SSH actual** fins que tot funcioni. Si la configures malament, et pots quedar fora.

## 60.4 Pas 1: generar una clau SSH forta

Al **teu ordinador** (no a la RPi), obre un terminal i genera una clau SSH:

```bash
ssh-keygen -t ed25519 -C "bernat@bernat-mbp" -f ~/.ssh/bernatlab
```

Explicació:

- `-t ed25519`: tipus de clau. Ed25519 és moderna, curta i segura.
- `-C "..."`: comentari per identificar-la (el teu correu o usuari).
- `-f ~/.ssh/bernatlab`: on guardar-la. **No usis el nom per defecte** (`id_ed25519`), perquè si més endavant tens altres claus per a altres servidors, no es barregen.

Et demanarà una **passphrase**. **Sempre posa'n una**. Això xifra la clau privada al teu disc: si algú te la roba, no pot fer-la servir.

Recorda la passphrase al teu gestor de contrasenyes.

Això genera dos fitxers:

- `~/.ssh/bernatlab` (clau privada — **no la comparteixis mai**).
- `~/.ssh/bernatlab.pub` (clau pública — la pots penjar a la RPi).

## 60.5 Pas 2: afegir la clau pública a la Raspberry

Des del teu **ordinador**, copia la clau pública a la RPi:

```bash
ssh-copy-id -i ~/.ssh/bernatlab.pub bernat@hortosona
```

Et demanarà la contrasenya (l'última vegada que l'hauràs de posar). Quan acabi, la clau pública estarà a `~/.ssh/authorized_keys` de la RPi.

Alternativa manual (si `ssh-copy-id` no funciona):

```bash
cat ~/.ssh/bernatlab.pub | ssh bernat@hortosona "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
```

## 60.6 Pas 3: provar la connexió amb clau

Ara intenta entrar amb la clau:

```bash
ssh -i ~/.ssh/bernatlab bernat@hortosona
```

Si et demana la passphrase de la clau (no la contrasenya!), és que tot funciona. Si entra directament sense demanar res, tens `ssh-agent` actiu i la clau ja està desxifrada.

Per evitar haver d'escriure la passphrase cada vegada, afegeix la clau a l'agent:

**Mac**:

```bash
ssh-add --apple-use-keychain ~/.ssh/bernatlab
```

**Linux**:

```bash
ssh-add ~/.ssh/bernatlab
```

Ara ja no hauries de necessitar posar la passphrase cada vegada.

## 60.7 Pas 4: simplificar la configuració SSH al teu ordinador

Al teu **ordinador**, crea o edita `~/.ssh/config`:

**Mac/Linux**:

```bash
nano ~/.ssh/config
```

**Windows** (PowerShell): `notepad $HOME\.ssh\config`

Afegeix:

```
Host hortosona
    HostName 192.168.1.100
    User bernat
    IdentityFile ~/.ssh/bernatlab
    IdentitiesOnly yes
```

Així, només amb `ssh hortosona`, el teu ordinador sap que ha de connectar a la IP correcta amb la clau correcta.

Si tens Tailscale configurat (pas següent), pots canviar el `HostName` per la IP del tailnet:

```
Host hortosona
    HostName 100.x.y.z
    User bernat
    IdentityFile ~/.ssh/bernatlab
    IdentitiesOnly yes
```

## 60.8 Pas 5: instal·lar Tailscale

Tailscale et permet accedir a la teva RPi des de qualsevol lloc del món, sense obrir ports al router. És una VPN moderna basada en WireGuard.

A la **RPi**:

```bash
curl -fsSL https://tailscale.com/install.sh | sh
```

Després:

```bash
sudo tailscale up
```

Això et donarà una URL. Obre-la al navegador, autentica't amb el compte que has creat al **Cap 58**, i la RPi quedarà afegida al teu tailnet.

Verifica:

```bash
tailscale status
```

Hauries de veure la RPi amb una IP del tipus `100.x.x.x`. Aquesta és la IP Tailscale.

## 60.9 Pas 6: provar l'accés per Tailscale

Ara, **des del teu ordinador** (o des del mòbil!), intenta accedir per la IP Tailscale:

```bash
ssh bernat@100.x.y.z
```

(Canvia la IP per la que t'hagi tocat.)

Si funciona, ja tens accés a la RPi des de qualsevol lloc amb Tailscale instal·lat. Sense obrir cap port al router, sense IP pública, sense res.

Si tens un amic amb qui vulguis compartir accés (per exemple, per ajudar-te amb el servidor), pots afegir-lo al teu tailnet des de la consola de Tailscale: https://login.tailscale.com/admin.

## 60.10 Pas 7: desactivar l'accés per contrasenya

Un cop la clau SSH funciona, **desactiva l'autenticació per contrasenya**. Això evita atacs de força bruta.

A la **RPi**:

```bash
sudo nano /etc/ssh/sshd_config
```

Cerca o afegeix aquestes línies (assegurant-te que no estan comentades amb `#`):

```
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
PermitEmptyPasswords no
```

Per trobar-les ràpid, pots fer:

```bash
sudo grep -E "^#?(PermitRootLogin|PasswordAuthentication|PubkeyAuthentication|PermitEmptyPasswords)" /etc/ssh/sshd_config
```

Si una línia està comentada (`#PasswordAuthentication yes`), lleva-li el `#` i canvia el valor a `no`.

Desa i reinicia SSH:

```bash
sudo systemctl restart sshd
```

**Important**: no tanquis la sessió SSH actual! Prova primer des d'un altre terminal:

```bash
ssh bernat@hortosona
```

Si funciona, llavors pots tancar la sessió original.

## 60.11 Pas 8: instal·lar 2FA a SSH (opcional però recomanat)

Afegeix una capa extra amb 2FA. Així, encara que robin la teva clau SSH, no podran entrar.

A la **RPi**:

```bash
sudo apt install libpam-google-authenticator
```

Configura per al teu usuari:

```bash
google-authenticator
```

Et mostrarà un codi QR. Escaneja'l amb Google Authenticator, Authy o 1Password al teu mòbil.

Guarda els **codis de recuperació** en un lloc segur (Bitwarden, paper en una caixa forta). Si perds el mòbil, aquests codis et deixaran entrar.

Edita la configuració de PAM:

```bash
sudo nano /etc/pam.d/sshd
```

Afegeix al final:

```
auth required pam_google_authenticator.so
```

Edita la configuració de SSH:

```bash
sudo nano /etc/ssh/sshd_config
```

Canvia o afegeix:

```
ChallengeResponseAuthentication yes
AuthenticationMethods publickey,keyboard-interactive
```

Reinicia SSH:

```bash
sudo systemctl restart sshd
```

Prova des d'un altre terminal:

```bash
ssh bernat@hortosona
```

Ara hauries de veure:

1. Contrasenya de la clau (si tens passphrase).
2. Codi de Google Authenticator.

Si tot funciona, ja tens SSH amb clau + 2FA. **Molt segur**.

## 60.12 Pas 9: configurar actualitzacions automàtiques

Hem parlat d'això al **Cap 48** (hardening). Apliquem-ho ara:

```bash
sudo apt install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

Tria "Yes" a la pregunta.

Edita la configuració:

```bash
sudo nano /etc/apt/apt.conf.d/50unattended-upgrades
```

Assegura't que tens aquestes línies (algunes poden estar comentades):

```
Unattended-Upgrade::Allowed-Origins {
    "Debian bookworm-security";
    "Debian bookworm-updates";
};
Unattended-Upgrade::AutoFixInterruptedDpkg "true";
Unattended-Upgrade::Remove-Unused-Kernel-Packages "true";
Unattended-Upgrade::Remove-Unused-Dependencies "true";
Unattended-Upgrade::Automatic-Reboot "false";
```

(Ajusta `bookworm` per la teva versió; a Debian 13 és `trixie`.)

Prova:

```bash
sudo unattended-upgrades --dry-run
```

Hauries de veure què passaria si s'executés ara.

## 60.13 Pas 10: configurar el tallafocs (UFW)

Hem parlat d'UFW al **Cap 47** (fail2ban i tallafocs). Apliquem una política restrictiva:

```bash
sudo apt install ufw
```

Política per defecte: denega tot, permet el necessari:

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
```

Permet SSH:

```bash
# Si tens 2FA, permet només per Tailscale
sudo ufw allow in on tailscale0 to any port 22

# Si vols SSH per la xarxa local també
sudo ufw allow from 192.168.1.0/24 to any port 22
```

Activa:

```bash
sudo ufw enable
sudo ufw status verbose
```

**Important**: comprova que pots seguir connectant per SSH abans de fer res més! Si UFW et talla l'accés, hauràs d'anar amb un monitor a la RPi.

## 60.14 Pas 11: instal·lar fail2ban

Recordeu el **Cap 47**: fail2ban bloqueja IPs que fan massa intents fallits. Activem-lo:

```bash
sudo apt install fail2ban
```

Crea la configuració local:

```bash
sudo nano /etc/fail2ban/jail.local
```

Afegeix:

```ini
[DEFAULT]
bantime = 1h
findtime = 10m
maxretry = 3
ignoreip = 127.0.0.1/8 100.64.0.0/10

[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 24h
```

El rang `100.64.0.0/10` és la xarxa Tailscale — molt important per no auto-bloquejar-te.

Reinicia:

```bash
sudo systemctl restart fail2ban
```

Verifica:

```bash
sudo fail2ban-client status sshd
```

## 60.15 Pas 12: permisos estrictes als fitxers crítics

Aplica els permisos del **Cap 48** (hardening):

```bash
sudo chmod 600 /etc/shadow
sudo chmod 600 /etc/gshadow
sudo chmod 644 /etc/passwd
sudo chmod 644 /etc/group
sudo chmod 600 /etc/ssh/sshd_config
```

## 60.16 Pas 13: crear la primera còpia amb restic

Recordeu el **Cap 45** (còpies de seguretat). Ara que el sistema base està net, fem la primera còpia:

```bash
sudo apt install restic
```

Crea una carpeta per a les còpies (pot ser a una SSD USB, a la microSD, o al núvol — decideix tu):

```bash
mkdir -p /home/bernat/backups
```

Inicialitza el repositori:

```bash
restic init --repo /home/bernat/backups
```

Et demanarà una **contrasenya** per al repo. **Guarda-la al gestor de contrasenyes**. Si la perds, les dades són irrecuperables.

Fes la primera còpia:

```bash
restic --repo /home/bernat/backups backup \
    /home/bernat \
    /etc \
    /var/lib/docker 2>/dev/null || true
```

(El `2>/dev/null || true` evita errors si la carpeta Docker encara no existeix.)

Comprova:

```bash
restic --repo /home/bernat/backups snapshots
```

Hauries de veure una còpia recent.

## 60.17 Pas 14: configurar el hostname i el missatge d'avís

Edita `/etc/issue.net` per mostrar un avís quan algú intenti accedir per SSH:

```bash
sudo nano /etc/issue.net
```

```
======================================================================
ALERTA: Aquest sistema és d'ús privat.
Tots els accessos queden registrats.
L'accés no autoritzat està prohibit i pot ser perseguit legalment.
======================================================================
```

Activa'l a SSH:

```bash
sudo nano /etc/ssh/sshd_config
```

Assegura't que tens:

```
Banner /etc/issue.net
```

Reinicia SSH:

```bash
sudo systemctl restart sshd
```

## 60.18 Pas 15: fer una còpia de la microSD amb el sistema base segur

Ara que el sistema està endureït, **torna a fer una còpia de la microSD**. Aquesta és la còpia "bona", la pots restaurar si tot es trenca.

Apaga:

```bash
sudo shutdown -h now
```

Fes la còpia igual que al **Cap 59** (pas 14). Guarda-la amb un nom clar, com `bernatlab-base-segur-2026-07-09.img`.

## 60.19 Què has après

Al final d'aquest capítol tens:

- **SSH amb clau** (sense contrasenya).
- **2FA opcional** a SSH.
- **Tailscale** funcionant (accés remot segur).
- **Tallafocs UFW** actiu.
- **fail2ban** actiu.
- **Actualitzacions automàtiques** configurades.
- **Còpia de seguretat** inicial feta.
- **Permisos estrictes** als fitxers crítics.
- **Còpia de la microSD** amb el sistema endureït.

Això és la base sobre la qual construirem la resta del BernatLab. Qualsevol cosa que instal·lem a partir d'ara partirà d'aquesta base sòlida.

## 60.20 Errors habituals

**Error 1: pèrdua d'accés SSH**.

Si canvies alguna cosa malament, pots perdre l'accés. **Mai tanquis la sessió actual** fins que no hagis provat des d'un altre terminal.

**Error 2: UFW et talla l'accés**.

Si t'has equivocat amb la regla, UFW et pot tallar SSH. Solució: connectar un monitor + teclat a la RPi i fer `sudo ufw disable`.

**Error 3: 2FA et bloqueja**.

Si canvies de mòbil o perds els codis, no podràs entrar. **Guarda sempre els codis de recuperació** en un lloc segur.

**Error 4: clau SSH sense passphrase**.

Si la clau no té passphrase, qualsevol que accedeixi al teu ordinador pot entrar al servidor. Sempre passphrase.

**Error 5: oblidar la contrasenya de restic**.

Si oblides la contrasenya, les còpies són irrecuperables. Guarda-la al gestor.

## 60.21 Resum

Aquest capítol converteix la teva RPi en un servidor **professional**. Hem vist:

- Generació i còpia de claus SSH.
- Tailscale per a accés remot segur.
- Desactivació de l'autenticació per contrasenya.
- 2FA per SSH (opcional però recomanat).
- Tallafocs UFW.
- fail2ban.
- Actualitzacions automàtiques.
- Còpia de seguretat amb restic.
- Còpia de la microSD amb el sistema endureït.

Al **Cap 61** instal·larem **Docker** i **Portainer**, la base de tots els serveis del BernatLab.

## 60.22 Exercicis pràctics

1. Genera una clau SSH ed25519 amb passphrase.
2. Afegeix-la a la RPi.
3. Configura `~/.ssh/config` per simplificar la connexió.
4. Instal·la Tailscale.
5. Desactiva l'autenticació per contrasenya.
6. Activa 2FA a SSH.
7. Configura actualitzacions automàtiques.
8. Activa UFW amb polítiques restrictives.
9. Instal·la fail2ban.
10. Aplica permisos estrictes.
11. Fes la primera còpia amb restic.
12. Fes una còpia de la microSD.
13. Documenta-ho tot al `homelab/setup-log.md`.
