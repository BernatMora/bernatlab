# Resum - Capitol 1: Amenaces comunes al servidor

## La idea clau

Una Raspberry Pi exposada a Internet (encara que sigui a traves de Tailscale) esta sotmesa a un flux constant d'amenaces automatitzades. No es paranoia: son bots que escanegen totes les adreces IP del planeta cada pocs minuts. Si el servidor te el port 22 obert, **ja t'estan atacant**, tant si ho veus com si no. Aquest capitol es per entendre quines son aquestes amenaces, com es manifesten, i quina es la superficie d'atac de la RPi del BernatLab.

## La superficie d'atac del BernatLab

La "superficie d'atac" es el conjunt de punts per on un atacant podria entrar. A la nostra RPi, de partida es aquesta:

- **Port 22 (SSH)**: obert per defecte a totes les IP publiques.
- **Port 80/443 (HTTP/HTTPS)**: si hi ha un reverse proxy com Nginx o Caddy.
- **Serveis Dockers exposats**: Home Assistant, Portainer, Gitea, etc.
- **Tailscale**: xarxa privada WireGuard, pero si les ACLs son permissives, es una porta oberta igual.
- **Subdominis DNS**: si tens un domini tipus `bernatlab.cat`, els bots el troben rapid.

A la practica, el risc mes gran es **SSH**, perque es l'entrada mes universal i on mes eines d'atac automatic existeixen.

## SSH bruteforce: el perill numero 1

Un atac de **bruteforce** consisteix a provar milers de combinacions d'usuari i contrasenya fins a encertar la bona. Eines com **Hydra**, **Medusa** o **SSHPass** automatitzen el proces. Els bots mes sofisticats fan **credential stuffing**: proven combinacions conegudes (email+contrasenya) que han fugit d'altres incidents.

Com es manifesta? Mira-ho tu mateix:

```bash
# Compta quants intents fallits ha tingut SSH desde l'inici
sudo journalctl -u ssh --no-pager | grep "Failed password" | wc -l

# Ultims 20 intents
sudo journalctl -u ssh -n 20 | grep "Failed"

# Usuaris mes intentats
sudo journalctl -u ssh --no-pager | grep "Failed password" | awk '{print $9}' | sort | uniq -c | sort -rn | head
```

En una RPi nova, en 24 hores pots tenir **milers** d'intents. Els mes comuns van contra `root`, `pi`, `admin`, `ubuntu`, `user`, `test`, `oracle`, `postgres`. Son noms per defecte que els bots coneixen be.

## Ports oberts: el nmap dels dolents

Un cop un bot sap la teva IP, fa un **port scan** per veure quins serveis exposes. L'eina es diu **nmap**, i n'hi ha una versio "dolenta" que fan servir tots els scripts kiddies:

```bash
# El mateix que farien contra la teva RPi (desde un altre equip)
nmap -sV -p 1-1000 bernatlab.ddns.net

# Escaneig rapid dels 100 ports mes comuns
nmap -F bernatlab.ddns.net
```

Si el resultat es:

```
22/tcp   open  ssh      OpenSSH 9.2
80/tcp   open  http     nginx
443/tcp  open  https    nginx
8080/tcp open  http     Node.js
```

... ja saben exactament on atacar. Per això un dels principis basics es **no exposar mes del que cal**. Cada port obert es un risc.

Aixo es el principi de **minim privilege** aplicat a la xarxa: obrir només els ports estrictament necessaris i tancar la resta.

## Vulnerabilitats conegudes: CVE

Quan es descobreix una fallada en un programa (un bug de seguretat, una porta trasera), se li assigna un identificador unic: el **CVE** (Common Vulnerabilities and Exposures). Per exemple, **CVE-2024-6387** es una vulnerabilitat recent a OpenSSH que permet executar codi remot.

Com saber si el teu sistema te vulnerabilitats? Hi ha eines com:

- `apt list --upgradable`: quins paquets del sistema tenen versions noves (sovint amb pegats de seguretat).
- `docker scan bernatlab-api:latest`: Trivy, Snyk, Grype. Escaneja imatges Docker.
- **Debian Security Tracker**: https://security-tracker.debian.org/ per buscar CVEs per paquet.

No cal obsessionar-se, pero si tenir un **sistema d'alertes basic**: saber quan hi ha un pegat critic i aplicar-lo en dies, no en mesos.

## Amenaces mes enlla del SSH

Tot i que SSH es el vector mes explotat, n'hi ha d'altres que tambe hem de considerar:

- **Exploits en aplicacions web**: si tens Home Assistant, Gitea, Nextcloud... cadascun te la seva historia de CVEs.
- **Docker APIs exposades**: mai exposar el socket de Docker (`/var/run/docker.sock`) sense autenticacio.
- **Credencials per defecte**: canviar `admin/admin` de Home Assistant, Portainer, etc. **immediatament**.
- **DNS rebinding**: atac contra serveis que nomes filtren per nom de domini, no per IP.
- **Supply chain**: imatges Docker de qualitat dubtosa poden contenir backdoors.
- **Acces fisic**: algú amb acces a la RPi pot extreure la SD i llegir les dades (si no estan xifrades).

## El model d'amenaca del BernatLab

No tothom te les mateixes amenaces. Al BernatLab el model es:

- **Confidencialitat alta** (dades de sensors, fitxers personals).
- **Integritat alta** (vull que els meus backups no estiguin corromputs).
- **Disponibilitat mitjana** (no es critic si la RPi cau 1 hora).
- **Atacant tipus**: bots automatitzats, curiosos, possiblement algun script kiddie.
- **NO soc objectiu d'un APT**: no cal paranoia de nivell estatal.

Això ens permet triar un nivell de seguretat **bo** pero no **paranòic**. Per exemple: HTTPS si, Tailscale si, fail2ban si, certificat EV no cal. Cal ser **pragmatic**.

## Com defensar-se: visio general

Les defenses que veurem al llarg del modul son:

1. **Xarxa privada amb Tailscale** (Cap 2): el servidor nomes escolta a la xarxa VPN, no a Internet.
2. **SSH hardening** (Cap 3): deshabilitar password, port no estandard, claus forçades.
3. **Firewall** (Cap 4): ufw o nftables per tancar tot el que no cal.
4. **TLS** (Cap 5): xifrar les comunicacions HTTP.
5. **Secrets** (Cap 6): no posar contrasenyes al codi ni al git.
6. **Backups xifrats** (Cap 7): una copia de seguretat que nomes jo puc restaurar.
7. **Monitoratge** (Cap 8): saber quan algú intenta entrar.
8. **Actualitzacions** (Cap 9): pegat de seguretat rapid.
9. **Auditoria** (Cap 10): revisar periodicament que tot esta en ordre.

Aquestes defenses son **capes d'una ceba**: cap es suficient per si sola, pero juntes formen una barrera robusta.

## Connexions amb altres capitols

- **M1 Cap 4** - Xarxa i SSH: els basics que ja coneixem.
- **M3 Cap 9** - Privadesa i xifrat: el xifratge es la base d'algunes defenses.
- **M2 Cap 6** - Seguretat en contenidors: molt relacionat amb el que veurem.
- **M8 Cap 1** - SSH amb claus: ja ho tens mig fet, ara cal enfortir-ho.
- **Cap 2 d'aquest modul** - Tailscale es la primera linea de defensa.

## Comandes utils

```bash
# Comprovar intents de login fallits
sudo lastb | head -20

# Qui esta connectat ara
who
w

# Veure totes les connexions TCP actives
ss -tan

# Buscar CVEs coneguts al teu sistema
sudo apt list --upgradable 2>/dev/null | grep -i security

# Escanejar la teva propia RPi desde fora
nmap -sV localhost  # nomes els serveis locals
```
