# Resum - Capitol 7: Actualitzacio segura

## La idea clau

Un sistema que no s'actualitza es un sistema vulnerable. Un sistema que s'actualitza MAL pot deixar-te amb serveis caiguts, dades corrompudes, o problemes de compatibilitat. La gràcia de l'actualitzacio segura es actualitzar AMB CONFIANCA: saber que passa, tenir plan B, i poder tornar enrrere si cal.

## Per que es vital actualitzar

Hi ha tres raons principals:

1. **Seguretat**: les vulnerabilitats es descobreixen constantment. CVE-2024-XXXX pot afectar el teu sistema i tu no ho saps. Les actualitzacions de seguretat son obligatories.
2. **Estabilitat**: les noves versions corregeixen bugs que poden fer-te caure.
3. **Funcionalitats**: nous serveis, millor rendiment, compatibilitat amb altres eines.

Un sistema sense actualitzacions en 6 mesos es un sistema VULNERABLE. A mes, amb el temps, els repositoris antics es queden sense suport i tens problemes per instalar coses noves.

## Apt: el gestor de paquets de Raspberry Pi OS

Apt (Advanced Package Tool) es el sistema que gestiona tot el programari del sistema. Es el "App Store" de Linux.

```bash
# Actualitzar la llista de paquets disponibles
sudo apt update

# Veure quins paquets tenen actualitzacio
apt list --upgradable

# Actualitzar tot el sistema
sudo apt upgrade -y

# Actualitzar tambe paquets que requereixen canvis mes profunds
sudo apt full-upgrade -y

# Netejar paquets no necessaris
sudo apt autoremove -y
sudo apt autoclean
```

El flux basic es sempre:

1. `apt update` (llista nova)
2. `apt upgrade` (instal·la les noves versions)
3. `apt autoremove` (neteja)

## unattended-upgrades: actualitzacions automatiques

Per a un sistema 24/7, volem que les actualitzacions de SEGURETAT es facin soles. La eina es `unattended-upgrades`:

```bash
sudo apt install -y unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

Configuracio a `/etc/apt/apt.conf.d/50unattended-upgrades`:

```
Unattended-Upgrade::Allowed-Origins {
    "origin=Debian,codename=${distro_codename},label=Debian-Security";
    "origin=Raspbian,codename=${distro_codename},label=Raspbian-Security";
};

Unattended-Upgrade::AutoFixInterruptedDpkg "true";
Unattended-Upgrade::MinimalSteps "true";
Unattended-Upgrade::Remove-Unused-Dependencies "true";
Unattended-Upgrade::Automatic-Reboot "false";
Unattended-Upgrade::Automatic-Reboot-Time "03:00";
```

Aixo configura perque:
- Nomes s'actualitzin els paquets de seguretat de Debian/Raspbian.
- Si una actualitzacio falla a mitges, es reintentara.
- Els paquets no usats es netejaran automaticament.
- **No** es reiniciara automaticament (tu decideixes quan).
- Si cal reinici, es fara a les 3:00 AM.

## Watchtower: actualitzacio automatica de contenidors

Per als contenidors Docker, la eina es **Watchtower**. Un contenidor que mira quines imatges tenen nova versio i les actualitza:

```yaml
  watchtower:
    image: containrrr/watchtower:latest
    container_name: watchtower
    restart: unless-stopped
    user: "0:0"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      - WATCHTOWER_CLEANUP=true
      - WATCHTOWER_POLL_INTERVAL=86400
      - WATCHTOWER_LABEL_ENABLE=true
      - WATCHTOWER_NOTIFICATIONS=shoutrrr
      - WATCHTOWER_NOTIFICATION_URL=telegram://...
    command:
      - '--label-enable'
      - '--include-stopped'
      - '--schedule'
      - '0 0 4 * * *'  # Cada dia a les 4:00 AM
```

Per defecte, Watchtower nomes actualitza els contenidors que tenen label `com.centurylinklabs.watchtower.enable=true`. Es la manera de controlar QUE s'actualitza:

```yaml
services:
  homeassistant:
    image: homeassistant/home-assistant:stable
    labels:
      - "com.centurylinklabs.watchtower.enable=true"
```

Si no poses aquesta label, Watchtower ignorara el contenidor. Es molt recomanable: NO vols que Watchtower actualitzi sol una base de dades critica sense la teva supervisio.

## Dependabot: actualitzacio dels teus repositoris

Si tens els teus `docker-compose.yml` i altres configuracions a un repositori Git, **Dependabot** de GitHub et pot avisar automaticament de:

- Noves versions de les imatges Docker.
- Noves versions de paquets apt.
- Vulnerabilitats conegudes (CVE matching).

Configuracio a `.github/dependabot.yml`:

```yaml
version: 2
updates:
  # Comprovar imatges Docker
  - package-ecosystem: "docker"
    directory: "/"
    schedule:
      interval: "weekly"
  
  # Comprovar paquets del sistema (GitHub Actions)
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
  
  # Pip (si tens scripts Python)
  - package-ecosystem: "pip"
    directory: "/scripts"
    schedule:
      interval: "weekly"
```

Cada dilluns rebràs una PR amb les noves versions. Tu la revises, la proves, i la merges.

## Blue-Green deployment per a contenidors

Si vols actualitzar un servei CRITIC sense temps d'inactivitat, la tecnica es **blue-green deployment**: tens dos entorns (blue i green), un esta actiu i l'altre es la nova versio. Quan la nova esta llesta, canvies quin es el "principal".

A la RPi això es complicat (pocs recursos per tenir 2 copies de cada cosa), pero es pot fer per serveis petits:

```bash
# Pas 1: desplega la nova versio amb un port diferent
docker run -d --name servei-green -p 8081:80 servei:v2

# Pas 2: comprova que funciona
curl http://localhost:8081

# Pas 3: atura la vella i arranca la nova al port original
docker stop servei-blue
docker rm servei-blue
docker run -d --name servei-blue -p 8080:80 servei:v2

# Pas 4: neteja
docker stop servei-green
docker rm servei-green
```

Per serveis mes complexes, docker-compose te una opcio `pull_policy: always` que fa que cada `docker compose up` torni a baixar la imatge.

## Rolling updates: mes realista

A la practica, per a una RPi fem **rolling updates manuals**:

1. **Abans d'actualitzar**: fer backup (cap 8 del M3).
2. **Llegir el CHANGELOG**: que canvia? hi ha breaking changes?
3. **Provar en un entorn local**: si tens un altre RPi o un portainer staging, prova primer aqui.
4. **Actualitzar en hores de baixa activitat**: no a les 8 del mati.
5. **Actualitzar un sol servei a la vegada**: no tot de cop.
6. **Verificar que funciona**: curl, grafana, logs.
7. **Si algo va malament**: torna a la versio anterior (pull de la imatge vella).

## El fitxer CHANGELOG

Quan actualitzis, SEMPRE mira el CHANGELOG. Es un fitxer que els projectes mantenen amb els canvis de cada versio. A Docker Hub, es a la dreta de la pagina de la imatge. A GitHub, es al fitxer `CHANGELOG.md` o `RELEASES.md`.

Exemple del que busques:

```
v2.5.0 (2026-05-01):
  BREAKING: canvi en la configuracio de xarxa
  Nova opcio: --new-feature
  Bugfix: corregit memory leak a HA
```

Si veus "BREAKING" o "breaking change", vol dir que la teva configuracio pot deixar de funcionar. Llegeix amb cura.

## El concepte de "pinning" de versions

Un dels errors mes comuns es fer `image: homeassistant/home-assistant:latest` (sense versio). Aixo vol dir que cada vegada que fas `docker pull`, pots obtenir una versio diferent. Si el projecte fa un canvi important, el teu sistema pot trencar-se d'un dia per l'altre.

SEMPRE usa versions explicites:

```yaml
# BE
image: homeassistant/home-assistant:2024.5.0

# MAL
image: homeassistant/home-assistant:latest
```

I si vols actualitzar periodicament, usa un rang:

```yaml
# Aixo sempre tindra la ultima 2024.X
image: homeassistant/home-assistant:2024
```

## Estrategia de versions

Un patro molt usat es el **MAJOR.MINOR.PATCH**:

- **MAJOR** (v1 -> v2): canvis incompatibles. Cal planificar.
- **MINOR** (v1.5 -> v1.6): noves funcionalitats, generalment compatibles.
- **PATCH** (v1.5.3 -> v1.5.4): correccions de bugs i seguretat. Sempre aplicar.

Per tant:
- **Sempre** actualitza PATCH.
- **Regularment** actualitza MINOR (cada 1-3 mesos).
- **Amb molta cura** actualitza MAJOR (1 cop l'any, amb proves).

## Connexions amb altres capitols

- **M2 Cap 7** - Actualitzacio de contenidors (versio previa, Docker basic).
- **M2 Cap 8** - Backups: SEMPRE fer backup abans d'actualitzar.
- **M6 Cap 4** - Alertes: rebràs alertes si una actualitzacio trenca alguna cosa.
- **M3 Cap 1** - Estrategia de backup: el backup es la teva xarxa de seguretat.
