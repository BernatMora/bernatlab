# Exercici practic - Capitol 2: Volums persistents

> 30-40 min · Real al teu sistema

## Objectiu

Practicar amb els tres tipus de volums (nomenat, bind mount, tmpfs) i entendre quan usar cada un. Acabaras sabent on Docker guarda les dades i com fer un backup basic.

## Requisits

- Docker instal·lat a la RPi
- 30-40 minuts
- Privilegis de sudo

## Pas 1: Crea i prova un volum nomenat (10 min)

```bash
# Crear el volum
docker volume create dades-test

# Inspeccionar-lo per veure on viu
docker volume inspect dades-test
# Hauria de mostrar Mountpoint: /var/lib/docker/volumes/dades-test/_data

# Arrencar un contenidor que l'usi
docker run -d --name test-vol -v dades-test:/app/data alpine \
  sh -c "echo 'Hola des de dins!' > /app/data/salutacio.txt && sleep 3600"

# Verificar que el fitxer existeix dins el contenidor
docker exec test-vol cat /app/data/salutacio.txt

# Verificar que existeix a l'amfitrio
sudo cat /var/lib/docker/volumes/dades-test/_data/salutacio.txt

# Ara atura i elimina el contenidor
docker stop test-vol
docker rm test-vol

# El volum encara existeix amb les dades
docker volume ls
sudo ls /var/lib/docker/volumes/dades-test/_data/
```

Aixo demostra que les dades **sobreviuen** al contenidor perque viuen al volum.

## Pas 2: Bind mount d'una carpeta real (10 min)

```bash
# Crea una carpeta a la teva home
mkdir -p ~/proves-bind
cd ~/proves-bind
echo "Això es un fitxer de l'amfitrio" > desde-amfitrio.txt

# Munta-la dins un contenidor
docker run -d --name test-bind \
  -v ~/proves-bind:/app/dades \
  alpine sh -c "ls /app/dades > /app/dades/llistat.txt && sleep 3600"

# Comprova des de l'amfitrio
ls ~/proves-bind/
cat ~/proves-bind/llistat.txt

# Edita el fitxer desde l'amfitrio
echo "Segon fitxer creat des de fora" >> ~/proves-bind/des-de-fora.txt

# Comprova des del contenidor
docker exec test-bind cat /app/dades/des-de-fora.txt

# Neteja
docker stop test-bind
docker rm test-bind
```

Has vist com pots editar fitxers desde fora i el contenidor els veu a l'instant.

## Pas 3: Prova tmpfs (5 min)

```bash
# Conenidor amb memoria temporal
docker run -d --name test-tmpfs --tmpfs /app/cache \
  alpine sh -c "echo 'secret' > /app/cache/token && sleep 3600"

# Verifica que el fitxer existeix
docker exec test-tmpfs cat /app/cache/token

# Comprova que NO esta al sistema de fitxers de l'amfitrio
sudo find /var/lib/docker -name "token" 2>/dev/null
# No trobara res, perque tmpfs nomes viu a la RAM

# Neteja
docker stop test-tmpfs
docker rm test-tmpfs
```

## Pas 4: Comparteix dades entre dos contenidors (10 min)

```bash
# Conenidor 1: escriu al volum
docker run -d --name writer -v compartit:/data alpine \
  sh -c "while true; do date >> /data/log.txt; sleep 2; done"

# Espera 5 segons i mira el fitxer
sleep 5
docker exec writer cat /data/log.txt

# Conenidor 2: llegeix el mateix volum
docker run --rm --name reader -v compartit:/data alpine \
  cat /data/log.txt
# Veuras les mateixes dades

# Neteja
docker stop writer
docker rm writer
docker volume rm compartit
```

Aixo demostra que un volum pot ser muntat per multiples contenidors simultaneament.

## Pas 5: Backup basic d'un volum (5 min)

```bash
# Reutilitza el volum del pas 1
docker run --rm \
  -v dades-test:/origen:ro \
  -v ~/proves-bind:/desti \
  alpine tar czf /desti/backup-dades-test.tar.gz -C /origen .

ls -lh ~/proves-bind/backup-dades-test.tar.gz

# Per restaurar (en un altre volum):
docker volume create dades-restaurades
docker run --rm \
  -v dades-restaurades:/desti \
  -v ~/proves-bind:/backup \
  alpine tar xzf /backup/backup-dades-test.tar.gz -C /desti

docker run --rm -v dades-restaurades:/data alpine ls /data
# Hauries de veure salutacio.txt
```

## Pas 6: Neteja final

```bash
# Neteja tots els volums de prova
docker volume rm dades-test dades-restaurades
rm -rf ~/proves-bind

# Comprova que no queda res
docker volume ls
```

## Validacio

Has acabat si:

- [ ] Has creat un volum nomenat i has vist que les dades sobreviuen al contenidor.
- [ ] Has fet un bind mount i has pogut editar fitxers desde l'amfitrio.
- [ ] Has provat un tmpfs i has confirmat que les dades no van al disc.
- [ ] Has compartit un volum entre dos contenidors.
- [ ] Has fet un backup basic amb tar i l'has restaurat.
- [ ] Has netejat tots els recursos de prova.

## Per aprofundir

- Investiga el driver `local` versus un driver NFS. Com es configuraria un volum NFS?
- Prova de muntar un volum nomes de lectura afegint `:ro` al final de `-v`.
- Compara el rendiment de tmpfs vs volum normal amb un test d'escriptura.
- Investiga la diferencia entre `docker volume` i `docker network` (tots dos son "managed resources").
