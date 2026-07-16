# Resum — Capitol 10: Visualitzacio de dades amb Grafana

## La idea clau

De que serveixen totes les dades que recollim si no les podem **veure** i **entendre**? Al BernatLab tinc anys de lectures de sensors emmagatzemades a InfluxDB, pero si nomes veig taules SQL o fitxers CSV, no serveix de gaire. Necessito **visualitzacions** que em permetin veure tendencies, comparar dies, detectar anomalies.

**Grafana** es l'eina estandard per visualitzar dades de series temporals. Es l'eina que tanca el cercle: sensors -> MQTT -> InfluxDB -> Grafana. Amb Grafana puc veure la temperatura del meu hivernacle en temps real, comparar amb la setmana passada, i rebre alertes si baixa de 5°C.

## Que es Grafana?

Grafana es una plataforma de **visualitzacio i monitoritzacio** open source. Permet:

- Crear **dashboards** amb grafics (linies, barres, pastis, mapes de calor, gauges).
- Connectar-se a **multiples fonts de dades** (InfluxDB, Prometheus, PostgreSQL, MySQL, Loki, etc.).
- Fer **alertes** automaticament (avisar si la temperatura baixa de 5°C).
- Compartir dashboards amb altres.
- Funciona com a **aplicacio web** o app d'escriptori.

### Quan usar Grafana

Grafana es la millor opcio quan:

- Tens **series temporals** (dades indexades per temps).
- Necessites **dashboards** visuals i intuïtius.
- Vols **alertes** automatiques.
- Tens multiples fonts de dades per **unificar**.

NO es la millor opcio quan:

- Les dades no son temporals (millor Metabase, Tableau, etc.).
- Nomes vols fer una consulta puntual (millor l'eina nativa de la BD).
- No tens cap pantalla on mostrar els grafics.

## Instal·lacio al BernatLab

```yaml
services:
  grafana:
    image: grafana/grafana-oss:latest
    container_name: bernatlab-grafana
    restart: unless-stopped
    environment:
      GF_SECURITY_ADMIN_USER: bernat
      GF_SECURITY_ADMIN_PASSWORD: ${GRAFANA_PASSWORD}
      GF_INSTALL_PLUGINS: ""
    volumes:
      - /home/pi/bernatlab/grafana/data:/var/lib/grafana
      - /home/pi/bernatlab/grafana/config:/etc/grafana
    ports:
      - "127.0.0.1:3000:3000"
```

## Configurar una font de dades (InfluxDB)

1. Accedeix a `http://localhost:3000` (via Tailscale).
2. Login amb les credencials.
3. Ves a **Connections > Data Sources > Add data source**.
4. Selecciona **InfluxDB**.
5. Configura:
   - URL: `http://influxdb:8086`
   - Organization: `bernatlab`
   - Token: el token que vas crear a InfluxDB.
   - Default bucket: `hort`
6. **Save & test**.

## Crear un dashboard

Un **dashboard** es una colleccio de **panells** (grafics). Per crear-ne un:

1. Ves a **Dashboards > New > New dashboard**.
2. **Add visualization**.
3. Selecciona la font de dades (InfluxDB).
4. Escriu una consulta **Flux**:

```flux
from(bucket: "hort")
  |> range(start: -24h)
  |> filter(fn: (r) => r._measurement == "temperatura")
  |> aggregateWindow(every: 5m, fn: mean, createEmpty: false)
```

5. Selecciona el tipus de grafic: **Time series** (linia).
6. Guarda el panell.
7. Repeteix per a cada sensor.

## Tipus de grafics utils

- **Time series** (linia): la mes comuna, ideal per series temporals.
- **Bar chart** (barres): per comparar categories.
- **Stat / Big number**: per mostrar un valor prominent (ultima temperatura).
- **Gauge**: per mostrar un valor respecte a un rang (percentatge d'humitat).
- **Heatmap**: per mostrar patrons al llarg del temps (dies x hores).
- **Table**: per mostrar dades tabulades.
- **Pie chart**: per mostrar composicio.

## Exemples de grafics per a l'hort

### Temperatura ultima setmana

```flux
from(bucket: "hort")
  |> range(start: -7d)
  |> filter(fn: (r) => r._measurement == "temperatura")
  |> aggregateWindow(every: 1h, fn: mean, createEmpty: false)
  |> yield(name: "temperatura")
```

Tipus: **Time series**, color blau, eix Y en graus.

### Humitat actual

```flux
from(bucket: "hort")
  |> range(start: -1h)
  |> filter(fn: (r) => r._measurement == "humitat")
  |> last()
```

Tipus: **Stat** (gran), color verd.

### Mitjana per dia

```flux
from(bucket: "hort")
  |> range(start: -30d)
  |> filter(fn: (r) => r._measurement == "temperatura")
  |> aggregateWindow(every: 1d, fn: mean, createEmpty: false)
```

Tipus: **Bar chart**.

### Mapa de calor (dies x hores)

Tipus: **Heatmap**. Eix X: hora del dia. Eix Y: dia.

## Alertes

Les **alertes** permeten rebre avisos quan alguna dada surt dels limits:

1. Ves a un panell existent.
2. **Edit > Alert > Create alert rule**.
3. Defineix:
   - Condicio: `temperatura < 5` (per sota de 5 graus).
   - Avaluacio cada: `1m`.
   - Durant: `5m` (avisar nomes si persisteix 5 min).
4. Configura el **contact point**: correu, Telegram, Slack, webhook.
5. Guarda.

Al BernatLab tinc configurades alertes per:
- Temperatura hivernacle < 2°C (risc de gelades).
- Humitat sol < 20% (sequera).
- Nivell del diposit < 10% (cal regar urgent).
- Servidor caigut (pings cada 30s).

## Variables i plantilles

Les **variables** permeten fer dashboards dinamics:

- `$sensor`: llista de sensors disponibles. Permet canviar quin sensor es mostra amb un desplegable.
- `$interval`: granularitat temporal (1m, 5m, 1h).

Exemple d'una consulta amb variable:

```flux
from(bucket: "hort")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) => r._measurement == "temperatura")
  |> filter(fn: (r) => r.sensor == "$sensor")
  |> aggregateWindow(every: $interval, fn: mean, createEmpty: false)
```

Aixo fa que el dashboard sigui **interactiu**: pots triar quin sensor vols veure.

## Bones practiques

1. **Organitza els dashboards per tema**: un dashboard per temperatura, un altre per humitat, un per l'estat del sistema.
2. **Usa variables**: facilita l'analisi i la reutilitzacio.
3. **Configura alertes per coses critiques**: no esperis a mirar per descobrir que alguna cosa va malament.
4. **Documenta els dashboards**: posa noms clars, descripcions, i un README.
5. **Exporta regularment**: pots exportar un dashboard com a JSON i fer-ne backup.
6. **Limita el rang temporal per defecte**: no carreguis 5 anys per defecte, posa "ultimes 24h".
7. **Fes servir plantilles oficials**: Grafana te plantilles per a casos comuns (servidors, Docker, IoT).

## Alternatives a Grafana

- **Metabase**: mes facil d'usar per a no tecnics, pero menys potent per series temporals.
- **Apache Superset**: mes orientat a BI empresarial.
- **Chronograf**: la UI oficial d'InfluxDB, pero limitada.
- **Power BI / Tableau**: comercials, cars.

Per a un homelab, **Grafana es imbatible**: open source, gratuit, potent, i amb una gran comunitat.

## Connexions amb altres capítols

- **Cap 1** — Les dades son utils quan es poden veure.
- **Cap 6** — InfluxDB es la font de dades mes comuna per a Grafana.
- **Cap 5** — Tambe es pot connectar a PostgreSQL.
- **Cap 7** — Els dashboards es poden desar com a JSON a `/home/pi/bernatlab/grafana/`.
