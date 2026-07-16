# Qüestionari — Capítol 8: Homepage

> 10 preguntes · ~15 min

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

## Pregunta 9 (oberta)
Explica amb les teves paraules: quin avantatge té Homepage respecte obrir directament cada servei (p. ex. http://hortosona:9000 per a Portainer)?

Pistes per respondre:
- Quantes adreces has de recordar sense Homepage?
- Com canvia l'experiència d'ús diari?
- Quin és l'efecte "wow" per als visitants?

## Pregunta 10 (oberta)
Vols afegir tres serveis nous al dashboard: PiHole (DNS), Jellyfin (multimèdia) i una pàgina personal. Escriu el fragment de `services.yaml` que ho faria.

Pistes per respondre:
- Quins camps són obligatoris (href, name)?
- Quins són opcionals (description, icon, siteMonitor)?
- Com els agruparies?
