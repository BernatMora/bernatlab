# P0 - Blink i LED via web

> Projecte P0 del Bernat Maker Lab: una ESP32 que encen i apaga un LED des d'una pagina web oberta al navegador.

## Estat

- [x] Documentat
- [ ] Material comprat
- [ ] Muntat
- [ ] Programat
- [ ] Validat amb captura de pantalla

## Que fa

Una ESP32 es connecta a la Wi-Fi de casa i aixeca un petit servidor web. Al navegador pots obrir una pagina que te dos botons (ON i OFF) que encenen i apaguen un LED connectat al pin GPIO2.

## Materials necessaris

| Component | Quantitat | Estat |
|---|---|---|
| ESP32 DevKit v1 | 1 | A comprar (kit basic) |
| LED 5 mm (el que sigui) | 1 | A comprar (kit basic) |
| Resistencia 220 ohm | 1 | A comprar (kit basic) |
| Cable USB micro-B | 1 | El del mobil o kit |
| Protoboard | 1 | A comprar (kit basic) |
| Cables Dupont | 3 | A comprar (kit basic) |

## Esquema de connexions

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

⚠️ **Important:**
- Mai connectis 5 V a un GPIO (es 3,3 V).
- Mai connectis res als pins GPIO6-11 (estan lligats a la memoria flash).
- La resistencia de 220 ohm es obligatoria per limitar el corrent.

## Codi complet

```cpp
#include <WiFi.h>
#include <WebServer.h>

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

## Instal·lacio

1. Instal·la Arduino IDE 2.x des de https://www.arduino.cc/en/software
2. A **File -> Preferences**, afegeix a "Additional boards manager URLs":
   `https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json`
3. A **Tools -> Board -> Boards Manager**, busca **esp32** i instal·la el paquet.
4. Connecta lESP32 al PC.
5. Si Windows no el reconeix, instal·la el driver CH340 des de https://www.wch-ic.com/downloads/CH341SER_EXE.html
6. A **Tools**:
   - **Board:** ESP32 Dev Module
   - **Upload Speed:** 115200
   - **Port:** el COM que t'aparegui
7. Enganxa el codi, canvia les credencials Wi-Fi, i puja'l.

## Proves

1. Obre **Tools -> Serial Monitor** a 115200 baud.
2. Hauries de veure "Connectant a Wi-Fi..." i despres "ESP32 connectat. Obre: http://X.X.X.X".
3. Apunta la IP.
4. Obre el navegador a la mateixa Wi-Fi i escriu la IP.
5. Prem els botons. El LED sha dencendre i apagar.

## Errors habituals

| Símptoma | Causa | Solucio |
|---|---|---|
| Caracters estranys al Serial Monitor | Baud incorrecte | Posa 115200 |
| "Connecting..." no acaba | SSID o password mal | Comprova majuscules i espais |
| "Failed to connect to ESP32" | Driver CH340 no instal·lat | Instal·la el driver |
| LED no sencen | Gira les potes del LED | Inverteix anode i catode |
| No es connecta a Wi-Fi | Xarxa 5 GHz | Usa una xarxa 2,4 GHz |

## Millores futures (per a P0+)

- Afegir autenticacio amb contrasenya a la pagina web.
- Llegir lestat del LED a `/status` en JSON.
- Usar WebSockets en lloc de recarregar la pagina.
- Posar la IP a una pantalla OLED.
- Controlar el LED amb un polsador fisic a mes de la web.

## On trobar mes informacio

- **Capitol del curs**: `book/curs/M9/01-blink-i-led-via-web/` (resum, quiz, exercici, respostes).
- **Capitol del llibre**: `book/chapters/70-bernat-maker-lab.md` (porta dentrada al Maker Lab).
- **Decisions**: `maker-lab/docs/decisions/0001-microcontrolador-inicial-esp32-devkit-v1.md` i `0002-llenguatge-inicial-arduino-ide.md`.
