# Respostes — Capítol 1: Blink i LED via web (Bernat Maker Lab)

> Mira les respostes DESPRÉS d'haver fet el qüestionari.

## Pregunta 1: Què és un microcontrolador?

**Resposta correcta**: Un xip amb processador, memòria i pins d'entrada/sortida, que executa un sol programa.

**Explicació**: Un microcontrolador és un "ordinador" en un sol xip. No té sistema operatiu (o en té un de molt mínim). El programa que hi carregues és l'únic que s'executa. L'ESP32 n'és un dels més populars perquè afegeix Wi-Fi i Bluetooth al mateix xip.

---

## Pregunta 2: Què significa GPIO?

**Resposta correcta**: Un pin configurable com a entrada o sortida digital.

**Explicació**: GPIO = General Purpose Input/Output. Són els pins "lliures" del xip que podem programar per posar tensions de 0 V o 3,3 V (mode sortida) o per llegir si hi ha tensió o no (mode entrada).

---

## Pregunta 3: A quina tensió treballen els GPIO de l'ESP32?

**Resposta correcta**: 3,3 V.

**Explicació**: Mai 5 V directament a un pin — cremaries l'ESP32. Si necessites connectar alguna cosa a 5 V, usa un conversor de nivell lògic bidireccional.

---

## Pregunta 4: Per què posem una resistència en sèrie amb el LED?

**Resposta correcta**: Per limitar el corrent i no cremar el LED ni forçar el pin.

**Explicació**: Un LED sense resistència pot demanar centenars de mA. El pin de l'ESP32 pot donar com a molt ~40 mA amb seguretat. La resistència de 220-330 Ω deixa passar uns 10-15 mA, perfecte per a la majoria de LEDs.

---

## Pregunta 5: Quin pin NO hem de tocar mai a l'ESP32?

**Resposta correcta**: GPIO6-11 (estan lligats a la memòria flash).

**Explicació**: Aquests pins estan connectats a la memòria flash SPI on viu el programa. Si els forcem, podem fer que la placa deixi de flashejar o es torni inestable. La resta de GPIO (0, 1, 2, 3, 4, 5, 12-33) són segurs.

---

## Pregunta 6: Què fa la funció `WiFi.begin(ssid, password)`?

**Resposta correcta**: Inicia la connexió a la xarxa Wi-Fi indicada.

**Explicació**: Aquesta funció és no-bloquejant: torna immediatament i la connexió passa en segon terme. Per això al codi hi ha un bucle `while (WiFi.status() != WL_CONNECTED)` que espera amb `delay(500)`.

---

## Pregunta 7: Què retorna `WiFi.localIP()` un cop connectats?

**Resposta correcta**: L'adreça IP que el router ha assignat a l'ESP32.

**Explicació**: El router, via DHCP, assigna una IP única a cada dispositiu de la xarxa. Pot canviar entre reinicis. Si vols una IP fixa, configura-la al router (DHCP static lease) o al codi amb `WiFi.config()`.

---

## Pregunta 8: Quin és el port per defecte d'un servidor HTTP?

**Resposta correcta**: 80.

**Explicació**: Per això al codi hi ha `WebServer servidor(80)`. Si canvies el port (per exemple, 8080), hauràs d'escriure la IP completa al navegador: `http://192.168.1.50:8080`.

---

## Pregunta 9: En aquest projecte, l'ESP32 actua com a servidor web.

**Resposta correcta**: Verdader.

**Explicació**: L'ESP32 serveix pàgines HTML. El navegador (client) les demana. La diferència amb el patró "normal" (un servidor al núvol) és que tot passa a la xarxa local — no cal internet, no cal cap proveïdor extern.

---

## Pregunta 10: Què passa si visites http://IP-ESP32/on al navegador?

**Resposta correcta**: S'encén el LED.

**Explicació**: La ruta `/on` està associada a la funció `handle_on()`, que posa el pin a HIGH (3,3 V) i torna la pàgina. La ruta `/off` fa el contrari.

---

## Pregunta 11: Per què la IP de l'ESP32 pot canviar entre reinicis?

**Resposta correcta**: Perquè el router assigna IPs dinàmiques via DHCP.

**Explicació**: El DHCP és un protocol pel qual el router "presta" IPs als dispositius que es connecten. Cada cop que l'ESP32 es reconnecta, pot rebre una IP diferent. Solució: DHCP static lease al router, o `WiFi.config(ip, gateway, subnet)` al codi.

---

## Pregunta 12: Què és millor per a sensors: HTTP com en aquest projecte, o MQTT?

**Resposta correcta**: MQTT, perquè gasta menys energia i és més flexible.

**Explicació**: HTTP serveix per a peticions puntuals. MQTT està dissenyat per a sensors que envien dades contínuament: el client manté una connexió persistent, el missatge és molt més petit, i pots subscriure't a patrons de temes. P3 del laboratori introdueix MQTT.

---

## Pregunta 13: Quina eina de programació recomanem per començar?

**Resposta correcta**: Arduino IDE.

**Explicació**: Arduino IDE és la porta d'entrada més suau al món ESP32. PlatformIO (VSCode) és més professional i l'usarem quan els projectes siguin grans. MicroPython és interessant però menys主流.

---

## Pregunta 14: Què passa si obres el Serial Monitor a una velocitat incorrecta?

**Resposta correcta**: Es mostren caràcters estranys o il·legibles.

**Explicació**: El Serial Monitor i l'ESP32 han d'acordar la velocitat (baud rate). Al codi tenim `Serial.begin(115200)`, i al monitor hem de posar 115200. Si no coincideixen, veuràs caràcters com `⸮⸮⸮` o text sense sentit.

---

## Pregunta 15: Quin cost aproximat té una ESP32 DevKit v1?

**Resposta correcta**: 5-7 €.

**Explicació**: És una de les plaques més barates del mercat. Per 5-7 € tens un xip de 32 bits amb Wi-Fi, Bluetooth, molts GPIO, ADC, DAC, I2C, SPI, UART, PWM... Una bestialitat.
