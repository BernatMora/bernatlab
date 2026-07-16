# Respostes - Capitol 1: Que son les dades d'un hort

> Mira les respostes DESPRES d'haver fet el qüestionari.

## Pregunta 1: Quines families de dades?

**Resposta correcta**: Ambientals, de soll, de cultiu, de gestio.

**Explicacio**: Son les quatre families que cobreixen tot el que passa a un hort. Ambientals = entorn (cel, aire). De soll = el que toca les arrels. De cultiu = la planta en si. De gestio = el que fa l'hortola. Qualsevol dada del teu hort ha de cabre en una d'aquestes quatre categories, sino potser estas inventant una quinta (ex. "dades economiques" -> gestio).

---

## Pregunta 2: Quin sensor per temperatura ambient?

**Resposta correcta**: BME280.

**Explicacio**: El BME280 es un sensor digital de Bosch que mesura temperatura, humitat i pressio en un sol xip petit. Es conectat per I2C a la RPi o a un microcontrolador. Costa uns 3-5€ i te una precisio raonable (±0.4°C). El DHT22 es una alternativa mes antiga pero menys precisa. El MiFlora es per al soll, no per a l'ambient.

---

## Pregunta 3: Que indica l'EC del soll?

**Resposta correcta**: La salinitat i presencia de nutrients.

**Explicacio**: L'EC (conductivitat electrica) es una mesura indirecta de la quantitat de sals dissoltes a l'aigua del soll. Mes sals = mes EC. Les sals son nutrients, pero també pot ser sal comuna que crema les arrels. Un EC de 800-1500 µS/cm es bo per a tomàquet; mes de 3000 comença a ser toxic.

---

## Pregunta 4: Frequencia de temperatura ambient?

**Resposta correcta**: Cada 5 minuts.

**Explicacio**: La temperatura ambient canviadespacio: en 5 min pot pujar o baixar 1-2°C. Amb 5 minuts tens 288 punts/dia, que es perfecte per grafiques suaus. Cada segon son masses (8.6M punts/dia, inutil). Cada hora son masses pocs (perduries les gelades curtes que duren 20 min).

---

## Pregunta 5: On guardem imatges?

**Resposta correcta**: A MinIO o sistema de fitxers.

**Explicacio**: InfluxDB es per series temporals numeriques, no per blobs binaris com JPEG. PostgreSQL pot guardar-los (bytea) pero no es eficient. MinIO es un magatzem S3-compatible perfecte per imatges i documents. Al sistema de fitxers local tambe va be si es una RPi petita amb poca camera.

---

## Pregunta 6: Per que no 1 Hz?

**Resposta correcta**: Perque la base de dades creix rapidissim.

**Explicacio**: 1 Hz = 86.400 punts/dia per sensor. Si tens 5 sensors son 432.000 punts/dia, 13M al mes, 156M a l'any. InfluxDB ho aguanta, pero la memoria RAM, la CPU per comprimir i l'espai de disc creixen tambe. Es captura inutil perque la temperatura no canvia 86.400 cops al dia (canviara unes 200-500 vegades significatives).

---

## Pregunta 7: Dada "de gestio"?

**Resposta correcta**: Registre d'un reg amb la seva durada.

**Explicacio**: La gestio es el que **fa** l'hortola o el sistema automaticament. Un registre de reg es gestio perque documenta una accio. Les dades ambientals i de soll son **mesures** (passives), mentre que les de gestio son **accions** (actives). Un reg es una accio amb data, durada, litres i sector.

---

## Pregunta 8: Millor magatzem per series temporals?

**Resposta correcta**: InfluxDB.

**Explicacio**: InfluxDB esta optimitzat per time-series: comprimeix molt be, te consultes natives en Flux i InfluxQL, retentions automatiques (esborrar dades velles), i downsampling (resumir dades antigues). PostgreSQL tambe pot fer-ho amb extensions (TimescaleDB) pero InfluxDB es mes lleuger per a una RPi.

---

## Pregunta 9 (oberta): Diferencia ambientals vs soll

**Resposta model**:

Les **dades ambientals** son les que mesuren el que envolta la planta: l'aire, la llum, el vent, la pluja. Es el que veuries si surts al carrer i mires amunt. A un hort de tomàquets, el BME280 del hivernacle pot marcar 28°C d'ambient i 65% d'humitat relativa. Són dades que canvien per causes externes (sol, núvols, vent).

Les **dades de soll** son les que mesuren el que esta **a dins** del test o del camp on viuen les arrels. Un MiFlora clavat al test del tomàquet pot marcar 19°C de temperatura de soll i 45% d'humitat del substrat. Aquestes dades canvien quan regues, quan el tomàquet beu, quan el sol s'assequega.

Exemple aplicat: un dia de juny a l'Hort Osona, el BME280 marca 32°C ambient, 40% humitat, pero el MiFlora del test marca 22°C de soll i 35% d'humitat. El soll esta mes fresc perque l'aigua del reg baixa la temperatura, i esta sec perque el tomàquet beu molt amb aquesta calor. Si nomes mires l'ambient, penses "ufa, que calor"; si mires el soll, saps que cal regar avui.

---

## Pregunta 10 (oberta): Taula de frequencies

**Resposta model**:

| Sensor              | Freq     | Justificacio                                                  |
|---------------------|----------|---------------------------------------------------------------|
| BME280 (ambient)    | 5 min    | 288 punts/dia, canviadespacio pero volem gelades             |
| Pluviometre         | 1 min    | Xàfecs intensos duren 10-30 min; amb 1 min els capturem      |
| MiFlora (soll)      | 15 min   | El soll canvia a poc a poc; 96 punts/dia son suficients      |
| Camera time-lapse   | 10 min   | 144 fotos/dia, bona resolucio temporal per veure creixement  |
| EC soll             | 30 min   | Els nutrients canvien lentament; 48 punts/dia son sobrats    |
| Comptador d'aigua   | esdeveniment | Només quan s'obre la electrovalvula, no cal periocitat   |

Justificacio general: he triat frequencies **adaptades a la dinàmica** del fenomen. La pluja es rapida i intensa, per tant molta freq. L'EC es lentissima, per tant poca freq. La regla es: **el periode de captura ha de ser 2-3 cops mes petit que el temps caracteristic del fenomen**. Si vols detectar una gelada de 30 min, captura cada 10-15 min, no cada hora.

---

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum i fer l'exercici practic amb el teu hort real.
- **3-4 encerts**: Repassar la taula d'emmagatzematge i les families de dades.
- **0-2 encerts**: Comencem pel basico: quines dades tens, on les guardes, a quina hora les mires.

## Que fer si has encertat totes

- Passa al **Capitol 2** (sensors MiFlora).
- Mira el projecte real Hort Osona al GitHub de BernatMora.
- Investiga que es un "digital twin" aplicat a un hort.
- Comença a pensar com visualitzaries aquestes dades (Grafana, pwa, etc.).
