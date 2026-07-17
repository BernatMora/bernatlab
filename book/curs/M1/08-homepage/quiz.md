# Qüestionari — Capítol 8: Homepage

> 15 preguntes · ~20 min

## Pregunta 1
Què és Homepage?

- [ ] Un sistema operatiu
- [x] Un dashboard self-hosted per visualitzar serveis del teu homelab
- [ ] Un sistema de còpies de seguretat
- [ ] Un editor de text

## Pregunta 2
A quin port per defecte escolta Homepage?

- [x] 3000 (intern) — exposem el 3010 al host
- [ ] 8080
- [ ] 9000
- [ ] 9090

## Pregunta 3
En quin llenguatge/framework està fet Homepage?

- [ ] PHP
- [ ] Python
- [x] Next.js (React)
- [ ] Java

## Pregunta 4
Quin fitxer conté la llista de serveis a mostrar?

- [ ] config.json
- [x] services.yaml
- [ ] services.xml
- [ ] .env

## Pregunta 5
Quin avantatge té la integració amb Docker (muntant /var/run/docker.sock)?

- [ ] Fa que el contenidor s'arrenqui més ràpid
- [x] Permet el widget Docker que llista contenidors amb el seu estat
- [ ] Redueix l'ús de RAM
- [ ] Dona accés al host

## Pregunta 6
Quin és el format de configuració de Homepage?

- [ ] JSON
- [ ] XML
- [ ] INI
- [x] YAML

## Pregunta 7
Quin widget mostra l'ús de CPU, RAM, disc i temperatura de la RPi?

- [ ] system
- [x] resources
- [ ] stats
- [ ] rpi

## Pregunta 8
Què passa quan edites un fitxer YAML a Homepage?

- [ ] Cal reiniciar el contenidor
- [x] Es recarrega automàticament (hot-reload)
- [ ] Cal fer docker compose up -d
- [ ] Cal fer build manual

## Pregunta 9
Quin és el risc d'exposar Homepage a Internet (sense Tailscale)?

- [ ] Lentitud
- [x] Tothom ve els teus serveis i les URL internes
- [ ] Consum excessiu de RAM
- [ ] Cap, és segur

## Pregunta 10
Quin avantatge té muntar la configuració amb bind mount en lloc d'un volum Docker?

- [ ] Més rapidesa
- [x] Pots editar els fitxers directament al host i fer-ne backup fàcilment
- [ ] Més seguretat
- [ ] No cal reiniciar

## Pregunta 11
Quin camp del `services.yaml` fa que Homepage comprovi periòdicament si el servei està actiu?

- [ ] monitor
- [x] siteMonitor
- [ ] healthCheck
- [ ] status

## Pregunta 12
Com s'agrupen els serveis al `services.yaml`?

- [ ] Per ordre alfabetic
- [x] En una llista amb sub-arrays, on cada sub-array es un grup
- [ ] Per categoria al fitxer settings.yaml
- [ ] Automàticament per tipus

## Pregunta 13 (oberta)
Explica amb les teves paraules: quin avantatge té Homepage respecte obrir directament cada servei (p. ex. http://hortosona:9000 per a Portainer)?

Pistes per respondre:
- Quantes adreces has de recordar sense Homepage?
- Com canvia l'experiència d'ús diari?
- Quin és l'efecte "wow" per als visitants?
- Quin és el risc si tens 20 serveis?

## Pregunta 14 (oberta)
Vols afegir tres serveis nous al dashboard: PiHole (DNS), Jellyfin (multimèdia) i una pàgina personal. Escriu el fragment de `services.yaml` que ho faria.

Pistes per respondre:
- Quins camps són obligatoris (href, name)?
- Quins són opcionals (description, icon, siteMonitor)?
- Com els agruparies?
- Com ho proves abans de fer commit?

## Pregunta 15 (oberta)
Al BernatLab tens Homepage, Portainer, Uptime Kuma i 4 serveis més. Volem afegir un nou servei (un servidor Plex) que trigarà 10 minuts a arrencar. Què passa amb el widget `siteMonitor` d'aquest servei durant l'arrancada? Com ho configuraries per evitar falses alarmes visuals al dashboard?

Pistes per respondre:
- Quin interval té `siteMonitor`?
- Què mostra quan falla (color, icona)?
- Es pot configurar un timeout més llarg?
- Què té a veure amb el `siteMonitor` d'Uptime Kuma (cap 7)?
