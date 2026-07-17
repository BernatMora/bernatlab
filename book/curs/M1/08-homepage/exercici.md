# Exercici pràctic — Capítol 8: Homepage

> 45-60 min · Real al teu sistema

## Objectiu

Instal·lar Homepage, configurar els serveis del BernatLab amb bind mount per poder editar la configuració còmodament, afegir widgets i deixar un dashboard personalitzat amb 5+ serveis, 2 widgets i un aspecte propi.

## Requisits
- Docker corrent
- Tailscale actiu
- 45-60 minuts
- Tenir Portainer, Uptime Kuma i whoami operatius (caps 6-7)

## Pas 1: Afegeix Homepage al compose (5 min)

Edita `~/homelab/docker/docker-compose.yml`:

```yaml
version: "3.9"

services:
  homepage:
    image: ghcr.io/gethomepage/homepage:latest
    container_name: homepage
    ports:
      - "3010:3000"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - homepage_config:/app/config
    restart: unless-stopped

  portainer:
    image: portainer/portainer-ce:latest
    container_name: portainer
    ports:
      - "9000:9000"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - portainer_data:/data
    restart: unless-stopped

  uptime-kuma:
    image: louislam/uptime-kuma:latest
    container_name: uptime-kuma
    ports:
      - "3001:3001"
    volumes:
      - uptime_data:/app/data
      - /var/run/docker.sock:/var/run/docker.sock
    restart: unless-stopped

  whoami:
    image: traefik/whoami
    container_name: whoami
    ports:
      - "8080:80"
    restart: unless-stopped

volumes:
  homepage_config:
  portainer_data:
  uptime_data:
```

```bash
cd ~/homelab/docker
docker compose up -d
```

## Pas 2: Accedeix a Homepage (5 min)

1. Obre `http://hortosona:3010`.
2. Hauries de veure la pàgina per defecte amb serveis d'exemple.

## Pas 3: Prepara una carpeta de configuració persistent (10 min)

Per facilitar l'edició, copiem la config per defecte i la muntem al host:

```bash
# Crea la carpeta
mkdir -p ~/homelab/config/homepage

# Copia la config per defecte del contenidor
docker cp homepage:/app/config/settings.yaml ~/homelab/config/homepage/settings.yaml
docker cp homepage:/app/config/services.yaml ~/homelab/config/homepage/services.yaml
docker cp homepage:/app/config/widgets.yaml ~/homelab/config/homepage/widgets.yaml
docker cp homepage:/app/config/bookmarks.yaml ~/homelab/config/homepage/bookmarks.yaml
docker cp homepage:/app/config/docker.yaml ~/homelab/config/homepage/docker.yaml 2>/dev/null

# Mira què tens
ls -la ~/homelab/config/homepage/

# Esborra el contenidor (per tornar-lo a crear amb el bind mount)
docker compose down homepage
```

Edita el `docker-compose.yml` per muntar la carpeta:

```yaml
homepage:
    image: ghcr.io/gethomepage/homepage:latest
    container_name: homepage
    ports:
        - "3010:3000"
    volumes:
        - /var/run/docker.sock:/var/run/docker.sock:ro
        - /home/bernat/homelab/config/homepage:/app/config   # bind mount
    restart: unless-stopped
```

```bash
docker compose up -d homepage
```

Ara editar fitxers al host és reflecteix al contenidor.

## Pas 4: Configura el services.yaml (15 min)

```bash
nano ~/homelab/config/homepage/services.yaml
```

Substitueix el contingut per:

```yaml
---
- BernatLab:
    - Portainer:
        href: http://hortosona:9000
        description: Administracio Docker
        icon: portainer
        siteMonitor: http://hortosona:9000
    - Uptime Kuma:
        href: http://hortosona:3001
        description: Monitoratge i alertes
        icon: uptime-kuma
        siteMonitor: http://hortosona:3001
    - Whoami:
        href: http://hortosona:8080
        description: Servei de proves HTTP
        icon: whoami
- Eines externes:
    - GitHub:
        href: https://github.com/bernatmora
        icon: github
        siteMonitor: https://github.com
    - Cloudflare:
        href: https://dash.cloudflare.com
        icon: cloudflare
    - DuckDuckGo:
        href: https://duckduckgo.com
        icon: duckduckgo
        siteMonitor: https://duckduckgo.com
```

Recarrega `http://hortosona:3010` (5-10 segons) i comprova els canvis.

## Pas 5: Configura widgets i settings (5 min)

```bash
nano ~/homelab/config/homepage/widgets.yaml
```

```yaml
---
resources:
    cpu: true
    memory: true
    disk: /
    network: false
    temperature: true
    cputemp: true
    uptime: true

search:
    provider: custom
    url: https://duckduckgo.com/?q=
```

```bash
nano ~/homelab/config/homepage/settings.yaml
```

```yaml
---
title: BernatLab
background:
    opacity: 30
    image: https://images.unsplash.com/photo-1517336714731-489689fd1ca8
color: slate
theme: dark
```

Recarrega la pàgina.

## Pas 6: Afegeix el widget d'Uptime Kuma (5 min)

Afegeix un widget que consumeixi la Status Page que vas crear al cap. 7:

```bash
nano ~/homelab/config/homepage/widgets.yaml
```

Afegeix a sota de `search:`:

```yaml
uptimekuma:
    - bernatlab Status Page
```

Ara navega a la teva Status Page pública d'Uptime Kuma, copia l'URL, i configura l'API:

```bash
nano ~/homelab/config/homepage/settings.yaml
```

Afegeix:

```yaml
---
# ... el que ja tens ...
# (deixa el que ja hi ha)
```

Afegeix un fitxer nou:

```bash
nano ~/homelab/config/homepage/uptimekuma.yaml
```

```yaml
---
- name: BernatLab
  id: bernatlab
  url: http://localhost:3001/status/bernatlab
  type: statusPage
```

Comprova que apareix un widget amb l'estat dels teus serveis.

## Pas 7: Personalitza el tema (5 min)

Prova diferents combinacions:

```bash
nano ~/homelab/config/homepage/settings.yaml
```

Canvia:
- `color: slate` → `color: indigo`, `color: emerald`, `color: amber`
- `theme: dark` → `theme: light`
- Prova diferents URLs al `background.image`

Recarrega la pàgina cada vegada. Escull el que més t'agradi.

## Pas 8: Comprova i documenta

Mira com queda tot plegat. Comparteix la URL amb tu mateix via Telegram i obre-la al mòbil (necessitaràs Tailscale al mòbil).

Documenta a `book/curs/M1/08-homepage/diari.md` amb:
- Captura de pantalla del dashboard final.
- Els 4 fitxers YAML finals.
- Quines personalitzacions has fet i per què.
- Quin widget trobes més útil.

## Validació

Has acabat si:
- [ ] Homepage corre a `http://hortosona:3010`.
- [ ] La configuració és persistent (bind mount).
- [ ] Tens almenys 5 serveis al dashboard.
- [ ] El widget `resources` funciona (CPU/RAM/temp).
- [ ] El widget `search` funciona.
- [ ] El widget d'Uptime Kuma mostra l'estat dels teus serveis.
- [ ] El títol i tema estan personalitzats.
- [ ] Has documentat l'experiència.

## Per aprofundir

- Afegeix el widget d'Uptime Kuma (consultant el slug del teu Status Page).
- Crea una icona personalitzada per a un servei que no en tingui.
- Experimenta amb diferents fons i paletes de colors.
- Afegeix un widget de temps per a la teva localitat (Vic, Manresa, etc.).
- Configura múltiples grups de serveis (per categoria).
- Afegeix bookmarks per a les webs que visites sovint.

## Ves un pas més enllà

**Repte avançat: layout responsive i personalitzat**.

Homepage permet organitzar els widgets en columnes. Per exemple, pots tenir el `resources` a l'esquerra, els serveis al centre, i un quadre de notes personal a la dreta.

1. Afegeix un quadre de notes a `~/homelab/config/homepage/widgets.yaml`:

```yaml
---
# ... el que ja tens ...
notes:
    - Cos a fer:
        - [ ] Comprar sensor temperatura hort
        - [ ] Configurar backups automatics
        - [ ] Acabar M2 del curs
    - Comandes utils:
        - ssh bernat@hortosona
        - cd ~/homelab/docker && docker compose ps
```

2. Configura un layout de columnes a `settings.yaml`:

```yaml
---
# ... el que ja tens ...
layout:
    header:
        style: row
    sidebar:
        style: column
        widgets: [resources, search]
    top:
        style: row
        widgets: [notes]
```

3. Crea un quadre de meteo local. Busca a https://openweathermap.org/ una API key gratuïta i:

```bash
nano ~/homelab/config/homepage/widgets.yaml
```

```yaml
weather:
    - Vic:
        lat: 41.9304
        lon: 2.2549
        provider: openweathermap
        apiKey: LA_TEVA_API_KEY
        units: metric
        cache: 30
```

4. Comprova que tot es veu com esperes. Fes captures a mòbil i escriptori — ha de ser usable als dos.

Ara tens un dashboard real, útil, i personalitzat. Comparteix-lo amb orgull.
