# Capítol 25 — LoRaWAN vs LoRa P2P: l'arbre de decisió

> *"Hi ha dues maneres de fer anar un missatge per ràdio: amb un director d'orquestra (LoRaWAN) o tots sols (P2P). Les dues funcionen; només cal saber quan toca cada una."*

## 25.1 Per què hem de triar

Quan vam al capítol 23 ja vam avançar la conclusió: per a Hort Osona, la millor opció és **LoRaWAN**. Però abans d'invertir temps i diners en una direcció, val la pena entendre les dues opcions a fons, per què cadascuna és millor en el seu context, i quines implicacions pràctiques té cadascuna.

Aquest capítol és una **decisió informada**. Si ja tens clar que vols LoRaWAN, pots saltar al capítol 26. Si tens dubtes, o vols entendre les alternatives, llegeix-lo sencer.

## 25.2 Recapitulació: què és LoRa i què és LoRaWAN

Ho vam veure al capítol 23, però ho repassem per tenir-ho fresc:

- **LoRa**: tecnologia de **modulació de ràdio** (PHY). Defineix com es modula el senyal a nivell físic. És propietat de Semtech.
- **LoRaWAN**: protocol de **xarxa** (MAC + aplicació) definit per la LoRa Alliance. Defineix com s'organitzen les dades, com s'autentiquen els nodes, com es xifra la comunicació, etc.

Això és similar a la distinció entre **Wi-Fi** (PHY) i **TCP/IP** (xarxa). Tots dos poden existir separadament, però combinats formen una xarxa completa.

## 25.3 LoRaWAN: l'opció "amb infraestructura"

### Com funciona

Un node LoRaWAN no parla directament amb el gateway. Emet a l'aire, i qualsevol gateway que senti el senyal redirigeix el paquet al **network server**. El network server autentica el node, desxifra el missatge, i l'envia a l'**application server** (que pot ser TTN, ChirpStack, o un altre).

```
[NODES]  --LoRa-->  [GATEWAY]  --Internet-->  [NETWORK SERVER]  --API/MQTT-->  [APP SERVER]
   ↑                                                                          ↓
   └───────────────────── resposta (downlink) ─────────────────────────────┘
```

Quan volem enviar una ordre al node (per exemple, "obre la vàlvula de reg"), el flow és invers: app server → network server → gateway → node.

### Avantatges

1. **Estàndard obert mantingut per una aliança industrial**. Compatibilitat entre fabricants, eines comunes, bona documentació.
2. **Network server gratuït o de baix cost**. TTN (The Things Stack) és gratuït per a ús no comercial. ChirpStack és open source i el podem autoallotjar.
3. **Escalabilitat**. Podem afegir tants nodes com vulguem, gestionats tots des d'una consola web.
4. **Seguretat integrada**. Xifratge AES-128, autenticació per DevEUI/AppKey, desduplicació, anti-replay.
5. **ADR automàtic**. El network server ajusta els paràmetres per optimitzar cada node.
6. **Downlink**. Podem enviar missatges al node (encara que amb limitacions de duty cycle).
7. **Mobilitat**. Si un node es mou d'un gateway a un altre, el network server redirigeix automàticament (roaming).
8. **Comunitat gran**. Milers de tutorials, fòrums, exemples de codi.
9. **Integracions fàcils**. TTN té integracions natives amb MQTT, webhooks, IFTTT, AWS, Azure, etc.

### Inconvenients

1. **Compleixitat inicial**. Cal entendre DevEUI, AppEUI, AppKey, OTAA vs ABP, classes A/B/C, ADR, etc. La corba d'aprenentatge no és negligible.
2. **Dependència d'un network server**. Si TTN cau o canvia les seves polítiques, ens quedem penjats (menys problema amb ChirpStack autoallotjat).
3. **Limits de volum a TTN**. Per a ús gratuït, hi ha un límit de missatges per dia (uns 500-1000, segons la regió).
4. **Duty cycle europeu**. Només podem transmetre l'1% del temps a la majoria de sub-bandes, cosa que limita la freqüència d'actualitzacions.
5. **Cost del gateway**. Si no n'hi ha cap comunitari a prop, hem de comprar o muntar un gateway propi (50-300 €).

## 25.4 LoRa P2P: l'opció "sense infraestructura"

### Com funciona

Dos mòduls SX1262 (o compatibles) es comuniquen directament entre ells, sense gateway, sense network server. Nosaltres definim tot: la freqüència, el SF, el payload, l'estructura del missatge, si hi ha ACK o no, etc.

```
[NODES]  --LoRa-->  [RX/TX mòdul]  --cable/serial-->  [Raspberry]
```

En aquest cas, la Raspberry (o un PC) té un mòdul SX1262 connectat per **SPI** o **USB** (amb un adaptador), i un script Python o C++ escolta els missatges rebuts.

### Avantatges

1. **Simplicitat**. No cal configurar DevEUI, AppEUI, AppKey, ni entendre les classes de LoRaWAN. Tu tries el format del payload.
2. **Sense dependència de tercers**. Tot és nostre, no hi ha network server extern.
3. **Sense limits de volum**. Podem transmetre tan sovint com el duty cycle ens permeti.
4. **Cost inicial més baix**. Només cal el node i un mòdul SX1262 a la Raspberry. No cal gateway separat.
5. **Aprenentatge**. Codi obert, podem entendre exactament què passa.

### Inconvenients

1. **Sense estandardització**. Cada projecte fa el seu propi protocol, la qual cosa significa més feina de manteniment.
2. **Sense seguretat per defecte**. Si volem xifrar, l'hem d'implementar nosaltres.
3. **Sense escalabilitat**. Si volem afegir un segon node, hem de modificar el codi del receptor. Si volem un tercer, igual. Per a més de 2-3 nodes, el P2P esdevé caòtic.
4. **Sense roaming**. Si un node canvia de posició, ens podem perdre.
5. **Sense ADR**. Hem de configurar manualment els paràmetres de cada node.
6. **Sense downlink estandarditzat**. Podem implementar ACK manualment, però no és tan net com el downlink de LoRaWAN.
7. **Compatibilitat limitada**. Si volem afegir una cosa comercial (un sensor de tercers que parli LoRaWAN), no es comunicarà amb el nostre P2P.

## 25.5 Quin model per a Hort Osona

L'arbre de decisió complet:

```
Comença
│
├── Tens previst tenir més d'un node al camp?
│   ├── Sí → LoRaWAN (amb TTN o ChirpStack)
│   └── No (un sol node)
│       │
│       ├── Vols afegir nodes en el futur?
│       │   ├── Sí → LoRaWAN
│       │   └── No
│       │       │
│       │       ├── T'agrada la idea d'un estàndard obert?
│       │       │   ├── Sí → LoRaWAN igualment
│       │       │   └── No → P2P
│       │       │
│       │       └── T'agrada tenir el control total?
│       │           ├── Sí → P2P
│       │           └── No → LoRaWAN
│   │
│   └── Sí (ja tenim 1, vindran més) → LoRaWAN
```

Per a Hort Osona, la resposta és clara: **LoRaWAN**. Tenim previst diversos nodes, voldrem afegir-ne més en el futur, i la integració amb la resta del BernatLab (via MQTT) és natural.

## 25.6 Quan el P2P és millor

Dit això, el P2P té el seu espai. Algunes situacions on és millor:

- **Projectes puntuals d'un sol node**: per exemple, un sensor de pluja aïllat que només volem monitorar, sense la complexitat de TTN.
- **Educació i aprenentatge**: per entendre LoRa a fons, res millor que un P2P on veiem exactament què passa.
- **Xarxes molt privades**: si volem una xarxa totalment aïllada, sense cap servidor extern, P2P és l'única opció.
- **Hackatges ràpids**: per a un prototip d'un dia, és més ràpid fer P2P que configurar LoRaWAN.

## 25.7 LoRaWAN: la pila de protocols completa

Quan parlem de LoRaWAN, tenim quatre capes:

1. **Capa física (PHY)**: la modulació LoRa (Semtech).
2. **Capa MAC**: el protocol LoRaWAN (LoRa Alliance).
3. **Capa de xarxa**: el network server (TTN, ChirpStack, Loriot).
4. **Capa d'aplicació**: el application server (pot ser el mateix network server, o un servei extern).

A més, hi ha components opcionals:

- **Servidor de join**: gestiona l'autenticació inicial dels nodes.
- **Servidor de dispositius**: emmagatzema l'estat i les claus de cada node.
- **Servidor d'aplicació**: processa les dades de cada aplicació.

TTN integra tot això en una sola consola. ChirpStack els separa en serveis independents, més modular però més complex.

## 25.8 El paper de cada peça

### Node (End Device)

El node és el sensor. Té un microcontrolador (ESP32, Pico, etc.) i un mòdul ràdio LoRa (SX1262, SX1276, etc.). Executa la pila LoRaWAN (LMIC, per exemple), gestiona les claus, i transmet.

### Gateway

El gateway és el "traductor" entre el món LoRa (ràdio) i el món IP (Internet). Té un mòdul concentrador (SX1302 o SX1303, no pas SX1262 — el SX1302 pot rebre 8 canals simultànis) i una connexió a Internet. La seva feina és: escoltar totes les freqüències a 868 MHz, detectar transmissions LoRa, i enviar-les al network server.

Quan un gateway rep un missatge, l'envia al network server amb la informació de:
- Freqüència, SF, BW del senyal rebut.
- RSSI, SNR.
- Timestamp (per calcular temps de vol i triangular).
- Payload xifrat (el gateway no el pot desxifrar; només el redirigeix).

### Network Server

El network server és el cervell. Funcions:

- Autenticar cada node (verificant DevEUI, AppKey).
- Desxifrar el payload (usant les claus de sessió derivades).
- Desduplicar missatges que arriben de múltiples gateways.
- Gestionar l'ADR.
- Encaminar el payload a l'application server correcte.
- Gestionar downlinks (respostes del node).

### Application Server

L'application server és on aterren les dades ja desxifrades. Pot ser:

- La mateixa consola web de TTN (amb UI per visualitzar).
- Un servei MQTT (TTN publica els payloads a un broker MQTT, i nosaltres ens hi connectem).
- Un webhook HTTP (TTN fa una petició POST a una URL nostra).
- Un servei d'integració (AWS IoT, Azure IoT Hub, etc.).

Al BernatLab, farem servir **integració MQTT**: TTN publicarà cada missatge rebut a un broker MQTT, i la resta de la cadena (Telegraf, InfluxDB, Node-RED, Grafana) consumirà des d'allà.

## 25.9 Com triar el hardware

### Per al gateway

Tres opcions principals:

1. **Waveshare SX1302 LoRaWAN Gateway HAT** (~50-80 €): un mòdul HAT per a Raspberry Pi, amb el chip SX1302. És la opció més comuna per a homelabs. Muntura fàcilment, bona documentació.

2. **RAK2287** (~70-100 €): un mòdul USB o mini-PCIe, basat en SX1302. Compatible amb moltes plaques (Raspberry, NUC, etc.).

3. **Dragino LPS8** (~200-300 €): un gateway comercial complet, amb caixa, PoE, antena externa. Més robust però més car.

4. **Construir amb un SX1302 + Raspberry Pi**: opció DIY, requereix soldar i configurar, però la més barata.

Per a Hort Osona, recomano la **opció 1 (Waveshare SX1302 HAT)** per la relació preu/facilitat.

### Per als nodes

Tres famílies principals:

1. **ESP32 + SX1262 breakout**: màxima flexibilitat, però cal muntar a protoboard o PCB.
2. **Heltec LoRa 32 V3**: ESP32 + SX1262 integrats, amb pantalla OLED, antena, bateria. Molt còmode per a prototips. (~25 €)
3. **TTGO LoRa**: similar a Heltec, una mica més cara però bona qualitat. (~30 €)
4. **RAK3172**: només el mòdul (no placa de desenvolupament), pensat per a productes comercials. (~15 €)
5. **LILYGO T-Beam**: ESP32 + SX1262 + GPS. Per a nodes mòbils o geolocalització. (~40 €)

Per a Hort Osona, recomano la **Heltec LoRa 32 V3** per començar: tot integrat, fàcil de programar, bona documentació, i barata.

## 25.10 Programari: el que instal·larem

A la Raspberry (gateway):

- **Concentratord** (programari de gateway, abans lora-packet-forwarder).
- **Packet forwarder** (processat de paquets, configurable).

A l'ordinador o Raspberry (recepció):

- **Mosquitto** (broker MQTT, ja instal·lat al M2).
- **Telegraf** (recol·lector, ja instal·lat al M2).
- **InfluxDB** (base de dades, ja instal·lat al M2).
- **Node-RED** (processament, ja instal·lat al M2).
- **Grafana** (visualització, ja instal·lat al M2).

Al node:

- **Arduino** + **MCCI LoRaWAN LMIC** o **RadioLib**.
- O **MicroPython** + **RadioLib** o una implementació específica.

Al network server (TTN, allotjat al núvol):

- Consola web de TTN.
- Integració MQTT.

## 25.11 Estimació de cost total

Per a un node LoRaWAN + gateway a Hort Osona, amb 1 node inicial i 1 gateway propi:

| Component | Preu (EUR) | Notes |
|---|---|---|
| Raspberry Pi 4 (4GB) | 60 | Ja la tenim. |
| Waveshare SX1302 HAT | 70 | Gateway LoRaWAN. |
| Antena 868 MHz (gateway) | 15 | Externa, amb cable. |
| Heltec LoRa 32 V3 | 25 | Node. |
| Antena 868 MHz (node) | 5 | Sol soldar a la Heltec. |
| Sensor BME280 | 5 | T, H, P. |
| Placa solar + bateria | 25 | Per a ús autònom. |
| Caixa estanca | 10 | Per a ús exterior. |
| Cables, connector, etc. | 10 | |
| **Total** | **~225 €** | Per a 1 node + 1 gateway. |

Per afegir nodes addicionals: ~50-60 € per node (Heltec + antena + sensor).

## 25.12 Resum

En aquest capítol hem vist les dues grans topologies per a xarxes LoRa: **LoRaWAN** (amb gateway i network server) i **LoRa P2P** (directe entre dos mòduls). Hem après els avantatges i inconvenients de cada una, hem decidit que per a Hort Osona la millor opció és **LoRaWAN amb TTN i un gateway propi** a la Raspberry, hem vist quin hardware cal, i hem estimat el cost. En el proper capítol ens endinsarem a la capa LoRaWAN: TTN, device profiles, formats de payload, i decoders.

## 25.13 Exercicis pràctics

1. Crea un compte a The Things Network: https://console.thingsnetwork.org/
2. Crea una aplicació nova a la consola de TTN. Dona-li un nom identificatiu (per exemple, `hort-osona-bernat`).
3. Afegeix un dispositiu de prova a l'aplicació. Anota el DevEUI, AppEUI, i AppKey generats.
4. Mira la documentació de TTN sobre data formats: https://www.thoughts.com/en/docs/concepts/data-formats/
5. Comprova quin data rate (DR0-DR5) t'ofereix TTN a la teva regió.
6. Fes una taula amb el cost total estimat del teu projecte LoRa, segons els components que vulguis comprar.
7. Documenta al README del projecte quina decisió has pres: LoRaWAN, P2P, o un híbrid.

Paraules clau: **LoRaWAN, LoRa, P2P, gateway, network server, application server, TTN, The Things Stack, ChirpStack, DevEUI, AppEUI, AppKey, OTAA, ABP, classe A, classe B, classe C, ADR, downlink, uplink, payload, decoder, codec, CayenneLPP, JSON, MQTT, Telegraf, InfluxDB, Node-RED, Grafana, Concentratord, packet forwarder, SX1302, SX1303, SX1262, ESP32, Heltec, TTGO, RAK, Waveshare, hardware, cost, comparativa, avantatges, inconvenients, decisió, node, end device, EU868, EU433, US915, 868 MHz, 915 MHz, ISM, duty cycle, ETSI, normativa, LoRa Alliance, Semtech, codi obert, integració, broker, application server, ChirpStack Gateway Bridge, MQTT broker, broker extern, broker intern, seguretat, AES-128, xifratge, autenticació, roaming, ADR, spreading factor, SF, BW, RSSI, SNR, packet loss, link budget, EUI-64, EUI-48, IEEE 802.15.4g, EU868, EU433, US915, AS923, AU915, CN470, KR920, IN865, regions, ISM band, regional parameters, Lora Alliance, regional parameters document, TTN v3, TTN v2, TTS, The Things Stack, LNS, JOIN, OTAA, ABP, session keys, NwkSKey, AppSKey, join procedure, join request, join accept, join server, device address, DevAddr, frame counter, FCnt, FCntUp, FCntDown, FPort, FRMPayload, MAC header, MHDR, Join-Request, Join-Accept, unconfirmed data up, confirmed data up, RX1, RX2, receive windows, transmission timing, hop limit, ADR bit, ADRACKReq, ADRACKCnt, LinkADRReq, LinkADRAns, DutyCycleReq, DutyCycleAns, RXParamSetupReq, RXParamSetupAns, DevStatusReq, DevStatusAns, NewChannelReq, NewChannelAns, RXTimingSetupReq, RXTimingSetupAns, class A, class B, class C, MAC commands, fopts, FOptsLen, payload size, maximum payload size, dwell time, dwell time limitation, EU868 dwell time, 868 MHz dwell time, 400 ms dwell time, 868.0 MHz, 868.6 MHz, 868.7 MHz, 869.2 MHz, 869.4 MHz, 869.65 MHz, ETSI EN 300 220, ERC Recommendation 70-03, duty cycle, 1% duty cycle, 0.1% duty cycle, 10% duty cycle, listen before talk, LBT, polite spectrum access, polite LoRa, polite LoRaWAN, polite protocol, polite stack, polite access**.
