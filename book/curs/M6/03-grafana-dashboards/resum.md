# Resum - Capitol 3: Grafana i dashboards

## La idea clau

Prometheus es la base de dades de metricas pero la seva UI es funcional, no maca. Grafana es la capa visual: agafa les dades de Prometheus (o altres fonts) i les presenta en dashboards bonics amb grafs interactius, mapes de calor, gauges i taules. A mes a mes, Grafana tambe pot crear alertes.

## Que es Grafana?

Grafana es una eina open source per visualitzar dades de series temporals. Pensa en ella com a "Tableau o Kibana pero per a metricas tecniques". Suporta moltes fonts de dades:

- **Prometheus** (la que usarem)
- **InfluxDB** (cap 6 del M3)
- **MySQL/PostgreSQL** (cap 5 del M3)
- **Loki** (per logs, ho veurem al cap 5 d'aquest modul)
- **CloudWatch, Datadog, Elasticsearch, etc.**

El que veus a Grafana es un **dashboard** compost per **panells**. Cada panell es un graf, un numero, una taula, o un mapa que consulta dades d'una font.

## Instal·lacio a la RPi

```yaml
# Afegeix al docker-compose.yml
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
      - GF_SECURITY_ADMIN_PASSWORD=canviar_aixo
      - GF_USERS_ALLOW_SIGN_UP=false
      - GF_INSTALL_PLUGINS=
    ports:
      - "3000:3000"
```

Accedeix a `http://IP_RPI:3000`, login amb admin/canviar_aixo. El primer que cal fer es canviar la contrassenya.

## Afegir Prometheus com a font de dades

A la UI de Grafana:

1. Ves a "Connections" -> "Data sources" -> "Add data source"
2. Tria "Prometheus"
3. A "URL" posa `http://prometheus:9090` (el nom del servei a docker, no localhost!)
4. Activa "Default" perque sigui la font per defecte
5. Guarda i testeja (hauria de dir "Data source is working")

## Crear el primer panell

1. Ves a "Dashboards" -> "New" -> "New dashboard"
2. Clica "Add visualization"
3. A la query, escriu una consulta PromQL. Per exemple:

```promql
# CPU del sistema
100 - (avg by(instance)(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
```

4. A la dreta, configura el tipus de graf (Time series, Stat, Gauge, etc.)
5. A "Title" posa algo descriptiu: "CPU sistema %"
6. Clica "Apply" i despres "Save dashboard"

## Tipus de panell comuns

- **Time series**: graf de linies en el temps. Perfecte per CPU, memoria, xarxa.
- **Stat**: un numero gran amb color segons el valor. Bonic per "Temperatura actual".
- **Gauge**: velocimetre semicircular. Bonic per "Disc usat %".
- **Bar chart**: barres. Per comparacio entre elements.
- **Table**: taula amb files i columnes. Per llistes de serveis.
- **Heatmap**: mapa de calor. Per patrons temporals.
- **Logs**: nomes amb Loki. Per veure logs al mateix panell.

## Variables: dashboards parametric

Un dels trucs mes poderosos de Grafana son les **variables**. Et permeten fer un panell parametritzat que canvii segons el que triis a un desplegable.

Exemple: una variable `$contenidor` que filtres metricas per contenidor:

1. A la part superior del dashboard, toca "Settings" -> "Variables" -> "New variable"
2. Nom: `contenidor`
3. Type: "Query"
4. Data source: Prometheus
5. Query: `label_values(container_last_seen{name=~".+"}, name)`
6. "Multi-value" i "Include All option" activats
7. Guarda

Ara pots fer consultes tipus:

```promql
container_memory_usage_bytes{name="$contenidor"}
```

I un desplegable et deixara triar quin contenidor vols veure.

## Provisioning: configuracio com a codi

En lloc de configurar tot per la UI (que es tedios i no es pot replicar), Grafana suporta **provisioning**: fitxers YAML que defineixen data sources, dashboards i alertes. Son al directori `/etc/grafana/provisioning/`.

Exemple de data source provisionada:

```yaml
# grafana/provisioning/datasources/prometheus.yml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    editable: true
```

Exemple de dashboard provisionat:

```yaml
# grafana/provisioning/dashboards/bernatlab.yml
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

Despres pots exportar els teus dashboards a JSON i copiar-los al directori `/var/lib/grafana/dashboards/`. Grafana els carregara automaticament.

## Dashboards essencials del BernatLab

Un bon dashboard base hauria de tenir:

1. **Vista general del sistema**:
   - CPU (per core i mitjana)
   - Memoria (usada, lliure, swap)
   - Disc (usat, IOPS)
   - Xarxa (in/out per interfície)
   - Temperatura
   - Uptime

2. **Contenidors Docker**:
   - Llista de contenidors amb estat
   - CPU per contenidor
   - Memoria per contenidor
   - Xarxa per contenidor

3. **Serveis aplicacio**:
   - Home Assistant: latencia API, nombre d'entitats
   - InfluxDB: punts escrits, queries per segon
   - Grafana mateix: temps de resposta de les peticions

4. **Xarxa**:
   - Latencia al router
   - DNS resolution time
   - Peticions HTTP per minut

No intentis posar-ho tot al primer dia. Comença amb 4-6 panells basics i ves afegint.

## Compartir dashboards

Grafana te una comunitat molt activa i milers de dashboards compartits. A "Dashboards" -> "New" -> "Import" pots posar un ID o URL i importar un dashboard de grafana.com.

Alguns IDs utils:
- **1860**: Node Exporter Full (dashbard complert del sistema)
- **893**: Docker Container (basat en cAdvisor)
- **13639**: Blackbox Exporter (per probes HTTP/TCP)

Pots agafar-ne un de base i personalitzar-lo per les teves necessitats.

## Alertes basiques a Grafana

Encara que Alertmanager (que veurem al cap 4) es l'eina "pura" d'alertes de Prometheus, Grafana tambe pot crear alertes directament:

1. Edita un panell
2. Ves a la pestanya "Alert"
3. Crea una "Alert rule" amb:
   - Condicio: per exemple, `WHEN last() OF query(A) IS ABOVE 80`
   - Evaluacio: cada 1 min, durant 5 min
   - Notifications: Telegram, email, webhook

Grafana es mes facil d'utilitzar pero menys flexible. Per a alertes complexes usa Alertmanager.

## Limitacions a la RPi

- **No abusis dels dashboards**: cada panell es una consulta a Prometheus. 20 panells = 20 consultes cada 15 segons = carrega.
- **Desactiva les auto-refresh molt seguides**: 30s en lloc de 10s ja està be.
- **Limita el periode**: per defecte es "Last 6 hours", no posis "Last 30 days" si no cal.
- **Rendering**: obrir Grafana al movil gasta memoria de la RPi. Tingues compte amb multiples usuaris.

## Connexions amb altres capitols

- **M6 Cap 2** - Prometheus, la font de dades principal.
- **M6 Cap 4** - Alertes: Grafana pot crear-les o pots usar Alertmanager.
- **M3 Cap 6** - InfluxDB tambe es pot visualitzar amb Grafana.
- **M3 Cap 10** - Visualitzacio de dades amb altres eines.
