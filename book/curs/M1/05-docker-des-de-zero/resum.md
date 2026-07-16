# Resum — Capítol 5: Docker des de zero

## La idea clau

**Docker** és l'eina que fa possible el BernatLab. En lloc d'instal·lar programes directament a la Raspberry Pi (que ompliria la SD i crearia conflictes), cada servei corre dins d'un **contenidor**: una capsa aïllada amb el programa i totes les seves dependències, que es pot aixecar, parar, moure o esborrar en segons.

Al cap del capítol sabràs crear contenidors, gestionar volums i xarxes, i definir tot l'homelab amb un sol fitxer `docker-compose.yml`.

## Què és un contenidor?

Pensa en un contenidor com un **apartament dins d'un edifici**. L'edifici és el sistema operatiu (Debian 13). Cada apartament té:

- El seu propi sistema de fitxers (amb el programa i llibreries).
- La seva pròpia interfície de xarxa.
- Els seus propis processos.
- La seva pròvida quantitat de CPU/RAM assignada.

Els apartaments comparteixen el mateix edifici (kernel Linux), però estan totalment aïllats entre ells. Si un contenidor es penja, no afecta la resta.

## Imatges vs contenidors

**Imatge** = plantilla de només lectura (la "receta" o "foto" del pis).
**Contenidor** = instància viva d'una imatge (el pis real on algunes hi viu).

Analogia: una imatge és un .ISO de Linux; el contenidor és la màquina virtual corrent.

```bash
# Descarregar una imatge (no baixa res si ja la tens)
docker pull nginx:1.27-alpine

# Llistar imatges descarregades
docker images
# REPOSITORY   TAG       IMAGE ID       CREATED       SIZE
# nginx        1.27-alpine  abc123...    2 weeks ago   43MB

# Crear un contenidor a partir d'una imatge
docker run -d --name web -p 8080:80 nginx:1.27-alpine
# -d = detached (en segon pla)
# --name web = li donem un nom
# -p 8080:80 = port 8080 del host -> port 80 del contenidor
```

## Comandes bàsiques de contenidors

```bash
docker ps                 # contenidors actius
docker ps -a              # tots els contenidors (inclosos els aturats)
docker logs web           # veure logs
docker logs -f web        # seguir logs en temps real
docker stop web           # aturar
docker start web          # arrencar
docker restart web        # reiniciar
docker rm web             # esborrar (cal estar aturat)
docker rm -f web          # forçar (atura i esborra)
docker stats              # ús de CPU/RAM en temps real
docker exec -it web sh    # entrar dins el contenidor (shell)
```

## Volums: on viuen les dades

Per defecte, quan esborres un contenidor, **es perden totes les dades** que hagi creat. Per persistir-les (bases de dades, configuracions, pujades), usem **volums**:

```bash
# Volum nombrat (Docker el gestiona)
docker volume create dades-portainer
docker run -d -p 9000:9000 -v dades-portainer:/data portainer/portainer-ce

# Muntar una carpeta del host
docker run -d -p 8080:80 -v /home/bernat/homelab/web:/usr/share/nginx/html nginx
```

Hi ha tres formes de persistir dades:

1. **Volums nombrats** (`docker volume create`): Docker els gestiona, ruta interna `/var/lib/docker/volumes/...`. Recomanat.
2. **Bind mounts** (`-v /path/host:/path/contenidor`): tu tries la ruta del host. Molt flexible però menys portable.
3. **Tmpfs**: a memòria RAM, s'esborra en parar. Per a dades temporals o sensibles.

## Xarxes Docker

Per defecte, els contenidors poden parlar entre ells per una xarxa interna. Hi ha tres xarxes predefinides:

- `bridge` (per defecte): aïlla contenidors en xarxes privades.
- `host`: el contenidor veu directament la xarxa del host.
- `none`: sense xarxa.

Crea xarxes personalitzades:

```bash
docker network create homelab
docker run -d --network homelab --name db postgres:16
docker run -d --network homelab --name portainer -p 9000:9000 portainer/portainer-ce

# Ara portainer pot accedir a la db amb el nom "db"
```

Això permet posar noms en lloc d'IPs. A `docker-compose.yml` és on ho aprofitarem.

## Docker Compose: el tot-en-un

Imagina aixecar 8 serveis un a un amb `docker run`. Massa complicat. **Docker Compose** ho resol amb un fitxer YAML:

```yaml
# ~/homelab/docker/docker-compose.yml
version: "3.9"

services:
  portainer:
    image: portainer/portainer-ce:latest
    container_name: portainer
    ports:
      - "9000:9000"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - portainer_data:/data
    restart: unless-stopped

  uptime:
    image: louislam/uptime-kuma:latest
    container_name: uptime-kuma
    ports:
      - "3001:3001"
    volumes:
      - uptime_data:/app/data
    restart: unless-stopped

volumes:
  portainer_data:
  uptime_data:
```

Ordres clau:

```bash
cd ~/homelab/docker
docker compose up -d          # aixeca tot en segon pla
docker compose down           # para i esborra tot
docker compose ps             # estat dels serveis
docker compose logs -f        # logs agregats
docker compose logs -f portainer  # logs d'un servei
docker compose pull           # actualitza imatges
docker compose up -d          # aplica canvis (recrea si cal)
```

## Dockerfile: les teves pròpies imatges

Quan vulguis empaquetar la teva pròpia aplicació:

```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install --production
COPY . .
EXPOSE 3000
CMD ["node", "index.js"]
```

Construeix i puja:

```bash
docker build -t bernat/la-meva-app:1.0 .
docker run -d -p 3000:3000 bernat/la-meva-app:1.0
```

Al BernatLab no en farem servir gaire (tot seran imatges ja fetes), però és útil saber-ho per si més endavant vols allotjar scripts o webs pròpies.

## Bones pràctiques

1. **Un servei per contenidor**: no posis dues apps al mateix contenidor.
2. **Imatges Alpine quan sigui possible**: ocupen 5-10 vegades menys (43 MB vs 180 MB).
3. **Volums per a dades**: mai confiïs en el sistema de fitxers del contenidor.
4. **`restart: unless-stopped`**: perquè els serveis tornin sols després d'un reboot.
5. **Etiqueta les imatges amb versions**: `nginx:1.27-alpine` en lloc de `nginx:latest`.
6. **Fes servir Compose**: un sol fitxer per gestionar tot l'homelab.

## Connexions amb altres capítols

- **Cap 2 i 3** — Docker corre sobre Debian 13 a la RPi.
- **Cap 4** — Accedirem als serveis via Tailscale.
- **Cap 6** — Portainer ens donarà una interfície gràfica per a tot això.
- **Cap 7-10** — Tots els serveis del BernatLab seran contenidors Docker.

Ja tens la peça central. Ara toca posar-hi serveis concrets.
