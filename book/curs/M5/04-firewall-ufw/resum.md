# Resum - Capitol 4: Firewall i ufw

## La idea clau

Un firewall es la barrera que decideix quin trafic pot entrar i sortir del servidor. Tailscale amaga el servidor a Internet, pero el firewall es la **defensa local**: controla quins serveis escolten a quines xarxes, i quines connexions son permeses. A Linux tenim tres tecnologies: **iptables** (el classic), **nftables** (el modern) i **ufw** (l'abstraccio senzilla). Al BernatLab farem servir ufw.

## Que es un firewall

Un firewall es un programa que inspecciona cada paquet de xarxa que entra o surt del sistema i decideix si el deixa passar o el bloqueja. Les regles es defineixen segons:

- **Adreça IP** d'origen o desti.
- **Port** (servei).
- **Protocol** (TCP, UDP, ICMP).
- **Interficie de xarxa** (eth0, tailscale0, wlan0...).

Per defecte, un firewall be configurat ha de ser **deny-by-default**: tot esta bloquejat, i nomes obrim el que realment cal. Aixo redueix la superficie d'atac: si un servei escolta en un port que no hem obert explicitament, es inaccessible, encara que s'hagi configurat malament.

## iptables, nftables, ufw

A Linux tenim tres maneres de fer firewall:

- **iptables**: el classic. Funciona, pero la sintaxi es feixuga i les regles son llargues. Es mantingut per compatibilitat.
- **nftables**: el successor modern d'iptables. Sintaxi mes neta, mes rapid, suporta mes funcionalitats. Es el futur.
- **ufw** (Uncomplicated Firewall): una eina que genera regles d'iptables o nftables per sota, pero amb una sintaxi molt mes simple. Es la que usarem al BernatLab.

Per veure quina usa ufw al teu sistema:

```bash
sudo update-alternatives --query iptables
# o
sudo iptables --version
# Si diu "nf_tables" es que nftables es el backend
```

## ufw: comandes basiques

Instal·lat per defecte a Ubuntu/Raspberry Pi OS, si no:

```bash
sudo apt install ufw
```

Comandes essencials:

```bash
# Estat
sudo ufw status
sudo ufw status verbose
sudo ufw status numbered

# Politica per defecte
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Permetre un port
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Permetre un port nomes a una IP
sudo ufw allow from 192.168.1.50 to any port 22

# Permetre nomes a Tailscale
sudo ufw allow in on tailscale0 to any port 22

# Denegar un port explicitament
sudo ufw deny 3306

# Eliminar una regla
sudo ufw delete allow 80/tcp
sudo ufw delete 3

# Activar / desactivar
sudo ufw enable
sudo ufw disable

# Reset (nuclear)
sudo ufw reset
```

## Aplicar ufw al BernatLab

Pas a pas (assegura't d'estar per Tailscale o amb consola fisica):

```bash
# 1. Politica per defecte
sudo ufw default deny incoming
sudo ufw default allow outgoing

# 2. SSH (important!)
sudo ufw allow 22/tcp comment "SSH"

# 3. Web
sudo ufw allow 80/tcp comment "HTTP"
sudo ufw allow 443/tcp comment "HTTPS"

# 4. Tailscale: permetre tot el trafic desde la xarxa Tailscale
sudo ufw allow in on tailscale0

# 5. DNS local
sudo ufw allow in on tailscale0 to any port 53

# 6. Activar
sudo ufw enable
# Et dira "Command may disrupt existing ssh connections. Proceed (y|n)?"
# Digues y nomes si estas connectat per Tailscale o tens consola fisica.

# 7. Comprovar
sudo ufw status verbose
```

## Regles aplicades: nftables/iptables

ufw no es mes que un frontend. Les regles reals estan a nftables o iptables. Pots veure-les amb:

```bash
# Si ufw fa servir nftables
sudo nft list ruleset

# Si fa servir iptables
sudo iptables -L -n -v
sudo iptables -t nat -L -n
```

## Per que importa aixo a Tailscale

Tailscale crea una interficie de xarxa anomenada `tailscale0`. Es una interficie **virtual** sobre Internet, pero el sistema la veu com una interficie de xarxa real. Per tant, podem fer regles de firewall especifiques per aquesta interficie.

Exemple: volem que SSH nomes sigui accessible desde Tailscale (mai des d'Internet):

```bash
sudo ufw allow in on tailscale0 to any port 22 proto tcp
sudo ufw deny 22/tcp
# Ara el port 22 nomes es accessible desde 100.x.y.z
```

Aixo es la **microsegmentacio**: cada servei te el seu permis, nomes per a la xarxa on toca.

## Bones practiques

- **Deny-by-default**: tanca tot per defecte, obre nomes el que cal.
- **Documenta cada regla** amb un `comment` al ufw.
- **Agrupa per interficie** (tailscale0, eth0) per claredat.
- **Audita periodicament**: `ufw status numbered` cada mes.
- **No desactivis el firewall** per depurar. Millor permetre el trafic temporalment i mirar els logs.
- **Activa els logs**: `sudo ufw logging on` per veure que passa.

## Comandes utils

```bash
# Veure les regles
sudo ufw status verbose
sudo ufw status numbered

# Comptar connexions bloquejades
sudo iptables -L -n -v | grep DROP

# Veure el backend
sudo update-alternatives --query iptables

# Logs del firewall
sudo journalctl -k -f | grep UFW
# o
sudo tail -f /var/log/ufw.log

# Aplicar una regla nomes des d'una IP concreta
sudo ufw allow from 100.64.0.0/10 to any port 22
```

## Connexions amb altres capitols

- **Cap 2** - Tailscale: amaga el servidor, el firewall local ho complementa.
- **Cap 3** - SSH: el firewall es on fail2ban aplica les regles.
- **Cap 8** - Monitoratge: els logs del firewall son font d'informacio.
- **M1 Cap 4** - Xarxa: conceptes basics.

## Conclusio

El firewall es la **barrera local** despres de Tailscale. Amb el combo Tailscale + ufw, el servidor nomes te ports oberts on realment toca. Si mai tens dubtes sobre quin port deixar obert, recorda la regla d'or: **si no cal, tanca**.
