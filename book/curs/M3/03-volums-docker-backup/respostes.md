# Respostes — Capitol 3: Backup de volums Docker

> Mira les respostes DESPRES d'haver fet el qüestionari.

## Pregunta 1: On son els volums natius?

**Resposta correcta**: /var/lib/docker/volumes.

**Explicacio**: Docker emmagatzema els volums natius a `/var/lib/docker/volumes/<nom>/_data/`. Es poden llistar amb `docker volume ls` i inspeccionar amb `docker volume inspect <nom>`. A la RPi amb bind mounts (com al BernatLab), les dades solen estar a `/home/pi/...` i NO a `/var/lib/docker/volumes/...`.

---

## Pregunta 2: Volum natiu vs bind mount

**Resposta correcta**: Un volum natiu el gestiona Docker; un bind mount tu tries una ruta de l'amfitrio.

**Explicacio**:
- **Volum natiu** (`volumes: - mi-volum:/path`): Docker tria on guardar-lo, normalment a `/var/lib/docker/volumes/`. Tu només coneixes el nom.
- **Bind mount** (`volumes: - /home/pi/dades:/path`): tu tries exactament quina carpeta de l'amfitrio es munta al contenidor. Es mes transparent i mes facil de navegar/backup.

---

## Pregunta 3: Per que `tar` no es segur per a BD actives?

**Resposta correcta**: El backup pot quedar inconsistent (fitxers nous i vells barrejats).

**Explicacio**: Quan la base de dades esta escrivint, els fitxers de dades estan en estat inconsistent: una taula pot tenir les dades noves pero l'index encara apunta a l'estat antic. Si fas `tar` en aquest moment, captures una "instantania" incoherent. Al restaurar, la BD pot no arrencar o retornar dades corruptes. La solucio es fer un **dump logic** (pg_dump, mysqldump) que llegeix les dades de manera consistent independentment de l'estat dels fitxers.

---

## Pregunta 4: Dump de PostgreSQL en contenidor

**Resposta correcta**: `docker exec postgres pg_dump -U user database`.

**Explicacio**: `pg_dump` es l'eina estandard de PostgreSQL per fer backups logics. L'ordre completa sol ser:
```
docker exec postgres pg_dump -U bernatlab bernatlab | gzip > backup.sql.gz
```
El `|` redirigeix la sortida a gzip, que la comprimeix al vol. El resultat es un fitxer SQL comprimit que es pot restaurar amb `psql -f` o amb `cat | psql`.

---

## Pregunta 5: Metode que NO atura el contenidor

**Resposta correcta**: Muntar el volum en un contenidor temporal amb `docker run --rm`.

**Explicacio**: 
```bash
docker run --rm \
  -v grafana-data:/source:ro \
  -v /tmp/backup:/backup \
  alpine tar -czf /backup/grafana.tar.gz -C /source .
```
El contenidor original (grafana) continua funcionant. nomes aixequem un contenidor temporal que munta el volum (nomes lectura) i el comprimeix. Es ideal per backups sense temps d'aturada, pero nomes funciona amb volums natius.

---

## Pregunta 6: Que es un DR test?

**Resposta correcta**: Disaster Recovery test: provar que el backup es pot restaurar correctament.

**Explicacio**: Un DR test es la prova periodica de restauracio. Consisteix en agafar un backup, intentar restaurar-lo, i verificar que les dades son correctes. Serveix per descobrir problemes abans que sigui massa tard: el fitxer esta corrupte, falta una dependencia, el format ha canviat, etc. Al BernatLab faig un DR test un cop al trimestre com a minim.

---

## Pregunta 7: On es guarden les dades al BernatLab?

**Resposta correcta**: En bind mounts a /home/pi/bernatlab/.

**Explicacio**: Tots els serveis productius del BernatLab usen bind mounts:
- `/home/pi/bernatlab/grafana` -> Grafana
- `/home/pi/bernatlab/postgres` -> PostgreSQL  
- `/home/pi/bernatlab/nextcloud` -> Nextcloud
- etc.

Aixo permet navegar per `/home/pi/bernatlab/` i veure totes les dades, fer backup amb `tar` o `rsync` igual que qualsevol altre directori, i saber sempre on son les coses.

---

## Pregunta 8: NO es bona per fer backup de BD

**Resposta correcta**: Copiar els .db mentre el servidor escriu.

**Explicacio**: Aixo es exactament el que NO s'ha de fer. Els fitxers de la base de dades (WAL logs, taules, indexs) estan en estat inconsistent durant les escriptures. Copiar-los garanteix un backup trencat. SEMPRE s'ha d'usar l'eina de dump nativa: `pg_dump`, `mysqldump`, `sqlite3 .dump`, `influx backup`, etc.

---

## Pregunta 9 (oberta): Importancia del DR test

**Resposta model**:

Fer un backup nomes te sentit si es pot restaurar. Si nomes crees backups pero mai els proves, estas vivint en una il·lusio: el dia que necessitis restaurar, descobriraes que el fitxer esta corrupte, que el format ha canviat, que falta una dependencia, o que simplement no saps COM fer-ho.

Al BernatLab vaig descobrir fa dos anys que el meu backup de Nextcloud estava **buit**. Resulta que el bind mount havia canviat de ruta amb una actualitzacio de Docker Compose, i el backup automatic feia mesos que copiava un directori buit. Si ho hagues necessitat, hauria estat un desastre. Pero gracies a un DR test rutinari, ho vaig descobrir i vaig poder corregir la configuracio.

**Regla practica**: fes un DR test **un cop al trimestre** com a minim. Tria un dia (pot ser el primer diumenge de cada trimestre), agafa un backup, intenta restaurar-lo en un entorn aillat, i verifica les dades. Documenta el que ha funcionat i el que no. Si fallen coses, corregeix el sistema de backup abans que sigui massa tard.

**Conclusio**: un backup no provat es com un paraigua foradat. Sembla que serveix, pero el dia de la tempesta t'adones que no.

---

## Pregunta 10 (oberta): Pla de backup pel BernatLab

**Resposta model**:

| Servei | Tipus de dada | FreqUencia | Metode | Desti |
|---|---|---|---|---|
| Grafana | Configuracio + dashboards | Setmanal | `tar` del bind mount | SSD local + Backblaze B2 |
| InfluxDB | Lectures de sensors (creix) | Cada 6 hores | `influx backup` | SSD local + B2 |
| Mosquitto | Config + usuaris MQTT | Setmanal | `tar` | SSD + B2 |
| Nextcloud | Fitxers d'usuari (grans) | Cada dia | `rsync` al SSD, despres a B2 | SSD + B2 |
| PostgreSQL | Dades estructurades | Cada dia | `pg_dump | gzip` | SSD + B2 |

**Justificacio**:

- **Grafana**: son fitxers petits (~10 MB). Setmanal es suficient perque els dashboards canvien poc. Backup amb `tar` esta be perque no es una BD activa en el moment del backup (Grafana ho permet, pero millor aturar-lo uns segons per consistencia).

- **InfluxDB**: creix rapidament amb cada lectura de sensor. Faig backup cada 6 hores perque perdre 6 h de lectures es acceptable, pero perdre 24 h no. Uso `influx backup` que es l'eina consistent.

- **Mosquitto**: nomes config + usuaris. Setmanal. Es un fitxer .conf i un .passwd que ocupen kilobytes.

- **Nextcloud**: els fitxers d'usuari poden ser grans (fotos de l'hort, documents). Backup diari amb rsync es eficient perque rsync nomes copia el que ha canviat.

- **PostgreSQL**: les dades mes critiques (recollides, configuracio, etc.). Backup diari amb `pg_dump | gzip` que garanteix consistencia. Comprimeixo perque els SQL plans poden ser grans.

Tots van a parar a `/home/pi/bernatlab/backups/` i despres restic els puja al Backblaze B2 amb la politica `keep-daily 7, keep-weekly 4, keep-monthly 6`.

---

## Pregunta 11 (oberta): Volums nomenats vs bind mounts

**Resposta model**:

Docker va triar tenir volums nomenats com a abstraccio per sobre dels bind mounts per varies raons historiques i practiques:

**1. Historia**:

Quan Docker va començar, el sistema de volums era molt basic. Els desenvolupadors volien una abstraccio que funcionés igual a Linux, Mac i Windows. Els bind mounts a Windows son molt diferents (`C:\Users\pi\...` vs `/home/pi/...`). Els volums nomenats amaguen aquesta diferencia.

**2. Portabilitat del docker-compose**:

Si tens un `docker-compose.yml` amb `volumes: ["data:/var/lib/postgresql/data"]`, el mateix fitxer funciona a qualsevol maquina. Si tens `volumes: ["/home/pi/data:/var/lib/postgresql/data"]`, nomes funciona a la teva maquina.

**3. Permisos automatics**:

Quan fas un bind mount a `/home/pi/data/`, els permisos del contenidor depenen dels permisos de la carpeta a lamfitrio. Si el PID del contenidor es 70 (postgres) i la carpeta es propietat de root, tindras problemes. Els volums nomenats gestionen aixo transparent.

**4. Millor integracio amb el daemon**:

Docker pot gestionar volums nomenats mes eficientment que bind mounts. Per exemple, `docker volume prune` nomes funciona amb volums nomenats. Els volums tenen metadades que permeten millor debug.

**Inconvenients dels volums nomenats**:

Pero tambe tenen inconvenients que cal considerar:
- **Camins críptics**: `/var/lib/docker/volumes/abc123def456/_data` es dificil de recordar.
- **Cal entrar al contenidor per accedir-hi**: no pots fer `ls` desde lamfitrio sense permisos especials.
- **Mes complexe per a scripts externs**: fer backup del volum nomes es pot fer des del daemon.

**Impacte al BernatLab**:

A la practica, al BernatLab uso una barreja:
- **Volums nomenats** per a bases de dades i configuracio (Nextcloud, Postgres, InfluxDB). Docker els gestiona be.
- **Bind mounts** per a fitxers que vull accedir desde lamfitrio (fotos, scripts, configuracions personals). Es mes convenient per editar amb un editor o copiar amb rsync.

**Per al backup**, la diferencia es minima:
- Volums nomenats: `docker run --rm -v volum:/data -v /backup:/backup alpine tar czf /backup/volum.tar.gz /data`
- Bind mounts: `tar czf /backup/data.tar.gz /home/pi/bernatlab/data/`

El resultat es el mateix. Tria segons les teves necessitats.

**Conclusio**: Docker va triar volums nomenats per la portabilitat i abstraccio. Pero la decisio no es absoluta. Usa volums nomenats quan vulguis abstraccio i bind mounts quan vulguis acces directe desde lamfitrio.

---

## Pregunta 12 (oberta): Metode de backup i consistencia

**Resposta model**:

La relacio entre metode de backup i consistencia de les dades restaurades es fonamental:

**1. tar en calent (contenidor en execucio)**:

- Risc: alt. Si el contenidor esta escrivint fitxers mentre tar els llegeix, pots obtenir un backup inconsistent.
- Cas concret: una base de dades SQLite pot estar escribint un commit mentre tar copia el fitxer. El backup pot contenir una versio parcial.
- Aplicable: fitxers de configuracio que canvien poc. No per a bases de dades.

**2. pg_dump / mysqldump (dump logic)**:

- Risc: zero. Eina oficial que sap com fer un snapshot consistent usant les APIs de la BD.
- Aplicable: SEMPRE per a bases de dades.
- Limitacio: nomes captura dades, no configuracio. Cal fer un altre backup per a la configuracio.

**3. Snapshot del sistema de fitxers (LVM/ZFS)**:

- Risc: zero si es consistent. Pero cal parar el servei o fer freeze del filesystem.
- Aplicable: volums grans amb moltes dades, on tar es lent.
- Limitacio: cal hardware que ho soporti (LVM, ZFS, BTRFS).

**4. Contenidor temporal amb volum montat**:

- Risc: baix. El volum esta en us pero es un read-only mount.
- Aplicable: quan vols un tar del volum pero no pots parar el servei.
- Limitacio: el backup pot no ser consistent per a BD.

**Quan usar cada metode al BernatLab**:

| Servei | Metode recomanat | Per que |
|---|---|---|
| Nextcloud (fitxers) | Aturar + tar | Fitxers poden estar escribint |
| PostgreSQL | pg_dump | Consistent, sense parar |
| InfluxDB | influx backup | Eina oficial, consistent |
| Mosquitto | tar en calent | Configuracio, baixa freqUencia |
| Grafana | Aturar + tar | Dashboards son petits |
| Ollama | Excloure del backup | Es pot tornar a baixar |

**Cas especial: contenidor temporal**:

```bash
# Backup d'un volum sense parar el servei
docker run --rm \
    -v nextcloud-data:/source:ro \
    -v /home/pi/bernatlab/backups:/backup \
    alpine tar czf /backup/nextcloud-$(date +%F).tar.gz -C /source .
```

Aixo fa un tar del volum sense afectar el servei. Pero si el servei esta escribint (com Nextcloud), el backup pot ser inconsistent. Per aixo es millor aturar el servei per a una mica estona.

**Conclusio**: la consistencia es el mes important. Un backup inconsistent es pitjor que no tenir backup, perque creus que estas protegit quan no ho estas.

---

## Pregunta 13 (oberta): Per que `cp -r` es insuficient

**Resposta model**:

El company que diu "faig `cp -r` de la carpeta de Nextcloud cada dia, ja esta be" te una serie de riscos que pot no haver considerat:

**1. Fitxers parcials**:

Si un usuari esta pujant un fitxer de 500 MB a Nextcloud i el `cp -r` s'executa exactament en aquest moment, el backup pot contenir un fitxer parcial (250 MB d'un fitxer que en te 500). Si intentas restaurar aquest fitxer, pot ser corrupte.

**2. No es un backup amb versionat**:

Si un dimarts crees un document, el dimecres el modifiques, i el dijous vols recuperar la versio del dimarts, amb `cp -r` nomes tens la del dijous. Restic et permet tornar a qualsevol versio.

**3. Si Nextcloud es corromp, el backup tambe**:

Aixo es sutil. Si la base de dades de Nextcloud es corromp per un bug, els fitxers de dades poden quedar en un estat inconsistent. Si el `cp -r` es fa despres de la corrupcio, el backup te el mateix problema.

**Exemple real**: Nextcloud te una funcionalitat de "trash bin" que esborra fitxers realment al cap de 30 dies. Si un usuari esborra accidentalment un fitxer, esta a la paperera. Pero si el bug de Nextcloud nomes permet recuperar 50% dels fitxers de la paperera, el teu `cp -r` nomes te aquesta versio parcial.

**4. Sense deteccio de fitxers nous**:

`cp -r` sempre copia tot, encara que no hagi canviat res. Es lent i gasta espai innecesari. rsync nomes copia el que ha canviat (incremental). Restic a mes desduplica.

**5. Sense verificacio**:

`cp -r` no verifica que els fitxers s'hagin copiat correctament. Restic te `check` que verifica integritat. Si el disc te sectors defectuosos, `cp -r` no t'ho dira.

**6. Permissos poden canviar**:

Depenent de com es faci el `cp -r`, els permisos dels fitxers poden canviar. Si el procés que ho fa no es root, pot ser que alguns fitxers no es puguin restaurar correctament.

**Alternativa mes robusta al BernatLab**:

```bash
# 1. Aturar Nextcloud temporalment
docker compose stop nextcloud

# 2. Fer tar del volum
docker run --rm \
    -v nextcloud-data:/source:ro \
    -v /home/pi/backups:/backup \
    alpine tar czf /backup/nextcloud-$(date +%F).tar.gz -C /source .

# 3. Tornar a arrancar
docker compose start nextcloud

# 4. Verificar
tar tzf /backup/nextcloud-2024-01-15.tar.gz | head
```

Aixo es 10 minuts de feina pero dona un backup consistent.

**O encara millor amb restic**:

```bash
# Backup consistent amb desduplicacio
docker compose stop nextcloud
restic -r /mnt/ssd/backups backup /var/lib/docker/volumes/nextcloud-data/_data
docker compose start nextcloud
```

Aixi el backup es incremental, deduplicat, i nomes copia el que ha canviat.

---

## Pregunta 14 (oberta): Script de backup per a l'hort IoT

**Resposta model**:

Per a l'hort IoT amb InfluxDB, Grafana, Mosquitto i un script Python, un script de backup periodic podria ser:

```bash
#!/bin/bash
# Script de backup per a l'hort IoT del BernatLab
# Programar amb cron: 0 2 * * * /home/pi/scripts/backup-hort.sh

set -e  # Parar si algo falla
BACKUP_DIR="/home/pi/bernatlab/backups"
DATE=$(date +%Y-%m-%d)
LOG="/var/log/backup-hort.log"

# Funcio per log
log() {
    echo "[$(date +%H:%M:%S)] $1" >> $LOG
}

mkdir -p $BACKUP_DIR/$DATE

# 1. InfluxDB (consistent amb l'eina oficial)
log "Backup InfluxDB"
docker exec influxdb influx backup /tmp/backup
docker cp influxdb:/tmp/backup $BACKUP_DIR/$DATE/influxdb
docker exec influxdb rm -rf /tmp/backup

# 2. Grafana (configuracio + dashboards)
log "Backup Grafana"
docker compose stop grafana
docker run --rm \
    -v grafana-data:/source:ro \
    -v $BACKUP_DIR/$DATE:/backup \
    alpine tar czf /backup/grafana.tar.gz -C /source .
docker compose start grafana

# 3. Mosquitto (configuracio petita)
log "Backup Mosquitto"
docker run --rm \
    -v mosquitto-config:/source:ro \
    -v $BACKUP_DIR/$DATE:/backup \
    alpine tar czf /backup/mosquitto.tar.gz -C /source .

# 4. Script Python (esta a Git, pero per si de cas)
log "Backup scripts"
cp -r /home/pi/bernatlab/scripts/ $BACKUP_DIR/$DATE/scripts/

# 5. Pujar a Backblaze B2 amb restic
log "Pujant a Backblaze B2"
restic -r b2:bernatlab-backup:/hort \
    backup $BACKUP_DIR/$DATE \
    --tag hort-$(date +%Y%m) \
    --exclude="*.tmp"

# 6. Netejar locals antics (mantenir 7 dies)
log "Neteja local"
find $BACKUP_DIR -maxdepth 1 -type d -mtime +7 -exec rm -rf {} \;

# 7. Aplicar politica de retencio al núvol
log "Retencio al núvol"
restic -r b2:bernatlab-backup:/hort \
    forget --tag hort-$(date +%Y%m) \
    --keep-daily 7 --keep-weekly 4 --keep-monthly 6 --prune

log "Backup complet"
```

**Caracteristiques del script**:

1. **Logs centralitzats**: tot va a `/var/log/backup-hort.log`. Pots veure quan sha fet cada backup.

2. **Atura serveis per consistencia**: Grafana satura per evitar perdua de configuracio de dashboards.

3. **Repositori estructurat per data**: cada backup sha en una carpeta amb la data, facil de restaurar.

4. **Surt al primer error** (`set -e`): si algo falla, el script para. No vols un backup parcial.

5. **Automatitzat amb cron**: sha cada dia a les 2 AM. No cal recordar.

6. **Cleanup automatic**: nomes conserva 7 dies locals. La historia completa esta al núvol.

**Verificar el backup**: afegiria una línia final que faci `restic check` per verificar la integritat del backup al núvol.

**Restauracio rapida**: per restaurar, nomes cal fer `restic -r b2:... restore latest --target /tmp/restore` i copiar el que necessitis.

---

## Pregunta 15 (oberta): Per que els tests de restauracio son essencials

**Resposta model**:

Els tests de restauracio (DR tests) son la unica manera de saber si el teu backup realment funciona. Sense ells, tens una falsa sensació de seguretat. Casos reals on un backup "existent" no serveix:

**1. Backup corrupte que no es detecta fins al moment de restaurar**:

Cas real: un disc te sectors defectuosos intermitents. El backup sha creat amb exit (el sistema no sap que el contingut esta corrupte). Anys despres, intentes restaurar i el fitxer es illgible. Has estat "salvat" durant anys pero no pots recuperar res.

**2. Format de backup canviat per una actualitzacio**:

Actualitzes restic a una versio nova que canvia el format intern. Les copies antigues ja no son compatibles amb la nova versio. Sense voler restaurar una copia antiga, no ho saps.

**3. Permissos canviats que impedeixen la lectura**:

Mous el backup a una maquina nova amb un usuari diferent. Els fitxers tenen permisos 600 propietat dun usuari que no existeix. No pots accedir.

**4. Clau de xifrat perduda o mal guardada**:

El backup esta xifrat amb restic. Perds la clau (o la vas guardar al mateix disc que es va trencar). Ara el backup es un munt de bytes illegibles.

**5. Ruta absoluta en lloc de relativa**:

El backup es va fer amb camins absoluts (`/home/pi/...`). Intentes restaurar a una maquina diferent i els camins no existeixen. Cal reescriure manualment.

**6. La nova versio de la BD no pot llegir el dump antic**:

Actualitzes PostgreSQL a una versio que ja no suporta el format del dump antic. Pots perdre acces a anys de dades.

**Per que la gent no fa tests**:

- Costa temps (1-2 h per sessio).
- Es tedios (res rar pasa la majoria del cops).
- Es posposa perque "ja ho fare mes tard".
- No es prioritari fins que passa algo.

**Consequencies al BernatLab**:

Si tens un hort IoT amb 5 anys de lectures i un dia necessites restaurar, vols descobrir ALESHORES que el backup no funciona? No. Vols haver-ho verificat periodicament.

**Recomanacio practica**:

1. **Test trimestral**: un cop cada 3 mesos, restaura un element de cada tipus de backup.
2. **Documenta el proces**: escriu els passos per restaurar. Aixi no has de pensar-ho enmig del panic.
3. **Automatitza el test**: un script que cada mes fa un test de restauracio automatic i t'avisa si falla.
4. **Practica el desastre**: un cop a l'any, simula un desastre. Esborra alguna cosa i restaura-la. Veuras quant trigues i quines dificultats trobes.

**Exemple de script de test**:

```bash
#!/bin/bash
# Test de restauracio automatic
BACKUP_TEST_DIR="/tmp/restic-test"
restic -r b2:bernatlab-backup:/hort restore latest --target $BACKUP_TEST_DIR
# Verificar que els fitxers existeixen
if [ -f "$BACKUP_TEST_DIR/influxdbbackup" ]; then
    echo "OK: backup verificat" | mail -s "Test backup OK" root
else
    echo "FALLA: backup no verificat" | mail -s "ATENCIO: test backup FALLA" root
fi
rm -rf $BACKUP_TEST_DIR
```

Aquest script satura cada mes, intenta restaurar, i t'avisa. 5 min de feina que poden estalviar un desastre.

**Conclusio**: un backup no provat es un backup dubtos. Millor provar i saber que funciona, que no pas descobrir-ho quan es massa tard.

---

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum.
- **3-4 encerts**: Rellegeix el capitol amb atencio, sobretot la seccio de backups consistents.
- **0-2 encerts**: Repassem junts el capitol. Es la base per als proxims 7 capitols del modul M3.

## Que fer si has encertat totes

- Passa al **Capitol 4** (SQLite).
- O fes l'**exercici practic** amb un Postgres real per consolidar.
