# Respostes — Capitol 5: PostgreSQL basic

> Mira les respostes DESPRES d'haver fet el qüestionari.

## Pregunta 1: Quin tipus de BD es PostgreSQL?

**Resposta correcta**: Client-servidor.

**Explicacio**: PostgreSQL es una base de dades **client-servidor**. Hi ha un dimoni (`postgres`) que escolta en un port (5432 per defecte), i les aplicacions s'hi connecten. Aixo permet multiples connexions concurrents, autenticacio per usuari, i acces per xarxa. En canvi, SQLite es embeguda: nomes un sol proces hi pot accedir alhora.

---

## Pregunta 2: Client de linia de comandes

**Resposta correcta**: psql.

**Explicacio**: `psql` es el client oficial de PostgreSQL. Permet connectar-se a una BD, fer consultes, veure metadades, i executar scripts. Es interactiu (entra en un REPL) o no interactiu (amb `-c "..."` o amb `< script.sql`). Al BernatLab el faig servir sovint via `docker exec bernatlab-postgres psql ...`.

---

## Pregunta 3: Backup consistent

**Resposta correcta**: `pg_dump -U user db > backup.sql`.

**Explicacio**: `pg_dump` es l'eina estandard per fer backups logics de PostgreSQL. Llegeix la BD de manera consistent (independentment de l'activitat) i genera un script SQL que es pot restaurar amb `psql`. Comprimeix amb `gzip` per estalviar espai. Nomes mai facis `tar` del directori de dades mentre Postgres esta corrent: el backup quedara inconsistent.

---

## Pregunta 4: Tipus de dada per a dates

**Resposta correcta**: TIMESTAMPTZ.

**Explicacio**: `TIMESTAMPTZ` (timestamp with time zone) es el tipus recomanat. Internament PostgreSQL sempre emmagatzema la data en UTC, i nomes converteix a la zona horaria local quan la llegeixes. Aixi evites errors amb horari d'estiu, sensors a diferents paisos, etc. `TIMESTAMP` (sense TZ) nomes guarda la data "nua", i pot ser confusa.

---

## Pregunta 5: Connexions concurrents

**Resposta correcta**: Milers.

**Explicacio**: PostgreSQL esta dissenyat per a concurrencia. Pot gestionar milers de connexions simultanies amb un sol servidor. Cada connexio te el seu aïllament transaccional (MVCC). El limit es mes de memoria RAM i CPU que del propi Postgres. Una RPi 4 pot gestionar centenars de connexions sense problema per a una app tipus hort IoT.

---

## Pregunta 6: Port per defecte

**Resposta correcta**: 5432.

**Explicacio**: El port per defecte de PostgreSQL es 5432. Al BernatLab el mapeig a `127.0.0.1:5432` nomes localhost per seguretat. Si vols accedir des d'un altre ordinador, fes un túnel SSH o un Wireguard/Tailscale.

---

## Pregunta 7: Llistar taules a psql

**Resposta correcta**: `\dt`.

**Explicacio**: A `psql` les meta-ordres comencen amb `\` (invertida). `\dt` llistar totes les taules. Altres utils: `\dt+` amb mes info, `\d nom_taula` per descriure una taula, `\dn` per llistar esquemes, `\dv` per vistes, `\df` per funcions. Son abreujaments de les consultes a `information_schema`.

---

## Pregunta 8: Tipus JSON indexable

**Resposta correcta**: JSONB.

**Explicacio**: `JSONB` (JSON Binary) es la versio binaria de JSON. Ocupa menys espai, es mes rapid de processar, i es pot **indexar** amb GIN per a cerques rapides dins del JSON. `JSON` nomes emmagatzema el text, ocupa mes, i no es pot indexar igual de be. Al BernatLab faig servir JSONB per a configuracions flexibles.

---

## Pregunta 9 (oberta): Per que TIMESTAMPTZ?

**Resposta model**:

`TIMESTAMPTZ` (timestamp with time zone) es **millor** que `TIMESTAMP` (sense zona horaria) per varies raons:

**1. Evita errors d'horari d'estiu**: si tens un sensor que envia lectures durant la matinada, i a les 2 de la matinada toca canviar l'hora (2 -> 3), tens una hora "duplicada" o "perduda" amb `TIMESTAMP`. Amb `TIMESTAMPTZ` això no passa, perque tot s'emmagatzema en UTC.

**2. Suporta sensors a diferents zones horaries**: si tens un sensor a Barcelona (CET) i un altre a Tokyo (JST), i els dos envien la mateixa "data-hora local", no pots compararles. Amb `TIMESTAMPTZ`, tot s'emmagatzema en UTC, i pots comparar-les facilment.

**3. Internament Postgres ja ho fa be**: PostgreSQL SEMPRE emmagatzema els `TIMESTAMPTZ` en UTC, i nomes converteix a la zona horaria de la sessio quan els llegeixes. Per tant, `TIMESTAMPTZ` no ocupa mes espai que `TIMESTAMP` (de fet, una mica menys perque no guarda la TZ literal). Es totalment transparent.

**4. Permet consultes en qualsevol TZ**: pots fer `SELECT ts AT TIME ZONE 'Europe/Madrid'` per veure l'hora local, o `AT TIME ZONE 'UTC'` per mantenir-la en UTC.

**Conclusio**: SEMPRE usa `TIMESTAMPTZ` per a dates que representen un instant en el temps. Usa `TIMESTAMP` (sense TZ) nomes per a dates purament "calendari" com "data de plantacio" o "data de factura".

---

## Pregunta 10 (oberta): Blog personal

**Resposta model**:

Per a un blog personal amb 50.000 articles i 10.000 visites diaries, la meva recomanacio es **PostgreSQL**.

**Arguments a favor**:
- **Volum**: 50.000 articles amb text + imatges + metadades son facilment 500 MB - 2 GB de BD. Es massa per a SQLite.
- **Consultes**: un blog te moltes consultes (per categoria, per data, per etiqueta, cerques de text). Els indexos de PostgreSQL i el seu `full text search` brillen aqui.
- **Concurrencia**: 10.000 visites diaries amb pics de 100 visites/hora suposa moltes connexions. SQLite no aguanta.
- **SEO**: el temps de resposta es important. PostgreSQL es rapid en aquest volum.
- **Replicacio**: si vols alta disponibilitat, PostgreSQL te streaming replication nativa.

**Arguments a favor de SQLite**:
- **Simplicitat**: nomes un fitxer, facil de backupejar.
- **Rendiment en lectura**: si nomes tu escrius, SQLite es rapidissim en lectura.

**Conclusions**:
- Si el blog es **estatic** (pocs articles nous al mes, poc trafic), **SQLite es perfecte**.
- Si el blog es **dinamic** (escritura regular, moltes visites, comentaris), **PostgreSQL es millor**.
- Si tens mes de 100.000 articles o centenars de milers de visites, considera un **CDN** + un **headless CMS** o una solucio basada en **Next.js + Vercel** + **Vercel Postgres**.

**Alternativa especifica**: WordPress funciona molt be amb MySQL/MariaDB, pero jo personalment evitaria WordPress per un blog modern. Un generador estatic (Hugo, Eleventy) amb Markdown i desplegament a Netlify es molt mes rapid i segur.

---

## Pregunta 11 (oberta): Maduresa de PostgreSQL

**Resposta model**:

PostgreSQL sha mantingut com una de les bases de dades mes populars durant mes de 30 anys per varies raons que la fan especialment atractiva al BernatLab:

**1. Maduresa tecnologica**:

PostgreSQL es va iniciar el 1986 (com a projecte POSTGRES a Berkeley) i sha anat evolucionant de forma constant. Cada versio ha afegit funcionalitats noves sense perdre estabilitat. Les queries que escrius avui funcionaran d'aqui 10 anys.

**2. Compliment d'estandards**:

PostgreSQL es la base de dades mes propera a l'estandard SQL. Si aprens SQL per PostgreSQL, pots migrar a Oracle, SQL Server, MySQL amb poc esforc. La inversa no es certa.

**3. Extensibilitat**:

PostgreSQL permet definir nous tipus de dades, funcions, operadors. Aixo ha permès crear extensions com:
- **PostGIS**: geospatial (GIS).
- **TimescaleDB**: series temporals.
- **pg_trgm**: cerca difusa de text.
- **pgvector**: embeddings per IA.

Aixo converteix PostgreSQL en una mena de "Lego" de BD: comences amb la base i afegeixes el que necessites.

**4. Comunitat activa**:

Hi ha una enorme comunitat de desenvolupadors i usuaris. Si tens un problema, algú l'ha tingut abans i la solucio esta a StackOverflow, GitHub, o la documentacio oficial.

**5. Llicencia permissiva**:

PostgreSQL es completament open source (llicencia PostgreSQL, similar a BSD). Pots usar-lo comercialment sense pagar res. No hi ha cap "Enterprise Edition" amb funcionalitats tancades.

**Impacte al BernatLab**:

Aquesta maduresa te consequencies directes:
- **Garantia de futur**: el teu Nextcloud o Gitea seguiran funcionant d'aqui 10 anys.
- **Documentacio abundant**: milers de llibres, tutorials, videos.
- **Eines compatibles**: casi totes les eines modernes funcionen amb PostgreSQL.
- **Talent disponible**: si mai necessites ajuda, es facil trobar gent que en sap.

**Contraste amb alternatives**:

- **MongoDB**: popular pero amb canvis breaking sovint (que van trencar aplicacions).
- **Firebase**: propietat de Google, amb risc de lock-in.
- **SQLite**: fantastic pero nomes per a casos basics.
- **PostgreSQL**: equilibrat entre potencia, estabilitat, i comunitat.

**Conclusio**: triar PostgreSQL al BernatLab es una aposta segura a llarg termini. Es la base de dades que podem recomanar amb el coneixement que no desapareixera.

---

## Pregunta 12 (oberta): Indexos i rendiment

**Resposta model**:

Els indexos son la diferencia entre una base de dades rapidissima i una que es queda penjada. Al BernatLab, entendre com funcionen es fonamental.

**Com funcionen els indexos**:

Sense index, una consulta `SELECT * FROM lectures WHERE sensor_id = 5` ha de fer un **escaneig sequencial**: llegeix totes les files una per una buscant les que compleixen la condicio. Amb 1 milio de files, son 1 milio de comparacions.

Amb un index `CREATE INDEX idx_sensor ON lectures(sensor_id)`, PostgreSQL crea una estructura de dades (B-tree) que permet trobar totes les files amb `sensor_id = 5` en O(log n). Amb 1 milio de files, son ~20 comparacions. **50.000 vegades mes rapid**.

**Tipus d'indexos**:

- **B-tree (default)**: bones per igualtat (`=`) i rangs (`<`, `>`, `BETWEEN`).
- **Hash**: nomes per igualtat. Mes rapids que B-tree en teoria, pero menys utils.
- **GIN (Generalized Inverted Index)**: per arrays, JSONB, text complet.
- **GiST (Generalized Search Tree)**: per dades geospatials, text complet.

**Cas practic al BernatLab amb 1 milio de files**:

```sql
-- Sense index: ~5 segons
SELECT * FROM lectures WHERE sensor_id = 5 AND timestamp > '2024-01-01';

-- Amb index: ~0.001 segons
CREATE INDEX idx_sensor_ts ON lectures(sensor_id, timestamp);
SELECT * FROM lectures WHERE sensor_id = 5 AND timestamp > '2024-01-01';
```

**Pero els indexos tenen cost**:

1. **Espai en disc**: cada index ocupa espai addicional (~10-30% de la taula).
2. **Escriptura mes lenta**: cada INSERT/UPDATE ha d'actualitzar tambe l'index. Una taula amb 5 indexos pot ser 2-3 vegades mes lenta en escriptures.
3. **Manteniment**: cal `VACUUM` i `ANALYZE` periòdics per mantenir l'index optim.

**Regles d'or pels indexos**:

1. Indexa les columnes que uses sovint a `WHERE`.
2. Indexa les columnes que uses a `ORDER BY` si la consulta es lenta.
3. No indexis columnes amb pocs valors unics (com booleans).
4. No indexis columnes que canvien sovint (com timestamps).
5. Comprova amb `EXPLAIN ANALYZE` si el teu index s'utilitza.

**Exemple al BernatLab amb sensors**:

```sql
-- Bones indexos
CREATE INDEX idx_lectures_sensor_ts ON lectures(sensor_id, timestamp);
CREATE INDEX idx_lectures_ts ON lectures(timestamp);

-- Mal index (no aporta gaire)
CREATE INDEX idx_lectures_unitat ON lectures(unitat);  -- nomes hi ha 4-5 unitats possibles
```

**Conclusio**: els indexos son essencials pero no gratuits. Crea'ls per a les consultes que fas sovint, no per a tot. Usa `EXPLAIN ANALYZE` per verificar que shi utilitzen.

---

## Pregunta 13 (oberta): Quan pujar a PostgreSQL

**Resposta model**:

El company que diu "per que complicar-me amb PostgreSQL si SQLite ja em fa el fet" te raons per pensar aixi, pero al BernatLab hi ha casos clars on val la pena pujar:

**1. Mes usuaris concurrents**:

SQLite serialitza les escriptures. Si tens 10 usuaris intentant pujar fitxers a Nextcloud alhora, SQLite (la BD de Nextcloud) pot tenir cues. PostgreSQL pot gestionar centenars de connexions concurrents.

**2. Mes robustesa davant corrupcio**:

SQLite es un sol fitxer. Si el filesystem es corromp, pots perdre tot. PostgreSQL te Write-Ahead Log, crash recovery, i replicacio. Es mes resilient.

**3. Funcionalitats avançades**:

- **JSONB**: pots guardar documents JSON amb indexacio.
- **Full Text Search**: cerca en text complet, similar a Elasticsearch.
- **GIS (PostGIS)**: per dades geospatials.
- **Foreign data wrappers**: accedir a altres fonts de dades com si fossin taules.

**4. Casos d'us on PostgreSQL te sentit al BernatLab**:

- **Nextcloud**: 5+ usuaris, milers de fitxers. PostgreSQL > SQLite.
- **Gitea**: mes de 1 usuari, centenars de repositoris. PostgreSQL > SQLite.
- **Wiki (BookStack, DokuWiki):** amb moltes pagines i revisions. PostgreSQL > SQLite.
- **Aplicacio web propia**: amb mes de 10 usuaris concurrents. PostgreSQL > SQLite.

**5. Casos on SQLite es millor**:

- **Scripts personals**: menys de 1000 files, 1 usuari.
- **App de configuracio**: pocs canvis, llegit per 1 proces.
- **Tests unitaris**: velocitat sobre funcionalitat.
- **Cues locals**: un sol proces productor/consumidor.

**Arguments emocionals**:

Molts projectes petits **comencen amb SQLite per simplicitat** i **migrar a PostgreSQL quan cal**. Aixo es una bona estrategia:

1. Comença amb SQLite per tenir algo funcionant rapidament.
2. Quan vegis senyals d'alerta (lentitud, errors, mes usuaris), migra.
3. La migracio es relativament facil (export SQL, import a Postgres).

**Senyals que cal migrar**:

- Les consultes triguen mes de 1 segon.
- Rebs errors "database is locked".
- Tens mes de 5 usuaris concurrents.
- Necessites una funcionalitat que SQLite no te (JSONB, full text, GIS).

**Conclusio al company**: SQLite es meravellos per a casos simples. Pero reconeix que arriba un moment que ja no es suficient. La bona noticia es que migrar a PostgreSQL no es traumatic, nomes cal planificar-lo.

---

## Pregunta 14 (oberta): Esquema PostgreSQL per a un cataleg de plantes

**Resposta model**:

Per a un cataleg de plantes amb 500 plantes, 20 atributs cadascuna, i 100 usuaris que consulten al BernatLab, un esquema PostgreSQL optimitzat seria:

**Esquema de taules**:

```sql
CREATE TABLE plantes (
    id SERIAL PRIMARY KEY,
    nom_comu TEXT NOT NULL,
    nom_cientific TEXT NOT NULL,
    familia TEXT,
    origen TEXT,
    dificultat SMALLINT CHECK (dificultat BETWEEN 1 AND 5),
    descripcio TEXT,
    data_alta DATE DEFAULT CURRENT_DATE,
    activa BOOLEAN DEFAULT TRUE
);

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    nom TEXT UNIQUE NOT NULL,
    descripcio TEXT
);

CREATE TABLE planta_categoria (
    planta_id INTEGER REFERENCES plantes(id) ON DELETE CASCADE,
    categoria_id INTEGER REFERENCES categories(id) ON DELETE CASCADE,
    PRIMARY KEY (planta_id, categoria_id)
);

CREATE TABLE atributs (
    id SERIAL PRIMARY KEY,
    planta_id INTEGER REFERENCES plantes(id) ON DELETE CASCADE,
    clau TEXT NOT NULL,  -- 'exposicio_sol', 'freq_reg', 'tipus_sol'
    valor TEXT NOT NULL
);

CREATE TABLE consultes_usuari (
    id BIGSERIAL PRIMARY KEY,
    usuari_id INTEGER,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    cerca TEXT,
    resultats INTEGER
);
```

**Indexos**:

```sql
-- Index unic compost per evitar duplicats
CREATE UNIQUE INDEX idx_planta_nom_cient ON plantes(nom_cientific);

-- Index per cerca per nom
CREATE INDEX idx_planta_nom_comu ON plantes(nom_comu);
CREATE INDEX idx_planta_familia ON plantes(familia);

-- Index per atributs
CREATE INDEX idx_atributs_planta ON atributs(planta_id);
CREATE INDEX idx_atributs_clau_valor ON atributs(clau, valor);

-- Index per estadistiques
CREATE INDEX idx_consultes_ts ON consultes_usuari(timestamp);
```

**Consideracions**:

1. **Us de SERIAL** en lloc de sequences manuals: PostgreSQL ho gestiona automaticament.
2. **ON DELETE CASCADE**: si s'esborra una planta, els atributs i categories s'esborren tambe.
3. **TIMESTAMPTZ** per a dates amb zona horaria.
4. **CHECK constraint** per validar dificultat entre 1 i 5.
5. **JSONB opcional**: per atributs variables, podries fer `atributs JSONB` en lloc de taula separada.

**Indexacio adicional per rendiment**:

- `pg_trgm` per cerca difusa de text:
```sql
CREATE EXTENSION pg_trgm;
CREATE INDEX idx_planta_nom_trgm ON plantes USING gin (nom_comu gin_trgm_ops);
```

Aixo permet cerques com `nom_comu ILIKE '%toma%'` rapidissimes.

**Consultes tipiques**:

```sql
-- Totes les plantes d'una familia
SELECT * FROM plantes WHERE familia = 'Solanaceae';

-- Plantes que requereixen poc sol
SELECT p.* FROM plantes p
JOIN atributs a ON p.id = a.planta_id
WHERE a.clau = 'exposicio_sol' AND a.valor IN ('ombra', 'semi-ombra');

-- Plantes afegides l'ultim mes
SELECT * FROM plantes WHERE data_alta > NOW() - INTERVAL '1 month';

-- Estadistiques: top cerques
SELECT cerca, COUNT(*) FROM consultes_usuari
WHERE timestamp > NOW() - INTERVAL '30 days'
GROUP BY cerca ORDER BY count DESC LIMIT 10;
```

**Recomanacio al BernatLab**:

- Aquest esquema funciona per a 500 plantes. Si creixes a 50.000, considera PostGIS o full text search.
- Important: fer backups regulars amb `pg_dump`.
- Monitoritzar consultes lentes amb `pg_stat_statements`.

---

## Pregunta 15 (oberta): Seguretat de PostgreSQL exposat

**Resposta model**:

Exposar PostgreSQL directament a internet al BernatLab (100.x.y.z) es una de les decisions mes perilloses que pots prendre. Analitzem els riscos i les alternatives:

**Riscs dexposar PostgreSQL a internet**:

1. **Atacs de brute force**: els atacants saben que PostgreSQL te el port 5432. Escanejen internet cercant ports oberts i intenten passwords. Un password feble es trencat en hores.

2. **Exploits de versions antigues**: si la teva versio de PostgreSQL te una vulnerabilitat coneguda (i les hi ha), un atacant pot comprometre el sistema sense ni tan sols necessitar password.

3. **Atac DoS (Denegacio de servei)**: un atacant pot fer milers de connexions concurrents per saturar la teva RPi. Encara que no entri, el sistema queda no operatiu.

4. **Exposicio de dades**: si aconsegueix accedir, pot llegir totes les dades de la teva BD. Nextcloud te tots els teus fitxers indexats alli.

5. **Escalada de privilegis**: un cop dins, pot intentar exploits per obtenir acces al sistema operatiu.

**Cas real**: el 2018, un atac massiu va explotar versions antigues de PostgreSQL a servidors exposats. Milers de bases de dades van ser esborrades o segrestades per ransomware.

**Bones practiques al BernatLab**:

1. **Mai exposar el port 5432 directament a internet**. Mai.

2. **Usar nomes a la xarxa interna**: el port 5432 nomes accessible des de la xarxa Docker o desde la RPi.

3. **Si cal acces remot, usar SSH tunnel**:
```bash
ssh -L 5433:localhost:5432 usuari@bernatlab
# Ara pots accedir a localhost:5433 que es la BD remota
```

4. **Autenticacio forta**: passwords llargs, autenticacio de dos factors per a usuaris admins.

5. **Configurar pg_hba.conf**: nomes permetre connexions desde IPs de confiança.

6. **Mantenir PostgreSQL actualitzat**: cada versio nova corregeix vulnerabilitats.

7. **Monitoritzar logs**: alertes de connexions sospitoses (molts intents fallits, IPs extranyes).

8. **Limit per connexions**: `max_connections = 100` per evitar DoS.

9. **Firewall**: `ufw deny 5432` o `iptables -A INPUT -p tcp --dport 5432 -j DROP`.

**Exemple de configuracio segura**:

```bash
# Al docker-compose de PostgreSQL
ports:
  - "127.0.0.1:5432:5432"  # nomes localhost

# O millor, sense port directe
expose:
  - "5432"  # nomes accesible desde altres contenidors de la xarxa
```

**Alternativa professional**: si necessites acces des de fora (per exemple, des dun portatil), usa un **VPN** (WireGuard, Tailscale). Aleshores la connexio es xifrada i autenticada, i nomes des de dispositius de confiança.

**Conclusio**: la regla es simple: **mai exposar una base de dades directament a internet**. Sempre hi ha una alternativa mes segura. Al BernatLab, aixo es encara mes important perque la RPi te recursos limitats per defensar-se.

---

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum.
- **3-4 encerts**: Rellegeix el capitol amb atencio, sobretot la seccio de tipus de dades.
- **0-2 encerts**: Repassem junts el capitol. Es la base per a Grafana (cap 10) i per a aplicacions amb IA.

## Que fer si has encertat totes

- Passa al **Capitol 6** (InfluxDB).
- O fes l'**exercici practic** amb mes dades i transaccions per consolidar.
