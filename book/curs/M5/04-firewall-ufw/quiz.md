# Qüestionari - Capitol 4: Firewall i ufw

> 10 preguntes · ~15 min

## Pregunta 1
Que es un firewall?

- [ ] Un antivirus per servidors
- [x] Un programa que filtra el trafic de xarxa segons unes regles
- [ ] Un sistema de fitxers xifrat
- [ ] Un servei de correu segur

## Pregunta 2
Que vol dir "deny-by-default"?

- [ ] Que el servidor denega totes les peticions HTTP
- [x] Que tot esta bloquejat per defecte i nomes es permet el que explicitem obrim
- [ ] Que nomes es permeten usuaris autenticats
- [ ] Que el servidor nomes funciona en horari laboral

## Pregunta 3
Que es ufw?

- [ ] Un protocol de xarxa
- [x] Un wrapper d'iptables/nftables amb sintaxi senzilla
- [ ] Un sistema de deteccio d'intrusions
- [ ] Una eina de monitoratge de xarxa

## Pregunta 4
Com permets el port 22 amb ufw?

- [ ] `sudo ufw open 22`
- [x] `sudo ufw allow 22/tcp`
- [ ] `sudo ufw permit 22`
- [ ] `sudo ufw add 22`

## Pregunta 5
Que es la interficie `tailscale0`?

- [ ] La IP publica del servidor
- [x] La interficie de xarxa virtual que Tailscale crea
- [ ] Un nom alternatiu per a eth0
- [ ] Un servei de DNS

## Pregunta 6
Com veus les regles ufw numerades?

- [ ] `sudo ufw list`
- [x] `sudo ufw status numbered`
- [ ] `sudo ufw show`
- [ ] `sudo cat /etc/ufw/rules`

## Pregunta 7
Que passa si executes `sudo ufw default allow incoming`?

- [ ] Es tanca tot el trafic entrant
- [x] Tots els ports queden accessibles des de qualsevol xarxa, com si no tinguesis firewall
- [ ] Nomes SSH queda accessible
- [ ] El sistema es reinicia

## Pregunta 8
Com permetes trafic nomes des de Tailscale?

- [ ] `sudo ufw allow 100.64.0.0/10`
- [x] `sudo ufw allow in on tailscale0`
- [ ] `sudo ufw allow tailscale`
- [ ] `sudo ufw enable tailscale`

## Pregunta 9 (oberta)
Escriu les regles ufw que aplicaries al BernatLab. Inclou politica per defecte, ports essencials, i una regla que limiti l'acces nomes a Tailscale.

Pistes per respondre:
- Comença amb `default deny incoming` i `default allow outgoing`.
- Permet SSH, HTTP, HTTPS pero nomes des de tailscale0.
- Afegeix una regla especifica per a DNS o Home Assistant si cal.
- Explica per que cada regla es a la llista.

## Pregunta 10 (oberta)
Per que tenir ufw si ja tens Tailscale activat? Dona almenys 3 raons tecniques.

Pistes per respondre:
- Defensa en profunditat: dues capes amb responsabilitats diferents.
- Bugs i caigudes: que passa si Tailscale falla?
- Errades de configuracio: que passa si un servei escolta a 0.0.0.0 per error?
- Segmentacio: pots fer que un servei nomes sigui accessible desde la interficie local.


## Pregunta 11
Explica per que un firewall nomes amb la politica per defecte 'deny incoming' ja dona molta seguretat.

**Pistes**: Pistes: Principi de minim, superficie datac, llistes blanques.

## Pregunta 12
Quina relacio hi ha entre ports oberts i serveis exposats? Pensa en el teu hort IoT.

**Pistes**: Pistes: Port 22, port 9443, port 3000, escaneig, servei.

## Pregunta 13
Si nomes tens SSH i Portainer, quines serien les regles UFW mes adients? Escriu-les.

**Pistes**: Pistes: 22/tcp, 9443/tcp, default deny, limit.


## Pregunta 14 (oberta amb pistes)
Per que un firewall nomes amb la politica per defecte deny incoming ja dona molta seguretat

**Pistes**: pensa en com aplicaries aquest concepte al teu hort IoT amb la teva RPi (hortosona, 100.115.134.76).
## Pregunta 15 (oberta amb pistes)
Quina relacio hi ha entre ports oberts i serveis exposats al teu hort IoT

**Pistes**: pensa en com aplicaries aquest concepte al teu hort IoT amb la teva RPi (hortosona, 100.115.134.76).
