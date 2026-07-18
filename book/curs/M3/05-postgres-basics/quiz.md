# Qüestionari - Capitol 5: PostgreSQL basic

> 15 preguntes · ~20 min

## Pregunta 1
Quin tipus de base de dades es PostgreSQL?

- [ ] Emmagatzemada en un sol fitxer
- [x] Client-servidor
- [ ] Nomes graf
- [ ] Nomes per a memoria

## Pregunta 2
Quin es el client de linia de comandes de PostgreSQL?

- [ ] mysql
- [x] psql
- [ ] pg-client
- [ ] postgres-cli

## Pregunta 3
Quina ordre faries servir per fer un backup consistent d'una BD?

- [ ] cp /var/lib/postgresql
- [x] pg_dump -U user db > backup.sql
- [ ] tar czf
- [ ] No cal fer backup

## Pregunta 4
Quin tipus de dada es millor per a dates amb zona horaria?

- [ ] TIMESTAMP
- [x] TIMESTAMPTZ
- [ ] DATE
- [ ] DATETIME

## Pregunta 5
Quantes connexions concurrents pot gestionar PostgreSQL?

- [ ] 1
- [ ] 10
- [x] Milers
- [ ] Infinit

## Pregunta 6
Quin es el port per defecte de PostgreSQL?

- [ ] 3306
- [ ] 8080
- [x] 5432
- [ ] 27017

## Pregunta 7
Quina ordre mostra les taules dins de psql?

- [ ] SHOW TABLES
- [x] \dt
- [ ] DESCRIBE TABLES
- [ ] LIST TABLES

## Pregunta 8
Quin tipus JSON es indexable a PostgreSQL?

- [ ] JSON
- [x] JSONB
- [ ] TEXT
- [ ] VARCHAR

## Pregunta 9 (oberta)
Explica amb les teves paraules: per que `TIMESTAMPTZ` es millor que `TIMESTAMP`? Pensa en un hort IoT amb sensors a diferents llocs del mon.

Pistes per respondre:
- Que passa amb lhorari destiu?
- Que passa si un sensor esta a una altra zona horaria?
- Com emmagatzema Postgres les dates internament?

## Pregunta 10 (oberta)
Tens un blog personal amb 50.000 articles i 10.000 visites diaries. Triaries SQLite, PostgreSQL o una altra cosa? Argumenta la decisio.

Pistes per respondre:
- Quin volum de dades tindras?
- Quants usuaris concurrents?
- Quin tipus de consultes faras?
- Es important el SEO i el temps de resposta?

## Pregunta 11 (oberta)
Per que creus que PostgreSQL sha mantingut com una de les bases de dades mes populars durant 30+ anys? Quin impacte te aquesta maduresa al BernatLab?

Pistes per respondre:
- Maduresa = moltes funcionalitats provades.
- Comunitat activa = moltes extensions.
- Compatibilitat: el que escrius avui funciona d'aqui 10 anys.
- Al BernatLab, quina garantia de futur tens amb les teves dades?

## Pregunta 12 (oberta)
Quina relacio hi ha entre els indexos i el rendiment de les consultes? Com afecta al BernatLab tenir 1 milio de files a una taula sense index correcte? Dona exemples concrets.

Pistes per respondre:
- Sense index: escaneig sequencial = lent.
- Amb index: cerca binaria = rapid.
- Pero cada index ocupa espai i alentza les escriptures.
- Trade-off: lectura rapida vs escriptura rapida.

## Pregunta 13 (oberta)
Imagina que el teu company et diu: "per que complicar-me amb PostgreSQL si SQLite ja em fa el fet?". Argumenta per que al BernatLab pot tenir sentit pujar a PostgreSQL per a certes aplicacions.

Pistes per respondre:
- Mes usuaris concurrents.
- Mes robustesa davant corrupcio.
- Funcionalitats avançades (JSONB, GIS, full text search).
- Cas d'us concret: Nextcloud o Gitea.

## Pregunta 14 (oberta)
Aplica el concepte de PostgreSQL al cas concret del BernatLab amb un servei de cataleg de plantes (tipus hortosona). Tinc 500 plantes amb 20 atributs cadascuna (nom, especie, data de plantacio, etc) i uns 100 usuaris que consulten. Dissenya l'esquema de taules amb els indexos necessaris.

Pistes per respondre:
- Una sola taula o multiples?
- Quins camps son els mes consultats?
- Quins indexos posaries?
- Caldria un JOIN amb una taula de categories?

## Pregunta 15 (oberta)
Quines consequencies te per a la seguretat exposar PostgreSQL a internet vs tenir-lo nomes a la xarxa interna? Argumenta amb exemples del risc real al BernatLab (100.x.y.z).

Pistes per respondre:
- PostgreSQL te autenticacio pero no xifrat per defecte.
- Un atacant que troba el port pot fer brute force.
- Nomes a xarxa interna: nomes accessible des de l'amfitrio.
- Trade-off: conveniencia vs seguretat.
- Millor practica: nomes xarxa interna, mai exposar directament.
