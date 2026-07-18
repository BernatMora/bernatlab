# Respostes — Capítol 6: Portainer

> Mira les respostes DESPRÉS d'haver fet el qüestionari.

## Pregunta 1: Què és Portainer?

**Resposta correcta**: Una interfície gràfica web per administrar Docker.

**Explicació**: Portainer és una eina que ens permet gestionar Docker sense memoritzar ordres. Per a homelabs és perfecta: ni massa simple ni aclaparadora. Alternatives: Dockge, Yacht, CasaOS.

## Pregunta 2: Port per defecte

**Resposta correcta**: 9000

**Explicació**: Portainer per defecte escolta al port 9000 (UI) i 9443 (HTTPS). Pots canviar-ho passant `ports:` al docker-compose. Al BernatLab l'exposem al 9000 per accedir fàcilment.

## Pregunta 3: Com accedir a Portainer al BernatLab

**Resposta correcta**: http://hortosona:9000 (o per IP Tailscale 100.x.y.z:9000)

**Explicació**: Un cop exposat el port 9000 al compose, pots accedir des de qualsevol dispositiu de la xarxa Tailscale. MagicDNS resol `hortosona` a la IP correcta.

## Pregunta 4: Com comunica amb Docker

**Resposta correcta**: A través del socket /var/run/docker.sock

**Explicació**: Muntem el socket dins del contenidor amb `-v /var/run/docker.sock:/var/run/docker.sock`. Això permet a Portainer executar ordres Docker "com si fos" l'amfitrió. Alternativa: API REST amb port 2375, però el socket és més segur.

## Pregunta 5: Què és un Stack?

**Resposta correcta**: Un grup de serveis relacionats, definit normalment amb docker-compose.yml.

**Explicació**: Un Stack a Portainer és el que s'anomena "projecte" a Docker Compose. Per convenció, un stack = un `docker-compose.yml`. Pots tenir stacks separats per "famílies" de serveis (monitoratge, emmagatzematge, etc.).

## Pregunta 6: Què pots fer dins d'un contenidor?

**Resposta correcta**: Veure logs, mètriques, consola, start/stop/restart, recrear.

**Explicació**: Pràcticament tot el que faries per terminal, excepte coses avançades com accedir a volums d'altres contenidors o configurar xarxes noves.

## Pregunta 7: Avantatge de Portainer

**Resposta correcta**: Visibilitat centralitzada, control amb clics, no cal recordar ordres.

**Explicació**: Amb Portainer, d'un cop d'ull saps què està actiu, què ha caigut, i pots fer les operacions habituals en 2-3 clics. Especialment útil quan tens 8-15 serveis i vols evitar-te teclejar ordres llargues.

## Pregunta 8: Conflikte docker-compose + Stack

**Resposta correcta**: Poden xocar i crear contenidors duplicats o conflictes de ports.

**Explicació**: Si el mateix servei el desplegues via `docker compose up` al sistema de fitxers I via un Stack a Portainer, tindràs dos contenidors amb el mateix nom o competint pel port. Per això al BernatLab mantenim la regla: tot via `docker-compose.yml`, Portainer només per visualitzar i operar.

## Pregunta 9 (oberta): Quan Portainer vs SSH

**Resposta model**:

Al BernatLab, la regla pràctica és:

**Fer servir Portainer per a**:
- **Visualitzar l'estat general**: d'un cop d'ull veure quins contenidors corren, quins han caigut.
- **Operacions ràpides**: reiniciar un servei que ha petat, mirar els seus logs, entrar a la consola.
- **Diagnòstic inicial**: quan alguna cosa no funciona, el primer que faig és anar a Portainer i mirar logs/mètriques.
- **Gestió de volums**: veure quins existeixen, la mida, navegar pel contingut.
- **Convèncer visitants**: "mira, tinc un servidor web corrent, mira aquesta gràfica de CPU, mira com reinicio el servei amb un clic" — impressiona més que una terminal.

**Fer servir SSH/terminal per a**:
- **Crear o modificar el `docker-compose.yml`**: nano és imbatible per a editar fitxers.
- **Construir imatges personalitzades**: `docker build`, dockerfiles.
- **neteja massiva**: `docker system prune`, scripts amb `docker rm $(docker ps -a -q)`.
- **Operacions avançades**: configurar xarxes complexes, modes Swarm, registre privat.
- **Automatització**: scripts que paren/inicien contenidors segons condicions.
- **Quan Portainer falla**: si el propi Portainer cau, no pots accedir-hi! Per això és vital saber fer les coses per terminal.

**Exemples concrets al BernatLab**:
- 6 del matí rebo una alerta d'Uptime Kuma: "Portainer no respon". Connecto per SSH, `docker ps -a`, veig que el contenidor ha mort. `docker logs portainer`, trobo l'error. `docker compose up -d portainer`. Solucionat.
- Vull afegir un nou servei (Jellyfin). Obro `nano ~/homelab/docker/docker-compose.yml`, afegigo el servei, `docker compose up -d`. Després miro Portainer per veure que tot ha pujat bé i per monitorar-lo.
- Tinc curiositat per veure quin procés consumeix més CPU. Vés a Portainer, contenidor, stats, i veig una gràfica en temps real. Més ràpid que `docker stats` per terminal.

## Pregunta 10 (oberta): Nou servei via Portainer

**Resposta model**:

Per afegir Gitea (servei d'allotjament de Git) fent servir NOMÉS Portainer:

**1. Anar a la secció Stacks**:
- Clica "App Templates" o "Add stack" al menú lateral.
- Clica "Add stack".

**2. Configurar el stack**:
- **Name**: `gitea`.
- **Build method**: "Web editor" (recomanable, veuràs el YAML).
- **Web editor**: enganxa el següent YAML:
  ```yaml
  services:
    gitea:
      image: gitea/gitea:latest
      container_name: gitea
      environment:
        - USER_UID=1000
        - USER_GID=1000
      restart: unless-stopped
      volumes:
        - gitea_data:/data
        - /etc/timezone:/etc/timezone:ro
        - /etc/localtime:/etc/localtime:ro
      ports:
        - "3000:3000"
        - "2222:22"

  volumes:
    gitea_data:
  ```

**3. Variables d'entorn** (opcional, aquí les hem posat dins el YAML).

**4. Clica "Deploy the stack"**. Portainer triga uns segons:
- Descarrega la imatge `gitea/gitea:latest` (pot trigar 1-2 min la primera vegada).
- Crea el volum.
- Aixeca el contenidor.

**5. Verificar**:
- Clica a "Containers" i comprova que `gitea` està "healthy" o "running".
- Clica sobre `gitea` > "Logs" per veure l'arrencada.
- Obre `http://hortosona:3000` al navegador per accedir a la UI de Gitea.

**6. Configurar Gitea**:
- Primera vegada et porta a `/install`.
- Configura la base de dades (SQLite3 per defecte, perfecte per homelab).
- Crea l'usuari admin.

**7. Si cal actualitzar**:
- Torna a "Stacks" > "gitea" > "Editor".
- Canvia `latest` per la nova versió o simplement fes "Pull and redeploy" si vols actualitzar.
- Clica "Update".

**Caveat important**: aquesta manera és bona per a proves, però al BernatLab preferim mantenir tot el `docker-compose.yml` al sistema de fitxers (a `~/homelab/docker/docker-compose.yml`) i usar Portainer només per visualitzar i operar. Així tenim una sola font de veritat i podem versionar el compose amb Git (cap 9).

## Què fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum, sobretot la part de "build method".
- **3-4 encerts**: Practica més amb Portainer en directe.
- **0-2 encerts**: Repassem el capítol.

## Què fer si has encertat totes

- Passa al **Capítol 7** (Uptime Kuma).
