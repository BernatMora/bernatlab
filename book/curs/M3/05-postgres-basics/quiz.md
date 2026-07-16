# Qüestionari — Capitol 5: PostgreSQL basic

> 10 preguntes · ~15 min

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
- Que passa amb l'horari d'estiu?
- Que passa si un sensor esta a una altra zona horaria?
- Com emmagatzema Postgres les dates internament?

## Pregunta 10 (oberta)
Tens un blog personal amb 50.000 articles i 10.000 visites diaries. Triaries SQLite, PostgreSQL o una altra cosa? Argumenta la decisio.

Pistes per respondre:
- Quin volum de dades tindras?
- Quants usuaris concurrents?
- Quin tipus de consultes faras?
- Es important el SEO i el temps de resposta?
