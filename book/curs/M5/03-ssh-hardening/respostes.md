# Respostes - Capitol 3: SSH Hardening

> Mira les respostes DESPRES d'haver fet el qüestionari.

## Pregunta 1: Que vol dir SSH hardening?

**Resposta correcta**: Aplicar mesures de seguretat addicionals al servei SSH.

**Explicacio**: Hardening es una paraula anglesa que vol dir "endurir". En seguretat, vol dir aplicar configuracions que redueixen la superficie d'atac d'un servei. En el cas de SSH, vol dir desactivar opcions perilloses (com el login amb contrasenya), limitar qui pot accedir, i bloquejar els bots. Es la diferencia entre tenir la porta de casa oberta o tancada amb clau.

---

## Pregunta 2: PermetrRootLogin no

**Resposta correcta**: No permetre que l'usuari root es conecti directament per SSH.

**Explicacio**: Si un atacant es connecta com a root, te control total del sistema. Es molt millor que es conecti com a usuari normal i faci `sudo` nomes quan cal. Aixi encara que la contrasenya es filtri, l'atacant nomes te un usuari limitat. Es un principi classic de minim privilege: mai treballis com a root.

---

## Pregunta 3: Comanda per generar claus

**Resposta correcta**: `ssh-keygen -t ed25519 -C "bernat@bernatlab"`.

**Explicacio**: Ed25519 es l'algoritme modern preferit. Es mes rapid, mes petit (claus de 68 caracters) i mes segur que RSA. `-t ed25519` especifica el tipus, `-C` posa un comentari per identificar la clau. Et demanara on guardar-la (~/.ssh/id_ed25519 per defecte) i una passphrase per protegir-la.

---

## Pregunta 4: PasswordAuthentication no

**Resposta correcta**: Desactivar el login amb contrasenya i forçar l'us de claus.

**Explicacio**: Amb `PasswordAuthentication no`, nomes les claus SSH podran entrar. Encara que un atacant conegui el teu usuari i la teva contrasenya, no podra entrar perque nomes s'accepten claus. Es la mesura mes important de SSH hardening. Es clar que primer has d'haver copiat la clau publica al servidor amb `ssh-copy-id`.

---

## Pregunta 5: Que es fail2ban?

**Resposta correcta**: Una eina que bloqueja IPs que fan massa intents fallits.

**Explicacio**: Fail2ban llegeix els logs (per defecte `/var/log/auth.log` o `journalctl`) i, quan detecta N intents fallits des de la mateixa IP, afegeix una regla temporal al firewall per bloquejar-la. Per exemple, 5 intents fallits en 10 minuts = bloqueig durant 1 hora. Es un complement a Tailscale, pero es bona practica tenir-lo igual per si Tailscale falla.

---

## Pregunta 6: Port 2222

**Resposta correcta**: Reduir el soroll dels scans automatic, pero NO es una mesura de seguretat real.

**Explicacio**: Canviar el port 22 a un altre (per exemple 2222 o 5022) no millora la seguretat. Un escaneig de ports basic (nmap) el trobara en 5 segons. Pero redueix el volum de scans automatic: la majoria de bots nomes miren el 22. Es com posar el nom de l'ascensor en comptes del principal a la porteria: la gent que busca el principal no el troba, pero un lladre amb un mapa de l'edifici, si. No et confius d'aixo sol.

---

## Pregunta 7: MaxAuthTries

**Resposta correcta**: El maxim numero d'intents de contrasenya per sessio.

**Explicacio**: `MaxAuthTries 3` vol dir que si fallen 3 autenticacions seguides, SSH talla la conexio. Es bona practica posar un numero baix (3-5) per dificultar el bruteforce. Combinat amb fail2ban, fa que un atacant tingui molt poc marge d'error.

---

## Pregunta 8: Fitxer authorized_keys

**Resposta correcta**: `~/.ssh/authorized_keys`.

**Explicacio**: Aquest fitxer conte les claus publiques que poden entrar amb aquest usuari. Quan un client intenta connectar, SSH mira si la clau publica del client esta en aquest fitxer. Si hi es, deixa entrar. Es la versio SSH del "la clau del client esta al clauer del servidor". El permisos han de ser 600 (lectura i escriptura nomes per al propietari).

---

## Pregunta 9 (oberta): Configuracio SSH

**Resposta model**:

Una configuracio de `/etc/ssh/sshd_config` dura i robusta per al BernatLab tindria aixo:

```sshconfig
# Port personalitzat per reduir scans (no es seguretat, nomes reduccio de soroll)
Port 5022

# Nomes IPv4 (evita soroll IPv6 si no el fem servir)
AddressFamily inet

# Desactivar login directe com a root
PermitRootLogin no

# Desactivar login amb contrasenya
PasswordAuthentication no
ChallengeResponseAuthentication no
UsePAM yes   # cal per a alguns casos

# Autenticacio nomes amb claus publiques
PubkeyAuthentication yes
AuthenticationMethods publickey

# Maxim 3 intents per conexio
MaxAuthTries 3

# Tallar conexions que tarden massa a autenticar
LoginGraceTime 30

# Limitar el numero de sessions concurrents
MaxSessions 3

# X11 forwarding nomes si cal
X11Forwarding no

# Port forwarding nomes si cal
AllowTcpForwarding no
GatewayPorts no

# No deixar que el client envii variables d'entorn perilloses
AcceptEnv LANG LC_*

# Banner (missatge legal abans d'autenticar)
Banner /etc/issue.net

# Subsistema SFTP nomes si cal
Subsystem sftp /usr/lib/openssh/sftp-server
```

Per que cada canvi importa:

- **`Port 5022`**: redueix ~95% dels scans automatic que miren nomes el 22.
- **`PermitRootLogin no`**: si l'atacant entra, no sera root. Hauria d'escalar privilegis (mes dificil).
- **`PasswordAuthentication no`**: nomes poden entrar amb claus. Bruteforce impossible.
- **`MaxAuthTries 3`**: poca paciencia per a un atacant.
- **`LoginGraceTime 30`**: si no t'autentiques en 30 segons, fora.
- **`MaxSessions 3`**: limita quantes connexions pot obrir un sol client.
- **`X11Forwarding no`**: reduim superficie d'atac. Si no sabem que es, no cal.
- **`AllowTcpForwarding no`**: no permetre fer tunnels per saltar-se ACLs.

Aixo es la configuracio que aplico jo a la RPi. Pero sempre **primer** configuro i poso en marxa amb una **segona sessio SSH oberta** per si la primera deixa de funcionar. Si nomes en tens una oberta i fas mal la configuracio, et quedes fora.

---

## Pregunta 10 (oberta): fail2ban al BernatLab

**Resposta model**:

Al BernatLab, amb Tailscale activat, fail2ban es una **defensa secundaria**. Perque? Perque Tailscale ja filtra l'accés: nomes les IP del tailnet poden intentar connectar-se. Si una maquina Tailscale es compromesa i fa bruteforce, fail2ban la pot parar. Pero Tailscale ja ens donaria l'avis "un nou dispositiu s'ha afegit" si fos un atacant real.

Aixo vol dir que fail2ban no es **imprescindible**, pero es **recomanable**. El configuraria amb aquestes directrius:

**Politica per defecte**: 5 intents fallits en 10 minuts = bloqueig durant 1 hora. Es prou agressiu per parar atacs reals, pero no tan agressiu com per bloquejar-te a tu mateix si tens un typo.

**Accions**: bloqueig via ufw (o iptables), perque ja el tindrem configurat. Fail2ban te plantilles predefinides per a SSH, Apache, Nginx, Postfix, etc. Usarem nomes la de SSH.

**Whitelist**: cal evitar que fail2ban bloquegi Tailscale (podria passar si l'IP Tailscale fos falsa o fluctuants). Configurar `/etc/fail2ban/jail.local` amb `ignoreip = 100.64.0.0/10` (el rang de Tailscale).

**Monitors**: vull veure els bloquejos. Per tant, activar `destemail = bernat@bernatlab.cat` i `action = %(action_mw)s` (que envia correu + afegeix regla al firewall). Pero no vull que m'inundi de correus: nomes un correu diari de resum.

**Configuracio de la preson SSH**:

```ini
[sshd]
enabled = true
port    = ssh
filter  = sshd
logpath = %(sshd_log)s
maxretry = 5
findtime = 600
bantime  = 3600
```

Aixo es basic pero efectiu. Combinat amb Tailscale (capes 1 i 2) i SSH sense contrasenyes (capa 3), tinc tres capes contra el bruteforce. Si tot falla, encara puc veure qui ha intentat entrar via els logs i bloquejar manualment.

---

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum i fer l'exercici practic.
- **3-4 encerts**: Refes l'exercici validant ambdues sessions obertes.
- **0-2 encerts**: Practica amb un VPS de prova abans de tocar la RPi.

## Que fer si has encertat totes

- Passa al **Capitol 4** (Firewall amb ufw).
- Investiga l'eina **CrowdSec**, una alternativa moderna a fail2ban col·laborativa.
- Configura **alertes** amb Prometheus o Healthchecks per saber quan fail2ban ha bloquejat.
- Llegeix el manual oficial: `man sshd_config` (son centenars de pagines pero es or pur).
