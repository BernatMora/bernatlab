# Qüestionari - Capitol 10: Orquestracio

> 15 preguntes · ~20 min

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

## Pregunta 11 (oberta)
Per que creus que Kubernetes ha esdevingut l'estandard de la industria tot i la seva complexitat? Quins beneficis reals aporta respecte a Docker Swarm en un entorn productiu?

Pistes per respondre:
- Ecosistema: milers d'eines integrades (Helm, Istio, ArgoCD, etc).
- Portabilitat: el mateix manifest funciona a AWS, GCP, Azure, on-prem.
- Comunitat: mes gent sap K8s que Swarm.
- Treball: mes feines demanen K8s.
- Trade-off: per a un homelab es overkill, pero per a una empresa es essencial.

## Pregunta 12 (oberta)
Quina relacio hi ha entre el cost economic d'un cluster i la disponibilitat que aporta? Al BernatLab (100.115.134.76), val la pena comprar 2 RPi mes per tenir alta disponibilitat? Argumenta amb calcul de cost/benefici.

Pistes per respondre:
- 2 RPi mes = ~120 EUR + 2 fonts + 2 SD = ~200 EUR.
- Temps dedicat a muntar i mantenir el cluster: ~20 h.
- Alta disponibilitat nomes importa si tens usuaris que pateixen caigudes.
- Si nomes ets tu i les caigudes son rares, potser no val la pena.
- Alternatives: una RPi de recanvi en standby, backups frequents.

## Pregunta 13 (oberta)
Imagina que el teu company et diu: "vull posar Kubernetes al BernatLab perque queda molt professional". Argumenta per que aixo es sobredimensionat i proposa alternatives mes adequades a un homelab.

Pistes per respondre:
- K8s nomes te sentit a partir de 3-5 nodes.
- La complexitat operativva es brutal (cert-manager, ingress, networking, storage).
- El overhead de memoria (~500 MB per node) es massa per a una RPi de 4 GB.
- Alternatives: Docker Compose (1 node), Swarm (3-5 nodes), K3s (si realment cal).
- La "professionalitat" no ve de la tecnologia sino de l'operativa: backups, monitoritzacio, documentacio.

## Pregunta 14 (oberta)
Aplica el concepte d'orquestracio al cas concret del BernatLab amb un servei web (Nextcloud) que vols que estigui disponible 24/7. Descriu una solucio progressiva: com començaries amb pocs recursos i com aniries evolucionant si el servei creix.

Pistes per respondre:
- Nivell 1: una sola RPi amb Docker Compose. Acceptar caigudes puntuals.
- Nivell 2: una RPi principal + una de backup amb rsync periodic.
- Nivell 3: cluster de 3 RPi amb Swarm. Auto-healing.
- Nivell 4: Kubernetes (K3s) amb ingress controller i persistent storage.
- Cada nivell te un cost economic i operatiu. Cal triar segons les necessitats.

## Pregunta 15 (oberta)
Quines consequencies te per a la productivitat (teva) la complexitat d'un orquestrador? Si el BernatLab es un projecte personal on tens temps limitat, com equilibraries la sofisticacio tecnica amb el temps que pots dedicar-hi cada setmana? Pensa en manteniment, actualitzacions i troubleshooting.

Pistes per respondre:
- Temps de manteniment d'un cluster K8s: 4-8 h/mes per a un amateur.
- Temps de manteniment d'un Swarm: 1-2 h/mes.
- Temps de manteniment d'un sol node amb Compose: 0-1 h/mes.
- Si tens 2 h/mes per al BernatLab, K8s no es viable.
- Millor un sistema simple que entens i mantens que un complex que no pots cuidar.
- Trade-off final: temps dedicat vs sofisticacio.
