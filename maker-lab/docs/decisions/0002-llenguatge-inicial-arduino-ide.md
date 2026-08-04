# ADR 0002 - Llenguatge inicial: Arduino IDE (C++)

> **Estat**: Acceptada · **Data**: 2026-08-03 · **Autor**: Bernat + Hermes

## Context

Per programar les plaques ESP32 tenim diverses opcions d'eines i llenguatges. Cal triar-ne una per defecte que ens permeti entrar amb poc fregament i que ens serveixi fins a P3 o P4 com a minim.

## Alternatives considerades

| Alternativa | Pros | Contres |
|---|---|---|
| **Arduino IDE + C++** | Molt facil dentrar-hi, documentacio abundantissima, llibreries per a gairebe tots els sensors. | Editor basic, projectes grans es fan pesats. |
| **PlatformIO + VSCode + C++** | Professional, integracio amb Git, gestor de dependencies, tests integrats. | Mes complex dentrar-hi. |
| **MicroPython** | Python en lloc de C++, iteracio rapidissima (repl). | Menys exemples, mes limitat en certes coses (PWM precis, BLE). |
| **ESPHome** | Integracio directa amb Home Assistant, configuracio com a YAML. | Menys flexible, lligat a un ecosistema. |
| **ESP-IDF (C natiu Espressif)** | Maxim control, optimitzacio extrema. | Molt mes complex, no recomanat per a primers passos. |

## Decisio

**Comencem amb Arduino IDE 2.x + C++** (llenguatge de l'Arduino adaptat a l'ESP32).

## Raonament

1. **Minim fregament dentrada**: Arduino IDE es installa en 2 minuts i el primer Blink es pot fer en 10.
2. **Cobertura maxima**: totes les llibreries de sensors, pantalles, moduls de radio, etc. tenen soport per a lArduino IDE.
3. **Compatibilitat universal**: si trobem un tutorial a Internet, segur que es per a lArduino IDE.
4. **Suficient per a P0-P4**: el que volem fer a curt termini no requereix optimitzacio ni funcionalitats avançades.
5. **Facilitat de migracio**: quan els projectes siguin grans, podem migrar a PlatformIO sense reescriure el codi (els fitxers `.ino` es poden convertir facilment).

## Conseqüencies

- Cal instal·lar Arduino IDE 2.x.
- Cal afegir la URL del gestor de plaques de lESP32: `https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json`.
- Cal instal·lar el driver CH340 si la placa en duu (o el CP2102 que sol funcionar automaticament).
- El codi dels projectes viura a fitxers `.ino` o `.cpp` dins de carpetes per projecte.
- Usarem la extensio de fitxer `.ino` per als projectes petits i `.cpp` per als mes grans.

## Notes operatives

- Velocitat del Serial Monitor: sempre 115200 baud per defecte.
- Cada projecte te la seva carpeta amb un sketch independent.
- Documentacio al wiki de lESP32: https://docs.espressif.com/projects/arduino-esp32/

## Quan migrar a PlatformIO

Migrar a PlatformIO si:

- El projecte te mes de 5-10 fitxers.
- Volem integracio directa amb Git i tests automatics.
- Volem un depurador grafic (debugger).
- Volem gestionar dependencies de manera mes robusta.

## Properes decisions

- ADR 0003 - Patron de capitols del Maker Lab dins del BernatLab.
