# Exercici practic - Capitol 5: Registre d'imatges

> 30-45 min · Real al teu sistema

## Objectiu

Muntar un registre Docker privat a la teva RPi, configurar autenticacio, pujar-hi una imatge i baixar-la des d'un altre node (o un altre usuari). Acabaras entenent com funciona un registre self-hosted.

## Requisits

- Docker instal·lat a la RPi
- 30-45 minuts
- Acces a la linia de comandes

## Pas 1: Arrenca el registre basic (5 min)

```bash
# Crea una carpeta per les dades
mkdir -p ~/registry-data

# Arrenca el registre
docker run -d -p 5000:5000 --restart=always --name registry \
  -v ~/registry-data:/var/lib/registry \
  registry:2

# Comprova que funciona
curl http://localhost:5000/v2/
# Hauria de retornar {} i un 200 OK

# Comprova la API
curl http://localhost:5000/v2/_catalog
# Retorna {"repositories":[]}
```

## Pas 2: Configura insecure-registries (5 min)

Per defecte, Docker nomes confia en registres HTTPS (excepte localhost). Si vols fer servir la IP o hostname, cal afegir-ho:

```bash
# Obte la teva IP local
hostname -I

# Edita la configuracio de Docker
sudo nano /etc/docker/daemon.json
```

Afegeix (canvia `192.168.1.100` per la teva IP):

```json
{
  "insecure-registries": ["192.168.1.100:5000"]
}
```

Si ja tens contingut al fitxer, simplement afegeix la clau:

```json
{
  "data-root": "/mnt/ssd/docker",
  "insecure-registries": ["192.168.1.100:5000"]
}
```

Reinicia Docker:

```bash
sudo systemctl restart docker

# El registre tambe cal reiniciar-lo
docker start registry
```

## Pas 3: Puja una imatge al registre (10 min)

```bash
# Crea una imatge simple (la pots obtenir d'un capitol anterior)
# Si no tens cap, fem-ne una de minima:
docker pull alpine
docker tag alpine:latest 192.168.1.100:5000/meu-alpine:1.0

# Comprova els tags locals
docker images | grep meu-alpine

# Puja-la al registre
docker push 192.168.1.100:5000/meu-alpine:1.0

# Comprova que esta al registre
curl http://localhost:5000/v2/_catalog
# Hauria de mostrar {"repositories":["meu-alpine"]}

curl http://localhost:5000/v2/meu-alpine/tags/list
# Hauria de mostrar {"name":"meu-alpine","tags":["1.0"]}
```

## Pas 4: Baixa la imatge des d'un altre node (5 min)

Si tens una segona maquina (una altre RPi, el teu PC), pots provar-hi:

```bash
# A l'altra maquina
# Primer configura la insecure-registry igual
sudo nano /etc/docker/daemon.json
# {"insecure-registries": ["192.168.1.100:5000"]}
sudo systemctl restart docker

# Despres baixa la imatge
docker pull 192.168.1.100:5000/meu-alpine:1.0

# Comprova
docker images | grep meu-alpine
```

Si no tens segona maquina, pots simular-ho netejant local i rebaixant:

```bash
# Elimina la imatge local
docker rmi 192.168.1.100:5000/meu-alpine:1.0

# Torna-la a baixar
docker pull 192.168.1.100:5000/meu-alpine:1.0

# Verifica
docker run --rm 192.168.1.100:5000/meu-alpine:1.0 echo "Hola des del registre privat!"
```

## Pas 5: Afegeix autenticacio (10 min)

Ara el registre es obert a tothom. Afegim basic auth:

```bash
# Crea un fitxer htpasswd
mkdir -p ~/registry-auth
docker run --rm --entrypoint htpasswd httpd:2 -Bbn bernat supersecret > ~/registry-auth/htpasswd
cat ~/registry-auth/htpasswd
# Hauries de veure bernat:$2y$05$... (hash bcrypt)

# Atura el registre antic
docker stop registry
docker rm registry

# Re-arrenca amb autenticacio
docker run -d -p 5000:5000 --restart=always --name registry \
  -v ~/registry-data:/var/lib/registry \
  -v ~/registry-auth:/auth \
  -e "REGISTRY_AUTH=htpasswd" \
  -e "REGISTRY_AUTH_HTPASSWD_REALM=Registry Realm" \
  -e "REGISTRY_AUTH_HTPASSWD_PATH=/auth/htpasswd" \
  registry:2

# Comprova que ara demana auth
curl http://localhost:5000/v2/_catalog
# Hauria de retornar 401 Unauthorized

# Amb credencials
curl -u bernat:supersecret http://localhost:5000/v2/_catalog
# Hauria de funcionar
```

## Pas 6: Login al registre (5 min)

```bash
# Logout de qualsevol altre registre
docker logout

# Login al nou registre privat
docker login 192.168.1.100:5000
# Username: bernat
# Password: supersecret

# Comprova que el login ha funcionat
cat ~/.docker/config.json
# Hauria de tenir "192.168.1.100:5000" amb credencials

# Ara ja pots tornar a fer push/pull
docker push 192.168.1.100:5000/meu-alpine:1.0
```

## Pas 7: Inspecciona el registre

```bash
# Quantes imatges tens?
curl -u bernat:supersecret http://localhost:5000/v2/_catalog

# Quins tags?
curl -u bernat:supersecret http://localhost:5000/v2/meu-alpine/tags/list

# Estadistiques del Docker host
docker system df
# Hauries de veure la mida de les imatges al registre

# Logs del registre
docker logs registry --tail 50
```

## Pas 8: Neteja (5 min)

Si vols deixar el registre en marxa, perfecte. Si no:

```bash
# Atura i elimina el registre
docker stop registry
docker rm registry

# Neteja les dades (compte, esborra totes les imatges)
rm -rf ~/registry-data
rm -rf ~/registry-auth

# Comprova
docker images
docker ps -a
```

## Validacio

Has acabat si:

- [ ] Has arrencat un registre Docker privat al port 5000.
- [ ] Has configurat insecure-registries per fer-hi accessible.
- [ ] Has pujat una imatge amb `docker push` i l'has tornat a baixar.
- [ ] Has afegit autenticacio htpasswd i has fet login.
- [ ] Has vist la llista d'imatges al registre amb la API REST.
- [ ] Has decidit si vols mantenir el registre o netejar-lo.

## Per aprofundir

- Configura HTTPS amb Caddy com a reverse proxy (molt recomanable!).
- Prova Harbor si tens mes ganes (es mes complet pero mes pesat).
- Investiga com fer garbage collection per netejar capes antigues.
- Compara el rendiment de pull des del registre privat vs Docker Hub.
