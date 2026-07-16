# Resum — Capitol 4: Bases de dades SQLite

## La idea clau

**SQLite** es la base de dades mes usada del mon, i probablement no ho sabies. Esta al teu telefon Android, al teu navegador Chrome, al teu sistema operatiu, a milers d'aplicacions. I el mes important: **es un sol fitxer**. No hi ha cap servidor, cap dimoni, cap port. Es la BD mes simple que pots fer servir, i alhora prou potent per a molts casos reals.

Al BernatLab la faig servir per a totes les dades petites i locals: historial de tasques, registres de configuracio, metadades de sensors, cache de consultes. Per a dades mes grans o amb mes concurrencia faig servir **PostgreSQL** (cap 5) o **InfluxDB** (cap 6). Pero abans de tirar cap a una BD "professional", pensa si SQLite no et serveix.

## Que es SQLite exactament?

Es una **base de dades embeguda** (embedded). Es a dir:

- **No es un servidor** que escolta en un port. No hi ha cap dimoni.
- **Es una llibreria** que la teva aplicacio enllaça.
- **La BD es un sol fitxer** al sistema de fitxers.
- **Un sol fitxer per aplicacio**, normalment a `/var/lib/...` o `/home/pi/...`.

Exemple tipic al BernatLab:

```bash
# La BD de notes de camp
/home/pi/bernatlab/notes/quadern-camp.db

# La BD de registre de tasques
/var/lib/homeassistant/home-assistant_v2.db
```

Les aplicacions accedeixen al fitxer `.db` directament. Si vols veure les dades, nomes cal `sqlite3 elmeu.db`.

## Per que SQLite es tant popular?

1. **Simplicitat**: no cal instalar ni configurar res. `pip install sqlite3` ja ve amb Python.
2. **Fiabilitat**: es una de les BD mes testejades del mon (mils de tests, mes de 20 anys d'ús intensiu).
3. **Rendiment**: per a aplicacions petites, es **mes rapid** que PostgreSQL (no hi ha latencia de xarxa).
4. **Portabilitat**: el fitxer es pot copiar a un USB, moure a una altra maquina, fer backup amb `cp`.
5. **ACID**: compleix les quatre propietats (Atomicity, Consistency, Isolation, Durability), com les BD grans.
6. **Sense cost**: es public domain. La pots fer servir on vulguis, gratis.

## Quan usar SQLite

SQLite brilla en aquests casos:

- **Aplicacions locals** (sense servidor): una app que nomes usa una persona, o un script periodic.
- **Dispositius mobils i IoT**: telofons, sensors, embarcats.
- **Prototips i MVPs**: començar rapidament sense configurar un servidor.
- **Cache i configuracio**: dades que no canvien sovint o que son molt llegides.
- **Fins a milers d'escriptures per segon** en condicions ideals.

Exemples reals al BernatLab:
- `home-assistant_v2.db` (Home Assistant te tota la BD a SQLite).
- Quadern de camp de l'hort.
- Cache de resultats de consultes de Grafana.
- Metadades dels sensors (nom, ubicacio, calibracio).

## Quan NO usar SQLite

SQLite te limits clars:

- **Escriptures concurrents**: nomes **una** escriptura a la vegada. Si tens 10 usuaris escribint alhora, hi haura cues.
- **Volum de dades**: per sobre d'1-2 GB comença a ser menys efficient. Fins a uns 5-10 GB funciona, pero per a mes cal una altra cosa.
- **Xarxa**: SQLite nomes es local. No es pot accedir per xarxa (cal aplicar capa d'aplicacio per sobre).
- **Replicacio**: no te master-slave ni clustering.

Si el teu cas es algun d'aquests, passa a **PostgreSQL** (cap 5).

## Eines per treballar amb SQLite

### sqlite3 (linia de comandes)

L'eina basica pero potent:

```bash
# Obrir una BD
sqlite3 hivernacle.db

# Dins de sqlite3>:
.help                  # ajuda
.tables                # llistar taules
.schema sensors        # estructura d'una taula
.headers on            # mostrar capçaleres
.mode column           # format de sortida
SELECT * FROM sensors LIMIT 5;
.quit
```

### DB Browser for SQLite (grafic)

Eina grafica multiplataforma. Es pot instal·lar a la RPi (`sudo apt install sqlitebrowser`) o al teu PC. Permet:

- Veure l'esquema visualment.
- Navegar per les dades en taula.
- Fer consultes amb resaltat de sintaxi.
- Exportar a CSV/JSON.

### sqlite-web (servidor web)

Un servidor web petit per a SQLite. Util per accedir a la BD des del navegador. Al BernatLab no el faig servir, pero es bona eina.

## Com fer backup d'una BD SQLite

Hi ha dues maneres:

### Metode 1: `.dump` (logic, recomanat)

```bash
sqlite3 hivernacle.db .dump > hivernacle-$(date +%Y%m%d).sql
```

Genera un fitxer SQL amb totes les sentencies CREATE i INSERT. Es pot restaurar a qualsevol altre SQLite (o fins i tot a una altre BD amb petites modificacions).

### Metode 2: Copiar el .db (nomes si la BD esta quieta)

```bash
# Aturar el servei que la fa servir
sudo systemctl stop home-assistant

# Copiar el fitxer
cp /var/lib/homeassistant/home-assistant_v2.db \
   /home/pi/bernatlab/backups/

# Tornar a aixecar
sudo systemctl start home-assistant
```

**Important**: mai copiis un .db mentre s'hi esta escribint. Pots obtenir un fitxer corrupte. Activa el mode WAL (`PRAGMA journal_mode=WAL;`) per millorar la seguretat en cas de copia en calent, pero el millor es aturar el servei.

## Com restaurar

Des del `.sql`:

```bash
sqlite3 nova-bd.db < hivernacle-20250615.sql
```

Des del `.db` copiat:

```bash
cp hivernacle-20250615.db hivernacle.db
```

## Optimitzacions per a l'hort IoT

Algunes configuracions que aplico al BernatLab:

```sql
-- Mode WAL per a millor rendiment i seguretat
PRAGMA journal_mode=WAL;

-- Sync normal (millor rendiment, encara segur amb WAL)
PRAGMA synchronous=NORMAL;

-- Incrementar cache
PRAGMA cache_size=-20000;  -- 20 MB

-- Per a moltes lectures de sensors, indexar
CREATE INDEX idx_sensor_ts ON sensors(sensor, ts);
```

## Connexions amb altres capítols

- **Cap 1** — Les BD son una de les coses mes importants a backupejar.
- **Cap 3** — Com fer backup consistent dels volums Docker.
- **Cap 5** — Quan cal mes potencia: PostgreSQL.
- **Cap 6** — Per a dades de sensors massives: InfluxDB.
