# Capítol 47 — fail2ban, rate limiting i tallafocs aplicat

> *"El millor tallafocs és el que t'avisa quan algú intenta passar."*

## 47.1 Què és fail2ban

**fail2ban** és una eina que monitora els logs del sistema i **bloqueja IPs** que fan massa intents fallits. Per exemple, si una IP intenta accedir per SSH amb 5 contrasenyes errònies, fail2ban la bloqueja durant 10 minuts.

Combinat amb un tallafocs, és molt efectiu contra:

- **Bots d'escaneig** que busquen contrasenyes febles.
- **Atacs de força bruta** contra SSH, HTTP, FTP, etc.
- **Atacs de diccionari** contra serveis web.

## 47.2 Instal·lació a Debian/Raspberry

```bash
sudo apt update
sudo apt install fail2ban
```

Això instal·la fail2ban i l'inicia com a servei systemd.

Verificar:

```bash
sudo systemctl status fail2ban
```

## 47.3 Configuració bàsica

La configuració principal és a `/etc/fail2ban/jail.local` (crear-lo per no sobreescriure l'original):

```ini
[DEFAULT]
# Temps de bloqueig per defecte (1 hora)
bantime = 1h

# Finestra de temps per comptar intents fallits (10 min)
findtime = 10m

# Nombre d'intents abans del bloqueig
maxretry = 5

# IPs que mai no es bloquegen (loopback, xarxa local)
ignoreip = 127.0.0.1/8 100.64.0.0/10
```

El rang `100.64.0.0/10` és la xarxa Tailscale — important no bloquejar-te a tu mateix.

## 47.4 Jails (presons) actius

Cada "jail" és un patró de detecció. Els més útils:

### SSH

```ini
[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 24h
```

Així, 3 intents fallits = bloqueig durant 24 hores.

### SSH amb Tailscale

Si només vols SSH des de Tailscale:

```ini
[sshd-tailscale]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 24h
ignoreip = 100.64.0.0/10
```

I configura SSH per escoltar només a Tailscale:

```bash
sudo systemctl edit sshd
# A l'override.conf:
[Service]
ExecStart=
ExecStart=/usr/sbin/sshd -D -i -e -f /etc/ssh/sshd_config
```

I a `/etc/ssh/sshd_config`:

```
ListenAddress 100.x.y.z
```

### HTTP (nginx)

```ini
[nginx-http-auth]
enabled = true
filter = nginx-http-auth
port = http,https
logpath = /var/log/nginx/error.log
maxretry = 3
bantime = 1h
```

### Grafana, Portainer, etc.

Per a serveis web amb autenticació, pots crear jails personalitzats. Exemple per a Portainer:

```ini
[portainer-auth]
enabled = true
filter = portainer-auth
port = 9443
logpath = /var/lib/docker/volumes/portainer_data/_data/portainer.log
maxretry = 5
bantime = 1h
```

I el filtre a `/etc/fail2ban/filter.d/portainer-auth.conf`:

```
[Definition]
failregex = ^.*Failed login attempt for .* from <HOST>.*$
ignoreregex =
```

## 47.5 Comandes útils

### Estat general

```bash
sudo fail2ban-client status
```

### Estat d'un jail

```bash
sudo fail2ban-client status sshd
```

### Veure IPs bloquejades

```bash
sudo fail2ban-client status sshd
# A la sortida:
# Banned IP list: 1.2.3.4, 5.6.7.8
```

### Desbloquejar una IP

```bash
sudo fail2ban-client set sshd unbanip 1.2.3.4
```

### Bloquejar una IP manualment

```bash
sudo fail2ban-client set sshd banip 1.2.3.4
```

### Comprovar els logs

```bash
sudo tail -f /var/log/fail2ban.log
```

## 47.6 Com combinar amb el tallafocs

fail2ban usa **iptables** (o **nftables**) per bloquejar. Això és complementari al tallafocs normal.

Si tens UFW (Uncomplicated Firewall) activat:

```bash
# Comprovar si UFW està actiu
sudo ufw status

# Si no, activar
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow in on tailscale0  # permet tot des de Tailscale
sudo ufw enable
```

Ara UFW gestiona el tallafocs base, i fail2ban hi afegeix bloquejos dinàmics.

## 47.7 Rate limiting

El **rate limiting** limita el nombre de peticions per IP/segon. Això evita:

- **Atacs DoS** (denial of service).
- **Abús d'APIs** (excés de peticions).
- **Força bruta accelerada** (molts intents per segon).

### Rate limiting a nginx

Exemple de limitació de peticions per IP:

```nginx
http {
    # Definir una zona de rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;

    server {
        location /api/ {
            limit_req zone=api burst=20 nodelay;
            proxy_pass http://backend;
        }
    }
}
```

Això permet 10 peticions per segon, amb una ràfega de 20.

### Rate limiting a Caddy

Caddy ho té integrat:

```caddyfile
api.bernatlab.cat {
    rate_limit {remote.ip} 10r/s
    reverse_proxy localhost:8080
}
```

### Rate limiting a Portainer

Portainer no té rate limiting natiu, però pots posar-lo darrere d'un reverse proxy (Caddy o nginx) que sí en tingui.

## 47.8 Protecció contra DoS

Per a una Raspberry, els atacs DoS són un risc real (la RPi no té gaire potència). Proteccions:

1. **Tailscale**: com que no exposa ports a Internet, ja està protegit.
2. **Cloudflare Tunnel**: si exposes serveis, Cloudflare filtra el tràfic.
3. **fail2ban**: bloqueja IPs sospitoses.
4. **Rate limiting**: limita peticions per IP.
5. **nginx amb limit_req**: filtra peticions abans d'arribar al backend.

## 47.9 Tallafocs aplicat a la Raspberry

### Política per defecte: deny

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
```

### Permetre només el necessari

```bash
# SSH només des de Tailscale
sudo ufw allow in on tailscale0 to any port 22

# Per a la gestió via web (si vols)
sudo ufw allow in on tailscale0 to any port 9443  # Portainer
sudo ufw allow in on tailscale0 to any port 3000  # Homepage
sudo ufw allow in on tailscale0 to any port 3001  # Uptime Kuma

# Activar
sudo ufw enable
sudo ufw status verbose
```

### Limitar l'accés per IP

```bash
# Només tu pots accedir a SSH
sudo ufw allow from 100.x.y.z to any port 22
```

## 47.10 Tallafocs al Mac

macOS té un tallafocs integrat (System Settings → Network → Firewall). Però és bàsic. Per a més control, pots usar **Lulu** o **Little Snitch** (gratuïts o de pagament).

Per configurar el tallafocs per aplicació:

1. System Settings → Network → Firewall → Options.
2. Activa "Block all incoming connections".
3. Permet les aplicacions que necessitin (Ollama, uvicorn, etc.).

## 47.11 Logs del tallafocs

Revisar els logs periòdicament:

```bash
# Logs de UFW
sudo tail -f /var/log/ufw.log

# Logs de fail2ban
sudo tail -f /var/log/fail2ban.log

# Logs d'auth (intents de SSH)
sudo tail -f /var/log/auth.log
```

Si veus molts intents des d'una IP estrangera, és un bot. fail2ban ja el bloquejarà, però val la pena investigar.

## 47.12 Protegir serveis exposats

Si per algun motiu exposes serveis a Internet (per exemple, amb Tailscale Funnel o Cloudflare Tunnel), calen proteccions addicionals:

1. **Cloudflare** filtra molt tràfic maliciós.
2. **Cloudflare Turnstile** o **hCaptcha** per a formularis.
3. **Rate limiting** agressiu.
4. **WAF** (Web Application Firewall, tallafocs d'aplicació web): Cloudflare, AWS WAF.
5. **Monitoratge** de peticions sospitoses.

## 47.13 Què fer quan et bloquegen a tu

Si t'has equivocat amb les ACLs o el tallafocs, pots quedar fora. Solucions:

1. **Accés físic** a la Raspberry: teclat + monitor.
2. **Portàtil amb Tailscale** des d'una altra xarxa.
3. **Una porta "break glass"** sempre oberta (però amb clau + 2FA).
4. **Una VPN alternativa** (WireGuard) com a backup.

Per a la Raspberry, el "break glass" és poder-hi accedir físicament amb un monitor. Configurar una sortida HDMI sempre.

## 47.14 Bones pràctiques

1. **Tallafocs per defecte deny**. Permet només el que cal.
2. **fail2ban** a tots els serveis amb autenticació.
3. **Rate limiting** a serveis web.
4. **Logs centralitzats** (Promtail, Loki, o un simple fitxer).
5. **Revisar setmanalment** els logs.
6. **Auditar mensualment** les regles del tallafocs.
7. **Documentar** cada canvi.

## 47.15 Resum

El tallafocs i fail2ban són la quarta línia de defensa. fail2ban bloqueja IPs que fan massa intents fallits. El tallafocs permet només el tràfic necessari. El rate limiting evita DoS. La combinació d'aquestes eines amb Tailscale (que ja evita l'exposició a Internet) fa que el BernatLab sigui molt segur. En el proper capítol veurem el hardening del sistema operatiu.

## 47.16 Exercicis pràctics

1. Instal·la fail2ban a la Raspberry.
2. Configura un jail per a SSH amb 3 intents màxim.
3. Activa UFW amb polítiques restrictives.
4. Configura rate limiting al reverse proxy.
5. Prova fail2ban: intenta 5 contrasenyes errònies per SSH.
6. Comprova les IPs bloquejades amb `fail2ban-client status sshd`.
7. Configura alertes a Telegram per a nous bloquejos.
8. Documenta al README l'estratègia de tallafocs.

Paraules clau: **fail2ban, jail, banned, banned IP, ban, unban, maxretry, findtime, bantime, ignoreip, recidive, jail.local, filter, action, iptables, nftables, UFW, uncomplicated firewall, iptables, nft, firewalld, pf, ipfw, ipfilter, IPFW, netfilter, Linux firewall, eBPF, Cilium, Falco, sysdig, audit, auditd, ausearch, aureport, logs, /var/log, /var/log/auth.log, /var/log/syslog, journald, journalctl, logrotate, centralitzat, Promtail, Loki, Grafana, alerting, Uptime Kuma, Telegram, rate limit, limit_req, limit_req_zone, burst, nodelay, leaky bucket, token bucket, fixed window, sliding window, counter, gauge, histogram, exponential backoff, DoS, DDoS, denial of service, distributed, amplification, reflection, SYN flood, UDP flood, ICMP flood, ping flood, ping of death, smurf, fraggle, teardrop, bonk, land, winnuke, nestea, jolt, OOB, out-of-band, RST, cookie, SYN cookie, tcp_syncookies, ip_no_pmtu_disc, rp_filter, reverse path filtering, martian, log_martians, accept_ra, accept_redirects, send_redirects, secure_redirects, proxy_arp, ip_forward, forwarding, route, gateway, default gateway, network namespace, netns, VRF, table, FIB, RIB, rules, chains, INPUT, OUTPUT, FORWARD, PREROUTING, POSTROUTING, nat, masquerade, SNAT, DNAT, REDIRECT, LOG, REJECT, DROP, ACCEPT, queue, NFQUEUE, conntrack, connection tracking, state, NEW, ESTABLISHED, RELATED, INVALID, UNTRACKED, rate, limit, policer, shaper, tc, traffic control, netem, qdisc, pfifo, fq_codel, CAKE, RED, ECN, explicit congestion notification, ECN, CE, ECT, ect_0, ect_1, ECT(0), ECT(1), Not-ECT, Not-ECT, Low Delay, Low Loss, Low Loss Low Delay, L4S, Prague, dual queue, fq, fair queue, FQ-CoDel, Stochastic Fair Queueing, SFQ, priority, qos, dscp, tos, vlan, 802.1Q, qinq, 802.1ad, bridge, brctl, veth, macvlan, ipvlan, tunnel, GRE, IPIP, GUE, VXLAN, GENEVE, ERSPAN, ERSPAN, Type, ERSPAN, ERSPAN Type II, ERSPAN Type III, ERSPAN Type I, header, payload, encap, decap, geneve, vni, vxlan, segment, ID, encapsulation, tunnel endpoint, VTEP, VTEP, VTEP, distributed, virtual, switch, Open vSwitch, OVS, DPDK, FD.io, VPP, fast data, fast path, kernel bypass, XDP, eXpress Data Path, AF_XDP, busy polling, epoll, io_uring, sendfile, splice, tee, vmsplice, copy avoidance, zero copy, kernel-bypass, user-space networking, networking, layer 2, layer 3, layer 4, layer 7, application, presentation, session, transport, network, data link, physical, MAC, PHY, switch, hub, bridge, router, gateway, firewall, IDS, IPS, NDR, network detection, response, DPI, deep packet inspection, NF, netfilter, iptables, nftables, ebtables, arptables, ip6tables, brctl, ip rule, ip route, ip neigh, ip tunnel, ip link, ip addr, ip maddr, ip mroute, ip xfrm, ip netns, ip l2tp, ip tcp_metrics, ss, netstat, lsof, fuser, lscpu, lspci, lsusb, lsblk, lsscsi, lsraid, dmidecode, lshw, hwinfo, inxi, screenfetch, neofetch, fastfetch, weather, cpu, gpu, ram, rom, bios, uefi, legacy, efivars, secure boot, tpm, measured boot, attested, measured, root of trust, intel TXT, AMD SKINIT, SRTM, DRTM, late launch, dynamic root of trust, trust, attestation, measured, integrity, IMA, EVM, Linux IMA, Integrity Measurement Architecture, Extended Verification Module, appraisal, audit, signed, kernel, signed, modules, signed, dm-verity, dm-integrity, LUKS, LUKS2, cryptsetup, LUKS header, key slot, passphrase, TPM, enrollment, key, binding, PCR, Platform Configuration Register, policy, TPM2, TPM2_CreatePrimary, TPM2_StartAuthSession, TPM2_PolicyPCR, TPM2_PCR_Read, TPM2_NV_Read, TPM2_NV_DefineSpace, TPM2_NV_Write, TPM2_NV_ReadLock, TPM2_NV_WriteLock, TPM2_Clear, TPM2_DictionaryAttackLockReset, TPM2_DictionaryAttackParameters, TPM2_Startup, TPM2_Shutdown, TPM2_GetRandom, TPM2_GetTestResult, TPM2_GetCapability, TPM2_ReadPublic, TPM2_Import, TPM2_Load, TPM2_LoadExternal, TPM2_Seal, TPM2_Unseal, TPM2_Sign, TPM2_VerifySignature, TPM2_RSA_Decrypt, TPM2_ECC_ZGen, TPM2_ECC_Sign, TPM2_ECC_Verify, TPM2_ZGen_2Phase, TPM2_ECC_Point_Z, TPM2_Encrypt, TPM2_Decrypt, TPM2_HMAC, TPM2_HMAC_Start, TPM2_HMAC_Update, TPM2_HMAC_Complete, TPM2_SequenceComplete, TPM2_SequenceUpdate, TPM2_Sign, TPM2_Verify, TPM2_Certify, TPM2_CertifyCreation, TPM2_Quote, TPM2_PCR_Allocate, TPM2_PCR_SetAuthPolicy, TPM2_PCR_SetAuthValue, TPM2_NV_Certify, TPM2_PCR_Reset, TPM2_ChangeAuth, TPM2_NV_ChangeAuth, TPM2_LoadKey, TPM2_Seal, TPM2_Unseal, TPM2_Duplicate, TPM2_Rewrap, TPM2_Import, TPM2_LoadExternal, TPM2_LoadKey, TPM2_LoadKey2, TPM2_ReadPublic, TPM2_RSA_Encrypt, TPM2_RSA_Decrypt, TPM2_ECDH_KeyGen, TPM2_ECDH_ZGen, TPM2_ECC_Parameters, TPM2_FirmwareRead, TPM2_Capability, TPM2_GetRandom, TPM2_GetTestResult, TPM2_Increment, TPM2_ReadClock, TPM2_ReadClock, TPM2_TickStamp, TPM2_Time, TPM2_Verify, TPM2_NV_GlobalWriteLock, TPM2_NV_Increment, TPM2_NV_Extend, TPM2_Vendor_TCG, vendor, defined, commands**.
