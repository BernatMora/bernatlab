# Exercici pràctic — Capítol 5: Docker des de zero

> 60-75 min · Real al teu sistema

## Objectiu

Instal·lar Docker a la RPi, practicar les ordres bàsiques amb contenidors simples, muntar el teu primer `docker-compose.yml` amb un parell de serveis, i aprendre a gestionar el cicle de vida complet d'un contenidor.

## Requisits
- RPi accessible per SSH
- 60-75 minuts
- ~1 GB d'espai lliure a la SD

## Pas 1: Instal·la Docker (10 min)

```bash
# Script oficial d'instal·lació
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Afegeix el teu usuari al grup docker (per no haver de fer sudo sempre)
sudo usermod -aG docker bernat
newgrp docker

# Comprova
docker --version
docker compose version
docker run hello-world
```

`hello-world` és un contenidor de prova que imprimeix un missatge i surt. Si el veus, Docker funciona.

Si tens errors, comprova:
- Tens connexió a Internet? `ping google.com`
- Tens espai? `df -h /`
- La RPi és ARM? Hauria de ser-ho (RPi 4 = arm64).

## Pas 2: Primera experiència amb contenidors (10 min)

```bash
# Aixeca un servidor Nginx de prova
docker run -d --name prova-nginx -p 8080:80 nginx:alpine

# Comprova
docker ps
curl http://localhost:8080
# Hauries de veure la pàgina de benvinguda d'Nginx

# Entra dins el contenidor
docker exec -it prova-nginx sh
# Dins, pots fer ls, cat, etc.
ls /usr/share/nginx/html/
cat /etc/os-release
exit

# Mira els logs
docker logs prova-nginx
docker logs -f prova-nginx  # Ctrl+C per sortir

# Estadistiques en temps real
docker stats prova-nginx
# prem Ctrl+C per sortir

# Atura i esborra
docker stop prova-nginx
docker rm prova-nginx
```

## Pas 3: Volums i persistència (10 min)

```bash
# Crea un volum
docker volume create dades-prova

# Crea un contenidor que escriu al volum
docker run -d --name writer -v dades-prova:/dades alpine sh -c "while true; do date >> /dades/log.txt; sleep 5; done"

# Mira com creix el fitxer
docker exec writer cat /dades/log.txt
sleep 15
docker exec writer cat /dades/log.txt

# On es desa al host?
docker volume inspect dades-prova | grep Mountpoint

# Para el contenidor
docker stop writer
docker rm writer

# Crea un altre contenidor que llegeix el mateix volum
docker run --rm -v dades-prova:/dades alpine cat /dades/log.txt
# Hauries de veure les dates que va escriure el primer contenidor!
```

Això demostra que el volum **persisteix** més enllà dels contenidors.

## Pas 4: Xarxes (10 min)

```bash
# Crea una xarxa
docker network create homelab-xarxa

# Crea dos contenidors a la mateixa xarxa
docker run -d --name db --network homelab-xarxa -e POSTGRES_PASSWORD=secret postgres:16-alpine
docker run -d --name web --network homelab-xarxa -p 8081:80 nginx:alpine

# Comprova que es poden resoldre per nom
docker exec web ping -c 2 db
# Hauria de respondre

# Comprova tambe el contrari
docker exec db ping -c 2 web

# Neteja
docker stop db web
docker rm db web
docker network rm homelab-xarza
```

Això demostra la **resolució de noms** automàtica de Docker: dins d'una xarxa, els contenidors es veuen pel nom.

## Pas 5: Variables d'entorn i ports (10 min)

```bash
# A vegades cal passar configuracio
docker run -d --name whoami-custom \
  -p 8082:80 \
  -e WHOAMI_NAME="BernatLab Test" \
  traefik/whoami

curl http://localhost:8082
# Hauria de retornar un JSON amb "Hostname" i el "Name" que hem posat

# Compara amb un whoami normal
docker run -d --name whoami-norm -p 8083:80 traefik/whoami
curl http://localhost:8083

# Neteja
docker stop whoami-custom whoami-norm
docker rm whoami-custom whoami-norm
```

## Pas 6: El teu primer docker-compose.yml (15 min)

Crea l'estructura de l'homelab:

```bash
mkdir -p ~/homelab/docker
cd ~/homelab/docker
nano docker-compose.yml
```

Contingut:

```yaml
version: "3.9"

services:
  whoami:
    image: traefik/whoami
    container_name: whoami
    ports:
      - "8080:80"
    restart: unless-stopped

  portainer:
    image: portainer/portainer-ce:latest
    container_name: portainer
    ports:
      - "9000:9000"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - portainer_data:/data
    restart: unless-stopped

volumes:
  portainer_data:
```

Aixeca tot:

```bash
docker compose up -d
docker compose ps

# Comprova
curl http://localhost:8080   # whoami
# A la tarda podràs entrar a Portainer via navegador

# Mira logs agregats
docker compose logs -f
# Ctrl+C per sortir

# Mira logs d'un sol servei
docker compose logs -f whoami
```

## Pas 7: Modificar el compose i veure com canvia (10 min)

Aprèn a iterar ràpid:

```bash
# Afegeix un altre servei al compose
nano docker-compose.yml
# Afegeix aquest servei nou:
#
#   hello:
#     image: nginxdemos/hello:plain-text
#     ports:
#       - "8084:80"
#     restart: unless-stopped

# Re-aplica els canvis
docker compose up -d
# Docker nomes recreara el que ha canviat

# Comprova que el nou servei esta
docker compose ps
curl http://localhost:8084

# Neteja
nano docker-compose.yml
# Esborra el servei "hello"
docker compose up -d
```

## Pas 8: Neteja i documenta

```bash
# Para tot
cd ~/homelab/docker
docker compose down

# Volums orfes (que ja no usa cap servei)
docker volume prune

# Imatges sense usar
docker image prune

# Documenta l'experiència a book/curs/M1/05-docker-des-de-zero/diari.md
```

## Validació

Has acabat si:
- [ ] Docker està instal·lat i `hello-world` funciona.
- [ ] El teu usuari pot fer `docker ps` sense sudo.
- [ ] Has creat i esborrat contenidors amb `docker run`, `stop`, `rm`.
- [ ] Has demostrat que un volum persisteix entre contenidors.
- [ ] Has vist com dos contenidors es resolen per nom dins d'una xarxa.
- [ ] Has vist com es passa una variable d'entorn a un contenidor.
- [ ] Has creat un `docker-compose.yml` i l'has aixecat amb `docker compose up -d`.
- [ ] Has afegit un servei al compose i has vist com Docker només recrea el que canvia.
- [ ] Has documentat a `diari.md`.

## Per aprofundir

- Investiga el `Dockerfile` de `nginx:alpine` a Docker Hub.
- Prova `docker stats` mentre aixeques diversos serveis.
- Llegeix sobre la diferència entre `docker-compose` (v1) i `docker compose` (v2).
- Experimenta amb `docker system prune` per netejar imatges/contenidors antics.
- Investiga `docker exec -u 0` per entrar com a root a un contenidor.
- Prova `docker inspect` sobre un contenidor o volum.
- Compara `docker top` amb `ps` dins el contenidor.

## Ves un pas més enllà

**Repte avançat: crea el teu propi contenidor "hola món"**.

En lloc d'usar una imatge de Docker Hub, crea la teva pròpia amb un Dockerfile:

```bash
mkdir -p ~/homelab/docker/el-meu-contenidor
cd ~/homelab/docker/el-meu-contenidor
nano Dockerfile
```

Contingut del Dockerfile:

```dockerfile
# Imatge base
FROM alpine:3.19

# Metadades
LABEL maintainer="bernat@hortosona.local"
LABEL description="El meu primer contenidor personalitzat"

# Instal·la curl per fer comprovacions
RUN apk add --no-cache curl

# Copia un script
COPY hola.sh /usr/local/bin/hola.sh
RUN chmod +x /usr/local/bin/hola.sh

# Comanda per defecte
CMD ["/usr/local/bin/hola.sh"]
```

Crea el script:

```bash
nano hola.sh
```

```bash
#!/bin/sh
echo "Hola des del meu contenidor personalitzat!"
echo "Avui es: $(date)"
echo "Estic corrent a: $(hostname)"
echo "IP del contenidor: $(hostname -i 2>/dev/null || echo 'desconeguda')"
```

Construeix i prova:

```bash
# Construeix la imatge
docker build -t el-meu-contenidor:1.0 .

# Mira la mida
docker images el-meu-contenidor

# Executa-la
docker run --rm el-meu-contenidor:1.0

# Puja-la al compose
cd ~/homelab/docker
nano docker-compose.yml
# Afegeix:
#   el-meu:
#     build: ./el-meu-contenidor
#     container_name: el-meu

docker compose up -d el-meu
docker compose logs el-meu
```

Has après a fer una imatge Docker personalitzada. Aquesta habilitat et servirà per a M5 (IoT) quan vulguis empaquetar els teus scripts.
