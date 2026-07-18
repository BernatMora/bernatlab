# Respostes — Capítol 4: Xarxa, SSH i Tailscale

> Mira les respostes DESPRÉS d'haver fet el qüestionari.

## Pregunta 1: Port SSH

**Resposta correcta**: 22

**Explicació**: SSH estandarditza el port 22. Es pot canviar, però gairebé tothom el deixa per defecte. Altres ports famosos: 21 (FTP), 80 (HTTP), 443 (HTTPS).

## Pregunta 2: Format de connexió SSH

**Resposta correcta**: ssh bernat@hortosona

**Explicació**: El format és `usuari@màquina`. Si s'omet l'usuari, agafa el del shell actual. Si s'omet la màquina, assumeix localhost.

## Pregunta 3: Què és Tailscale?

**Resposta correcta**: Una VPN basada en WireGuard.

**Explicació**: Tailscale és una capa de gestió sobre WireGuard (el protocol VPN modern). Permet crear xarxes privades entre dispositius sense configurar manualment les claus WireGuard. Alternativa: ZeroTier, Nebula, Netmaker.

## Pregunta 4: Rang d'IPs Tailscale

**Resposta correcta**: 100.64.0.0/10

**Explicació**: Tailscale assigna IPs del rang 100.64.0.0/10, que és part del rang CGNAT (Carrier-Grade NAT) reservat per a xarxes intermèdies. Per això la teva RPi té 100.x.y.z.

## Pregunta 5: Generar claus SSH

**Resposta correcta**: ssh-keygen

**Explicació**: `ssh-keygen` genera el parell. `-t ed25519` és l'algoritme modern recomanat (curt, ràpid, segur). Alternatives: `-t rsa -b 4096` (clàssic però més llarg). `ssh-add` afegeix claus a l'agent.

## Pregunta 6: MagicDNS

**Resposta correcta**: La funcionalitat de Tailscale que resol noms de màquina a IP automàticament.

**Explicació**: MagicDNS fa que puguis fer `ssh bernat@hortosona` i Tailscale tradueixi "hortosona" a 100.x.y.z sense configurar res. També permet `hortosona.tailnet.ts.net` o noms personalitzats.

## Pregunta 7: Avantatge de Tailscale

**Resposta correcta**: No cal tocar la configuració del router (NAT/port forwarding).

**Explicació**: Obrir ports al router (port forwarding) exposa serveis a Internet i és arriscat. Tailscale crea un túnel xifrat directament entre dispositius, sense passar pel router. Resultat: més segur, més fàcil, zero configuració de xarxa.

## Pregunta 8: On es desa la clau pública autoritzada

**Resposta correcta**: ~/.ssh/authorized_keys

**Explicació**: Cada línia del fitxer `~/.ssh/authorized_keys` conté una clau pública autoritzada. Quan et connectes, el servidor comprova si tens la clau privada corresponent. Permisos recomanats: 700 a `.ssh` i 600 a `authorized_keys`.

## Pregunta 9 (oberta): Per què claus SSH millor que contrasenya?

**Resposta model**:

Les claus SSH són superiors a les contrassenyes per diversos motius tècnics:

**1. Longitud i complexitat**: una clau ed25519 té l'equivalent a ~128 bits de seguretat, que es trencaria en trilions d'anys amb força bruta. Una contrasenya típica té 8-12 caràcters amb possibles 70-90 opcions per caràcter, resultant en 50-70 bits d'entropia — atacable en dies/mesos amb hardware dedicat.

**2. Resistència a atacs de diccionari**: les claus SSH no es poden endevinar amb un atac de diccionari perquè no es deriven d'una paraula. Les contrasenyes sí (per molt bones que siguin, hi ha llistes de "123456", "password", etc.). A més, la contrasenya es transmet (o es comprova) cada vegada que entres, cosa que permet atacs de man-in-the-middle si la connexió no està ben configurada.

**3. No es poden filtrar fàcilment**: la clau privada mai surt del teu portàtil. Si un servidor es compromet, l'atacant veu la clau pública, que no serveix per entrar a cap lloc. Si un servidor amb autenticació per contrasenya es compromet, totes les contrasenyes (reutilitzades o no) queden exposades.

**4. Permet automatitzar**: pots fer còpies de seguretat, rsync, deploys continus sense escriure la contrasenya cada vegada. Amb una passphrase + ssh-agent, tens la comoditat de no haver d'escriure-la sempre, però la seguretat d'una clau.

**5. Auditable**: pots veure exactament quines claus estan autoritzades a cada servidor, i revocar-les individualment (només cal esborrar la línia de `authorized_keys`).

## Pregunta 10 (oberta): Flux complet des d'una cafeteria

**Resposta model**:

**Preparació prèvia (un sol cop, dies o setmanes abans)**:

1. **A la RPi del BernatLab**:
   - Instal·lar Tailscale: `curl -fsSL https://tailscale.com/install.sh | sh && sudo tailscale up`. Autenticar-se amb el meu compte.
   - Verificar que SSH està actiu: `sudo systemctl enable --now ssh`.
   - Assegurar-se que el tallafocs permet SSH des de Tailscale: per defecte Tailscale passa, però comprovar amb `sudo ufw status`.

2. **Al portàtil**:
   - Instal·lar Tailscale (https://tailscale.com/download) i autenticar-me amb el MATEIX compte.
   - Generar una clau SSH: `ssh-keygen -t ed25519 -C "bernat@portatil-2026"`.
   - Copiar la clau pública a la RPi amb `ssh-copy-id bernat@hortosona` (o manualment).
   - Configurar `~/.ssh/config` amb l'àlies `hortosona` apuntant a `100.x.y.z`.

3. **A la RPi (opcional però recomanable)**:
   - Desactivar autenticació per contrasenya: editar `/etc/ssh/sshd_config` posant `PasswordAuthentication no` i reiniciar SSH.

**Al moment de connectar (a la cafeteria)**:

1. **Connectar-me a la WiFi de la cafeteria** (obert o amb WPA2).
2. **Activar Tailscale al portàtil**: si no està en background, obrir l'app de Tailscale o fer `sudo tailscale up` (Linux).
3. **Verificar la connexió Tailscale**: `tailscale status` (hauria de veure la RPi amb la IP `100.x.y.z`).
4. **Connectar per SSH**:
   ```bash
   ssh bernat@hortosona
   ```
   Si he posat passphrase a la clau, l'introdueixo. Si no, entro directament. MagicDNS tradueix `hortosona` a la IP Tailscale.
5. **Ja soc dins**: puc fer el que necessiti (mirar logs, reiniciar serveis, etc.) amb el mateix rendiment i seguretat que si fos a casa.

**Diferència clau**: sense Tailscale, l'IP `192.168.1.50` no és accessible des de la cafeteria perquè és una IP privada local. Tailscale em dóna una IP `100.x.y.z` que SÍ és accessible des de qualsevol lloc amb túnel xifrat.

## Què fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum, sobretot la part de claus i Tailscale.
- **3-4 encerts**: Practica SSH manual amb contrasenya abans de passar a claus.
- **0-2 encerts**: Repassem junts el capítol.

## Què fer si has encertat totes

- Passa al **Capítol 5** (Docker des de zero).
- O fes l'**exercici pràctic** per consolidar.
