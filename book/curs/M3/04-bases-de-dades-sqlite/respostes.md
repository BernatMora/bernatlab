# Respostes — Capitol 4: Bases de dades SQLite

> Mira les respostes DESPRES d'haver fet el qüestionari.

## Pregunta 1: Quin tipus de base de dades es SQLite?

**Resposta correcta**: Emmagatzemada en un sol fitxer .db o .sqlite.

**Explicacio**: SQLite es una base de dades **embeguda** (embedded). No hi ha cap servidor separat: la base de dades sencera es un sol fitxer al disc. Això la fa molt facil de fer backup (nomes cal copiar el fitxer) i molt adequada per a aplicacions petites. En contrast, PostgreSQL o MySQL son client-servidor: hi ha un servei que escolta en un port, i les aplicacions s'hi connecten per xarxa.

---

## Pregunta 2: Limit practic de SQLite

**Resposta correcta**: Al voltant d'1 TB (pero va millor amb menys).

**Explicacio**: Segons la documentacio oficial, SQLite pot gestionar bases de dades fins a **140 TB** teorics, pero el rendiment comença a degradar-se a partir d'uns quants GB. El sweet spot es menys d'1 GB. Al BernatLab les BD SQLite solen ser d'uns quants MB (registres de configuracio, historial de logs, etc.).

---

## Pregunta 3: Navegador grafic

**Resposta correcta**: DB Browser for SQLite.

**Explicacio**: **DB Browser for SQLite** (anteriorment SQLite Browser) es una eina grafica multiplataforma que permet veure l'esquema, les dades, fer consultes, i exportar. Es perfecta per a l'hort IoT perque no requereix cap servidor. Alternatives: `sqlite-web` (un servidor web lightweight) o simplement la linia de comandes.

---

## Pregunta 4: Backup consistent

**Resposta correcta**: `sqlite3 db.db .dump > backup.sql`.

**Explicacio**: L'ordre `.dump` genera un fitxer SQL pla amb totes les sentencies CREATE i INSERT necessaries per reconstruir la base de dades. Es l'equivalent a `pg_dump` per a SQLite. El resultat es un .sql que es pot restaurar amb `sqlite3 db.db < backup.sql`. Tambe es pot fer backup nomes copiant el .db si la BD no esta sent modificada (pero `.dump` sempre es consistent).

---

## Pregunta 5: Avantatge principal de SQLite

**Resposta correcta**: No necessita servidor, es un sol fitxer.

**Explicacio**: SQLite no requereix cap instal·lacio de servidor ni configuracio. Es una llibreria que la teva aplicacio enllaça. La BD es un fitxer al disc, facil de copiar, moure, fer backup. Es la BD mes usada del mon (esta a tots els Android, iOS, navegadors, etc.). En canvi, PostgreSQL requereix un servidor corrent, configuracio de xarxa, autenticacio, etc.

---

## Pregunta 6: Mode de journaling mes segur

**Resposta correcta**: WAL (Write-Ahead Log).

**Explicacio**: El mode **WAL** (Write-Ahead Log) es el mes modern i robust. Permet lectures i escriptures concurrents (millor rendiment) i es mes resistent a corrupcions per talls de llum. Al BernatLab activo WAL a totes les BD SQLite que son importants: `PRAGMA journal_mode=WAL;`.

---

## Pregunta 7: Extensio de fitxer

**Resposta correcta**: .db, .sqlite, .sqlite3.

**Explicacio**: Totes tres son valides i es poden intercanviar. La mes comuna es `.db` (la mes curta) o `.sqlite` (la mes descriptiva). SQLite es "tipo-tolerant" amb les extensions: no li importa quina faci servir, el que importa es el contingut.

---

## Pregunta 8: Cas NO adequat per a SQLite

**Resposta correcta**: Una botiga online amb 1000 usuaris concurrents.

**Explicacio**: SQLite te un **lock global**: nomes una escriptura a la vegada a tota la BD. Si tens 1000 usuaris fent comandes, hi hauran cues i timeouts. PostgreSQL pot gestionar milers de connexions concurrents. SQLite es per a aplicacions amb poques escriptures concurrents (un sol usuari, o un sol script periodica).

---

## Pregunta 9 (oberta): Quan SQLite vs PostgreSQL

**Resposta model**:

**SQLite** es la millor opcio quan:
- Tens **poques escriptures concurrents** (un sol script, una sola app).
- La BD es **petita** (menys d'1 GB).
- No necessites **replicacio** ni alta disponibilitat.
- Vols **simplicitat** (no vols mantenir un servidor).
- Les dades son **locals** a una maquina.

Exemples al BernatLab:
- Historial de tasques programades (cron logs).
- Registres de configuracio dels serveis.
- Notes personals i quadern de camp.
- Cache de consultes de Grafana.
- Metadades petites de sensors (nom, ubicacio, calibracio).

**PostgreSQL** es la millor opcio quan:
- Tens **moltes escriptures** concurrents (multiples usuaris, scripts, app web).
- La BD creix **mes enlla d'1-5 GB**.
- Necessites **consultes complexes** (JOINs de moltes taules, agregacions).
- Vols **replicacio** o alta disponibilitat.
- Cal **transaccions ACID** rigoroses (integracio financera, per exemple).

Exemples al BernatLab:
- Dades de sensors de l'hort (moltes lectures per segon).
- Inventari de plantes i collites.
- Registres meteorologics historics.
- Logs d'auditoria.

**Regla practica**: si la teva aplicacio nomes hi ha un sol "actor" escrivint, **SQLite**. Si hi ha mes d'un, **PostgreSQL**.

---

## Pregunta 10 (oberta): 8 GB de lectures, migrar?

**Resposta model**:

8 GB es al limit superior del que SQLite pot gestionar amb dignitat. No es que no funcioni, pero:
- Les consultes comencen a ser lentes (1-2 segons en lloc de mil·lisegons).
- Els backups amb `.dump` triguen mes (1-2 minuts comprimits).
- El risc de corrupcio augmenta lleugerament.

**Recomanacio: NO migrar automaticament**. Primer intenta:

1. **Netejar dades antigues**: segurament no necessites 5 anys de lectures. Les dades de fa 3 anys son historiques, pero les agregades (mitjanes diaries) son suficients. Esborra les lectures antigues, guarda les agregacions. La BD baixarà a 1-2 GB.
2. **Activa WAL i altres optimitzacions**: `PRAGMA journal_mode=WAL; PRAGMA synchronous=NORMAL;`
3. **Indexa correctament**: segurament ja ho tens, pero revisa els indexs.

Si despres de netejar segueix creixent (per exemple, tens 50 sensors i cada un escriu cada 10 segons = 5 files/segon = ~13 milions/mes), llavors **si, migra a PostgreSQL**. El cost es moderat (un parell d'hores) pero el benefici es clar:
- Millor rendiment amb milions de files.
- Consultes mes complexes i mes rapides.
- Replicacio si vols alta disponibilitat.
- Millor gestio de transaccions.

**Conclusio**: 8 GB de lectures pures es senyal de que la BD esta fent una feina que no es la seva. Primer neteja, despres avalua, i finalment migra nomes si cal.

---

## Pregunta 11 (oberta): Per que SQLite es la BD mes usada del mon

**Resposta model**:

SQLite es la base de dades mes utilitzada del mon (inclús mes que MySQL o PostgreSQL) per varies raons que sovint es passen per alt:

**1. Esta integrada a tot arreu**:

Cada telefon Android, cada Mac, cada Windows 10/11, cada navegador Chrome/Firefox, cada instancia de Python te SQLite. Son milers de milions de copies en dispositius. Aixo supera amb diferencia qualsevol altre base de dades.

**2. No cal configurar res**:

No hi ha servidor, no hi ha dimonis, no hi ha ports oberts. Es un sol fitxer. Pots usar-la amb una sola línea de codi en qualsevol llenguatge.

**3. Cumple el 80/20**:

Per al 80% dels casos d'us, SQLite es mes que suficient. No cal la potencia d'Oracle o PostgreSQL. La gent ho descobreix i l'adopta.

**4. Tests d'unitat**:

Es l'eina estandard per fer tests d'aplicacions. No cal aixecar un PostgreSQL nomes per testejar.

**5. Aplicacions embarques**:

Sistemes embeguts (IoT, dispositius medic, avions) usen SQLite per la seva petita mida i zero configuracio. Airbus, per exemple, la usa en alguns sistemes critics.

**6. Edge computing**:

Quan tens dades que es generen a ledge (sensors IoT, aplicacions mòbils), pujar-les a un núvol es costós i lent. SQLite permet processar-les localment.

**7. Maduresa i estabilitat**:

El codi de SQLite te mes de 20 anys de proves. Es una de les biblioteques de programari mes audidades del mon. Pocs bugs, alta fiabilitat.

**Lliço per al BernatLab**:

La lliço es clara: **no sempre necessites la tecnologia mes potent**. Al BernatLab:
- Per a l'hort IoT amb 5 sensors: SQLite es perfecte.
- Per a Nextcloud o Gitea: ja cal PostgreSQL per volum d'usuaris.
- Per a metriques de Grafana: InfluxDB (no SQLite).

La regla es: comença amb el mes simple (SQLite) i migra nomes quan cal. La migracio es cara (temps, risc), pero el canvi a mes potent es gratis.

**Analogia**: no compris un Ferrari per anar a comprar pa. Un bon bicicleta et porta igual de lluny amb mes salut i menys cost.

---

## Pregunta 12 (oberta): WAL i rendiment en escriptures

**Resposta model**:

El mode **WAL (Write-Ahead Log)** canvia fonamentalment com SQLite gestiona les escriptures i lectures concurrents. Aixo es particularment important al BernatLab amb sensors que escriuen constantment.

**Com funciona SQLite sense WAL (rollback journal)**:

1. Un proces vol escriure. Agafa un lock exclusiu.
2. Cap altre pot llegir ni escriure fins que sha fet el commit.
3. Si una lectura triga 5 segons, les escriptures esperen.
4. Si una escriptura triga 10 ms, les lectures esperen.

**Amb WAL**:

1. Un proces vol escriure. Afegeix al log WAL.
2. Les lectures poden continuar usant la versio antiga.
3. Periòdicament, WAL es "checkpointed" al fitxer principal.
4. Lectures i escriptures no es bloquegen entre si (en la majoria de casos).

**Impacte al BernatLab amb 10 sensors escrivint cada segon**:

- **Sense WAL**: 10 escriptures/segon serialitzades. Si cada escriptura triga 5 ms, es pot gestionar, pero les lectures pateixen.
- **Amb WAL**: 10 escriptures/segon en paral·lel amb lectures. Millor experiencia.

**Cas real al BernatLab**:

Tens una aplicacio web (Nextcloud o una API) que llegeix les dades dels sensors de SQLite per mostrar grafiques. Mentrestant, els sensors segueixen escrivint.

- Sense WAL: quan un sensor escriu, la web ha desperar. Grafiques amb delay.
- Amb WAL: la web llegeix la versio consistent mes recent sense delays.

**Activar WAL**:

```sql
PRAGMA journal_mode=WAL;
PRAGMA synchronous=NORMAL;  -- opcional, mes rapid pero menys segur
```

**Important**: WAL te un cost. Crea un fitxer `database.db-wal` a mes del principal. Cal fer backup tambe daquest fitxer, no nomes del principal.

**Limitacions de WAL**:

- WAL no funciona be en xarxes NFS (no es recomana).
- Si el sistema es penja entre un write a WAL i el checkpoint, el proper read fara automatic checkpoint. Pero cal `PRAGMA wal_checkpoint(TRUNCATE)` periòdicament.
- En bases de dades molt grans (>1 GB), WAL pot ser mes lent que el mode tradicional per certes operacions.

**Recomanacio al BernatLab**: activa WAL per defecte a totes les BD SQLite. El benefici en rendiment es clar i els inconvenients son minims per a casos tipics.

---

## Pregunta 13 (oberta): SQLite no es una BD de joguina

**Resposta model**:

El mite que "SQLite es una BD de joguina" es fals i pot fer que la gent esculli solucions mes complexes innecesariament. Casos reals on SQLite es la eleccio correcta:

**1. Aplicacions desktori milionaries**:

- **Firefox**: usa SQLite per guardar historial, marcadors, cookies, cache. Milions dusuaris.
- **Chrome**: igual que Firefox. Cada perfil es una BD SQLite.
- **Apple Photos**: la galeria de fotos de macOS i iOS usa SQLite per metadades.
- **Android**: cada app pot tenir la seva BD SQLite.

Son aplicacions amb milions dusuaris, altament optimitzades, que confien en SQLite.

**2. Embedded systems**:

- **Airbus A350**: usa SQLite en alguns sistemes de cabina.
- **Boeing 787**: igual.
- **Tesla**: usa SQLite en el sistema dinfotainment.
- **Sistemes militars**: per la seva petita mida i zero configuracio.

**3. Web apps petites i mitjanes**:

Moltes web apps amb milers dusuaris diaries usen SQLite amb exit:
- **Django** (framework Python): per defecte usa SQLite en desenvolupament, pero tambe en produccio per a molts casos.
- **WordPress** (parcialment): pot usar SQLite amb un plugin.
- **Moltes SaaS petites**: comencen amb SQLite i creixen a PostgreSQL nomes quan cal.

**4. Casos al BernatLab**:

- **Cataleg de plantes** (hortosona): 500 plantes, 20 atributs = perfecte per SQLite.
- **Blog personal**: 50 articles, 100 visites diaries = perfecte per SQLite.
- **App de notes local**: perfecte per SQLite.
- **Lector RSS**: perfecte per SQLite.
- **Calculadora de cultius**: perfecte per SQLite.

**Arguments tecnics a favor de SQLite**:

- **Atomicitat**: les transaccions son ACID. Mes robust que moltes BD.
- **Concurrencia**: amb WAL, mes rapid que MySQL en molts casos.
- **Fiabilitat**: zero perdua de dades en 20+ anys de proves.
- **Simplicitat**: un sol fitxer, zero administracio.

**Limitacions que SI cal reconeixer**:

- Concurrencia massiva (>100 escriptures/segon): limita.
- Replicacio nativa: no inclou.
- Consultes massivament paral·leles: no es el seu fort.
- Mes de 1 TB de dades: no es practic.

**Conclusio**: al BernatLab, per al 80% dels casos, SQLite es mes que suficient. No la descartis per prejudicis.

---

## Pregunta 14 (oberta): Esquema SQLite per a l'hort IoT

**Resposta model**:

Per a 5 sensors que escriuen lectures cada minut al BernatLab, un esquema SQLite optimitzat seria:

**Opcio A: Una sola taula per a tots els sensors**:

```sql
CREATE TABLE lectures (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sensor_id INTEGER NOT NULL,
    timestamp TEXT NOT NULL,  -- ISO 8601 UTC
    valor REAL NOT NULL,
    unitat TEXT,  -- 'C', '%', 'lux', etc.
    FOREIGN KEY (sensor_id) REFERENCES sensors(id)
);

CREATE INDEX idx_lectures_sensor_ts ON lectures(sensor_id, timestamp);
CREATE INDEX idx_lectures_ts ON lectures(timestamp);

CREATE TABLE sensors (
    id INTEGER PRIMARY KEY,
    nom TEXT NOT NULL,
    tipus TEXT NOT NULL,  -- 'temperatura', 'humitat', 'llum'
    ubicacio TEXT,  -- 'bancal-1', 'bancal-2', etc.
    actiu BOOLEAN DEFAULT 1
);
```

**Avantatges**: una sola consulta agafa tot. Facil d'agregar nous sensors.

**Opcio B: Una taula per tipus de sensor**:

```sql
CREATE TABLE temperatura (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sensor_id INTEGER NOT NULL,
    timestamp TEXT NOT NULL,
    valor REAL NOT NULL,  -- graus Celsius
    FOREIGN KEY (sensor_id) REFERENCES sensors(id)
);

CREATE TABLE humitat (...);
CREATE TABLE llum (...);
```

**Avantatges**: cada taula es petita, consultes optimitzades per tipus.

**Desventatges**: cal una consulta per tipus. Menys flexible.

**Indexacio**:

Per a les consultes tipiques "valor del sensor X en les ultimes 24 h":
- `CREATE INDEX idx_temp_sensor_ts ON temperatura(sensor_id, timestamp);`
- Permet cerques per rang de temps dun sensor en O(log n).

**Politica de retencio**:

```sql
-- Esborrar lectures mes antigues de 1 any
DELETE FROM lectures WHERE timestamp < datetime('now', '-1 year');
```

O usar **tables particionades per temps** (mes complicat pero mes rapid).

**Volum esperat**:

5 sensors x 1 lectura/min x 60 min x 24 h x 365 dies = 2.628.000 lectures/any. A 100 bytes/lectura = 263 MB/any. En 5 anys: 1.3 GB. Encara acceptable per SQLite.

**Backup**:

```bash
# Backup consistent amb sqlite3
sqlite3 /var/lib/bernatlab/hort.db ".backup /home/pi/backups/hort-$(date +%F).db"

# O exportar a SQL
sqlite3 /var/lib/bernatlab/hort.db .dump > /home/pi/backups/hort-$(date +%F).sql
```

**Optimitzacions**:

- `PRAGMA journal_mode=WAL;` per millorar concurrencia.
- `PRAGMA synchronous=NORMAL;` per millorar rendiment (menys segur pero acceptable).
- `VACUUM;` periodicament per netejar espai.
- Considerar movir a InfluxDB si es passa de 5 sensors o el volum creix.

---

## Pregunta 15 (oberta): Consequencies de SQLite nomes una escriptura a la vegada

**Resposta model**:

SQLite te una limitacio fundamental: nomes permet una escriptura a la vegada (sense WAL). Al BernatLab, cal entendre quan aixo es un problema i quan no.

**Com funciona el lock**:

Quan un proces vol fer un INSERT o UPDATE:
1. Agafa un lock exclusiu sobre tota la BD.
2. Fins que sha fet el commit, cap altre pot escriure.
3. Les lectures poden continuar (sobretot amb WAL).
4. Si dos processos intenten escriure alhora, un sha desperar.

**Impacte amb pocs sensors (cas BernatLab)**:

Amb 5 sensors escribint cada minut:
- Frequencia: 5 INSERT cada 60 segons = 1 cada 12 segons.
- Durada de cada INSERT: <10 ms.
- Probabilitat de colissio: molt baixa.
- L'usuari no nota res.

**Impacte amb molts sensors**:

Amb 100 sensors escribint cada segon:
- Frequencia: 100 INSERT per segon.
- Durada de cada INSERT: 5-10 ms.
- Temps total: 500-1000 ms per segon = 50-100% del temps.
- Colissions constants. Rendiment baixa molt.

**Solucions**:

**1. WAL**: permet paral·lelisme parcial. No elimina la limitacio, pero la millora.

**2. Aplicar batching**: en lloc de fer 1 INSERT per lectura, fer 1 INSERT per minut amb 60 lectures. Molt mes efficient.

**3. Canviar a una BD amb mes concurrencia**:
- **PostgreSQL**: suporta milers d'escriptures concurrents.
- **InfluxDB**: dissenyat especificament per series temporals.
- **TimescaleDB**: extensio de PostgreSQL per series temporals.

**4. Buffer intermedi**: usar un sistema de cues (MQTT, Redis) que reculli les dades i un sol proces les escrigui a SQLite en batches.

**Cas concret al BernatLab**:

Tens un hort amb 10 sensors que escriuen cada 30 segons:
- FreqUencia: 20 INSERT per minut.
- Triguen 0.5 ms cadascun: 10 ms total per minut = 0.017% del temps.
- Nomes hi hauria problemes amb 1000+ sensors.
- Per tant, SQLite es perfecte.

**Si creixes**:

Si passes a 100+ sensors, cada 5 segons:
- 1200 INSERT per minut.
- Probable saturacio.
- Cal canviar a InfluxDB o similar.

**Conclusio**: la limitacio de SQLite es important pero nomes arriba a ser un problema a escales grans. Al BernatLab amb pocs sensors, no es un problema. Pero cal saber que existeix per planificar el creixement.

---

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum.
- **3-4 encerts**: Rellegeix el capitol amb atencio, sobretot la seccio de "quan usar SQLite".
- **0-2 encerts**: Repassem junts el capitol. Es la base per als capitols de PostgreSQL i InfluxDB.

## Que fer si has encertat totes

- Passa al **Capitol 5** (PostgreSQL).
- O fes l'**exercici practic** amb mes dades per consolidar.
