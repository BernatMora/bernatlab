# Capítol 26 — La capa LoRaWAN: TTN, device profiles, payloads

> *"LoRaWAN és com parlar una llengua: tens un vocabulari, una gramàtica, i unes normes de cortesia. Un cop les domines, parlar amb un node és natural."*

## 26.1 Què és The Things Network (TTN)

**The Things Network** (ara **The Things Stack**, TTS) és un **network server LoRaWAN comunitari i gratuït**, allotjat al núvol per la fundació The Things Network. Va començar el 2015 com un projecte de crowdsourcing per cobrir el món amb gateways comunitaris, i actualment té cobertura a centenars de països, inclosa una bona part de Catalunya i la resta d'Espanya.

La URL de la consola web és https://console.thingsnetwork.org/. Allà podrem:

- Crear **aplicacions** (agrupacions de dispositius).
- Registrar **dispositius** (nodes).
- Configurar **integracions** (MQTT, webhooks, etc.).
- Veure les **trames rebudes** en temps real.
- Monitorar la salut dels **gateways** propers.

TTN és la millor opció per començar amb LoRaWAN perquè:

- **És gratuït** per a ús no comercial, amb un volum raonable.
- **No requereix instal·lar cap servidor** propi.
- **Té una documentació excel·lent**.
- **Comunitat gran** amb milers de projectes, fòrums actius, tutorials.
- **Integracions fàcils** amb MQTT, webhooks, AWS, Azure, etc.

## 26.2 Crear un compte i una aplicació

El primer pas és crear un compte a la consola de TTN. Només cal un correu electrònic. Un cop registrats:

1. **Creem una aplicació** amb un nom identificatiu. Per a Hort Osona, jo faria servir `hort-osona-bernat`.
2. **Anotem l'Application ID** i l'**Application EUI** (un identificador únic generat per TTN).
3. **Accedim a la secció "Integrations"** per afegir la integració MQTT.

La consola web de TTN és intuïtiva. Si tens dubtes, la documentació oficial és a https://www.thoughts.com/en/docs/.

## 26.3 DevEUI, AppEUI, AppKey: els identificadors

Cada node LoRaWAN té **tres identificadors** principals:

- **DevEUI**: identificador únic del dispositiu, similar a una adreça MAC. 64 bits. Cada node ha de tenir-ne un d'únic.
- **AppEUI** (o **JoinEUI**): identificador de l'aplicació. 64 bits. Indica a quin "tenant" pertany el node.
- **AppKey**: clau mestra de 128 bits, usada per autenticar el node durant el procés de join.

A TTN, quan registrem un node, podem:

- **Generar automàticament** els identificadors (TTN ens els dona).
- **Introduir-los manualment** si el node ja ve amb identificadors preconfigurats (com passa amb molts mòduls comercials).

Els valors generats per TTN es mostren **una sola vegada**. Cal guardar-los en un lloc segur (per exemple, un fitxer `.env` o un document xifrat).

## 26.4 OTAA vs ABP: els dos mètodes d'unió

Quan un node vol connectar-se a la xarxa LoRaWAN, ho pot fer de dues maneres:

### OTAA (Over-The-Air Activation)

Aquest és el **mètode recomanat** i l'estàndard de facto. Funciona així:

1. El node envia un **Join Request** amb el seu DevEUI, AppEUI, i un nonce.
2. El network server valida la sol·licitud usant l'AppKey.
3. Si tot és correcte, el NS envia un **Join Accept** amb un DevAddr (adreça dinàmica) i les claus de sessió (NwkSKey, AppSKey).
4. A partir d'aquí, el node pot transmetre amb les claus de sessió.

Avantatges d'OTAA:
- Més segur: les claus de sessió es renegocien cada vegada.
- Permet el roaming: el node pot canviar de network server.
- Permet l'ADR: el NS pot ajustar els paràmetres.

### ABP (Activation By Personalization)

En aquest mètode, les claus de sessió (NwkSKey, AppSKey) i el DevAddr es configuren **directament al node**, sense cap handshake. El node ja està "unida" a la xarxa per sempre, amb aquestes claus fixes.

Inconvenients d'ABP:
- Si les claus es comprometen, cal reprogramar el node.
- No suporta roaming.
- No suporta ADR de manera nativa.

Recomanació: usa **OTAA sempre**, tret que tinguis un motiu específic per usar ABP.

## 26.5 Device profiles

TTN permet definir **device profiles** que descriuen les capacitats d'un tipus de dispositiu:

- Versió de LoRaWAN (1.0.2, 1.0.3, 1.0.4, 1.1).
- Versió de la Regional Parameters (RP001-1.0.3, etc.).
- Capacitat de l'ADR.
- Classes suportades (A, B, C).
- Màxima potència de transmissió.
- Fabrique i model.

Els device profiles ajuden a mantenir la consistència quan tenim molts dispositius similars. Per a Hort Osona, podem crear un device profile comú per a tots els nodes de sensors ambientals.

## 26.6 Payload formats: CayenneLPP i altres

Quan un node LoRaWAN transmet, el payload és una seqüència de bytes (típicament 5-50 bytes). Com interpretem aquests bytes?

Hi ha diversos estàndards i convencions:

### CayenneLPP (Cayenne Low Power Payload)

És el format més popular per a sensors LoRaWAN. Creat per myDevices, està pensat per ser molt eficient en bytes. Cada dada es codifica amb:

- 1 byte: tipus de dada (per exemple, 0x67 = temperatura).
- 1 byte: canal (per exemple, 0x01 = canal 1).
- N bytes: el valor (per exemple, 2 bytes per a un enter amb signe de 16 bits, o 4 bytes per a un float).

Exemples de canals CayenneLPP:

| Tipus | Valor | Bytes |
|---|---|---|
| 0x67 (Temperatura) | graus C × 10 (signed 16-bit) | 2 |
| 0x68 (Humitat) | % × 2 (unsigned 16-bit) | 2 |
| 0x69 (Acceleròmetre) | tres eixos (3 × signed 16-bit) | 6 |
| 0x6E (Il·luminació) | lux (unsigned 16-bit) | 2 |
| 0x75 (Humitat del sòl) | % (unsigned 8-bit) | 1 |
| 0x02 (Sortida analògica) | valor (float, 4 bytes) | 4 |
| 0x03 (Sortida analògica) | valor (float, 4 bytes) | 4 |

Exemple de payload CayenneLPP per a un sensor amb temperatura, humitat i lluminositat:

```
67 01 00 FF    # Temperatura al canal 1: 0x00FF = 255, /10 = 25.5°C
68 02 00 B6    # Humitat al canal 2: 0x00B6 = 182, /2 = 91%
6E 03 0B B8    # Lluminositat al canal 3: 0x0BB8 = 3000 lux
```

Total: 12 bytes. Molt eficient.

### JSON sobre LoRaWAN

Una altra opció és enviar JSON com a payload:

```json
{"t": 25.5, "h": 91, "l": 3000, "id": "n1", "v": 1}
```

Avantatges: llegible, fàcil de debugar.
Inconvenients: ocupa més bytes. Un missatge de 50 bytes amb JSON pot trigar molt més a transmetre que un CayenneLPP equivalent.

### Binari personalitzat

Si tenim moltes dades idèntiques, podem definir el nostre propi format binari. Per exemple, 2 bytes per a la temperatura, 1 byte per a la humitat, 2 bytes per al voltatge de la bateria. Total: 5 bytes per a tres dades. Molt eficient, però menys estàndard.

## 26.7 Payload formatters a TTN

TTN permet definir **payload formatters** que interpreten el payload del node:

- **Decoder**: converteix el payload binari en JSON per a l'aplicació.
- **Converter** (uplink): format JSON que TTN rep i publica.
- **Encoder** (downlink): converteix JSON en payload binari per enviar al node.

Exemple de decoder CayenneLPP en JavaScript:

```javascript
function decodeUplink(input) {
    var decoded = {};
    var i = 0;
    while (i < input.bytes.length) {
        var channel = input.bytes[i++];
        var type = input.bytes[i++];
        switch (type) {
            case 0x67:  // Temperatura
                var t = (input.bytes[i++] << 8) | input.bytes[i++];
                if (t > 0x7FFF) t -= 0x10000;
                decoded.temperatura = t / 10.0;
                break;
            case 0x68:  // Humitat
                var h = (input.bytes[i++] << 8) | input.bytes[i++];
                decoded.humitat = h / 2.0;
                break;
            // Afegir altres tipus segons calgui
        }
    }
    return {
        data: decoded,
        warnings: [],
        errors: []
    };
}
```

Aquest codi es pot enganxar directament a la consola de TTN, secció "Payload formatters" del dispositiu.

## 26.8 Integració amb el broker MQTT

La integració clau per al BernatLab és **MQTT**. TTN ens permet configurar una integració MQTT on cada vegada que un node transmet, el payload desxifrat (en JSON) es publica a un broker MQTT.

A TTN, a la secció "Integrations":

1. **Triem "MQTT"**.
2. **Configurem el broker**:
   - **Broker Address**: `mqtt://100.x.y.z:1883` (la Tailscale IP del BernatLab).
   - **Username**: `ttn-bridge` (o el que hàgim creat a Mosquitto).
   - **Password**: la contrasenya.
3. **Triem el topic prefix** (per defecte, `v3/{application_id}@{tenant_id}/devices/{device_id}/`).
4. **Desem**.

Un cop configurat, cada vegada que un node transmet, TTN publicarà un missatge JSON al broker MQTT. Aquest missatge el pot consumir Telegraf (per guardar-lo a InfluxDB) o Node-RED (per processar-lo).

### Format del missatge MQTT

El missatge que TTN publica té aquesta estructura:

```json
{
  "end_device_ids": {
    "device_id": "eui-70b3d57ed004f1ce",
    "application_ids": {
      "application_id": "hort-osona-bernat"
    },
    "dev_eui": "70B3D57ED004F1CE",
    "join_eui": "0000000000000000"
  },
  "received_at": "2026-07-08T12:34:56Z",
  "uplink_message": {
    "f_port": 2,
    "f_cnt": 42,
    "frm_payload": "GAEABbYBmAu4",
    "decoded_payload": {
      "temperatura": 25.5,
      "humitat": 91,
      "lux": 3000
    },
    "rx_metadata": [{
      "gateway_ids": {
        "gateway_id": "raspi-gw-1"
      },
      "rssi": -67,
      "snr": 9.5,
      "channel_rssi": -67,
      "channel_index": 5
    }],
    "settings": {
      "data_rate": {
        "lora": {
          "bandwidth": 125000,
          "spreading_factor": 9
        }
      },
      "frequency": "868100000"
    }
  }
}
```

Com veieu, el payload decodificat ja ve en JSON, juntament amb metadades útils: RSSI, SNR, data rate, etc.

### Topics MQTT

Per defecte, TTN publica a:

```
v3/{application_id}@{tenant_id}/devices/{device_id}/up
```

on `up` indica que és un missatge uplinki (del node al servidor). Els altres tipus de missatge són:

- `up`: uplink del node.
- `down`: downlink (resposta del servidor al node).
- `join`: peticions de join (OTAA).
- `ack`: confirmacions.
- `error`: errors.

## 26.9 Downlink: enviar comandes al node

A més de rebre dades dels nodes, podem **enviar ordres** (downlinks). Això és útil per:

- Canviar la configuració d'un node a distància.
- Activar un actuador (per exemple, obrir una vàlvula de reg).
- Fer un "ping" per comprovar si el node està viu.

Limitacions del downlink:

- **Només a classe A**: el node només pot rebre durant les finestres RX1 i RX2, just després d'haver transmès.
- **Duty cycle igual**: cada downlink compta contra el duty cycle.
- **FPort**: el downlink s'envia en un port concret (1-223).

A TTN, podem programar un downlink des de la consola web, o via API, o escoltant un topic MQTT específic.

## 26.10 Classes de dispositius

LoRaWAN defineix tres classes:

- **Classe A**: el node pot rebre **només immediatament** després d'haver transmès. La majoria de sensors són classe A per estalviar energia.
- **Classe B**: el node pot rebre en finestres programades (pings del network server). Sincronitza amb el NS periòdicament.
- **Classe C**: el node pot rebre **continuament** (excepte quan està transmetent). Consumeix més energia, però permet downlinks immediats. Útil per a actuadors o nodes endollats.

Per a sensors amb piles, **classe A** és l'estàndard. La Heltec LoRa 32 V3 pot treballar en classe A o C.

## 26.11 Procediment de join: detall tècnic

Quan un node OTAA arrenca, segueix aquest procediment:

1. **Genera un nonce aleatori** (DevNonce).
2. **Construeix el Join Request** amb DevEUI, AppEUI, DevNonce.
3. **Xifra el Join Request** amb l'AppKey.
4. **Envia el Join Request** a un canal aleatori.
5. **Escolta el Join Accept** a RX1 (al cap de 1 segon ± 20 µs al canal de resposta) o RX2 (al cap de 2 segons al canal i data rate configurats).
6. Si rep el Join Accept, **deriva les claus de sessió** (NwkSKey, AppSKey) i el DevAddr.
7. A partir d'aquí, **pot transmetre dades normals** amb aquestes claus.

Si no rep el Join Accept, torna a provar amb un altre canal i un altre DevNonce. Després de N intents, espera més estona (backoff exponencial).

## 26.12 El paper de l'AppKey

L'AppKey és la clau mestra. Està emmagatzemada al node (en memòria no volàtil) i al network server (a la configuració del dispositiu). S'usa per:

- **Xifrar el Join Request** (per demostrar que el node és legítim).
- **Derivar les claus de sessió** durant el join.
- **No s'usa mai per xifrar les dades normals**: això ho fan les claus de sessió derivades.

Si l'AppKey es compromet, algú podria suplantar el node. Per tant, **cal guardar-la en lloc segur** (fitxer xifrat, gestors de secrets, etc.).

## 26.13 Configurar la integració MQTT a TTN

Pas a pas, en detall:

1. **Crear un usuari MQTT a Mosquitto**:

```bash
docker exec -it mosquitto mosquitto_passwd -c /mosquitto/config/passwordfile ttn-bridge
```

(Per afegir a un fitxer existent, sense `-c`).

2. **Configurar les ACLs** per a l'usuari `ttn-bridge`:

```
user ttn-bridge
topic write v3/+/@/devices/+/up
topic write v3/+/@/devices/+/join
topic write v3/+/@/devices/+/down
topic write v3/+/@/devices/+/ack
topic read v3/+/@/devices/+/down
```

3. **A la consola de TTN**, a la secció "Integrations":

- Clic a "MQTT".
- Clic a "Add integration".
- A la URL del broker: `mqtt://100.x.y.z:1883`.
- Username: `ttn-bridge`.
- Password: la contrasenya.
- Desar.

4. **Verificar** que TTN es pot connectar al broker. A la consola, a la secció "Integrations", hauria d'aparèixer "Connected".

## 26.14 El paper de l'Application Server

Al BernatLab, l'**application server** és el que consumeix les dades de TTN. En el model de TTN, això podem ser:

- La **consola web de TTN** (per visualitzar i debugar).
- Un **broker MQTT** (com el nostre Mosquitto).
- Un **servei extern** (AWS IoT, Azure IoT Hub, etc.).

Per al nostre cas, l'application server és el **broker Mosquitto del BernatLab**, i els consumidors són Telegraf, Node-RED, i Grafana.

## 26.15 Resum

En aquest capítol hem après com funciona la capa LoRaWAN: els identificadors (DevEUI, AppEUI, AppKey), els mètodes d'unió (OTAA recomanat, ABP com a excepció), els formats de payload (CayenneLPP, JSON, binari personalitzat), la integració amb MQTT, els downlinks, les classes de dispositius, i el procediment de join. Hem configurat la integració MQTT a TTN perquè les dades dels nodes arribin al broker del BernatLab. En el proper capítol muntarem un gateway LoRaWAN a la Raspberry amb Concentratord.

## 26.16 Exercicis pràctics

1. Crea un compte a TTN: https://console.thingsnetwork.org/
2. Crea una aplicació anomenada `hort-osona-bernat`.
3. Afegeix un dispositiu de prova a l'aplicació. Anota DevEUI, AppEUI, AppKey.
4. Configura la integració MQTT a TTN apuntant al broker del BernatLab.
5. Prova de subscriure't a `v3/#` al broker Mosquitto. Hauries de veure algun missatge de keepalive.
6. Escriu un payload formatter (decoder CayenneLPP) per a un node que envia temperatura, humitat, i humitat del sòl.
7. Documenta al README del projecte els identificadors de cada node, mai en text pla al repositori.

Comandes útils:

```bash
# Crear usuari MQTT per a TTN
docker exec mosquitto mosquitto_passwd -c /mosquitto/config/passwordfile ttn-bridge

# Provar la connexió
mosquitto_sub -h 100.x.y.z -t "v3/#" -v -u bernat -P CONTRASENYA
```

Paraules clau: **TTN, The Things Network, The Things Stack, TTS, consola, aplicació, dispositiu, DevEUI, AppEUI, AppKey, NwkSKey, AppSKey, DevAddr, OTAA, ABP, join, join request, join accept, device profile, payload, CayenneLPP, JSON, binari, decoder, encoder, formatter, MQTT, integració, broker, topic, uplink, downlink, classe A, classe B, classe C, RX1, RX2, duty cycle, dev nonce, app nonce, fcnt, fport, EUI-64, EUI-48, IEEE 802.15.4g, xarxa, network server, application server, MQTT broker, Mosquitto, ACL, usuari, contrasenya, keepalive, packet forwarder, concentratord, xifrat, AES-128, integritat, autenticació, anti-replay, FCntUp, FCntDown, session keys, session context, NwkSKey, AppSKey, derivació, seguretat LoRaWAN, EU868, 868 MHz, EU868, channels, data rates, DR0-DR5, ADR, datr, payload size, maximum payload size, dwell time, ETSI, ISM, sub-banda, normativa**.
