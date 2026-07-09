# Capítol 44 — Tailscale ACLs i segmentació de xarxa

> *"El tallafocs més segur és el que no deixa passar res. Però llavors no tens xarxa. La gràcia és trobar l'equilibri."*

## 44.1 Què són les ACLs de Tailscale

**ACLs** (Access Control Lists, llistes de control d'accés) són regles que defineixen **qui pot accedir a què** dins del teu tailnet. S'apliquen a Tailscale i permeten una segmentació fina.

Per defecte, Tailscale permet que **tots els dispositius del tailnet es comuniquin entre ells**. Això és convenient però no segur. Les ACLs permeten canviar-ho.

Exemple d'ACL:

```json
{
  "acls": [
    {
      "action": "accept",
      "src": ["tag:admin"],
      "dst": ["tag:admin:*", "tag:server:*", "tag:iot:*"]
    },
    {
      "action": "accept",
      "src": ["tag:server"],
      "dst": ["tag:server:*", "tag:iot:1883"]
    },
    {
      "action": "accept",
      "src": ["tag:iot"],
      "dst": ["tag:server:1883"]
    }
  ]
}
```

Aquesta ACL diu:

- Els administradors (tag admin) poden accedir a tot.
- Els servidors poden accedir a altres servidors i al port 1883 (MQTT) dels dispositius IoT.
- Els dispositius IoT només poden accedir al port 1883 dels servidors.

## 44.2 Com s'apliquen les ACLs

Les ACLs s'apliquen a tots els dispositius del tailnet des de la consola d'administració de Tailscale:

1. Vés a https://login.tailscale.com/admin/acls.
2. Edita el JSON de les ACLs.
3. Desa.

Els canvis s'apliquen automàticament en qüestió de segons.

## 44.3 Tags: organitzar els dispositius

Els **tags** són etiquetes que pots posar als dispositius. Serveixen per agrupar-los en les ACLs.

Per assignar un tag, edita el dispositiu a la consola i afegeix el tag:

- `tag:server`: servidors (Raspberry, Mac).
- `tag:iot`: dispositius IoT (Raspberry, nodes ESP32).
- `tag:admin`: dispositius d'administració (el teu portàtil).
- `tag:guest`: dispositius de convidats.

També pots usar tags per funcionalitat:

- `tag:db`: bases de dades.
- `tag:web`: servidors web.
- `tag:monitor`: monitoratge.

## 44.4 L'estructura del BernatLab amb ACLs

Aplica aquesta estructura al teu tailnet:

```
tag:admin (bernat@windows, bernat@mac)
   │
   ↓ pot accedir a tot
   │
tag:server (hortosona@linux, portainer@server)
   │
   ├──> tag:iot (port 1883, MQTT)
   └──> tag:monitor (port 3001, Uptime Kuma)

tag:iot (cap pot accedir a res per defecte)
   │
   └──> tag:server:1883 (pot publicar a MQTT)

tag:guest (visitants)
   │
   └──> (sense accés per defecte)
```

## 44.5 Exemple complet d'ACLs

Aquí tens una configuració completa per al BernatLab:

```json
{
  // ACLs principals
  "acls": [
    // L'administrador pot accedir a tot
    {
      "action": "accept",
      "src": ["tag:admin"],
      "dst": ["*:*"]
    },
    // Els servidors poden parlar entre ells
    {
      "action": "accept",
      "src": ["tag:server"],
      "dst": ["tag:server:*"]
    },
    // Els servidors poden llegir d'IoT
    {
      "action": "accept",
      "src": ["tag:server"],
      "dst": ["tag:iot:80", "tag:iot:1883"]
    },
    // Els dispositius IoT poden publicar a MQTT
    {
      "action": "accept",
      "src": ["tag:iot"],
      "dst": ["tag:server:1883"]
    },
    // El monitor pot accedir als serveis
    {
      "action": "accept",
      "src": ["tag:monitor"],
      "dst": ["tag:server:80", "tag:server:443", "tag:server:3000",
              "tag:server:3001", "tag:server:8080", "tag:server:9443"]
    }
  ],

  // Regles SSH: només admin pot accedir per SSH
  "ssh": [
    {
      "action": "accept",
      "src": ["tag:admin"],
      "dst": ["tag:server", "tag:iot"],
      "users": ["autogroup:nonroot"]
    }
  ],

  // Tests: l'administrador pot fer tests
  "tests": [
    {
      "src": ["tag:admin"],
      "dst": ["tag:server", "tag:iot", "tag:monitor"],
      "accept": ["*:*"]
    }
  ],

  // Tag dels dispositius
  "tagOwners": {
    "tag:admin": ["autogroup:members"],
    "tag:server": ["tag:admin"],
    "tag:iot": ["tag:admin"],
    "tag:monitor": ["tag:server"],
    "tag:guest": ["tag:admin"]
  },

  // Per defecte, denega tot
  "defaultPolicy": {
    "action": "deny"
  }
}
```

Aquesta configuració:

- Defineix clarament qui pot accedir a què.
- Denega tot per defecte.
- Permet SSH només a l'administrador.
- Permet que els dispositius IoT només publiquin a MQTT.

## 44.6 Com verificar les ACLs

Després d'aplicar les ACLs, verifica que funcionen:

1. **Des d'un dispositiu admin**, intenta accedir a un servei. Hauria de funcionar.
2. **Des d'un dispositiu IoT**, intenta accedir a un servei que no toca. Hauria de fallar.
3. **Des d'un dispositiu guest**, intenta accedir a qualsevol cosa. Hauria de fallar.

Exemple de prova:

```bash
# Des d'un admin
ssh bernat@hortosona
# Hauria de funcionar

# Des d'un IoT (com un ESP32)
curl http://100.115.134.76:8080
# Hauria de fallar (denegat)
```

## 44.7 Polítiques per defecte

A Tailscale pots triar entre dues polítiques per defecte:

1. **allow-all** (per defecte): tothom pot accedir a tot.
2. **deny**: ningú pot accedir a res sense regla explícita.

Recomanació: **deny per defecte**, i anar afegint regles específiques. Això és la postura Zero Trust.

## 44.8 ACLs avançades

### Limitar per usuari

```json
{
  "action": "accept",
  "src": ["bernat@"],
  "dst": ["tag:server:22"]
}
```

Així, només l'usuari "bernat" pot accedir al port 22 (SSH), no altres usuaris del tailnet.

### Limitar per temps

Tailscale no suporta ACLs basades en temps directament, però pots combinar amb eines externes com **cron + iptables** a la Raspberry.

### Limitar per geolocalització

Tailscale admet localització geogràfica. Pots crear regles que només permetin accessos des de Catalunya:

```json
{
  "acls": [
    {
      "action": "accept",
      "src": ["bernat@", "bernatmora@"],
      "dst": ["tag:server:*"]
    }
  ]
}
```

Això és per usuari, no per geolocalització. Per geolocalització, cal Tailscale Enterprise o eines externes.

## 44.9 Segmentació més fina: sub-xarxes

Si tens molts dispositius, pots crear **sub-xarxes** dins del tailnet. Tailscale admet **subnet routers**: un dispositiu del tailnet pot exposar una xarxa sencera.

Exemple: la Raspberry del camp (hortosona) té un node ESP32 connectat per Wi-Fi. Pots fer que la Raspberry comparteixi la xarxa 192.168.1.0/24 amb el tailnet:

```bash
# A la Raspberry
sudo tailscale up --advertise-routes=192.168.1.0/24
```

A la consola de Tailscale, aprova la ruta. Ara pots accedir a 192.168.1.10 (l'ESP32) des del teu portàtil.

Això és útil per accedir a dispositius que no poden executar Tailscale directament.

## 44.10 Gestió de secrets amb Tailscale

Tailscale té un **gestor de secrets** integrat (des de 2024) per desar variables d'entorn de manera xifrada:

```bash
# Desa un secret
tailscale env set DATABASE_URL "postgres://user:pass@db:5432/bernatlab"

# Llegeix un secret
tailscale env get DATABASE_URL
```

Això és útil per desar credencials que necessiten múltiples dispositius.

## 44.11 Logs i visibilitat

Tailscale té un panell d'**administració** on pots veure:

- Tots els dispositius connectats.
- El tràfic per dispositiu.
- Les ACLs aplicades.
- Els intents d'accés denegats.

Revisa'l periòdicament. Si veus un dispositiu estrany, és una alerta.

## 44.12 Com canviar les ACLs en producció

Quan canvies les ACLs en un sistema en producció, cal:

1. **Provar primer** amb un dispositiu no crític.
2. **Fer còpia de seguretat** de les ACLs actuals.
3. **Aplicar els canvis gradualment**.
4. **Monitorar** els logs per veure si algú queda fora.

Si t'equivoques, pots tornar a la configuració anterior des de la consola.

## 44.13 Errors habituals

**Error 1: ficar-se en un lock-out**. Si denegues l'accés a la teva pròpia IP, no podràs accedir. Solució: tenir sempre una porta oberta (port 22, amb autenticació per clau) o un usuari de "break glass" amb permisos amplis.

**Error 2: oblidar els tags**. Sense tags, les ACLs no funcionen. Assegura't que tots els dispositius tenen els tags adequats.

**Error 3: massa permisos**. Si tot és "accept all", no has avançat gaire. Sigues estricte.

**Error 4: no documentar**. Sense documentació, ningú no entendrà per què una regla és com és.

## 44.14 Bones pràctiques

1. **Comença amb deny per defecte**.
2. **Agrupa dispositius** amb tags lògics.
3. **Dona el mínim** a cada grup.
4. **Audita cada mes**: les ACLs encara tenen sentit?
5. **Documenta cada regla** amb comentaris JSON.
6. **Prova abans d'aplicar**: usa l'eina de test de Tailscale.
7. **Fes còpies** de les ACLs (exporta el JSON periòdicament).

## 44.15 Resum

Les ACLs de Tailscale permeten controlar amb precisió qui pot accedir a què dins del tailnet. Combinades amb tags i el principi de Zero Trust, són la primera línia de defensa del BernatLab. En el proper capítol veurem les còpies de seguretat: la segona línia de defensa quan tot falla.

## 44.16 Exercicis pràctics

1. Inventaria tots els teus dispositius Tailscale i els seus tags.
2. Crea una ACL amb deny per defecte i afegint només el que necessitis.
3. Afegeix tags almenys a 3 dispositius.
4. Prova les ACLs des de cada tipus de dispositiu.
5. Documenta les ACLs al README amb comentaris.
6. Fes una còpia de seguretat de les ACLs.
7. Configura un usuari "break glass" per a emergències.

Paraules clau: **Tailscale, ACL, access control list, llistes de control, JSON, regla, action, accept, deny, src, dst, tag, tags, device, tailnet, subnet router, subnet, route, IP, 100.x, 192.168, ssh, autogroup, members, nonroot, test, defaultPolicy, allow-all, deny, deny-by-default, least privilege, Zero Trust, no confiïs, verificar, autenticació, segmentació, microsegmentation, network, network policy, network segmentation, firewall, tallafocs, port, 22, 80, 443, 1883, 3000, 3001, 8080, 9443, administrador, admin, server, iot, monitor, guest, convidat, convidats, convidada, etiqueta, group, grup, role, rol, permís, permissions, scope, àmbit, project, projecte, account, compte, organization, organització, user, usuari, identity, identitat, principal, subject, claim, scope, role, binding, policy, política, enforcement, aplicació, regla, rule, condition, condició, expression, expressió, match, match, glob, wildcard, pattern, patró, prefix, suffix, contains, contains, exact, exact, regex, regular expression, IPv4, IPv6, CIDR, mask, subnet mask, broadcast, network address, host address, gateway, router, default gateway, route, routing table, FIB, RIB, BGP, OSPF, RIP, static route, dynamic route, distance vector, link state, path vector, convergence, routing domain, autonomous system, AS, AS number, ASN, BGP peer, BGP session, eBGP, iBGP, route reflector, route map, prefix list, community, extended community, large community, AS path, MED, local preference, weight, origin, next hop, IGP, EGP, routing protocol, OSPF, area, backbone, stub, totally stubby, NSSA, summarization, aggregation, summarization, LSA, link state advertisement, hello, dead interval, cost, bandwidth, delay, reliability, load, MTU, path, shortest, cost, Dijkstra, SPF, shortest path first, BFD, bidirectional forwarding detection, LDP, MPLS, label, label distribution, FEC, forwarding equivalence class, LSP, label switched path, VPN, virtual private network, VRF, virtual routing and forwarding, VPLS, virtual private LAN service, VPRN, virtual private routed network, layer 2 VPN, layer 3 VPN, IPsec, AH, ESP, IKE, ISAKMP, SA, security association, transform, encryption, integrity, authentication, key exchange, Diffie-Hellman, RSA, ECDH, PFS, perfect forward secrecy, DH group, lifetime, rekey, replay protection, anti-replay, sequence number, ESP, transport mode, tunnel mode, NAT-T, NAT traversal, IKEv2, MOBIKE, DPD, dead peer detection, keepalive, hello, liveness, MTU, fragmentation, DF, don't fragment, MSS, maximum segment size, PMTU, path MTU, discovery, ICMP, error, message, type, code, checksum, pointer, embedded, packet, header, trailer, payload, padding, authentication, integrity, ESP header, ESP trailer, ESP authentication, ICV, integrity check value, HMAC, keyed hash, SHA, MD5, AES, CBC, CTR, GCM, AEAD, authenticated encryption, associated data, confidentiality, integrity, replay, ordering, sequence, anti-replay, window, sliding window, bitmap, sequence number, 32-bit, 64-bit, ESN, extended sequence number, lifetime, byte, packet, time, kilobytes, seconds, soft, hard, renegotiation, rekey, PFS, forward secrecy, compromise, post-compromise, recovery, agility, cryptographic agility, migration, transition, post-quantum, PQC, hybrid, classical, quantum, ML-KEM, Kyber, ML-DSA, Dilithium, SLH-DSA, SPHINCS, NIST, FIPS 203, FIPS 204, FIPS 205, TLS, 1.2, 1.3, cipher suite, negotiation, handshake, client hello, server hello, certificate, key exchange, finished, change cipher spec, alert, warning, fatal, close notify, renegotiation_info, extended master secret, encrypt-then-MAC, MAC-then-encrypt, padding, padding oracle, Lucky 13, BEAST, POODLE, DROWN, Heartbleed, ROBOT, Logjam, FREAK, SLOTH, Sweet32, Ticketbleed, return of Bleichenbacher, Bleichenbacher, ROBOT, timing, padding, oracle, downgrade, attack, defense, mitigation, countermeasure**.
