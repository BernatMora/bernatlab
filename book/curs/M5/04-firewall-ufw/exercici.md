# Exercici practic - Capitol 4: Firewall i ufw

> 30-45 min · Real al teu sistema

## Objectiu

Configurar ufw a la RPi amb una politica deny-by-default i nomes els ports estrictament necessaris. Al final, nomes el que tu vulguis ser accessible des de Tailscale, i la resta nomes des de la maquina local.

## Requisits

- Acces a la RPi amb sudo, idealment per Tailscale o consola fisica
- 30-45 minuts

## Pas 1: Estat actual (5 min)

Primer mira quina es la situacio actual del firewall:

```bash
# ufw esta actiu?
sudo ufw status

# Si no, mira iptables directament
sudo iptables -L -n -v | head -30

# Quines interficies tens?
ip addr
# Hauries de veure eth0 (o wlan0) i tailscale0
```

## Pas 2: Politica per defecte (5 min)

Defineix la politica mes segura: denegar tot el que entra, permetre tot el que surt.

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
```

**Compte**: despres d'aquesta ordre, si tens serveis escoltant a ports oberts, deixaran de ser accessibles fins que no els permetis explicitament. Es el que volem.

## Pas 3: Regles basiques (10 min)

Permet els ports essencials, nomes des de Tailscale:

```bash
# SSH nomes des de Tailscale
sudo ufw allow in on tailscale0 to any port 22 proto tcp comment "SSH via Tailscale"

# Web HTTP nomes des de Tailscale
sudo ufw allow in on tailscale0 to any port 80 proto tcp comment "HTTP via Tailscale"

# Web HTTPS nomes des de Tailscale
sudo ufw allow in on tailscale0 to any port 443 proto tcp comment "HTTPS via Tailscale"
```

## Pas 4: Altres serveis opcionals (10 min)

Si tens mes serveis, configura'ls tambe:

```bash
# DNS nomes per Tailscale
sudo ufw allow in on tailscale0 to any port 53 comment "DNS via Tailscale"

# Home Assistant nomes per Tailscale
sudo ufw allow in on tailscale0 to any port 8123 proto tcp comment "Home Assistant"

# Gitea nomes per Tailscale
sudo ufw allow in on tailscale0 to any port 3000 proto tcp comment "Gitea"
```

## Pas 5: Activa i verifica (10 min)

```bash
# Activa
sudo ufw enable
# Et dira: "Command may disrupt existing ssh connections. Proceed (y|n)?"
# Digues 'y'

# Estat
sudo ufw status verbose
sudo ufw status numbered
```

Hauries de veure una llista de regles numerades, totes amb `ALLOW IN` i `tailscale0`.

Des d'un altre dispositiu (portatil amb Tailscale):

```bash
# Hauria de funcionar
ssh bernat@raspberry
curl http://raspberry:8123

# Hauria de fallar (port no permes)
ssh bernat@raspberry -p 3306
```

## Pas 6: Logs (5 min)

Activa els logs per veure que passa:

```bash
sudo ufw logging on

# Veure els logs en directe
sudo tail -f /var/log/ufw.log
```

Prova de fer una connexio a un port no permes i mira com apareix al log.

## Pas 7: Documenta (5 min)

Al fitxer `inventari-seguretat.md`, afegeix una seccio "Firewall ufw" amb:

- La politica per defecte.
- La llista de regles numerades.
- Quin comportament esperar (qui pot accedir a què).
- Data de la propera auditoria.

## Validacio

- [ ] ufw esta actiu amb default deny incoming.
- [ ] Tens les regles per a SSH, HTTP, HTTPS nomes desde Tailscale.
- [ ] Tens una regla que permet trafic general des de tailscale0.
- [ ] Pots accedir als serveis permesos des de Tailscale.
- [ ] Els ports no permesos queden bloquejats.
- [ ] Els logs del firewall funcionen.

## Per aprofundir

- Mira les regles reals: `sudo nft list ruleset` o `sudo iptables -L -n -v`.
- Prova **gufw** si vols una interficie grafica.
- Configura **alertes per correu** amb `postfix` o amb un script que llegeixi `/var/log/ufw.log`.
- Investiga **nftables directament** sense ufw: tens mes control pero mes complexitat.
