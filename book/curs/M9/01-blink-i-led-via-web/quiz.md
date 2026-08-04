# Qüestionari — Capítol 1: Blink i LED via web (Bernat Maker Lab)

> 15 preguntes · ~20 min · Pots repetir les vegades que vulguis.

## Pregunta 1
Què és un microcontrolador?

- [ ] Un PC de mida petita
- [x] Un xip amb processador, memòria i pins d'entrada/sortida, que executa un sol programa
- [ ] Un sistema operatiu per a servidors
- [ ] Un tipus de sensor de temperatura

## Pregunta 2
Què significa GPIO?

- [ ] General Purpose Input/Output (Entrada/Sortida de Propòsit General)
- [x] Un pin configurable com a entrada o sortida digital
- [ ] Un bus de comunicació ràpida
- [ ] Una mena d'antena Wi-Fi

## Pregunta 3
A quina tensió treballen els GPIO de l'ESP32?

- [ ] 5 V
- [x] 3,3 V
- [ ] 12 V
- [ ] 230 V

## Pregunta 4
Per què posem una resistència en sèrie amb el LED?

- [ ] Per fer-lo brillar més
- [x] Per limitar el corrent i no cremar el LED ni forçar el pin
- [ ] Per canviar el color del LED
- [ ] No cal posar-ne cap

## Pregunta 5
Quin pin NO hem de tocar mai a l'ESP32?

- [ ] GPIO2
- [ ] GPIO4
- [x] GPIO6-11 (estan lligats a la memòria flash)
- [ ] GPIO32

## Pregunta 6
Què fa la funció `WiFi.begin(ssid, password)`?

- [ ] Inicialitza el servidor web
- [x] Inicia la connexió a la xarxa Wi-Fi indicada
- [ ] Apaga la Wi-Fi
- [ ] Res, és sols decorativa

## Pregunta 7
Què retorna `WiFi.localIP()` un cop connectats?

- [ ] El SSID de la xarxa
- [x] L'adreça IP que el router ha assignat a l'ESP32
- [ ] La contrasenya de la Wi-Fi
- [ ] Un error si no estem connectats

## Pregunta 8
Quin és el port per defecte d'un servidor HTTP?

- [ ] 21
- [ ] 22
- [ ] 8080
- [x] 80

## Pregunta 9
Veritable o fals: en aquest projecte, l'ESP32 actua com a servidor web.

- [x] Verdader
- [ ] Fals

## Pregunta 10
Què passa si visites http://IP-ESP32/on al navegador?

- [ ] S'apaga el LED
- [x] S'encén el LED
- [ ] Es reinicia l'ESP32
- [ ] No passa res, perquè cal enviar un POST

## Pregunta 11
Per què la IP de l'ESP32 pot canviar entre reinicis?

- [ ] Perquè l'ESP32 s'equivoca
- [x] Perquè el router assigna IPs dinàmiques via DHCP
- [ ] Perquè la placa es trenca
- [ ] Perquè el Wi-Fi no funciona

## Pregunta 12
Què és millor per a sensors: HTTP com en aquest projecte, o MQTT?

- [ ] Sempre HTTP
- [x] MQTT, perquè gasta menys energia i és més flexible
- [ ] Són equivalents
- [ ] Cap dels dos

## Pregunta 13
Quina eina de programació recomanem per començar?

- [x] Arduino IDE
- [ ] Emacs
- [ ] Microsoft Word
- [ ] Photoshop

## Pregunta 14
Què passa si obres el Serial Monitor a una velocitat (baud rate) incorrecta?

- [ ] No es mostra res
- [x] Es mostren caràcters estranys o il·legibles
- [ ] Es destrueix l'ESP32
- [ ] Es canvia el color del LED

## Pregunta 15
Quin cost aproximat té una ESP32 DevKit v1?

- [ ] 50 €
- [ ] 25 €
- [x] 5-7 €
- [ ] 0 € (és gratuïta)
