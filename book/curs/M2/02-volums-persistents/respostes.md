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

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum i fer l'exercici practic.
- **3-4 encerts**: Refas l'exercici amb mes atencio a cada pas.
- **0-2 encerts**: Repassem el capitol abans de continuar; els volums son basics.

## Que fer si has encertat totes

- Passa al **Capitol 3** (xarxes Docker).
- Investiga els volums en lectura-escriptura compartida entre multiples hosts.
- Llegeix sobre els "CSI drivers" (Container Storage Interface), pero ja es nivell Kubernetes.
