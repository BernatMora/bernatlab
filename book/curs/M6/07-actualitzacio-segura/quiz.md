# Qüestionari - Capitol 7: Actualitzacio segura

> 10 preguntes · ~15 min

## Pregunta 1
Quina comanda actualitza la llista de paquets disponibles a apt?

- [ ] sudo apt install
- [x] sudo apt update
- [ ] sudo apt upgrade
- [ ] sudo apt list

## Pregunta 2
Quin paquet s'encarrega de les actualitzacions automatiques de seguretat a Debian/Raspbian?

- [ ] cron-apt
- [x] unattended-upgrades
- [ ] apt-cacher
- [ ] auto-update

## Pregunta 3
Quina eina s'encarrega d'actualitzar automaticament els contenidors Docker?

- [ ] Portainer
- [x] Watchtower
- [ ] Docker Auto-Update
- [ ] Compose Auto

## Pregunta 4
Quina label de Docker cal posar a un contenidor perque Watchtower l'actualitzi?

- [ ] com.docker.auto-update=true
- [x] com.centurylinklabs.watchtower.enable=true
- [ ] watchtower.update=true
- [ ] auto-update.enable=true

## Pregunta 5
Per que es mala idea fer `image: servei:latest`?

- [ ] Latest es mes lent
- [x] Perque cada pull pot obtenir una versio diferent i el sistema pot trencar-se
- [ ] Latest no existeix a Docker Hub
- [ ] Latest nomes funciona a Linux

## Pregunta 6
Quin eina de GitHub revisa automaticament dependències i envia PRs?

- [ ] GitHub Actions
- [x] Dependabot
- [ ] Renovate
- [ ] GitHub Security

## Pregunta 7
Quina tecnica permet actualitzar un servei sense temps d'inactivitat?

- [ ] Cold start
- [x] Blue-Green deployment
- [ ] Hard reset
- [ ] Force upgrade

## Pregunta 8
Quin tipus d'actualitzacio (PATCH/MINOR/MAJOR) es pot aplicar sempre sense riscos?

- [x] PATCH
- [ ] MINOR
- [ ] MAJOR
- [ ] Totes tenen el mateix risc

## Pregunta 9 (oberta)
Explica quina es la teva estrategia per actualitzar els serveis del BernatLab de forma segura. Quins automatitzaries i quins faries manualment? Justifica per que.

Pistes per respondre:
- Automatitzar: actualitzacions de seguretat del sistema (unattended-upgrades), Watchtower per serveis no critics.
- Manual: bases de dades, contenidors amb dades importants, serveis que canvien sovint.
- Justifica amb criteris: risc, criticitat, facilitat de rollback.

## Pregunta 10 (oberta)
Has d'actualitzar la versio major de Home Assistant (de 2024.5 a 2025.1) que te canvis incompatibles. Escriu el procediment pas a pas que seguiries per minimizar el risc de deixar la casa "tonta".

Pistes per respondre:
- Pas 1: llegir CHANGELOG i breaking changes.
- Pas 2: fer backup complet (base de dades, configuracio, snapshots).
- Pas 3: provar en entorn local si es pot.
- Pas 4: actualitzar en hora baixa.
- Pas 5: verificar funcionalitats claus (automatitzacions, integracions).
- Pas 6: tenir pla de rollback.


## Pregunta 11 (oberta amb pistes)
Per que es important actualitzar tambe el kernel de la RPi i no nomes els paquets

**Pistes**: pensa en com aplicaries aquest concepte al teu hort IoT amb la teva RPi (hortosona, 100.115.134.76).
## Pregunta 12 (oberta amb pistes)
Explica que es un rolling update i per que sha daplicar al teu sistema

**Pistes**: pensa en com aplicaries aquest concepte al teu hort IoT amb la teva RPi (hortosona, 100.115.134.76).
## Pregunta 13 (oberta amb pistes)
Com validaries que una actualitzacio sha funcionat correctament

**Pistes**: pensa en com aplicaries aquest concepte al teu hort IoT amb la teva RPi (hortosona, 100.115.134.76).
