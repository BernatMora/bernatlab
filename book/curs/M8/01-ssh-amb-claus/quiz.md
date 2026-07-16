# Quiz - M8 Cap 1: SSH amb claus

## Pregunta 1
Quantes claus es generen amb `ssh-keygen -t ed25519`?

- [ ] 1 (una sola clau compartida)
- [x] 2 (una privada i una publica)
- [ ] 3 (inclou una de backup)
- [ ] 4 (clau per cada algoritme)

## Pregunta 2
Quina clau NO has de compartir mai amb ningu?

- [ ] La clau publica
- [x] La clau privada
- [ ] Totes dues son igual de segures
- [ ] Cap de les dues, son secretes

## Pregunta 3
Quin algoritme es recomana actualment per a claus SSH?

- [ ] RSA
- [ ] DSA
- [x] ed25519
- [ ] AES

## Pregunta 4
On es copia la clau publica a la RPi?

- [x] ~/.ssh/authorized_keys
- [ ] ~/.ssh/id_ed25519
- [ ] /etc/ssh/sshd_config
- [ ] ~/.bashrc

## Pregunta 5
Quina comanda copies la teva clau publica a la RPi desde Windows?

- [x] type $env:USERPROFILE\.ssh\id_ed25519.pub | ssh ...
- [ ] copy .ssh\id_ed25519.pub
- [ ] scp .ssh\id_ed25519.pub bernat@hortosona:
- [ ] rsync -av .ssh bernat@hortosona:

## Pregunta 6
Perque Serveix la passphrase de la clau?

- [ ] Es la contrasenya del servidor
- [x] Protegeix la clau privada si el teu PC es robat
- [ ] Es un nom de usuari alternatiu
- [ ] Es per a connexions multiples

## Pregunta 7
Quins permisos ha de tenir `~/.ssh/authorized_keys`?

- [ ] 777 (llegir, escriure, executar per tothom)
- [ ] 644
- [x] 600
- [ ] 755

## Pregunta 8 (oberta)
Explica amb les teves paraules per que les claus SSH son mes segures que les contrasenyes tradicionals.

Pistes:
- Quants caracters te una contrasenya tipica? 12-20?
- Quants bits te una clau ed25519? Mils.
- Quant temps trigaries a trencar cada una per brute force?

## Pregunta 9 (oberta)
Imagina que perds el portatil on tens la clau privada. Que hauries de fer?

Pistes:
- La clau es pot revocar al servidor?
- Que passa amb altres dispositius que tenien la mateixa clau?
- Com pots prevenir aquest problema en el futur?

## Pregunta 10 (oberta)
Per que et recomano desactivar `PasswordAuthentication yes` despres de configurar les claus?

Pistes:
- Que passa si nomes tens autenticacio per clau?
- Que passa si algú encerta la teva contrasenya per casualitat?
- Quin es el "attack surface" en cada cas?
