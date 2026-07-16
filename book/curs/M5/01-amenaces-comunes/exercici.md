# Exercici practic - Capitol 1: Amenaces comunes

> 30-45 min · Real al teu sistema

## Objectiu

Auditar l'estat actual de seguretat de la RPi del BernatLab: veure quins intents d'intrusio ha rebut, quins ports te oberts, i quin perfil d'amenaces tenim. Acabaras amb un document "baseline" que et servira com a referencia per mesurar millores.

## Requisits

- Acces SSH a la RPi amb permissos sudo
- 30-45 minuts
- Coneixement basic de la terminal (ja ho tens del M1)

## Pas 1: Inventari de serveis i ports (10 min)

Connecta't a la RPi i fes un inventari del que esta escoltant a la xarxa:

```bash
# Tots els ports TCP oberts
sudo ss -tlnp

# Versio mes humana amb nom de servei
sudo ss -tlnp | awk 'NR>1 {print $4, $6}'

# Que esta escoltant nomes per IP, no per unix socket
sudo lsof -i -P -n | grep LISTEN
```

Crea un fitxer `inventari-seguretat.md` al teu repo d'Obsidian amb el que has trobat. Anota cada servei i el seu port.

## Pas 2: Comptar els intents de login fallits (10 min)

Mira quanta gent ha intentat entrar al teu servidor:

```bash
# Total d'intents fallits
sudo journalctl -u ssh --no-pager | grep "Failed password" | wc -l

# Ultims 50 intents
sudo journalctl -u ssh --no-pager | grep "Failed password" | tail -50

# Top 10 usuaris mes intentats
sudo journalctl -u ssh --no-pager | grep "Failed password" | awk '{print $9}' | sort | uniq -c | sort -rn | head

# Adreces IP dels atacants (top 20)
sudo journalctl -u ssh --no-pager | grep "Failed password" | awk '{print $11}' | sort | uniq -c | sort -rn | head -20
```

Anota a l'inventari:
- Total d'intents fallits en tota la historia
- Total d'IPs uniques
- Usuaris mes atacats

## Pas 3: Escanejar la teva propia maquina (10 min)

Des de la propia RPi, mira com es veu des de fora:

```bash
# Instal·la nmap
sudo apt install -y nmap

# Escaneig basic dels 1000 ports mes comuns
nmap localhost

# Escaneig amb deteccio de versio
nmap -sV localhost

# Si tens Tailscale actiu, mira tambe la IP de Tailscale
tailscale ip -4
nmap $(tailscale ip -4)
```

Compara el resultat amb el que vas obtenir al Pas 1. Coincideix? Hi ha serveis que no sabies que estaven oberts?

## Pas 4: Buscar patrons sospitosos (10 min)

Mira si algu ha aconseguit entrar o si hi ha senyals d'activitat rara:

```bash
# Logins exitosos
sudo last -20

# Logins fallits (inclou SSH, TTY, etc)
sudo lastb -20

# Autenticacions desde IPs extranyes
sudo journalctl -u ssh | grep "Accepted"

# Usuaris amb shell interactiva
grep -v "nologin\|false" /etc/passwd

# Processos actius sospitosos
ps auxf | head -50

# Connexions xarxa actives cap a fora (pot revelar malware)
sudo ss -tnp | grep ESTAB
```

Anota qualsevol cosa que no reconeguis. Si hi ha molta activitat, no t'espantis: pot ser el propi sistema fent actualitzacions, backups remots, etc.

## Pas 5: Redacta el baseline (5 min)

Al fitxer `inventari-seguretat.md`, escriu una seccio "Baseline" amb:

- Data i hora de l'auditoria
- Versio del sistema (`cat /etc/os-release`)
- Versio del kernel (`uname -r`)
- Llista de serveis i ports
- Total d'intents SSH fallits
- Adreces IP atacants principals
- Connexions actives actuals
- Conclusions: quines son les prioritats (molt probablement: SSH hardening + firewall)

## Validacio

- [ ] Has fet un inventari complet de serveis i ports oberts.
- [ ] Has comptabilitzat els intents de login fallits.
- [ ] Has identificat els usuaris mes atacats.
- [ ] Has fet un escaneig amb nmap i l'has comparat amb l'inventari.
- [ ] Has creat el document `inventari-seguretat.md` amb el baseline.

## Per aprofundir

- Instal·la **Lynis** (`sudo apt install lynis && sudo lynis audit system`) per una auditoria automatica mes completa.
- Mira les ultimes 100 IPs que t'han atacat a https://www.abuseipdb.com/ (la web te una API per automatitzar-ho).
- Prova `whois IP_ATACANT` per veure d'on venen els atacs.
- Si tens temps, configura un **honeypot** amb `cowrie` per veure que fan els atacants un cop dins (només en un entorn aillat, mai en produccio).
