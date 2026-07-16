# Respostes - Capitol 2: Tailscale i ACLs

> Mira les respostes DESPRES d'haver fet el qüestionari.

## Pregunta 1: Que es Tailscale?

**Resposta correcta**: Una eina que crea una xarxa privada (VPN) entre els teus dispositius usant WireGuard.

**Explicacio**: Tailscale es la capa d'identitat i xarxa. Fa servir WireGuard per xifrar les comunicacions i un servidor de coordinacio per intercanviar claus publices. Es un "mesh VPN": cada dispositiu connecta directament amb l'altre, no hi ha un servidor central pel trafic. Es diferent d'un antivirus o un sistema operatiu: nomes construeix una xarxa privada.

---

## Pregunta 2: Protocol de Tailscale

**Resposta correcta**: WireGuard.

**Explicacio**: WireGuard es un protocol modern (~4000 linies de codi) que es mes rapid i simple que OpenVPN o IPSec. Tailscale l'envolta amb una gestio de claus automatica (el que seria un maldecap fer manualment). El trafic sempre va xifrat amb ChaCha20 i autenticat amb Poly1305.

---

## Pregunta 3: MagicDNS

**Resposta correcta**: El servei de DNS automatic de Tailscale que permet usar noms en lloc d'IPs.

**Explicacio**: MagicDNS configura el DNS del sistema per resoldre automàticament els noms dels teus dispositius Tailscale. Pots fer `ssh raspberry` en lloc de `ssh pi@100.64.0.1`. Es molt convenient per scripts i per Humans. No te res a veure amb seguretat de contrasenyes o filtres web.

---

## Pregunta 4: Format de les ACLs

**Resposta correcta**: HuJSON (JSON amb comentaris).

**Explicacio**: HuJSON es com JSON pero permet comentaris amb `//` i `/* */`. Es molt mes facil de mantenir ACLs llargues amb comentaris explicatius. Tailscale el converteix a JSON valid abans d'aplicar-lo. La consola web tambe et mostra la sintaxi correcta si t'equiviques.

---

## Pregunta 5: dst: ["raspberry:22,80,443"]

**Resposta correcta**: Que la maquina raspberry es accessible pels ports 22, 80 i 443.

**Explicacio**: La part abans dels dos punts es la maquina desti (pot ser nom, IP, o etiqueta). La part despres es el port o llista de ports. Si poses `*` vol dir "tots els ports", pero nomes usa-ho si realment cal. Els ports 22, 80 i 443 son la combinacio classica: SSH, HTTP i HTTPS.

---

## Pregunta 6: Que son les tag?

**Resposta correcta**: Etiquetes que permeten agrupar maquines per funcio i aplicar regles per grup.

**Explicacio**: Les tags (etiquetes) son metadades que assignes a una maquina. Son mes estables que el nom del host (que pot canviar) i mes flexibles que la IP (que es especifica d'una maquina). Pots etiquetar maquines com "server", "homelab", "personal", i despres escriure regles que afectin tot el grup. Per exemple, "tots els personal poden accedir al server pels ports web".

---

## Pregunta 7: Politica per defecte

**Resposta correcta**: Tot esta denegat (els membres nomes es veuen entre ells a la xarxa Tailscale).

**Explicacio**: Tailscale segueix el principi de "deny by default". Si no hi ha cap regla que permeti una comunicacio, esta bloquejada. Els teus dispositius es veuen entre ells pero cap servei concret es accessible fins que una ACL ho permeti explicitament. Es la postura mes segura.

---

## Pregunta 8: Comanda per veure la IP

**Resposta correcta**: `tailscale ip`.

**Explicacio**: `tailscale ip` retorna la IP que Tailscale ha assignat a la maquina actual. `tailscale status` llista totes les maquines del tailnet amb les seves IPs. `tailscale ping maquina` comprova si pots arribar a una maquina concreta. `tailscale get` llegeix prefs del client.

---

## Pregunta 9 (oberta): Minim privilege al BernatLab

**Resposta model**:

El principi de **minim privilege** diu que cada usuari nomes ha de tenir els permisos que realment necessita per fer la seva feina, ni mes ni menys. Es el mateix principi que a una empresa: el comptable no ha de poder entrar al servidor de desenvolupament, tot i que tots dos son treballadors. Aplica aquesta logica a les ACLs.

Al BernatLab, amb 3 rols tipics:

**Administrador (bernat@bernatlab.cat)**: soc jo, l'unic que fa manteniment. Necessito **tots** els acces: SSH al servidor (port 22), web (80/443), Home Assistant (8123), Gitea (3000), Portainer (9000), la base de dades (5432), tot. Per tant:

```json
{
  "action": "accept",
  "src":    ["autogroup:admin"],
  "dst":    ["tag:server:*"]
}
```

**Company de casa (marina@bernatlab.cat)**: nomes vol consultar els sensors de temperatura i obrir el garatge des del telefon. No toca ni la configuracio ni les dades. Nomes cal el port 8123 (Home Assistant) i prou:

```json
{
  "action": "accept",
  "src":    ["user:marina@bernatlab.cat"],
  "dst":    ["tag:server:8123"]
}
```

**Amic tecnic que m'ajuda puntualment**: l'Oriol, que em va muntar la RPi al principi. Li dono acces nomes a SSH i nomes durant 1 setmana. Despres li trec:

```json
{
  "action": "accept",
  "src":    ["user:oriol@amics.cat"],
  "dst":    ["tag:server:22"]
}
```

Si comparteixo la contrasenya de Tailscale amb tothom i poso una sola regla "tot per a tothom", l'Oriol accidentalment podria esborrar una base de dades, la Marina podria veure coses que no toca, i jo tindria menys visibilitat sobre qui ha fet què. El minim privilege no es nomes per seguretat tecnica, tambe es per **evitar accidents humans**.

---

## Pregunta 10 (oberta): Tailscale vs port 22 obert

**Resposta model**:

Tenir el port 22 obert a Internet es com viure en un carrer transitat amb la porta de casa oberta. Tothom que passa pot mirar, i els lladres saben que en algun moment trobaran algú que s'ha deixat la clau al pany. Segons la meva propia auditoria (capitol 1), la RPi rebrà milers d'intents de bruteforce al dia. La majoria son bots, pero alguns son humans, i tots ells **tenen la oportunitat** d'entrar.

Tailscale amb ACLs es com viure en un carrer privat amb porter. La porta principal nomes es pot creuar si el porter et reconeix. Els bots ni tan sols saben que existeixo, perque **la meva IP publica ni tan sols te cap servei exposat** (el servidor nomes escolta a la interfície Tailscale, no a `0.0.0.0`). Si proves `nmap` a la meva IP publica, veuras que tots els ports estan tancats, ni tan sols el 22.

El risc que queda amb Tailscale es: que robin les meves credencials de Tailscale (un atac de phishing, un password reuse, o un token filtrat). Es un risc **molt inferior** al risc de tenir el port obert, perque Tailscale te 2FA obligatori, monitoratge de sessions, i pots revocar un dispositiu des de la consola en 10 segons. Si rebo el correu "Bernat, un nou dispositiu s'ha afegit al teu tailnet" i no soc jo, el bloqueges immediatament i l'atacant perd l'acces.

Aixo es la gran diferencia: amb el port 22 obert, l'atacant te temps infinit per probar. Amb Tailscale, l'atacant nomes te una oportunitat, i a mes jo rebo un avís. Per tant, Tailscale es **la millor inversio** de temps i diners que pots fer en seguretat homelab.

---

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum i fer l'exercici practic.
- **3-4 encerts**: Repeteix l'exercici sense mirar les ACLs d'exemple.
- **0-2 encerts**: Torna a mirar la consola de Tailscale i juga amb les opcions.

## Que fer si has encertat totes

- Passa al **Capitol 3** (SSH hardening).
- Investiga com configurar **Taildrop** per transferir fitxers.
- Apren sobre **subnets** a Tailscale: pots exposar tota la xarxa local darrere d'un node.
- Llegeix sobre les **diferencies entre Tailscale i ZeroTier** (un competidor open source).
