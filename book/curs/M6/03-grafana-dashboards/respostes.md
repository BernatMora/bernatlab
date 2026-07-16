# Respostes - Capitol 3: Grafana i dashboards

> Mira les respostes DESPRES d'haver fet el qüestionari.

## Pregunta 1: Funcio principal de Grafana

**Resposta correcta**: Visualitzar dades de series temporals en dashboards.

**Explicacio**: Grafana es una eina de visualitzacio. No guarda dades per si mateixa (tot i que pot tenir una mica de cache), sino que consulta fonts com Prometheus, InfluxDB, Loki, etc. i presenta les dades de forma amigable. Es la diferencia entre "tenir dades" i "entendre que volen dir".

---

## Pregunta 2: Port per defecte

**Resposta correcta**: 3000.

**Explicacio**: Grafana escolta al port 3000 per defecte. Es un port que la gent recorda facil. Compte amb el conflicte si tens altres serveis com Node-RED (tambe sol usar 3000 - configura un altre).

---

## Pregunta 3: Element basic

**Resposta correcta**: Panell.

**Explicacio**: Un panell (panel) es la unitat minima d'un dashboard. Pot ser un graf de linies, un numero, una taula, un mapa, etc. Els panells s'organitzen en files (rows) dins del dashboard, i pots moure'ls i redimensionar-los.

---

## Pregunta 4: Tipus per a un sol numero

**Resposta correcta**: Stat.

**Explicacio**: El tipus Stat mostra un unic valor numeric gran, amb un titol a sobre. Es perfecte per valors puntuals com "Temperatura actual: 47°C". Si vols el velocimetre amb arc, seria Gauge. Si vols un graf temporal, Time series.

---

## Pregunta 5: Variables

**Resposta correcta**: Parametres que permeten personalitzar les consultes amb un desplegable.

**Explicacio**: Les variables son la funcionalitat que fa Grafana tan util. Defineixes una variable (per exemple "contenidor") que s'omple amb els noms dels teus contenidors. Despres a les consultes PromQL poses `name=~"$contenidor"` i Grafana substituira la variable pel valor triat. Combinat amb "Include All" pots fer un panell que mostri tots o un de concret.

---

## Pregunta 6: Provisioning

**Resposta correcta**: Configurar data sources i dashboards amb fitxers YAML.

**Explicacio**: El provisioning es la manera "GitOps" de gestionar Grafana. En lloc de configurar tot per la UI, poses fitxers YAML a `/etc/grafana/provisioning/`. Grafana els llegeix a l'arrencar i configura tot automaticament. Es ideal quan tens multiples servidors o vols replicar la configuracio.

---

## Pregunta 7: ID dashboard Node Exporter

**Resposta correcta**: 1860.

**Explicacio**: 1860 es el dashboard "Node Exporter Full" de la comunitat. Es molt complet i te centenars de panells organitzats per seccions. Es un bon punt de partida encara que pot ser excessiu per una RPi. 893 es "Docker Container" i 13639 es "Blackbox Exporter".

---

## Pregunta 8: URL correcta dins Docker

**Resposta correcta**: `http://prometheus:9090`.

**Explicacio**: Dins de la xarxa Docker, els serveis es comuniquen pel seu NOM, no per localhost. `prometheus` es el `container_name` que hem definit. Si poses `localhost`, Grafana buscaria un servei al seu propi contenidor, no trobaria res i donaria error. Aixo es diferent quan accedeixes des del navegador: allà si que es localhost del teu PC.

---

## Pregunta 9 (oberta): Variables a Grafana

**Resposta model**:

Les **variables** a Grafana son parametres configurables que permeten canviar el contingut dels panells de forma interactiva. Es defineixen a "Dashboard settings" -> "Variables" i apareixen com a desplegables a la part superior del dashboard.

Tipus de variables:
- **Query**: el valor s'obte d'una consulta a una font de dades. Es la mes comuna.
- **Custom**: llista fixa de valors que tu escrius.
- **Constant**: valor fixe que no es pot canviar.
- **Text box**: l'usuari escriu el valor.
- **Data source**: permet canviar la font de dades al moment.

Exemple concret al BernatLab: tens 4-5 contenidors (Home Assistant, InfluxDB, Prometheus, Grafana, nodered) i vols veure l'ús de memoria de cada un. En lloc de fer 5 panells iguals canviant el nom, crees una variable "contenidor" que tingui tots els noms, i un sol panell amb la consulta:

```promql
container_memory_usage_bytes{name=~"$contenidor"}
```

Ara un desplegable a dalt et permet triar "homeassistant" i veure nomes la seva memoria, o triar "All" i veure'ls tots en un graf.

Avantatges respecte fer un panell per contenidor:
- Un sol panell = una sola consulta a Prometheus = menys carrega.
- Si afegeixes un contenidor nou, nomes cal actualitzar la variable.
- Pots combinar mes d'una variable (per exemple, contenidor + periode de temps).
- Reutilitzable: copies el dashboard a un altre servidor i nomes has de reconfigurar la font de dades.

---

## Pregunta 10 (oberta): Dashboard basic del BernatLab

**Resposta model**:

Un dashboard basic per la RPi del BernatLab hauria de tenir 4-6 panells essentials organitzats en 2 files:

**Fila 1 - Estat del sistema (vista rapida):**

1. **CPU sistema %** (Type: Time series)
   - Consulta: `100 - (avg by(instance)(rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)`
   - Per que: la CPU es el primer indicador de si el sistema esta sobrecarregat. Veure una pujada sobtada et pot indicar un bucle infinit o un atac.

2. **Memoria usada %** (Type: Gauge)
   - Consulta: `(1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100`
   - Per que: una RPi amb 4-8 GB es pot quedar sense memoria rapid si un contenidor te fuites. El gauge et dona una visio instantania amb codi de colors (verd/groc/vermell).

3. **Temperatura CPU** (Type: Stat)
   - Consulta: `node_thermal_zone_temp`
   - Per que: a l'estiu, una RPi sense bona ventilacio pot passar de 80 graus i fer throttling. Aquest numero et permet veure-ho d'una ullada.

**Fila 2 - Espai i serveis:**

4. **Disc lliure (GB)** (Type: Stat amb sparkline)
   - Consulta: `node_filesystem_avail_bytes{mountpoint="/"} / 1024 / 1024 / 1024`
   - Per que: el disc ple es la causa numero 1 de caiguda del sistema. Logs, contenidors, imatges... tot va al disc.

5. **Xarxa (in/out)** (Type: Time series)
   - Consulta: `rate(node_network_receive_bytes_total{device!="lo"}[5m])` i una altra per transmit
   - Per que: pics inusuals poden indicar un atac o un servei que esta fent masses peticions.

6. **Contenidors actius** (Type: Table)
   - Consulta: `container_last_seen{name=~".+"}`
   - Per que: una llista visual de quins serveis estan vius. Si un desapareix, saps rapid quin ha caigut.

Bonus: una **variable "contenidor"** que permeti filtrar els panells 4, 5 i 6 per un sol contenidor. I un **panell d'alertes actives** (a Grafana o integrat d'Alertmanager) per veure quines alertes estan disparades en aquest moment.

L'ordre dels panells segueix la jerarquia "piramide de Maslow" del sistema: primer la supervivencia (CPU, memoria, temperatura), despres els recursos (disc, xarxa), finalment els serveis especifics (contenidors). Es la mateixa logica que posaries a la pantalla inicial d'un cotxe: velocimetre, gasolina, temperatura del motor, i despres la radio.

---

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum i fer l'exercici practic.
- **3-4 encerts**: Refes l'exercici desde zero observant cada pas.
- **0-2 encerts**: Repassem junts el capitol abans de continuar.

## Que fer si has encertat totes

- Passa al **Capitol 4** (Alertes Telegram).
- Investiga Loki per tenir tambe logs centralitzats visualitzables a Grafana.
- Mira com fer alertes basiques des de Grafana directament.
