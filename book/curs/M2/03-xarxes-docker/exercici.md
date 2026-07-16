# Exercici practic - Capitol 3: Xarxes Docker

> 30-45 min · Real al teu sistema

## Objectiu

Practicar amb xarxes bridge custom, port mapping, DNS automatic i segmentacio de serveis. Acabaras entenent com comunicar contenidors entre ells i amb el mon exterior.

## Requisits

- Docker instal·lat a la RPi
- 30-45 minuts
- Imatges nginx i alpine disponibles (es baixaran automaticament)

## Pas 1: La xarxa per defecte (5 min)

```bash
# Mira les xarxes existents
docker network ls

# Fixa't en la xarxa "bridge" (per defecte)
docker network inspect bridge

# Arrenca un contenidor a la bridge per defecte
docker run -d --name test1 alpine sleep 3600
docker network inspect bridge
# Veuras que test1 esta connectat

# Comprova que no pot resoldre altres noms
docker exec test1 nslookup google.com
# Hauria de funcionar (per que te acces a internet)

# Neteja
docker stop test1
docker rm test1
```

## Pas 2: Crea una xarxa custom (10 min)

```bash
# Crea una xarxa bridge custom
docker network create xarxa-test

# Inspecciona-la
docker network inspect xarxa-test

# Arrenca dos contenidors a la xarxa custom
docker run -d --name api --network xarxa-test alpine sleep 3600
docker run -d --name web --network xarxa-test alpine sleep 3600

# Comprova DNS automatic
docker exec api ping -c 2 web
# Hauria de respondre! Magic del DNS automatic

# I viceversa
docker exec web ping -c 2 api

# Inspecciona la xarxa per veure els dos contenidors
docker network inspect xarxa-test
```

## Pas 3: Port mapping (10 min)

```bash
# Arrenca nginx exposant el port 80 del contenidor al 8080 de l'amfitrio
docker run -d --name web-public -p 8080:80 nginx:alpine

# Comprova que respon des del navegador o amb curl
curl http://localhost:8080

# Arrenca un SEGON nginx mapejat a un port diferent
docker run -d --name web-public2 -p 8081:80 nginx:alpine

curl http://localhost:8081

# Quins contenidors tenen ports mapejats?
docker ps --format "table {{.Names}}\t{{.Ports}}"
```

## Pas 4: Segmentacio de serveis (15 min)

Ara el cas practic real: frontend + backend + base de dades amb segmentacio.

```bash
# Crea dues xarxes: frontend i backend
docker network create xarxa-frontend
docker network create xarxa-backend

# La base de dades nomes va a la xarxa backend
docker run -d --name db \
  --network xarxa-backend \
  -e POSTGRES_PASSWORD=test \
  postgres:16-alpine

# El backend va a les dues xarxes (pot parlar amb db i amb frontend)
docker run -d --name backend \
  --network xarxa-backend \
  alpine sleep 3600
docker network connect xarxa-frontend backend

# El frontend nomes va a la xarxa frontend (accessible des de fora)
docker run -d --name frontend \
  --network xarxa-frontend \
  -p 9090:80 \
  nginx:alpine

# Comprova les connexions
# Frontend pot parlar amb backend?
docker exec frontend ping -c 1 backend
# Hauria de respondre

# Frontend pot parlar amb db?
docker exec frontend ping -c 1 db
# NO hauria de respondre (no comparteixen xarxa)

# Backend pot parlar amb db?
docker exec backend ping -c 1 db
# SI hauria de respondre

# DB pot parlar amb frontend?
docker exec db ping -c 1 frontend
# NO hauria de respondre
```

Has aconseguit la segmentacio: la base de dades nomes es accessible des del backend, el frontend nomes pot rebre trafic extern i parlar amb el backend.

## Pas 5: Prova el host network (5 min)

```bash
# Arrenca un contenidor amb xarxa host
docker run -d --name test-host --network host nginx:alpine

# Ara nginx escolta directament al port 80 de l'amfitrio
curl http://localhost

# Quants contenidors tenen el port 80?
# Nomes un, perque si n'hi ha un altre fent servir 80, el segon falla
docker ps --format "table {{.Names}}\t{{.Ports}}"

# Neteja
docker stop test-host
docker rm test-host
```

## Pas 6: Neteja final

```bash
# Atura i elimina tots els contenidors
docker stop $(docker ps -q)
docker rm $(docker ps -aq)

# Esborra les xarxes custom
docker network rm xarxa-test xarxa-frontend xarxa-backend

# Comprova
docker network ls
```

## Validacio

Has acabat si:

- [ ] Has vist la xarxa bridge per defecte.
- [ ] Has creat una xarxa custom i has comprovat el DNS automatic.
- [ ] Has fet port mapping de dos serveis alhora.
- [ ] Has aconseguit segmentar frontend, backend i base de dades amb dues xarxes.
- [ ] Has provat el host network.
- [ ] Has netejat tots els recursos.

## Per aprofundir

- Investiga el flag `--ip` per assignar una IP fixa a un contenidor dins una xarxa custom.
- Compara el rendiment de host network vs bridge amb un test de transferencia (iperf).
- Llegeix sobre les "macvlan networks" per a casos on necessites que el contenidor sigui visible a la xarxa fisica amb la seva propia MAC.
- Investiga com es fa service discovery mes sofisticat amb DNS round-robin i "network aliases".
