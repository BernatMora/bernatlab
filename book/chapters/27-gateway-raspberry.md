# Capítol 27 — Gateway LoRaWAN a la Raspberry amb Concentratord

> *"Un gateway LoRaWAN és com una torre de telefonia, però minúscula: 50 grams, 50 euros, i pot cobrir quilòmetres. La diferència és que el muntes tu."*

## 27.1 Què és un gateway LoRaWAN

Un **gateway** LoRaWAN és un dispositiu que escolta les transmissions LoRa a 868 MHz i les redirigeix al network server (com The Things Stack) per Internet. A diferència d'un node (que és un sensor amb poca potència), un gateway ha de ser capaç de rebre **molts canals simultàniament** i durant **tot el temps**.

Per fer-ho, els gateways moderns usen un xip **concentrador** que pot rebre 8 o més canals alhora. El més popular actualment és el **SX1302** (o el seu successor, el **SX1303**), de Semtech. Aquest xip no és un transmissor LoRa normal (com el SX1262); és un processador de senyals dedicat que pot rebre transmissions de múltiples nodes alhora.

El gateway típic té:

- Un **mòdul concentrador** (SX1302).
- Un **microcontrolador** o **ordinador** que gestiona el mòdul i la connexió a Internet.
- Una **antena externa** (per a bon abast).
- Un **programari** (packet forwarder) que envia els paquets rebuts al network server.

## 27.2 Tipus de gateways

Hi ha diverses maneres de tenir un gateway LoRaWAN:

### Gateways comercials

Aparells complets, amb caixa, antena, i software preinstal·lat:

- **Dragino LPS8**: molt popular, robust, amb PoE. ~200-300 €.
- **RAK7268 / RAK7258**: bons, amb Wi-Fi i 4G. ~250-350 €.
- **MikroTik LoRa**: barat però limitat. ~100 €.

### DIY amb Raspberry Pi + mòdul SX1302

La opció més comuna per a homelabs. Es compon de:

- Una **Raspberry Pi** (que ja tenim al BernatLab).
- Un **mòdul SX1302** connectat per **SPI** o **USB**.
- **Software**: Concentratord (o altres com ChirpStack Gateway Bridge).

Aquesta opció és la que veurem en detall, perquè és la que farem servir al BernatLab.

### Gateways virtuals

En alguns casos, podem usar un gateway d'un altre (per exemple, un gateway TTN comunitari) sense tenir-ne un de propi. Això és el que passa si hi ha cobertura TTN a menys de 5-10 km amb visió directa.

## 27.3 Hardware: el mòdul SX1302

Hi ha diversos mòduls al mercat:

1. **Waveshare SX1302 LoRaWAN Gateway HAT**: la opció més popular. Es connecta directament als pins GPIO de la Raspberry Pi. ~70 €.

2. **RAK2287**: mòdul mini-PCIe amb SX1302. Es connecta a una placa base com la RAK2287 PCIe. ~80-100 €.

3. **Seeed Studio WM1302**: mòdul mini-PCIe similar al RAK. ~70 €.

4. **SX1302 + Raspberry directament**: mòdul sol + cable, per als més agoserats. ~50 €.

Al BernatLab, recomanem el **Waveshare SX1302 HAT** per la facilitat d'instal·lació. Només cal encaixar-lo als pins GPIO de la Raspberry, sense cables, sense soldar.

### Característiques del SX1302

- **8 canals de recepció simultània** (pot rebre transmissions de fins a 8 nodes alhora).
- **SF7-SF12** suportat.
- **125 / 250 / 500 kHz** de BW.
- **868 / 915 / 923 MHz** (multibanda).
- **Connexió SPI** (a través dels pins GPIO de la Raspberry).
- **Consum**: ~1-2 W en recepció.

## 27.4 Antena

L'antena és **tan important com el mòdul**. Una mala antena pot reduir l'abast a la meitat o més.

Per a 868 MHz, opcions:

- **Antena de rubber ducky** (petita, omnidireccional, ~5 dBi): bona per a provar.
- **Antena de fibra de vidre** (més llarga, ~5-8 dBi): millor rendiment, bona per a exteriors.
- **Antena direccional Yagi** (~8-12 dBi): molt abast en una direcció concreta, útil si el node està en una posició fixa.

A 868 MHz, una antena de 1/4 d'ona fa ~8.6 cm. Una de 1/2 d'ona, ~17 cm. Una de 5/8 d'ona, ~35 cm.

Al BernatLab, recomanem una **antena de fibra de vidre omnidireccional** per a ús general. Si tenim una posició fixa del node, podem considerar una Yagi per augmentar l'abast.

### Cable i connectors

El SX1302 HAT de Waveshare porta un **connector U.FL** (IPEX) a la placa. Per connectar una antena externa, cal un **pigtail U.FL a SMA** (un cable petit d'uns 10-15 cm). Un extrem va al HAT, l'altre a l'antena.

Compte amb els cables massa llargs: a 868 MHz, cada metre de cable perd ~0.5-1 dB. Mantenim el cable el més curt possible.

## 27.5 Software: Concentratord

**Concentratord** (abans conegut com a **lora-packet-forwarder**) és el programari estàndard per a gateways basats en SX1302. Està desenvolupat per xdegaye (Benjamin}) i mantingut activament.

Hi ha dues variants:

- **Concentratord**: la nova versió, refeta des de zero, modular.
- **lora-packet-forwarder**: la versió clàssica, encara funcional però menys activa.

Recomanem **Concentratord** per a noves instal·lacions.

### Altres opcions de programari

- **ChirpStack Gateway Bridge**: si volem integrar el gateway amb un ChirpStack autoallotjat.
- **TTN Packet Forwarder**: oficial de TTN, però menys flexible.

## 27.6 Instal·lació de Concentratord a la Raspberry

Al BernatLab, la Raspberry ja té Docker. Podem executar Concentratord com un contenidor, o com a servei natiu. Recomanem el **contenidor Docker** per la facilitat de gestió.

### Opció 1: Contenidor Docker (recomanada)

Al `docker-compose.yml` del BernatLab, afegim un servei:

```yaml
services:
  concentratord:
    image: chirpstack/chirpstack-concentratord:2
    container_name: concentratord
    restart: unless-stopped
    devices:
      - /dev/spidev0.0:/dev/spidev0.0
    volumes:
      - ./concentratord:/etc/chirpstack-concentratord
    ports:
      - "3001:3001"
```

Això munta el dispositiu SPI de la Raspberry al contenidor (perquè pugui parlar amb el SX1302) i munta una carpeta amb la configuració.

### Opció 2: Instal·lació nativa

```bash
# Afegir el repositori
sudo apt install -y software-properties-common
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 1FF3F2DB 
sudo add-apt-repository ppa:chirpstack/chirpstack-gateway
sudo apt update
sudo apt install chirpstack-concentratord
```

## 27.7 Configuració de Concentratord

El fitxer principal és `chirpstack-concentratord.toml`. A `/home/bernat/homelab/concentratord/`:

```toml
# Configuració del gateway
[gateway]
  # Identificador únic del gateway (EUI-64)
  gateway_id = "AA555A0000000001"

  # Servidor TTN
  server_address = "eu1.cloud.thethings.network:1700"

  # Interval en què enviem estadístiques
  statistics_interval = "30s"

  # Ubicació del gateway (per a TTN)
  latitude = 41.9304
  longitude = 2.2546
  altitude = 500

# Configuració del concentrador
[concentrator]
  # El SX1302 es comunica amb la Raspberry per SPI
  spi_path = "/dev/spidev0.0"
  spi_speed_hz = 2000000
```

### Gateway ID: el EUI-64

Cada gateway ha de tenir un **EUI-64 únic**. Podem generar-lo:

```bash
echo "AA555A$(openssl rand -hex 5 | tr a-f A-F | cut -c 1-10)"
```

O simplement fem servir un valor vàlid que no coincideixi amb cap altre gateway de TTN. El prefix `AA555A` és un prefix reservat per a gateways experimentals.

### Configurar el servidor TTN

El `server_address` ha de ser l'endpoint de TTN. Per a la UE, és `eu1.cloud.thethings.network:1700`. Per a altres regions, TTN té altres servidors (nam1.cloud.thethings.network, au1.cloud.thethings.network, etc.).

## 27.8 Registrar el gateway a TTN

Un cop tenim el gateway funcionant, cal registrar-lo a TTN:

1. A la consola de TTN, anem a la secció **Gateways**.
2. Clic a **+ Register gateway**.
3. **Gateway EUI**: introduïm el EUI-64 que hem configurat a `chirpstack-concentratord.toml`.
4. **Gateway ID**: un nom únic (per exemple, `raspi-hortosona-gw`).
5. **Gateway name**: un nom descriptiu.
6. **Frequency plan**: `Europe 868 MHz` (o el que correspongui).
7. **Router**: el que ens suggereixi TTN (no importa gaire per a un homelab).
8. **Desem**.

TTN ens donarà un **Gateway Server Address** (que hem de posar al `server_address` de la nostra configuració) i una clau d'autenticació. A Concentratord 2.x, l'autenticació és per **API key** o per **TLS client certificates**, configurable al `chirpstack-concentratord.toml`.

### Exemple de configuració amb API key

```toml
[gateway]
  gateway_id = "AA555A0000000001"
  server_address = "eu1.cloud.thethings.network:1700"

  [gateway.auth]
    api_key = "NNSXS.XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX..."
```

## 27.9 Verificar la connexió

Un cop en marxa, podem comprovar:

1. **A la consola de TTN**, a la pàgina del gateway, veure l'estat. Si apareix "Connected" o "Last seen: recent", tot va bé.
2. **Els logs del contenidor**:

```bash
docker compose logs -f concentratord
```

3. **L'estat del SX1302** amb la comanda `chirpstack-concentratord-ctl`:

```bash
docker exec concentratord chirpstack-concentratord-ctl gateway status
```

## 27.10 Proves amb un node

Per validar que el gateway funciona, podem fer servir un node comercial o un prototip:

1. **Configurar un node** (per exemple, una Heltec LoRa 32 V3) amb el nostre DevEUI i AppEUI.
2. **Programar-lo** per transmetre cada 30 segons.
3. **Mirar la consola de TTN**: a la secció "Live data" o a la pàgina del node, hauríem de veure els uplink.

Si veiem els uplink, tenim:
- Gateway LoRaWAN funcionant.
- Concentratord connectat a TTN.
- Node transmettent correctament.
- Xarxa TTN rebent i desxifrant.

Si NO veiem res, caldrà depurar. Aquest és el tema del capítol 32.

## 27.11 Configuració avançada

### Múltiples concentradors (no típic)

Si volem tenir dos SX1302 a la mateixa Raspberry (per diversitat d'antena, per exemple), cal configurar dos serveis `concentratord` amb pins SPI diferents.

### Múltiples xarxes (TTN + ChirpStack)

Concentratord 2.x pot enviar els mateixos uplink a múltiples network servers. Cal afegir múltiples seccions `[gateway]` o usar la funció de "multi-server".

### Filtratge de canals

Podem configurar quins canals de 868 MHz volem rebre. Per defecte, els 8 canals principals estan actius. Podem desactivar-ne alguns per reduir la càrrega de la CPU.

### GPS del gateway

Si la Raspberry té un mòdul GPS connectat, podem passar la posició exacta a TTN. Això millora la cobertura i permet triangular.

## 27.12 Monitoratge del gateway

Com monitorem el gateway?

### Uptime Kuma

Afegim un monitor al port 3001 (el port per defecte de la interfície de debug de Concentratord):

- **Tipus**: HTTP(s).
- **URL**: `http://100.115.134.76:3001/`.
- **Interval**: 60 segons.

Alternativament, podem monitorar si el procés està viu:

```bash
docker ps | grep concentratord
```

### Logs a Uptime Kuma

Si volem centralitzar els logs, podem muntar un volum compartit i configurar logrotate. Però això és opcional per a un homelab.

### Estadístiques a TTN

TTN ensenya estadístiques del gateway: nombre d'uplinks rebuts, RSSI mitjà, SNR mitjà, taxa d'error. Això és molt útil per diagnosticar.

## 27.13 Consum d'energia i alimentació

El SX1302 HAT consumeix ~1-2 W. La Raspberry Pi 4 consumeix ~3-7 W segons la càrrega. Total, ~5-9 W.

Per a ús 24/7, podem:

- Usar l'alimentador oficial de la Raspberry (5.1V, 3A).
- Considerar PoE (Power over Ethernet) si tenim un switch compatible.
- Considerar una font UPS per a talls de llum.

A llarg termini, una UPS petita (per exemple, un PowerBank amb pass-through) pot evitar reinicis innecessaris.

## 27.14 Posició del gateway

La **posició** del gateway és crítica. Un gateway ben col·locat pot cobrir 5-10 km; un mal col·locat, 100 metres.

Criteris:

- **Alçada**: com més amunt, millor. Teulada, torre, arbre alt.
- **Visió directa**: sense arbres, edificis, o muntanyes al mig.
- **L'allunyament de metalls**: estructures metàl·liques reflecteixen el senyal.
- **L'allunyament d'altres antenes**: per evitar interferències.
- **Accés a corrent elèctric i xarxa**: evidentment.

A Hort Osona, el millor lloc per al gateway seria la teulada de la casa, amb l'antena sobresortint. Si no és possible, una finestra alta o un balcó pot servir.

## 27.15 Resum

En aquest capítol hem vist com muntar un gateway LoRaWAN a la Raspberry amb un mòdul SX1302 (recomanem el Waveshare HAT) i el programari Concentratord. Hem après a configurar-lo, registrar-lo a TTN, i verificar la connexió. Hem vist com monitorar-lo amb Uptime Kuma i com col·locar-lo correctament. En el proper capítol veurem el hardware del node: ESP32 + SX1262, esquema elèctric, antena, i alimentació.

## 27.16 Exercicis pràctics

1. Compra o demana un mòdul SX1302 HAT (Waveshare, RAK2287, o similar).
2. Connecta'l a la Raspberry Pi 4 (apaga la Raspberry, encén el HAT als pins GPIO, torna a encendre).
3. Desplega Concentratord amb Docker a la Raspberry.
4. Configura `chirpstack-concentratord.toml` amb un EUI-64 únic.
5. Registra el gateway a TTN amb el EUI-64.
6. Comprova l'estat a la consola de TTN.
7. Configura un monitor d'Uptime Kuma per al gateway.
8. Documenta al README del projecte l'estructura del gateway, l'EUI-64, i la configuració.

Comandes útils:

```bash
# Verificar que el SX1302 és detectat
ls -la /dev/spidev*

# Veure els logs de Concentratord
docker compose logs -f concentratord

# Verificar l'estat del concentrador
docker exec concentratord chirpstack-concentratord-ctl gateway status

# Monitorar el tràfic
docker exec concentratord chirpstack-concentratord-ctl gateway config
```

Paraules clau: **gateway, concentratord, SX1302, SX1303, HAT, Waveshare, RAK2287, Seeed, RAK, Mini-PCIe, GPIO, SPI, spidev, packet forwarder, U.FL, IPEX, SMA, pigtail, antena, 868 MHz, omnidireccional, direccional, Yagi, fibbra de vidre, dBi, gateway EUI, gateway ID, EUI-64, TTN, EU1.cloud.thethings.network, NAM1, AU1, router, autenticació, API key, TLS, certificat, server address, last seen, connected, last seen, live data, uplink, downlink, RSSI, SNR, posicionament, latitud, longitud, altitud, location, monitoratge, Uptime Kuma, Docker, contenidor, ChirpStack Gateway Bridge, lora-packet-forwarder, multi-server, filtratge de canals, GPS, PoE, UPS, alimentació, posicionament del gateway, visió directa, cobertura, abast, distancia, alçada, interferències, reflexió, soroll, RSSI mitjà, SNR mitjà, taxa d'error, gateway status, gateway config, chirpstack-concentratord-ctl, SPI speed, 2 MHz, 8 MHz, EU868, 868 MHz, 868.1, 868.3, 868.5, 867.1, 867.3, 867.5, 867.7, 867.9**.
