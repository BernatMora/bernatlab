# Qüestionari — Capitol 6: InfluxDB per a dades de sensors

> 10 preguntes · ~15 min

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
Quin es el port per defecte d'InfluxDB?

- [ ] 5432
- [ ] 3306
- [x] 8086
- [ ] 9090

## Pregunta 8
Quina ordre faries servir per fer un backup consistent d'InfluxDB?

- [ ] cp -r /var/lib/influxdb
- [x] influx backup /tmp/backup
- [ ] tar czf
- [ ] docker save influxdb

## Pregunta 9 (oberta)
Explica amb les teves paraules: per que InfluxDB es millor que PostgreSQL per emmagatzemar lectures de sensors que generen una lectura cada 10 segons?

Pistes per respondre:
- Quin es el volum de dades per any?
- Com es fan les agregacions (mitjana per hora)?
- Quin es l'espai en disc necessari?
- Quin cost te fer consultes per rang temporal?

## Pregunta 10 (oberta)
Tens 50 sensors escrivint cada 5 segons durant 2 anys. Calcula el volum de dades en GB i proposa una estrategia de retencio amb downsampling.

Pistes per respondre:
- Quantes lectures en total?
- Quant ocupa cada lectura a InfluxDB?
- Quanta memoria RAM cal per consultes?
- Estrategia: 30 dies raw, 1 any per hora, 5 anys per dia.
