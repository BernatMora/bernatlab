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

## Pregunta 11 (oberta): Per que la gent no fa backups

**Resposta model**:

La gent no fa backups fins que perd dades per una combinacio de factors psicologics i economics:

**Factors psicologics**:

1. **Optimisme irracional**: "a mi no em pasara". Es la mateixa logica que porta a la gent a no fer testament o a no portar cinturo. La vulnerabilitat es invisible fins que es real.

2. **Cost tangible vs benefici intangible**: el backup costa temps, espai, configuracio. El benefici nomes es materialitza en cas de perdua, que es un esdeveniment futur i improbable. El cervell prioriza el present.

3. **Pensament magic**: "tinc una RAID", "tinc el núvol", "el meu proveidor ja fa còpies". Totes son excuses per evitar la tasca. Cap es equivalent a un backup real.

4. **Por d'admetre la perdua**: si no tinc backup, no he de pensar en que passaria si ho perdés. Es mes facil viure en la negacio.

5. **Procrastinacio tecnologica**: "quan tingui temps ho fare". El temps no arriba mai. I quan arriba un incident, ja es massa tard.

**Cas emocional al BernatLab**:

Imagina que tens un Nextcloud amb 5 anys de fotos familiars: vacances, moments amb fills, documents importants. Un dia la microSD falla. Les fotos son **irreemplaçables**: no hi ha còpia al núvol de Google, no hi ha album de la iaia. Tot es al teu Nextcloud que ja no arranca.

El sentiment es devastador. No es una perdua economica, es una perdua personal. I passa mes sovint del que sembla: les microSD tenen una vida util limitada (~5 anys d'escriptura), els discs SSD fallen, els lladres entren a cases, els ramsomware son reals.

**Solucio realista**:

1. **Automatitza el backup**: un cop configurat, el backup es transparent. No cal pensar-hi mes.
2. **Fes-lo un cop i oblida't**: posa el cron a les 3 de la matinada. El backup es nomes responsabilitat del sistema.
3. **Verifica un cop al trimestre**: dedica 1 hora cada 3 mesos a restaurar un fitxer random. Això et recorda que el backup funciona.
4. **Documenta el procés de restauracio**: quan tinguis que restaurar (i tindras que restaurar), no vols haver d'aprendre com fer-ho enmig del panic.

El millor backup es el que ja esta configurat abans que el necessitis.

---

## Pregunta 12 (oberta): Mida del backup i RPO

**Resposta model**:

El **RPO (Recovery Point Objective)** es la quantitat maxima de dades que estaries disposat a perdre en cas d'incident. Es un parametre que defineixes tu segons el valor de les dades i el cost del backup.

**Exemples de RPO al BernatLab**:

| Servei | RPO acceptable | Freq backup | Motiu |
|---|---|---|---|
| Nextcloud (documents) | 1 dia | Diari | Documents de feina es poden refer pero costa |
| Nextcloud (fotos) | 1 setmana | Setmanal | Fotos son irreemplaçables, pero el volum es gran |
| Base de dades (Postgres) | 1 hora | Horari | Canvis petits pero constants |
| Logs d'aplicacio | 1 dia | Diari | Util per debug pero no critic |
| Configuracio (compose) | N/A | Git | Ja esta versionat |
| Models LLM (Ollama) | N/A | Mai | Es poden tornar a baixar |

**Calcul del cost d'un RPO d'1 hora**:

Si tens 50 GB de dades que canvien activament:
- Backup horari: 50 GB/hora x 24 = 1.2 TB/dia (si es backup complet).
- Backup incremental: nomes els canvis. 1-2 GB/hora x 24 = 24-50 GB/dia.
- Restic deduplica: encara menys.

**Trade-off RPO vs cost**:

- RPO = 1 setmana: backup setmanal. Economic. Acceptable per a fotos.
- RPO = 1 dia: backup diari. Cost moderat. Acceptable per a documents.
- RPO = 1 hora: backup continu (o molt frequent). Cost alt. Per a dades critiques.
- RPO = 0 (zero perdua): replicacio sincrona. Molt car. Nomes per a produccio profesional.

**Recomanacio al BernatLab**:

- Documents personals: backup diari amb retencio de 30 dies.
- Bases de dades: backup horari amb retencio de 7 dies + 1 backup diari amb retencio de 30 dies.
- Fotos: backup setmanal (son grans i no canvien sovint).

**Realitat practica**: la majoria d'incidents al BernatLab son humans (rm -rf accidental, contenidor borrat, etc.) i no pas fallades de hardware. Un backup diari minimitza el risc en aquests casos.

---

## Pregunta 13 (oberta): RAID no es backup

**Resposta model**:

El company que diu "tinc RAID al servidor, no cal backup" te una confusio comuna pero perillosa. RAID i backup son dues coses completament diferents que resolen problemes diferents:

**Que protegeix RAID**:

- Fallada d'un disc individual. Si tens RAID 1 (mirror) o RAID 5 (parity), el sistema continua funcionant quan un disc falla. Potes substituir el disc i reconstruir.

**Que NO protegeix RAID**:

1. **Borrat accidental**: si un `rm -rf` esborre un directori, el RAID replica la perdua. Tots els discs del mirror tenen la mateixa informacio borrada.

2. **Ransomware**: si un atacant xifra els teus fitxers, el RAID tambe es xifra. El ransomware actua sobre les dades, no sobre el hardware.

3. **Atac amb rootkit/backdoor**: si un atacant instal·la un programa malicios que es replica, tambe es replica al mirror.

4. **Desastre fisic**: incendi, inundacio, robatori. Si es perden tots els discs junts (per exemple, al servidor), el RAID no salva res.

5. **Corrupcio silenciosa de dades**: alguns discs poden corrompre dades sense avisar. RAID nomes detecta quan un disc falla del tot, no quan alguns bits canvien.

6. **Errors d'usuari en lots**: si un script aplica canvis no desitjats a totes les dades (per exemple, un update de Nextcloud que falla), el RAID tambe es veu afectat.

**Combinacio correcta**:

Per a un BernatLab amb dades importants, la combinacio ideal es:
- **RAID 1** (mirror) o **RAID-Z1** (ZFS): per tolerancia a fallada de disc.
- **Backup separat**: per protegir contra borrat, ransomware, desastre.
- **Backup al núvol**: per protegir contra desastre fisic.

**Analogia**: RAID es com tenir dos cotxes iguals (un de recanvi). Backup es com tenir les fotografies dels cotxes al núvol. Si els dos cotxes son robats, les fotografies son al núvol. Si nomes tens un cotxe (RAID = 1, no mirror), no tens res.

**Al BernatLab**: molta gent fa servir la RPi amb una microSD i un SSD USB. El SSD te una copia? Si no, considera posar-ne dos en RAID 1 (amb `mdadm` o ZFS). I encara mes important: backup al núvol.

---

## Pregunta 14 (oberta): Politica de backup per a Hort Osona

**Resposta model**:

Per a l'stack Hort Osona amb Ollama, ChromaDB, Open WebUI i InfluxDB, l'analisi de criticitat de cada component:

**Ollama (models LLM)**:
- Criticitat: BAIXA. Els models es poden tornar a baixar amb `ollama pull`.
- Backup: NO cal.
- Justificacio: cada model es 4-30 GB. Fer backup d'ells al núvol es costos i innecesari.
- Excepcio: si descarregues models custom o els has entrenat tu, llavors si cal.

**ChromaDB (vector store)**:
- Criticitat: MITJANA-ALTA. Conte els embeddings dels documents Hort Osona. Es pot regenerar (reindexar) pero triga 30 min.
- Backup: setmanal, amb retencio de 4 setmanes.
- Eina: `docker exec chromadb tar czf /backup/chromadb-$(date +%F).tar.gz /chroma`. O un script dedicat.
- Validacio: que es pugui muntar i llegir.

**Open WebUI (configuracio i historial)**:
- Criticitat: MITJANA. Conte configuracio personalitzada, historials de conversa, usuaris.
- Backup: diari, nomes la base de dades SQLite.
- Eina: copiar `/app/backend/data/webui.db` (es nomes uns MB).

**InfluxDB (dades de sensors)**:
- Criticitat: ALTA si els sensors son de produccio. MITJANA si son experimentals.
- Backup: diari amb retencio de 30 dies, exportacio a CSV setmanal.
- Eina: `influx backup` (oficial).
- Validacio: poder restaurar i llegir les ultimes 24 h.

**Script d'indexacio (codi Python)**:
- Criticitat: ALTA pero ja esta a Git.
- Backup: N/A (versionat a Git).

**Resum de la politica**:

| Component | Criticitat | Freq | Retencio | Eina |
|---|---|---|---|---|
| Ollama | Baixa | Mai | - | - |
| ChromaDB | Mitjana | Setmanal | 4 setmanes | tar.gz |
| Open WebUI | Mitjana | Diari | 30 dies | cp webui.db |
| InfluxDB | Alta | Diari | 30 dies | influx backup |
| Codi indexacio | Alta | Git | Infinit | git push |

**Validacio**: una vegada al mes, restaura ChromaDB en un entorn de test i comprova que el sistema RAG funciona correctament. Això et dona la confiança que els backups son utils.

---

## Pregunta 15 (oberta): Privacitat dels backups al núvol

**Resposta model**:

Fer backups al núvol de dades sensibles te implicacions importants que cal considerar:

**Riscos de pujar dades al núvol**:

1. **El proveidor te acces**: Backblaze, AWS S3, Google Cloud, tots tenen tecnicament la capacitat d'accedir a les teves dades. Encara que la politica digui que no ho fan, hi ha casos documentats on s'ha accedit per ordre judicial o per accident.

2. **Vulnerabilitats del proveidor**: si el proveidor te una bretxa de seguretat (cosa que pasa), les teves dades queden exposades.

3. **Compliance**: si les dades son d'un client o d'un treball (no personal), pujar-les al núvol pot ser una violacio de GDPR o altres normatives.

4. **Transferencia internacional**: les dades viatgen per la xarxa i poden passar per servidors en altres paisos. Algunes normatives ho regulen.

**Solucions**:

**1. Xifrat local abans de pujar**:
- Restic xifra per defecte amb AES-256. La clau la defines tu.
- BorgBackup tambe permet xifrat.
- La clau d'encriptacio ha d'estar guardada **fora** del backup (altrament no pots recuperar).
- Avantatge: encara que el proveidor sigui compromes, les dades son illegibles.

**2. Xifrat manual amb GPG**:
- `tar czf - /path | gpg -c --cipher-algo AES256 > backup.tar.gz.gpg`
- Control total, pero mes manual.

**3. Només dades no sensibles al núvol**:
- Els documents de feina al núvol (xifrats), les fotos personals nomes local.
- Trade-off: en cas de desastre, perds les fotos personals.

**4. No usar núvol public**:
- Usar una maquina propia a casa d'un amic o familiar.
- O un NAS remot amb VPN.
- Mes control pero mes feina.

**Recomanacio al BernatLab**:

- **Restic amb `--encryption-mode repokey`**: xifrat fort amb clau que nomes tu tens.
- **Guardar la clau al password manager** (Bitwarden, KeePass) **i impresa en paper** en un lloc segur (caixa forta). Si perds la clau, no pots recuperar res.
- **Restrictir el que puges al núvol**: nomes dades que poden ser llegides per un atacant sense consequencies greus. El DNI escanejat, millor en local.
- **Politica de retencio agressiva al núvol**: nomes 30 dies, no pas 10 anys. Menys exposicio.

**Exemple de configuracio Restic**:

```bash
restic -r b2:bucket-name:/bernatlab backup /home/pi/important \
    --encryption-mode repokey \
    --tag important \
    --exclude-file=exclude.txt
```

Aixo puja les dades xifrades amb AES-256 a Backblaze B2. La clau es la que poses al `restic init` i l'has de guardar be.

---

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum i fer l'exercici practic.
- **3-4 encerts**: Refes l'exercici posant mes atencio a la verificacio.
- **0-2 encerts**: Repassem. Els backups son basics i critics.

## Que fer si has encertat totes

- Passa al **Capitol 9** (monitoritzacio).
- Configura borgbackup o restic al BernatLab real.
- Prova de restaurar des del núvol (disaster recovery real).
