# Respostes - Capitol 2: Sensors Xiaomi MiFlora

> Mira les respostes DESPRES d'haver fet el qüestionari.

## Pregunta 1: Que mesura el MiFlora?

**Resposta correcta**: Humitat del soll, temperatura del soll, EC i lluminositat.

**Explicacio**: Son les quatre lectures canoniques del sensor. La humitat del substrat en %, la temperatura del soll en graus, la conductivitat electrica (proxy de nutrients) en µS/cm, i la lluminositat en lux. NO mesura temperatura ambient, pluja o vent - per aixo necessites altres sensors com el BME280.

---

## Pregunta 2: Protocol del MiFlora?

**Resposta correcta**: Bluetooth Low Energy (BLE).

**Explicacio**: BLE es una variant del Bluetooth 4.0+ dissenyada per consum molt baix. Perfecta per sensors amb pila de botó. No es WiFi (consum massa alt), ni Zigbee (no es suporta al MiFlora), ni LoRa (també no suportat).

---

## Pregunta 3: Durada de la pila?

**Resposta correcta**: Un any.

**Explicacio**: La pila CR2032 dona uns 220 mAh. El MiFlora transmitent cada 5-10 min gasta uns 0.5-1 µA de mitjana, amb pics de 15 mA durant les transmissions. El calcul dona entre 6 i 18 mesos, amb l'any sent un bon promig. Factors que redueixen la vida: temperatures extremes, transmissions massa frequents, distancia al receptor.

---

## Pregunta 4: Abast del BLE?

**Resposta correcta**: 10-20 metres.

**Explicacio**: Un adapter BLE USB basic (com els de la RPi 4) dona uns 10 metres en interior i 20 en exterior amb visio directa. Amb un dongle USB amb antena externa pots arribar a 30-50 metres. Per mes abast cal un node repetidor o canviar a LoRa (veure cap 3).

---

## Pregunta 5: Llibreria Python?

**Resposta correcta**: miflora.

**Explicacio**: `miflora` es una llibreria Python de codi obert que descodifica els advertisements BLE del MiFlora. Combina amb `btlewrap` per suportar multiples backends (bluepy, gatttool). Alternativa: `bleak` (mes moderna, asyncio) o `homeassistant-mitemp_bt` si estas a Home Assistant.

---

## Pregunta 6: Comanda per descobrir MACs?

**Resposta correcta**: `sudo hcitool lescan`.

**Explicacio**: `hcitool` es la CLI de BlueZ per interactuar amb Bluetooth classic i LE. `lescan` fa un scan actiu de 8 segons mostrant tots els BLE visibles. Alternatives modernes: `bluetoothctl` o `btmgmt`. Totes requereixen root o pertanyer al grup `bluetooth`.

---

## Pregunta 7: Sol argilos?

**Resposta correcta**: Dona lectures menys fiables.

**Explicacio**: El sensor d'humitat del MiFlora es **capacitiu** (mesura la permitivitat electrica del soll). En substrat universal o torba, funciona molt be. En argila pura o sòl calcari, la lectura pot ser uns punts per sobre o per sota del real. Per aixo es important calibrar: posa el sensor en un test amb aigua destil·lada (100%) i en un test sec al aire (0%), i ajusta.

---

## Pregunta 8: Limitacio vs sensor amb SD?

**Resposta correcta**: No te datalogger intern; si la RPi no esta, no guarda res.

**Explicacio**: El MiFlora nomes transmet quan te un receptor a prop. Si la RPi esta apagada o lluny, les lectures es perden per sempre. Un sensor amb SD (com el Sensoterra o un ESP32 amb MicroSD) guarda en local i pujarà les dades quan trobi xarxa. Es un trade-off: preu (MiFlora 12€) vs robustesa (SD 50€+).

---

## Pregunta 9 (oberta): Per que BLE i no WiFi

**Resposta model**:

El MiFlora fa servir **Bluetooth Low Energy (BLE)** principalment per raons d'**estalvi energetic**. La pila CR2032 te una capacitat d'uns 220 mAh, i BLE esta dissenyat especificament per a transmissions curtes i poc frequents amb un consum de microamperes en repòs. Si el sensor fes servir WiFi, la pila duraria dies en lloc d'un any. Per tant, BLE es l'unica opcio viable per a sensors amb pila de botó.

Comparat amb Zigbee: Zigbee es similar a BLE en consum pero usa una xarxa mesh nativa (els dispositius es reenvien senyals entre ells). El MiFlora no suporta Zigbee, pero seria una bona opcio teòrica. Zigbee te l'avantatge que la xarxa es auto-configura i pots cobrir mes distancia amb molts sensors.

Comparat amb LoRa: LoRa es per **llarg abast** (km) i consum encara mes baix, pero les transmissions son mes lentes i la capacitat de dades es molt petita. Per a sensors que nomes envien 4 lectures curtes cada 15 min, LoRa seria ideal si el preu no fos un problema (un radio LoRa costa 5-10€ pero el gateway es car).

Avantatges de BLE: barat (4€ de radio integrat), estandard, suport a tots els smartphones, llibreries Python cuidades, firmware estable del MiFlora.

Inconvenients de BLE: abast limitat (10-20 m), no es mesh nativament, no es apte per horts grans sense infraestructura.

---

## Pregunta 10 (oberta): MiFlora vs LoRa per 100 m

**Resposta model**:

**Opcio A: 10 MiFlora amb RPi central**

Pros:
- Preu molt baix: 10 x 12€ = 120€ en sensors. La RPi ja la tens.
- Precisio bona en substrat (lectura valida per a l'hort).
- Facil de muntar amb la llibreria `miflora`.
- Si un sensor falla, es canvia per 12€.

Contres:
- Abast 10-20 m, per tant amb una sola RPi nomes cobreixes uns 30-40 m de l'hort.
- Necesitaries 2-3 RPi com a gateways repartides, o repetidors ESP32.
- Coordinacio: cada RPi te la seva propia instància del servei, has de coordinar.
- Si fallen les 3 RPi (apagada, calor, etc.) totes les dades es perden.

**Opcio B: 5 sensors LoRa amb un gateway unic**

Pros:
- Abast de kms, un sol gateway al centre de l'hort cobreix tots els 100 m (i de sobres).
- Cada sensor es autonom amb la seva pila (dura mes que MiFlora, 2-5 anys).
- Una sola font de dades, un sol pipeline.
- Molt mes robust: si un sensor falla, els altres 4 continuen.

Contres:
- Preu: 5 x 50€ = 250€ en sensors, mes 100€ del gateway LoRa = 350€ total. ~3x mes car.
- Has de soldar o muntar els sensors tu (no son plug-and-play).
- Necessites un gateway LoRa (un ESP32 + radio SX1276 + antena).
- Menys opcions comercials: poca oferta, mes DIY.

**Recomanacio**: Per a un hort de 100 m amb **pressupost limitat** (cas del BernatLab), triaria **Opcio A amb 2 RPi** (una a cada extrem) i cable Ethernet entre elles. Cobreixes tot l'hort, gastes poc, i si tens experiencia amb soldadura pots migrar a LoRa despres. Per a un **hort professional** o una explotacio que necessiti cobertura garantida 24/7, aniria directe a LoRa per la robustesa.

---

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum i fer l'exercici practic amb el teu MiFlora.
- **3-4 encerts**: Repassar la diferencia entre BLE, Zigbee i LoRa.
- **0-2 encerts**: Comencem pel basico: que es BLE, com funciona una pila CR2032.

## Que fer si has encertat totes

- Passa al **Capitol 3** (LoRa per a abast mes gran).
- Investiga el projecte TheengsGateway per suportar multiples sensors BLE.
- Mira el firmware alternatiu OpenMiFlora per canviar la freq de transmissio.
- Compara amb el projecte BParasite que es DIY pero mes barat.
