# Qüestionari - Capitol 3: Grafana i dashboards

> 10 preguntes · ~15 min

## Pregunta 1
Quina es la funcio principal de Grafana?

- [ ] Guardar metricas
- [x] Visualitzar dades de series temporals en dashboards
- [ ] Enviar alertes per correu
- [ ] Substituir Prometheus

## Pregunta 2
Quin es el port per defecte de Grafana?

- [ ] 8080
- [ ] 9090
- [x] 3000
- [ ] 80

## Pregunta 3
Com es diu l'element basic d'un dashboard de Grafana?

- [ ] Widget
- [ ] Grafica
- [x] Panell
- [ ] Vista

## Pregunta 4
Quin tipus de panell mostraria un sol numero gran (com "42°C")?

- [ ] Time series
- [ ] Gauge
- [x] Stat
- [ ] Bar chart

## Pregunta 5
Quines son les variables a Grafana?

- [ ] Variables d'entorn del sistema
- [x] Parametres que permeten personalitzar les consultes amb un desplegable
- [ ] Constants que no es poden canviar
- [ ] Un altre nom per les queries

## Pregunta 6
Que es el provisioning a Grafana?

- [ ] Una forma de comprar llicencies
- [x] Configurar data sources i dashboards amb fitxers YAML
- [ ] Un sistema de pagament
- [ ] Un protocol d'autenticacio

## Pregunta 7
Quin ID de grafana.com correspon al dashboard "Node Exporter Full"?

- [ ] 13639
- [x] 1860
- [ ] 893
- [ ] 1

## Pregunta 8
Quina es la URL correcta per afegir Prometheus com a data source dins Docker?

- [ ] http://localhost:9090
- [x] http://prometheus:9090
- [ ] http://127.0.0.1:9090
- [ ] http://host.docker.internal:9090

## Pregunta 9 (oberta)
Explica que son les variables a Grafana i posa un exemple concret de com les usaries al BernatLab per monitorar diversos contenidors.

Pistes per respondre:
- Variables son parametres configurables amb un desplegable.
- Exemple: una variable "contenidor" que filtra per nom.
- Com canviaries una consulta per usar la variable.
- Per que es mes util que fer un panell per contenidor.

## Pregunta 10 (oberta)
Descriu un dashboard basic que tindries per a la RPi del BernatLab. Quins 4-6 panells essentials posaries i per que?

Pistes per respondre:
- Pensa en les coses que vols vigilar: sistema, contenidors, serveis.
- Quines metricas son les mes importants per a la salut del servidor.
- Quin tipus de panell (time series, stat, gauge) per cada una.
- Com els organitzaries al dashboard (files, columnes).


## Pregunta 11 (oberta amb pistes)
Per que Grafana sha convertit en leina de referencia per a monitoritzacio

**Pistes**: pensa en com aplicaries aquest concepte al teu hort IoT amb la teva RPi (hortosona, 100.115.134.76).
## Pregunta 12 (oberta amb pistes)
Explica que es un dashboard i quina diferencia hi ha entre un grafic i una metrica

**Pistes**: pensa en com aplicaries aquest concepte al teu hort IoT amb la teva RPi (hortosona, 100.115.134.76).
## Pregunta 13 (oberta amb pistes)
Quin seria el dashboard mes important del teu hort IoT amb 5 grafiques

**Pistes**: pensa en com aplicaries aquest concepte al teu hort IoT amb la teva RPi (hortosona, 100.115.134.76).
