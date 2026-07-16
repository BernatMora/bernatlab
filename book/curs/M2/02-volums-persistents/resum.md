# Resum - Capitol 2: Volums persistents

## La idea clau

Els contenidors son **volatils per disseny**. Si apagues un contenidor, tot el que hi havia a dins desapareix: fitxers, base de dades, configuracio. Això esta be per a serveis stateless, pero es un desastre si vols guardar res. Els **volums** son la solucio: espai d'emmagatzematge que viu **fora** del contenidor.

## Per que els contenidors son volatils

Docker agrupa tot el sistema de fitxers d'un contenidor en una "capa escribible" que es lligada a la vida del contenidor. Quan fas `docker rm`, aquesta capa desapareix. Si vols que les dades sobrevisquin, cal muntar alguna cosa desde fora.

```
Contenidor (volatile)         Emmagatzematge extern (persistent)
+---------------------+        +---------------------+
| /app/data -> buit   |   -->  | Volum o bind mount  |
| log, db, uploads    |        | viu a l'amfitrio    |
+---------------------+        +---------------------+
```

## Tipus de volums

Docker te tres mecanismes principals per persistir dades:

### 1. Volums nomenats (named volumes)

Docker els gestiona ell. Viuen a `/var/lib/docker/volumes/` a l'amfitrio.

```bash
# Crear un volum
docker volume create dades-meves

# Usar-lo
docker run -v dades-meves:/app/data nginx

# Llistar volums
docker volume ls

# Inspeccionar
docker volume inspect dades-meves
```

**Avantatges**: Docker els gestiona (backup, neteja, etc.). Son portables. Es la opcio recomanada per defecte.

### 2. Bind mounts

Muntes una carpeta **concreta** del sistema amfitrio dins el contenidor.

```bash
docker run -v /home/pi/photos:/app/photos nginx
# o amb sintaxi nova
docker run --mount type=bind,source=/home/pi/photos,target=/app/photos nginx
```

**Avantatges**: veus els fitxers desde l'amfitrio, pots editar-los amb qualsevol eina.
**Desavantatges**: depen de l'estructura de l'amfitrio. Menys portable.

### 3. tmpfs mounts

Viuen nomes a la **memoria RAM**. S'utilitzen per a dades temporals que no vols que toquin el disc (caches, fitxers sensibles).

```bash
docker run --tmpfs /tmp nginx
```

**Avantatges**: rapidissim. No toca el disc. No persisteix res (perfecte per secrets).
**Desavantatges**: ocupa RAM. Es perd en reiniciar.

## Quan usar cada un

A la practica del BernatLab:

| Cas | Tipus | Exemple |
|---|---|---|
| Base de dades | Volum nomenat | `/var/lib/postgresql/data` |
| Configuracio editable | Bind mount | `/home/pi/config/app.conf` |
| Codi font en dev | Bind mount | `/home/pi/projekte:/app` |
| Cache de imatges | Volum nomenat o tmpfs | depen |
| Secrets temporals | tmpfs | claus SSH dins un contenidor |

Regla simple: **per dades de servei, volum nomenat. Per coses que vols tocar desde l'amfitrio, bind mount.**

## Drivers de volums

Per defecte Docker usa el driver `local` (tot viu a la mateixa maquina). Pero hi ha drivers per emmagatzematge distribuït:

- **local**: per defecte.
- **nfs**: muntatges NFS (una mica antic pero funciona).
- **cifs/smb**: carpetes compartides Windows.
- **cloud**: aws-ebs, gcp-pd, azure-disk. Per Kubernetes al núvol.

A la RPi del BernatLab fem servir nomes `local` perque tenim un sol node. Si tingues un cluster, canviaries a un driver distribuït.

## Backup de volums

Un volum es nomes una carpeta a `/var/lib/docker/volumes/`. Per fer-ne backup:

```bash
# Metode simple: crear un contenidor temporal que munta el volum
docker run --rm -v dades-meves:/data -v $(pwd):/backup \
  alpine tar czf /backup/dades-meves.tar.gz -C /data .
```

Aixo empaqueta el volum en un `.tar.gz` que pots desar on vulguis. Automaticar-ho amb cron ja es un altre tema (veure capitol 8).

## Volums a Docker Compose

A `docker-compose.yml` es defineixen els volums a dalt i es muntant als serveis:

```yaml
version: "3.8"
services:
  postgres:
    image: postgres:16
    volumes:
      - db-data:/var/lib/postgresql/data  # volum nomenat
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql  # bind mount
volumes:
  db-data:  # Docker el crea automaticament
```

## Inspeccio i neteja

```bash
# Veure tots els volums i la seva mida
docker system df -v

# Esborrar volums no usats
docker volume prune

# Compte! Mai facis --rm en un volum amb dades importants
```

## Connexions amb altres capitols

- **M2 Cap 1** - Les imatges son volums de lectura; els volums persistents son d'escriptura.
- **M2 Cap 4** - Compose gestiona volums de forma declarativa.
- **M2 Cap 8** - Estrategies de backup automatitzat.
- **M2 Cap 9** - Monitoritzar l'espai de disc dels volums.
