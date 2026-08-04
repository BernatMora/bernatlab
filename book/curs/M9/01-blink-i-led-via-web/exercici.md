# Exercici pràctic — Capítol 1: Blink i LED via web (Bernat Maker Lab)

> 60-90 min · Real al teu PC i la teva ESP32

## Objectiu

Muntar, programar i fer funcionar el **projecte P0 del Bernat Maker Lab**: una ESP32 que encén i apaga un LED des d'una pàgina web oberta al navegador. Verificar que tota la cadena funciona (Wi-Fi → ESP32 → LED) abans de passar a P1.

## Requisits

- 1 × ESP32 DevKit v1 (la del kit).
- 1 × LED 5 mm, 1 × resistència 220 Ω, 1 × protoboard, 3 cables Dupont.
- 1 × cable USB micro-B (el del kit o el del mòbil).
- PC amb Windows 10/11.
- Connexió a una xarxa Wi-Fi de 2,4 GHz (l'ESP32 **no** suporta 5 GHz).
- 60-90 minuts.

## Pas 1: Instal·la Arduino IDE (10 min)

1. Descarrega Arduino IDE 2.x des de https://www.arduino.cc/en/software
2. Instal·la'l amb les opcions per defecte.
3. Obre'l. Vés a **File → Preferences**.
4. Al quadre "Additional boards manager URLs", enganxa:
   `https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json`
5. Vés a **Tools → Board → Boards Manager**.
6. Busca **esp32** i instal·la el paquet d'Espressif Systems (pot trigar 1-2 min).

## Pas 2: Connecta l'ESP32 i instal·la el driver si cal (5 min)

1. Connecta l'ESP32 al PC amb el cable USB.
2. A Windows, obre **Device Manager** (Administrador de dispositius).
3. Mira si apareix un port COM nou a la secció "Ports (COM & LPT)".
4. Si **no** apareix:
   - Les plaques amb xip **CH340** necessiten el driver: descarrega'l des de https://www.wch-ic.com/downloads/CH341SER_EXE.html
   - Les plaques amb xip **CP2102** solen funcionar directament.
5. Apunta't el número de port (per exemple, COM5). El necessitaràs més tard.

## Pas 3: Munta el circuit (5 min)

1. Desconnecta l'ESP32 del PC.
2. Munta a la protoboard:
   - **GND** de l'ESP32 → un cable cap a la fila de GND de la protoboard.
   - **GPIO2** de l'ESP32 → un cable cap a una fila lliure.
   - **Pota llarga** del LED (ànode) → connecta-la a la **resistència de 220 Ω**, i l'altre extrem de la resistència al cable que ve de GPIO2.
   - **Pota curta** del LED (càtode) → fila de GND.
3. Revisa que no hi hagi cap curtcircuit visible.

## Pas 4: Escriu i puja el codi (10 min)

1. A Arduino IDE, obre **File → New Sketch**.
2. Esborra tot el codi per defecte i enganxa el codi del resum (apartat "Codi mínim").
3. **Canvia les credencials** `ssid` i `password` per les de la teva Wi-Fi de 2,4 GHz.
4. A **Tools**, configura:
   - **Board:** "ESP32 Dev Module"
   - **Upload Speed:** 115200
   - **Port:** el COM que t'ha aparegut al Pas 2.
5. Fes clic a la **fletxa de pujar** (→).
6. Espera 20-40 segons. Al final hauries de veure "Leaving... Hard resetting...".

## Pas 5: Verifica que tot funciona (5 min)

1. Obre **Tools → Serial Monitor**.
2. A la part de baix, posa la velocitat a **115200 baud**.
3. Hauries de veure missatges com:
   ```
   Connectant a Wi-Fi.......
   ESP32 connectat. Obre: http://192.168.1.XX
   ```
4. **Apunta't la IP** que surt.
5. Obre el navegador (del PC o del mòbil, a la mateixa Wi-Fi) i escriu `http://LA-IP`.
6. Hauries de veure la pàgina web amb dos botons.
7. Prem **ON** → el LED s'ha d'encendre.
8. Prem **OFF** → el LED s'ha d'apagar.

## Pas 6: Prova el Blink clàssic (variació, 5 min)

Per comprovar que la placa està sana, prova el Blink sense Wi-Fi:

1. Fes una còpia de l'sketch.
2. Substitueix tot el codi per:
   ```cpp
   void setup() {
     pinMode(2, OUTPUT);
   }
   void loop() {
     digitalWrite(2, HIGH);
     delay(500);
     digitalWrite(2, LOW);
     delay(500);
   }
   ```
3. Puja'l. El LED ha de pampalloguejar cada segon.

Si això funciona, la placa, el cable i el driver estan bé.

## Validació

Has acabat si:

- [ ] Has vist "ESP32 connectat" al Serial Monitor.
- [ ] Has pogut obrir la pàgina web a la IP de l'ESP32.
- [ ] El LED s'encén i s'apaga en prémer els botons.
- [ ] Has provat el Blink clàssic per separat i funciona.
- [ ] Has fet una captura de pantalla de la pàgina web funcionant.

## Què fer si alguna cosa falla

| Símptoma | Causa probable | Solució |
|---|---|---|
| El Serial Monitor mostra caràcters estranys | Baud rate mal posat | Posa 115200 |
| "Connecting..." no acaba mai | SSID o contrasenya incorrectes | Comprova majúscules i espais |
| "Failed to connect to ESP32" | Driver CH340 no instal·lat o port COM mal tri | Re-instal·la el driver, canvia de port USB |
| LED no s'encén | Gira'l (potes intercanviades) o la resistència és massa gran | Inverteix les potes, prova amb 220 Ω |
| LED molt dèbil | Massa resistència | 220 Ω és l'estàndard |
| No es connecta a la Wi-Fi | Xarxa 5 GHz o SSID ocult | Usa una xarxa 2,4 GHz, comprova el SSID |

## Què ve després

Quan tot funcioni, ja tens la base per a:

- **P1** — Llegir un sensor (DHT22 o DS18B20) i mostrar-lo a la pàgina web.
- **P2** — Posar una segona ESP32 i fer-les parlar.
- **P3** — Connectar-les via MQTT a la teva Raspberry Pi.
- **P4** — Guardar les dades a InfluxDB i visualitzar-les amb Grafana.

Guarda la captura de pantalla: et servirà com a "foto inicial" del laboratori maker.
