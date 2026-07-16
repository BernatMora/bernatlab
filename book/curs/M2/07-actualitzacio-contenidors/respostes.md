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

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum. Watchtower es la clau.
- **3-4 encerts**: Refes l'exercici i llegeix sobre healthchecks.
- **0-2 encerts**: Repassem. Es un capitol practic.

## Que fer si has encertat totes

- Passa al **Capitol 8** (backup).
- Configura Watchtower amb notificacions a Telegram o Discord.
- Investiga el `Diun` (Docker Image Update Notifier) per notificacions alternatives.
