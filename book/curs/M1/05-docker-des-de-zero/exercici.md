# Exercici pràctic — Capítol 5: Docker des de zero

> 40-60 min · Real al teu sistema

## Objectiu
Instal·lar Docker a la RPi, practicar les ordres bàsiques amb contenidors simples, i muntar el teu primer `docker-compose.yml` amb un parell de serveis.

## Requisits
- RPi accessible per SSH
- 40-60 minuts
- ~500 MB d'espai lliure a la SD

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
exit

# Mira els logs
docker logs prova-nginx
docker logs -f prova-nginx  # Ctrl+C per sortir

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

# Neteja
docker stop db web
docker rm db web
docker network rm homelab-xarxa
```

## Pas 5: El teu primer docker-compose.yml (15 min)

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
```

## Pas 6: Neteja i documenta

```bash
# Para tot
cd ~/homelab/docker
docker compose down

# Documenta l'experiència a book/curs/M1/05-docker-des-de-zero/diari.md
```

## Validació

Has acabat si:
- [ ] Docker està instal·lat i `hello-world` funciona.
- [ ] El teu usuari pot fer `docker ps` sense sudo.
- [ ] Has creat i esborrat contenidors amb `docker run`, `stop`, `rm`.
- [ ] Has demostrat que un volum persisteix entre contenidors.
- [ ] Has vist com dos contenidors es resolen per nom dins d'una xarxa.
- [ ] Has creat un `docker-compose.yml` i l'has aixecat amb `docker compose up -d`.
- [ ] Has documentat a `diari.md`.

## Per aprofundir

- Investiga el `Dockerfile` de `nginx:alpine` a Docker Hub.
- Prova `docker stats` mentre aixeques diversos serveis.
- Llegeix sobre la diferència entre `docker-compose` (v1) i `docker compose` (v2).
- Experimenta amb `docker system prune` per netejar imatges/contenidors antics.
