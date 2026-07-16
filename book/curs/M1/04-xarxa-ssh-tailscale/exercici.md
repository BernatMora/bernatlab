# Exercici pràctic — Capítol 4: Xarxa, SSH i Tailscale

> 30-45 min · Real al teu sistema

## Objectiu
Configurar l'accés remot segur a la RPi del BernatLab mitjançant claus SSH i Tailscale. Acabaràs podent entrar des de qualsevol lloc amb `ssh bernat@hortosona` sense contrasenya.

## Requisits
- Portàtil amb terminal (PowerShell, WSL, Git Bash o Terminal de Mac)
- RPi del BernatLab accessible per SSH
- 30-45 minuts

## Pas 1: Instal·la Tailscale a la RPi (10 min)

Des de la RPi (per SSH des de la xarxa local):

```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
# S'obrirà un enllaç al navegador. Autentica't amb el teu compte Google/GitHub.

# Comprova l'estat
sudo tailscale status
# Hauries de veure la teva RPi amb IP 100.X.Y.Z (anota-la, hauria de ser 100.115.134.76)

tailscale ip -4
```

## Pas 2: Instal·la Tailscale al portàtil

- Windows/Mac/Linux: https://tailscale.com/download
- Tots els SO tenen un installer gràfic.
- Un cop instal·lat, autentica't amb el MATEIX compte que a la RPi.

Comprova des del portàtil:

```bash
# Linux/Mac/WSL:
tailscale status

# Windows PowerShell:
tailscale.exe status
```

Hauries de veure la RPi a la llista.

## Pas 3: Genera una clau SSH al portàtil (10 min)

Al teu portàtil:

```bash
# Genera la clau amb un comentari identificatiu
ssh-keygen -t ed25519 -C "bernat@portatil-2026"

# Et preguntarà on desar-la (per defecte va bé).
# Et preguntarà una passphrase (opcional però recomanable per seguretat extra).
```

A Windows la clau queda a `C:\Users\iadmin\.ssh\id_ed25519`.

## Pas 4: Copia la clau pública a la RPi (10 min)

```bash
# Des del teu portàtil, amb Tailscale actiu:

# Mètode 1: amb ssh-copy-id (Linux/Mac/WSL)
ssh-copy-id bernat@hortosona

# Mètode 2: manual (Windows PowerShell o si el mètode 1 falla)
type $env:USERPROFILE\.ssh\id_ed25519.pub | ssh bernat@hortosona "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"

# Mètode 3: manual amb cat (Linux/Mac)
cat ~/.ssh/id_ed25519.pub | ssh bernat@hortosona "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
```

Prova que funciona:

```bash
ssh bernat@hortosona
# Hauria d'entrar SENSE demanar contrasenya (només la passphrase de la clau si n'has posat).
```

## Pas 5: Configura el fitxer ~/.ssh/config (5 min)

Crea/edita `~/.ssh/config` al portàtil:

```
Host hortosona
    HostName 100.115.134.76
    User bernat
    IdentityFile ~/.ssh/id_ed25519
    ServerAliveInterval 60

Host rpi
    HostName hortosona
    User bernat
```

Ara `ssh hortosona` i `ssh rpi` funcionen directament.

## Pas 6: Desactiva l'autenticació per contrasenya (opcional, recomanable)

A la RPi, edita la configuració SSH:

```bash
sudo nano /etc/ssh/sshd_config
# Assegura't que diu:
#   PasswordAuthentication no
#   PubkeyAuthentication yes

sudo systemctl restart ssh
```

**Compte**: fes això NOMÉS quan estigis segur que la clau funciona. Si no, et quedes fora.

## Pas 7: Documenta

Crea `book/curs/M1/04-xarxa-ssh-tailscale/configuracio.md` amb:

- La teva IP Tailscale (la RPi i el portàtil).
- La fingerprint de la clau (`ssh-keygen -lf ~/.ssh/id_ed25519.pub`).
- Un parell de captures de `tailscale status`.

## Validació

Has acabat si:
- [ ] Tailscale instal·lat a RPi i portàtil amb el mateix compte.
- [ ] `tailscale status` mostra ambdós dispositius.
- [ ] Has generat una clau SSH al portàtil.
- [ ] La clau pública està a `~/.ssh/authorized_keys` de la RPi.
- [ ] `ssh bernat@hortosona` entra sense contrasenya.
- [ ] Has configurat `~/.ssh/config` al portàtil.
- [ ] Has documentat la configuració a `configuracio.md`.

## Per aprofundir

- Activa la 2FA al compte de Tailscale.
- Afegeix un node compartit (un amic) per aprendre ACLs.
- Configura un servidor SSH personalitzat a un port no estàndard (p. ex. 2222).
- Investiga `ssh-agent` per no haver d'introduir la passphrase cada vegada.
