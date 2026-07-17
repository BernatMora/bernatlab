# Qüestionari - Capitol 4: Bases de dades SQLite

> 15 preguntes · ~20 min

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
Quin es lavantatge principal de SQLite respecte a PostgreSQL?

- [ ] Mes rapid per a milions descriptures
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
Explica amb les teves paraules: quan triaries SQLite i quan triaries PostgreSQL per a un servei del BernatLab? Posa exemples concrets.

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

## Pregunta 11 (oberta)
Per que creus que SQLite ha esdevingut la base de dades mes usada al mon (mes que MySQL o PostgreSQL)? Quina lliço podem extreure per a les nostres decisions al BernatLab?

Pistes per respondre:
- Esta integrada en moltes aplicacions (telefons, navegadors, etc).
- La simplicitat guanya a la potencia en la majoria de casos.
- Menys parts móbils = menys fallades.
- Trade-off: simplicitat vs potència.

## Pregunta 12 (oberta)
Quina relacio hi ha entre el mode WAL (Write-Ahead Log) i el rendiment de SQLite en escriptures concurrents? Com afecta al BernatLab si tens 10 sensors escrivint cada segon? Argumenta amb exemples.

Pistes per respondre:
- WAL permet lectures i escriptures simultanies.
- Sense WAL, les lectures bloquegen les escriptures.
- Al BernatLab amb sensors continus, WAL es recomanable.
- Trade-off: un fitxer adicional vs rendiment.

## Pregunta 13 (oberta)
Imagina que el teu company et diu: "SQLite es una base de dades de joguina, no serveix per res seriós". Argumenta per que aixo es fals al BernatLab, donant exemples de projectes grans que usen SQLite en produccio.

Pistes per respondre:
- Moltes aplicacions d'escriptori i mobil usen SQLite.
- Fins i tot Airbus l'usa en alguns sistemes.
- Cada vegada mes llocs web petits usen SQLite amb molts de visites.
- Al BernatLab, per a molts casos es mes que suficient.

## Pregunta 14 (oberta)
Aplica el concepte de SQLite al cas concret del BernatLab amb l'hort IoT: tens 5 sensors que escriuen lectures cada minut a una base de dades SQLite local. Dissenya l'esquema de taules, les indexacions, i la estrategia de backup. Considera el creixement esperat a 5 anys.

Pistes per respondre:
- Una taula per sensor o una taula amb sensor_id?
- Quins indexos calen per consultes freqUents?
- On guardes el fitxer .db?
- Quan faries backup i com?

## Pregunta 15 (oberta)
Quines consequencies te per al rendiment del sistema el fet que SQLite nomes permet una escriptura a la vegada (fora de WAL)? Com afecta a l'aplicacio si tens pics de 100 escriptures per segon? Argumenta amb exemples del BernatLab.

Pistes per respondre:
- Sense WAL, les escriptures es serialitzen.
- WAL permet paral·lelisme parcial.
- Al BernatLab amb pocs sensors, no es problema.
- Si cresquis a 1000 sensors, caldria canviar.
- Trade-off: simplicitat de SQLite vs necessitat de paral·lelisme.
