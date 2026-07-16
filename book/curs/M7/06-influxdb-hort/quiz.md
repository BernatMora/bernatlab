# Qüestionari - Capitol 6: InfluxDB per a l'Hort Osona

> 10 preguntes · ~15 min

## Pregunta 1
Que vol dir TSDB?

- [ ] Time Series Database
- [x] Time Series Data Block
- [ ] Total Storage Data Buffer
- [ ] Tagged SQL Database

## Pregunta 2
Quins son els tres conceptes basics d'InfluxDB per a una lectura de sensor?

- [ ] Table, row, column
- [ ] Document, field, value
- [x] Measurement, tags, fields
- [ ] Entity, attribute, relation

## Pregunta 3
Quin es el llenguatge de consulta d'InfluxDB 2.x?

- [ ] SQL estandard
- [ ] GraphQL
- [x] Flux
- [ ] YAML

## Pregunta 4
Quin es l'avantatge principal d'InfluxDB respecte a PostgreSQL per a series temporals?

- [x] Compressio ~10x i consultes rapidissimes sobre intervals de temps
- [ ] Te mes eines de BI
- [ ] Es mes segur
- [ ] Es open source

## Pregunta 5
Que es un "bucket" a InfluxDB 2.x?

- [ ] Un contenidor d'imatges
- [x] Un contenidor de dades amb retencio
- [ ] Un usuari
- [ ] Un proces automatic

## Pregunta 6
Que es un "task" a InfluxDB?

- [ ] Un tipus de dada
- [x] Un proces automatic que transforma dades (e.g. downsample)
- [ ] Un client de consulta
- [ ] Un trigger d'alerta

## Pregunta 7
Quin es el port per defecte de la API HTTP d'InfluxDB?

- [ ] 1883
- [x] 8086
- [ ] 5000
- [ ] 3000

## Pregunta 8
Que fa el "line protocol" d'InfluxDB?

- [ ] Es un protocol d'encriptacio
- [x] Es el format text per escriure punts (measurement,tag=v field=v timestamp)
- [ ] Es un protocol de xarxa
- [ ] Es el protocol de backup

## Pregunta 9 (oberta)
Explica el model de dades d'InfluxDB (measurement, tag, field, time) i posa un exemple concret amb una lectura del sensor BME280. Compara amb una taula SQL equivalent.

Pistes per respondre:
- Measurement = "bme".
- Tags = device, sector (indexats, per agrupar).
- Fields = temp_c, humidity, pressure (els valors).
- Time = timestamp.
- A SQL: taula lectures(id, device, sector, ts, temp, hum, pres).

## Pregunta 10 (oberta)
Vols guardar lectures de sensors durant 5 anys pero no vols que la base de dades ocupi 500 GB. Explica una estrategia de retencio i downsampling amb InfluxDB.

Pistes per respondre:
- Raw: 30 dies (granularitat original, ocupacio alta).
- Downsample 1h: 1 any (mitjana horaria, ocupacio 1/60).
- Downsample 1d: 5 anys (mitjana diaria, ocupacio 1/1440).
- Crea tasks automatitzades amb Flux.
- Explica quant espai estalviaries per a 5 sensors a 5 min.
