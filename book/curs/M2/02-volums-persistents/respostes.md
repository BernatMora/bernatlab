# Respostes - Capitol 2: Volums persistents

> Mira les respostes DESPRES d'haver fet el qüestionari.

## Pregunta 1: Que passa amb les dades al `docker rm`?

**Resposta correcta**: Es perden, perque la capa escribible s'elimina amb el contenidor.

**Explicacio**: Docker munta el sistema de fitxers del contenidor en un capa union file system. La capa escribible (que conte tots els canvis que ha fet el contenidor) esta lligada al contenidor. Si l'elimines, la capa desapareix i totes les dades amb ella. Per això cal un volum extern.

---

## Pregunta 2: Quin tipus per defecte?

**Resposta correcta**: Volum nomenat.

**Explicacio**: Els volums nomenats son els mes portables i els gestiona Docker. Son la opcio recomanada per defecte per a dades de servei. Els bind mounts son per a casos on vols accedir a fitxers desde l'amfitrio de manera directa.

---

## Pregunta 3: On viuen els volums?

**Resposta correcta**: A `/var/lib/docker/volumes/`.

**Explicacio**: Docker desa tots els volums gestionats per ell en aquesta ruta. Cada volum te la seva subcarpeta. Es pot veure amb `docker volume inspect <nom>` que et dona el Mountpoint exacte.

---

## Pregunta 4: Diferencia entre volum nomenat i bind mount?

**Resposta correcta**: El volum nomenat el gestiona Docker; el bind mount munta una ruta concreta de l'amfitrio.

**Explicacio**: El volum nomenat Docker el crea, l'administra i el neteja. Tu nomes dones un nom. El bind mount tu li dones una ruta absoluta de l'amfitrio i Docker la munta dins el contenidor tal qual. Son casos d'us diferents.

---

## Pregunta 5: Quan usar tmpfs?

**Resposta correcta**: Per a dades temporals que vols nomes en RAM (caches, secrets).

**Explicacio**: tmpfs viu a la memoria RAM, no toca el disc. Es rapidissim pero volatil. Es perfecte per caches temporals o secrets que no vols que quedin al sistema de fitxers. Mai per a dades importants.

---

## Pregunta 6: Comanda per llistar volums?

**Resposta correcta**: `docker volume ls`.

**Explicacio**: Docker te comandes separades per cada tipus de recurs: `docker container ls`, `docker image ls`, `docker volume ls`, `docker network ls`. Totes segueixen el mateix patro.

---

## Pregunta 7: Bind mount correcte?

**Resposta correcta**: `docker run -v /home/pi/photos:/app/photos nginx`.

**Explicacio**: La sintaxi `-v` (o `--volume`) te la forma `host_path:container_path`. Per un volum nomenat, nomes poses el nom. Per tmpfs, usaries `--tmpfs`. Algunes banderes modernes (--mount) son mes explicites pero la forma `-v` encara es la mes comuna.

---

## Pregunta 8: Que fa `docker volume prune`?

**Resposta correcta**: Esborra tots els volums que no estan en us per cap contenidor.

**Explicacio**: Es equivalent a `docker system prune` pero nomes per volums. Compte: si tens un volum amb dades importants i no esta muntat, es podria esborrar sense avis. Sempre revisa abans amb `docker volume ls`.

---

## Pregunta 9 (oberta): Per que volatil i consequencies

**Resposta model**:

Un contenidor Docker es **volatil** per disseny perque Docker munta el sistema de fitxers del contenidor en una "capa escribible" (escriptura sobre lectura) que esta lligada al cicle de vida del contenidor. Quan fas `docker stop` o `docker rm`, Docker elimina aquesta capa i totes les dades que s'hi havien escrit dins el contenidor es perden per sempre.

La **consequencia practica** es greu si no fas servir volums. Per exemple, al BernatLab tinc un Nextcloud amb totes les meves fotos i documents. Si el configuressim **sense** volums, les pujades de fitxers anirien a la capa escribible del contenidor. Si un dia actualitzo la imatge, fes una nova build o simplement rebo la RPi, totes les dades desapareixerien. Hauria de tornar a pujar centenars de fitxers.

Amb una base de dades encara es pitjor: si el PostgreSQL del BernatLab no tingues un volum muntat a `/var/lib/postgresql/data`, qualsevol reinici del contenidor esborraria totes les taules, usuaris, indexs. Tornaries a tenir una base de dades buida i hauries de restaurar un backup (si en tens).

Per això la **primera regla** quan poses qualsevol servei en marxa es: identifica on desa les dades i munta un volum allà. Sense volums, un contenidor es nomes un "juguet" per a proves.

---

## Pregunta 10 (oberta): Servidor de fotos al BernatLab

**Resposta model**:

Per a un servidor de fotos com Immich o PhotoPrism al BernatLab, usaria una **combinacio** de volum nomenat i bind mount, segons el cas:

**Per a les fotos originals** (que poden ser 50-200 GB): usaria un **bind mount** a una carpeta de l'amfitrio com `/home/pi/fotos/`. Per que?
- Les fotos viuen a un disc extern SSD que es munta a `/home/pi/fotos/`. Es on ja les tinc organitzades per any/mes.
- Vull poder veure-les i editar-les desde l'amfitrio (amb un script, File Manager, etc.) sense entrar al contenidor.
- Vull poder fer backup de la carpeta sencera amb `rsync` cap a un altre disc, independentment de Docker.
- El rendiment es millor perque es un accès directe al sistema de fitxers, no passa per la capa Docker.

**Per a la base de dades** (que es petita, pocs MB): usaria un **volum nomenat** com `immich-db`. Per que?
- Docker el gestiona: el puc fer backup amb un sol `tar` (com hem vist a l'exercici).
- Es mes facil de moure a un altre host: nomes cal copiar `/var/lib/docker/volumes/immich-db/`.
- No necessito accedir-hi desde fora: la base de dades nomes la toca el contenidor d'Immich.

**Per a la configuracio** (`config.json`, `.env`): un **bind mount** a una carpeta de `/home/pi/config/immich/` per poder-la editar facilment amb un editor de text.

**Resum de l'estrategia**:
```
/home/pi/fotos/        -> bind mount -> /usr/src/app/upload
volum "immich-db"      -> volum nomenat -> /var/lib/postgresql/data
/home/pi/config/immich/ -> bind mount -> /etc/immich
```

Aixi cada cosa te el tractament adequat: les dades grosses al bind mount (peraccio directa), la base de dades a un volum nomenat (per backups senzills), i la configuracio accessible.

---

## Pregunta 11 (oberta): Per que els volums son una capa d'abstraccio

**Resposta model**:

Docker va triar dissenyar els volums com a capa d'abstraccio a sobre del sistema de fitxers de l'amfitrio per resoldre quatre problemes practics:

1. **Permisos entre UID del contenidor i de l'amfitrio**: si munto directament `/home/pi/photos` al contenidor, el UID del procés dins el contenidor (sovint 33 per www-data) pot no tenir permisos d'escriptura. Els volums nomenats permeten a Docker gestionar aixo transparentement.

2. **Portabilitat entre sistemes operatius**: un bind mount a `/home/pi/photos` nomes funciona a Linux. A Windows o Mac les rutes son diferents. Els volums nomenats son independents del sistema de fitxers de l'amfitrio: `volum-db:/var/lib/postgresql/data` funciona igual a tot arreu.

3. **Eines de backup consistents**: Docker pot fer un backup consistent del volum garantit que nomes es captura quan el volum no esta en us. Un bind mount es nomes una carpeta de l'amfitrio i pot estar sent modificada en qualsevol moment.

4. **Evitar perdre dades per accident**: si un script esborra `/home/pi/fotos/`, tot es perd. Els volums nomenats viuen a `/var/lib/docker/volumes/` i nomes Docker els gestiona; no es toquen facilment per accident.

Aixo es el que es coneix com el principi de "abstraccio del emmagatzematge" (storage abstraction). Es el mateix principi que en programacio: no acoblar-se als detalls de la maquina.

---

## Pregunta 12 (oberta): Volums i estrategia de backup

**Resposta model**:

L'eleccio entre volum nomenat i bind mount afecta directament la teva estrategia de backup. Si tens una hora per configurar el BernatLab i vols minimitzar la feina futura, triaria aquesta estrategia:

1. **Volums nomenats per a totes les dades d'aplicacio**: PostgreSQL, MariaDB, Nextcloud data, InfluxDB, etc. Raons: `docker volume ls` et dona tots els volums, pots fer un loop que els empaqueti tots amb un script, i el backup es consistent. Per exemple, un script que faci `for vol in $(docker volume ls -q); do docker run --rm -v $vol:/data -v /backups:/backup alpine tar czf /backup/$vol.tar.gz /data; done`.

2. **Bind mounts nomes per a coses que necessites accedir des de l'amfitrio**: configuracio, scripts personals, fotos originals. Raons: els vols editar amb un editor normal, accedir per SMB, o compartir amb altres serveis.

3. **Volum centralitzat per a backups**: un volum anomenat `backups` que esta montat a tots els contenidors de backup. Aixi s'escriuen tots al mateix lloc i es poden sincronitzar al núvol amb rsync/restic.

4. **Documentar la ubicacio de cada volum**: un `README` al costat del `docker-compose.yml` que digui "volum db: conte la base de dades PostgreSQL, fer backup diari, retenir 7 dies". D'aqui un any, ho agrairas.

Aquesta estrategia et permet fer un backup complet del BernatLab amb una sola ordre i restaurar en un altre maquina nomes copiant els volums i el compose.

---

## Pregunta 13 (oberta): Argumentar contra `docker cp`

**Resposta model**:

Si un company em digues que guarda les dades amb `docker cp`, li explicaria els riscos amb aquesta analogia: es com guardar els diners a la butxaca d'una jaqueta que pots llençar a la rentadora en qualsevol moment.

**Risques concrets**:

1. **Contenidor corromput**: si el contenidor no arranca, no pots fer `docker cp` perque el contenidor no existeix. Les dades queden inaccessible. En canvi, un volum nomenat esta al sistema de fitxers de l'amfitrio, accessible sempre.

2. **Actualitzacio de la imatge**: si fas `docker pull nextcloud:28` i el contenidor antic es substituit, les dades son a la capa escribible del contenidor antic que s'ha eliminat. Amb volum, fas `docker run -v nextcloud-data:/var/www/html/data nextcloud:28` i les dades continuen allà.

3. **Esborrat accidental**: `docker rm nextcloud` esborra el contenidor i amb ell la capa escribible. Bye-bye dades. Amb volum, `docker rm` nomes toca el contenidor, no pas el volum.

4. **No es pot fer backup consistent**: `docker cp` copia fitxer a fitxer mentres el contenidor esta actiu. Pot capturar estats inconsistents. Els volums es poden backupar amb el contenidor aturat (`docker stop` + tar) o amb eines com `restic` que garanteixen consistència.

5. **Portabilitat zero**: si vols moure les dades a una altra maquina, amb `docker cp` has de fer un altre cop. Amb volum, nomes cal moure la carpeta `/var/lib/docker/volumes/nextcloud-data/`.

L'alternativa robusta es: volum nomenat per a les dades + `docker run` amb `-v` o `docker-compose.yml` amb `volumes:`. Es la mateixa complexitat que `docker cp` pero molt mes segur.

---

## Pregunta 14 (oberta): Estrategia de volums per a 4 serveis del BernatLab

**Resposta model**:

Per a aquests quatre serveis, l'estrategia de volums seria:

**Nextcloud (fitxers dels usuaris)**:
- **Volum nomenat** `nextcloud-data` mapat a `/var/www/html/data`.
- Justificacio: les dades son critiques (irreemplaçables) i el volum es pot fer backup amb `restic` o un script tar. Mida esperada: 5-100 GB.
- **Volum nomenat** separat `nextcloud-config` per a `/var/www/html/config` (aixo es nomes uns pocs fitxers PHP).
- **Volum nomenat** `nextcloud-db` per a la base de dades (si es SQLite dins el propi contenidor, en cas contrari va a part).

**PostgreSQL (base de dades)**:
- **Volum nomenat** `postgres-data` mapat a `/var/lib/postgresql/data`.
- Justificacio: nomes es gestiona amb `pg_dump` per backup logic, pero el volum es la "font de veritat" per si cal reinicialitzar.
- **Volum nomenat** `postgres-config` per a `/etc/postgresql`.
- Mida esperada: 1-10 GB.

**InfluxDB (metriques de sensors)**:
- **Volum nomenat** `influxdb-data` mapat a `/var/lib/influxdb2`.
- Justificacio: pot créixer molt amb el temps (cada sensor genera punts). Cal poder-lo inspeccionar o netejar.
- Politica de retencio: 90 dies dins InfluxDB, despres els snapshots van al backup.
- Mida esperada: 1-50 GB.

**Ollama (models LLM)**:
- **Volum nomenat** `ollama-data` mapat a `/root/.ollama`.
- Justificacio: els models son grans (4-30 GB cadascun) i es poden tornar a baixar, pero la descarrega es lenta. Mantenir-los al volum evita haver-los de rebaixar.
- **NO cal fer backup** dels models: es poden recuperar amb `ollama pull`.
- Mida esperada: 10-50 GB.

**Estrategia global**: tots els volums son nomenats i es listen amb `docker volume ls`. Un script de backup pot fer un tar.gz de cada un i pujar-lo al núvol. La configuracio de cada servei (compose) esta a Git.

---

## Pregunta 15 (oberta): Bind mounts vs volums nomenats en seguretat

**Resposta model**:

Els bind mounts exposen rutes de l'amfitrio directament al contenidor. Si un atacant compromet el proces dins el contenidor, pot accedir a tots els fitxers de la ruta montada (i sovint mes, si te permisos elevats). Aixo es un risc de seguretat significatiu.

**Risques dels bind mounts**:
- Un exploit a Nextcloud pot accedir a `/home/pi/photos/` i totes les subcarpetes.
- Si el bind mount es al directori `/home/pi` (per compartir config), pot accedir a les teves claus SSH, configuracio, etc.
- Els permisos de fitxers (UID/GID) son visibles i manipulables.

**Avantatges dels volums nomenats**:
- Aillament: nomes veu el volum, no pas altres carpetes de l'amfitrio.
- Permisos controlats per Docker: el daemon gestiona els UID.
- Un atacant nomes pot accedir al volum especific, no a tot `/home/pi`.

**Excepcio**: els bind mounts en **read-only** son relativament segurs. Pots muntar `/home/pi/photos:/photos:ro` i el contenidor nomes pot llegir, no escriure ni esborrar. Es perfecte per a casos com la lectura d'imatges per a un visor.

**Recomanacio al BernatLab**:
- Volums nomenats per defecte per a totes les dades dinamiques.
- Bind mounts nomes quan calgui editar des de l'amfitrio o quan calgui read-only.
- Mai bind mounts a directoris pares (`/home/pi`, `/`).
- Usar `:ro` sempre que el cas d'us ho permeti.

Aixi, encara que un servei sigui compromes, l'impacte queda limitat al seu volum.

---

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum i fer l'exercici practic.
- **3-4 encerts**: Refas l'exercici amb mes atencio a cada pas.
- **0-2 encerts**: Repassem el capitol abans de continuar; els volums son basics.

## Que fer si has encertat totes

- Passa al **Capitol 3** (xarxes Docker).
- Investiga els volums en lectura-escriptura compartida entre multiples hosts.
- Llegeix sobre els "CSI drivers" (Container Storage Interface), pero ja es nivell Kubernetes.
