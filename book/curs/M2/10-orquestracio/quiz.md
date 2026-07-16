# Qüestionari - Capitol 10: Orquestracio

> 10 preguntes · ~15 min

## Pregunta 1
Quina es la funcio principal d'un orquestrador de contenidors?

- [ ] Fer les imatges mes petites
- [x] Gestionar automaticament contenidors en multiples maquines (desplegar, escalar, balancejar)
- [ ] Xifrar les dades
- [ ] Compilar el codi

## Pregunta 2
Quin es l'orquestrador mes simple integrat a Docker?

- [x] Docker Swarm
- [ ] Kubernetes
- [ ] Mesos
- [ ] OpenShift

## Pregunta 3
Quin es l'estandard de la industria per a orquestracio?

- [ ] Docker Compose
- [x] Kubernetes
- [ ] Docker Swarm
- [ ] Podman

## Pregunta 4
Quina es la versio "lleugera" de Kubernetes ideal per a RPi?

- [ ] minikube
- [x] K3s
- [ ] microk8s
- [ ] Docker Swarm

## Pregunta 5
Quan no necessites cap orquestrador?

- [ ] Mai, sempre cal
- [x] Quan tens un sol node i pocs serveis
- [ ] Quan tens mes de 100 serveis
- [ ] Quan tens Windows

## Pregunta 6
Que vol dir "alta disponibilitat" en un cluster?

- [ ] Que el cluster es rapid
- [x] Que un node pot caure sense que els serveis deixin de funcionar
- [ ] Que el cluster te mes memoria
- [ ] Que el cluster te mes CPU

## Pregunta 7
Quin es el principal inconvenient de Kubernetes respecte a Swarm?

- [x] Mes complex i mes recursos necessaris
- [ ] Pitjor rendiment
- [ ] No te auto-healing
- [ ] No es open source

## Pregunta 8
Quantes RPi son el minim recomanable per a un cluster Swarm?

- [ ] 1
- [x] 3 (1 manager + 2 workers)
- [ ] 10
- [ ] 50

## Pregunta 9 (oberta)
Explica amb les teves paraules: quina es la diferencia entre Docker Compose i un orquestrador (Swarm o K8s)? Quan et cal canviar de Compose a Swarm/K8s?

Pistes per respondre:
- Compose: gestio d'un sol host, declarativa, basic.
- Orquestrador: multi-host, auto-healing, rolling updates, alta disponibilitat.
- Si nomes tens 1 RPi i uns 10 serveis, Compose es perfecte.
- Si tens 3-5 RPi i vols que un falli sense parar el servei, llavors cal orquestrador.

## Pregunta 10 (oberta)
Al BernatLab tens una sola RPi amb 8 serveis (Nextcloud, MariaDB, Uptime Kuma, Prometheus, Grafana, etc.). Vols afegir alta disponibilitat. Quines opcions tens? Compara Docker Swarm amb K3s (Kubernetes lleuger) en aquest cas concret.

Pistes per respondre:
- Opcio A: comprar 2 RPi mes i muntar un cluster Swarm (3 nodes).
- Opcio B: comprar 2 RPi mes i muntar un cluster K3s.
- Avantatges i inconvenients de cada un.
- Cost i manteniment.
