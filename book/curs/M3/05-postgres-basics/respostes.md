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

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum.
- **3-4 encerts**: Rellegeix el capitol amb atencio, sobretot la seccio de tipus de dades.
- **0-2 encerts**: Repassem junts el capitol. Es la base per a Grafana (cap 10) i per a aplicacions amb IA.

## Que fer si has encertat totes

- Passa al **Capitol 6** (InfluxDB).
- O fes l'**exercici practic** amb mes dades i transaccions per consolidar.
