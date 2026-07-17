# Qüestionari - Capitol 6: InfluxDB per a dades de sensors

> 15 preguntes · ~20 min

## Pregunta 1
Que significa TSDB?

- [ ] Total System DataBase
- [x] Time Series DataBase
- [ ] Tagged System DataBase
- [ ] Transactional Structured DataBase

## Pregunta 2
Quin tipus de dades estan optimitzades per InfluxDB?

- [ ] Documents JSON
- [x] Series temporals (lectures de sensors amb timestamp)
- [ ] Grafs de relacions
- [ ] Fitxers binaris

## Pregunta 3
Quantes lectures per any pot generar un sensor que escriu cada minut?

- [ ] 52.500
- [x] 525.600
- [ ] 5.256.000
- [ ] 52.560.000

## Pregunta 4
Quin nom rep una "taula" a InfluxDB?

- [ ] Table
- [x] Measurement
- [ ] Series
- [ ] Bucket

## Pregunta 5
Quina diferencia hi ha entre tags i fields?

- [ ] Son el mateix
- [x] Tags son metadades indexades; fields son els valors
- [ ] Fields son indexats; tags no
- [ ] Tags son obligatoris, fields opcionals

## Pregunta 6
Quin llenguatge de consultes fa servir InfluxDB v2?

- [ ] SQL
- [ ] NoSQL
- [x] Flux
- [ ] InfluxQL

## Pregunta 7
Quin es el port per defecte dInfluxDB?

- [ ] 5432
- [ ] 3306
- [x] 8086
- [ ] 9090

## Pregunta 8
Quina ordre faries servir per fer un backup consistent dInfluxDB?

- [ ] cp -r /var/lib/influxdb
- [x] influx backup /tmp/backup
- [ ] tar czf
- [ ] docker save influxdb

## Pregunta 9 (oberta)
Explica amb les teves paraules: per que InfluxDB es millor que PostgreSQL per emmagatzemar lectures de sensors que generen una lectura cada 10 segons?

Pistes per respondre:
- Quin es el volum de dades per any?
- Com es fan les agregacions (mitjana per hora)?
- Quin es lespai en disc necessari?
- Quin cost te fer consultes per rang temporal?

## Pregunta 10 (oberta)
Tens 50 sensors escrivint cada 5 segons durant 2 anys. Calcula el volum de dades en GB i proposa una estrategia de retencio amb downsampling.

Pistes per respondre:
- Quantes lectures en total?
- Quant ocupa cada lectura a InfluxDB?
- Quanta memoria RAM cal per consultes?
- Estrategia: 30 dies raw, 1 any per hora, 5 anys per dia.

## Pregunta 11 (oberta)
Per que creus que InfluxDB ha introduit el llenguatge Flux en lloc de mantenir nomes InfluxQL? Quins beneficis aporta al BernatLab i quins inconvenients?

Pistes per respondre:
- Flux permet consultes mes potents (joins, matemàtica, etc).
- Pero la corba daprenentatge es mes alta.
- Migracio de v1 a v2 requereix reescriure consultes.
- Al BernatLab, val la pena la potencia extra?

## Pregunta 12 (oberta)
Quina relacio hi ha entre la cardinalitat (número de series uniques) i el rendiment dInfluxDB? Com afecta al BernatLab si tens 100 sensors amb 50 tags cadascun? Calcula lexplot memory.

Pistes per respondre:
- Cardinalitat alta = mes memoria RAM.
- Cada serie te un index intern.
- 100 sensors x 50 tags = 5000 series.
- Si cada serie creix amb el temps, el consum es multiplica.
- Trade-off: riquesa de dades vs rendiment.

## Pregunta 13 (oberta)
Imagina que el teu company et diu: "InfluxDB es nomes per a grans volums de dades, per a 5 sensors nhi ha prou amb un fitxer CSV". Argumenta per que al BernatLab InfluxDB te sentit inclús per a pocs sensors.

Pistes per respondre:
- Com consultes un CSV per rang temporal?
- Com agreges lectures per hora?
- Com comparteixes les dades amb Grafana?
- Cas concret: 5 sensors x 5 anys = 13M de files, gestionables amb InfluxDB pero no amb CSV.

## Pregunta 14 (oberta)
Aplica el concepte dInfluxDB al cas concret del BernatLab amb lhort IoT. Tens 10 sensors (temperatura, humitat, llum, etc) que envien lectures cada 30 segons via MQTT. Dissenna lespai de dades: measurements, tags i fields. Justifica cada decisio.

Pistes per respondre:
- Un measurement per tipus de dada o un per tot?
- Que va com a tag (indexat) i que va com a field (valor)?
- Quins son els patrons de consulta mes freqUents?
- Quant creixera la base de dades en un any?

## Pregunta 15 (oberta)
Quines consequencies te per a la sostenibilitat a llarg termini triar InfluxDB (que esta en constant evolucio) al BernatLab? Com t'afecten els canvis de versio i la possible migracio futura?

Pistes per respondre:
- InfluxDB 1.x a 2.x: canvis breaking.
- 2.x a 3.x: mes canvis.
- Les dades antigues son compatibles?
- Quina estrategia de migracio tindries?
- Trade-off: funcionalitat moderna vs estabilitat.
