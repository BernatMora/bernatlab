# Exercici practic - Capitol 3: SSH Hardening

> 30-45 min · Real al teu sistema

## Objectiu

Endurir el servei SSH de la RPi: desactivar contrasenyes, canviar el port, instal·lar fail2ban, i verificar que tot funciona. Acabaras amb un SSH que nomes accepta claus i que bloqueja atacs automatic.

## Requisits

- Una clau SSH ja creada al teu client (la del M8 Cap 1).
- Acces fisic o consola de rescat a la RPi (per si et quedes fora).
- 30-45 minuts.

## Pas 1: Assegura la teva clau (5 min)

Abans de tocar res, verifica que la teva clau publica ja esta al servidor:

```bash
# Des del client, comprova
ssh bernat@raspberry "cat ~/.ssh/authorized_keys"

# Si nomes tens una clau, l'ideal es tenir-ne dues (backup).
# Genera una segona clau
ssh-keygen -t ed25519 -C "bernat-backup@bernatlab"
ssh-copy-id -i ~/.ssh/id_ed25519_backup.pub bernat@raspberry

# Confirma que tens les dues
ssh bernat@raspberry "cat ~/.ssh/authorized_keys"
```

## Pas 2: Fes una copia de seguretat (5 min)

```bash
# Copia de la configuracio actual
sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak

# Copia del directori ssh complet (per si de cas)
sudo cp -r /etc/ssh /etc/ssh.bak
```

## Pas 3: Aplica la nova configuracio (10 min)

Edita `/etc/ssh/sshd_config`:

```bash
sudo nano /etc/ssh/sshd_config
```

Assegura't que aquestes linies son com aixo (afegeix-les si cal, descomenta-les):

```sshconfig
Port 5022
AddressFamily inet
PermitRootLogin no
PubkeyAuthentication yes
PasswordAuthentication no
ChallengeResponseAuthentication no
AuthenticationMethods publickey
MaxAuthTries 3
LoginGraceTime 30
MaxSessions 3
X11Forwarding no
AllowTcpForwarding no
GatewayPorts no
AcceptEnv LANG LC_*
```

**IMPORTANT**: abans de continuar, obre una **SEGONA sessio SSH** desde una altra finestra. No tanquis la primera.

## Pas 4: Valida i reinicia (5 min)

```bash
# Valida sintaxi
sudo sshd -t
# Si no surt res, perfecte. Si surt error, corregeix.

# Veure la configuracio efectiva
sudo sshd -T | grep -E "port|permitroot|password|pubkey|authmethods"
# Hauries de veure:
#   port 5022
#   permitrootlogin no
#   passwordauthentication no
#   pubkeyauthentication yes
#   authenticationmethods publickey

# Reinicia el servei
sudo systemctl restart sshd

# Comprova que segueix funcionant
sudo systemctl status sshd
```

## Pas 5: Verifica la nova connexio (5 min)

Des de la segona sessio oberta, intenta connectar-te:

```bash
# Amb el port nou
ssh -p 5022 bernat@raspberry

# Amb verbose per veure el procés
ssh -p 5022 -v bernat@raspberry 2>&1 | grep -i "auth"
# Hauries de veure: "Authentication succeeded (publickey)"
```

**Ara comprova que la contrasenya NO funciona**:

```bash
# Amb una sessio amb password forçada
sshpass -p "intentionally_wrong" ssh -p 5022 -o PubkeyAuthentication=no bernat@raspberry
# Hauria de fallar amb "Permission denied (publickey)"
```

Si tot funciona, **desconnecta la primera sessio**.

## Pas 6: Instal·la i configura fail2ban (10 min)

```bash
sudo apt install -y fail2ban

# Crea el fitxer de configuracio local
sudo nano /etc/fail2ban/jail.local
```

Contingut:

```ini
[DEFAULT]
ignoreip = 127.0.0.1/8 100.64.0.0/10
maxretry = 5
findtime = 600
bantime = 3600
banaction = ufw

[sshd]
enabled = true
port    = ssh
filter  = sshd
logpath = %(sshd_log)s
```

Activa:

```bash
sudo systemctl enable fail2ban
sudo systemctl restart fail2ban
sudo fail2ban-client status
sudo fail2ban-client status sshd
```

## Pas 7: Documenta (5 min)

Al fitxer `inventari-seguretat.md`, afegeix una seccio "SSH hardening" amb:

- Port SSH actual (5022).
- Que `PasswordAuthentication` esta desactivat.
- Que fail2ban esta actiu.
- Comandos per veure logs i bloquejos.

## Validacio

- [ ] Has fet copia de seguretat de la configuracio original.
- [ ] Has aplicat la nova configuracio amb una segona sessio oberta.
- [ ] Pots connectar-te amb clau al port 5022.
- [ ] NO pots connectar-te amb contrasenya.
- [ ] fail2ban esta actiu i monitora SSH.
- [ ] Has documentat els canvis.

## Per aprofundir

- Configura **alertes per correu** a fail2ban: `destemail = bernat@bernatlab.cat` i `mta = sendmail`.
- Prova **Google Authenticator** per tenir 2FA sobre SSH.
- Investiga **CrowdSec**: un fail2ban modern i col·laboratiu.
- Si tens mes d'un servidor, considera **Ansible** per gestionar la configuracio SSH de tots alhora.
