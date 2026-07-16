# Respostes — Capítol 5: Docker des de zero

> Mira les respostes DESPRÉS d'haver fet el qüestionari.

## Pregunta 1: Diferència imatge vs contenidor

**Resposta correcta**: La imatge és la plantilla de només lectura; el contenidor és la instància viva.

**Explicació**: La imatge és com una classe en programació (plantilla), el contenidor és l'objecte instanciat. Pots crear molts contenidors des de la mateixa imatge. Una imatge no canvia mai; el contenidor escriu en una capa superior.

## Pregunta 2: docker run -d

**Resposta correcta**: Executa el contenidor en segon pla (detached).

**Explicació**: `-d` (detached) desacobla la terminal del contenidor, que queda corrent al fons. Sense `-d`, la terminal queda "enganxada" als logs del contenidor. Combinat amb `--name` li donem un nom, i amb `-p` exposem ports.

## Pregunta 3: Funció d'un volum

**Resposta correcta**: Persistir dades més enllà de la vida del contenidor.

**Explicació**: Els volums munten un directori persistent (gestor per Docker o per tu) dins del contenidor. Si el contenidor s'esborra, les dades del volum es conserven. Això és vital per a bases de dades, configuracions, pujades d'arxius, etc.

## Pregunta 4: Fitxer estàndard de Compose

**Resposta correcta**: docker-compose.yml

**Explicació**: Per convenció s'anomena `docker-compose.yml` (o `compose.yaml` a la nova especificació). El format és YAML, amb tres seccions principals: `services`, `volumes`, `networks`.

## Pregunta 5: docker compose up -d

**Resposta correcta**: Aixeca tots els serveis definits al fitxer compose en segon pla.

**Explicació**: `up` construeix (si cal), descarrega imatges, crea xarxes/volums i arrenca serveis. `-d` ho fa en segon pla. Si canvies el fitxer, tornar a fer `up -d` aplica els canvis (recreant només el que calgui).

## Pregunta 6: Avantatge Alpine

**Resposta correcta**: Ocupa molt menys espai (5-10x).

**Explicació**: Alpine Linux és una distribució mínima (~5 MB vs 120 MB de Debian). Per tant, imatges com `nginx:alpine` (43 MB) ocupen 5-10 vegades menys que `nginx:latest' (~180 MB). Trade-off: usa musl libc en lloc de glibc, cosa que pot causar problemes amb alguns binaris.

## Pregunta 7: docker ps -a

**Resposta correcta**: Mostra tots els contenidors, inclosos els aturats.

**Explicació**: `docker ps` mostra només els actius. `-a` (all) mostra tots, amb el seu estat (Up, Exited, Created). Molt útil per netejar: `docker rm $(docker ps -a -q)` esborra tots els aturats.

## Pregunta 8: restart automàtic

**Resposta correcta**: restart: unless-stopped

**Explicació**: Opcions vàlides: `no` (mai), `always` (sempre, inclús si el pare mor), `on-failure` (només si falla), `unless-stopped` (sempre, excepte si l'aturen manualment). `unless-stopped` és el sweet spot per a serveis d'homelab.

## Pregunta 9 (oberta): Per què Docker per a un homelab?

**Resposta model**:

Docker és útil per a un homelab perquè resol diversos problemes pràctics:

**1. Aïllament de dependències**: cada servei té les seves pròpies llibreries, versions de Python, configuracions. Pots tenir Nextcloud amb PHP 8.2 i un altre servei amb PHP 7.4 sense conflicte. Sense Docker, hauries de mantenir màquines virtuals separades o gestionar entorns virtuals a mà.

**2. Portabilitat**: el mateix `docker-compose.yml` funciona igual a la RPi, al portàtil, a un servidor al núvol. Si un dia vols migrar a un Mini PC x86, copies la carpeta i fas `docker compose up -d`. Si el BernatLab es trenca, en 10 minuts tens un altre igual.

**3. Reproducibilitat**: la imatge és immutable. Si algo funciona avui, funcionarà demà (excepte canvis de volum/configuració). Pots fer `docker compose down && docker compose up -d` sense por de "trencar" res.

**4. Instal·lació neta**: cada contenidor té el seu propi sistema de fitxers. Pots esborrar-lo i començar de zero en un segon. Perfecte per provar coses noves sense contaminar el sistema base.

**5. Actualitzacions fàcils**: `docker compose pull && docker compose up -d` actualitza tots els serveis. Si algo falla, `docker compose down` torna a la versió anterior (sempre que conservis la imatge antiga o el `docker-compose.yml` vell).

**6. Backups nets**: persistir dades en volums permet fer backup senzill (copiar la carpeta del volum) sense por de perdre configuracions dins dels contenidors.

**7. Eficiència de recursos**: un contenidor Docker consumeix ~5-50 MB de RAM extra, mentre que una màquina virtual consumiria 200-500 MB. En una RPi amb 4 GB, això és la diferència entre poder tenir 8 serveis o només 2.

## Pregunta 10 (oberta): Afegir un nou servei al compose

**Resposta model**:

Per afegir un servidor de jocs (per exemple, Minecraft) al BernatLab, els passos serien:

**1. Buscar la imatge oficial a Docker Hub**:
- Vaig a https://hub.docker.com i busco "minecraft server".
- Trobo `itzg/minecraft-server` (una de les més populars).
- Apunto la imatge i la versió, p. ex. `itzg/minecraft-server:latest`.

**2. Editar `~/homelab/docker/docker-compose.yml`** i afegir el servei:

```yaml
version: "3.9"

services:
  # ... altres serveis existents (portainer, etc.) ...

  minecraft:
    image: itzg/minecraft-server:latest
    container_name: minecraft
    ports:
      - "25565:25565"        # port per defecte de Minecraft
    environment:
      - EULA=TRUE             # cal acceptar la llicència
      - MEMORY=2G             # RAM assignada
    volumes:
      - mc_data:/data         # volum per a dades del món
    restart: unless-stopped

volumes:
  mc_data:
```

**3. Validar el fitxer**:

```bash
cd ~/homelab/docker
docker compose config
# Mostra el YAML interpretat; errors de sintaxi apareixen aquí
```

**4. Pujar el servei**:

```bash
docker compose up -d minecraft
# O simplement:
docker compose up -d
# (aquesta puja TOTS els serveis que ja existeixen, però només crea els nous)
```

**5. Comprovar**:

```bash
docker compose ps
docker compose logs -f minecraft
# Veure com arrenca el servidor
```

**6. Accedir des d'un client Minecraft**: afegir servidor `hortosona:25565` o `100.115.134.76:25565` des del client.

**7. Si cal actualitzar**:

```bash
docker compose pull minecraft
docker compose up -d minecraft
```

**Aspectes clau del YAML**:
- **`image`**: d'on treure la imatge.
- **`container_name`**: nom legible.
- **`ports`**: mapeig port_host:port_contenidor.
- **`volumes`**: persistència.
- **`environment`**: variables d'entorn (configuració).
- **`restart`**: política d'arrencada.

## Què fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum i practicar les ordres bàsiques.
- **3-4 encerts**: Torna a fer l'exercici pas a pas.
- **0-2 encerts**: Repassem junts.

## Què fer si has encertat totes

- Passa al **Capítol 6** (Portainer).
- Comença a pensar quins serveis vols al teu homelab.
