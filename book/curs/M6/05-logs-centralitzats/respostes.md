# Respostes - Capitol 5: Logs centralitzats

> Mira les respostes DESPRES d'haver fet el qüestionari.

## Pregunta 1: Que es un log

**Resposta correcta**: Una linia de text amb timestamp i missatge.

**Explicacio**: Un log es la unitat minima d'informacio. Pot ser tan simple com "el sistema ha arrencat" o tan complexe com un JSON amb camps anidats. El important es que te un instant de temps (per poder-lo ordenar) i un missatge lliure (per poder buscar). Els serveis professionals estructuren els logs en JSON perque sigui mes facil de parsejar.

---

## Pregunta 2: Servei de logs del sistema

**Resposta correcta**: journald (systemd-journald).

**Explicacio**: systemd-journald (sovint dit nomes journald) es el dimoni que recull tots els logs del sistema a distribucions modernes amb systemd (com Raspberry Pi OS). Substitueix el tradicional `syslog` i desa els logs en format binari optimitzat per consultes. Es pot accedir amb `journalctl`.

---

## Pregunta 3: Comanda per veure logs Docker

**Resposta correcta**: `docker logs`.

**Explicacio**: `docker logs NOM_CONTENIDOR` mostra els logs stdout/stderr del contenidor. Opcions utils: `--tail N` (ultimes N linies), `-f` (follow, com tail -f), `--since` (des de quan), `--until` (fins quan). Aixo es mes rapid que entrar dins el contenidor.

---

## Pregunta 4: Equivalent a Prometheus per logs

**Resposta correcta**: Loki.

**Explicacio**: Loki ve del mateix equip que Grafana i esta dissenyat per ser el "company" de Prometheus: metricas a Prometheus, logs a Loki, traces a Tempo, tot visualitzat a Grafana. La gràcia de Loki es que NO indexa el text (aixo el fa rapid i lleuger) sino nomes els labels.

---

## Pregunta 5: Agent per enviar logs a Loki

**Resposta correcta**: Promtail.

**Explicacio**: Promtail es l'agent oficial de Loki. Llegeix fitxers de log, journald, o altres fonts, etiqueta les linies amb labels, i les envia a Loki. Es lleuger i fàcil de configurar. Alternativament hi ha Fluentd, Fluentbit i altres.

---

## Pregunta 6: Llenguatge de Loki

**Resposta correcta**: LogQL.

**Explicacio**: LogQL es mes simple que PromQL. Esta dissenyat per filtres de text (|=, !=, |~) mes que per operacions matematiques complexes. Per a coses basiques (filtrar per text, per labels, per periode) es perfecte. Per a agregacions tambe te funcions com `count_over_time`, `rate`, etc.

---

## Pregunta 7: Operador "conté el text"

**Resposta correcta**: `|=`.

**Explicacio**: A LogQL: `|=` es "conté el text" (case-insensitive), `!=` es "no conté", `|~` es regex. La diferencia amb PromQL es que aqui els filtres operen sobre el contingut del missatge, no sobre el valor numeric.

---

## Pregunta 8: Eina de rotacio

**Resposta correcta**: logrotate.

**Explicacio**: logrotate es una eina de Linux que rota fitxers de log: els comprimeix, els guarda N dies, i els reanomena. Ve pre-instal·lada a gairebe totes les distribucions. La seva limitacio es que no enten journald (aquest te la seva propia gestio de retencio).

---

## Pregunta 9 (oberta): Tres opcions de stack de logs

**Resposta model**:

Les tres opcions que hem vist son:

1. **Només journald** (la mes simple). El sistema ja recull els logs a `/var/log/journal/`. Pots consultar-los amb `journalctl` per terminal. Es perfecte si tens 2-3 serveis i no necessites buscar gaire. La limitacio es que no te UI web i les consultes avancades son complicades. Per a una RPi minima, pot ser suficient.

2. **Grafana Loki + Promtail** (la meva recomanacio). Loki es el magatzem de logs i Promtail es l'agent que els hi envia. Es open source, gratuit, i esta dissenyat per ser lleuger. La gràcia es que ja tens Grafana instal·lat (cap 3), nomes cal afegir un data source. Loki nomes indexa els labels (no el text), cosa que el fa 10x mes rapid i menys exigent en disc que Elasticsearch. Es la opcio "modular" que creix amb tu.

3. **ELK Stack** (Elasticsearch + Logstash + Kibana, la mes completa pero pesada). Es l'estandard industrial i te funcionalitats molt potents (cerca de text complert, agregacions complexes, ML). Pero Elasticsearch sol necessita 2-4 GB de RAM nomes per arrencar, Logstash es complicat de configurar, i Kibana te mil opcions. A una RPi amb 4-8 GB de RAM total, dedicarli 3-4 GB nomes al stack de logs es massa.

Per que **Loki es la millor opcio per al BernatLab**:
- **Recursos**: Loki consumeix uns 100-200 MB de RAM, Promtail uns 30 MB. ELK en consumeix 10-20x mes.
- **Integracio amb el que ja tens**: Grafana ja el tens instal·lat. Loki ve del mateix equip.
- **Cost zero**: tant Loki com Promtail son open source purs.
- **Aprenentatge suau**: LogQL es similar a PromQL que ja coneixes.
- **Escala amb tu**: si passes de 5 serveis a 50, Loki continua funcionant be. Si passes de 50 a 500, potser cal ELK, pero per una RPi mai arribaras a 50 serveis.
- **Retencio configurable**: pots guardar 7 dies o 90 dies canviant un parametre.

L'unic inconvenient real de Loki respecte ELK es que la cerca de text complert es mes basica. Pero per fer coses tipus "troba tots els errors de HA" o "comptador d'errors per hora" es perfecte.

---

## Pregunta 10 (oberta): Investigar un error a HA

**Resposta model**:

Per investigar per que el contenidor de Home Assistant falla, faria servir Loki + Grafana amb el seguent flux de treball:

**Pas 1: Detectar que hi ha un problema**
- Rebo una alerta a Telegram: "ContenidorCaigut homeassistant" (la regla del cap 4).
- O be ho veig al panell "Contenidors actius" del dashboard de Grafana on apareix "Down".

**Pas 2: Anar a Loki amb la cerca inicial**
- A Grafana -> "Explore" -> triar Loki.
- Consulta inicial: `{container="homeassistant"}` per veure TOTS els logs del contenidor.
- Ajustar el periode temporal a "Last 1 hour" o "Last 6 hours".

**Pas 3: Filtrar per errors**
- Afegir el filtre d'errors: `{container="homeassistant"} |= "error"`
- Si hi ha pocs resultats, ampliar amb: `{container="homeassistant"} |= "ERROR"`
- Per warnings tambe: `{container="homeassistant"} |~ "error|warning|fail"`

**Pas 4: Cercar patrons específics**
Si sospito que es un problema de memoria:
```logql
{container="homeassistant"} |~ "memory|OOM|killed"
```
Si sospito que es un problema de xarxa:
```logql
{container="homeassistant"} |= "connection" |= "refused"
```
Si es un tema de la base de dades:
```logql
{container="homeassistant"} |= "database" |= "error"
```

**Pas 5: Correlacionar amb metricas**
- Obrir una nova pestanya d'Explore amb Prometheus.
- Veure la memoria del contenidor: `container_memory_usage_bytes{name="homeassistant"}`
- Veure la CPU: `rate(container_cpu_usage_seconds_total{name="homeassistant"}[5m])`
- Si la memoria va pujant en les ultimes hores, es una fuita.
- Si la CPU es manté alta, pot ser un bucle.

**Pas 6: Buscar l'error especific**
Un cop identificada la finestra temporal i el patro, restringir la cerca:
```logql
{container="homeassistant"} |= "Traceback" |= "2026-05-12T14:3"
```
(amb el periode ajustat a 5 minuts abans i despres de la caiguda)

**Pas 7: Guardar la consulta**
- Un cop trobada l'arrel del problema, guardar la consulta com a "Query" favorita a Grafana.
- Si es un error recurrent, crear una alerta Loki: avisar si surt "Error X" mes de N cops per hora.
- Documentar-ho al runbook (cap 10 d'aquest modul) per tenir-ho a ma la propera vegada.

Exemple real: si veig que HA falla cada 3-4 dies i el log mostra `MemoryError: Out of memory`, la causa es una fuita de memoria. Solucio: limit de memoria al docker-compose + reinici programat, o reportar el bug al projecte HA.

---

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum i fer l'exercici practic.
- **3-4 encerts**: Refes l'exercici desde zero observant cada pas.
- **0-2 encerts**: Repassem junts el capitol abans de continuar.

## Que fer si has encertat totes

- Passa al **Capitol 6** (Uptime i disponibilitat).
- Investiga Grafana Tempo per traces distribuits.
- Prova a configurar el plugin de Loki per a Prometheus alerting.
