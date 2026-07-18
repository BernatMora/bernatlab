# Qüestionari - Capitol 4: Arquitectura de l'Hort Osona

> 10 preguntes · ~15 min

## Pregunta 1
Quin es el patro arquitectonic principal de l'Hort Osona?

- [ ] Monolit
- [ ] Microserveis
- [x] Pipe-and-filter (modular amb bus de missatges)
- [ ] Serverless

## Pregunta 2
Quin protocol s'usa com a bus de missatges?

- [ ] HTTP
- [ ] gRPC
- [x] MQTT
- [ ] AMQP

## Pregunta 3
Quantes etapes te el pipeline basic de dades?

- [ ] 2
- [ ] 4
- [x] 6
- [ ] 10

## Pregunta 4
Per que MQTT i no HTTP per al bus de missatges?

- [ ] Es mes rapid
- [x] Permet desacoblar productors i consumidors i te QoS, LWT i buffer
- [ ] Es mes segur
- [ ] Es mes modern

## Pregunta 5
Quin es el port per defecte de Mosquitto?

- [ ] 80
- [ ] 443
- [x] 1883
- [ ] 8086

## Pregunta 6
Quin es l'esquema de topics MQTT que usa l'Hort Osona?

- [ ] pla amb comes
- [x] jerarquic amb barres (hort-osona/miflora/1B32)
- [ ] numerat per id
- [ ] aleatori

## Pregunta 7
Que pasa si la RPi central es mor?

- [ ] Tot deixa de funcionar immediatament
- [x] Les dades deixen d'entrar pero l'historic es conserva
- [ ] Es reinicia sola
- [ ] Mosquitto les guarda totes igual

## Pregunta 8
Quin patro fa que un missatge MQTT sigui processat per multiples serveis (e.g. InfluxDB + alerta)?

- [ ] Pipeline
- [x] Fan-out
- [ ] Fan-in
- [ ] Round-robin

## Pregunta 9 (oberta)
Descriu les 6 etapes del pipeline de dades de l'Hort Osona i dona un exemple de cada una aplicat al sensor MiFlora.

Pistes per respondre:
- 1. Sensor captura la dada.
- 2. Gateway llegeix i publica.
- 3. Broker MQTT distribueix.
- 4. Processador transforma.
- 5. Emmagatzematge guarda.
- 6. API/Web mostra.
- Dona un producte o llibreria concreta per cada etapa.

## Pregunta 10 (oberta)
L'API web esta caiguda pero els sensors segueixen funcionant. Explica per que l'arquitectura modular sobreviu a aquesta fallada. Que passaria si el processador que escriu a InfluxDB tambe caigues? I si el broker MQTT caigues?

Pistes per respondre:
- L'API nomes llegeix d'InfluxDB; no afecta l'entrada.
- Si InfluxDB cau, el processador pot fer buffer a disc o esperar.
- Si Mosquitto cau, els missatges nous es perden (no hi ha buffer persistent per defecte).
- Raona sobre quin es l'element mes critic del pipeline.


## Pregunta 11 (oberta amb pistes)
Per que sha de pensar en larquitectura de lhort abans de comprar sensors

## Pregunta 12 (oberta amb pistes)
Explica les capes de larquitectura IoT amb un exemple del teu hort

## Pregunta 13 (oberta amb pistes)
Quin seria el flux de dades del teu hort des del sensor fins a la web
