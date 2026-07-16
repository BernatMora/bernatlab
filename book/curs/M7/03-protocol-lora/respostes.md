# Respostes - Capitol 3: Protocol LoRa (SX1262 868 MHz)

> Mira les respostes DESPRES d'haver fet el qüestionari.

## Pregunta 1: Que es LoRa?

**Resposta correcta**: Una modulacio de radio de llarg abast.

**Explicacio**: LoRa es la **tecnologia de capa fisica** (com la modulacio QAM del WiFi o el GFSK del Bluetooth). LoRaWAN es el protocol de xarxa que va a sobre. Confondre'ls es l'error mes comu: LoRa nomes es la "radio", com LTE nomes es la radio del 4G.

---

## Pregunta 2: Frequencia a Europa?

**Resposta correcta**: 868 MHz.

**Explicacio**: Europa usa la banda ISM 868 MHz (868-870 MHz). EUA usa 915 MHz. Asia, depen del pais (alguns 433 MHz, altres 920 MHz). Es important triar el modul adequat: el SX1262 ve en dues versions, una per 868 i una per 915. Si compres el de 915 a Europa, no funciona be.

---

## Pregunta 3: Modul radio mes utilizat?

**Resposta correcta**: SX1262.

**Explicacio**: El SX1262 de Semtech es l'ultim modul LoRa i el mes estès. Te millor consum que el seu predecessor SX1276 i mes sensibilitat (fins a -148 dBm). Alternatives: el SX1276 (mes antic, mes barat) o el LLCC68 (variant low-cost). Per a nous projectes, SX1262 es la millor eleccio.

---

## Pregunta 4: Augmentar SF?

**Resposta correcta**: Es mes lent pero mes abast.

**Explicacio**: El Spreading Factor es el nombre de "chips" per simbol. SF7 = 128 chips, SF12 = 4096 chips. Mes chips = mes robustesa en condicions dolentes (mes distancia, mes obstacles), pero el temps de transmisio es molt mes llarg. SF7 transmet 10 bytes en 50 ms; SF12 en 1600 ms. Es un trade-off classic entre velocitat i abast.

---

## Pregunta 5: Potencia maxima sense llicencia?

**Resposta correcta**: +14 dBm.

**Explicacio**: A Europa, la banda 868 MHz esta subjecta a una limitacio de **+14 dBm (25 mW)** EIRP i un **duty cycle de l'1%** per no necessitar llicencia. Als EUA (915 MHz) la potencia maxima es +30 dBm amb duty cycle mes permis. Aixo vol dir que NO pots posar el SX1262 a +22 dBm (que es el maxim del xip) a Europa - es illegal.

---

## Pregunta 6: Durada amb piles AA?

**Resposta correcta**: 2-3 anys.

**Explicacio**: 2 piles AA (2x2500 mAh = 5000 mAh). El node es desperta, transmet durant 1 segon (100 mA), i torna a dormir. El consum mitjana es de 0.5-1 mA. Calcul: 5000 mAh / 0.5 mA = 10.000 hores = 416 dies ~ 1.4 anys. Si la transmissio es menys frequent (cada 1 hora en lloc de cada 15 min), pots arribar a 3-5 anys. Es l'avantatge de LoRa: consum mitjana molt baix.

---

## Pregunta 7: Duty cycle?

**Resposta correcta**: El percentatge de temps que pots transmetre; limit 1%.

**Explicacio**: A la banda 868 MHz a Europa, les regulacions ETSI limiten a un **duty cycle de l'1%**: si transmitis 1 segon, has d'esperar 99 segons abans de poder tornar a transmetre. Aixo es perque la banda es compartida amb altres aplicacions (alarmes, telemandaments, etc.). Si no es compleix, interfereixes altres usuaris legals.

---

## Pregunta 8: LoRa vs LoRaWAN?

**Resposta correcta**: LoRa es la capa fisica; LoRaWAN es el protocol de xarxa.

**Explicacio**: Analogia: LoRa es com el "FM" de la radio; LoRaWAN es com el "protocol de Radio Nacional". LoRa nomes es la modulacio (com els uns i zeros son codificats a la radio). LoRaWAN afegeix: adreces de dispositiu (DevAddr), seguretat (AppKey, NwkSKey), classes de dispositiu (A, B, C), un servidor de xarxa (TTN, ChirpStack), etc. LoRa P2P es com una conversa a walkie-talkie: nomes LoRa, sense servidor.

---

## Pregunta 9 (oberta): Trade-off SF, BW i abast

**Resposta model**:

El **Spreading Factor (SF)** controla la sensibilitat del receptor. Mes SF = mes robustesa = mes abast, pero mes temps a l'aire i menys capacitat. La **Bandwidth (BW)** controla l'ample de banda del canal. Mes estret (125 kHz) = mes sensibilitat pero menys capacitat; mes ample (500 kHz) = menys abast pero mes capacitat.

Per a un hort amb sensors a **500 metres** del gateway amb possibles arbres pel mig, recomanaria:

- **SF = 10**: dona ~2 km d'abast amb visio directa i ~1 km amb arbres. Suficient per 500 m amb marge.
- **BW = 125 kHz**: ample estret, maxima sensibilitat. A 500 m no necessitem capacitat, sino abast.
- **CR = 4/5**: correccio d'errors minima, nomes si hi ha molt de soroll.

No recomanaria SF=12 perque el temps a l'aire es massa llarg (1600 ms per 10 bytes) i el duty cycle de l'1% et limitaria molt. Tampoc recomanaria SF=7 perque a 500 m amb arbres pot ser insuficient.

Si el sector esta en **visio directa** (sense arbres), SF=9 es perfecte. Si hi ha **arbres o edificis**, puja a SF=10 o SF=11. Si hi ha **molt d'obstacle**, considera SF=12 + un node repetidor.

---

## Pregunta 10 (oberta): 3 sectors a 50 m, 500 m, 3 km

**Resposta model**:

**Sector 1 - 50 m del gateway**:
Recomanaria **BLE (MiFlora)**. A 50 m el BLE hi arriba perfectament (fins i tot amb parets), es el mes economic (12€ per sensor), i te bona autonomia amb pila. Alternatives: WiFi si ja tens cobertura, pero consumeix massa per a piles.

**Sector 2 - 500 m del gateway**:
Recomanaria **LoRa SF=10**. BLE no arriba, WiFi no arriba, LoRa es perfecte per aquesta distancia. Preu: 25€ per node ESP32+SX1262, 15€ per gateway. Autonomia: 2-3 anys amb 2 piles AA. Si tens cobertura cellular, podries fer servir un modul NB-IoT (SIM7000) per 20€ + una SIM amb tarifa IoT, pero el cost mensual es alt (1-3€ per dispositiu).

**Sector 3 - 3 km del gateway**:
Recomanaria **LoRa SF=12 amb bona antena**. SF=12 amb antena Yagi arriba a 5-10 km. Si la visio es directa, es la opcio mes barata (40€ per node, 20€ per antena). Alternativa: **cellular (NB-IoT o LTE-M)** si tens cobertura a la zona. Cellular es mes car per node (40€) pero no requereix antena Yagi. Consideracio: si no tens cobertura de cap operador, nomes queda LoRa (o satel·lit, pero es molt car).

**Resum**: per a un hort mixt, la combinacio **BLE + LoRa** es la mes practica. Cellular nomes val la pena si tens cobertura garantida i vols simplificar la gestio (no cal gateway LoRa). Satellite nomes per a casos extrems (hort remot sense cobertura).

---

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum, sobretot la part de SF i BW.
- **3-4 encerts**: Repassar la diferencia entre LoRa i LoRaWAN.
- **0-2 encerts**: Comencem pel basic: que es una modulacio de radio i quines bandes ISM hi ha.

## Que fer si has encertat totes

- Passa al **Capitol 4** (arquitectura completa del Hort Osona).
- Investiga TTN (The Things Network) per fer LoRaWAN amb cobertura comunitaria.
- Compara SX1276 vs SX1262 vs LLCC68 amb benchmarks reals.
- Munta un node LoRa amb panell solar i un sensor de pluja.
