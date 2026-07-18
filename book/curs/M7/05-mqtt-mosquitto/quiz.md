# Qüestionari - Capitol 5: MQTT i Mosquitto

> 10 preguntes · ~15 min

## Pregunta 1
Quin es el model de comunicacio de MQTT?

- [ ] Client-server amb HTTP
- [x] Publish/subscribe amb un broker central
- [ ] Peer-to-peer
- [ ] Broadcasting UDP

## Pregunta 2
Quin es el broker MQTT mes utilizat i lleuger?

- [ ] RabbitMQ
- [x] Mosquitto
- [ ] Kafka
- [ ] Redis Pub/Sub

## Pregunta 3
Quin wildcard MQTT escolta tots els missatges que comencen per `hort-osona/`?

- [ ] `hort-osona/*`
- [x] `hort-osona/#`
- [ ] `hort-osona/+`
- [ ] `hort-osona/all`

## Pregunta 4
Que significa el retain flag en un missatge MQTT?

- [ ] El missatge nomes s'entrega un cop
- [x] El broker guarda l'ultim missatge i l'entrega als nous subscribers
- [ ] El missatge es borra despres d'entregar
- [ ] El missatge nomes va a un sol subscriber

## Pregunta 5
Quin QoS garanteix exactly-once delivery?

- [ ] QoS 0
- [ ] QoS 1
- [x] QoS 2
- [ ] QoS 3

## Pregunta 6
Que es el Last Will and Testament (LWT)?

- [ ] Un missatge de comiat quan el client es desconnecta voluntariament
- [x] Un missatge que el broker envia automaticament si el client cau abruptament
- [ ] Un missatge de benvinguda al connectar
- [ ] Un missatge de heartbeat periòdic

## Pregunta 7
Quin es el port per defecte de MQTT amb TLS?

- [ ] 1883
- [x] 8883
- [ ] 8083
- [ ] 8888

## Pregunta 8
Quina ordre pots fer servir per subscriure't a tots els missatges del broker?

- [ ] mosquitto_list
- [x] mosquitto_sub -t "#" -v
- [ ] mqtt_listen
- [ ] mqttcat

## Pregunta 9 (oberta)
Explica la diferencia entre QoS 0, QoS 1 i QoS 2. Per a cada cas d'us dels següents, escriu quin QoS triaries: (a) temperatura ambient cada 5 min, (b) comanda d'obrir una electrovalvula, (c) heartbeat periodic del gateway, (d) imatge de la camera cada 10 min.

Pistes per respondre:
- QoS 0: at most once, rapid, no garanties. OK per telemetria no critica.
- QoS 1: at least once, pot duplicar. OK per sensors normals.
- QoS 2: exactly once, lent. OK per comandes critiques.
- Bufa les lectures en ordre d'importancia.

## Pregunta 10 (oberta)
Un dels teus sensors MiFlora de sobte deixa d'apareixer al dashboard durant 2 hores. Explica 3 maneres de detectar aquest incident usant mecanismes de MQTT (LWT, retain, QoS).

Pistes per respondre:
- LWT: el gateway configura un LWT que es publica si el client MQTT cau.
- QoS: pots configurar QoS 1 i rebre alerta si el broker no pot entregar.
- Subscriptors amb `clean_session=False` reben els missatges perduts quan tornen.
- Compara el ultim timestamp vs. ara; si fa >30 min que no arriba, alerta.


## Pregunta 11 (oberta amb pistes)
Per que MQTT sha adoptat tant a IoT. Pensa en alternatives com HTTP

## Pregunta 12 (oberta amb pistes)
Explica la diferencia entre un topic, un payload i un client a MQTT

## Pregunta 13 (oberta amb pistes)
Com organitzaries els topics MQTT per al teu hort amb 10 sensors diferents
