# Qüestionari - Capitol 9: Monitoritzacio de contenidors

> 10 preguntes · ~15 min

## Pregunta 1
Que mostra `docker stats`?

- [ ] Nomes els ports oberts dels contenidors
- [x] Estadistiques en temps real de CPU, RAM, xarxa i disc per contenidor
- [ ] Nomes la memoria usada
- [ ] El contingut dels logs

## Pregunta 2
Quina comanda mostra els logs d'un contenidor?

- [ ] docker show
- [x] docker logs
- [ ] docker read
- [ ] docker inspect --logs

## Pregunta 3
Que es cAdvisor?

- [ ] Un sistema operatiu
- [x] Una eina de Google que mostra metricques visuals dels contenidors
- [ ] Un client Docker
- [ ] Un registre privat

## Pregunta 4
Quina combinacio es l'estandard de la industria per monitoritzar?

- [ ] Apache + PHP
- [x] Prometheus + Grafana
- [ ] Nginx + MySQL
- [ ] Git + Jenkins

## Pregunta 5
Que fa Dozzle?

- [ ] Un servidor de correu
- [x] Una eina web que mostra els logs de tots els contenidors en temps real
- [ ] Un sistema de backups
- [ ] Un balancejador de carrega

## Pregunta 6
Quina es la funcio d'un healthcheck?

- [ ] Auditar la seguretat
- [x] Determinar si un servei esta funcionant correctament dins el contenidor
- [ ] Mesurar la temperatura
- [ ] Comprimir els logs

## Pregunta 7
Quina eina es recomana per monitoritzar si els serveis responen (uptime)?

- [ ] Prometheus
- [x] Uptime Kuma
- [ ] Loki
- [ ] cAdvisor

## Pregunta 8
Quin es el perill de no posar limits als logs?

- [ ] Que els logs es perdin
- [x] Que els logs poden omplir el disc
- [ ] Que els logs no es puguin llegir
- [ ] Que els logs es xifrin automaticament

## Pregunta 9 (oberta)
Explica amb les teves paraules: quina diferencia hi ha entre monitoritzar els recursos (CPU, RAM) i monitoritzar l'aplicacio (latencia, errors)? Per que calen les dues coses?

Pistes per respondre:
- Recursos: el que consumeix el contenidor de l'amfitrio.
- Aplicacio: el que fa l'aplicacio per als usuaris.
- Un pot estar be mentre l'altre falla.
- Dona un exemple: un servei que consumeix poca CPU pero te errors.

## Pregunta 10 (oberta)
Al BernatLab vols muntar un sistema de monitoritzacio amb Prometheus, Grafana i cAdvisor per visualitzar l'estat de tots els teus contenidors. Escriu un `docker-compose.yml` basic que els posi en marxa. Quins serveis afegiries a mes per tenir una visio completa?

Pistes per respondre:
- Els tres basics: Prometheus, Grafana, cAdvisor.
- Afegeix node-exporter per la RPi (CPU, RAM, temperatura).
- Afegeix Uptime Kuma per l'estat dels serveis.
- Afegeix Dozzle per veure els logs.
