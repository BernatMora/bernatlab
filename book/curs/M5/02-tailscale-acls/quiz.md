# Qüestionari - Capitol 2: Tailscale i ACLs

> 10 preguntes · ~15 min

## Pregunta 1
Que es Tailscale?

- [ ] Un antivirus per servidors
- [ ] Un sistema operatiu per Raspberry Pi
- [x] Una eina que crea una xarxa privada (VPN) entre els teus dispositius usant WireGuard
- [ ] Un servei de DNS public

## Pregunta 2
Quin protocol utilitza Tailscale per xifrar les comunicacions?

- [ ] OpenVPN
- [ ] IPSec
- [x] WireGuard
- [ ] SSH

## Pregunta 3
Que es MagicDNS?

- [ ] Un sistema per generar contrasenyes aleatories
- [ ] Un servei de DNS magic per la web
- [x] El servei de DNS automatic de Tailscale que permet usar noms en lloc d'IPs
- [ ] Un filtre de contingut web

## Pregunta 4
Quin format te el fitxer d'ACLs de Tailscale?

- [ ] XML
- [ ] YAML
- [x] HuJSON (JSON amb comentaris)
- [ ] TOML

## Pregunta 5
Que vol dir `dst: ["raspberry:22,80,443"]` en una ACL?

- [ ] Que raspberry nomes pot accedir als ports 22, 80 i 443
- [ ] Que raspberry es accessible nomes des dels ports 22, 80 i 443 del client
- [x] Que la maquina raspberry es accessible pels ports 22, 80 i 443
- [ ] Que els clients han d'estar als ports 22, 80 i 443

## Pregunta 6
Que son les "tag" a Tailscale?

- [ ] Marques dins del text per trobar maquines
- [x] Etiquetes que permeten agrupar maquines per funcio i aplicar regles per grup
- [ ] Noms alternatius per les maquines
- [ ] Sistemes d'alerta per events

## Pregunta 7
Per defecte, quina es la politica d'ACLs si no en poses cap?

- [ ] Tot esta permes
- [x] Tot esta denegat (els membres nomes es veuen entre ells a la xarxa Tailscale)
- [ ] Tot nomes es pot fer localment
- [ ] Cal demanar permís a l'admin cada vegada

## Pregunta 8
Quina ordre mostra la IP Tailscale assignada a la teva maquina?

- [ ] tailscale status
- [ ] tailscale ping
- [x] tailscale ip
- [ ] tailscale get

## Pregunta 9 (oberta)
Explica que es el principi de "minim privilege" aplicat a les ACLs. Dona un exemple concret amb tres rols diferents al BernatLab.

Pistes per respondre:
- Pensa en qui ha d'accedir a quines coses.
- Inventa tres rols: administrador, company de casa, amic tecnic que t'ajuda puntualment.
- Escriu les regles JSON que farien falta per a cada cas.
- Explica per que NO es bona idea que tothom ho pugui fer tot.

## Pregunta 10 (oberta)
Per que Tailscale amb ACLs es considera la millor primera defensa, encara que tambe posem altres mesures? Compara-ho amb l'escenari de tenir el port 22 obert a Internet.

Pistes per respondre:
- Calcula quants intents de bruteforce reps al dia amb el port 22 obert.
- Explica com Tailscale canvia el pais: de "a tothom" a "nomes jo".
- Esmenta quin risc queda un cop tens Tailscale activat.
- Conclou amb una analogia: tenir casa a un carrer transitat vs un carrer privat.


## Pregunta 11
Per que Tailscale utilitza ACLs en lloc de regles de firewall tradicionals? Quins avantatges te per a un homelab?

**Pistes**: Pistes: Identitat vs IP, escalabilitat, MagicDNS, nodes personals.

## Pregunta 12
Explica la diferencia entre una ACL que permet 'tag:server ssh' i una que permet '192.168.1.10:22'.

**Pistes**: Pistes: Tags, identitat, manteniment, futur.

## Pregunta 13
Quines consequencies pot tenir una ACL massa permissiva al teu hort IoT? Pensa en sensors i dades personals.

**Pistes**: Pistes: Exposicio, atac, dades personals, sensors.


## Pregunta 14 (oberta amb pistes)
Per que Tailscale utilitza ACLs en lloc de regles de firewall tradicionals

## Pregunta 15 (oberta amb pistes)
Explica la diferencia entre tag:server ssh i 192.168.1.10:22 a una ACL
