# Respostes — Capitol 10: Visualitzacio amb Grafana

> Mira les respostes DESPRES d'haver fet el qüestionari.

## Pregunta 1: Port per defecte de Grafana

**Resposta correcta**: 3000.

**Explicacio**: Grafana escolta al port **3000** per defecte. Es pot canviar, pero 3000 es el port estandard. Al BernatLab l'he mapeig a `127.0.0.1:3000` per seguretat (nomes accesible via Tailscale o tunel SSH). Si vols accedir desde qualsevol lloc, hauras de posar un reverse proxy amb HTTPS (Caddy o Nginx).

---

## Pregunta 2: Llenguatge amb InfluxDB 2

**Resposta correcta**: Flux.

**Explicacio**: **Flux** es el llenguatge de consultes d'InfluxDB 2 (i per extensio, de Grafana quan es connecta a InfluxDB 2). Es funcional i orientat a series temporals, amb pipes `|>`. InfluxQL es el llenguatge antic (v1) que esta deprecated. Si tens InfluxDB 1, Grafana tambe el soporta, pero has de triar InfluxQL a la configuracio.

---

## Pregunta 3: Tipus de grafic per a series temporals

**Resposta correcta**: Time series (linia).

**Explicacio**: El **Time series** (linia) es el tipus mes natural per visualitzar series temporals: mostra l'evolucio d'una variable al llarg del temps. Es perfecte per veure tendencies, pics, vall, periodicitat. Altres tipus com Bar chart son millors per a categories, Pie chart per a composicio, Heatmap per a patrons 2D.

---

## Pregunta 4: Que es un dashboard?

**Resposta correcta**: Una coleccio de panells (grafics).

**Explicacio**: Un **dashboard** a Grafana es una pagina web que conte multiples **panells** (grafics) organitzats. Cada panell te la seva font de dades, consulta, i configuracio visual. Pots organitzar els panells en files i columnes, moure'ls, copiar'ls, i compartir el dashboard sencer amb un enllaç.

---

## Pregunta 5: Grafic per a la humitat actual

**Resposta correcta**: Stat (Big number).

**Explicacio**: El tipus **Stat** (o **Big number**) mostra un sol valor prominent amb estils opcionals. Es perfecte per mostrar l'ultima lectura d'un sensor ("65% humitat"). Time series mostraria una linia, pero si nomes vols el valor actual, Stat es mes clar i directe. Tambe es pot afegir un Sparkline (mini-grafic) al costat per veure la tendencia.

---

## Pregunta 6: Que es una alerta?

**Resposta correcta**: Un avis automatic quan una dada surt dels limits.

**Explicacio**: Una **alerta** (alert rule) a Grafana es una regla que s'avalua periodicament. Si la condicio es compleix (per exemple, "temperatura < 2°C durant 5 minuts"), s'envia un **avís** (notification) al contact point configurat (correu, Telegram, Slack, webhook). Es ideal per coses critiques: gelades, servidor caigut, nivell d'aigua baix, etc.

---

## Pregunta 7: Fonts de dades de Grafana

**Resposta correcta**: Multiples: InfluxDB, Prometheus, PostgreSQL, MySQL, Loki, etc.

**Explicacio**: Grafana es **agnostica** a la font de dades. Pot connectar-se a mes de 30 fonts diferents: InfluxDB, Prometheus, PostgreSQL, MySQL, Elasticsearch, Loki (logs), CloudWatch, Azure Monitor, etc. Aixi pots tenir un sol dashboard amb dades de moltes fonts. Per a series temporals, InfluxDB i Prometheus son les mes populars.

---

## Pregunta 8: Que es una variable?

**Resposta correcta**: Un parametre dinamic que es pot canviar desde la UI.

**Explicacio**: Una **variable** a Grafana es un parametre que l'usuari pot canviar desde la UI del dashboard. Per exemple, `$sensor` pot ser una llista de tots els sensors disponibles, i l'usuari pot triar quin vol veure amb un desplegable. Aixi un sol dashboard pot mostrar dades de multiples sensors. Altres variables utils: `$interval` (granularitat temporal), `$host` (quina maquina), etc.

---

## Pregunta 9 (oberta): Grafana vs UI InfluxDB

**Resposta model**:

Veure les dades directament a la UI d'InfluxDB es valid per a tasques tecniques (inspeccionar una consulta, exportar dades), pero per a un **pages que vol veure la temperatura del seu hivernacle cada mati**, Grafana es molt millor per varies raons:

**1. Visualitzacio molt mes clara**: un grafic de linia es molt mes rapid d'entendre que una taula amb 1000 files. El pages veu immediatament: "ah, ahir a les 6 del mati la temperatura va baixar a 3 graus, pero despres va pujar". Amb una taula, hauria de fer scroll i calculs mentals.

**2. Multiples grafics en una sola pagina**: a Grafana pots tenir 10 panells en un sol dashboard, organitzats. A InfluxDB has d'anar consultant una serie temporal a la vegada.

**3. Personalitzacio**: el pages pot triar colors, mides, eixos. Fins i tot pot posar un fons amb foto del seu hort.

**4. Alertes automatiques**: a Grafana pots dir "avisame per Telegram si la temperatura baixa de 2°C". A InfluxDB no hi ha sistema d'alertes (cal afegir un altre servei).

**5. Compartir facil**: pots generar un enllaç public per compartir el dashboard amb un tecnic, o amb un ve que t'ajuda amb l'hort.

**6. Vista per a no tecnics**: la UI d'InfluxDB es per enginyers. Grafana es per qualsevol.

**Limitacio**: Grafana nomes es util si tens **dades per visualitzar**. Si nomes tens una sola taula amb 5 files, no cal Grafana. Pero quan tens anys de lectures de 10 sensors, es indispensable.

**Conclusio**: Grafana es la **cara** del teu homelab. Es el que veus quan obres la pestanya del matí. Si nomes tens dades pero no les visualitzes, es com tenir un hort pero no mirar-lo mai.

---

## Pregunta 10 (oberta): Dashboard complet per a l'hort

**Resposta model**:

Dissenya un dashboard amb aquests **5 panells**:

**1. Temperatura actual (panell superior, gran)**
- Tipus: **Stat** (gran, amb sparkline)
- Consulta: `last(temperatura)` dels darrers 5 min
- Color: blau (fred) si < 5, groc si 5-25, vermell si > 35
- Justificacio: el mes important. El pages vol saber immediatament la temperatura actual.

**2. Temperatura ultimes 24h (grafic de linia)**
- Tipus: **Time series**
- Consulta: agregat per 5 min, ultimes 24h
- Eix Y: 0-40°C
- Justificacio: veure la tendencia diaria. A quines hores ha fet mes calor? Hi ha hagut cap pic?

**3. Humitat del sol (Gauge)**
- Tipus: **Gauge**
- Consulta: `last(humitat_sol)`
- Llindars: 0-30 (sec, vermell), 30-60 (normal, verd), 60-100 (humit, blau)
- Justificacio: l'humitat del sol es critica. Si baixa de 30, cal regar.

**4. Nivell d'aigua del diposit (Stat)**
- Tipus: **Stat**
- Consulta: `last(nivell_diposit)`
- Color: vermell si < 10%, groc si 10-30%, verd si > 30%
- Justificacio: si el diposit es buida, el reg automatic falla. Cal avisar abans.

**5. Mapa de calor (dies x hores)**
- Tipus: **Heatmap**
- Consulta: temperatura agregada per hora
- Eix X: hora del dia (0-23)
- Eix Y: dia de la setmana (dilluns a diumenge)
- Justificacio: veure patrons setmanals. A quines hores fa mes calor? Hi ha algun dia especialment problematic?

**Alertes associades**:
- Temperatura < 2°C durant 5 min -> avis (risc de gelada)
- Humitat sol < 20% durant 30 min -> avis (sequera)
- Nivell diposit < 10% -> avis (cal omplir)

**Organitzacio del dashboard**:
- Fila 1: Temperatura actual (gran) + Humitat sol + Nivell diposit (3 stats petits)
- Fila 2: Temperatura 24h (ample complet)
- Fila 3: Heatmap (ample complet)

**Configuracio adicional**:
- Auto-refresh: cada 30 segons
- Time range per defecte: ultimes 24h
- Tema: fosc (millor per a una pantalla sempre encesa)
- Titol: "Hort IoT BernatLab"

**Resultat**: un cop guardat, tens una "finestra" al teu hort que pots obrir cada mati amb un clic. En 10 segons saps l'estat general, i tens les dades historiques per anar mes profund si cal.

---

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum, sobretot la seccio de configuracio d'InfluxDB.
- **3-4 encerts**: Rellegeix el capitol amb atencio. Practica consultant la documentacio de Grafana.
- **0-2 encerts**: Repassem junts el capitol. Es la part mes visual i potent del BernatLab.

## Que fer si has encertat totes

- **Felicitats!** Has completat el Modul 3 (Dades) del curs.
- Repassa els 10 capitols i fes una **revisio general** dels conceptes.
- Comença a **aplicar** el que has après: instal·la els serveis productius, fes els teus propis dashboards, configura les teves alertes.
- Considera fer el **quiz final** del modul per consolidar.
