# Respostes — Capítol 8: Homepage

> Mira les respostes DESPRÉS d'haver fet el qüestionari.

## Pregunta 1: Què és Homepage?

**Resposta correcta**: Un dashboard self-hosted per visualitzar serveis del teu homelab.

**Explicació**: Homepage és un "application dashboard" modern. Mostra una graella de targetes amb els teus serveis, widgets d'informació, i integracions amb altres eines. Alternatives: Heimdall, Dashy, Organizr, Flame.

## Pregunta 2: Port per defecte

**Resposta correcta**: 3000 (intern) — exposem el 3010 al host

**Explicació**: Dins del contenidor, Homepage escolta al port 3000 (port per defecte de Next.js). Al `docker-compose.yml` del BernatLab mapejem a `3010:3000` per evitar col·lisions amb altres serveis i tenir una numeració coherent (3001=Uptime, 3010=Homepage).

## Pregunta 3: Framework

**Resposta correcta**: Next.js (React)

**Explicació**: Homepage està feta amb Next.js (framework de React) i s'exporta com a aplicació estàtica + API per a les dades dinàmiques. Codi font: https://github.com/gethomepage/homepage.

## Pregunta 4: Fitxer de serveis

**Resposta correcta**: services.yaml

**Explicació**: Homepage té diversos fitxers YAML organitzats: `settings.yaml` (configuració general), `services.yaml` (serveis), `widgets.yaml` (widgets), `bookmarks.yaml` (dreceres), `docker.yaml` (integració Docker). Tots al volum `/app/config`.

## Pregunta 5: Avantatge de muntar docker.sock

**Resposta correcta**: Permet el widget Docker que llista contenidors amb el seu estat.

**Explicació**: Muntant el socket, Homepage pot parlar amb el dimoni Docker i mostrar tots els contenidors amb el seu estat, CPU%, RAM, etc. És una integració de només lectura (`:ro` = read-only) per seguretat.

## Pregunta 6: Format de configuració

**Resposta correcta**: YAML

**Explicació**: Tots els fitxers de configuració de Homepage són YAML, organitzats per seccions. Avantatge respecte JSON: més llegible, comentaris amb `#`, sintaxi més natural.

## Pregunta 7: Widget de recursos

**Resposta correcta**: resources

**Explicació**: El widget `resources` mostra CPU, RAM, disc, xarxa, temperatura (si està disponible) i uptime del sistema on corre Homepage. Molt útil per veure d'un cop d'ull l'estat de la RPi.

## Pregunta 8: Edició de fitxers

**Resposta correcta**: Es recarrega automàticament (hot-reload)

**Explicació**: Homepage té un sistema de file watcher que detecta canvis als fitxers YAML i recarrega automàticament en qüestió de segons. No cal reiniciar res. Si hi ha errors de sintaxi, ho veuràs als logs (`docker logs homepage`).

## Pregunta 9 (oberta): Avantatge de Homepage

**Resposta model**:

Homepage aporta un salt qualitatiu respecte obrir cada servei per separat. Els avantatges principals:

**1. Reducció de la càrrega cognitiva**: sense Homepage, cada vegada que vull entrar a Portainer he de recordar `http://hortosona:9000` o cercar-lo a l'historial del navegador. Amb Homepage, clico una targeta i ja hi soc. Amb 8-10 serveis, això es nota molt en l'ús diari.

**2. Visió de conjunt**: d'un cop d'ull veig tots els serveis amb el seu estat. Si tinc un widget de recursos, veig si la RPi està patint. Si tinc un widget d'Uptime Kuma, veig quin servei ha caigut. Això és informació que abans havia d'anar a buscar a 3 llocs diferents.

**3. Punt d'entrada consistent**: tant si vinc del portàtil com del mòbil, la primera pàgina és sempre la mateixa. No cal recordar URLs específiques per a cada dispositiu.

**4. Compartible selectivament**: puc ensenyar Homepage a un amic sense donar-li accés a res més. Ell veu que tinc un servidor amb Portainer, Uptime Kuma, etc., però no pot entrar-hi (calen credencials pròpies).

**5. Personalització**: el puc personalitzar amb el meu estil. Títol, fons, colors, icones. Fins i tot afegir el meu logotip. Això el fa "meu".

**6. Autoexplicatiu per a tercers**: si un dia vull explicar a algú què tinc al homelab, obro Homepage i ell ho entén visualment. Més eficaç que una llista d'URLs.

**7. Educatiu**: quan aprens a configurar un nou servei, l'afegeixes a Homepage. Això et força a pensar en la integració, el port, el nom, la descripció. És un exercici d'arquitectura.

**8. "Wow effect"**: una pàgina neta amb icones, amb el teu nom, és molt més impactant que una terminal. Útil per convèncer la parella que el que fas al cap de setmana té sentit.

## Pregunta 10 (oberta): Tres serveis nous al services.yaml

**Resposta model**:

Per afegir PiHole, Jellyfin i una pàgina personal al `services.yaml`:

```yaml
---
# Afegir dins del grup existent o crear-ne un de nou

- Multimèdia:
    - Jellyfin:
        href: http://hortosona:8096
        description: Servidor de pel·lícules i sèries
        icon: jellyfin
        siteMonitor: http://hortosona:8096
        widget:
            type: jellyfin
            url: http://jellyfin:8096
            enableNowPlaying: true

- Xarxa:
    - Pi-hole:
        href: http://hortosona:8081/admin
        description: Blocador de publicitat DNS
        icon: pihole
        siteMonitor: http://hortosona:8081/admin
        widget:
            type: pihole
            url: http://pihole:80
            token: el_teu_token_api

- Personal:
    - El meu blog:
        href: https://bernatmora.cat
        description: Notes i articles personals
        icon: blog
        siteMonitor: https://bernatmora.cat
    - Currículum:
        href: https://cv.bernatmora.cat
        icon: file
        siteMonitor: https://cv.bernatmora.cat
```

**Camps utilitzats**:

- **`href`**: URL on va el link (obligatori).
- **`description`**: text sota el nom (opcional però recomanable).
- **`icon`**: nom de la icona de la galeria d'Homepage (opcional però queda millor). Si no existeix, pots posar `icon: nom-icona.png` i afegir la imatge a `/app/config/icons/`.
- **`siteMonitor`**: URL que Homepage fa ping per veure si el servei està viu. Mostra un punt verd o vermell.
- **`widget`**: tipus de widget avançat (Jellyfin mostra "now playing", PiHole mostra estadístiques de bloqueig).

**Agrupació**: he posat els serveis en tres grups nous (`Multimèdia`, `Xarxa`, `Personal`) per organitzar-los. També podries afegir-los a grups existents com `BernatLab` o `Eines externes`.

**El widget de Jellyfin** mostrarà el que s'està reproduint ara mateix (si hi ha alguna sessió activa). **El widget de Pi-hole** mostrarà quantes peticions DNS ha bloquejat, quants clients hi ha connectats, etc.

## Què fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum, sobretot la part de configuració YAML.
- **3-4 encerts**: Practica editant el `services.yaml` directament.
- **0-2 encerts**: Repassem junts.

## Què fer si has encertat totes

- Passa al **Capítol 9** (Git i documentació).
