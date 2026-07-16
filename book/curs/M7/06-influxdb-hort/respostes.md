# Respostes - Capitol 6: InfluxDB per a l'Hort Osona

> Mira les respostes DESPRES d'haver fet el qüestionari.

## Pregunta 1: Que vol dir TSDB?

**Resposta correcta**: Time Series Database.

**Explicacio**: TSDB = Time Series Database. Es un tipus de base de dades optimitzat per guardar i consultar series de dades amb un timestamp. Exemples: InfluxDB, TimescaleDB, Prometheus, QuestDB. No son relacionals ni documentals; son columnars o d'altres estructures.

---

## Pregunta 2: Els 3 conceptes basics?

**Resposta correcta**: Measurement, tags, fields.

**Explicacio**: A InfluxDB una "taula" es un **measurement**, les columnes indexades son **tags** (per agrupar/filtrar rapid), i els valors son **fields** (els nombres reials). El **time** es sempre present. Es diferent de SQL: aqui totes les files d'un measurement comparteixen la mateixa estructura de tags i fields pero poden tenir camps opcionals (null es ignorat).

---

## Pregunta 3: Llenguatge de consulta?

**Resposta correcta**: Flux.

**Explicacio**: Flux es el llenguatge funcional d'InfluxDB 2.x. Esta inspirat en JavaScript i es similar a les pipes Unix. Alternativa: InfluxQL (SQL-like, mes simple pero menys potent) i SQL (a InfluxDB 3.0). Flux es el recomanat per a tasques complexes.

---

## Pregunta 4: Avantatge respecte PostgreSQL?

**Resposta correcta**: Compressio ~10x i consultes rapidissimes sobre intervals de temps.

**Explicacio**: InfluxDB comprimeix les dades amb TSI (Time-Structured Merge Tree) i pot assolir ratios de 10:1 o millor sobre dades de sensors. Les consultes amb `range()` i `aggregateWindow()` son ordenacions de magnitud mes rapides perque el motor sap que les dades estan ordenades per temps i pot saltar blocs sencers. PostgreSQL es excel·lent pero no esta optimitzat per aixo.

---

## Pregunta 5: Que es un bucket?

**Resposta correcta**: Un contenidor de dades amb retencio.

**Explicacio**: Un bucket es com una "base de dades" dins d'un organization. Te retencio propia (e.g. 30 dies raw, 1 any downsample). Pots tenir multiples buckets per separar projectes o per aplicar politiques de retencio diferents. A l'Hort Osona tenim `hort-osona` (raw 30d) i `hort-osona-downsampled` (1h 365d).

---

## Pregunta 6: Que es un task?

**Resposta correcta**: Un proces automatic que transforma dades.

**Explicacio**: Un task es un script Flux que s'executa periodicament. Usos habituals: downsampling (agregar lectures raw a 1h), neteja, ETL, calculs derivats (e.g. index de calor a partir de temp i humitat). S'editen a la UI i es poden activar/desactivar.

---

## Pregunta 7: Port API HTTP?

**Resposta correcta**: 8086.

**Explicacio**: 8086 es el port per defecte de la API HTTP d'InfluxDB (write, query, gestio). Es pot canviar amb la variable `INFLUXD_HTTP_BIND_ADDRESS`. Altres ports comuns: 8088 (RPC, deprecated a 2.x).

---

## Pregunta 8: Line protocol?

**Resposta correcta**: El format text per escriure punts.

**Explicacio**: El line protocol es un format molt eficient per enviar punts: `measurement,tag=v,tag=v field=v,field=v timestamp_ns`. Es pot enviar amb `curl` o qualsevol client HTTP. Es la manera mes directa d'escriure sense una llibreria. Exemple: `miflora,device=miflora-1B32 soil_moisture=42 1712926800000000000`.

---

## Pregunta 9 (oberta): Model de dades amb BME280

**Resposta model**:

El model d'InfluxDB es diferent del model relacional. En lloc de taules amb files, tenim **measurements** amb **tags** (indexats) i **fields** (valors). El temps es sempre present.

Exemple amb una lectura de BME280 del Hort Osona (sensors ambientals del hivernacle):

- **Measurement**: `bme` (nom del "tipus" de lectura)
- **Tags**:
  - `device` = `bme-hivernacle`
  - `sector` = `toma-cherry`
- **Fields**:
  - `temp_c` = 21.3
  - `humidity` = 65.0
  - `pressure_hpa` = 1014.3
  - `lux` = 12500
- **Time**: `2026-04-12T10:00:00Z`

Representacio en line protocol: `bme,device=bme-hivernacle,sector=toma-cherry temp_c=21.3,humidity=65,pressure_hpa=1014.3,lux=12500 1712926800000000000`

**Equivalencia SQL**: la taula equivalent seria `bme_readings(id SERIAL, device VARCHAR, sector VARCHAR, ts TIMESTAMPTZ, temp_c FLOAT, humidity FLOAT, pressure_hpa FLOAT, lux INT)` amb un index compost `(device, ts)`. Pero a mes a mes hauriem d'afegir un index BRIN sobre `ts` per a consultes temporals rapides. Es a dir, moltes mes estructures de suport.

A InfluxDB, la compressio automatica i l'indexacio per temps es gratuïta. A PostgreSQL, has de tunar molt be la BD per obtenir un rendiment equivalent.

---

## Pregunta 10 (oberta): Retencio i downsampling per 5 anys

**Resposta model**:

Per guardar 5 anys de dades de sensors sense ocupar 500 GB, la estrategia es **multi-nivell amb downsampling progresiu**:

1. **Nivell 0 - Raw (alta frequencia)**: retencio 30 dies. Tot el que arriba del sensor (cada 5 min). Ocupa molt pero es recent i detallat.

2. **Nivell 1 - Downsample 1 hora**: retencio 1 any. Cada hora, una task Flux calcula la mitjana, min, max de cada camp raw i ho guarda al bucket `hort-osona-downsampled`. 1 punt/hora en lloc de 12/hora. 12x menys espai.

3. **Nivell 2 - Downsample 1 dia**: retencio 5 anys. Cada dia, una task agafa les mitjanes horaries i calcula la mitjana diaria. 1 punt/dia en lloc de 288. 288x menys espai.

**Calcul per a 5 sensors a 5 min**:

- Raw: 5 sensors × 12 punts/h × 24 h × 30 d = 43.200 punts. Amb ~30 bytes/punt comprimit = 1.3 MB. Trivial.
- Downsample 1h: 5 sensors × 1 punt/h × 24 h × 365 d = 43.800 punts/any. 1.3 MB/any. Perfecte.
- Downsample 1d: 5 sensors × 1 punt/d × 365 d × 5 anys = 9.125 punts. 0.3 MB per 5 anys. Ridícul.

En total, 5 anys de dades ocuparien menys de **5 MB**. L'estalvi es aclaparador: sense downsampling serien 50 MB raw × 5 anys = 250 MB. Pero el downsampling fa que les dades antigues ocupin menys, i les consultes sobre dades agregades son mes rapides perquè hi ha menys punts.

**Tasks necessaries**:

```flux
// Cada hora, downsample a 1h
option task = {name: "ds_1h", every: 1h, offset: 5m}
from(bucket: "hort-osona")
  |> range(start: -1h, stop: now())
  |> filter(fn: (r) => contains(value: r._measurement, set: ["miflora", "bme"]))
  |> aggregateWindow(every: 1h, fn: mean, createEmpty: false)
  |> to(bucket: "hort-osona-1h", org: "bernatlab")

// Cada dia, downsample a 1d
option task = {name: "ds_1d", every: 1d, offset: 1h}
from(bucket: "hort-osona-1h")
  |> range(start: -1d, stop: now())
  |> filter(fn: (r) => contains(value: r._measurement, set: ["miflora_1h", "bme_1h"]))
  |> aggregateWindow(every: 1d, fn: mean, createEmpty: false)
  |> to(bucket: "hort-osona-1d", org: "bernatlab")
```

Aixo es l'estrategia que fem servir a l'Hort Osona. Ens permet tenir **5 anys d'historic** per a analisis estacionals amb un cost d'emmagatzematge minim.

---

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum, sobretot la part de model de dades.
- **3-4 encerts**: Repassar la diferencia entre tags i fields.
- **0-2 encerts**: Comencem pel basic: quina es la diferencia entre una BD relacional i una TSDB.

## Que fer si has encertat totes

- Passa al **Capitol 7** (API REST amb Flask).
- Investiga Telegraf com a collector universal per a InfluxDB.
- Compara InfluxDB amb TimescaleDB (l'extensio time-series de PostgreSQL).
- Apren a usar `influxctl` o el client CLI per a scripting.
- Prova la integracio amb Apache Superset per a BI.
