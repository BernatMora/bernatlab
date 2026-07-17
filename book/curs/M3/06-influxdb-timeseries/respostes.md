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

## Pregunta 11 (oberta): Per que Flux en lloc dInfluxQL

**Resposta model**:

InfluxDB va introduir el llenguatge **Flux** a la versio 2.0 (2020) substituint el classic **InfluxQL**. Aixo va ser una decisio polèmica amb avantatges i inconvenients:

**Per que Flux**:

**1. Consultes mes potents**:

Flux permet coses que InfluxQL no podia:
- **Joins** entre measurements: pots creuar dades de temperatura amb humitat a la mateixa consulta.
- **Matematica complexa**: derivades, integrals, regressions.
- **Manipulacio de strings**: procesar noms de sensors.
- **Pipelines**: chaining de operadors com en programacio funcional.

Exemple Flux:
```flux
from(bucket: "hort")
  |> range(start: -1h)
  |> filter(fn: (r) => r._measurement == "temperatura")
  |> map(fn: (r) => ({r with temperatura_f: r._value * 9/5 + 32}))
```

**2. Consistència amb altres eines**:

Flux te una sintaxis mes propera a JavaScript o Rust, llenguatges moderns. La gent jove el troba mes natural.

**3. Preparacio per al futur**:

InfluxDB v3 (en desenvolupament) usara **Arrow Flight** i **SQL** com a alternatives a Flux. Pero Flux sha quedat com a aposta de mig termini.

**Inconvenients**:

1. **Corba daprenentatge alta**: gent acostumada a SQL o InfluxQL ha d'aprendre una sintaxi nova.
2. **Documentacio menys abundant**: hi ha menys tutorials de Flux que de SQL.
3. **Mes lent per a consultes simples**: Flux te overhead de parseig que InfluxQL no te.
4. **No es estandard**: nomes serveix per InfluxDB, a diferencia de SQL.

**Impacte al BernatLab**:

Si estas començant:
- **Apren Flux directament**: sera la inversio a futur.
- **O utilitza InfluxQL si nomes necessites coses basiques**: mes simple.

**Cas real al BernatLab**:

Per a grafiques basiques (mitjana per hora d'una sensor), tant InfluxQL com Flux funcionen. Pero si vols fer alguna cosa mes complexe, com correlacio entre temperatura i humitat, nomes Flux te la capacitat.

```flux
// Correlacio entre temperatura i humitat les ultimes 24h
t = from(bucket: "hort")
  |> range(start: -24h)
  |> filter(fn: (r) => r._measurement == "temperatura")
  |> mean()

h = from(bucket: "hort")
  |> range(start: -24h)
  |> filter(fn: (r) => r._measurement == "humitat")
  |> mean()

join(tables: {t: t, h: h}, on: ["_time"])
  |> map(fn: (r) => ({r with correlacio: r._value_t - r._value_h}))
```

Aixo es impossible amb InfluxQL.

**Conclusio**: Flux es el futur dInfluxDB. A curt termini, InfluxQL es mes facil. A llarg termini, Flux dona mes potencia. La decisio depen de quant de temps tens per invertir en aprenentatge.

---

## Pregunta 12 (oberta): Cardinalitat i memoria RAM

**Resposta model**:

La **cardinalitat** (número de series uniques) es el parametre mes critic per al rendiment d'InfluxDB. Al BernatLab, entendre-ho es fonamental per evitar sorpreses.

**Que es la cardinalitat**:

Una serie es una combinacio de (measurement, tags). Per exemple:
- Measurement: `temperatura`
- Tags: `sensor_id=1, ubicacio=bancal-1`
- Es una serie.

Si tens 100 sensors x 50 tags cadascun (per exemple: sensor_id, ubicacio, marca, model, firmware, etc), tens 100 x 50 = **5000 series** (combinacions possibles).

**Impacte en memoria**:

InfluxDB mante un **index en memoria** de totes les series. A mesura que la cardinalitat creix, el index creix. La regla empirica es:

- **100k series**: 1-2 GB RAM.
- **1M series**: 8-12 GB RAM.
- **10M series**: 64+ GB RAM.

**Cas real al BernatLab**:

Si tens 100 sensors amb aquesta configuracio:
- `sensor_id` (100 valors)
- `ubicacio` (5 valors)
- `tipus_sensor` (3 valors: temperatura, humitat, llum)
- `marca` (4 marques)
- `firmware` (5 versions)

Cardinalitat = 100 x 5 x 3 x 4 x 5 = **30.000 series**.

Aixo son uns 500 MB de RAM nomes per l'index. Acceptable per a una RPi 4 de 4 GB, pero ja considerable.

**Riscos de cardinalitat explosiva**:

Un error comu es ficar camps d'alta cardinalitat com a tag:
- `timestamp_ns` (nanosegons del timestamp): 1 milio de valors.
- `usuari_id` (si tens molts usuaris): 1 milio.
- `request_id` (UUID per cada request): infinites.

Aixo pot passar si el teu codi afegeix aquests camps com a tag. El resultat es InfluxDB consumint tota la RAM i el sistema caure.

**Bones practiques**:

1. **Auditar els tags regularment**: `SHOW TAG VALUES` per veure quants valors unics te cada tag.
2. **Evitar tags d'alta cardinalitat**: usa fields per aixo.
3. **Limitar el número de tags**: 3-5 tags per measurement es raonable.
4. **Monitoritzar memoria**: alerta si InfluxDB passa de X GB.

**Exemple al BernatLab**:

```sql
-- Be: pocs valors
sensor_id: 1, 2, 3, ..., 100
ubicacio: bancal-1, bancal-2, ...

-- Dolent: alta cardinalitat
timestamp_ns: 1697000000000000, 1697000001000000, ...
usuari: anna, pere, joan, maria, ...
```

**Conclusio**: la cardinalitat es la metrica mes important a monitoritzar. Si creix sense control, InfluxDB consumira tota la RAM del sistema. Sigues conscient de quants tags tens i quants valors unics pot tenir cadascun.

---

## Pregunta 13 (oberta): InfluxDB nomes per grans volums?

**Resposta model**:

El company que diu "InfluxDB es nomes per a grans volums, per a 5 sensors nhi ha prou amb un fitxer CSV" te una visio que te part de raons pero ignora molts avantatges:

**Avantatges dInfluxDB inclús per a pocs sensors**:

1. **Consultes temporals natives**: amb CSV, has de carregar tot el fitxer, filtrar, agregar. Amb InfluxDB, la consulta es instantania.

```flux
from(bucket: "hort")
  |> range(start: -7d)
  |> filter(fn: (r) => r._measurement == "temperatura")
  |> aggregateWindow(every: 1h, fn: mean)
```

Amb CSV, hauries de fer un script Python amb pandas, carregar el CSV, filtrar, agrupar. Triga mes i es menys elegant.

2. **Integracio amb Grafana**: Grafana es el estandard de facto per visualitzacio. InfluxDB te integracio nativa. Amb CSV, hauries de fer un script de conversio.

3. **API nativa**: qualsevol aplicacio pot fer consultes HTTP a InfluxDB. Amb CSV, cada app ha de reinventar la roda.

4. **Compressio automatic**: InfluxDB comprimeix les dades (pot ser 10x mes petit que CSV).

5. **Retencio i downsampling**: politiques automatiques de quant temps guardar les dades raw. Amb CSV, totes les files creixen igual.

6. **Consultes concurrents**: multiples usuaris o aplicacions poden consultar alhora. Amb CSV, nomes un proces pot llegir a la vegada.

**Cas concret al BernatLab amb 5 sensors**:

5 sensors x 1 lectura/min x 60 min x 24 h x 365 dies = **2.628.000 lectures/any**.

Aixo es un CSV de ~250 MB/any. A 5 anys: 1.25 GB. Es manejable, pero:
- Obrir aquest CSV a Excel es lent.
- Filtrar per data es lent.
- Fer agregacions (mitjana per hora) es lent.
- Comparet amb InfluxDB: ~50 MB comprimit, consultes en ms.

**Pero tambe es veritat que**:

Si nomes tens 5 sensors i mires les dades un cop al mes, potser CSV es suficient. Pero si vols:
- Alertes automatic (temperatura > 30 graus).
- Comparatives entre períodes.
- Grafiques en temps real.
- Integracio amb Grafana.

...aleshores InfluxDB es la resposta correcta.

**Conclusio al company**: InfluxDB no es nomes "per a grans volums". Es una eina optimitzada per a **series temporals**, independentment del volum. Inclús amb 5 sensors, els beneficis en consultes, integracio i manteniment justifiquen la complexitat adicional.

**Sweet spot al BernatLab**:
- **1-2 sensors, hobby pur**: CSV o SQLite.
- **3-10 sensors, visualitzacio**: InfluxDB + Grafana.
- **10-100 sensors, dashboard sofisticat**: InfluxDB + Grafana + alertes.
- **100+ sensors, analisi**: InfluxDB + Kapacitor o similar.

---

## Pregunta 14 (oberta): Esquema InfluxDB per a l'hort IoT

**Resposta model**:

Per a 10 sensors (temperatura, humitat, llum, etc) que envien lectures cada 30 segons via MQTT, un esquema InfluxDB optimitzat seria:

**Decisions de disseny**:

**1. Un measurement per tipus o un per tot?**:

Recomano **un measurement per tipus** per aquesta escala:
- `temperatura` (5 sensors)
- `humitat` (3 sensors)
- `llum` (2 sensors)

Avantatges:
- Consultes mes rapides (l'index es mes petit per measurement).
- Millor compressio (les dades del mateix tipus es comprimeixen millor).
- Mes clar semanticament.

**2. Que va com a tag vs field**:

**Tags (indexats, per a agrupar/filtrar)**:
- `sensor_id` (identificador unic: "temp-01", "temp-02")
- `ubicacio` ("bancal-1", "bancal-2", " hivernacle")
- `tipus_unitat` (redundant amb measurement pero pot ser util)

**Fields (valors numerics, per a calcular)**:
- `valor` (el valor real de la lectura)
- `unitat` (pot ser tag si vols agregar per unitat)

**3. Schema concret**:

```sql
-- Mesurament: temperatura
-- Tags: sensor_id, ubicacio
-- Fields: valor (graus Celsius)
-- Timestamp: automatic dInfluxDB

-- Exemple de linia:
temperatura,sensor_id=temp-01,ubicacio=bancal-1 valor=22.5 1697000000000000000
```

**4. Vida esperada**:

- 10 sensors x 1 lectura cada 30s = 20 lectures/segon = **1.728.000 lectures/dia**.
- A 100 bytes/lectura = **172 MB/dia** = **63 GB/any** en cru.
- InfluxDB comprimeix ~10x: **6 GB/any**.
- En 5 anys: **30 GB**. Encara acceptable per una RPi amb SSD.

**Indexacio**:

Els tags creen series. Cardinalitat:
- 10 sensors x 5 ubicacions = **50 series** per measurement.
- 3 measurements = 150 series totals.
- Excel·lent per a rendiment.

**Consultes tipiques**:

```flux
// Temperatura actual del bancal-1
from(bucket: "hort")
  |> range(start: -5m)
  |> filter(fn: (r) => r._measurement == "temperatura")
  |> filter(fn: (r) => r.ubicacio == "bancal-1")
  |> last()

// Mitjana de temperatura per hora de tots els sensors
from(bucket: "hort")
  |> range(start: -24h)
  |> filter(fn: (r) => r._measurement == "temperatura")
  |> aggregateWindow(every: 1h, fn: mean)

// Sensors amb temperatura > 30 graus
from(bucket: "hort")
  |> range(start: -1h)
  |> filter(fn: (r) => r._measurement == "temperatura" and r._value > 30)
```

**Politiques de retencio**:

Aplica downsampling automatic:
- 30 dies raw (totes les lectures).
- 1 any amb agregacio horaria (mitjana, max, min).
- 5 anys amb agregacio diaria.

```flux
// Task d'agregacio cada hora
option task = {name: "downsample_1h", every: 1h}

from(bucket: "hort_raw")
  |> range(start: -1h)
  |> filter(fn: (r) => r._measurement == "temperatura")
  |> aggregateWindow(every: 1h, fn: mean, createEmpty: false)
  |> to(bucket: "hort_1h")
```

**Recomanacio al BernatLab**:

- Aquest esquema funciona per a 10-50 sensors.
- Si creixes a 100+ sensors, considera la particio per temps o altres optimitzacions.
- Important: fer backups regulars amb `influx backup`.

---

## Pregunta 15 (oberta): InfluxDB i sostenibilitat a llarg termini

**Resposta model**:

InfluxData (lempresa darrere dInfluxDB) ha fet canvis importants al llarg dels anys que plantegen reptes de sostenibilitat. Analitzem el context:

**Historia recents**:

- **InfluxDB 1.x** (2014-2020): versio estable, open source, amb InfluxQL.
- **InfluxDB 2.x** (2020-actualitat): canvis breaking, nou llenguatge Flux, focus en cloud.
- **InfluxDB 3.x** (en desenvolupament): reescritura completa amb Arrow i SQL.

**Canvis que afecten la sostenibilitat**:

1. **InfluxDB 1.x a 2.x**: cal reescriure totes les consultes. Les dades es poden migrar amb eines pero no es automatic.
2. **InfluxDB 2.x a 3.x**: encara mes canvis. La comunitat esta esperançada pero tambe nerviosa.
3. **Focus en cloud**: InfluxDB Cloud es el negoci principal. La versio open source cada vegada te mes limitacions.

**Riscos al BernatLab**:

1. **Aplicacio queda obsoleta**: si la versio open source es discontinuada, cal migrar.
2. **Canvis breaking**: actualitzar pot requerir reescriure codi.
3. **Documentacio canviant**: tutorials antics poden no aplicar.
4. **Alternatives que pugen**: TimescaleDB, QuestDB, Prometheus son alternatives.

**Com mitigar**:

1. **Usar tags** (InfluxDB 2.x) en lloc dInfluxQL. Es el futur.
2. **Documentar les teves consultes**: aixi pots migrar-les mes rapid.
3. **Exportar dades regularment**: CSV o Parquet. Encara que InfluxDB mori, tens les dades.
4. **Considerar alternatives**:
   - **TimescaleDB**: extensio de PostgreSQL, mes estable.
   - **QuestDB**: open source pur, SQL natiu.
   - **Prometheus**: si el teu cas dus es mes de monitoring que de series temporals.

**Argument a favor de continuar amb InfluxDB**:

- Gran ecosistema de clients i eines.
- Grafana funciona perfectament.
- Molta gent lusa, per tant la comunitat es forta.
- InfluxData encara dona suport a la versio OSS.

**Argument per canviar a TimescaleDB**:

- Es PostgreSQL, que ja coneixes.
- SQL estandard, no llenguatge propietari.
- Combinar dades de sensors amb altres dades (Nextcloud, Gitea) en una sola BD.
- Replicacio i backup mes robustos.

**La meva recomanacio al BernatLab**:

- Si tens 5-10 sensors i vols resultats rapids: **continua amb InfluxDB**.
- Si tens mes de 20 sensors o vols un sistema mes robust: **considera TimescaleDB**.
- Si ja tens PostgreSQL per a altres coses: **TimescaleDB te sentit**.

**Conclusio**: InfluxDB es una bona eina pero no es immortal. Tingues un pla B (export de dades) i sigues conscient de quan pot ser necessari migrar.

---

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum, sobretot les seccions de series temporals i downsampling.
- **3-4 encerts**: Rellegeix el capitol amb atencio. Investiga exemples de Flux al web.
- **0-2 encerts**: Repassem junts el capitol. Es la base per a Grafana.

## Que fer si has encertat totes

- Passa al **Capitol 7** (gestio de fitxers).
- O fes l'**exercici practic** amb mes sensors i configuracio de downsampling.
