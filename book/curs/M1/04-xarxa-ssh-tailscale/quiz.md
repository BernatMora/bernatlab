# Qüestionari — Capítol 4: Xarxa, SSH i Tailscale

> 15 preguntes · ~20 min

## Pregunta 1
Quin port usa SSH per defecte?

- [ ] 21
- [ ] 80
- [x] 22
- [ ] 443

## Pregunta 2
Quin és el format correcte per connectar-se per SSH a l'usuari `bernat` de la màquina `hortosona`?

- [ ] ssh hortosona@bernat
- [x] ssh bernat@hortosona
- [ ] connect bernat hortosona
- [ ] telnet bernat:hortosona

## Pregunta 3
Què és Tailscale?

- [ ] Un sistema operatiu
- [ ] Un client de correu
- [x] Una VPN basada en WireGuard
- [ ] Un antivirus

## Pregunta 4
Quin és el rang d'IPs que assigna Tailscale per defecte?

- [ ] 192.168.0.0/16
- [ ] 10.0.0.0/8
- [x] 100.64.0.0/10
- [ ] 172.16.0.0/12

## Pregunta 5
Quina ordre genera un parell de claus SSH?

- [ ] ssh newkey
- [x] ssh-keygen
- [ ] ssh-add
- [ ] ssh-keypair

## Pregunta 6
Què és MagicDNS?

- [ ] Un servidor DNS extern
- [x] La funcionalitat de Tailscale que resol noms de màquina a IP automàticament
- [ ] Un protocol de seguretat SSH
- [ ] Un servei de noms de domini gratuït

## Pregunta 7
Quin avantatge principal té Tailscale respecte a obrir ports al router?

- [ ] És més ràpid
- [x] No cal tocar la configuració del router (NAT/port forwarding)
- [ ] Dona IPv6
- [ ] Dona una IP pública fixa

## Pregunta 8
On es desa la clau pública del servidor quan autoritzem una clau?

- [ ] /etc/ssh/keys
- [x] ~/.ssh/authorized_keys
- [ ] /var/ssh/keys
- [ ] /home/bernat/.sshkey

## Pregunta 9
Quin algorisme de clau SSH és el recomanat actualment per defecte?

- [ ] RSA 1024
- [ ] RSA 4096
- [x] ed25519
- [ ] DSA

## Pregunta 10
Què fa l'ordre `ssh-copy-id bernat@hortosona`?

- [ ] Copia la clau privada al servidor
- [x] Copia la clau pública al servidor i l'afegeix a authorized_keys
- [ ] Crea una nova clau SSH
- [ ] Esborra totes les claus del servidor

## Pregunta 11
Quin és el risc d'obrir el port 22 d'SSH a Internet (sense Tailscale ni cap VPN)?

- [ ] Cap, és segur
- [x] Milers d'atacs de força bruta diaries des d'IPs de tot el món
- [ ] Només és lent
- [ ] Consum excessiu de CPU

## Pregunta 12
Què és el fitxer `~/.ssh/config`?

- [ ] Un fitxer de claus
- [x] Un fitxer on definir àlies i opcions per host SSH
- [ ] El log de connexions SSH
- [ ] La configuració del dimoni SSH del servidor

## Pregunta 13 (oberta)
Explica amb les teves paraules: per què és millor usar claus SSH que contrasenya? Enumera almenys 2 motius tècnics.

Pistes per respondre:
- Longitud de la clau vs. contrasenya típica.
- Què passa si la contrasenya és curta o reutilitzada.
- Possibilitat d'automatitzar tasques sense contrasenya.

## Pregunta 14 (oberta)
Descriu el flux complet: vols accedir a la RPi `hortosona` des del teu portàtil quan ets a una cafeteria. Quins passos has fet prèviament perquè això funcioni? Quines ordres executes en el moment de connectar?

Pistes per respondre:
- Què necessites tenir instal·lat al portàtil?
- Què necessites tenir a la RPi?
- Quina diferència hi ha entre IP local (192.168.x) i IP Tailscale (100.x)?
- Contrasenya vs. clau.
- Què passaria si la xarxa WiFi de la cafeteria és hostil (man-in-the-middle)?

## Pregunta 15 (oberta)
Imagina que perds el portàtil on tens la teva clau privada SSH. Què hauries de fer immediatament per protegir el BernatLab? Enumera les accions en ordre de prioritat.

Pistes per respondre:
- Què pot fer algú amb la teva clau privada?
- Què hauries de revocar?
- Què hauries de regenerar?
- Com evites que això passi un altre cop (passphrase, 2FA, backup de la clau)?
