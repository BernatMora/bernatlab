# Qüestionari - Capitol 3: SSH Hardening

> 10 preguntes · ~15 min

## Pregunta 1
Que vol dir "SSH hardening"?

- [ ] Instal·lar la versio mes recent d'OpenSSH
- [x] Aplicar mesures de seguretat addicionals al servei SSH
- [ ] Desinstal·lar SSH del servidor
- [ ] Canviar la IP del servidor

## Pregunta 2
Que fa la directiva `PermitRootLogin no`?

- [ ] Desactiva l'usuari root del sistema
- [x] No permetre que l'usuari root es conecti directament per SSH
- [ ] Permet que root es conecti nomes amb clau
- [ ] Activa el compte root amb una contrasenya per defecte

## Pregunta 3
Quina comanda genera un parell de claus SSH modernes?

- [ ] `ssh-keygen -t rsa -b 4096`
- [x] `ssh-keygen -t ed25519 -C "bernat@bernatlab"`
- [ ] `openssl genrsa 2048`
- [ ] `gpg --gen-key`

## Pregunta 4
Que fa la directiva `PasswordAuthentication no`?

- [ ] Canvia la contrasenya de l'usuari SSH
- [x] Desactivar el login amb contrasenya i forçar l'us de claus
- [ ] Fa que les contrasenyes siguin mes segures
- [ ] Activa la doble autenticacio per contrasenya

## Pregunta 5
Que es fail2ban?

- [ ] Un antivirus per Linux
- [x] Una eina que bloqueja IPs que fan massa intents fallits
- [ ] Un sistema de fitxers xifrat
- [ ] Un servei de correu electronic segur

## Pregunta 6
Per que es recomana canviar el port SSH de 22 a 5022?

- [ ] Perque 5022 es un port magic
- [x] Per reduir el soroll dels scans automatic, pero NO es una mesura de seguretat real
- [ ] Perque SSH nomes funciona al port 5022
- [ ] Perque es mes rapid

## Pregunta 7
Que controla la directiva `MaxAuthTries`?

- [ ] El maxim de vegades que pots fer servir una clau
- [x] El maxim numero d'intents de contrasenya per sessio
- [ ] El temps maxim que pot durar una sessio
- [ ] El maxim de fitxers que pots transferir

## Pregunta 8
A quin fitxer copiem la clau publica per permetre l'acces a un usuari?

- [ ] /etc/ssh/sshd_config
- [x] ~/.ssh/authorized_keys
- [ ] /root/.ssh/id_rsa
- [ ] /var/log/auth.log

## Pregunta 9 (oberta)
Escriu una configuracio `/etc/ssh/sshd_config` que aplicaries al BernatLab. Explica per que cada línia es important.

Pistes per respondre:
- Canvia el port.
- Desactiva el login de root.
- Desactiva PasswordAuthentication.
- Limita MaxAuthTries.
- Desactiva X11Forwarding i AllowTcpForwarding.
- Explica per que cada canvi ajuda (o no) a la seguretat.

## Pregunta 10 (oberta)
Com configuraries fail2ban al BernatLab tenint en compte que ja tens Tailscale? Que whitelist posaries? Que bantime? Explica la teva logica.

Pistes per respondre:
- Tailscale ja filtra molt acces, pero fail2ban es la capa extra.
- Has de posar el rang 100.64.0.0/10 a ignoreip.
- Explica per que posaries un maxretry de 5 (ni massa agressiu ni tou).
- Esmenta com vols veure els bloquejos (logs, correu, etc).


## Pregunta 11
Per que es mes segur utilitzar claus SSH que contrasenyes? Explica el per que tecnic.

**Pistes**: Pistes: Longitud, criptografia asimetrica, brute force, keylogger.

## Pregunta 12
Quina relacio hi ha entre 'PermitRootLogin no' i la seguretat del teu servidor? Pensa en un atac.

**Pistes**: Pistes: Superusuari, escalada, audit, responsabilitat.

## Pregunta 13
Si un company te demana accedir al teu servidor, quina seria la millor manera? Pensa en les Bones Practiques.

**Pistes**: Pistes: Usuaris separats, claus, auditar, revocar.


## Pregunta 14 (oberta amb pistes)
Per que es mes segur utilitzar claus SSH que contrasenyes

**Pistes**: pensa en com aplicaries aquest concepte al teu hort IoT amb la teva RPi (hortosona, 100.115.134.76).
## Pregunta 15 (oberta amb pistes)
Quina relacio hi ha entre PermitRootLogin no i la seguretat del teu servidor

**Pistes**: pensa en com aplicaries aquest concepte al teu hort IoT amb la teva RPi (hortosona, 100.115.134.76).
