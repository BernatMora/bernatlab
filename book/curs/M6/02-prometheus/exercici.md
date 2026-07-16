# Exercici practic - Capitol 2: Prometheus

> 45-60 min · Real a la teva RPi

## Objectiu

Instal·lar Prometheus, node-exporter i cAdvisor a la teva RPi. Configurar els seus targets i fer les primeres consultes PromQL per entendre quines dades tens disponibles. Acabaras sabent extreure la temperatura de la RPi i l'ús de CPU de cada contenidor.

## Requisits

- RPi amb Docker ja instal·lat
- 500 MB d'espai lliure
- docker-compose funcionant
- 45-60 minuts

## Pas 1: Crea l'estructura de carpetes (5 min)

```bash
cd ~/bernatlab
mkdir -p prometheus/data
ls -la prometheus/
```

## Pas 2: Crea el fitxer prometheus.yml (10 min)

```bash
nano prometheus/prometheus.yml
```

Enganxa aquesta configuracio inicial:

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'node'
    static_configs:
      - targets: ['node-exporter:9100']

  - job_name: 'cadvisor'
    static_configs:
      - targets: ['cadvisor:8080']

  - job_name: 'dockercontainers'
    static_configs:
      - targets: ['cadvisor:8080']
```

Guarda i tanca (`Ctrl+O`, `Enter`, `Ctrl+X`).

## Pas 3: Afegeix els serveis al docker-compose (10 min)

Edita el teu `docker-compose.yml` i afegeix els tres serveis nous:

```yaml
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    restart: unless-stopped
    user: "0:0"
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
      - ./prometheus/data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.retention.time=30d'
      - '--storage.tsdb.retention.size=2GB'
    ports:
      - "9090:9090"

  node-exporter:
    image: prom/node-exporter:latest
    container_name: node-exporter
    restart: unless-stopped
    pid: host
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/rootfs:ro
    command:
      - '--path.procfs=/host/proc'
      - '--path.sysfs=/host/sys'
      - '--path.rootfs=/rootfs'
      - '--collector.filesystem.mount-points-exclude=^/(sys|proc|dev|host|etc)($$|/)'
    ports:
      - "9100:9100"

  cadvisor:
    image: gcr.io/cadvisor/cadvisor:latest
    container_name: cadvisor
    restart: unless-stopped
    privileged: true
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:ro
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
    ports:
      - "8080:8080"
```

Aixeca els serveis:

```bash
docker compose up -d prometheus node-exporter cadvisor
docker ps | grep -E "prometheus|exporter|cadvisor"
```

## Pas 4: Verifica que tot funciona (10 min)

Mira els targets a la UI de Prometheus:

```
http://IP_RPI:9090/targets
```

Hauries de veure 4 targets (prometheus, node, cadvisor x2), tots amb estat "UP" en verd.

Si algun esta "DOWN", comprova:
- El contenidor esta corrent? `docker ps`
- El port esta accessible? `curl http://localhost:9100/metrics`
- Hi ha errors al log? `docker logs prometheus`

## Pas 5: Fes les primeres consultes PromQL (15 min)

A `http://IP_RPI:9090/graph`, prova aquestes consultes una a una:

```promql
# 1. Numero de CPUs logiques
count(node_cpu_seconds_total{mode="idle"})

# 2. CPU en us (per core, en %)
100 - (avg by(cpu)(rate(node_cpu_seconds_total{mode="idle"}[2m])) * 100)

# 3. Memoria disponible en GB
node_memory_MemAvailable_bytes / 1024 / 1024 / 1024

# 4. Espai lliure al disc principal (%)
(node_filesystem_avail_bytes{mountpoint="/"} * 100) / node_filesystem_size_bytes{mountpoint="/"}

# 5. Temperatura de la CPU (RPi)
node_thermal_zone_temp

# 6. Bytes rebuts a la xarxa
rate(node_network_receive_bytes_total{device!="lo"}[5m])

# 7. Memoria usada per contenidor
container_memory_usage_bytes{name=~".+"}

# 8. CPU per contenidor
rate(container_cpu_usage_seconds_total{name=~".+"}[5m]) * 100
```

Per cada consulta, canvia a la pestanya "Graph" per veure el graf temporal.

## Pas 6: Mira les metricas raw (5 min)

Accedeix als endpoints directament:

```bash
# Metricas de la RPi
curl -s http://localhost:9100/metrics | head -20
curl -s http://localhost:9100/metrics | grep node_thermal

# Metricas dels contenidors
curl -s http://localhost:8080/metrics | head -20
curl -s http://localhost:8080/metrics | grep container_memory

# Comptador de series
curl -s http://localhost:9090/api/v1/status/tsdb | python3 -m json.tool
```

## Validacio

Has acabat si:

- [ ] Prometheus, node-exporter i cAdvisor corren com a contenidors.
- [ ] Els 4 targets apareixen com a "UP" a la UI.
- [ ] Has fet almenys 5 consultes PromQL amb resultats.
- [ ] Pots veure la temperatura de la RPi.
- [ ] Pots veure l'ús de memoria i CPU per contenidor.
- [ ] Has explorat l'endpoint `/metrics` directament.

## Per aprofundir

- Afegeix un quart target: si tens nginx, afegeix nginx_exporter.
- Investiga les `recording rules` per fer consultes mes eficients.
- Prova a canviar `scrape_interval` a 30s i observa l'efecte.
- Mira quantes series temporals tens i calcula quant ocupen.
