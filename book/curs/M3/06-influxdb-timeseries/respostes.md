# Respostes — Capitol 6: InfluxDB per a dades de sensors

> Mira les respostes DESPRES d'haver fet el qüestionari.

## Pregunta 1: Que significa TSDB?

**Resposta correcta**: Time Series DataBase.

**Explicacio**: TSDB = Time Series DataBase. Es una categoria especifica de base de dades optimitzada per emmagatzemar i consultar dades indexades per temps. Exemples: InfluxDB, TimescaleDB, Prometheus, QuestDB, etc. Son disseny des de zero per al cas de "una lectura cada X segons, durant anys".

---

## Pregunta 2: Dades optimitzades

**Resposta correcta**: Series temporals (lectures de sensors amb timestamp).

**Explicacio**: InfluxDB esta optimitzada per a **series temporals**: dades amb un component temporal (timestamp) i uns quants valors numerics. La seva estructura interna emmagatzema les dades en blocs comprimits per temps, cosa que fa que les consultes per rang temporal siguin molt rapides. Altres tipus de dades (documents JSON, grafs, etc.) no son el seu fort.

---

## Pregunta 3: Lectures per any (cada minut)

**Resposta correcta**: 525.600.

**Explicacio**: 
- 1 lectura/minut = 60 lectures/hora
- 60 × 24 = 1.440 lectures/dia
- 1.440 × 365 = **525.600 lectures/any**

Aixo es el volum d'UN sol sensor. Imagina 50 sensors: 26 milions de files/any. Per aixo cal una base de dades especifica, no una BD tradicional.

---

## Pregunta 4: Nom de "taula" a InfluxDB

**Resposta correcta**: Measurement.

**Explicacio**: A InfluxDB, l'equivalent a una "taula" SQL es un **measurement** (mesura). Exemples: `temperatura`, `humitat`, `pressio`. Es una mica diferent perque cada fila pot tenir camps (fields) diferents dins del mateix measurement, pero a la practica funciona com una taula.

---

## Pregunta 5: Tags vs fields

**Resposta correcta**: Tags son metadades indexades; fields son els valors.

**Explicacio**:
- **Tags**: metadades que es repeteixen i que vols filtrar/agrupar sovint (sensor, ubicacio, etc.). Son **indexats** internament, per la qual cosa les consultes per tag son rapides. Limitats a strings.
- **Fields**: els valors numerics reals (temperatura, humitat, etc.). **No** son indexats per defecte (encara que es poden indexar manualment). Es on van les lectures.

Exemple: `temperatura,sensor=t1,ubicacio=hivernacle value=22.5`
- Tags: `sensor`, `ubicacio` (indexats)
- Fields: `value` (no indexat)

---

## Pregunta 6: Llenguatge de consultes v2

**Resposta correcta**: Flux.

**Explicacio**: **Flux** es el llenguatge de consultes d'InfluxDB v2. Es funcional (pipes `|>`) i orientat a series temporals. Sembla una mica a jq o APL. La v1 feia servir **InfluxQL** (similar a SQL), pero a v2 es considera deprecated. Al BernatLab he actualitzat a Flux per normalitzar amb Grafana.

---

## Pregunta 7: Port per defecte

**Resposta correcta**: 8086.

**Explicacio**: El port HTTP d'InfluxDB es 8086 (API i UI). Es pot canviar, pero 8086 es el estandard. Al BernatLab l'he mapeig a `127.0.0.1:8086` per seguretat (nomes accessible localment o via Tailscale).

---

## Pregunta 8: Backup consistent

**Resposta correcta**: `influx backup /tmp/backup`.

**Explicacio**: L'ordre `influx backup` es l'eina oficial per fer backups consistents. Funciona tant per a v1 com per a v2 (canvia la sintaxi). Fa un snapshot de tots els buckets, mesures i tasques. **Mai** facis `tar` del directori de dades d'InfluxDB actiu: el backup quedara inconsistent.

---

## Pregunta 9 (oberta): InfluxDB vs PostgreSQL per sensors

**Resposta model**:

Un sensor que escriu cada 10 segons genera **8.640 lectures/dia = 3,15 milions/any**. Amb 10 sensors son **31,5 milions/any**. Aixo es MOLT.

**A PostgreSQL**:
- Cada fila ocupa uns 200-300 bytes (taula, index, WAL, etc.).
- 31,5 milions × 300 bytes = **~9 GB/any** nomes en dades.
- Els indexs B-tree per timestamp creixen mes rapid i ocupen mes espai.
- Les consultes d'agregacio ("mitjana per hora") llegeixen moltes files, encara que estiguin indexades.
- Cal VACUUM periodic, ANALYZE, i altres manteniments.
- L'espai en disc a la SD/SSD s'exhaurira rapid.

**A InfluxDB**:
- Compressio nativa: les lectures iguals s'agrupen i comprimeixen (~10-20x).
- Estructura en blocs per temps: les consultes per rang temporal llegeixen nomes els blocs necessaris.
- Politiques de retencio automatiques: les dades velles s'esborren soles.
- Downsample automatic: les dades velles es resumeixen (mitjana per hora, maxim per dia) sense perdre informacio agregada.

**Tambe te inconvenients**: InfluxDB es menys flexible per a JOINs i consultes ad-hoc. Si necessites dades **diferents** a series temporals (relacions, transaccions), millor PostgreSQL. Pero per a **aquest cas d'us especific** (moltes lectures, consultes per temps), InfluxDB es 10-100x mes efficient.

**Conclusio**: per a 31,5 milions de files/any de series temporals, InfluxDB es la opcio correcta. PostgreSQL pot funcionar pero sera lent, ocupara molt d'espai, i necessitara manteniment.

---

## Pregunta 10 (oberta): 50 sensors cada 5 segons, 2 anys

**Resposta model**:

**Calcul del volum**:
- 50 sensors × 1 lectura / 5 segons = 10 lectures/segon
- 10 × 60 = 600 lectures/minut
- 600 × 60 = 36.000 lectures/hora
- 36.000 × 24 = 864.000 lectures/dia
- 864.000 × 365 = **315,4 milions de lectures/any**
- En 2 anys: **630,8 milions de lectures**

**Espai en disc**:
- InfluxDB comprimeix molt be les dades numeriques. ~1-2 bytes per valor numeric.
- Suposant 2 fields per lectura (ex: temperatura + humitat): 4 bytes + overhead (~20 bytes/lectura).
- 630 milions × 20 bytes = **~12 GB** comprimit. Pot ser menys (5-8 GB) si els valors son repetitius.

**RAM per consultes**:
- Per a consultes d'agregacio, InfluxDB carrega blocs en memoria.
- 1-2 GB de RAM son raonables per a aquest volum.

**Estrategia de retencio amb downsampling**:

1. **Bucket `hort_raw`**: guarda TOTES les lectures originals durant 30 dies.
2. **Bucket `hort_1h`**: consulta continua que agrega per hora i guarda durant 1 any.
3. **Bucket `hort_1d`**: consulta continua que agrega per dia i guarda durant 5 anys.

Exemple de consulta continua (Flux task):

```flux
// Cada hora, agrega les lectures del darrer hora
option task = {
  name: "downsample-1h",
  every: 1h
}

from(bucket: "hort_raw")
  |> range(start: -1h)
  |> filter(fn: (r) => r._measurement == "temperatura")
  |> aggregateWindow(every: 1h, fn: mean, createEmpty: false)
  |> to(bucket: "hort_1h", org: "bernatlab")
```

**Espai total estimat**:
- 30 dies raw: ~150 MB comprimit
- 1 any per hora: 24 × 365 = 8.760 files × 2 sensors = ~17.520 files/any = **~5 MB**
- 5 anys per dia: 365 × 5 = 1.825 files × 2 sensors = ~3.650 files = **~1 MB**

**Total**: ~150 MB de raw + ~6 MB d'agregats = **~156 MB per a 2 anys**. 

Aixo es la magia d'InfluxDB: 630 milions de lectures comprimits en pocs centenars de MB, amb consultes rapidissimes a qualsevol nivell d'agregacio.

---

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum, sobretot les seccions de series temporals i downsampling.
- **3-4 encerts**: Rellegeix el capitol amb atencio. Investiga exemples de Flux al web.
- **0-2 encerts**: Repassem junts el capitol. Es la base per a Grafana.

## Que fer si has encertat totes

- Passa al **Capitol 7** (gestio de fitxers).
- O fes l'**exercici practic** amb mes sensors i configuracio de downsampling.
