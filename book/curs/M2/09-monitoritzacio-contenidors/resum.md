# Resum - Capitol 9: Monitoritzacio de contenidors

## La idea clau

Si tens contenidors en marxa 24/7, necessites **veure que esta passant**: quanta CPU gasten, quanta memoria, quin tràfic de xarxa, quins errors surten als logs. Sense monitoritzacio, estas a cegues: no saps si un servei es lent, si s'ha caigut, o si el disc esta ple fins que es massa tard.

## Que cal monitoritzar

Tres dimensions basics:

1. **Recursos de l'amfitrio**: CPU, RAM, disc, xarxa, temperatura de la CPU.
2. **Contenidors individuals**: quina part dels recursos consumeix cada un, quants reinicis ha tingut, quants bytes ha enviat/rebut.
3. **Aplicacio**: logs, errors, latencia, peticions HTTP, metriques de negoci (usuaris actius, transaccions per segon).

## Estadistiques en temps real amb `docker stats`

La comanda mes simple:

```bash
docker stats
```

Retorna una taula en temps real amb:

```
CONTAINER   CPU %   MEM USAGE / LIMIT   MEM %   NET I/O           BLOCK I/O   PIDS
web         0.05%   50MiB / 1GiB        4.89%   1.2kB / 0B       0B / 0B     3
db          1.20%   200MiB / 1GiB       19.5%   5.4kB / 8.1kB    100MB / 50MB 12
```

- **CPU %**: percentatge de CPU que esta fent servir.
- **MEM USAGE / LIMIT**: memoria actual / limit (si n'hi ha).
- **NET I/O**: bytes rebuts / enviats per xarxa.
- **BLOCK I/O**: bytes llegits / escrits a disc.
- **PIDS**: nombre de processos dins el contenidor.

Opcions utils:

```bash
# Sense streaming, nomes un snapshot
docker stats --no-stream

# Format custom
docker stats --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"

# Nomes alguns contenidors
docker stats web db

# Mostrar mes d'un cop
docker stats --no-trunc
```

## Logs: `docker logs`

Cada contenidor te els seus logs a `stdout` i `stderr`. Docker els captura i els pots veure:

```bash
# Ultimes linies
docker logs web

# Seguint en temps real
docker logs -f web

# Ultimes 100 linies
docker logs --tail 100 web

# Des de fa 10 min
docker logs --since 10m web

# Amb timestamps
docker logs -t web
```

### Drivers de logs

Per defecte Docker escriu els logs a un fitxer JSON a l'amfitrio (`json-file`). Pero pots canviar-ho:

- **json-file**: per defecte.
- **journald**: systemd journal.
- **syslog**: servidor syslog.
- **fluentd, gelf, awslogs, splunk**: eines externes.
- **local**: optimitzat per a poca espai.

Configuracio al daemon:

```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

Aixo limita cada log a 10 MB i max 3 fitxers per contenidor. Sense limit, els logs poden omplir el disc!

## cAdvisor: monitoritzacio visual

**cAdvisor** (Container Advisor) es una eina de Google que mostra metricques visuals dels teus contenidors. Es perfecta per a un homelab.

```yaml
# docker-compose.yml
services:
  cadvisor:
    image: gcr.io/cadvisor/cadvisor:latest
    ports:
      - "8080:8080"
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:ro
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
    privileged: true  # cal per accedir a /sys
```

Amb aixo tens una UI web a `http://raspberry.local:8080` que mostra:

- Grafiques de CPU/RAM per contenidor.
- Us de xarxa i disc.
- Historial.

Pero compte: cAdvisor te limitacions. No guarda metricques a llarg termini. Si vols historic, cal combinar-lo amb Prometheus.

## Prometheus + Grafana: la combinacio profesional

Si vols una monitoritzacio de veritat (historic, alarmes, dashboards), la combinacio classica es:

- **Prometheus**: recull metricques de moltes fonts (cAdvisor, Node Exporter, exporters de aplicacions).
- **Grafana**: visualitza les metricques en dashboards bonics.
- **Alertmanager**: envia alarmes (email, Slack, etc.) si algo va malament.

Exemple amb Compose:

```yaml
version: "3.8"
services:
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana-data:/var/lib/grafana
    depends_on:
      - prometheus

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

  node-exporter:
    image: prom/node-exporter:latest
    ports:
      - "9100:9100"

volumes:
  prometheus-data:
  grafana-data:
```

`prometheus.yml`:

```yaml
global:
  scrape_interval: 15s
scrape_configs:
  - job_name: 'cadvisor'
    static_configs:
      - targets: ['cadvisor:8080']
  - job_name: 'node'
    static_configs:
      - targets: ['node-exporter:9100']
```

Aixo es la base d'un sistema de monitoritzacio professional. Es mes complexe pero es la referencia a la industria.

## Logs centralitzats

Si tens molts serveis, anar mirant `docker logs` de cada un es tedios. La solucio es centralitzar-los:

- **Loki + Promtail** (Grafana): la opcio mes moderna. Loki es un "Prometheus pero per a logs". Promtail els recull de cada contenidor.
- **ELK Stack** (Elasticsearch + Logstash + Kibana): molt potent pero molt pesat.
- **Graylog**: alternativa mes lleugera.
- **Simplement `docker logs -f` + un multiplexor** com `multitail` o `dozzle**.

### Dozzle: una eina web lleugera

Una eina molt recomanable per a homelab:

```yaml
services:
  dozzle:
    image: amir20/dozzle:latest
    ports:
      - "9999:8080"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
```

A `http://raspberry.local:9999` tens una UI web que mostra els logs de tots els teus contenidors en temps real, amb cerca i filtres.

## Uptime monitoring

A mes dels recursos, vols saber si els teus serveis responen. Hi ha eines especifiques:

- **Uptime Kuma**: una eina web self-hosted que comprova periodicament si els teus serveis responen.
- **Healthchecks.io**: servei extern (gratis) per a cron jobs.

Exemple amb Uptime Kuma:

```yaml
services:
  uptime-kuma:
    image: louislam/uptime-kuma:latest
    ports:
      - "3001:3001"
    volumes:
      - uptime-kuma-data:/app/data
```

A `http://raspberry.local:3001` tens una web amb estat de tots els teus serveis (HTTP, TCP, ping, etc.).

## Healthchecks definits als serveis

Ja ho hem vist al capitol 7, pero es important recordar-ho. Un healthcheck es una comanda que Docker executa per saber si el servei esta "sa":

```yaml
services:
  db:
    image: postgres
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 30s
```

Docker pot mostrar l'estat del healthcheck amb `docker ps`:

```
CONTAINER   STATUS                    PORTS
db          Up 2 hours (healthy)      5432/tcp
```

## Connexions amb altres capitols

- **M2 Cap 6** - Els escaners de vulnerabilitats son part de la seguretat pero tambe del monitoring.
- **M2 Cap 7** - Les actualitzacions son reaccions a l'observacio.
- **M2 Cap 8** - Els backups son part del monitoring (saber que el backup sha fet be).
