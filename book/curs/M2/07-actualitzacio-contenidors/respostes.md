# Respostes - Capitol 7: Actualitzacio de contenidors

> Mira les respostes DESPRES d'haver fet el qüestionari.

## Pregunta 1: Que fa Watchtower?

**Resposta correcta**: Mira si hi ha noves versions de les imatges i actualitza els contenidors automaticament.

**Explicacio**: Watchtower es un contenidor que es connecta al socket de Docker, mira quines imatges tenen una versio nova a Docker Hub, i si en troba, atura el contenidor antic i n'arrenca un amb la imatge nova. Tot automatic.

---

## Pregunta 2: Diferencia entre update i upgrade?

**Resposta correcta**: Update es el proces; upgrade es el resultat concret d'una nova versio.

**Explicacio**: En l'informatica, "update" pot significar qualsevol canvi (un parche, una nova funcionalitat, un security fix). "Upgrade" es mes especific: passar a una nova versio major. Per exemple, de Nextcloud 27 a 28 es un upgrade; un parche de seguretat 27.1.5 es un update.

---

## Pregunta 3: Blue-green?

**Resposta correcta**: Mantenir dues versions corrent i canviar el tràfic nomes quan la nova funciona.

**Explicacio**: Es una tecnica per fer actualitzacions sense temps d'inactivitat. Tens la versio "blue" corrent (usuaris l'usen). Muntes la versio "green" en paral·lel, la proves, i quan funciona, canvies el balancer per enviar el tràfic a "green". Si falla, pots tornar rapidament a "blue".

---

## Pregunta 4: Que es rolling update?

**Resposta correcta**: Actualitzar un servei de mica en mica, substituint instances gradualment.

**Explicacio**: Si tens 5 instancies d'un servei, en lloc d'aturar-les totes alhora, les vas substituint una a una: atura la 1, arranca la nova, espera que estigui llesta, atura la 2, etc. Aixi sempre hi ha capacitat de servei.

---

## Pregunta 5: Per que labels?

**Resposta correcta**: Perque Watchtower nomes actualitzi els contenidors que tu vols, no tots.

**Explicacio**: Sense label, Watchtower actualitzaria tots els teus contenidors automaticament. Amb `com.bernatlab.enable=true` (o qualsevol altre), tu controles quins volem que s'actualitzin automaticament i quins prefereixes actualitzar manualment (per exemple, una base de dades on les actualitzacions poden ser delicades).

---

## Pregunta 6: Interval de Watchtower?

**Resposta correcta**: `WATCHTOWER_POLL_INTERVAL=86400` (un cop al dia).

**Explicacio**: Per defecte, Watchtower comprova cada 5 minuts. Pero si nomes vols comprovar un cop al dia, pots posar `--schedule "0 0 4 * * *"` (cron) o posar un interval llarg. Un cop al dia es un bon equilibri per a un homelab.

---

## Pregunta 7: Que es un healthcheck?

**Resposta correcta**: Una comanda que Docker executa per saber si el servei esta funcionant be.

**Explicacio**: Un healthcheck es una definicio al servei que diu "executa aquesta comanda cada X segons. Si retorna 0, el servei esta healthy; si no, esta unhealthy". Docker pot reiniciar el contenidor si esta unhealthy massa estona. Es la base del autohealing.

---

## Pregunta 8: Que es zero-downtime?

**Resposta correcta**: Actualitzar sense que els usuaris notin cap tall del servei.

**Explicacio**: Es l'objectiu de qualsevol actualitzacio ben feta. Combinant rolling updates, healthchecks i un balancer, pots actualitzar serveis sense que ningú noti res. Els usuaris sempre veuen una versio que funciona.

---

## Pregunta 9 (oberta): Manual vs automatic

**Resposta model**:

Hi ha avantatges clars per a cada enfocament:

**Arguments a favor de les actualitzacions manuals:**

1. **Control total**: tu decideixes QUAN s'actualitza. Si una versio nova te un bug, pots retardar l'actualitzacio fins que estigui resolt. Amb Watchtower automatic, el bug ja esta en produccio.

2. **Test previ**: abans d'actualitzar, pots fer proves. Per exemple, abans d'actualitzar Nextcloud a una nova versio major, llegeixes les notes de la versio, mires si hi ha canvis incompatibles amb els teus plugins, i si tot esta be, actualitzes.

3. **Coordinacio amb backups**: abans d'actualitzar, sempre vols fer un backup. Amb Watchtower automatic, no tens la oportunitat de fer un backup abans.

4. **Evitar actualitzacions no desitjades**: de vegades Docker Hub corregeix un tag (canvien el que apunten). Si tens `nginx:latest` i Watchtower comprova a les 3 de la matinada, pot actualitzar-te a una versio que no vols. Amb manual, pots triar.

5. **Aprenentatge**: fer actualitzacions manuals t'ensenya com funciona el sistema. Si nomes tens Watchtower, quan falla no saps on mirar.

**Arguments a favor de les actualitzacions automatiques (Watchtower):**

1. **Confort**: no t'has de recordar d'actualitzar. Watchtower ho fa per tu. En un homelab amb 10-20 serveis, dedicar una hora a actualitzar nomes es un mal de cap.

2. **Seguretat immediata**: quan hi ha un CVE critic a una llibreria, vols actualitzar **avui**, no d'aqui dues setmanes quan et recordis. Watchtower t'ho aplica automaticament.

3. **Menos feina per a serveis menors**: per a un container d'una eina petita (un exporter de metricques, una eina d'analisi), no val la pena dedicar-hi temps. Que Watchtower ho actualitzi.

4. **Consistencia**: tots els teus serveis estan en versions recents. No tens una base de dades amb 3 anys d'antiguitat per descuit.

**La meva recomanacio al BernatLab**: **mixt**. Faig servir Watchtower nomes per a serveis "menors" (expositors de metricques, eines d'analisi, eines de dev). Per a serveis critics (Nextcloud, base de dades, eina de backups), faig actualitzacio manual. Pero cada 3-6 mesos, faig una "sessio d'actualitzacio" on reviso tot manualment.

A mes, SEMPRE tinc Watchtower amb label activat. No vull que m'actualitzi la base de dades de produccio a les 3 de la matinada.

---

## Pregunta 10 (oberta): Actualitzar un Nextcloud

**Resposta model**:

Pas a pas, actualitzaria el Nextcloud del BernatLab de la versio 27 a la 28 amb Watchtower activat pero el servei protegit:

**1. Backup previ (obligatori!)**

Abans de qualsevol actualitzacio, backup complet:
```bash
# Backup de la base de dades
docker exec nextcloud-db pg_dump -U blog blogdb > /backup/blogdb-$(date +%F).sql

# Backup del volum
docker run --rm \
  -v nextcloud-data:/origen:ro \
  -v /backup:/desti \
  alpine tar czf /desti/nextcloud-data-$(date +%F).tar.gz -C /origen .
```

**2. Comprovar compatibilitat**

Llegeixo les release notes de Nextcloud 28. Hi ha algun canvi incompatible amb els meus plugins? Si uso Nextcloud Office, cal una versio especifica. Si uso Talk, idem. Comprovo la matriu de compatibilitat.

**3. Desactivar Watchtower per a aquest servei temporalment**

Al compose del Nextcloud, trec el label `com.bernatlab.enable=true` per evitar que Watchtower l'actualitzi a mitges. O simplement aturo Watchtower durant l'actualitzacio:
```bash
docker compose stop watchtower
```

**4. Actualitzar manualment**

```bash
# Edito el compose: canvio la versio
sed -i 's|nextcloud:27|nextcloud:28|g' docker-compose.yml

# Tiro la nova imatge
docker compose pull nextcloud

# Aturo el servei
docker compose stop nextcloud

# Aplicar l'upgrade de la base de dades (Nextcloud cal executar un script)
docker compose run --rm nextcloud php occ upgrade

# Torno a arrencar
docker compose up -d nextcloud

# Comprovar logs
docker compose logs -f nextcloud
```

**5. Verificar**

- Accedeixo a la UI web de Nextcloud.
- Comprovo que totes les apps segueixen funcionant.
- Faig una pujada i una baixada d'un fitxer de prova.
- Miro els logs: `docker compose logs nextcloud --tail 100`.

**6. Si falla, tornar enrera**

Si algo va malament (un plugin deixa de funcionar, error de base de dades):
```bash
# Aturar el servei
docker compose down

# Restaurar el backup de la base de dades
docker exec -i nextcloud-db psql -U blog blogdb < /backup/blogdb-2024-01-15.sql

# Restaurar el volum
docker run --rm \
  -v nextcloud-data:/desti \
  -v /backup:/backup \
  alpine sh -c "rm -rf /desti/* && tar xzf /backup/nextcloud-data-2024-01-15.tar.gz -C /desti"

# Tornar a la versio anterior
sed -i 's|nextcloud:28|nextcloud:27|g' docker-compose.yml
docker compose up -d
```

**7. Reactivar Watchtower (opcional)**

Si tot ha anat be, torno a posar el label per a futures actualitzacions menors.

Aquest proces es pot trigar 30-60 minuts pero es la manera **correcta** d'actualitzar un servei critic. Watchtower nomes es per a serveis on puc assumir risc.

---

## Pregunta 11 (oberta): Per que les actualitzacions tenen mala fama

**Resposta model**:

Les actualitzacions automatitzades tenen mala fama entre administradors per una combinacio d'experiencies reals i mites:

**Experiencies reals (legitimes)**:

1. **L'actualitzacio de les 3 de la matinada**: el 2014, una actualitzacio de GLibc a Linux va trencar milers de servidors quan els processos antics es reiniciaven. Watchtower automatic podria haver causat una caiguda global.

2. **Incompatibilitat entre versions**: actualitzar Nextcloud pot requerir tambe actualitzar el schema de la base de dades. Si Watchtower actualitza Nextcloud pero la DB no esta preparada, el sistema queda inconsistent.

3. **Pèrdua de configuracio**: algunes imatges sobrescriuen configuracio a `/config` o `/etc/app/` durant l'actualitzacio. Un reinici automatic pot perdre hores de configuracio manual.

4. **Plugins incompatibles**: Nextcloud te plugins de tercers. Una actualitzacio pot trencar la compatibilitat amb els teus plugins.

**Mites (menys justificats)**:

1. "Les actualitzacions sempre trencen coses": en realitat, la majoria son transparents. Les que trencen son minoria pero son molt visibles.

2. "Millor no tocar res": deixar un sistema sense actualitzar es la **garantia** de tenir problemes. La questio no es si, sino quan.

3. "Les actualitzacions automatiques son insegures": el risc real es baix comparat amb el risc de no actualitzar.

**Aplica al BernatLab**:

Watchtower al BernatLab esta en un entorn **controlat** (la teva propia xarxa, els teus serveis). Si una actualitzacio falla, l'impacte es limitat. Per tant, els riscos son mes petits que en produccio.

**Recomanacio**: configura Watchtower amb:
- `WATCHTOWER_NOTIFICATIONS=true` (t'avisa per email/Telegram).
- `WATCHTOWER_CLEANUP=true` (neteja imatges antigues).
- Labels per activar Watchtower nomes en serveis de baix risc.
- Un interval de 24h (no 5 min).

Aixi tens el millor dels dos mons: actualitzacions regulars pero amb temps per reaccionar.

---

## Pregunta 12 (oberta): Frequencia d'actualitzacio i finestra de risc

**Resposta model**:

La **finestra de risc** es el temps entre que es publica una vulnerabilitat i el moment que el teu sistema la te corregida. Com mes llarga es la finestra, mes probable es que algú t'ataqui.

**Calcul mental**:

Si vols dir "estic segur perquè actualitzo cada setmana", la teva finestra de risc es de 7 dies. Pero el temps entre que es publica una vulnerabilitat i l'exploit public es cada vegada mes curt:
- 2010: mesos.
- 2015: setmanes.
- 2020: dies.
- 2024: hores (vulnerabilitats 0-day son explotades el mateix dia).

Per tant, una finestra de 7 dies es **insuficient** per a serveis exposats a internet. Caldria actualitzar en hores.

**Cas del BernatLab (100.115.134.76)**:

Si tens serveis exposats:
- Watchtower amb interval de 24h: finestra maxima de 24h. Acceptable.
- Watchtower amb interval d'1h: finestra maxima d'1h. Pero mes carrega de xarxa.
- Manual: finestra variable, pot ser setmanes. Perillos.

Si tens serveis nomes a la xarxa local:
- Fins i tot 7 dies es acceptable perque l'atacant necessita acces a la xarxa local.

**Cas especial: actualitzacions de kernel o sistema base**:
Aquestes NO les gestiona Watchtower. Son actualitzacions del sistema operatiu de la RPi, que cal fer manualment amb `apt upgrade`. Cal planificar una finestra de manteniment mensual o trimestral.

**Recomanacio al BernatLab**:

- Watchtower diari per a serveis exposats.
- Watchtower setmanal per a serveis interns.
- `unattended-upgrades` al sistema base per pegats de seguretat automatics.
- Auditoria manual mensual de les actualitzacions majors.

**Equilibri**: una finestra de 24h es bona. Mes curta comença a ser excessiva (massa actualitzacions, possibles falles). Mes llarga es perillosa.

---

## Pregunta 13 (oberta): Estrategia mixta d'actualitzacio

**Resposta model**:

El company que diu "Watchtower es perillos, jo actualitzo manualment" assumeix un cost operatiu mes alt del que sembla. Arguments i alternativa:

**Cost amagat del manual**:

1. **Memoria humana**: actualitzar "quan me'n recordo" vol dir mai. El cervell prioritza coses urgents; les actualitzacions preventives sempre queden al final.

2. **Temps de context**: cada vegada que actualitzes, has de recordar quins serveis tens, quines versions, quins canvis hi ha hagut. Es un overhead mental.

3. **Inconsistencia**: pots oblidar serveis. Si tens 20 serveis i nomes n'actualitzes 18, els 2 restants son punts febles.

4. **Ventana de risc oberta**: mentre recordes actualitzar, la vulnerabilitat pot ser explotada.

**Estrategia mixta proposada**:

1. **Watchtower nomes per actualitzacions de seguretat**:
   - `WATCHTOWER_LABEL_ENABLE=true` nomes serveis marcats.
   - Marcar nomes serveis on les actualitzacions son segures (nginx, postgres).
   - NO marcar serveis amb estat (bases de dades, sistemes amb volums).

2. **Notifications (no updates) per a serveis critics**:
   - Usar `Diun` (Docker Image Update Notifier) que nomes t'avisa.
   - Tu decideixes quan i com actualitzar.

3. **Actualitzacions majors manuals**:
   - Nextcloud 27 -> 28: manual, amb backup previ, finestres de manteniment.
   - Un cop al mes o quan hi ha un canvi important.

4. **Calendari recordatori**:
   - Un recordatori al calendari: "revisar actualitzacions manuals".
   - El primer diumenge de cada mes, 1 hora.

**Exemple practic al BernatLab**:

```yaml
# Serveis que Watchtower pot actualitzar automatic:
- nginx (web, recovery rapid)
- portainer (UI, no te estat)
- uptime-kuma (no te estat)
- dozzle (logs, no te estat)

# Serveis que actualitzo manualment:
- nextcloud (amb backup previ)
- postgres (verificar migrations)
- mariadb (verificar versions)
- influxdb (verificar compatibilitat amb Grafana)
- ollama (pot trencar embeddings)
```

Aixi automatitzes el 60% (lo facil) i controles el 40% (lo critic). Es el millor dels dos mons.

---

## Pregunta 14 (oberta): Politica d'actualitzacio per a Hort Osona

**Resposta model**:

Per a l'stack d'Hort Osona amb Ollama, ChromaDB i Open WebUI, la politica d'actualitzacio seria:

**Ollama**:
- **Politica**: mixta.
- **Justificacio**: Ollama actualitza sovint amb nous models i optimitzacions. Pero actualitzar pot canviar la compatibilitat amb els embeddings existents. Si actualitzes Ollama pero el model d'embeddings nomes el tens en una versio antiga, la base de coneixement queda inconsistent.
- **Practica**: actualitza manualment cada 2-3 mesos. Abans, comprova que el model d'embeddings (per exemple `nomic-embed-text`) esta en la versio esperada. Si canvies Ollama i el model, has de reindexar ChromaDB (30 min).
- **Watchtower**: NO.

**ChromaDB**:
- **Politica**: manual.
- **Justificacio**: ChromaDB te versions breaking changes. Actualitzar pot requerir reindexar tota la base de coneixement. A mes, ChromaDB es l'emmagatzematge de les dades; actualitzar automatic es arriscat.
- **Practica**: actualitza nomes quan hi ha un feature que necessites o una vulnerabilitat critica. Cada 6-12 mesos.
- **Watchtower**: NO.
- **Backup**: obligatori abans de qualsevol actualitzacio (es pot exportar la DB).

**Open WebUI**:
- **Politica**: automatica amb Watchtower.
- **Justificacio**: es una aplicacio web front-end. Les actualitzacions son majorment compatibles. Watchtower pot gestionar-ho be.
- **Practica**: Watchtower amb label, interval 24h.
- **Watchtower**: SI.

**Resum de la politica**:
- Ollama: manual cada 2-3 mesos, amb reindexacio preventiva.
- ChromaDB: manual cada 6-12 mesos, amb backup.
- Open WebUI: automatic via Watchtower.

**Avantatge**: el que te Watchtower, s'actualitza. El que es critic, el controles. La teva atencio va a les coses que importen.

---

## Pregunta 15 (oberta): Finestres de manteniment i disponibilitat

**Resposta model**:

Al BernatLab, fins i tot si ets lunic usuari, les finestres de manteniment son importants per minimitzar la interrupcio. Consideracions:

**Quan fer manteniment**:

1. **Hora de baixa activitat**: si uses els serveis intensivament durant el dia, la matinada es ideal.
2. **Dia de baixa activitat personal**: caps de setmana, festius.
3. **Sense deadlines propers**: no fer actualitzacio el dia abans d'un treball important que usara els serveis.

**Exemple al BernatLab**:
- "Diumenges a les 4 de la matinada" es la finestra tipica.
- Pero: a les 4 dorms. Si algo falla, te n'adones al mati.
- Alternativa: diumenges a les 10 del mati, quan estas despert i pots revisar.

**Eines per planificar**:

1. **Uptime Kuma amb finestres de manteniment**: configura finestres on les caigudes no generen alertes.
2. **Watchtower amb schedule**: pots configurar a quina hora fa els checks (no nomes cada 24h, sino a les 03:00 cada nit).
3. **Scripts amb "dry-run"**: alguns scripts de backup poden fer un simulacre abans de fer res.

**Pla de rollback**:

Sempre que facis una actualitzacio important, tingues un pla per tornar enrera:

1. **Backup abans** (sempre).
2. **Coneix la versio anterior** (no vagis a la ultima de cop).
3. **Documenta l'ordre per revertir** (tots la podem executar en 5 min).
4. **Practica el rollback** almenys un cop abans que calgui fer-lo realment.

**Exemple**:

```bash
# Abans d'actualitzar:
docker compose pull
docker exec nextcloud-db pg_dump -U user nextcloud > backup_pre_upgrade.sql

# Actualitzar:
docker compose up -d

# Si falla, tornar enrera:
docker compose down
# Restaurar imatges antigues
docker tag nextcloud:28 nextcloud:28-broken
docker pull nextcloud:27
docker compose up -d
# Restaurar DB si cal
psql -U user nextcloud < backup_pre_upgrade.sql
```

**Disponibilitat vs seguretat**:

Al BernatLab, el risc de tenir una caiguda de 30 min un diumenge al mati es **menys greu** que el risc de tenir una vulnerabilitat sense pegat durant setmanes. Per tant, val la pena actualitzar sovint, encara que sigui molest.

---

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum. Watchtower es la clau.
- **3-4 encerts**: Refes l'exercici i llegeix sobre healthchecks.
- **0-2 encerts**: Repassem. Es un capitol practic.

## Que fer si has encertat totes

- Passa al **Capitol 8** (backup).
- Configura Watchtower amb notificacions a Telegram o Discord.
- Investiga el `Diun` (Docker Image Update Notifier) per notificacions alternatives.
