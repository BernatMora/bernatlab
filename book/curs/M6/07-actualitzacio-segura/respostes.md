# Respostes - Capitol 7: Actualitzacio segura

> Mira les respostes DESPRES d'haver fet el qüestionari.

## Pregunta 1: Comanda apt update

**Resposta correcta**: `sudo apt update`.

**Explicacio**: `apt update` nomes actualitza la LLISTA de paquets disponibles (la info del que hi ha als repositoris). No instala res nomes. Cal executar `apt upgrade` despres per instalar les noves versions. Si nomes fas `apt upgrade` sense update, treballaras amb informacio obsoleta.

---

## Pregunta 2: Actualitzacions automatiques

**Resposta correcta**: `unattended-upgrades`.

**Explicacio**: `unattended-upgrades` es el paquet oficial de Debian/Ubuntu/Raspbian per fer actualitzacions automatiques. Es pot configurar quins origens (repositoris) vols actualitzar, quan, i si vols rebre notificacions. Es la opcio "standard" i suportada oficialment.

---

## Pregunta 3: Actualitzacio de contenidors

**Resposta correcta**: Watchtower.

**Explicacio**: Watchtower es un contenidor que mira periodicament si les imatges dels teus altres contenidors tenen nova versio, i les actualitza. Es el mes popular, pero hi ha alternatives com Ouroboros (molt mes lleuger) o Diun (que nomes avisa, no actualitza). El control fi es amb labels.

---

## Pregunta 4: Label de Watchtower

**Resposta correcta**: `com.centurylinklabs.watchtower.enable=true`.

**Explicacio**: Quan Watchtower s'executa amb `--label-enable`, nomes toca els contenidors que tenen aquesta label. Es la manera de controlar QUE s'actualitza. Si no tens label, Watchtower no toca el contenidor. Es opt-in, no opt-out.

---

## Pregunta 5: Per que no `latest`

**Resposta correcta**: Perque cada pull pot obtenir una versio diferent i el sistema pot trencar-se.

**Explicacio**: `latest` es un tag mutable. Avui apunta a la versio 2024.5, demà a la 2024.6, passat demà a la 2024.7 amb un canvi incompatible. Si el teu build o el teu `docker compose up` torna a fer pull, pot obtenir una versio totalment diferent. Amb tags explicits (com `2024.5.0`), tens REPRODUCIBILITAT: avui i d'aqui un any, el mateix tag dona la mateixa imatge.

---

## Pregunta 6: Eina de GitHub

**Resposta correcta**: Dependabot.

**Explicacio**: Dependabot es el servei de GitHub (gratis) que revisa els teus fitxers de dependències (requirements.txt, package.json, docker-compose.yml, etc.) i crea PRs automaticament quan hi ha noves versions. Es pot configurar la frequencia, els limits, i els ignorats. Alternativa externa: Renovate (molt mes configurable).

---

## Pregunta 7: Tecnica sense temps d'inactivitat

**Resposta correcta**: Blue-Green deployment.

**Explicacio**: Blue-green es la tecnica classica per fer deploys sense downtime. Tens dos entorns identics (blue i green), un es el "live" i l'altre es la nova versio. Quan la nova esta validada, canvies el balancejador o el router perque apunti al green. Si algo falla, tornes al blue. A la RPi, fer-ho be es complicat perque no tens molts recursos, pero per serveis petits es pot fer.

---

## Pregunta 8: Tipus d'actualitzacio sempre segura

**Resposta correcta**: PATCH.

**Explicacio**: PATCH son correccions (v1.0.0 -> v1.0.1) que per definicio NO trenquen compatibilitat. Soles corregeixen bugs i vulnerabilitats. SEMPRE s'han d'aplicar. MINOR (v1.0 -> v1.1) afegeix funcionalitat pero tambe pot fer canvis menors, i MAJOR (v1 -> v2) trencara coses. El risc va en ordre: PATCH < MINOR < MAJOR.

---

## Pregunta 9 (oberta): Estrategia d'actualitzacio

**Resposta model**:

La meva estrategia per al BernatLab combinaria automatitzacio i control manual segons la criticitat:

**AUTOMATITZAR (sense intervencio):**

1. **Actualitzacions de seguretat del sistema** amb `unattended-upgrades`. Son les MES importants perque tapen forats de seguretat. Es configuren nomes per a actualitzacions de seguretat (no pas per a totes les actualitzacions). Configuracio: `Automatic-Reboot "false"` perque no reinicii sol a les 3 de la matinada, i `Remove-Unused-Dependencies "true"` per netejar.

2. **Contenidors "stateless"** (sense dades importants) amb **Watchtower + label**. Serien: Grafana (te les dades a Prometheus, no local), Portainer, Uptime Kuma, Heimdall (dashboard), Homer. Si fallen, els torno a aixecar i tornen a funcionar. Watchtower s'executa a les 4:00 AM i nomes toca els que tenen label.

**MANUAL (amb supervisio):**

1. **Bases de dades** (InfluxDB, PostgreSQL). Mai amb Watchtower. Actualitzo quan he llegit el CHANGELOG, he fet backup, i soc en una finestra de manteniment. Les bases de dades son la pitjor cosa per actualitzar perque un canvi de format pot fer-te perdre dades.

2. **Home Assistant**. Es el cervell de la casa. Les actualitzacions poden trencar automatitzacions o integracions. Actualitzo un cop al mes, en cap de setmana, havent llegit el forum per si hi ha problemes coneguts. Mai a la versio beta.

3. **Prometheus i Loki**. Son la base de la monitoritzacio. Si fallen, perdo visibilitat. Actualitzo manualment quan hi ha una novetat important i he provat en un entorn local.

4. **Canvis de versio MAJOR** de qualsevol servei. Sempre amb backup previ, prova, i pla de rollback.

**Criteris de decisio:**

| Criteri | Automatic | Manual |
|---------|-----------|--------|
| Es de seguretat? | Si | - |
| Te dades importants? | No | Si |
| Es critic pel funcionament de la casa? | No | Si |
| Es un canvi MAJOR? | No | Si |
| He llegit el CHANGELOG? | - | Si |

La clau es **minimitzar la feina manual** que has de fer pero maximitzar el control. No vull haver d'estar cada setmana fent `apt upgrade`, pero tampoc vull que Watchtower em trenqui la base de dades a les 4 AM.

---

## Pregunta 10 (oberta): Actualitzar HA amb canvis incompatibles

**Resposta model**:

Per actualitzar Home Assistant de 2024.5 a 2025.1 (que te canvis incompatibles), el procediment pas a pas seria:

**Pas 1: Investigacio (1-2 dies abans)**
- Llegir el blog oficial de HA: https://www.home-assistant.io/blog/
- Mirar el CHANGELOG de cada versio entre 2024.5 i 2025.1 (pot haver-hi 5-6 versions).
- Buscar al forum de HA si hi ha problemes reportats.
- Identificar quines integracions o automatitzacions te afecten els canvis.

**Pas 2: Backup complet (1 hora abans)**
- Fer backup de la base de dades HA (el volum Docker `/config`).
- Fer backup de les automatitzacions personalitzades (`/config/.storage/`).
- Fer backup de la configuracio de HA (`/config/configuration.yaml`).
- Backup extern: pujar-ho a un altre lloc (un altre PC, cloud) per si la RPi es mor.
- Apuntar quina versio de HA tens actualment.

**Pas 3: Prova en entorn local (si es possible)**
- Si tens una RPi vella o pots fer servir Portainer amb un entorn separat, replica la configuracio.
- Actualitza a la versio nova aqui primer.
- Comprova que les automatitzacions funcionen.
- Identifica quines integracions fallen.
- Si tot va be, continua. Si no, espera a la 2025.2 o 2025.3.

**Pas 4: Preparar el rollback**
- Abans d'actualitzar, fes una copia de la imatge actual:
  ```bash
  docker tag homeassistant/home-assistant:2024.5 homeassistant/home-assistant:2024.5-backup
  ```
- Apunta l'ordre exacta per tornar a la versio anterior.

**Pas 5: Actualitzacio (en hora baixa, tipus diumenge al mati)**
- Atura els serveis que depenen d'HA (nodered, scripts personalitzats).
- Edita el docker-compose: `image: homeassistant/home-assistant:2025.1`
- `docker compose pull homeassistant`
- `docker compose up -d homeassistant`
- **Mantingues el terminal obert** durant 5-10 minuts per si cal fer rollback.

**Pas 6: Verificacio**
- Comprova que HA arranca: `docker logs -f homeassistant`
- Accedeix al dashboard web: ha d'apareixer la nova versio.
- Comprova les automatitzacions critiques:
  - Les llums s'encenen?
  - Les alarmes sonen?
  - Els sensors reporten dades?
  - Les integracions externes funcionen (Zigbee, MQTT, etc.)?
- Mira els logs per warnings/errors nous.

**Pas 7: Si algo falla, rollback**
- Si alguna cosa important no funciona:
  ```bash
  docker compose down homeassistant
  # Edita docker-compose per tornar a la versio antiga
  docker compose up -d homeassistant
  ```
- Investiga amb calma que ha fallat.
- Reporta el bug a la comunitat HA si cal.

**Pas 8: Documentar i netejar**
- Apunta al CHANGELOG del BernatLab que has actualitzat HA, amb data i possibles problemes trobats.
- Despres d'una setmana sense problemes, esborra la imatge backup: `docker rmi homeassistant/home-assistant:2024.5-backup`.

**Consideracions addicionals:**
- Avisa la familia/companys que hi haura una mica d'inactivitat.
- Tingues el movil a ma per si has de fer rollback rapid.
- Si tens un sistema d'alarmes, avisa tambe que potser no funciona durant 10-15 min.

---

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum i fer l'exercici practic.
- **3-4 encerts**: Refes l'exercici desde zero observant cada pas.
- **0-2 encerts**: Repassem junts el capitol abans de continuar.

## Que fer si has encertat totes

- Passa al **Capitol 8** (Manteniment programat).
- Investiga Diun (Docker Image Update Notifier) com a alternativa a Watchtower.
- Crea una politica de versions al teu repositori del BernatLab.
