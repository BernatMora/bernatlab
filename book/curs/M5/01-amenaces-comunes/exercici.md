# Exercici practic - Capitol 1: Amenaces comunes al servidor

> 35-50 min · Real a la teva RPi o maquina Linux

## Objectiu
Auditar la superficie d'atac del teu BernatLab: quins serveis son accessibles, quins intents d'atac reps, i quines mesures ja tens. Acabaras amb un informe clar de la teva posicio de seguretat.

## Requisits

- Linux (RPi, servidor, o maquina virtual)
- 35-50 minuts
- Acces sudo

## Pas 1: Inventari de serveis exposats (10 min)

```bash
# Quins ports TCP escolten al sistema?
ss -tlnp

# Versio detallada
sudo ss -tlnp4
```

Anota cada servei: port, protocol, programa, estat (LISTEN).

## Pas 2: Escaneja't a tu mateix (10 min)

Des de la RPi, comprova que nomes veus el que hauries:

```bash
# Instal·la nmap
sudo apt install nmap

# Escaneig basic
nmap localhost

# Escaneig mes detallat (pot trigar)
nmap -sV -p 1-10000 localhost
```

Hauries de veure:
- Port 22 (SSH) nomes a 127.0.0.1 si Tailscale esta actiu.
- Port 80/443 nomes si tens Nginx/Caddy exposat.
- Altres ports de serveis locals nomes a 127.0.0.1.

## Pas 3: Comprova els intents d'atac a SSH (10 min)

```bash
# Total d'intents fallits desde l'inici del sistema
sudo journalctl -u ssh --no-pager | grep "Failed password" | wc -l

# Ultims 50
sudo journalctl -u ssh -n 50 | grep "Failed"

# Top 10 usuaris mes intentats
sudo journalctl -u ssh --no-pager | grep "Failed password" \
  | awk '{print $9}' | sort | uniq -c | sort -rn | head

# Top 10 IPs mes insistents
sudo journalctl -u ssh --no-pager | grep "Failed password" \
  | awk '{print $11}' | sort | unic -c | sort -rn | head
```

Documenta: quants intents, quins usuaris, quines IPs.

## Pas 4: Comprova fail2ban (5 min)

```bash
# Esta instal·lat?
which fail2ban-client

# Esta actiu?
sudo systemctl status fail2ban

# Quantes IPs te bloquejades ara?
sudo fail2ban-client status sshd
```

Si fail2ban no esta instal·lat, instal·la'l:

```bash
sudo apt install fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

## Pas 5: Verifica que SSH nomes escolta a Tailscale (5 min)

```bash
ss -tlnp | grep :22
```

Si diu `0.0.0.0:22` o `[::]:22`, SSH esta obert a tothom. Riscos.

Per fer que nomes escolti a Tailscale:

```bash
sudo nano /etc/ssh/sshd_config.d/99-tailscale-only.conf
```

```sshconfig
ListenAddress 100.64.0.1
```

(Canvia la IP per la teva IP de Tailscale). Despres:

```bash
sudo systemctl restart sshd
```

⚠️ **Atencio**: assegura't que tens una sessio SSH activa abans de reiniciar, per no perdre acces.

## Pas 6: Escaneig des de fora (5 min)

Si tens una IP publica o un VPS, pots comprovar des de fora:

```bash
nmap bernat.tuservidor.cat
```

Si nomes veus el port 22 a una IP de Tailscale (100.x), perfecte. Si veus mes, cal revisar.

## Pas 7: Crea un informe d'auditoria (10 min)

Crea `informe_seguretat.md`:

```markdown
# Informe d'auditoria de seguretat - BernatLab

## Data
[avui]

## Serveis exposats
| Port | Servei | Adreça | Estat |
|------|--------|--------|-------|
| 22 | SSH | 100.64.0.1 | OK (nomes Tailscale) |
| 80 | HTTP | - | Tancat |
| ... | ... | ... | ... |

## Atacs detectats
- Intents SSH fallits (24h): X
- Usuaris mes atacats: pi (N), root (N), ...
- IPs mes insistents: ...

## Mesures de seguretat en marxa
- [ ] Tailscale instal·lat i actiu
- [ ] SSH nomes a Tailscale
- [ ] ufw/firewall actiu
- [ ] fail2ban actiu
- [ ] Actualitzacions automatiques

## Riscos identificats
1. [Risc 1]
2. [Risc 2]

## Proximes accions
1. [Accio 1]
2. [Accio 2]
```

## Validacio

Has acabat si:

- [ ] Has identificat tots els serveis que escolten.
- [ ] Has fet un escaneig nmap del teu propi sistema.
- [ ] Has revisat els logs de SSH.
- [ ] Has verificat fail2ban.
- [ ] Has confirmat que SSH nomes escolta a Tailscale.
- [ ] Has escrit l'informe d'auditoria.

## Per aprofundir

- Investiga "Shodan" i "Censys": serveis que mostren quantes maquines amb ports oberts hi ha a Internet.
- Compara el teu sistema amb un "antes" (amb port 22 obert) i un "despres" (amb Tailscale).
- Llegeix sobre "honeypots": maquines trampa per estudiar atacs.
- Investiga "OSSEC" o "Wazuh": sistemes de deteccio d'intrusions (HIDS).

## Ves un pas mes enlla

**Repte avançat**: Munta un sistema de monitoritzacio basic amb fail2ban + telegram:
1. Configura fail2ban per enviar alertes a Telegram quan es bloquegi una IP.
2. Configura un script que cada hora enviï un resum d'atacs.
3. Dibuixa un graf de intents d'atac al llarg del temps (amb Grafana o un CSV simple).

Aixo es la base d'un SOC (Security Operations Center) personal.
