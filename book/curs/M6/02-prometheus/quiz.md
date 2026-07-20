# Qüestionari - Capitol 2: Prometheus

> 10 preguntes · ~15 min

## Pregunta 1
Que es exactament una metrica per a Prometheus?

- [ ] Un missatge d'error
- [x] Un valor numeric amb marca de temps i opcionalment labels
- [ ] Un log del sistema
- [ ] Un fitxer de text

## Pregunta 2
Quin model d'arquetip fa servir Prometheus per recollir dades?

- [ ] Push: els serveis li envien dades
- [x] Pull: Prometheus va a buscar-les periòdicament
- [ ] Peer-to-peer
- [ ] Per correu electronic

## Pregunta 3
Que es un exporter?

- [ ] Un sistema de copia de seguretat
- [x] Un programa que converteix l'estat d'un servei en metricas Prometheus
- [ ] Un protocol de xarxa
- [ ] Un client de correu

## Pregunta 4
Cada quan recull metricas Prometheus per defecte?

- [ ] Cada segon
- [ ] Cada minut
- [x] Cada 15 segons
- [ ] Cada hora

## Pregunta 5
Quin exporter fa servir Prometheus per obtenir metricas dels contenidors Docker?

- [ ] node_exporter
- [x] cadvisor
- [ ] docker_exporter
- [ ] containerd_exporter

## Pregunta 6
Quin llenguatge de consultes utilitza Prometheus?

- [ ] SQL
- [x] PromQL
- [ ] JSONPath
- [ ] YAML

## Pregunta 7
Quin parametre limita la mida maxima de la base de dades de Prometheus?

- [ ] --storage.tsdb.path
- [x] --storage.tsdb.retention.size
- [ ] --memory.max-size
- [ ] --database.max-bytes

## Pregunta 8
A quin port escolta Prometheus per defecte?

- [ ] 8080
- [ ] 3000
- [x] 9090
- [ ] 9100

## Pregunta 9 (oberta)
Explica la diferencia entre els models pull i push per recollir metricas. Per que Prometheus va triar pull en lloc de push? Posa un exemple del BernatLab.

Pistes per respondre:
- Pull: Prometheus es el que truca. Push: el servei es el que truca.
- Avantatges de pull: saps quins serveis monitors, falla si el servei no respon.
- Desavantatges: els serveis darrere de NAT/firewall son complicats.
- Exemple: node-exporter exposa /metrics, Prometheus el consulta cada 15s.

## Pregunta 10 (oberta)
Has d'afegir monitoritzacio a la teva RPi del BernatLab. Quins 3 exporters afegiries i per que? Pensa en el que es mes important per un servidor casola.

Pistes per respondre:
- node_exporter: metricas del sistema (CPU, RAM, disc, xarxa, temperatura).
- cadvisor: metricas dels teus contenidors Docker.
- Algun altre: nginx_exporter si tens proxy, blackbox_exporter per serveis externs, etc.
- Explica quines metricas de cada un son les mes valuoses.


## Pregunta 11 (oberta amb pistes)
Per que Prometheus emmagatzema dades en series temporals en lloc de base de dades

## Pregunta 12 (oberta amb pistes)
Explica que es un exporter i quina relacio te amb el teu hort IoT

## Pregunta 13 (oberta amb pistes)
Com dissenyaries un dashboard de Prometheus per a la teva RPi
