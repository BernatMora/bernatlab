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

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum.
- **3-4 encerts**: Rellegeix el capitol amb atencio, sobretot la seccio de "quan usar SQLite".
- **0-2 encerts**: Repassem junts el capitol. Es la base per als capitols de PostgreSQL i InfluxDB.

## Que fer si has encertat totes

- Passa al **Capitol 5** (PostgreSQL).
- O fes l'**exercici practic** amb mes dades per consolidar.
