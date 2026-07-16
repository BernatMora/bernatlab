# Qüestionari - Capitol 3: Protocol LoRa (SX1262 868 MHz)

> 10 preguntes · ~15 min

## Pregunta 1
Que es LoRa?

- [ ] Un protocol de xarxa com LoRaWAN
- [x] Una modulacio de radio de llarg abast
- [ ] Una variant de WiFi
- [ ] Un sistema de cellular

## Pregunta 2
A quina frequencia opera LoRa a Europa?

- [ ] 2.4 GHz
- [ ] 433 MHz
- [x] 868 MHz
- [ ] 5 GHz

## Pregunta 3
Quin es el modul radio mes utilizat actualment per LoRa?

- [ ] nRF24L01
- [ ] ESP8266
- [x] SX1262
- [ ] SIM800

## Pregunta 4
Que pasa si augmentes el Spreading Factor de SF7 a SF12?

- [ ] Es mes rapid pero mes curt
- [x] Es mes lent pero mes abast
- [ ] No canvia res
- [ ] Es mes rapid i mes abast

## Pregunta 5
Quina es la potencia maxima de transmissio permesa a 868 MHz sense llicencia a Europa?

- [ ] +5 dBm
- [x] +14 dBm
- [ ] +25 dBm
- [ ] +33 dBm

## Pregunta 6
Quant dura aproximadament un sensor LoRa amb 2 piles AA enviant cada 15 min?

- [ ] Un dia
- [ ] Un mes
- [x] 2-3 anys
- [ ] 10 anys

## Pregunta 7
Que es el duty cycle a 868 MHz i quin es el limit?

- [ ] El temps total de vida del sensor
- [x] El percentatge de temps que pots transmetre; limit 1%
- [ ] La distancia maxima
- [ ] La potencia maxima

## Pregunta 8
Quina diferencia hi ha entre LoRa i LoRaWAN?

- [ ] Son sinonims
- [x] LoRa es la capa fisica; LoRaWAN es el protocol de xarxa
- [ ] LoRaWAN es nomes per a USA
- [ ] LoRa nomes funciona a l'espai

## Pregunta 9 (oberta)
Explica el trade-off entre Spreading Factor (SF), Battery Width (BW) i abast. Quins valors triaries per a un hort amb sensors a 500 m del gateway, i per que?

Pistes per respondre:
- SF7-SF12: mes SF = mes abast pero mes temps a l'aire.
- BW 125-500 kHz: mes estret = mes sensible pero menys capacitat.
- 500 m no es gaire lluny, per tant SF9-SF10 es suficient.
- Si tens arbres pel mig, millor pujar SF.

## Pregunta 10 (oberta)
Tens un hort amb 3 sectors: un a 50 m, un a 500 m i un a 3 km del gateway. Tria la tecnologia adequada (BLE, WiFi, LoRa, Cellular) per a cada un i justifica. Considera consum, preu, abast i cobertura cellular.

Pistes per respondre:
- 50 m: BLE perfecte si el MiFlora hi arriba; alternativa WiFi si tens cobertura.
- 500 m: loRa SF10 es suficient; BLE no arriba; WiFi no arriba; cellular depen de cobertura.
- 3 km: nomes LoRa SF12 o cellular (si tens cobertura).
- Considera tambe el cost del sensor i el consum.
