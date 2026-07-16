# Exercici practic - Capitol 7: Actualitzacio de contenidors

> 30-45 min · Real al teu sistema

## Objectiu

Practicar Watchtower per actualitzar contenidors automaticament, fer manual rolling updates i provar un mini blue-green deployment. Acabaras sabent com mantenir els teus serveis actualitzats sense caigudes.

## Requisits

- Docker Compose instal·lat
- 30-45 minuts
- 500 MB d'espai lliure

## Pas 1: Prepara el projecte (5 min)

```bash
mkdir -p ~/actualitzacio-test
cd ~/actualitzacio-test
```

Crea un `docker-compose.yml`:

```yaml
version: "3.8"
services:
  web:
    image: nginx:1.25-alpine
    ports:
      - "8080:80"
    labels:
      - "com.bernatlab.enable=true"

  watchtower:
    image: containrrr/watchtower
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      - WATCHTOWER_LABEL_ENABLE=true
      - WATCHTOWER_CLEANUP=true
      - WATCHTOWER_POLL_INTERVAL=60
    command: --label-enable --cleanup
```

## Pas 2: Arrenca l'stack i verifica (5 min)

```bash
# Arrenca
docker compose up -d

# Comprova
docker compose ps

# Comprova que nginx funciona
curl -s http://localhost:8080 | head -5
# Hauria de mostrar "Welcome to nginx!"

# Mira la versio d'nginx
docker exec actualitzacio-test-web-1 nginx -v
# nginx version: nginx/1.25.x
```

## Pas 3: Configura Watchtower (10 min)

```bash
# Mira els logs de Watchtower
docker compose logs watchtower
# Veuras missatges de "Polling" cada 60 segons

# Comprova quins contenidors monitoritza
docker exec actualitzacio-test-watchtower-1 watchtower --debug
```

Watchtower nomes monitoritza els contenidors amb el label `com.bernatlab.enable=true`. Si poses una web sense label, Watchtower la deixa en pau.

Per provar-ho, podem canviar l'etiqueta d'una web. Pero primer, provem un cas real.

## Pas 4: Forca una actualitzacio (10 min)

Watchtower comprova si hi ha una nova versio a Docker Hub. Normalment espera dies/mesos, pero podem forçar-ho usant un altre tag.

```bash
# Atura l'stack
docker compose down

# Edita el compose: canvia nginx:1.25-alpine a nginx:1.27-alpine
sed -i 's|nginx:1.25-alpine|nginx:1.27-alpine|g' docker-compose.yml

# Arrenca de nou
docker compose up -d

# Comprova la nova versio
docker exec actualitzacio-test-web-1 nginx -v
# nginx version: nginx/1.27.x
```

Aixo demostra com es fa una actualitzacio manual. Watchtower faria el mateix pero automaticament.

## Pas 5: Prova un blue-green deployment manual (10 min)

La idea: tenir dues versions corrent i canviar el tràfic nomes quan la nova funciona.

```bash
# Crea un directori per a la nova versio
mkdir -p ~/actualitzacio-test/green
cd ~/actualitzacio-test/green

# Crea un docker-compose per a la nova versio
cat > docker-compose.yml <<EOF
version: "3.8"
services:
  web-green:
    image: nginx:1.27-alpine
    ports:
      - "8081:80"
EOF

# Arrenca la nova versio a un port diferent
docker compose up -d

# Comprova
curl -s http://localhost:8080 | head -3   # antiga
curl -s http://localhost:8081 | head -3   # nova

# Compara les versions
docker exec actualitzacio-test-web-1 nginx -v
docker exec actualitzacio-test-green-web-green-1 nginx -v

# Si la nova funciona, podem aturar l'antiga i remapejar el port
# Per fer-ho amb compose, editem i reconfigurem
cd ~/actualitzacio-test
docker compose -f green/docker-compose.yml down

# Ara actualitzem el compose principal a la nova versio
sed -i 's|nginx:1.25-alpine|nginx:1.27-alpine|g' docker-compose.yml
docker compose up -d
curl -s http://localhost:8080 | head -3
docker exec actualitzacio-test-web-1 nginx -v
```

Aixo es un **rolling update manual**. En sistemes mes grans (Docker Swarm, Kubernetes) es fa automaticament.

## Pas 6: Configura notificacions (5 min)

Watchtower pot enviar-te un correu o un missatge a Discord/Telegram/Slack quan actualitza alguna cosa. Exemple amb Discord:

```bash
# Atura l'stack
cd ~/actualitzacio-test
docker compose down

# Afegeix el webhook al compose
# Edita el fitxer i afegeix WATCHTOWER_NOTIFICATIONS=shoutrrr
# WATCHTOWER_NOTIFICATION_URL=discord://token@channel

cat > docker-compose.yml <<EOF
version: "3.8"
services:
  web:
    image: nginx:1.27-alpine
    ports:
      - "8080:80"
    labels:
      - "com.bernatlab.enable=true"

  watchtower:
    image: containrrr/watchtower
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      - WATCHTOWER_LABEL_ENABLE=true
      - WATCHTOWER_CLEANUP=true
      - WATCHTOWER_POLL_INTERVAL=86400
      - WATCHTOWER_NOTIFICATIONS=shoutrrr
      - WATCHTOWER_NOTIFICATION_URL=shoutrrr://discord://token@channel
    command: --label-enable --cleanup --schedule "0 0 4 * * *"
EOF

# Torna a arrencar
docker compose up -d

# Mira els logs
docker compose logs watchtower
```

## Pas 7: Neteja

```bash
cd ~/actualitzacio-test
docker compose down
rm -rf ~/actualitzacio-test

docker system df
docker system prune -a --volumes  # Neteja totes les imatges no usades
```

## Validacio

Has acabat si:

- [ ] Has creat un compose amb Watchtower.
- [ ] Has vist com Watchtower monitoritza nomes els contenidors amb label.
- [ ] Has fet una actualitzacio manual canviant el tag d'una imatge.
- [ ] Has practicat un blue-green deployment.
- [ ] Has configurat notificacions (Discord o similar).
- [ ] Has netejat els recursos.

## Per aprofundir

- Investiga `docker-autoheal` que reinicia contenidors que fallen healthchecks.
- Compara Watchtower amb alternatives com Ouroboros, Diun (basat en labels de Docker).
- Investiga les estratgies de rolling update a Docker Swarm i Kubernetes.
- Practica amb `docker compose pull && docker compose up -d` que es l'equivalent manual a Watchtower.
