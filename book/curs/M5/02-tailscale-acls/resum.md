# Resum - Capitol 2: Tailscale i ACLs

## La idea clau

Tailscale ens dona una **xarxa privada** (una VPN basada en WireGuard) entre tots els nostres dispositius. Pero Tailscale nomes es la meitat del joc: nomes connecta. Qui pot accedir a quines maquines, per quins ports, i en quines condicions, ho decideixen les **ACLs** (Access Control Lists). Una configuracio de Tailscale sense ACLs es com un edifici amb portes obertes a tothom que hi entra.

## Que es Tailscale (repàs rapid)

**Tailscale** es una eina que crea una xarxa privada entre els teus dispositius sense necessitat d'obrir ports al router. Utilitza el protocol **WireGuard** (rapid i modern) i un servidor de coordinacio per intercanviar claus.

```bash
# Instal·la a Debian/Ubuntu
curl -fsSL https://tailscale.com/install.sh | sh

# Arrenca
sudo tailscale up

# Estat
tailscale status

# IP assignada per Tailscale
tailscale ip -4
```

Cada maquina te una IP del rang 100.x.y.z. Entre elles es comuniquen com si fossin a la mateixa LAN, pero a traves d'Internet el trafic va xifrat punt a punt.

## MagicDNS: noms en lloc d'IPs

Tailscale inclou un servei de DNS automatic anomenat **MagicDNS**. En lloc d'haver de recordar IP, pots accedir a les maquines pel seu nom:

```bash
# En lloc de ssh pi@100.64.0.1
ssh pi@raspberry

# O amb domini complet
ssh pi@raspberry.tailnet-xxxx.ts.net
```

Això es molt util per scripts i per accedir al servidor des de qualsevol lloc. Per veure els noms disponibles:

```bash
tailscale status
```

## Que son les ACLs

Les **ACLs** (Access Control Lists) son regles que diuen a Tailscale "qui pot accedir a què". Son un fitxer en format **HuJSON** (JSON amb comentaris) que es penja a la consola d'administracio de Tailscale (https://login.tailscale.com/admin/acls/file).

Exemple minimal:

```json
{
  "acls": [
    {
      "action": "accept",
      "src": ["autogroup:members"],
      "dst": ["raspberry:22"]
    }
  ]
}
```

Això diu: "tots els membres del tailnet poden accedir al port 22 de la maquina `raspberry`". Tot el que no esta permes, esta denegat per defecte.

## Anatomia d'una ACL

Una regla te quatre parts principals:

- **action**: "accept" (permetre) o "deny" (bloquejar).
- **src**: qui intenta accedir (un usuari, grup, etiqueta, o "autogroup: members").
- **dst**: a quina maquina i port (format `machine:port` o `tag:port`).
- **proto**: protocol (tcp, udp, icmp). Per defecte tcp.

Exemple mes complet:

```json
{
  "acls": [
    {
      "action": "accept",
      "src": ["autogroup:members"],
      "dst": [
        "raspberry:22",         // SSH
        "raspberry:80,443",     // Web
        "raspberry:8123"        // Home Assistant
      ]
    },
    {
      "action": "deny",
      "src": ["*"],
      "dst": ["raspberry:*"]
    }
  ]
}
```

## Etiquetes (tags): segmentacio per rol

Les **etiquetes** permeten agrupar maquines per funcio i aplicar regles per grup:

```json
{
  "tagOwners": {
    "tag:server":    ["autogroup:admin"],
    "tag:iot":       ["autogroup:admin"],
    "tag:personal":  ["autogroup:admin"]
  }
}
```

Aixo asigna les etiquetes a la gent que les pot assignar. Despres pots tenir maquines com:

- `tag:server`: la RPi del BernatLab.
- `tag:iot`: dispositius smart home que nomes es comuniquen amb el servidor.
- `tag:personal`: portatil, telefon... nomes per a tu.

I fer regles tipus:

```json
{
  "action": "accept",
  "src": ["tag:personal"],
  "dst": ["tag:server:22,80,443"]
}
```

Aixi, encara que algun dispositiu IoT sigui compromes, no pot accedir a la resta.

## Com aplicar ACLs al BernatLab

Pas a pas:

1. Ves a https://login.tailscale.com/admin/acls/file.
2. Edita el fitxer amb les teves regles.
3. Guarda. Tailscale aplica les noves regles en segons, sense reinstal·lar res.

Exemple d'ACL aplicat al BernatLab:

```json
{
  // Etiquetes que pot assignar l'admin
  "tagOwners": {
    "tag:server": ["autogroup:admin"],
    "tag:homelab": ["autogroup:admin"]
  },

  // Regles d'acces
  "acls": [
    {
      // El portatil pot accedir a tot del servidor
      "action": "accept",
      "src": ["autogroup:admin"],
      "dst": ["tag:server:*"]
    },
    {
      // Els companys de casa nomes poden fer SSH
      "action": "accept",
      "src": ["user:marina@bernatlab.cat"],
      "dst": ["tag:server:22"]
    }
  ]
}
```

## Bones practiques amb ACLs

- **Principi de minim privilege**: dona nomes el que cada usuari necessita.
- **Etiqueta per funcio, no per maquina**: si tens 2 servidors, posa'ls la mateixa etiqueta.
- **Documenta cada regla**: posa comentaris al HuJSON. D'aqui 6 mesos no recordaras per que.
- **Audita periodicament**: cada 3 mesos, mira si totes les regles encara son valides.
- **No deixis "all ports"**: mai facis `dst: ["machine:*"]` si no es absolutament necessari.
- **Combina amb ufw**: les ACLs son a nivell Tailscale, pero un firewall local es la segona capa.

## Comandes utils

```bash
# Estat general
tailscale status

# Quin es el meu nodeID, IP, hostname
tailscale status --json | jq '.Self'

# Ping a una maquina per Tailscale
tailscale ping raspberry

# Mostrar les ACLs aplicades (en local, debug)
tailscale debug

# Treure una maquina temporalment
sudo tailscale down

# Reactivar
sudo tailscale up
```

## Connexions amb altres capitols

- **M1 Cap 4** - Xarxa i SSH: la base.
- **Cap 3 d'aquest modul** - SSH hardening: ACLs + claus = seguretat real.
- **Cap 4 d'aquest modul** - Firewall: la segona capa despres de Tailscale.
- **Cap 8 d'aquest modul** - Monitoratge: veure qui intenta accedir.

## Conclusio: per que Tailscale + ACLs es la millor inversio

Tots els capitols d'aquest modul son importants, pero si nomes poguessim triar **una sola mesura** de seguretat, seria Tailscale amb ACLs restrictives. Perque:

1. **Amaga el servidor a Internet**: el port 22 deixa d'estar obert al mon.
2. **Autenticacio forta nomes per a tu**: ningunes altres IPs poden ni intentar entrar.
3. **Zero configuracio de xarxa**: no cal tocar el router, no cal obrir ports.
4. **Funciona desde qualsevol lloc**: cafe, hotel, mobil, igual.

Aixo nomes deixa el risc a un atacant que **robi les teves credencials de Tailscale**, que es un escenari molt mes improbable que un bot qualsevol fent bruteforce a port 22.
