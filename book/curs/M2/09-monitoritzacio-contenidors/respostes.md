# Respostes - Capitol 9: Monitoritzacio de contenidors

> Mira les respostes DESPRES d'haver fet el qüestionari.

## Pregunta 1: docker stats?

**Resposta correcta**: Estadistiques en temps real de CPU, RAM, xarxa i disc per contenidor.

**Explicacio**: `docker stats` es la comanda Docker que mostra una taula en temps real (s'actualitza cada segon per defecte) amb les principals metricques de cada contenidor. Es la primera eina que has d'aprendre.

---

## Pregunta 2: Logs?

**Resposta correcta**: `docker logs`.

**Explicacio**: `docker logs <contenidor>` mostra els logs (stdout/stderr) capturats del contenidor. Amb `-f` segueixes en temps real. Amb `--tail N` veus les ultimes N linies. Molt basic pero indispensable.

---

## Pregunta 3: cAdvisor?

**Resposta correcta**: Una eina de Google que mostra metricques visuals dels contenidors.

**Explicacio**: cAdvisor ve de "Container Advisor". Te una UI web que mostra CPU, RAM, xarxa i disc per contenidor en temps real. Es perfecte per a un homelab perque es molt simple. No guarda historic.

---

## Pregunta 4: Combinacio estandard?

**Resposta correcta**: Prometheus + Grafana.

**Explicacio**: Prometheus recull i emmagatzema metricques al llarg del temps. Grafana les visualitza en dashboards. Es la combinacio estandard a la industria (Netflix, Uber, etc. l'usen). Hi ha alternatives (InfluxDB + Telegraf + Grafana, Datadog, etc.) pero aquesta es la mes popular.

---

## Pregunta 5: Dozzle?

**Resposta correcta**: Una eina web que mostra els logs de tots els contenidors en temps real.

**Explicacio**: Dozzle es una eina molt lleugera (10-20 MB) que es connecta al socket de Docker i mostra els logs de tots els teus contenidors en una UI web, amb cerca i filtres. Es perfecta per a un homelab.

---

## Pregunta 6: Healthcheck?

**Resposta correcta**: Determinar si un servei esta funcionant correctament dins el contenidor.

**Explicacio**: Un healthcheck es una comanda que Docker executa periodicament. Si retorna 0, el servei esta "healthy"; si no, esta "unhealthy" i Docker pot reiniciar-lo. Es la base de l'autohealing.

---

## Pregunta 7: Uptime?

**Resposta correcta**: Uptime Kuma.

**Explicacio**: Uptime Kuma es una eina self-hosted que comprova periodicament si els teus serveis responen (HTTP, TCP, ping, etc.) i mostra un taulell d'estat molt maco. Es perfecta per a un homelab i es mantinguda activament per la comunitat.

---

## Pregunta 8: Perill dels logs?

**Resposta correcta**: Que els logs poden omplir el disc.

**Explicacio**: Sense limit de mida, un contenidor pot escriure gigabytes de logs al dia i acabar omplint el disc. Es important posar `max-size` i `max-file` al driver de logs. O usar eines centralitzades que netegin automaticament.

---

## Pregunta 9 (oberta): Recursos vs aplicacio

**Resposta model**:

Son dos tipus de monitoritzacio ben diferents que cal combinar:

**Monitoritzar els recursos** (CPU, RAM, xarxa, disc) es mirar la **salut del sistema**. Es com posar un termometre a un malalt: ens diu la temperatura, la pressio, el pols. Pero no ens diu si esta content o trist. A un homelab amb Docker, aixo son les metricques que ens avisa si un contenidor consumeix massa, si el disc esta ple, si la CPU esta al 100% (coll d'ampolla). Son essentials per evitar problemes **operatius**.

**Monitoritzar l'aplicacio** (latencia, errors, peticions, usuaris actius) es mirar **que esta fent per als usuaris**. Es com preguntar al malalt "com et trobes?". Sabem si la web carrega rapid, si hi ha errors 500, si els usuaris reben les respostes correctes. Son essentials per a la **qualitat del servei**.

**Per que calen les dues coses**:

Un exemple practic al BernatLab: tinc el Nextcloud. Un dia, `docker stats` mostra:
- CPU: 1% (tot normal)
- RAM: 200 MB (perfecte)
- Xarxa: 50 KB/s (tot be)

Tot sembla correcte! Pero si nomes mires l'aplicacio, veus:
- Temps de resposta: 5 segons (hauria de ser 200 ms)
- Errors 500: 20% de les peticions
- Usuaris actius: 0 (han marxat tots)

Que ha passat? Doncs potser la base de dades esta fent un lock i no respon, pero el Nextcloud en si no consumeix mes recursos. O potser el disc SSD esta a punt de fallar i les lectures son lentes. O potser hi ha un bug al codi que nomes es manifesta en certes condicions.

Si nomes mires els recursos, no saps res. Si nomes mires l'aplicacio, saps que algo va malament pero no per que. Combinant les dues coses, pots correlacionar: "ah, la latencia puja quan la latencia del disc puja" -> el problema es el disc.

Un altre exemple: un contenidor pot estar **molt actiu** (CPU 50%, RAM 80%) pero **funcionar perfectament** (latencia 100 ms, 0 errors). Son les dades importants del que s'ha de processar. Si nomes mires recursos, et penses que hi ha un problema.

Aixo es la diferencia entre **"estic funcionant"** (recursos OK) i **"estic treballant be"** (aplicacio OK). Un sistema sa es ambdues coses.

---

## Pregunta 10 (oberta): docker-compose per a monitoritzacio

**Resposta model**:

Aqui tens el `docker-compose.yml` per a una pila de monitoritzacio completa al BernatLab:

```yaml
version: "3.8"

services:
  # Prometheus: base de dades de metricques
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--storage.tsdb.retention.time=30d'  # guarda 30 dies
      - '--web.console.libraries=/usr/share/prometheus/console_libraries'
    restart: unless-stopped

  # Grafana: visualitzacio
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=bernatlab
      - GF_USERS_ALLOW_SIGN_UP=false
    volumes:
      - grafana-data:/var/lib/grafana
      - ./grafana/provisioning:/etc/grafana/provisioning
    depends_on:
      - prometheus
    restart: unless-stopped

  # cAdvisor: metricques dels contenidors
  cadvisor:
    image: gcr.io/cadvisor/cadvisor:latest
    ports:
      - "8080:8080"
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:ro
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
    privileged: true
    restart: unless-stopped

  # Node Exporter: metricques de l'amfitrio (CPU, RAM, temperatura)
  node-exporter:
    image: prom/node-exporter:latest
    ports:
      - "9100:9100"
    command:
      - '--path.rootfs=/host'
      - '--collector.filesystem.mount-points-exclude=^/(sys|proc|dev|host|etc)($$|/)'
    volumes:
      - /:/host:ro,rslave
    restart: unless-stopped

  # Dozzle: UI web per als logs
  dozzle:
    image: amir20/dozzle:latest
    ports:
      - "9999:8080"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
    restart: unless-stopped

  # Uptime Kuma: monitor d'estat dels serveis
  uptime-kuma:
    image: louislam/uptime-kuma:latest
    ports:
      - "3001:3001"
    volumes:
      - uptime-kuma-data:/app/data
    restart: unless-stopped

  # (Opcional) Loki + Promtail per a logs centralitzats
  loki:
    image: grafana/loki:latest
    ports:
      - "3100:3100"
    volumes:
      - ./loki-config.yaml:/etc/loki/local-config.yaml
    restart: unless-stopped

  promtail:
    image: grafana/promtail:latest
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - /var/lib/docker/containers:/var/lib/docker/containers:ro
      - ./promtail-config.yaml:/etc/promtail/config.yml
    restart: unless-stopped

volumes:
  prometheus-data:
  grafana-data:
  uptime-kuma-data:
```

I el `prometheus.yml`:

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'cadvisor'
    static_configs:
      - targets: ['cadvisor:8080']

  - job_name: 'node'
    static_configs:
      - targets: ['node-exporter:9100']
```

**Explicacio dels serveis**:

- **Prometheus**: el cor. Guarda les metricques al llarg del temps. Porta una UI web a port 9090.
- **Grafana**: visualitzacio. Connectes Grafana a Prometheus com a data source, i crees dashboards. Port 3000.
- **cAdvisor**: metricques dels contenidors Docker. Port 8080.
- **node-exporter**: metricques de l'amfitrio (CPU, RAM, temperatura, xarxa). Port 9100. Important per veure la temperatura de la RPi!
- **Dozzle**: logs web. Port 9999. No requereix config.
- **Uptime Kuma**: monitor d'estat. Port 3001. Configures les URLs dels teus serveis i tens un taulell d'estat.
- **Loki + Promtail (opcional)**: si vols logs centralitzats (cerca a tots els contenidors des de Grafana).

**Quins serveis afegiria a mes**:

- **Alertmanager**: per a alarmes automatic. Si la CPU passa del 90% durant 5 min, envia'm un missatge a Telegram.
- **Postgres exporter**: si tens una base de dades, vols veure conexions, queries lentes, etc.
- **Nextcloud exporter**: si tens Nextcloud, hi ha un exporter oficial que mostra usuaris, fitxers, etc.
- **Watchtower + Diun**: per actualitzacions automatic.

**Aquesta pila consumeix a la RPi**:
- Prometheus: ~150 MB RAM, 1-2 GB de disc per 30 dies
- Grafana: ~100 MB RAM
- cAdvisor: ~50 MB RAM
- node-exporter: ~20 MB RAM
- Dozzle: ~30 MB RAM
- Uptime Kuma: ~150 MB RAM

Total: ~500 MB RAM, 2-3 GB de disc. Perfecte per a la RPi 4 de 4 GB (et queda ~1.5 GB per a la resta de serveis).

Aquesta es la meva pila actual al BernatLab. Es la referencia.

---

## Pregunta 11 (oberta): Per que la monitoritzacio es menyspreada

**Resposta model**:

La monitoritzacio es sovint menyspreada pels usuaris particulars per una combinacio de factors:

**1. "Si funciona, per què mirar?"**:
Es la mentalitat mes perillosa. Un servei pot estar caigut durant dies sense que ningú se n'adoni. Hi ha fallades silencioses: la base de dades no escriu pero el servei sembla funcionar (les lectures funcionen, les escriptures fallen). L'usuari nomes nota el problema quan busca una dada que no hi es.

**2. La monitoritzacio no te un benefici immediat**:
Com el backup, la monitoritzacio es una inversio per al futur. Configurar Prometheus + Grafana porta 4-6 hores. Els beneficis es veuen mes endavant, quan algu t'avisa abans que tu t'adonis.

**3. La complexitat percebuda**:
Prometheus + Grafana + node-exporter + cAdvisor + Dozzle + Uptime Kuma son 6 serveis. Per a un homelab amb 5 serveis propis, es molt overhead. Es la mateixa proporcio que posar 6 vigilants per vigilar 5 cases.

**4. "Si soc lunic usuari, qui pateix?"**:
Fins i tot sent lunic usuari, pateixes tu. Una caiguda de 6 hores d'un Nextcloud es temps on no pots accedir als teus documents. Si estas treballant i necessites un fitxer, es un problema.

**5. "Ja mirarem `docker ps` un cop al dia"**:
Aixo es com tenir un cotxe i mirar la pressio dels neumàtics un cop al dia. Serveix per a algunes coses pero no per a incidents que pasen en minuts.

**Cas concret al BernatLab (100.x.y.z)**:

Si tens serveis exposats a internet i un atacant intenta entrar:
- Sense monitoritzacio: pot estar dies intentant fins que ho aconsegueix.
- Amb monitoritzacio: reps una alerta d'activitat sospitosa (CPU alta, connexions anormals) i pots actuar.

Si la teva RPi te un problema de temperatura:
- Sense monitoritzacio: la CPU fa throttling i tot va lent, pero no saps per que.
- Amb monitoritzacio: veus la temperatura pujant i pots netejar la caixa.

**Solucio realista**:

Per a un homelab amb temps limitat:
- Comença amb Uptime Kuma (la mes simple). Nomes comprova que els serveis responen.
- Afegeix Grafana + Prometheus quan tinguis temps.
- Configura alertes critiques nomes (disc ple, servei caigut), no totes les possibles.

**Filosofia**: la monitoritzacio es com la assegurança de la casa. No la necessites mai... fins que la necessites. I aleshores, val cada euro que hi has posat.

---

## Pregunta 12 (oberta): Logs, velocitat i cost

**Resposta model**:

Els logs son essencials per entendre que passa, pero tenen un cost que cal gestionar:

**Problema del creixement**:

Els logs creixen de forma constant. Un Nextcloud amb 10 usuaris pot generar 100 MB de logs al dia. Un servidor web amb molt trafic pot generar 1 GB/hora. Sense gestio, el disc s'omple.

**Disc ple = servei que falla**:

Quan el disc esta al 100%:
- El sistema operatiu no pot escriure logs nous.
- Les aplicacions fallen (no poden escriure fitxers temporals).
- La base de dades pot perdre dades o corrupte's.
- El sistema pot entrar en un estat inconsistent que nomes es recupera amb un reinici.

**Solucions per gestionar logs**:

**1. Logrotate**:
Eina classica de Linux. Configures quants dies/volum maxim保留. Per exemple: comprimir logs de mes de 7 dies, esborrar de mes de 30.
- Avantatge: simple, robust, integrat al sistema.
- Desavantatge: nomes funciona per fitxers, no per flux de logs.

**2. Limits per contenidor (Docker)**:
- `--log-opt max-size=10m` i `--log-opt max-file=3` al `docker run`.
- Docker trunca i rota automatic.
- Avantatge: simple, funciona per contenidor.
- Desavantatge: no comprimeix, no centralitza.

**3. Sistema centralitzat (Loki, ELK)**:
- Loki (de Grafana Labs): indexa logs i permet cerques rapides.
- Elasticsearch + Kibana: el estandard de la industria pero pesat.
- Avantatge: busqueda potent, alertes basades en contingut.
- Desavantatge: servei adicional que tambe cal mantenir.

**Politica practica al BernatLab**:

```yaml
# A cada servei al docker-compose:
logging:
  driver: json-file
  options:
    max-size: "10m"
    max-file: "3"
```

Aixo limita cada contenidor a 30 MB de logs (10 MB x 3 fitxers). Suficient per a la majoria de casos.

**Politica de retencio**:

- **En calent**: 7 dies de logs. Rotacio automatica.
- **Comprimits**: 30 dies. Els logs antics es comprimeixen (gzip).
- **Al núvol**: opcional. Si tens una solucio com Loki, pots tenir mes historia.

**Cas especial: logs de seguretat**:

Els logs de authenticacio, intents d'intrusio, etc. s'han de retenir mes (90 dies minim, 1 any per compliance). Aixo justifica un sistema centralitzat.

**Alerta important**: configura una alerta de "disc > 85%" per evitar sorpreses. La majoria de monitors fallen per disc ple, no per altres raons.

---

## Pregunta 13 (oberta): Per que `docker ps` un cop al dia es insuficient

**Resposta model**:

L'estrategia de mirar `docker ps` un cop al dia te multiples fallades:

**1. La finestra de deteccio es llarga**:

Un cop al dia vol dir que un servei pot estar caigut 24 hores abans que te n'adonis. Si la caiguda es a les 17:00 i mires a les 8:00 del mati següent, son 15 hores. Multiplica per un negoci: son 15 hores de perdua de productivitat.

**2. La memoria humana juga males passades**:

Quan mires `docker ps`, veus una llista. Pero el teu cervell nomes detecta canvis evidents ("un contenidor no hi es"). Si un contenidor esta corrent pero el servei intern no respon (per exemple, nginx esta corrent pero PHP-FPM ha mort), no ho veus.

**3. Les fallades silencioses son les mes perilloses**:

Hi ha fallades que no apareixen a `docker ps`:
- La base de dades no accepta connexions pero el proces esta corrent.
- Un worker esta penjat pero el contenidor es considera "healthy".
- Un servei respon pero retorna 500 sempre.
- La memoria esta al 99% i tot va lent.

`docker ps` nomes et diu "el contenidor esta corrent". No et diu res sobre la salut interna.

**4. L'efecte "novetat"**:

Els primers dies mires `docker ps` cada hora. Al cap d'una setmana, un cop al dia. Al cap d'un mes, un cop per setmana. Al cap d'un any, t'has oblidat. La monitoritzacio automatica no pateix aquest efecte.

**5. Impacte al BernatLab**:

Si tens un Nextcloud amb els teus documents i la teva musica, una caiguda de 6 hores et pot costar:
- No poder accedir a un document urgent.
- Perdre la oportunitat de pujar una foto a temps.
- No poder recordar on es un PDF que nomes tens alli.

Si ho compares amb el cost de configurar Uptime Kuma (1-2 hores), el ROI es evident.

**Alternativa progressiva**:

Si encara no tens temps per una pila completa de monitoritzacio:
1. Comença amb Uptime Kuma nomes. Configura 5-10 serveis. 1 hora.
2. Configura alertes per Telegram. 30 min.
3. Afegeix Prometheus + Grafana mes endavant quan vegis el valor.

Aixi la barrera d'entrada es baixa i pots veure resultats immediats.

---

## Pregunta 14 (oberta): Metriques i alertes per al stack de dades

**Resposta model**:

Per a l'stack de dades amb PostgreSQL, InfluxDB i Grafana, les metricques essencials i alertes serien:

**PostgreSQL**:

Metriques essencials:
- Connexions actives (`pg_stat_activity`)
- Tamany total de la base de dades
- Ratio de cache hit (`pg_stat_user_tables`)
- Replicacio (si l'uses)
- Dead tuples (indicador de vacuum necessari)
- Locks en espera

Alertes:
- Connexions actives > 80% del maxim: pot ser saturacio.
- Cache hit ratio < 95%: memoria insuficient.
- Dead tuples > 10k: vacuum no s'ha executat.
- Disc > 85%: risc de fallada.

**InfluxDB**:

Metriques essencials:
- Memoria usada (InfluxDB es RAM-golaf).
- Write throughput (puntos per segon).
- Cardinalitat de series (número de series uniques).
- Query latency p95.
- Errors d'escriptura.

Alertes:
- Memoria > 80% del limit: el servei pot caure.
- Write errors > 0 per minut: algo falla amb els sensors o xarxa.
- Cardinalitat creixent rapidament: pot ser un bug que genera series infinites.
- Query latency p95 > 1s: rendiment pobre.

**Grafana**:

Metriques essencials:
- Up (esta corrent).
- Resposta a la UI.
- Connexions a la base de dades (si Grafana es cau, tot el sistema es cec).

Alertes:
- Grafana down: alerta critica. Si Grafana es cau, no pots veure res.
- Alertes d'altres serveis no arriben: probablement el canal d'alertes te problema.

**Exemple de regla d'alerta Prometheus**:

```yaml
groups:
- name: database
  rules:
  - alert: PostgresConnectionsHigh
    expr: pg_stat_activity_count > 80
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "PostgreSQL connexions altes"
      description: "Connexions {{ $value }} > 80"
  
  - alert: DiskSpaceLow
    expr: (node_filesystem_avail_bytes / node_filesystem_size_bytes) < 0.15
    for: 10m
    labels:
      severity: critical
    annotations:
      summary: "Disc {{ $labels.mountpoint }} al {{ $value | humanizePercentage }}"
```

**Llindars inicials**:

- Comença amb llindars conservadors. No vols falses alarmes.
- Ajusta basant-te en l'experiencia de 1-2 setmanes.
- Millor una alerta que salta un cop per fals positiu que una que no salta quan cal.

---

## Pregunta 15 (oberta): Monitoritzar la salut de la RPi

**Resposta model**:

La RPi te especificitats que cal monitoritzar, mes enlla dels serveis:

**1. Temperatura**:

La RPi pot escalfar-se molt, especialment en caixas tancades. La CPU comença a fer throttling a 80°C, lo que redueix el rendiment.

- Perill: throttling = rendiment baixa, latencies augmenten.
- Mesura: `vcgencmd measure_temp` o el sensor intern exposat per `node-exporter`.
- Alerta: temperatura > 75°C, risc > 80°C.
- Solucio: disipador, ventilador, netejar la caixa de pols, moure a un lloc ventilat.

**2. Vida util de la microSD**:

Les microSD tenen una vida util limitada (~100k cicles d'escriptura per cel·la). Si tens molts logs o una base de dades a la SD, pot fallar.

- Perill: fallada sobtada = perdua de dades + temps de recuperacio.
- Mesura: `mmc` SMART info o monitoring de write amplification.
- Alerta: SMART errors, write count alt.
- Solucio: moure dades a SSD, minimitzar escriptures (`noatime`, logs a tmpfs).

**3. Alimentacio**:

Si la font d'alimentacio es inadequada (menys de 3A per RPi 4), pot haver caigudes intermitents que es manifesten com a reinicis random.

- Perill: corromp filesystem, perdua de dades.
- Mesura: `dmesg | grep -i undervoltage`, o el flag de undervoltage a `/sys`.
- Alerta: `Under-voltage detected!` a logs.
- Solucio: font oficial o de qualitat, evitar sobrecregues.

**4. Memoria RAM i swap**:

Si la RPi esta saturada de memoria, comenca a usar swap (a la microSD!), lo que accelera el desgast.

- Perill: degradacio de rendiment + desgast de SD.
- Mesura: `node-exporter` te metricques de RAM i swap.
- Alerta: swap in/out > 0 constant, RAM > 90%.
- Solucio: tancar serveis, optimitzar, pujar RAM (RPi 4 fins a 8 GB).

**5. Xarxa**:

Si la connexio es inestable, els serveis poden ser lents sense motiu aparent.

- Perill: falsejar mètriques (timeout), serveis inconsistents.
- Mesura: `node-exporter` amb `collectors.enabled: netdev`, o `smokeping` extern.
- Alerta: packet loss > 1%, latency > 100ms.
- Solucio: cable en lloc de WiFi si es possible, router de qualitat.

**Configuracio de node-exporter al BernatLab**:

```yaml
node-exporter:
  image: prom/node-exporter:latest
  command:
    - '--path.rootfs=/host'
    - '--collector.filesystem.mount-points-exclude=^/(sys|proc|dev|host|etc)($$|/)'
  volumes:
    - /:/host:ro,rslave
  networks: [monitoring]
```

Aixo exposa totes les metricques del sistema a Prometheus. Despres pots crear alerts i dashboards.

**Limitacio**: la monitoritzacio de la RPi consumeix recursos. A una RPi 4 de 4 GB amb 10 serveis, afegir node-exporter + Prometheus + Grafana consumeix ~500 MB de RAM. Es acceptable, pero no ilimitat.

---

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum. La monitoritzacio es llarga pero basica.
- **3-4 encerts**: Refes l'exercici. Cal practicar amb Prometheus/Grafana.
- **0-2 encerts**: Repassem. Es un capitol dens pero practic.

## Que fer si has encertat totes

- Passa al **Capitol 10** (orquestracio).
- Configura Alertmanager amb notificacions a Telegram.
- Apren PromQL basic.
