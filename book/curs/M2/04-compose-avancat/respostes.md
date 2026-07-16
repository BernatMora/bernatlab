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

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum. Docker Compose es una eina que s'aprena usant-la.
- **3-4 encerts**: Refes l'exercici. La practica es lo que fa que ho interioritzis.
- **0-2 encerts**: Repassem junts. Es un capitol dens.

## Que fer si has encertat totes

- Passa al **Capitol 5** (registre d'imatges).
- Investiga les plantilles `cookiecutter-docker` per generar projectes nous rapidament.
- Mira com es fan "blue-green deployments" amb Compose.
