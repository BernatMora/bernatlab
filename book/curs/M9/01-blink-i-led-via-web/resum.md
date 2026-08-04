# Resum — Capitol 1: Blink i LED via web (Bernat Maker Lab)

> Modul M9 - Bernat Maker Lab - Introduccio als microcontroladors

## La idea clau

Un **microcontrolador** es un xip que executa un programa i pot posar tensions de 0 V o 3,3 V a qualsevol dels seus pins (els **GPIO**). L'**ESP32** n'es un dels mes populars perque duu Wi-Fi i Bluetooth integrats, i es pot programar des de qualsevol PC amb un cable USB.

En aquest primer projecte farem dues coses molt senzilles:

1. Encendre i apagar un LED amb un programa classic ("Blink").
2. Encendre i apagar **el mateix LED des d'una pagina web** oberta al navegador.

Aixo demostra el cami complet **PC o telefon -> Wi-Fi -> ESP32 -> GPIO -> LED**, sense necessitat de cap servidor extern.

## Per que comencem per aqui

Perque es el projecte mes petit possible que tanca el cicle basic:

- Sabrem flashejar un firmware a l'ESP32.
- Sabrem fer servir un pin GPIO de sortida.
- Sabrem connectar l'ESP32 a la xarxa Wi-Fi de casa.
- Sabrem aixecar un petit servidor web dins del propi xip.
- Sabrem rebre una ordre HTTP i reaccionar-hi canviant l'estat d'un pin.

Tot el que vindra despres nomes es afegir coses a aquesta base, no pas nous fonaments.

## Que es un microcontrolador (en 30 segons)

Un microcontrolador es un ordinador molt petit, en un sol xip, que te:

- Un **processador** (cervell que executa instruccions).
- Una **memoria** per al programa i les dades.
- Uns **pins d'entrada/sortida** (GPIO) que podem posar a 0 V o 3,3 V.
- Algunes **interficies** de comunicacio: UART, I2C, SPI, i a vegades Wi-Fi, Bluetooth, USB.

A diferència d'un PC o una Raspberry Pi, un microcontrolador **no te sistema operatiu** (o en te un de molt minim). El programa que hi carregues es l'unic que s'executa, en bucle, sempre.

L'**ESP32** es un microcontrolador d'Espressif Systems que te **Wi-Fi i Bluetooth integrats** al xip, cosa que el fa ideal per a projectes que necessiten connectivitat sense afegir moduls externs.

## Que necessitem

| Component | Quantitat | On |
|---|---|---|
| ESP32 DevKit v1 (xip ESP32-WROOM-32) | 1 | Kit basic |
| LED 5 mm (el que sigui) | 1 | Kit basic |
| Resistencia 220 ohm (o 330 ohm) | 1 | Kit basic |
| Cable USB micro-B | 1 | El del kit o el del mobil |
| Protoboard i cables Dupont | 1 + 3 | Kit basic |
| PC amb Arduino IDE o PlatformIO | 1 | El teu |

**Cost:** uns 5-7 EUR (la placa). La resta ve amb el kit basic.

## Connexions

```
ESP32                    Protoboard
+-----------+
|           |      LED + R 220 ohm
|       GND +------+[ 220 ohm ]--+
|           |                    |
|     GPIO 2+--------------------+ (costat llarg del LED, anode)
|           |                    (costat curt del LED, catode, al GND)
+-----------+
```

- **Anode** (pota llarga) del LED -> passa per la resistencia -> **GPIO2**.
- **Catode** (pota curta) del LED -> **GND**.
- La resistencia **limita el corrent**. Sense ella, el LED es pot cremar i, pitjor, pots forcar massa el pin de l'ESP32.

**Truc:** moltes plaques DevKit v1 ja duen un LED soldat a GPIO2. Si nomes vols provar el Blink sense cables, pots usar el LED integrat i estalviar-te el muntatge. Despres muntaras el LED extern per practicar.

## Per que GPIO2 i no un altre?

Per defecte, molts DevKit v1 ja tenen un LED a GPIO2. Es una eleccio segura perque:

- Esta **documentat** a quasi tots els tutorials.
- Es pot fer servir el LED de la placa sense soldar res.
- Esta lluny dels pins de la memoria flash (veure mes avall).

**Important:** mai connectis res als pins **GPIO6, GPIO7, GPIO8, GPIO9, GPIO10, GPIO11**. Estan lligats a la memoria flash interna de l'ESP32 i, si els forcem, la placa pot deixar de flashejar.

## Codi minim (tot el projecte)

```cpp
#include <WiFi.h>
#include <WebServer.h>

// Substitueix per les teves credencials reals
const char* ssid     = "EL_TEU_WIFI";
const char* password = "LA_TEUA_CONTRASENYA";

const int LED_PIN = 2;
WebServer servidor(80);

void handle_root() {
  String html = R"(
    <!doctype html>
    <html><head><meta charset='utf-8'>
    <title>Bernat Maker Lab - P0</title>
    <style>
      body { font-family: system-ui; max-width: 480px; margin: 40px auto; text-align: center; }
      a.btn { display: inline-block; padding: 12px 24px; margin: 8px;
              background: #0a84ff; color: white; text-decoration: none; border-radius: 8px; }
      a.off { background: #555; }
    </style></head><body>
      <h1>Bernat Maker Lab</h1>
      <h2>Projecte P0 - LED via web</h2>
      <p><a class='btn' href='/on'>ON</a>
         <a class='btn off' href='/off'>OFF</a></p>
    </body></html>
  )";
  servidor.send(200, "text/html", html);
}

void handle_on()  { digitalWrite(LED_PIN, HIGH); handle_root(); }
void handle_off() { digitalWrite(LED_PIN, LOW);  handle_root(); }

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);

  WiFi.begin(ssid, password);
  Serial.print("Connectant a Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.print("ESP32 connectat. Obre: http://");
  Serial.println(WiFi.localIP());

  servidor.on("/",  handle_root);
  servidor.on("/on",  handle_on);
  servidor.on("/off", handle_off);
  servidor.begin();
}

void loop() {
  servidor.handleClient();
}
```

## Que fa el programa, pas a pas

1. **Inicialitza** el pin GPIO2 com a sortida i l'apaga.
2. **Es connecta** a la xarxa Wi-Fi amb el SSID i contrasenya que li hem posat.
3. Un cop connectat, **imprimeix la IP** que li ha assignat el router (per exemple, `192.168.1.50`).
4. **Aixeca un servidor HTTP** al port 80 que escolta peticions.
5. Quan algu visita `http://IP/`, serveix la pagina HTML amb dos botons.
6. Quan algu visita `http://IP/on`, encen el LED i re-serveix la pagina.
7. Quan algu visita `http://IP/off`, apaga el LED i re-serveix la pagina.
8. **En bucle**, escolta noves peticions.

No hi ha cap núvol, cap servidor extern, cap dependència. Tot passa a la xarxa local.

## Eines de programacio: quina triar

| Eina | Pros | Contres |
|---|---|---|
| **Arduino IDE** | Senzill, molt documentat, llibreries per a tot. | Editor basic, projectes grans es fan pesats. |
| **PlatformIO** (VSCode) | Professional, integracio amb Git, gestor de dependencies. | Mes complex d'entrar-hi. |
| **MicroPython** | Python en lloc de C++, iteracio rapidissima. | Menys exemples, mes limitat en algunes coses. |

Per començar, **Arduino IDE** es la millor opcio. Es la que farem servir en aquest capitol.

## Connexions amb altres capitols

- **Cap 70 del llibre (Bernat Maker Lab: afegir nova maquinaria al laboratori)** - visio general del projecte.
- **M1 del llibre, Cap 9 (Git i documentacio)** - com versionar el firmware.
- **M2 del llibre, Cap 12 (MQTT des de zero)** - alternativa millor a HTTP per a sensors.
- **M2 del llibre, Cap 20 (API publica)** - com fer un panell web de veritat.
