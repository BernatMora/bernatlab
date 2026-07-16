# Respostes - Capitol 2: Prometheus

> Mira les respostes DESPRES d'haver fet el qüestionari.

## Pregunta 1: Que es una metrica?

**Resposta correcta**: Un valor numeric amb marca de temps i opcionalment labels.

**Explicacio**: Una metrica Prometheus te tres parts: un valor (42.5), un instant de temps (1716000000) i opcionalment uns labels (`{host="rpi", core="0"}`). Els labels son com "tags" que permeten filtrar i agrupar. Sense labels, no podries distingir la CPU del core 0 de la del core 1.

---

## Pregunta 2: Model d'arquetip

**Resposta correcta**: Pull: Prometheus va a buscar-les periòdicament.

**Explicacio**: Pull vol dir que Prometheus es el que truca al servei. El servei nomes ha d'exposar un endpoint HTTP. Es diferent del model push (com InfluxDB en alguns modes) on el servei envia les dades. Pull te l'avantatge que saps exactament quins serveis monitors i si un falla es veu rapid (deixa de respondre). En canvi, amb push, un servei podria deixar d'enviar i tu no te per que saber que existeix.

---

## Pregunta 3: Que es un exporter?

**Resposta correcta**: Un programa que converteix l'estat d'un servei en metricas Prometheus.

**Explicacio**: Els serveis normals no exposen metricas en format Prometheus. Els exporters son "adaptadors" que llegeixen l'estat intern (fitxers /proc, APIs del servei, etc.) i ho exposen en format Prometheus a `/metrics`. Per exemple, node_exporter llegeix `/proc/stat`, `/proc/meminfo` etc. i ho tradueix a series temporals.

---

## Pregunta 4: Interval per defecte

**Resposta correcta**: Cada 15 segons.

**Explicacio**: El `scrape_interval` per defecte es 15 segons. Es un bon equilibri entre tenir prou resolucio temporal i no saturar els serveis. A la RPi pots pujar-ho a 30-60 segons si tens molts targets, pero no ho recomano perque perds capacitat de detectar problemes puntuals.

---

## Pregunta 5: Exporter per Docker

**Resposta correcta**: cadvisor.

**Explicacio**: cAdvisor (Container Advisor) es el que Google va crear per extreure metricas de contenidors Docker. Ve amb el seu propi dashboard a port 8080 pero el mes interessant es que exposa les metricas en format Prometheus. Es la millor eina per veure CPU, memoria, xarxa i disc per contenidor.

---

## Pregunta 6: Llenguatge de consultes

**Resposta correcta**: PromQL.

**Explicacio**: PromQL (Prometheus Query Language) es un llenguatge funcional inspirat en part en SQL pero dissenyat especificament per series temporals. Permet funcions com `rate()`, `sum()`, `avg()`, `histogram_quantile()`, etc. La corba d'aprenentatge es suau si ja coneixes funcions agregades.

---

## Pregunta 7: Parametre de mida maxima

**Resposta correcta**: `--storage.tsdb.retention.size`.

**Explicacio**: Hi ha dos parametres de retencio: `--storage.tsdb.retention.time` (per temps) i `--storage.tsdb.retention.size` (per mida). A la RPi es important limitar la mida perque el disc es petit. Pots posar els dos: el que s'assoleixi primer es el que s'aplica.

---

## Pregunta 8: Port per defecte

**Resposta correcta**: 9090.

**Explicacio**: 9090 es el port UI/API de Prometheus. 9100 es node_exporter, 8080 es cAdvisor, 3000 es Grafana. Es bo recordar-los perque a l'hora de configurar firewalls i proxies has de saber quin port serveix quin servei.

---

## Pregunta 9 (oberta): Pull vs Push

**Resposta model**:

El **model pull** es quan el sistema de monitoritzacio (Prometheus) es el que truca periòdicament al servei per demanar-li les dades. El **model push** es al reves: el servei es el que envia les dades al sistema de monitoritzacio.

Prometheus va triar pull per varies raons:

1. **Visibilitat del que monitors**: amb pull, tu controles exactament quins serveis monitors perque els poses a la configuracio. Si un servei deixa d'estar a la llista, no el monitors. Amb push, un servei podria començar a enviar-te dades sense que ho sàpigues.
2. **Deteccio de fallades facil**: si un servei penja, simplement deixa de respondre a Prometheus. La diferencia entre "ultima vegada que vaig rebre dades" i "ara" es la deteccio de la fallada. Amb push, si el servei cau, no reps res pero tambe podries tenir un problema de xarxa.
3. **No cal que el serveixi sàpiga res de Prometheus**: nomes ha d'exposar `/metrics` en format estandard. Es mes facil afegir nous serveis.
4. **Configuracio centralitzada**: tens un unic fitxer `prometheus.yml` que defineix tota la monitoritzacio. Es mes facil d'auditar.

El desavantatge es que serveis darrere de NAT o firewalls son complicats (permetre que Prometheus els pugui trucar). Tambe per a serveis molt volatils (workers que apareixen i desapareixen) push es millor.

Exemple del BernatLab: el **node-exporter** corre a la RPi exposant les metricas del sistema a port 9100. Prometheus cada 15 segons fa `GET http://rpi:9100/metrics` i guarda les dades. Si la RPi es queda sense xarxa, simplement deixa de rebre dades i Prometheus ho detecta automaticament.

---

## Pregunta 10 (oberta): Els 3 exporters

**Resposta model**:

Per la RPi del BernatLab, els 3 exporters essencials serien:

1. **node_exporter** - Es el mes important. Dona metricas de tot el sistema: CPU per core, memoria, swap, disc per particio, lecto-escriptures per segon, trafic de xarxa per interfície, temperatura, càrrega del sistema, uptime. Sense ell, no tens visibilitat de res que passi a la RPi. Es molt lleuger (consumeix molt poc CPU i memoria). Permet detectar problemes com "estic quedant sense memoria", "el disc esta ple" o "la CPU es sobrecàrrega cada matí a les 9".

2. **cadvisor** - Dona metricas dels contenidors Docker. Permet veure l'ús de memoria i CPU de cada contenidor individualment. Al BernatLab tens uns quants contenidors (Home Assistant, InfluxDB, Grafana, nodered) i cAdvisor et permet saber quin esta consumint mes, quin s'ha reiniciat, o quin te fuites de memoria. Es la millor eina per "el meu contenidor de HA esta menjant-se 600 MB de RAM, es normal?". Important: privilegejat i amb acces a /var/lib/docker, sino no pot llegir les metricas.

3. **blackbox_exporter** - Serveix per fer probes externes. En lloc de recollir metricas d'un servei, ell fa peticions (HTTP, TCP, ICMP, DNS) a serveis i et diu si responen, quant triguen, o si fallen. Es ideal per monitorar serveis externs (com una API de meteo que fas servir) o per fer "ping" a serveis interns des de fora (simula un usuari real). Tambe es pot fer servir per validar certificats SSL.

Bonus que podries afegir:
- **nginx_exporter** si tens nginx com a proxy invers (per veure peticions, errors, latencia).
- **process-exporter** per monitorar processos especifics (com un script Python concret).
- **smarthome_exporter** si tens Home Assistant i vols metricas personalitzades.

A la RPi has d'anar amb compte de no posar-ne masses. Cada exporter son mes series temporals i mes CPU. Amb 3-4 exports i uns 5-10 containers estas be. Si passes de 20 targets, considera baixar el `scrape_interval` a 30s.

---

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum i fer l'exercici practic.
- **3-4 encerts**: Refes l'exercici desde zero observant cada pas.
- **0-2 encerts**: Repassem junts el capitol abans de continuar.

## Que fer si has encertat totes

- Passa al **Capitol 3** (Grafana).
- Investiga Grafana Mimir o Cortex per escalabilitat.
- Mira com configurar `recording rules` per a consultes complexes.
