# Qüestionari — Capítol 6: Portainer

> 10 preguntes · ~15 min

## Pregunta 1
Què és Portainer?

- [ ] Un sistema operatiu per servidors
- [x] Una interfície gràfica web per administrar Docker
- [ ] Una eina de còpies de seguretat
- [ ] Un editor de text

## Pregunta 2
A quin port per defecte escolta Portainer?

- [ ] 80
- [ ] 8080
- [x] 9000
- [ ] 9090

## Pregunta 3
Com accedeixes a Portainer al BernatLab des del navegador?

- [ ] només per IP pública
- [x] http://hortosona:9000 (o per IP Tailscale 100.115.134.76:9000)
- [ ] només per SSH
- [ ] No té interfície web

## Pregunta 4
Com comunica Portainer amb el dimoni Docker?

- [ ] Per una API REST externa
- [x] A través del socket /var/run/docker.sock
- [ ] Per SNMP
- [ ] Per SSH

## Pregunta 5
Què és un "Stack" a Portainer?

- [ ] Un contenidor individual
- [x] Un grup de serveis relacionats, definit normalment amb docker-compose.yml
- [ ] Una imatge Docker
- [ ] Un volum

## Pregunta 6
Què pots fer dins d'un contenidor des de Portainer?

- [ ] Només veure logs
- [x] Veure logs, mètriques, consola, start/stop/restart, recrear
- [ ] Només parar-lo
- [ ] Només veure la mida

## Pregunta 7
Quin avantatge té Portainer respecte a fer-ho tot per SSH?

- [ ] És més ràpid
- [x] Visibilitat centralitzada, control amb clics, no cal recordar ordres
- [ ] Ocupa menys memòria
- [ ] No requereix Docker

## Pregunta 8
Què passa si tens un `docker-compose.yml` al sistema de fitxers I un Stack amb el mateix nom a Portainer?

- [ ] No passa res, coexisteixen pacíficament
- [x] Poden xocar i crear contenidors duplicats o conflictes de ports
- [ ] Portainer sobreescriu sempre
- [ ] El sistema de fitxers té prioritat absoluta

## Pregunta 9 (oberta)
Explica amb les teves paraules: quan faries servir Portainer i quan faries servir la terminal SSH per administrar Docker? Posa exemples concrets al BernatLab.

Pistes per respondre:
- Quines operacions són ràpides per GUI?
- Quines operacions necessiten la terminal?
- Què passa quan tens 3 contenidors vs. 15?

## Pregunta 10 (oberta)
Descriu el flux per afegir un nou servei (per exemple, un servidor Gitea per allotjar repositoris) fent servir Només Portainer, sense tocar la terminal.

Pistes per respondre:
- Quin és el "build method" recomanable?
- Quines dades necessites: imatge, ports, volums, variables?
- Comproves els logs un cop desplegat?
