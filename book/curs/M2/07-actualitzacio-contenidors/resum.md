# Resum - Capitol 7: Actualitzacio de contenidors

## La idea clau

Els serveis en contenidors s'han d'actualitzar periodicament: per seguretat (CVE nous), per noves funcionalitats, per compatibilitat. Hi ha dues maneres principals: **manual** (tu decideixes quan) o **automàtica** amb Watchtower. La bona noticia es que Docker facilita molt les actualitzacions: nomes cal canviar el tag de la imatge i tornar a arrencar.

## Per que cal actualitzar

- **Seguretat**: cada setmana es descobreixen noves vulnerabilitats a llibreries comunes. Si no actualitzes, el teu servei es vulnerable a atacs coneguts.
- **Estabilitat**: les versions noves solen corregir bugs.
- **Funcionalitats**: cada versio aporta millores.
- **Compatibilitat**: si tot evoluciona, el teu servei queda obsolet.

Risc: actualitzar pot trencar coses (un plugin deixa de funcionar, una API canvia, etc.). Per això sempre es fa amb **backup previ** i preferiblement en un entorn de proves.

## Com s'actualitza manualment

El cas basic: canviar la versio d'una imatge.

```bash
# Pas 1: backup
# (sempre abans!)

# Pas 2: parar el servei antic
docker compose down web

# Pas 3: baixar la nova imatge
docker compose pull web

# Pas 4: arrencar amb la nova versio
docker compose up -d web

# Pas 5: verificar
docker compose logs -f web
```

Si tot funciona be, perfecte. Si no, tornar al pas 1 i restaurar el backup.

## Watchtower: actualitzacio automatica

**Watchtower** es un contenidor que mira automaticament si hi ha noves versions de les imatges dels teus contenidors i, si en troba, els actualitza.

### Instal·lacio

```yaml
# docker-compose.yml
services:
  watchtower:
    image: containrrr/watchtower
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      - WATCHTOWER_LABEL_ENABLE=true   # nomes actua amb label
      - WATCHTOWER_CLEANUP=true        # esborra imatges antigues
      - WATCHTOWER_POLL_INTERVAL=86400 # un cop al dia
```

I al servei que vols que s'actualitzi automaticament:

```yaml
services:
  nextcloud:
    image: nextcloud:stable
    labels:
      - "com.bernatlab.enable=true"  # <- aixo permet que Watchtower l'actualitzi
```

### Com funciona

Cada `WATCHTOWER_POLL_INTERVAL` segons (per defecte cada 5 min, recomanable 86400 = 1 cop al dia), Watchtower:

1. Mira tots els contenidors actius.
2. Filtra pels labels (si `--label-enable` esta activat).
3. Per a cada contenidor, mira a Docker Hub si la imatge te una versio nova.
4. Si la te, atura el contenidor antic, n'arrenca un amb la nova imatge.
5. Esborra la imatge antiga (si `WATCHTOWER_CLEANUP=true`).
6. Envia una notificacio (si esta configurada).

### Configuracio important

```bash
# Nomes actualitzar contenidors amb label especific
--label-enable
WATCHTOWER_LABEL_ENABLE=true

# Esborrar imatges antigues
WATCHTOWER_CLEANUP=true

# Interval (cron format: min hora dia mes dia_setmana)
--schedule "0 0 4 * * *"  # cada dia a les 4 AM
WATCHTOWER_POLL_INTERVAL=86400

# Notificacions
WATCHTOWER_NOTIFICATIONS=shoutrrr
WATCHTOWER_NOTIFICATION_URL=shoutrrr://discord://token@channel

# Watchtower nomes per a imatges especifiques
WATCHTOWER_INCLUDE_STOPPED=false
WATCHTOWER_REVIVE_STOPPED=false
```

## Bones practiques

1. **Label nomes el que vulguis actualitzar**: no activis Watchtower per a serveis critics (bases de dades, eina de backups). Fes-los manualment.

2. **Backup abans d'actualitzar**: Watchtower no fa backups. Si una actualitzacio trenca algo, has d'estar preparat per restaurar.

3. **Notifications**: configura Watchtower per a que t'avisi quan actualitza. Aixi saps que ha passat i pots verificar.

4. **Interval raonable**: un cop al dia es el minim recomanable. Un cop per hora es massa frequent (molta carrega al servidor i al Docker Hub).

5. **Monitoritza els logs**: revisa els logs de Watchtower regularment. Si una actualitzacio falla, vols saber-ho.

## Rolling updates i blue-green

Si tens multiples instancies d'un servei (tipicament amb un balancer), pots fer actualitzacions **sense temps d'inactivitat**.

### Rolling update

Substituir instancies una a una:

```
Inici:    [v1] [v1] [v1]   <- 3 instancies
Pas 1:    [v2] [v1] [v1]   <- substituim la 1, hi ha servei
Pas 2:    [v2] [v2] [v1]
Final:     [v2] [v2] [v2]   <- tot actualitzat
```

A Docker Swarm i Kubernetes es fa automaticament. Amb Compose normal, has de fer-ho manualment:

```bash
docker compose up -d --no-deps --scale web=2 web
# Ara tens 2 instancies noves (v2) i 1 d'antiga (v1)
docker compose up -d --no-deps --scale web=1 web
# Finalment nomes queden les noves
```

### Blue-green deployment

Tenir dues versions corrent en paral·lel i canviar el tràfic nomes quan la nova funciona:

```
Inici:    [blue v1]  <- usuaris
Pas 1:    [blue v1] [green v2]  <- green en proves
Pas 2:    [green v2]  <- balancer apunta a green, blue aturat
Final:     [green v2]  <- nomes queda green
```

Si algo falla, pots tornar a blue en segons. Es la tecnica mes segura pero mes costosa (duplica els recursos temporalment).

## Healthchecks: el cor de l'autohealing

Un healthcheck es una comanda que Docker executa periodicament. Si falla, Docker pot reiniciar el contenidor:

```yaml
services:
  web:
    image: nginx
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 10s
    restart: unless-stopped
```

Quan Docker veu que un contenidor esta "unhealthy" durant massa estona, el reinicia. Combinat amb Watchtower, tens un sistema que s'auto-repara.

## Limitacions de Watchtower

Watchtower te alguns inconvenients:

- **No fa backups**: si una actualitzacio trenca algo, no tens un backup automatic.
- **No sempre enten l'API**: alguns serveis necessiten executar scripts d'upgrade (com Nextcloud). Watchtower nomes canvia la imatge, no executa scripts.
- **Pot trencar volums**: si la nova versio canvia el format de les dades, pots perdre dades.
- **No es bo per a bases de dades**: actualitzar una base de dades sense un upgrade plan es perillos.

Per aixo, la recomanacio al BernatLab es:
- Watchtower nomes per a serveis "menors" (eines de dev, exporters, eines d'analisi).
- Actualitzacio manual per a serveis critics (Nextcloud, base de dades, eina de backups).
- Sempre amb backup previ.

## Connexions amb altres capitols

- **M2 Cap 1** - Les imatges noves son les que es descarrega Watchtower.
- **M2 Cap 5** - Si tens un registre privat, Watchtower pot treballar nomes amb ell.
- **M2 Cap 6** - Actualitzar es part de la seguretat.
- **M2 Cap 8** - Backup automatic abans d'actualitzar.
