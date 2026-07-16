# Exercici practic - Capitol 9: Monitoritzacio de contenidors

> 40-60 min · Real al teu sistema

## Objectiu

Muntar una pila de monitoritzacio amb cAdvisor, Dozzle, Uptime Kuma i Prometheus + Grafana (basic). Acabaras tenint un sistema que et mostra en temps real l'estat dels teus contenidors.

## Requisits

- Docker Compose instal·lat
- 40-60 minuts
- 1-2 GB de RAM lliure addicional (per Prometheus + Grafana)

## Pas 1: Crea el directori (5 min)

```bash
mkdir -p ~/monitoring-test
cd ~/monitoring-test
mkdir -p grafana-data prometheus-data
```

## Pas 2: Crea el compose amb cAdvisor i Dozzle (10 min)

Crea `docker-compose.yml`:

```yaml
version: "3.8"
services:
  # Monitoritzacio basica: cAdvisor
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

  # Logs centralitzats: Dozzle
  dozzle:
    image: amir20/dozzle:latest
    ports:
      - "9999:8080"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
    restart: unless-stopped

  # Uptime: Uptime Kuma
  uptime-kuma:
    image: louislam/uptime-kuma:latest
    ports:
      - "3001:3001"
    volumes:
      - uptime-kuma-data:/app/data
    restart: unless-stopped

volumes:
  uptime-kuma-data:
```

Arrenca:

```bash
docker compose up -d
docker compose ps
```

## Pas 3: Prova cAdvisor (5 min)

Obre `http://raspberry.local:8080` al navegador. Hauries de veure:

- Llista de contenidors amb CPU i RAM.
- Grafiques en temps real.
- Informacio de xarxa i disc.

Si vols, pots explorar les pestanyes "Overview" i "Docker containers".

## Pas 4: Prova Dozzle (5 min)

Obre `http://raspberry.local:9999`. Hauries de veure:

- Llista de tots els contenidors.
- Logs en temps real.
- Filtres per contenidor.
- Cerca de text.

Prova a fer clic en un contenidor i mira els logs.

## Pas 5: Configura Uptime Kuma (10 min)

Obre `http://raspberry.local:3001`. Primer cop:

1. Crea un usuari (admin/admin).
2. Afegeix un monitor HTTP:
   - Type: HTTP(s)
   - Friendly name: "Portainer test" (o el que tinguis)
   - URL: http://localhost:9000 (Portainer, si el tens)
   - Heartbeat interval: 60 seconds
3. Fes clic a "Save".
4. Repeteix per a altres serveis:
   - Grafana: http://localhost:3000
   - cAdvisor: http://localhost:8080

Si tens 3-4 serveis configurats, tens un taulell d'estat basic.

## Pas 6: Afegeix Prometheus + Grafana (15 min)

Afegeix al `docker-compose.yml`:

```yaml
  # Prometheus: recollida de metricques
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
      - '--web.console.libraries=/usr/share/prometheus/console_libraries'
    restart: unless-stopped

  # Grafana: visualitzacio
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
    restart: unless-stopped

  # Node exporter: metricques de la RPi
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
```

Crea `prometheus.yml`:

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

Afegeix els nous volums al final:

```yaml
volumes:
  uptime-kuma-data:
  prometheus-data:
  grafana-data:
```

Re-arrenca:

```bash
docker compose up -d
docker compose ps
```

## Pas 7: Verifica Prometheus (5 min)

Obre `http://raspberry.local:9090`. Hauries de veure la UI de Prometheus.

- Ves a "Status" > "Targets". Hauries de veure "prometheus", "cadvisor" i "node" com a "UP".
- Ves a "Graph" i prova una query: `container_memory_usage_bytes{container_label_com_docker_compose_project="monitoring-test"}`

## Pas 8: Connecta Grafana amb Prometheus (10 min)

Obre `http://raspberry.local:3000` (admin/admin).

1. Ves a "Configuration" > "Data sources" > "Add data source".
2. Tria "Prometheus".
3. URL: `http://prometheus:9090`
4. Fes clic a "Save & test".

Si tot va be, veuras un missatge "Data source is working".

Ara importa un dashboard:

1. Ves a "Dashboards" > "Import".
2. ID: 893 (Docker Container/Host Monitoring)
3. Selecciona el teu data source de Prometheus.
4. Fes clic a "Import".

Hauries de veure un dashboard amb grafiques dels teus contenidors.

## Pas 9: Explora (5 min)

- Fes clic al dashboard.
- Prova de canviar el temps (es pot posar "Last 5 minutes", "Last 1 hour", etc.).
- Mira les grafiques de CPU, RAM, xarxa, disc.
- Juga amb les queries a Prometheus.

## Pas 10: Neteja

```bash
cd ~/monitoring-test
docker compose down
rm -rf ~/monitoring-test
```

## Validacio

Has acabat si:

- [ ] Has vist cAdvisor funcionant i mostrant metricques dels teus contenidors.
- [ ] Has vist Dozzle mostrant logs en temps real.
- [ ] Has configurat Uptime Kuma amb algun monitor.
- [ ] Has vist Prometheus recollint metricques.
- [ ] Has configurat Grafana amb un dashboard de Docker.
- [ ] Has netejat tots els recursos.

## Per aprofundir

- Configura Alertmanager per a que t'avisi per Telegram/Discord si alguna metrica es dispara.
- Investiga els "exporters" especifics per a les teves aplicacions (PostgreSQL exporter, Nextcloud exporter, etc.).
- Apren les queries basics de PromQL.
- Configura la retencio de Prometheus (per defecte nomes guarda 15 dies).
