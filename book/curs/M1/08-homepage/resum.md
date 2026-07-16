# Resum — Capítol 8: Homepage

## La idea clau

Un cop tens 5-10 serveis corrent (Portainer, Uptime Kuma, Whoami, etc.), el problema és: "com recordo l'adreça de cadascun?". **Homepage** és un dashboard modern que centralitza tots els serveis del BernatLab en una sola pàgina web bonica. És la "porta d'entrada" al teu homelab, accessible via `http://hortosona:3010` (o `http://100.115.134.76:3010` des de fora).

## Què és exactament Homepage?

Homepage és una aplicació web de tipus "application dashboard" feta en Next.js (React). Mostra una graella de targetes, cadascuna representant un servei. Algunes d'elles mostren dades en temps real (latència, estat, pings, temperatures, etc.).

Característiques:

- **100% self-hosted**: totes les dades viuen al teu servidor.
- **Configuració en YAML**: un sol fitxer, fàcil de versionar amb Git.
- **Molts widgets integrats**: serveis, recursos del sistema, cerques, informació meteorològica, etc.
- **Integracions natives**: Docker, Uptime Kuma, PiHole, Glances, Proxmox, NPM, Traefik, etc.
- **Temes**: clar, fosc, personalitzable.
- **Bookmarks i cerques**: dreceres ràpides.

Alternatives: Heimdall (clàssic, menys polit), Dashy, Organizr, Flame. Homepage és la que té millor equilibri funcionalitat/estètica el 2026.

## Per què l'usem al BernatLab

- **Punt d'entrada únic**: en lloc de recordar 8 URLs, tens una pàgina.
- **Visió ràpida**: d'un cop d'ull saps l'estat de tot.
- **Personal**: pots personalitzar-la amb el teu gust (colors, logotip, layout).
- **Compartible**: la pots mostrar a amics sense donar-los accés a res més.
- **Autoexplicatiu**: si algú veu el BernatLab, entén ràpidament què hi ha.

## Instal·lació al BernatLab

```yaml
# Afegir a ~/homelab/docker/docker-compose.yml
services:
  homepage:
    image: ghcr.io/gethomepage/homepage:latest
    container_name: homepage
    ports:
      - "3010:3000"
    volumes:
      - homepage_config:/app/config
      - /var/run/docker.sock:/var/run/docker.sock:ro
    restart: unless-stopped

volumes:
  homepage_config:
```

```bash
cd ~/homelab/docker
docker compose up -d homepage
```

Accedeix a `http://hortosona:3010`. La primera vegada veuràs una pàgina amb serveis d'exemple.

## Configuració: fitxers YAML

Tota la configuració viu a `/app/config` dins del contenidor (que és el volum `homepage_config` al host). Els fitxers principals són:

- **`settings.yaml`**: configuració general (títol, tema, fons, color d'accent, etc.).
- **`services.yaml`**: llista de serveis amb les seves targetes.
- **`widgets.yaml`**: configuració dels widgets (resources, search, etc.).
- **`bookmarks.yaml`**: dreceres ràpides.
- **`docker.yaml`**: integració automàtica amb Docker.
- **`/icons/`**: icones personalitzades dels serveis.

Pots muntar una carpeta local per editar-los fàcilment:

```yaml
volumes:
  - /home/bernat/homelab/config/homepage:/app/config
```

Així edites amb `nano` a la RPi i els canvis es recarreguen automàticament (Homepage té hot-reload).

## Un services.yaml bàsic

```yaml
---
# services.yaml
- BernatLab:
    - Portainer:
        href: http://hortosona:9000
        description: Administracio Docker
        icon: portainer
        siteMonitor: http://hortosona:9000
    - Uptime Kuma:
        href: http://hortosona:3001
        description: Monitoratge de serveis
        icon: uptime-kuma
        siteMonitor: http://hortosona:3001
        widget:
            type: uptime-kuma
            url: http://uptime-kuma:3001
            sitesMonitorSlug: bernatlab
    - Whoami:
        href: http://hortosona:8080
        description: Servei de proves
        icon: whoami
        siteMonitor: http://hortosona:8080
- Eines:
    - Grafana:
        href: http://hortosona:3030
        description: Grafiques del sistema
        icon: grafana
    - File Browser:
        href: http://hortosona:8082
        description: Gestor de fitxers web
        icon: filebrowser
- Externs:
    - GitHub:
        href: https://github.com/bernatmora
        icon: github
        siteMonitor: https://github.com
    - Cloudflare:
        href: https://dash.cloudflare.com
        icon: cloudflare
```

Aquí veiem tres grups ("BernatLab", "Eines", "Externs") amb serveis dins. Cada servei té:
- `href`: on va el link.
- `description`: text sota el nom.
- `icon`: icona (Homepage té una galeria d'icones preconfigurades).
- `siteMonitor`: si vols monitorar si l'URL respon.
- `widget`: configuració de widget avançat.

## Widgets destacats

Homepage té widgets que mostren dades en temps real. Alguns dels millors:

### Resources (CPU, RAM, Disc)

Mostra l'ús actual dels recursos del sistema on corre Homepage (la RPi).

```yaml
# widgets.yaml
resources:
    cpu: true
    memory: true
    disk: /
    network: false
    temperature: true
    uptime: true
    cputemp: true
```

Si tens el sensor de temperatura de la RPi, veuràs la temperatura del SoC.

### Uptime Kuma

Mostra l'estat dels monitors d'Uptime Kuma en forma de llista compacta:

```yaml
- Uptime Kuma:
    widget:
        type: uptime-kuma
        url: http://uptime-kuma:3001
        sitesMonitorSlug: bernatlab
        # slug del Status Page configurat a Uptime Kuma
```

### Search

Una barra de cerca ràpida (Google, DuckDuckGo, etc.):

```yaml
- Search:
    widget:
        type: search
        url: https://duckduckgo.com/?q=
```

### Weather (Open-Meteo, sense API key)

```yaml
- Weather:
    widget:
        type: weather
        location: Vic, Catalunya
        units: metric
```

### Docker

Llista tots els contenidors amb el seu estat:

```yaml
# Cal tenir /var/run/docker.sock muntat
- Docker:
    widget:
        type: docker
        server: local  # el propi Docker
```

## Settings.yaml: el toc personal

```yaml
---
# settings.yaml
title: BernatLab
background:
    opacity: 50
    blur: yes
    image: https://images.unsplash.com/photo-...
color: slate
theme: dark
favicon: /icons/favicon.ico
```

Camps clau:
- **`title`**: títol a la pestanya del navegador.
- **`background`**: imatge de fons (opcional).
- **`color`**: paleta de colors (slate, gray, zinc, etc.).
- **`theme`**: `dark` o `light`.
- **`favicon`**: icona personalitzada.

## Icones personalitzades

Homepage té una galeria d'icones preconfigurades (~500). Si el teu servei no n'hi té, pots:

1. Afegir la icona a `/app/config/icons/` (muntatge).
2. Referenciar-la amb `icon: nom-icona.png` o `icon: nom-icona.svg`.

Formats suportats: SVG, PNG, ICO.

## Hot-reload i desenvolupament

Quan edites un fitxer YAML, els canvis es recarreguen automàticament en pocs segons. Per veure errors de sintaxi:

```bash
docker logs homepage
```

Si tens problemes, mira els logs.

## Connexions amb altres capítols

- **Cap 5-7** — Homepage és un contenidor Docker que enllaça a Portainer i Uptime Kuma.
- **Cap 9** — La configuració YAML es pot versionar amb Git.
- **Cap 22** — Grafana donarà mètriques molt més riques que el widget de Resources.
- **Cap 23** — Status Pages més elaborades (s'independitzen d'Homepage).

Ja tens la porta d'entrada. Ara toca posar ordre: versionar tota aquesta configuració amb Git.
