# Respostes - Capitol 4: Compose avançat

> Mira les respostes DESPRES d'haver fet el qüestionari.

## Pregunta 1: Objectiu dels perfils?

**Resposta correcta**: Definir serveis opcionals que nomes s'activen en certes situacions (dev, prod, debug).

**Explicacio**: Els perfils permeten tenir un sol fitxer compose amb serveis opcionals. Actives nomes els que necessites amb `--profile`. Per exemple, phpMyAdmin nomes en dev, no en prod.

---

## Pregunta 2: Dependencia "sa"?

**Resposta correcta**: `depends_on: condition: service_healthy`.

**Explicacio**: `depends_on` nomes espera que el contenidor **inicii**, no que estigui llest. Amb `condition: service_healthy` Docker espera que el `healthcheck` retorni "healthy" abans d'arrencar el dependent. Es el que necessites per a una base de dades.

---

## Pregunta 3: Que fa `extends`?

**Resposta correcta**: Hereta configuracio d'un altre servei (base) per evitar duplicar-la.

**Explicacio**: Pots definir un servei "base" a un fitxer i que altres serveis l'extenguin, sobreescrivint nomes el que cal. Es molt util quan tens molts serveis amb configuracio similar (per exemple, mateix entorn, mateixa xarxa, mateix usuari).

---

## Pregunta 4: Format dels perfils?

**Resposta correcta**: `profiles: [dev, debug]`.

**Explicacio**: Es una llista, perque un servei pot estar en multiples perfils. Si poses `profiles: dev` (string), Docker no ho enten be. La sintaxi correcta es una llista.

---

## Pregunta 5: Com activar serveis amb perfil?

**Resposta correcta**: `docker compose --profile dev up`.

**Explicacio**: Els serveis sense perfil s'activen sempre. Els que tenen perfil nomes s'activen si especifiques `--profile`. Pots posar mes d'un perfil: `--profile dev --profile debug`.

---

## Pregunta 6: -d vs sense -d?

**Resposta correcta**: -d deixa els serveis en segon pla (detached); sense -d es veuen els logs.

**Explicacio**: `docker compose up` es queda enganxat mostrant logs (Ctrl+C per aturar). `docker compose up -d` torna el control immediatament i els contenidors queden corrent. Es l'equivalent de `docker run` vs `docker run -d`.

---

## Pregunta 7: Comanda per veure logs?

**Resposta correcta**: `docker compose logs -f`.

**Explicacio**: `-f` (follow) es com `tail -f`: veus els logs a temps real. `docker compose logs api` mostra nomes els d'un servei. Per defecte, Docker intercala els logs de tots els serveis amb colors.

---

## Pregunta 8: Que fa `secrets`?

**Resposta correcta**: Injectar fitxers sensibles (contrasenyes, claus) sense posar-los al fitxer compose.

**Explicacio**: Docker munta el fitxer del secret a `/run/secrets/<nom>` dins el contenidor. L'aplicacio llegeix el contingut del fitxer en lloc d'agafar la variable d'entorn. Es mes segur perque el secret no apareix a `docker inspect` ni a logs.

---

## Pregunta 9 (oberta): Per que perfils dev vs prod

**Resposta model**:

Tenir perfils separats per a "dev" i "prod" es una bona practica per diverses raons:

1. **Seguretat**: eines com phpMyAdmin, Adminer, portainer o qualsevol eina d'administracio son comodissimes en dev pero **perilloses** en produccio. Si un atacant troba phpMyAdmin exposat, pot intentar atacar la base de dades. Amb perfils, simplement no es desplega en prod.

2. **Recursos**: les eines de dev consumeixen memoria i CPU innecessaris en prod. Un container de phpMyAdmin nomes son ~150 MB pero amb 10 eines son 1.5 GB que podries fer servir per als serveis productius.

3. **Configuracio especifica**: en dev potser vols `LOG_LEVEL=debug` i `FLASK_DEBUG=1`, mentre que en prod vols `LOG_LEVEL=warning` i cap mode debug. Els perfils permeten tenir fitxers `docker-compose.override.yml` amb les diferencies.

4. **Claretat**: quan llegeixes el fitxer compose, veus clarament quines eines son opcionals. Si algu nou mira l'stack, enten a l'instant que "ah, phpmyadmin es nomes per dev".

Exemple concret al BernatLab: tinc un Nextcloud amb MariaDB. A dev hi tinc un `adminer` (un phpMyAdmin mes lleuger) connectat a la xarxa interna. Si vull accedir a la base de dades per curiositat, obro `http://raspberry.local:8080`. Pero quan faig `--profile prod`, adminer ni existeix. La base de dades nomes es accessible des del Nextcloud per xarxa interna.

Un altre cas: un `node_exporter` o un `prometheus` amb `profiles: [monitoring]` que nomes s'activen quan vols recollir metricques, no sempre.

---

## Pregunta 10 (oberta): App web amb 4 serveis

**Resposta model**:

Aixo es el fitxer `docker-compose.yml` complert:

```yaml
version: "3.9"

services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"
    networks:
      - frontend
    depends_on:
      api:
        condition: service_healthy
    profiles: [prod, dev]

  api:
    build: ./api
    environment:
      - DB_HOST=db
      - CACHE_HOST=cache
    networks:
      - frontend
      - backend
    depends_on:
      db:
        condition: service_healthy
      cache:
        condition: service_started
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 10s
      timeout: 3s
      retries: 3
    profiles: [prod, dev]

  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_USER=app
      - POSTGRES_PASSWORD=secret
      - POSTGRES_DB=appdb
    volumes:
      - db-data:/var/lib/postgresql/data
    networks:
      - backend
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app"]
      interval: 10s
      timeout: 3s
      retries: 5
    profiles: [prod, dev]

  cache:
    image: redis:7-alpine
    volumes:
      - cache-data:/data
    networks:
      - backend
    profiles: [prod, dev]

volumes:
  db-data:
  cache-data:

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
```

**Explicacio de les decisions**:

- **Xarxes**: dues. `frontend` per a web i api (on nomes api ha d'estar exposada via web). `backend` nomes per a api, db i cache. La db i la cache mai son accessibles desde l'exterior.

- **Ports**: nomes `web` te port mapping (`8080:80`). Ni `api` ni `db` ni `cache` son accessibles des de l'amfitrio directament. Si vols accedir a l'API, passes per `web` (que pot fer de proxy invers).

- **Volums**: `db-data` per a la base de dades (les dades han de persistir). `cache-data` per a Redis (encara que es pot perdre, es agradable mantenir-lo per rendiment).

- **Ordre d'arrencada**:
  1. `db` i `cache` arrenquen independentment (no depenen de res).
  2. `api` espera a que `db` estigui healthy i a que `cache` hagi iniciat.
  3. `web` espera a que `api` estigui healthy.
  - Tot automatic gracies a `depends_on` amb `condition: service_healthy`.

- **Perfils**: tots els serveis essentials estan en `prod` i `dev`. Si vols eines addicionals (adminer, monitoring), les posaries nomes a `dev`.

**Validacio de la segmentacio**:
- `docker compose exec web ping db` -> **falla** ✓ (no comparteixen xarxa)
- `docker compose exec api ping db` -> **funciona** ✓
- `docker compose exec db ping web` -> **falla** ✓
- Navegador pot accedir a `http://raspberry.local:8080` -> **funciona** ✓
- Navegador pot accedir a `http://raspberry.local:5432` -> **falla** ✓ (db no exposada)

---

## Pregunta 11 (oberta): Per que els perfils en lloc de fitxers separats

**Resposta model**:

Docker Compose va introduir els perfils per evitar un problema practic molt comu: la duplicacio de configuracio entre entorns. Si tens `docker-compose.dev.yml`, `docker-compose.prod.yml` i `docker-compose.test.yml`, acabes tenint tres fitxers que comparteixen el 80% del contingut i divergen subtilment en el 20% restant. Quan toques un servei, l'has de tocar a tres llocs i es facil oblidar-ne un.

Els perfils permeten mantenir **un sol fitxer** que conte totes les definicions, marcant amb `profiles:` les que son opcionals. Les avantatges practiques:

1. **Un sol lloc de veritat**: el `docker-compose.yml` es l'unic fitxer. Si toques el servei `db`, queda tocat per a tots els perfils.

2. **Comparacio facil**: amb `git diff` veus exactament quins canvis s'han fet, sense haver de comparar multiples fitxers.

3. **Menos errors de sincronitzacio**: abans, afegir una variable d'entorn a `dev` pero no a `prod` podia ser un bug subtil. Ara, si el servei esta definit una sola vegada, tothom el veu igual.

4. **Composicio flexible**: pots activar multiples perfils a la vegada (`--profile dev --profile debug`).

5. **Documentacio inherent**: el fitxer es l'esquema complet de l'app. Qualsevol persona que el llegeix enten tots els modes d'operacio.

Per a un homelab com el BernatLab, aixo vol dir que el teu `docker-compose.yml` conte el graf complert del que podries arribar a fer, i tu nomes actives els perfils que necessites en cada moment. La complexitat queda organitzada, no pas amagada.

---

## Pregunta 12 (oberta): Healthchecks i ordre d'arrencada

**Resposta model**:

`depends_on` nomes comprova que el contenidor ha arrencat (el proces principal esta corrent). Pero un servei pot estar **iniciat** pero no **llest**: una base de dades pot estar fent recovery, una API pot estar carregant models en memoria, un web pot estar esperant la base de dades. Si l'API es connecta a la base de dades massa aviat, obtindra errors intermitents i caldran reinicis.

`depends_on: condition: service_healthy` es la solucio: el contenidor espera a que el **healthcheck** del servei depenent retorni `healthy`. El healthcheck es una comanda que el servei exposa per dir "estic llest per rebre peticions" (per exemple, una query SELECT 1 a una base de dades, una peticio HTTP a /health).

**Exemple del BernatLab amb Nextcloud + MariaDB**:

Si nomes uses `depends_on: db`, pasa el seguent:
1. `db` arrenca (proces iniciat).
2. `nextcloud` arrenca inmediatament.
3. `nextcloud` intenta connectar-se a `db:3306` -> falla perque MariaDB encara esta fent init.
4. Nextcloud mostra errors, cal reiniciar manualment.

Amb `depends_on: db: { condition: service_healthy }`:
1. `db` arrenca.
2. MariaDB fa el seu init.
3. El healthcheck (`mysqladmin ping`) retorna `healthy`.
4. Aleshores `nextcloud` arrenca.
5. Nextcloud es connecta a MariaDB ja llesta.

Aixo es la diferencia entre "funciona la majoria del temps" i "funciona sempre". Per a serveis amb molta logica d'inicialitzacio, es essencial.

---

## Pregunta 13 (oberta): Per que comentar el compose

**Resposta model**:

El `docker-compose.yml` es un fitxer de configuracio, pero tambe es **documentacio viva**. Si nomes treballes tu al BernatLab, pots pensar que no cal comentar res perque "ja ho recordare". Pero aixo es fals per varies raons:

1. **La memoria humana es deficient**: d'aqui 6 mesos no recordaras per que vas posar `cap_drop: ALL` a un servei en concret. El context del moment (una noticia sobre una vulnerabilitat) s'ha esborrat de la teva memoria.

2. **Versions i dependències canvien**: un comentari que avui sembla obvi pot ser critic d'aqui un any perque la documentacio oficial ha canviat.

3. **El per que importa mes que el que**: el codi ja diu **que** fas (`environment: - DB_PASS=xxx`). El que necessita explicacio es **per que** (`# MariaDB 10.11 requereix aquesta variable per aceptar connexions externes`).

4. **Bones practiques que t'agrairàs**: com `secrets` en lloc d'env vars, o per que un servei nomes te el perfil `dev`.

5. **Cultura de projecte**: si mai comparteixes el projecte, una persona nova entendrà el per que de cada decisio.

**Exemple d'un bon `docker-compose.yml` comentat**:

```yaml
services:
  db:
    # MariaDB 10.11. A partir de la 11 cal explicit authentication plugin
    image: mariadb:10.11
    # Read-only fs nomes amb write al volum de dades. Seg cap 6.
    read_only: true
    tmpfs:
      - /tmp
      - /run/mysqld
    # ... etc
```

Els comentaris son una inversio de 5 minuts que estalviaran 2 hores de "que collons vaig pensar fa un any".

---

## Pregunta 14 (oberta): Stack de monitoritzacio amb Compose

**Resposta model**:

Per a l'stack de monitoritzacio amb Prometheus, Grafana, cAdvisor, node-exporter i Uptime Kuma, el `docker-compose.yml` seria:

```yaml
services:
  prometheus:
    image: prom/prometheus:latest
    profiles: ["prod", "dev"]  # essencial
    volumes:
      - prometheus-data:/prometheus
      - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
    networks: [monitoring]
    # No cal cap port exposat si Grafana es a la mateixa xarxa
    
  grafana:
    image: grafana/grafana:latest
    profiles: ["prod", "dev"]
    depends_on:
      prometheus: { condition: service_healthy }
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASS}
    volumes:
      - grafana-data:/var/lib/grafana
    ports:
      - "127.0.0.1:3000:3000"  # nomes localhost
    networks: [monitoring, frontend]
    
  cadvisor:
    image: gcr.io/cadvisor/cadvisor:latest
    profiles: ["prod", "dev"]
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:ro
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
    networks: [monitoring]
    
  node-exporter:
    image: prom/node-exporter:latest
    profiles: ["dev"]  # nomes en dev, perque en prod ja va amb cadvisor
    networks: [monitoring]
    
  uptime-kuma:
    image: louislam/uptime-kuma:latest
    profiles: ["prod", "dev"]
    volumes:
      - uptime-kuma-data:/app/data
    ports:
      - "127.0.0.1:3001:3001"
    networks: [monitoring, frontend]

volumes:
  prometheus-data:
  grafana-data:
  uptime-kuma-data:

networks:
  monitoring: {}
  frontend: {}
```

**Perfils**: els serveis essencials (`prometheus`, `grafana`, `cadvisor`, `uptime-kuma`) son a `prod` i `dev`. `node-exporter` nomes a `dev` perque es redundant amb `cadvisor` en un sol node.

**Xarxes**: `monitoring` (interna) i `frontend` (per exposar Grafana i Uptime Kuma). Prometheus nomes a `monitoring` perque no l'ha de veure l'usuari directament.

**Ordre d'arrencada**: Grafana espera a Prometheus. La resta poden arrencar en paral·lel. Uptime Kuma no depen de res perque nomes fa pings.

**Volums**: nomes Grafana i Uptime Kuma necessiten volum persistent. Prometheus i cAdvisor poden perdre dades en reiniciar (es rediseny per ser temporal o per rebre dades en temps real).

---

## Pregunta 15 (oberta): Secrets i variables d'entorn

**Resposta model**:

Posar totes les credencials al `docker-compose.yml` te una consequencia greu: el fitxer es queda al repositori Git, i totes les contrasenyes son accessibles a qualsevol persona que tingui acces al repo. Inclús en un repo privat, hi ha riscos: el repo es clona accidentalment, es comparteix amb un company, es penja a un backup al núvol, etc.

**Les tres estrategies**:

**1. Fitxer `.env` separat**:
- Avantatge: pots posar `.env` al `.gitignore`.
- Desavantatge: el fitxer `.env` nomes es xifrat per la proteccio del sistema de fitxers. Si la maquina es compromet, tambe.
- Us: variables d'entorn que no son altament sensibles pero que no vols al repo (exemple: contrasenyes de base de dades, tokens d'APIs externes).

**2. `secrets` (Docker native)**:
- Avantatge: els secrets es guarden com a fitxers a `/run/secrets/` dins el contenidor, no com a variables d'entorn. Es poden muntar nomes als serveis que els necesiten.
- Desavantatge: cal gestionar els fitxers de secrets manualment (els pots generar amb scripts).
- Us: credencials que han d'estar molt protegides (claus SSH, certificats, API keys importants).

**3. Gestor de secrets extern (Vault, Infisical, Bitwarden)**:
- Avantatge: secrets centralitzats, amb auditoria, rotacio, revocacio.
- Desavantatge: complexitat. Cal un servei addicional.
- Us: entorns de produccio amb multiples aplicacions.

**Recomanacio al BernatLab**:
- `.env` al `.gitignore` per a la majoria de credencials.
- `secrets` (fitxers xifrats) per a les coses mes sensibles (la clau privada del proxy, tokens d'API importants).
- Gestor extern nomes si tens mes de 5-10 serveis amb secrets i vols centralitzar.

**Trade-off final**: un sol `.env` es convenient pero menys segur. Els secrets son mes segurs pero requereixen mes feina. La majoria de persones al BernatLab poden viure amb `.env` al `.gitignore`, pero val la pena saber que existeixen alternatives.

---

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum. Docker Compose es una eina que s'aprena usant-la.
- **3-4 encerts**: Refes l'exercici. La practica es lo que fa que ho interioritzis.
- **0-2 encerts**: Repassem junts. Es un capitol dens.

## Que fer si has encertat totes

- Passa al **Capitol 5** (registre d'imatges).
- Investiga les plantilles `cookiecutter-docker` per generar projectes nous rapidament.
- Mira com es fan "blue-green deployments" amb Compose.
