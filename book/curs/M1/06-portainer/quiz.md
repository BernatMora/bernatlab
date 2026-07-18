# Qüestionari — Capítol 6: Portainer

> 15 preguntes · ~20 min

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
- [x] http://hortosona:9000 (o per IP Tailscale 100.x.y.z:9000)
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

## Pregunta 9
Quina pestanya de Portainer et mostra gràfiques de CPU i RAM d'un contenidor?

- [ ] Logs
- [x] Stats
- [ ] Inspect
- [ ] Console

## Pregunta 10
Què passa si crees un contenidor des de Portainer sense volum muntat?

- [ ] El contenidor no arrenca
- [x] Les dades es perden quan el contenidor s'atura
- [ ] S'usa la memòria RAM com a emmagatzematge
- [ ] Docker ho impedeix

## Pregunta 11
Com esborraries un contenidor de forma segura des de Portainer?

- [ ] Stop + Remove (volums inclosos)
- [x] Stop + Remove (sense volumes, mantenint-los)
- [ ] Directament Delete
- [ ] No es pot esborrar

## Pregunta 12
Quin és el risc principal de donar accés a Portainer a algú que no ets tu?

- [ ] Que consumeixi CPU
- [x] Que pugui esborrar serveis, imatges, volums sense confirmar
- [ ] Que vegi les teves contrasenyes
- [ ] Cap, Portainer no pot fer res perillós

## Pregunta 13 (oberta)
Explica amb les teves paraules: quan faries servir Portainer i quan faries servir la terminal SSH per administrar Docker? Posa exemples concrets al BernatLab.

Pistes per respondre:
- Quines operacions són ràpides per GUI?
- Quines operacions necessiten la terminal?
- Què passa quan tens 3 contenidors vs. 15?
- Quin flux de treball és més segur (reversible vs destructiu)?

## Pregunta 14 (oberta)
Descriu el flux per afegir un nou servei (per exemple, un servidor Gitea per allotjar repositoris) fent servir Només Portainer, sense tocar la terminal.

Pistes per respondre:
- Quin és el "build method" recomanable?
- Quines dades necessites: imatge, ports, volums, variables?
- Comproves els logs un cop desplegat?
- Quin risc té fer canvis només per GUI (sense git)?

## Pregunta 15 (oberta)
Al BernatLab tens Portainer exposat a la xarxa Tailscale. Vols deixar accedir-hi a un amic que t'ajuda amb el projecte, però sense que pugui esborrar res. Quines mesures prendries?

Pistes per respondre:
- Quin sistema d'autenticació té Portainer?
- Com es creen rols i usuaris?
- On és el límit del que Portainer pot protegir?
- Quina és la diferència entre autenticació i autorització?
