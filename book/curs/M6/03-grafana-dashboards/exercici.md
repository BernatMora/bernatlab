# Exercici practic - Capitol 3: Grafana i dashboards

> 45-60 min · Real a la teva RPi

## Objectiu

Instal·lar Grafana, connectar-lo a Prometheus, i crear el teu primer dashboard amb panells basics del sistema. Acabaras tenint una vista visual de la teva RPi.

## Requisits

- RPi amb Prometheus ja funcionant (capitol 2)
- 45-60 minuts
- Conexio a la xarxa local

## Pas 1: Afegeix Grafana al docker-compose (10 min)

Edita el teu `docker-compose.yml` i afegeix:

```yaml
  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    restart: unless-stopped
    user: "0:0"
    volumes:
      - ./grafana/data:/var/lib/grafana
      - ./grafana/provisioning:/etc/grafana/provisioning
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=bernatlab2026
      - GF_USERS_ALLOW_SIGN_UP=false
    ports:
      - "3000:3000"
```

Crea les carpetes i puja el servei:

```bash
cd ~/bernatlab
mkdir -p grafana/data grafana/provisioning/datasources grafana/provisioning/dashboards
docker compose up -d grafana
docker ps | grep grafana
```

Accedeix a `http://IP_RPI:3000` i entra amb `admin` / `bernatlab2026`.

## Pas 2: Connecta Prometheus a Grafana (5 min)

A la UI de Grafana:
1. Ves a "Connections" -> "Data sources" -> "Add data source"
2. Tria "Prometheus"
3. URL: `http://prometheus:9090`
4. Activa "Default"
5. Clica "Save & test" (hauria de dir "Data source is working")

## Pas 3: Crea el teu primer panell (15 min)

1. Ves a "Dashboards" -> "New" -> "New dashboard"
2. "Add visualization" -> tria Prometheus com a data source
3. Escriu la consulta PromQL:

```promql
100 - (avg by(instance)(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
```

4. A la dreta:
   - Title: "CPU sistema %"
   - Visualization: Time series
   - Unit: Percent (0-100)
5. A "Panel options" -> "Graph styles" -> posa el "Fill opacity" a 20
6. Clica "Apply"
7. "Save dashboard" amb nom "BernatLab Sistema"

## Pas 4: Afegeix 4 panells mes (15 min)

Repeteix el proces per afegir:

**Panell 2 - Memoria** (Gauge):
- Title: "Memoria usada %"
- Consulta:
```promql
(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100
```
- Type: Gauge
- Unit: Percent
- Thresholds: 0-60 verd, 60-80 groc, 80-100 vermell

**Panell 3 - Disc** (Stat):
- Title: "Disc lliure"
- Consulta:
```promql
node_filesystem_avail_bytes{mountpoint="/"} / 1024 / 1024 / 1024
```
- Type: Stat
- Unit: GB
- Thresholds: > 5 verd, 1-5 groc, < 1 vermell

**Panell 4 - Temperatura** (Stat):
- Title: "Temperatura CPU"
- Consulta:
```promql
node_thermal_zone_temp
```
- Type: Stat
- Unit: Celsius
- Thresholds: 0-60 verd, 60-75 groc, 75+ vermell

**Panell 5 - Contenidors** (Table):
- Title: "Contenidors actius"
- Consulta:
```promql
container_last_seen{name=~".+"}
```
- Type: Table
- Transformations: "Organize fields" -> mostra nomes `name` i `value`

Organitza els panells: 2 a la fila de dalt (CPU + Memoria), 3 a la fila de baix (Disc, Temperatura, Contenidors).

## Pas 5: Importa un dashboard de la comunitat (10 min)

1. Ves a "Dashboards" -> "New" -> "Import"
2. A "Import via grafana.com" posa l'ID `1860`
3. Tria Prometheus com a data source
4. Clica "Import"

Ara tens un dashboard super complert amb centenars de panells. Explora'l i veuras metricas que ni sabies que existien. Pots esborrar panells que no t'interessin.

## Pas 6: Configura el provisioning (5 min)

Crea el fitxer:

```bash
nano grafana/provisioning/datasources/prometheus.yml
```

Enganxa:

```yaml
apiVersion: 1
datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    editable: true
```

Despres:

```bash
nano grafana/provisioning/dashboards/bernatlab.yml
```

Enganxa:

```yaml
apiVersion: 1
providers:
  - name: 'BernatLab'
    orgId: 1
    folder: 'BernatLab'
    type: file
    disableDeletion: false
    updateIntervalSeconds: 30
    allowUiUpdates: true
    options:
      path: /var/lib/grafana/dashboards
```

```bash
docker compose restart grafana
```

Si exportes un dashboard a JSON i el poses a `grafana/dashboards/`, es carregara automaticament.

## Validacio

Has acabat si:

- [ ] Grafana esta corrent i accessible al port 3000.
- [ ] Has connectat Prometheus com a data source.
- [ ] Tens un dashboard "BernatLab Sistema" amb almenys 5 panells.
- [ ] Has importat el dashboard 1860 (Node Exporter Full).
- [ ] Has creat els fitxers de provisioning.
- [ ] Has canviat la contrasenya d'admin per defecte.

## Per aprofundir

- Afegeix una variable "contenidor" al dashboard i parametritza els panells.
- Crea alertes basiques a Grafana (p.ex. temperatura > 75 graus).
- Exporta el teu dashboard a JSON i guarda'l al repositori del BernatLab.
- Explora els dashboards de la comunitat (893 per Docker).
