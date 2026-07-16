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

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum. La monitoritzacio es llarga pero basica.
- **3-4 encerts**: Refes l'exercici. Cal practicar amb Prometheus/Grafana.
- **0-2 encerts**: Repassem. Es un capitol dens pero practic.

## Que fer si has encertat totes

- Passa al **Capitol 10** (orquestracio).
- Configura Alertmanager amb notificacions a Telegram.
- Apren PromQL basic.
