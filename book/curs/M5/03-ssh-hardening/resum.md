# Resum - Capitol 3: SSH Hardening

## La idea clau

SSH es la porta d'entrada al servidor. Si un atacant entra per aqui, te control absolut. Per tant, hem de posar totes les barreres possibles: només autenticacio amb claus (no contrasenyes), un port personalitzat per reduir soroll, fail2ban per bloquejar atacs automatitzats, i limitacions per evitar escalades. Es **la mesura mes important** despres de Tailscale.

## Per que SSH es un objectiu prioritari

Tot i que Tailscale amaga el port 22 a Internet, SSH continua sent el servei mes critic del servidor. Perque:

- Es l'entrada a la consola: shell d'administracio.
- Te permisos de superusuari: un `sudo` et dona tot el control.
- Es universal: qualsevol Linux te SSH.
- Es el que mes saben atacar els bots.

Si Tailscale falla o te una errada de configuracio, SSH es la **porta que queda oberta**. Cal que aquesta porta sigui **forta**.

## Desactivar el login amb contrasenya

Aixo es la mesura mes important. Per defecte, OpenSSH accepta tant contrasenyes com claus. Si nomes acceptes claus, els atacs de bruteforce contra contrasenyes fallen sempre.

```bash
# 1. Genera una clau forta (a la maquina CLIENT, no al servidor)
ssh-keygen -t ed25519 -C "bernat@bernatlab"

# 2. Copia la clau publica al servidor
ssh-copy-id -i ~/.ssh/id_ed25519.pub bernat@raspberry

# 3. Prova que funciona (sense que et demani contrasenya)
ssh bernat@raspberry

# 4. Ara desactiva les contrasenyes
sudo nano /etc/ssh/sshd_config
```

Edita `/etc/ssh/sshd_config`:

```sshconfig
# Nomes claus publiques
PubkeyAuthentication yes
PasswordAuthentication no
ChallengeResponseAuthentication no
AuthenticationMethods publickey
```

Aplica:

```bash
sudo sshd -t   # valida la sintaxi
sudo systemctl restart sshd
```

**IMPORTANT**: abans de tancar la sessio actual, obre una **segona sessio SSH** i comprova que la nova autenticacio funciona. Si no, et quedes fora.

## Desactivar root login

L'usuari `root` te permisos absoluts. No cal que un atacant hi entri directament; si entra com a usuari normal, pot escalar amb `sudo` (i aixo deixa rastre als logs).

```sshconfig
PermitRootLogin no
```

Alternatives:

- `prohibit-password`: nomes claus (no contrasenya) per a root. Util si vols mantenir root actiu.
- `forced-commands-only`: root pot entrar nomes per executar una comanda concreta (per scripts automatitzats).

## Canviar el port (soroll, no seguretat)

```sshconfig
Port 5022
```

Perque? Perque la gran majoria de bots nomes escanegen el port 22. Si mous SSH a 5022, el 95% del soroll desapareix. Pero no es una mesura de seguretat per si sola: un nmap el trobara. Es un complement, no la solucio.

Recorda: si canvies el port, els clients s'hi han de connectar amb `-p 5022` o configurat al `~/.ssh/config`.

## fail2ban: el vigilant

**fail2ban** es una eina que llegeix els logs de SSH i bloqueja temporalment les IPs que fan massa intents fallits. Es pot configurar per molts serveis (SSH, Apache, Postfix...) pero nosaltres el farem servir nomes per a SSH.

Instal·lacio:

```bash
sudo apt install fail2ban
```

Configuracio: crea `/etc/fail2ban/jail.local` (es un override, no toques el `.conf`):

```ini
[DEFAULT]
# Ignorar Tailscale (la xarxa privada) i localhost
ignoreip = 127.0.0.1/8 100.64.0.0/10

# 5 intents fallits
maxretry = 5

# en 10 minuts
findtime = 600

# bloqueig durant 1 hora
bantime = 3600

# Quin accio prendre
banaction = ufw
banaction_allports = ufw

[sshd]
enabled = true
port    = ssh
filter  = sshd
logpath = %(sshd_log)s
```

Activar i veure els bloquejos:

```bash
sudo systemctl enable fail2ban
sudo systemctl start fail2ban

# Estat general
sudo fail2ban-client status
sudo fail2ban-client status sshd

# IPs bloquejades ara mateix
sudo fail2ban-client status sshd | grep "Banned IP list"

# Desbloquejar una IP manualment
sudo fail2ban-client set sshd unbanip 1.2.3.4
```

## Configuracio completa recomanada

```sshconfig
# /etc/ssh/sshd_config

Port 5022
AddressFamily inet
Protocol 2

# Autenticacio
PermitRootLogin no
PubkeyAuthentication yes
PasswordAuthentication no
ChallengeResponseAuthentication no
AuthenticationMethods publickey
MaxAuthTries 3
LoginGraceTime 30
MaxSessions 3

# Forwarding i extras (desactiva tot lo que no usis)
X11Forwarding no
AllowTcpForwarding no
GatewayPorts no
PermitUserEnvironment no

# Permetre variables d'entorn segures
AcceptEnv LANG LC_*

# Banner
Banner /etc/issue.net
```

## Com verificar la configuracio

```bash
# Validar sintaxi sense reiniciar
sudo sshd -t

# Veure la configuracio efectiva
sudo sshd -T | head -30

# Veure les claus publiques que pot acceptar cada usuari
sudo sshd -T | grep authorizedkeys

# Des d'un altre shell, intentar connectar-se
ssh -p 5022 -v bernat@raspberry
# -v mostra el procés d'autenticacio, veuras que nomes accepta "publickey"
```

## Bones practiques

- **Mai canviïs la configuracio amb una sola sessio oberta**. Sempre dues.
- **`sudo sshd -t` abans de reiniciar**. Si falla, el servei no arranca.
- **Còpia de seguretat** del fitxer abans de editar-lo: `sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak`.
- **Tens una consola fisica** (teclat + monitor) com a salvavides si tot falla.
- **Revisa els logs** setmanalment: `sudo journalctl -u sshd --since "1 week ago"`.

## Connexions amb altres capitols

- **M1 Cap 4** - Xarxa i SSH: els basics.
- **M8 Cap 1** - SSH amb claus: ja ho tens.
- **Cap 2 d'aquest modul** - Tailscale: amaga el port 22 a Internet.
- **Cap 4 d'aquest modul** - Firewall: ufw es on fail2ban aplica les regles.
- **Cap 8 d'aquest modul** - Monitoratge: veure els logs i els bloquejos.

## Comandes utils

```bash
# Connexio amb un port diferent
ssh -p 5022 bernat@raspberry

# Connexio amb verbose (debug)
ssh -vvv bernat@raspberry

# Copiar una clau
ssh-copy-id -i ~/.ssh/id_ed25519.pub bernat@raspberry

# Gestionar claus a authorized_keys
ssh-keygen -l -f ~/.ssh/authorized_keys

# Veure la configuracio efectiva del servidor
sudo sshd -T | grep -E "permitroot|password|pubkey"
```

## Conclusio: el triple combo

SSH fort = **Tailscale (amaga)** + **claus (autenticacio)** + **fail2ban (vigila)**. Si tens aquestes tres coses, es quasi impossible que un atacant pugui entrar per SSH. Encara que ho intenti amb contrasenyes, amb claus, amb exploits: Tailscale ja el filtra, les claus no es poden adivinar, i fail2ban el bloqueja. Es el que anomenem "defensa en profunditat".
