# Qüestionari — Capitol 4: Bases de dades SQLite

> 10 preguntes · ~15 min

## Pregunta 1
Quin tipus de base de dades es SQLite?

- [ ] Client-servidor (com PostgreSQL)
- [x] Emmagatzemada en un sol fitxer .db o .sqlite
- [ ] Nomes per a memoria RAM
- [ ] Nomes per a grans volums de dades

## Pregunta 2
Quin es el limit practic de SQLite?

- [ ] 1 MB
- [ ] 1 GB
- [x] Al voltant d'1 TB (pero va millor amb menys)
- [ ] Il·limitat

## Pregunta 3
Quin navegador grafic es recomana per veure una base de dades SQLite?

- [ ] phpmyadmin
- [ ] pgAdmin
- [x] DB Browser for SQLite
- [ ] Adminer

## Pregunta 4
Quina ordre faries servir per fer un backup consistent d'una BD SQLite?

- [ ] cp -r /path
- [ ] tar czf
- [x] sqlite3 db.db .dump > backup.sql
- [ ] No cal fer backup, ja es consistent sempre

## Pregunta 5
Quin es l'avantatge principal de SQLite respecte a PostgreSQL?

- [ ] Mes rapid per a milions d'escriptures
- [x] No necessita servidor, es un sol fitxer
- [ ] Millor concurrencia
- [ ] Millor seguretat

## Pregunta 6
Quin mode de journaling es el mes segur a SQLite?

- [ ] DELETE (el classic)
- [x] WAL (Write-Ahead Log)
- [ ] OFF
- [ ] MEMORY

## Pregunta 7
Quina extensio de fitxer es la mes comuna per a una BD SQLite?

- [x] .db, .sqlite, .sqlite3
- [ ] .sql
- [ ] .data
- [ ] .csv

## Pregunta 8
Quin cas NO es adequat per a SQLite?

- [ ] Un blog personal
- [ ] Un registre de lectures de sensors
- [x] Una botiga online amb 1000 usuaris concurrents
- [ ] Una app de notes local

## Pregunta 9 (oberta)
Explica amb les teves paraules: quan triaries SQLite i quan triaries PostgreSQL per a un servei del BernatLab. Posa exemples concrets.

Pistes per respondre:
- Quin volum de dades tindras?
- Quants accessos concurrents?
- Necessites replicacio o transaccions distribuides?
- Quin tipus de consultes faras?

## Pregunta 10 (oberta)
Imagina que tens una base de dades SQLite amb 5 anys de lectures de sensors i ha crescut fins a 8 GB. Et convindra seguir amb SQLite o migrar a PostgreSQL? Argumenta la decisio.

Pistes per respondre:
- Quin es el rendiment esperat a 8 GB?
- Es pot netejar la BD vella?
- Quines avantatges tindria migrar a PostgreSQL?
- Quin cost te la migracio (temps, risc)?
