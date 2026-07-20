# Qüestionari - Capitol 2: Sensors Xiaomi MiFlora

> 10 preguntes · ~15 min

## Pregunta 1
Que mesura el sensor MiFlora?

- [ ] Temperatura ambient i humitat
- [x] Humitat del soll, temperatura del soll, EC i lluminositat
- [ ] Pluja i vent
- [ ] Qualitat de l'aire

## Pregunta 2
Quin protocol de comunicacio fa servir el MiFlora?

- [ ] WiFi
- [ ] Zigbee
- [x] Bluetooth Low Energy (BLE)
- [ ] LoRa

## Pregunta 3
Quant dura aproximadament la pila CR2032 del MiFlora?

- [ ] Un dia
- [ ] Una setmana
- [x] Un any
- [ ] Deu anys

## Pregunta 4
Quin es l'abast habitual d'un MiFlora amb un adapter BLE USB normal?

- [ ] 2 metres
- [x] 10-20 metres
- [ ] 100 metres
- [ ] 1 km

## Pregunta 5
Quina llibreria Python s'usa habitualment per llegir el MiFlora?

- [ ] pyserial
- [x] miflora
- [ ] requests
- [ ] flask

## Pregunta 6
Quina ordre pots fer servir per descobrir les MAC dels sensors BLE a la RPi?

- [ ] ifconfig
- [x] sudo hcitool lescan
- [ ] ping
- [ ] mqtt ls

## Pregunta 7
Que passa si poses el sensor en sol molt argilos?

- [ ] Dona lectures mes precises
- [x] Dona lectures menys fiables
- [ ] Es trenca immediatament
- [ ] Canvia a WiFi

## Pregunta 8
Quina es una limitacio important del MiFlora respecte a un sensor professional amb SD?

- [ ] Es mes car
- [x] No te datalogger intern; si la RPi no esta, no guarda res
- [ ] No te bluetooth
- [ ] No funciona a l'exterior

## Pregunta 9 (oberta)
Explica per que el MiFlora fa servir BLE i no WiFi. Quines avantatges i inconvenients te respecte altres tecnologies com Zigbee o LoRa?

Pistes per respondre:
- Pensa en consum energetic: una pila CR2032 dona pocs mAh.
- BLE esta dissenyat per transmissions curtes i poc frequents.
- Zigbee i LoRa son opcions, pero el MiFlora no les soporta.
- L'abast es limitat (10-20 m) i això es un inconvenient per horts grans.

## Pregunta 10 (oberta)
Vols cobrir un hort de 100 metres de llarg amb sensors de soll. Tens dues opcions: 10 MiFlora amb una RPi central, o 5 sensors LoRa amb un gateway unic. Escriu 3 pros i 3 contres de cada opcio i recomana una.

Pistes per respondre:
- MiFlora: barata pero curt abast. 10 MiFlora = 120€, una RPi a prop.
- LoRa: mes car (50€/sensor) pero arriba a kms. Un gateway central.
- Hort de 100 m: el MiFlora potser necessita 2-3 RPi com a repetidors.
- Per a una startup es valid MiFlora; per a un hort industrial, LoRa.


## Pregunta 11 (oberta amb pistes)
Per que els sensors MiFlora son una bona opcio per a un hort petit

## Pregunta 12 (oberta amb pistes)
Explica els reptes de fer lectures regulars de sensors Bluetooth desde una RPi

## Pregunta 13 (oberta amb pistes)
Quines dades sha de llegir dun sensor MiFlora i quines son les mes utils
