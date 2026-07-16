# Respostes - Capitol 5: MQTT i Mosquitto

> Mira les respostes DESPRES d'haver fet el qüestionari.

## Pregunta 1: Model de comunicacio?

**Resposta correcta**: Publish/subscribe amb un broker central.

**Explicacio**: MQTT es pub/sub pur. Els publishers envien a topics, els subscribers escolten topics, i el broker fa d'intermediari. No hi ha conexio directa publisher-subscriber. Això es el que permet l'escalabilitat i el desacoblament que fan d'MQTT l'estandard IoT.

---

## Pregunta 2: Broker lleuger?

**Resposta correcta**: Mosquitto.

**Explicacio**: Mosquitto es la implementacio de referencia d'MQTT, escrita en C, mantinguda per l'Eclipse Foundation. Es la mes lleugera (unes 30 MB de RAM) i la mes popular per a IoT petit. RabbitMQ es mes potent pero mes pesat; Kafka es per a streaming massiu; Redis Pub/Sub nomes es per a missatgeria en memoria.

---

## Pregunta 3: Wildcard per `hort-osona/`?

**Resposta correcta**: `hort-osona/#`.

**Explicacio**: `#` es un wildcard multi-nivell. Escolta tots els missatges que comencen per `hort-osona/` independentment dels sub-nivells. `+` es nomes per un nivell. L'asterisc `*` no existeix a MQTT. Recorda: `+` es UN nivell, `#` es MOLTS.

---

## Pregunta 4: Retain flag?

**Resposta correcta**: El broker guarda l'ultim missatge i l'entrega als nous subscribers.

**Explicacio**: El retain es una mena de "cache". Si un publisher envia un missatge amb `retain=True`, el broker el desa. Quan un nou subscriber subscriu al topic, rep immediatament l'ultim missatge. Es perfecte per a "ultim valor conegut" (temperatura actual, estat d'un actuator, etc.).

---

## Pregunta 5: Exactly-once?

**Resposta correcta**: QoS 2.

**Explicacio**: QoS 2 es el mes car pero garantitza exactly-once. Usa un handshake de 4 passes (PUBLISH -> PUBREC -> PUBREL -> PUBCOMP). Es molt mes lent que QoS 0 o 1. Usar nomes per a comandes critiques on un duplicat podria ser problematic (ex. una transferencia bancaria, no pas una lectura de temperatura).

---

## Pregunta 6: LWT?

**Resposta correcta**: Un missatge que el broker envia automaticament si el client cau abruptament.

**Explicacio**: Quan un client es connecta, pot configurar un LWT. Si el client es desconnecta sense enviar DISCONNECT (caiguda, pèrdua de xarxa, kill -9), el broker publica automaticament el missatge LWT. Es una manera elegante de detectar caigudes de sensors.

---

## Pregunta 7: Port MQTT amb TLS?

**Resposta correcta**: 8883.

**Explicacio**: 1883 es MQTT sense TLS, 8883 es MQTT sobre TLS. Altres ports possibles: 9001 per WebSockets (navegadors). Mosquitto pot escoltar multiples ports simultanis amb `listener` repetits.

---

## Pregunta 8: Subscriure a tots els missatges?

**Resposta correcta**: `mosquitto_sub -t "#" -v`.

**Explicacio**: `mosquitto_sub` es la CLI de Mosquitto per subscriure's. `-t "#"` selecciona tots els topics (el wildcard universal). `-v` mostra tambe el topic per cada missatge. `mqttcat` existeix pero es una eina de tercers, no oficial.

---

## Pregunta 9 (oberta): QoS per cada cas

**Resposta model**:

**QoS 0** ("at most once"): el missatge es lliura una vegada o gens. Es el mes rapid i el que menys ample de banda gast. No hi ha ACK. Aplica a:
- **Heartbeat periodic del gateway** (cada 30 s). Si en perdem un, el seguent ja es normal. No es critic.
- **Imatge de la camera cada 10 min** (es molt voluminos, i si en perdem una, la seguent ja vindrà). Important: en aquest cas, el payload es gran i QoS 0 evita gast de memoria al broker.

**QoS 1** ("at least once"): el missatge pot arribar duplicat, pero garantitza que arriba. Es el mes usat a IoT. Aplica a:
- **Temperatura ambient cada 5 min**. Si arriba dos cops el mateix valor, InfluxDB el desat amb el mateix timestamp i es sobreescriu. No te importancia.

**QoS 2** ("exactly once"): el missatge arriba exactament un cop. Es el mes lent. Aplica a:
- **Comanda d'obrir una electrovalvula**. Si arriba dos cops, l'electrovalvula obre, tanca, i torna a obrir - o pitjor, s'hi queda oberta massa estona. Es critic garantir unicitat.

Resum: QoS 0 = telemetria no critica. QoS 1 = sensors normals. QoS 2 = comandes actuators. A l'Hort Osona tenim 95% de QoS 1, 4% de QoS 0 (heartbeats), i 1% de QoS 2 (comandes de reg).

---

## Pregunta 10 (oberta): Detectar sensor caigut amb MQTT

**Resposta model**:

Hi ha tres maneres d'usar els mecanismes de MQTT per detectar que un sensor ha deixat d'enviar:

**1. Last Will and Testament (LWT)**: el sensor configura un LWT en connectar-se. Si es desconnecta abruptament (pèrdua de WiFi, bateria esgotada, kill -9), el broker publica automaticament un missatge a `hort-osona/status/sensor/1B32` amb payload `{"status": "offline"}`. Un script escolta aquest topic i actualitza un dashboard o envia una alerta. Avantatge: deteccio instantania. Limitacio: nomes detecta caigudes sobtades, no sensors "vius pero penjats".

**2. Retain + status periòdic**: el sensor publica un heartbeat cada 1-5 min amb `retain=True` a `hort-osona/status/sensor/1B32`. Si un monitor veu que el ultim heartbeat te timestamp de fa >10 min, considera el sensor caigut. Avantatge: detecta qualsevol tipus d'incident (caiguda, congelament, etc). Limitacio: nomes actualitza cada N min.

**3. QoS 1 + acuse de rebut**: el sensor envia amb QoS 1. El broker ha d'enviar un PUBACK. Si el broker no pot entregar (e.g. el sensor esta desconnectat), el missatge queda al buffer (fins a `max_queued_messages`). Un monitor pot revisar el buffer i detectar cuues creixents com a senyal d'incident. Avantatge: deteccio indirecta pero robusta. Limitacio: complex de monitorar.

A l'Hort Osona usem una combinacio: **LWT per a caigudes sobtades** (gateway RPi), i **retain heartbeat cada 5 min** per a sensors individuals. Si el heartbeat no arriba durant 20 min, enviem una alerta per Telegram. Aixo ens permet reaccionar en menys de mitja hora.

---

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum, sobretot QoS i LWT.
- **3-4 encerts**: Repassar la diferencia entre retain, QoS i LWT.
- **0-2 encerts**: Comencem pel basic: quines parts te una comunicacio pub/sub.

## Que fer si has encertat totes

- Passa al **Capitol 6** (InfluxDB per a series temporals).
- Investiga MQTT 5 (la nova versio amb shared subscriptions, message expiry, etc).
- Munta un bridge entre dos brokers Mosquitto (replicacio).
- Compara MQTT amb AMQP, STOMP i CoAP.
- Llegeix l'especificacio oficial d'MQTT 3.1.1 i 5.0 (son curtes).
