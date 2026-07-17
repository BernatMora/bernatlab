# Exercici pràctic — Capítol 4: Xarxa, SSH i Tailscale

> 45-60 min · Real al teu sistema

## Objectiu

Configurar l'accés remot segur a la RPi del BernatLab mitjançant claus SSH i Tailscale. Acabaràs podent entrar des de qualsevol lloc amb `ssh bernat@hortosona` sense contrasenya, i entendràs què passa per sota.

## Requisits
- Portàtil amb terminal (PowerShell, WSL, Git Bash o Terminal de Mac)
- RPi del BernatLab accessible per SSH
- 45-60 minuts

## Pas 1: Verifica Tailscale a la RPi (5 min)

Des de la RPi (per SSH des de la xarxa local):

```bash
# Comprova si Tailscale ja esta instal·lat
tailscale status 2>/dev/null || echo "No instal·lat"

# Si no ho esta:
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
# S'obrirà un enllaç al navegador. Autentica't amb el teu compte Google/GitHub.

# Comprova l'estat
sudo tailscale status
# Hauries de veure la teva RPi amb IP 100.X.Y.Z (anota-la, hauria de ser 100.115.134.76)

tailscale ip -4
```

## Pas 2: Instal·la Tailscale al portàtil (5 min)

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

Hauries de veure la RPi a la llista. Si no hi és, espera 30 segons i torna-ho a provar.

## Pas 3: Ping i resolució de noms (5 min)

Comprova que la xarxa funciona als dos nivells:

```bash
# Per IP directa
ping 100.115.134.76
# prem Ctrl+C per parar

# Per nom MagicDNS
ping hortosona
# Hauria de resoldre a 100.115.134.76

# Forca la resolucio
nslookup hortosona
# o amb dig si el tens
dig hortosona
```

Si `ping hortosona` no funciona però `ping 100.115.134.76` sí, és un problema de MagicDNS. Activa'l a la consola de Tailscale.

## Pas 4: Genera una clau SSH al portàtil (5 min)

Al teu portàtil:

```bash
# Genera la clau amb un comentari identificatiu
ssh-keygen -t ed25519 -C "bernat@portatil-2026"

# Et preguntarà on desar-la (per defecte va bé).
# Et preguntarà una passphrase (opcional però recomanable per seguretat extra).
```

A Windows la clau queda a `C:\Users\iadmin\.ssh\id_ed25519`.

Mira què has creat:

```bash
ls -la ~/.ssh/
# Hauries de veure:
# id_ed25519      (clau privada - NO la comparteixis mai)
# id_ed25519.pub  (clau publica - aquesta es la que comparteixes)

# Mira la fingerprint de la teva clau publica
ssh-keygen -lf ~/.ssh/id_ed25519.pub
```

## Pas 5: Copia la clau pública a la RPi (10 min)

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

## Pas 6: Configura el fitxer ~/.ssh/config (5 min)

Crea/edita `~/.ssh/config` al portàtil:

```
Host hortosona
    HostName 100.115.134.76
    User bernat
    IdentityFile ~/.ssh/id_ed25519
    ServerAliveInterval 60
    ServerAliveCountMax 3

Host rpi
    HostName hortosona
    User bernat
```

Ara `ssh hortosona` i `ssh rpi` funcionen directament. Prova-ho:

```bash
ssh hortosona "echo funciona; uptime"
# Hauria d'executar l'ordre sense obrir sessio interactiva
```

## Pas 7: Desactiva l'autenticació per contrasenya (5 min)

A la RPi, edita la configuració SSH:

```bash
sudo nano /etc/ssh/sshd_config
# Assegura't que diu:
#   PasswordAuthentication no
#   PubkeyAuthentication yes
#   PermitRootLogin no

# Comprova la sintaxi abans de reiniciar
sudo sshd -t
# Si no escriu res, tot OK

sudo systemctl restart ssh
```

**Compte**: fes això NOMÉS quan estigis segur que la clau funciona. Si no, et quedes fora. Per seguretat, no tanquis la sessió SSH actual fins que n'hagis obert una altra de nova i hagueu comprovat que entra.

## Pas 8: SSH agent per no escriure passphrase (5 min)

Si has posat passphrase a la clau, cada vegada que connectes te la demana. La solució és `ssh-agent`:

```bash
# Inicia l'agent
eval "$(ssh-agent -s)"

# Afegeix la clau (et demanara la passphrase un sol cop)
ssh-add ~/.ssh/id_ed25519

# Comprova quines claus te l'agent
ssh-add -l

# Ara ssh bernat@hortosona ja no et demanara passphrase
ssh bernat@hortosona "echo agent funciona"
```

A Mac i Windows, l'agent sol estar integrat al sistema. A Linux, l'ordre anterior és la forma estàndard.

## Pas 9: Documenta

Crea `book/curs/M1/04-xarxa-ssh-tailscale/configuracio.md` amb:
- La teva IP Tailscale (la RPi i el portàtil).
- La fingerprint de la clau (`ssh-keygen -lf ~/.ssh/id_ed25519.pub`).
- Un parell de captures de `tailscale status`.
- Sortida de `ssh -vv bernat@hortosona` (primeres 20 línies) per veure el que passa per sota.
- Confirmació que has desactivat PasswordAuthentication.

## Validació

Has acabat si:
- [ ] Tailscale instal·lat a RPi i portàtil amb el mateix compte.
- [ ] `tailscale status` mostra ambdós dispositius.
- [ ] `ping hortosona` funciona (MagicDNS actiu).
- [ ] Has generat una clau SSH al portàtil.
- [ ] La clau pública està a `~/.ssh/authorized_keys` de la RPi.
- [ ] `ssh bernat@hortosona` entra sense contrasenya.
- [ ] Has configurat `~/.ssh/config` al portàtil.
- [ ] Has desactivat PasswordAuthentication a la RPi.
- [ ] (Opcional) Has configurat `ssh-agent` per evitar teclejar la passphrase.
- [ ] Has documentat la configuració a `configuracio.md`.

## Per aprofundir

- Activa la 2FA al compte de Tailscale.
- Afegeix un node compartit (un amic) per aprendre ACLs.
- Configura un servidor SSH personalitzat a un port no estàndard (p. ex. 2222).
- Investiga `ssh-agent` per no haver d'introduir la passphrase cada vegada.
- Prova `scp` per copiar fitxers: `scp fitxer.txt bernat@hortosona:~/`.
- Prova `rsync` per sincronitzar carpetes: `rsync -avz carpetes/ bernat@hortosona:~/backup/`.
- Configura `ProxyJump` al config per saltar entre hosts.

## Ves un pas més enllà

**Repte avançat: túnel invers per exposar un servei temporal**.

A vegades vols ensenyar a algú un servei que corre a la teva RPi sense publicar-lo a Internet. Una tècnica elegant és el **port forwarding** via SSH.

Des del portàtil, executa:

```bash
# Exposa el Portainer de la RPi al port 9999 del teu portàtil
ssh -L 9999:localhost:9000 bernat@hortosona -N
```

Ara, si obres `http://localhost:9999` al navegador del portàtil, veuràs el Portainer de la RPi, passant per dins del túnel xifrat de Tailscale + SSH.

Proves que has de fer:
1. Connecta't al túnel.
2. Obre `http://localhost:9999` al navegador del portàtil.
3. Comprova que tens el Portainer.
4. Fes `Ctrl+C` per tancar el túnel.
5. Comprova que el port ja no respon.

Això és la base de moltes eines com VSCode Remote, portainer agent, etc. Documenta al teu `configuracio.md` què has après.
