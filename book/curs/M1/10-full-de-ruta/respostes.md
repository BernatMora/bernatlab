# Respostes — Capítol 10: Full de ruta

> Mira les respostes DESPRÉS d'haver fet el qüestionari.

## Pregunta 1: Rol de File Browser

**Resposta correcta**: Navegar, pujar, baixar i editar fitxers des del navegador.

**Explicació**: File Browser és una interfície web per al sistema de fitxers. Permet fer gairebé tot el que faries per SSH/SCP/SFTP però des del navegador. Alternativa més avançada: Nextcloud (que afegeix sincronització amb apps d'escriptori i mòbil).

## Pregunta 2: Tipus d'eina de Node-RED

**Resposta correcta**: Una eina de programació visual basada en fluxos.

**Explicació**: Node-RED és low-code: arrossegues nodes (blocs funcionals) i els connectes amb cables. Cada node té una funció (llegir un sensor, enviar un correu, transformar dades). Combinant nodes crees fluxos complexos sense escriure gairebé codi. Alternativa: n8n, Node-RED és la més popular al món IoT.

## Pregunta 3: Què és MQTT?

**Resposta correcta**: Un protocol de missatgeria lleuger publish/subscribe per a IoT.

**Explicació**: MQTT (Message Queuing Telemetry Transport) va ser creat per IBM el 1999 per a sensors amb poc ample de banda. El model publish/subscribe permet que molts dispositius parlin amb molts altres sense coneixement mutu: només coneixen el "topic". Broker: Mosquitto, EMQ X, HiveMQ.

## Pregunta 4: InfluxDB

**Resposta correcta**: Per emmagatzemar dades de sèries temporals (temperatura, mètriques, sensors).

**Explicació**: InfluxDB és una TSDB (Time Series Database) optimitzada per ingents volums de dades amb marca temporal. Cada "mesura" té un timestamp, camps (valors) i tags (etiquetes). Compressions, agregacions i retenció són natives. Alternativa: TimescaleDB (extensió de PostgreSQL), Prometheus (per mètriques).

## Pregunta 5: Rol de Grafana

**Resposta correcta**: Visualitzar dades amb dashboards, gràfiques i alertes.

**Explicació**: Grafana és l'eina estàndard per a dashboards d'observabilitat. Suporta 50+ fonts de dades (InfluxDB, Prometheus, PostgreSQL, MySQL, Elasticsearch, Loki, ...). Permet crear panells interactius, alertes per Slack/Telegram, plantilles reutilitzables.

## Pregunta 6: Diferència InfluxDB vs PostgreSQL

**Resposta correcta**: InfluxDB és per a sèries temporals d'alta velocitat; PostgreSQL per a dades estructurades.

**Explicació**: InfluxDB brilla amb milions de punts/dia (temperatura cada 30s = 2880 punts/dia per sensor, escala horriblement bé fins a milions). PostgreSQL brilla amb dades amb relacions complexes i transaccions (un usuari, moltes comandes, transaccions ACID). Al BernatLab farem servir les dues: InfluxDB per a mètriques, PostgreSQL per a Gitea, Nextcloud, etc.

## Pregunta 7: Què és LoRa?

**Resposta correcta**: Una tecnologia de ràdio de baix consum i llarg abast per a IoT.

**Explicació**: LoRa (Long Range) és una modulació de ràdio patentada per Semtech. Combinada amb el protocol LoRaWAN, permet dispositius IoT amb bateries que duren 5-10 anys comunicant-se a 1-10 km. Alternativa: SigFox (propietari), NB-IoT (cel·lular).

## Pregunta 8: Freqüència LoRa a Europa

**Resposta correcta**: 868 MHz

**Explicació**: Europa usa la banda 868 MHz (ETSI EN 300 220), amb sub-bandes i duty cycle limitat (1% a 0.1%). EUA usa 915 MHz, Àsia 433 MHz. A Espanya, la regulació la gestiona la CNMC.

## Pregunta 9 (oberta): Flux MQTT → InfluxDB → Grafana

**Resposta model**:

Per mesurar la temperatura de l'hort i veure-la a una gràfica, el flux és:

**1. Capa física (sensor)**: un sensor LoRa (com el BME280 + placa LoRa) mesura temperatura i humitat cada 5 minuts. S'activa, pren la lectura, l'envia per ràdio a 868 MHz, i torna a dormir (durada de la bateria: 2-5 anys amb piles AA).

**2. Gateway LoRa**: un dispositiu com el RAK7240 o un Heltec + Raspberry Pi Zero escolta contínuament a 868 MHz. Quan rep un paquet LoRa del sensor, el descodifica i l'envia per WiFi/ethernet al servidor ChirpStack (que viu a la RPi del BernatLab o un Mini PC dedicat).

**3. ChirpStack (LoRaWAN Network Server)**: autentica el sensor (ús de AppKey + DevNonce per evitar repeticions), descodifica el payload (sovint binari compacte, tipus CayenneLPP o similar), i publica un missatge MQTT al broker:
- Topic: `application/1/device/abcdef1234567890/event/up`
- Payload (JSON): `{"temperature": 23.5, "humidity": 65.2, "battery": 3.2, "timestamp": "2026-07-16T10:30:00Z"}`

**4. Broker MQTT (Mosquitto)**: rep el missatge al topic. Qualsevol subscriptor pot rebre'l. Aquí hi ha diversos actors interessats.

**5. Node-RED (opcional, com a "traductor")**: escolta el topic de ChirpStack i l'envia a InfluxDB en un format que InfluxDB entén. Alternativa: Telegraf (agent de dades de la família InfluxData) pot fer aquesta feina directament sense Node-RED.

**6. InfluxDB (emmagatzemament)**: rep un "punt" amb timestamp, camps (temperature, humidity) i tags (sensor_id="hort-nord", location="hort"). Cada 5 minuts s'afegeix un nou punt. Al cap d'un dia tens 288 punts per sensor. Al cap d'un mes, 8.640. InfluxDB comprimeix automàticament.

**7. Grafana (visualització)**: té InfluxDB configurat com a "Data source". Creo un dashboard amb un panell "Temperatura hort" que fa:
- Query: `SELECT mean("temperature") FROM "measurement" WHERE $timeFilter GROUP BY time(15m)`
- Tipus: gràfica de línia.
- Eix X: temps.
- Eix Y: graus Celsius.

Veig la gràfica en temps real. Si vull, puc posar alertes: "Avisa'm si la temperatura baixa de 0°C (per gelades) o puja de 35°C (per estrès tèrmic)".

**Visualització final**: obro el navegador a `http://hortosona:3030` (Grafana via Tailscale) i veig la temperatura actual i la gràfica de les últimes 24h, setmana, mes o any. També ho puc incrustar a Homepage com a iframe o un widget personalitzat.

**Resum del flux**:
```
Sensor (LoRa) → Gateway → ChirpStack → MQTT broker → InfluxDB → Grafana
                                          ↑
                                       (i Node-RED si cal transformar)
```

Cada component fa UNA cosa i la fa bé. Combinant-los, construeixo sistemes potents sense escriure aplicacions monolítiques.

## Pregunta 10 (oberta): Projecte preferit

**Resposta model**:

Tria personal — jo em decantaria pel **M4 (Dades) i M5 (IoT)** perquè el projecte de l'Hort Osona és el que m'apassiona.

**El projecte**: monitorar les condicions ambientals de l'hort familiar que tenim a Osona. Quatre sectors amb cultius diferents (tomàquets, enciams, carbassons, herbes aromàtiques). Vull saber:
- Temperatura i humitat de l'aire.
- Temperatura i humitat del terra.
- Pluviometria.
- Radiació solar.
- Vent.

**Per què m'interessa**: el meu avi tenia molt de coneixement intuïtiu sobre l'hort ("si el cel és vermell al matí, avui plourà"). Vull capturar part d'aquest coneixement amb dades reals, i veure si puc correlacionar lectures amb el rendiment dels cultius. A més, és una excusa per aprendre tecnologia fent quelcom útil.

**Eines que hi hauria d'utilitzar**:
- **LoRa + ChirpStack** (M5-31): perquè l'hort no té WiFi ni cobertura cel·lular. La tecnologia LoRa em permet sensors amb piles que duren anys.
- **MQTT (Mosquitto)** (M4-25): per comunicar sensors amb el sistema central.
- **Node-RED** (M3-19): per processar les dades, fer càlculs (punt de rosada, sensació tèrmica, etc.) i enviar alertes.
- **InfluxDB** (M4-26): per emmagatzemar l'historial de lectures.
- **Grafana** (M4-27): per visualitzar gràfiques i tendències.
- **Homepage** (M1-8): per tenir un accés ràpid al dashboard de l'hort des del mòbil.
- **Telegram** (M1-7): per rebre alertes al mòbil quan alguna cosa vagi malament (gelada imminent, manca d'aigua, etc.).

**Problema concret que em resoldrà**:
1. Detectar gelades a temps per protegir les plantes amb mantes tèrmiques (alerta Telegram quan la temperatura baixa de 2°C).
2. Optimitzar el reg (no regar si ja ha plogut prou).
3. Aprendre quines varietats de tomàquet funcionen millor al microclima de l'hort.
4. Comparar l'evolució entre anys ("l'any passat vam tenir X kg de tomàquets, enguany Y, les condicions van ser...").

**Primer pas concret**: acabar el M2 (Mòdul de Productivitat) per tenir ben muntada la infraestructura bàsica (PostgreSQL, Gitea, Nextcloud), i després saltar al M4 i M5 per al projecte de l'hort. També vull fer un viatge a veure el meu avi per recollir el seu coneixement abans que es perdi.

## Què fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum, sobretot la part del flux MQTT-InfluxDB-Grafana.
- **3-4 encerts**: Torna a llegir amb atenció les seccions d'InfluxDB i Grafana.
- **0-2 encerts**: Repassem junts el capítol.

## Què fer si has encertat totes

- **Felicitats! Has acabat el Mòdul 1 (Fonaments) del curs del BernatLab.**
- Passa al **Mòdul 2 (Productivitat)** — el primer capítol serà sobre File Browser i compartició de fitxers.
- Comparteix el que has après amb algú (escriu un post, ensenya-ho a un amic, etc.).
