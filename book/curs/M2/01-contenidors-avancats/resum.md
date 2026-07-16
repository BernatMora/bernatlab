# Resum - Capitol 1: Contenidors avançats

## La idea clau

Un contenidor Docker no es magic. Es un procés de Linux aillat que comparteix el kernel del sistema amfitrio pero te el seu propi sistema de fitxers, xarxa i processos. Aquest capitol es per entendre què passa per sota: com es construeixen les imatges, com s'apilen les capes, i com fer builds eficients amb multi-stage.

## Que es una imatge Docker?

Una **imatge Docker** es un paquet de lectura nomes que conte tot el que cal per executar un programa:

- Un sistema de fitxers base (normalment Alpine, Debian slim o Ubuntu)
- Les dependencies (biblioteques, eines)
- El teu codi o aplicacio
- Les metadades (port, variable d'entorn, comanda d'arrencada)

Les imatges es guarden en un **registre** (Docker Hub, registre privat) i es descarreguen quan fas `docker run`.

```
docker run nginx  -> baixa nginx: latest del Docker Hub (si no la tens)
                -> crea un contenidor a partir de la imatge
                -> arrenca el procés nginx
```

## Les capes (layers)

Una imatge Docker no es un bloc unic. Es composa de **capes** apilades. Cada instruccio d'un Dockerfile crea una capa nova:

```
FROM debian:bookworm-slim     <- capa 1: el sistema base
RUN apt update && install...  <- capa 2: les dependencies
COPY app.py /                 <- capa 3: el teu codi
CMD ["python", "app.py"]      <- (metadada, no es una capa)
```

Per que importa? Perque Docker guarda en **cache** cada capa. Si canvies nomes el codi pero les dependencies son les mateixes, Docker refara nomes la capa 3. Es rapidissim.

Pero atencio: cada capa es un **diff** del sistema de fitxers. Si tens 5 instruccions `RUN`, tindras 5 capes (i 5 registres al historial de la imatge). Per això es recomana combinar instruccions:

```dockerfile
# MAL: 3 capes
RUN apt update
RUN apt install -y python3
RUN pip install flask

# BE: 1 sola capa
RUN apt update && apt install -y python3 && pip install flask
```

## Multi-stage builds

Aqui ve la magia. Quan compiles una aplicacio, necessites totes les eines de build (compilador, llibreries de dev, node_modules amb coses de testing). Pero per **executar-la** nomes necessites el binari final. Amb multi-stage tens dos `FROM`:

```dockerfile
# Etapa 1: build (te totes les eines)
FROM node:20 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Etapa 2: runtime (nomes el que cal)
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
```

La imatge final pot passar de **800 MB** (amb totes les eines) a **40 MB** (nomes el static compilat). A una RPi amb microSD, aquesta diferencia es_or_d_or.

## Bones practiques als Dockerfiles

He anat aprenent coses que fan la vida mes facil:

- **Sempre posa tag concret**: `FROM debian:12-slim` en lloc de `FROM debian:latest`. Si no, el build pot trencar-se d'aqui un mes.
- **Usuari no-root**: `USER 1000` al final. Si algú exploita el teu contenidor, no sera root al sistema amfitrio.
- **Copia el minim**: millor `COPY package.json` i `RUN npm install` abans de `COPY . .`. Aixi les dependencies es cachejen.
- **Usa `.dockerignore`**: igual que `.gitignore` pero per Docker. Evita que el context del build contingui `node_modules`, `.git`, etc.
- **Npm ci en lloc de npm install**: mes rapid i deterministic.

Exemple real del BernatLab (un servei Python petit):

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
USER 1000
EXPOSE 8000
CMD ["python", "main.py"]
```

## Inspeccio d'imatges

Algunes comandes que val la pena conèixer:

```bash
# Veure les capes d'una imatge
docker history bernatlab-api:latest

# Inspeccionar metadades
docker image inspect nginx:alpine

# Mida de totes les imatges
docker system df

# Netejar imatges i capes no usades
docker system prune -a
```

## Connexions amb altres capitols

- **M1 Cap 5** - Els basics de Docker que ja saps.
- **M2 Cap 2** - Sense volums persistents, tot el que facis es volat.
- **M2 Cap 4** - Compose es construeix sobre aquestes imatges.
- **M2 Cap 5** - On es desen les imatges que construeixes.
- **M2 Cap 6** - Seguretat comença amb imatges minimals i usuaris no-root.
