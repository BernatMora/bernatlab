# Respostes - Capitol 8: Backup de contenidors

> Mira les respostes DESPRES d'haver fet el qüestionari.

## Pregunta 1: Regla 3-2-1?

**Resposta correcta**: 3 copies, 2 suports diferents, 1 fora de la maquina.

**Explicacio**: Aquesta es la regla estandard de la industria dels backups. Garantitza que encara que falli un disc, falli un segon, o es perdi tot a la maquina original, sempre tens una còpia intacta.

---

## Pregunta 2: Backup d'un volum?

**Resposta correcta**: Usar un contenidor temporal que munta el volum i empaqueta amb tar.

**Explicacio**: Docker no te una comanda nativa per fer backup d'un volum. El truc es muntar-lo en un contenidor temporal amb tar, que pot llegir i empaquetar tot. Es la forma mes portable i funciona amb qualsevol tipus de volum.

---

## Pregunta 3: pg_dump?

**Resposta correcta**: `docker exec postgres-container pg_dump -U user dbname > backup.sql`.

**Explicacio**: Cada base de dades te la seva eina de dump. PostgreSQL usa pg_dump, MySQL/MariaDB usa mysqldump, MongoDB usa mongodump. Totes creen un fitxer de text amb les instruccions SQL per reconstruir la base de dades.

---

## Pregunta 4: Per que xifrar?

**Resposta correcta**: Perque si el backup es perd o es robat, les dades estiguin protegides.

**Explicacio**: Un backup al núvol o a un disc extern pot caure en males mans. Si esta xifrat, nomes tu pots llegir-lo. Es una bona practica sempre, pero especialment per a dades personals o confidencials.

---

## Pregunta 5: Backup verificat?

**Resposta correcta**: Un backup que sha provat de restaurar i sha confirmat que funciona.

**Explicacio**: Un backup no verificat es inutil. Pots tenir un script trencat que "fa backup" pero que nomes esta creant fitxers buits. La unica manera de saber que un backup funciona es provar-lo. Moltes empreses fan "disaster recovery drills" periòdics.

---

## Pregunta 6: Eina per incrementals al núvol?

**Resposta correcta**: restic, borgbackup o rclone.

**Explicacio**: Aquestes eines modernes fan backups incrementals (nomes els canvis), suporten diversos backends al núvol (S3, B2, etc.), i permeten restaurar facilment. Restic i borgbackup tambe xifren per defecte.

---

## Pregunta 7: Automatitzar a hora concreta?

**Resposta correcta**: cron.

**Explicacio**: Cron es el servei classic de Linux per executar feines periòdiques. Es perfecte per a backups: un cop al dia, setmanal, etc. Tambe es poden usar systemd timers (mes modern) pero cron es mes simple.

---

## Pregunta 8: Frequencia minima?

**Resposta correcta**: Un cop al dia.

**Explicacio**: Un cop al dia es el minim raonable. Si tens dades molt valuables (una base de dades de transaccions), potser vols cada hora o cada 4 hores. Si son dades mes aviat estatiques (fitxers personals), un cop al dia es suficient.

---

## Pregunta 9 (oberta): Diferencies i criticitat

**Resposta model**:

Son tres tipus diferents de backups, cadascun amb el seu objectiu:

**1. Backup d'un volum (tar.gz)**: es un **snapshot binari** de totes les dades que hi ha al volum. Per exemple, si el volum es `/var/lib/postgresql/data`, el backup es una copia exacta de tots els fitxers que PostgreSQL gestiona: WAL logs, fitxers de dades, configuracio. Avantatge: rapid (es una copia binaria). Inconvenient: nomes es pot restaurar a un volum de la mateixa mida o mes gran, i nomes serveix per a la mateixa versio de la base de dades. Si tens 50 GB de volum, el backup ocupara 50 GB (o menys si comprimeix be).

**2. Backup d'una base de dades (dump SQL)**: es un **fitxer de text** amb totes les instruccions SQL per reconstruir la base de dades: CREATE TABLE, INSERT, CREATE INDEX, etc. Avantatge: portable, es pot restaurar a qualsevol versio de PostgreSQL posterior, ocupa menys espai (es text pla), es pot inspeccionar amb un editor. Inconvenient: mes lent de generar (cal "dumpar" totes les dades), nomes serveix per a bases de dades.

**3. Backup dels fitxers de configuracio (docker-compose.yml, .env)**: es una **copia dels fitxers** que defineixen el stack: quins serveis, quines imatges, quins volums, quins secrets, quines xarxes. Avantatge: rapidissim (son pocs KB), permet reproduir l'stack en qualsevol altre maquina. Inconvenient: no conté les dades, nomes la "recepta" per muntar-les.

**Mes critic**: la combinacio de tots tres, pero si nomes poguessim triar un, triaria el **dump SQL + el volum**. Les dades son el mes important. La configuracio es pot tornar a escriure (es poca estona), pero les dades si es perden no es poden recuperar.

La **millor estrategia** es fer TOTS tres:
- El volum per a una restauracio rapida.
- El dump SQL per a portabilitat.
- La configuracio per a reproduir el stack.

I sempre verificar que els tres es poden restaurar. Un backup no verificat es un no-backup.

---

## Pregunta 10 (oberta): Estrategia 3-2-1 al BernatLab

**Resposta model**:

La meva estrategia complerta per a 50 GB de fotos + MariaDB al BernatLab:

**Còpia 1: Original (local)**

- **On**: `/home/pi/fotos/` (volum nomenat `nextcloud-data`) i la base de dades `nextcloud-db` (volum nomenat).
- **Per que**: son les dades "vives" del Nextcloud, les que faig servir diàriament.
- **Cada quan**: sempre.

**Còpia 2: Backup local (rapid)**

- **On**: disc SSD extern USB de 500 GB muntat a `/mnt/backup/`.
- **Com**: un script amb `rsync --link-dest` per fer backups incrementals diaries. Cada dia es crea un directori `daily.0`, `daily.1`, etc. i `rsync` nomes copia els canvis respecte al dia anterior.
- **Cada quan**: cada nit a les 3 AM via cron.
- **Retencio**: 7 dies de backups diaries + 4 setmanals (cada dilluns) + 3 mensuals.

```bash
#!/bin/bash
# backup-local.sh - cada nit a les 3 AM
set -e
BACKUP_BASE=/mnt/backup
DATA=$(date +%F)

# 1. Dump de la base de dades
docker exec nextcloud-db mysqldump -u root -p"$DB_PASS" nextcloud > ${BACKUP_BASE}/db/nextcloud-${DATA}.sql

# 2. Rsync incremental de les fotos
mkdir -p ${BACKUP_BASE}/fotos/daily.${DATA}
rsync -a --delete /home/pi/fotos/ ${BACKUP_BASE}/fotos/daily.${DATA}/

# 3. Cleanup
find ${BACKUP_BASE}/db -name "*.sql" -mtime +30 -delete
```

**Còpia 3: Núvol (fora de la maquina)**

- **On**: Backblaze B2 (o S3, Wasabi) amb `restic`.
- **Com**: restic fa backups incrementals amb desduplicacio i xifrat. Si puja 50 GB al núvol el primer cop, els seguents son nomes els canvis.
- **Cada quan**: cada nit a les 5 AM (despres del backup local).
- **Retencio**: 30 dies al núvol.

```bash
#!/bin/bash
# backup-nuvol.sh - cada nit a les 5 AM
export B2_ACCOUNT_ID=<id>
export B2_ACCOUNT_KEY=<key>
export RESTIC_REPOSITORY=b2:bernatlab-backup
export RESTIC_PASSWORD=<passphrase>

restic backup /home/pi/fotos/ --tag=fotos
restic backup /home/pi/backups/db/ --tag=db

# Neteja els antics
restic forget --keep-daily 30 --prune
```

**Verificacio (mensual)**

Un cop al mes, faig un test de restauracio:
```bash
# Restaurar a un directori temporal
mkdir -p /tmp/restore-test
restic -r b2:bernatlab-backup restore latest --target /tmp/restore-test/
ls -la /tmp/restore-test/home/pi/fotos/ | head
diff -q /tmp/restore-test/home/pi/fotos/ /home/pi/fotos/ 2>&1 | head
```

Si `diff` retorna alguna cosa, el backup te un problema.

**Monitoritzacio**

El cron ha de fallar si algo va malament. Configuro notificacions:
```bash
0 3 * * * /home/pi/scripts/backup-local.sh >> /var/log/backup.log 2>&1 || \
  curl -X POST https://ntfy.sh/bernatlab-backup-error -d "Backup ha fallat!"
```

Aixi rebo una notificacio push al mobil si el backup falla.

**Xifrat**

Restic xifra per defecte. Els volums de backup local els puc xifrar amb LUKS al SSD extern. La base de dades la xifro nomes si te dades molt sensibles (un Nextcloud de fotos personals no ho necessita urgentment).

**Resum**:

| Còpia | On | Eina | Cada quan | Retencio |
|---|---|---|---|---|
| Original | RPi (volums) | - | sempre | - |
| Local | SSD USB | rsync | cada nit | 7+4+3 |
| Núvol | Backblaze B2 | restic | cada nit | 30 dies |

Aixo es la **regla 3-2-1 complerta**: 3 copies (original, SSD, núvol), 2 suports (disc intern + núvol), 1 fora (el núvol). Si la RPi es mor, tinc el SSD. Si la casa crema, tinc el núvol.

---

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum i fer l'exercici practic.
- **3-4 encerts**: Refes l'exercici posant mes atencio a la verificacio.
- **0-2 encerts**: Repassem. Els backups son basics i critics.

## Que fer si has encertat totes

- Passa al **Capitol 9** (monitoritzacio).
- Configura borgbackup o restic al BernatLab real.
- Prova de restaurar des del núvol (disaster recovery real).
