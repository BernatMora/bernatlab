# Capítol 61 — Docker i Portainer: la base dels serveis

> *"Si has d'instal·lar una sola aplicació al teu servidor, fes-ho amb Docker. Si n'has d'instal·lar vint, fes-ho també amb Docker. La diferència és que amb la següent opció, vint aplicacions esdevenen un infern de dependències. Amb Docker, segueixen sent vint aplicacions, però cadascuna en una capsa."*

## 61.1 Què aprendràs

- Què és Docker i per què serveix.
- Com instal·lar Docker i Docker Compose.
- Com instal·lar Portainer.
- Com crear el teu primer contenidor.
- Com organitzar els teus serveis amb `docker-compose`.

## 61.2 Durada estimada

30-45 minuts.

## 61.3 Per què Docker

A la Raspberry, si instal·léssim cada aplicació directament (`apt install grafana`, `apt install mosquitto`...), tindríem un món de:

- Versions barrejades.
- Conflictes de dependències.
- Dificultat per actualitzar.
- Dificultat per reproduir la instal·lació en una altra màquina.

Docker ho soluciona tot. Cada aplicació va en un **contenidor** que conté:

- El codi.
- Les llibreries.
- La configuració.
- Tot el que necessita per funcionar.

I aquests contenidors **no es barregen entre ells**. Pots tenir 20 contenidors corrent simultàniament, cadascun amb les seves pròpies dependències, sense conflictes.

Si alguna cosa falla, esborres el contenidor i el tornes a crear. Com si fos nova.

## 61.4 Instal·lar Docker

Docker ja ve preparat per a Debian. A la RPi:

```bash
# Script oficial d'instal·lació
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
rm get-docker.sh
```

Afegeix el teu usuari al grup `docker` per no haver de fer servir `sudo` cada vegada:

```bash
sudo usermod -aG docker bernat
```

Tanca la sessió SSH i torna a entrar perquè el canvi tingui efecte:

```bash
exit
ssh bernat@hortosona
```

Verifica:

```bash
docker --version
docker compose version
docker run hello-world
```

L'últim comanda descarrega una imatge de prova i l'executa. Si funciona, tens Docker correctament instal·lat.

## 61.5 Instal·lar Portainer

**Portainer** és una interfície web per gestionar Docker. Per a un homelab és perfecta: pots veure contenidors, imatges, volums, xarxes, logs — tot des del navegador.

Crea una carpeta per a Portainer:

```bash
mkdir -p ~/homelab/portainer
```

Crea el contenidor:

```bash
docker run -d -p 9443:9443 --name portainer \
    --restart=always \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v ~/homelab/portainer/data:/data \
    portainer/portainer-ce:latest
```

Explicació:

- `-d`: en segon pla (detached).
- `-p 9443:9443`: exposa el port 9443 (HTTPS) al host.
- `--name portainer`: li posa nom.
- `--restart=always`: si la RPi es reinicia, Portainer torna a engegar.
- `-v /var/run/docker.sock:/var/run/docker.sock`: li dóna accés a Docker.
- `-v ~/homelab/portainer/data:/data`: persistència de dades.

Obre el navegador a `https://hortosona:9443` (o `https://IP-LOCAL:9443`). La primera vegada et demanarà crear un compte d'administrador. **Fes-ho immediatament** — Portainer sense admin és un forat de seguretat.

A la primera configuració, tria "Get Started" (entorn local). Ja tens Portainer.

## 61.6 Explorar Portainer

Al panell principal veuràs:

- **Stacks**: grups de contenidors (els teus "serveis").
- **Containers**: contenidors individuals.
- **Images**: imatges Docker descarregades.
- **Volumes**: emmagatzematge persistent.
- **Networks**: xarxes virtuals entre contenidors.
- **Events**: registre d'activitat.

Per ara, explora. Encara no tens gaire cosa per mirar.

## 61.7 Crear el teu primer contenidor a mà

A la terminal, creem un contenidor de prova: **Nginx**, el servidor web més usat del món.

```bash
docker run -d -p 8080:80 --name nginx-test nginx
```

Ara:

- Portainer mostra el contenidor `nginx-test` en marxa.
- Si obres `http://hortosona:8080` al navegador, veuràs la pàgina de benvinguda de Nginx.

Per veure els logs del contenidor:

```bash
docker logs nginx-test
```

Per aturar-lo:

```bash
docker stop nginx-test
```

Per tornar-lo a engegar:

```bash
docker start nginx-test
```

Per esborrar-lo:

```bash
docker rm -f nginx-test
```

## 61.8 Què és Docker Compose

Quan tens més d'un contenidor, gestionar-los amb `docker run` un per un és tediós. **Docker Compose** permet definir tots els teus serveis en un fitxer YAML.

Exemple: un fitxer `docker-compose.yml` per a Portainer:

```yaml
version: "3.8"

services:
  portainer:
    image: portainer/portainer-ce:latest
    container_name: portainer
    restart: unless-stopped
    ports:
      - "9443:9443"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ./portainer/data:/data
```

Aquest fitxer fa exactament el mateix que la comanda `docker run` d'abans, però en format declaratiu.

Per engegar:

```bash
docker compose up -d
```

Per aturar:

```bash
docker compose down
```

Per veure els logs:

```bash
docker compose logs -f
```

## 61.9 Estructura recomanada per a serveis

A la teva RPi, crea aquesta estructura:

```
~/homelab/
├── README.md              # Notes generals
├── compose/               # Tots els docker-compose
│   ├── portainer.yml
│   ├── uptime-kuma.yml
│   ├── mqtt.yml
│   ├── influxdb.yml
│   ├── grafana.yml
│   └── ...
├── data/                  # Volums persistents
│   ├── portainer/
│   ├── uptime-kuma/
│   ├── mqtt/
│   └── ...
├── secrets/               # Fitxers .env amb secrets
│   ├── mqtt.env
│   ├── influxdb.env
│   └── ...
└── scripts/               # Scripts de manteniment
    ├── backup.sh
    ├── update.sh
    └── healthcheck.sh
```

Aquesta estructura t'acompanyarà durant anys.

## 61.10 Convertir Portainer a Compose

Mou el Portainer que hem creat a mà a un fitxer Compose:

Crea `~/homelab/compose/portainer.yml`:

```yaml
version: "3.8"

services:
  portainer:
    image: portainer/portainer-ce:latest
    container_name: portainer
    restart: unless-stopped
    ports:
      - "9443:9443"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ./data/portainer:/data
```

Aquest fitxer farà servir `./data/portainer/` dins de la carpeta `compose/`, que és la mateixa ruta que ja estem usant.

Atura i esborra el contenidor antic:

```bash
docker stop portainer
docker rm portainer
```

Engega'l amb Compose:

```bash
cd ~/homelab/compose
docker compose -f portainer.yml up -d
```

Verifica que funciona obrint `https://hortosona:9443`. Si tot va bé, ja tens Portainer sota Compose.

## 61.11 Comandes útils de Docker

```bash
# Veure contenidors en marxa
docker ps

# Veure tots els contenidors (inclosos aturats)
docker ps -a

# Veure imatges descarregades
docker images

# Veure espai ocupat per Docker
docker system df

# Netejar recursos no utilitzats
docker system prune -a
# Compte: això esborra imatges, contenidors aturats, xarxes no usades.
# NO esborra volums (per seguretat).

# Veure logs d'un contenidor
docker logs -f portainer
# -f = follow (en temps real)

# Entrar dins d'un contenidor
docker exec -it portainer /bin/sh
# Per Nginx Alpine, /bin/sh
# Per Debian/Ubuntu, /bin/bash

# Estadístiques en temps real
docker stats
```

## 61.12 Bones pràctiques

1. **No posis secrets al docker-compose.yml**. Usa un fitxer `.env` a part.
2. **Posa `restart: unless-stopped`** a tots els serveis. Si la RPi es reinicia, tot torna a engegar.
3. **Fes servir volums** per a totes les dades persistents. Mai guardis dades dins del contenidor.
4. **Etiqueta les imatges**: usa tags específics (`nginx:1.25.3`) en lloc de `:latest`.
5. **Limita els recursos** dels contenidors que poden consumir molt.
6. **Monitora** els contenidors (capítol 67).

## 61.13 Què ve després

Ara tens Docker i Portainer funcionant. Al **Cap 62** afegirem el primer servei de monitoratge: **Uptime Kuma**.

## 61.14 Resum

Docker + Portainer és la base de tot el que vindrà. Hem vist:

- Què és Docker i per què serveix.
- Com instal·lar Docker i Docker Compose.
- Com instal·lar Portainer i gestionar-lo via web.
- Comandes bàsiques de Docker.
- L'estructura recomanada per als teus serveis.
- Bones pràctiques.

## 61.15 Exercicis pràctics

1. Instal·la Docker.
2. Afegeix el teu usuari al grup docker.
3. Instal·la Portainer.
4. Crea el teu primer contenidor (Nginx de prova).
5. Esborra'l i crea'l de nou amb Compose.
6. Mou Portainer a Compose.
7. Explora Portainer des del navegador.
8. Crea l'estructura `~/homelab/{compose,data,secrets,scripts}/`.
9. Documenta-ho al `homelab/setup-log.md`.
