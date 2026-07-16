# Respostes - Capitol 4: Arquitectura de l'Hort Osona

> Mira les respostes DESPRES d'haver fet el qüestionari.

## Pregunta 1: Patro arquitectonic?

**Resposta correcta**: Pipe-and-filter (modular amb bus de missatges).

**Explicacio**: Pipe-and-filter vol dir que cada component es un filtre independent (sensor, gateway, processador, DB, API) i es comuniquen a traves de "pipes" (MQTT, HTTP, fitxers). Es un patro arquitectonic classic que permet reemplaçar cada peça sense tocar les altres. Monolit es tot en un sol proces; microserveis es similar pero amb serveis HTTP; serverless es funcions al núvol.

---

## Pregunta 2: Bus de missatges?

**Resposta correcta**: MQTT.

**Explicacio**: MQTT (Message Queuing Telemetry Transport) es el protocol estandard per a IoT, dissenyat per ser lleuger, eficient en xarxes limitades i amb suport QoS. Alternativa: AMQP (mes complex), Kafka (millor per a streaming massiu), ZeroMQ (mes baix nivell). MQTT es el que fan totes les plataformes IoT grans.

---

## Pregunta 3: Quantes etapes?

**Resposta correcta**: 6.

**Explicacio**: Sensor -> Gateway -> MQTT -> Processador -> Emmagatzematge -> API/Web. Son 6 etapes. Es important veure que **cada etapa es independent** i pot ser substituida sense tocar les altres (e.g. canviar InfluxDB per TimescaleDB nomes afecta l'etapa 5).

---

## Pregunta 4: Per que MQTT i no HTTP?

**Resposta correcta**: Permet desacoblar productors i consumidors i te QoS, LWT i buffer.

**Explicacio**: MQTT te moltes avantatges sobre HTTP per a streaming: el broker retè missatges si el consumidor no esta, pots subscriure't a patrons de topics, tens QoS 0/1/2 per garantires l'entrega, LWT per detectar clients caiguts, i es binari (mes rapid que JSON+HTTP). HTTP esta be per a peticions puntuals pero no per a streaming continu.

---

## Pregunta 5: Port de Mosquitto?

**Resposta correcta**: 1883.

**Explicacio**: 1883 es el port per defecte per a MQTT sense TLS. Per a MQTT sobre TLS es 8883. Mosquitto pot escoltar multiples ports (e.g. 1883 intern i 8883 extern amb TLS). Altres brokers (EMQX, HiveMQ) tambe usen 1883 per defecte.

---

## Pregunta 6: Esquema de topics?

**Resposta correcta**: jerarquic amb barres.

**Explicacio**: L'esquema jerarquic amb `/` permet wildcard subscriptions: `+` per un nivell, `#` per multiples. Per exemple, `hort-osona/miflora/+` escolta tots els sensors MiFlora. Si usessim comes o punts, no podriem fer wildcards tan facilment. L'estil "jerarquic amb barres" es l'estandard de facto a MQTT.

---

## Pregunta 7: Si la RPi central mor?

**Resposta correcta**: Les dades deixen d'entrar pero l'historic es conserva.

**Explicacio**: Si la RPi central cau, Mosquitto cau, els gateways BLE no poden publicar res. Pero InfluxDB esta emmagatzemat en un volum Docker (o SSD), per tant l'historic es conserva. Quan tornem a aixecar la RPi, els sensors tornen a enviar. Es l'avantatge d'arquitectura modular: el mal es local, no global.

---

## Pregunta 8: Patro fan-out?

**Resposta correcta**: Fan-out.

**Explicacio**: Fan-out es quan **un missatge** es lliurat a **multiples consumidors**. A MQTT es fa naturalment: el broker entrega el missatge a tots els subscriptors del topic. Un missatge de BME280 pot ser escrit a InfluxDB, evaluat per l'alerta de gelada, i mostrat a la PWA - tres consumidors independents del mateix missatge. Fan-in es el contrari: molts missatges acaben en un (e.g. agregacio).

---

## Pregunta 9 (oberta): Les 6 etapes amb exemple MiFlora

**Resposta model**:

1. **Sensor (MiFlora)**: un tub de plastic amb sensors d'humitat, temperatura, EC i lluminositat. Cada 15 minuts envia una lectura per BLE. Concretament, un Xiaomi HHCCJCY10 amb la MAC `C4:7C:8D:65:1B:32`.

2. **Gateway (RPi amb script Python)**: una RPi 4B amb un adapter BLE USB. Executa `miflora_service.py` (cap 2) que llegeix el sensor i publica a MQTT. Utilitza les llibreries `miflora` i `paho-mqtt`.

3. **Broker MQTT (Mosquitto)**: contenidor Docker `eclipse-mosquitto:2` que escolta al port 1883. Rep el missatge JSON i el distribueix a tots els subscriptors. Te buffer a disc per a missatges pendents.

4. **Processador (script Python)**: contenidor Docker `mqtt-to-influx` (el que hem creat a l'exercici). Escolta `hort-osona/#`, parseja el JSON, construeix un `Point` d'InfluxDB, i l'escriu. Utilitza `paho-mqtt` i `influxdb-client`.

5. **Emmagatzematge (InfluxDB)**: contenidor Docker `influxdb:2.7` que desa les series temporals al bucket `hort-osona` amb retencio de 30 dies. El bucket es a `/var/lib/influxdb2` que es un volum persistent.

6. **API/Web (Flask + PWA)**: una API REST en Flask al port 5000 consulta InfluxDB amb el `QueryClient` i exposa JSON. La PWA (cap 8) consumeix l'API i mostra grafiques amb Chart.js. Tot allotjat a GitHub Pages com a estatic.

---

## Pregunta 10 (oberta): Tolerancia a fallades

**Resposta model**:

L'arquitectura modular sobreviu a la caiguda de l'API web perque **l'API nomes llegeix d'InfluxDB** - no participa en el cami d'entrada de dades. Els sensors continuen enviant, el gateway continua publicant a MQTT, i el processador continua escrivint a InfluxDB. L'unic que es perd es la **visualitzacio** temporal: l'hortola no pot veure les grafiques. Es una fallada "lleu" - les dades son segures.

Si el processador que escriu a InfluxDB tambe caigues, la situacio es mes greu. Mosquitto te **buffer a disc** per defecte (`persistence true` i `persistence_location`), per tant pot retenir milers de missatges pendents. Pero aixo te limits: si el procesador esta caigut durant dies, el buffer pot omplir-se. A mes, el gateway BLE nomes reintenta unes quantes vegades - si no pot publicar, llenca la lectura. Solucio: configurar `max_queued_messages` i `max_queued_bytes` a Mosquitto, i afegir retry logic al gateway.

Si el broker MQTT caigues, es la **peor situacio**. Els missatges nous es perden perque no hi ha qui els distribueixi. Els gateways BLE (MiFlora) no tenen buffer persistent - el que no es publica es perd. Els nodes LoRa tampoc: transmeten i esperen que algu escolti. Solucio per aixo: **replicar el broker** amb un segon Mosquitto en HA (active/passive), o fer que els gateways puguin escriure directament a InfluxDB quan detectin que Mosquitto no respon.

L'element mes critic es, per tant, **el broker MQTT**. Es el "cor" del sistema. Si ell cau, tot es perd. Per això a l'Hort Osona el tenim en un contenidor amb `restart: unless-stopped` i la base de dades en un volum separat.

---

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum, sobretot el diagrama.
- **3-4 encerts**: Repassar MQTT i els seus avantatges respecte HTTP.
- **0-2 encerts**: Comencem pel basic: quines parts te un sistema IoT.

## Que fer si has encertat totes

- Passa al **Capitol 5** (MQTT i Mosquitto en detall).
- Investiga altres brokers: EMQX, HiveMQ, VerneMQ.
- Llegeix sobre arquitectures serverless aplicades a IoT.
- Compara MQTT amb AMQP i Kafka.
- Comença a pensar com muntaries HA per al broker.
