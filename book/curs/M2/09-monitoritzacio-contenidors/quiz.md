# Qüestionari - Capitol 9: Monitoritzacio de contenidors

> 15 preguntes · ~20 min

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

## Pregunta 11 (oberta)
Per que creus que la monitoritzacio es sovint menyspreada pels usuaris particulars? Quines consequencies te per al BernatLab no saber si un servei ha caigut fins que tu mateix t'hi connectes? Argumenta amb exemples.

Pistes per respondre:
- "Si funciona, per que mirar?": mentalitat perillosa.
- Un servei pot estar caigut durant dies sense que ningú se n'adoni.
- Hi ha fallades silencioses (ex: la base de dades no escriu pero el servei sembla funcionar).
- Solucio: alertes (Uptime Kuma, Alertmanager) que t'avisen via Telegram/email.
- Trade-off: el temps de configurar la monitoritzacio vs el temps perdut en fallades no detectades.

## Pregunta 12 (oberta)
Quina relacio hi ha entre el volum de logs, la velocitat d'analisi i el cost d'emmagatzematge? Com afecta al BernatLab (100.x.y.z) tenir logs que creixen sense limit? Proposa una politica de retencio raonable.

Pistes per respondre:
- Els logs creixen de forma constant. Sense limit, omplen el disc.
- Disc ple = servei que deixa de funcionar.
- Solucions: rotacio (logrotate), limits per contenidor, enviar a un sistema extern (Loki).
- Politica tipica: 7 dies de logs en calent, 30 dies comprimits, 1 any al núvol.
- Trade-off: quant de temps de historia necessites?

## Pregunta 13 (oberta)
Imagina que el teu company et diu: "jo miro `docker ps` un cop al dia i ja esta". Argumenta per que aixo es insuficient al BernatLab, especialment per a serveis accessibles des d'internet. Quin impacte te una caiguda de 6 hores no detectada?

Pistes per respondre:
- Un cop al dia nomes detecta les fallades que duren mes de 24 hores o que coincideixen amb la teva mirada.
- Una caiguda a les 3 de la matinada pot durar 8 hores fins que te n'adones.
- Si es un servei public, els usuaris pateixen.
- Solucio: monitoritzacio automatica amb alertes.
- Trade-off: inversio de temps en configurar vs. risc d'incidents no detectats.

## Pregunta 14 (oberta)
Aplica el concepte de monitoritzacio al cas concret del BernatLab amb l'stack de dades (PostgreSQL, InfluxDB, Grafana). Quines metricques son essencials per cadascun? Quines alertes configuraries i amb quins llindars? Escriu mentalment un parell de regles d'alerta per a cadascun.

Pistes per respondre:
- PostgreSQL: connexions actives, tamany de la base de dades, replicacio.
- InfluxDB: memoria, write throughput, cardinalitat de series.
- Grafana: si grafana es cau, tot el sistema es cec.
- Alerta tipica: "disk > 85% per a 5 min" via Telegram.
- Llindars inicials: conservador (no vols falses alarmes).

## Pregunta 15 (oberta)
Quines consequencies te per a la salut de la RPi no monitoritzar la temperatura i la salut de la microSD? Al BernatLab, quines metricques del hardware hauries de vigilar i per que? Com pots obtenir-les?

Pistes per respondre:
- La RPi pot escalfar-se, sobretot en caixas tancades. Throttling = rendiment baixa.
- Les microSD tenen una vida util limitada (~100k escritures per cel·la).
- `node-exporter` pot exposar aquestes metricques a Prometheus.
- Alerta important: temperatura > 80°C, SMART errors a la SD.
- Trade-off: mes monitoritzacio = mes consum de recursos. Cal triar.
