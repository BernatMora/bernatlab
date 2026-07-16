# Exercici practic — Capitol 4: Bases de dades SQLite

> 30-40 min · Real al teu sistema

## Objectiu

Crear una base de dades SQLite, omplir-la amb dades de sensors, practicar el backup amb `.dump`, provar consultes, i restaurar-les. Tot amb un script Python per veure com s'hi accedeix des de codi.

## Requisits

- Tailscale actiu
- Connexio SSH a la RPi
- Python 3 instal·lat (ja ho hauries de tenir)
- 30-40 minuts

## Pas 1: Instal·la SQLite i DB Browser (5 min)

```bash
# Comprova que ja tens sqlite3
sqlite3 --version
# Hauria de dir algo com: 3.40.x

# Si no, instal·la'l
sudo apt update
sudo apt install -y sqlite3

# DB Browser (opcional, pero molt recomanable)
sudo apt install -y sqlitebrowser
```

## Pas 2: Crea la base de dades (10 min)

```bash
mkdir -p /home/pi/bernatlab/proves
cd /home/pi/bernatlab/proves

# Crea una BD i una taula
sqlite3 hivernacle.db <<EOF
CREATE TABLE sensors (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  sensor TEXT NOT NULL,
  valor REAL NOT NULL,
  ts DATETIME DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_sensor_ts ON sensors(sensor, ts);

INSERT INTO sensors (sensor, valor) VALUES
  ('temperatura', 22.5),
  ('humitat', 65.0),
  ('llum', 850.0),
  ('temperatura', 23.0),
  ('humitat', 64.0);

SELECT * FROM sensors;
EOF
```

## Pas 3: Practica consultes (5 min)

```bash
# Entra al mode interactiu
sqlite3 /home/pi/bernatlab/proves/hivernacle.db

# Prova aquestes consultes (una per una):
.mode column
.headers on

SELECT * FROM sensors WHERE sensor = 'temperatura';
SELECT sensor, AVG(valor) FROM sensors GROUP BY sensor;
SELECT COUNT(*) FROM sensors;

# Mitjana per hora
SELECT 
  strftime('%Y-%m-%d %H:00', ts) AS hora,
  sensor,
  AVG(valor) AS mitjana
FROM sensors
GROUP BY hora, sensor;

# Surt
.quit
```

## Pas 4: Fes un backup consistent (5 min)

```bash
# Metode 1: .dump (logic, sempre consistent)
sqlite3 /home/pi/bernatlab/proves/hivernacle.db .dump > \
  /home/pi/bernatlab/proves/hivernacle-backup-$(date +%Y%m%d).sql

ls -lh /home/pi/bernatlab/proves/
# Hauries de veure hivernacle.db (~8K) i el .sql (~8K)

# Comprova
head -20 /home/pi/bernatlab/proves/hivernacle-backup-*.sql
# Es SQL pla que es pot restaurar a qualsevol altre BD
```

## Pas 5: Simula un desastre i restaura (10 min)

```bash
# Esborrem l'original
rm /home/pi/bernatlab/proves/hivernacle.db

# La restaurem des del backup
sqlite3 /home/pi/bernatlab/proves/hivernacle.db < \
  /home/pi/bernatlab/proves/hivernacle-backup-*.sql

# Comprova
sqlite3 /home/pi/bernatlab/proves/hivernacle.db "SELECT COUNT(*) FROM sensors;"
# Hauries de veure 5 (les files originals)
```

## Pas 6: Accedeix des de Python (5 min)

```bash
# Crea un script Python
cat > /home/pi/bernatlab/proves/insertar.py <<'PY'
import sqlite3
import time

db = sqlite3.connect('/home/pi/bernatlab/proves/hivernacle.db')
cur = db.cursor()

# Inserir una lectura nova
cur.execute(
    "INSERT INTO sensors (sensor, valor) VALUES (?, ?)",
    ('temperatura', 22.7)
)
db.commit()
print("Inserit!")

# Llegir les ultimes 5 temperatures
cur.execute("""
    SELECT * FROM sensors
    WHERE sensor = 'temperatura'
    ORDER BY ts DESC
    LIMIT 5
""")
for fila in cur.fetchall():
    print(fila)

db.close()
PY

# Executa'l
python3 /home/pi/bernatlab/proves/insertar.py
```

## Pas 7: Usa DB Browser per visualitzar (5 min)

```bash
# Obre DB Browser (via SSH+X11 o localment)
sqlitebrowser /home/pi/bernatlab/proves/hivernacle.db &

# O visualitza nomes l'esquema en text
sqlite3 /home/pi/bernatlab/proves/hivernacle.db ".schema"
```

## Validacio

Has acabat si:

- [ ] Has creat una base de dades SQLite amb una taula.
- [ ] Has inserit dades amb l'ordre `.dump` i INSERT.
- [ ] Has practicat consultes (SELECT, WHERE, GROUP BY).
- [ ] Has fet un `.dump` per fer backup.
- [ ] Has "perdut" el .db i l'has restaurat des del .sql.
- [ ] Has vist com accedir-hi des de Python.
- [ ] Has obert la BD amb DB Browser (o almenys has vist l'esquema).

## Per aprofundir

- Practica transaccions amb `BEGIN; ... COMMIT;` a l'intèrpret de sqlite3.
- Prova el mode WAL: `PRAGMA journal_mode=WAL;`
- Investiga com activar el xifratge amb SQLCipher si vols dades privades.
- Compara el rendiment fent 100.000 insercions a SQLite vs a PostgreSQL.
