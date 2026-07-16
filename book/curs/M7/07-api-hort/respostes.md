# Respostes - Capitol 7: API REST per a l'Hort Osona

> Mira les respostes DESPRES d'haver fet el qüestionari.

## Pregunta 1: Que vol dir REST?

**Resposta correcta**: Representational State Transfer.

**Explicacio**: REST es un estil d'arquitectura definit per Roy Fielding l'any 2000. Es basa en recursos identificats per URLs, verbs HTTP estandard (GET, POST, PUT, DELETE), respostes en JSON, i ser sense estat (stateless). No es un protocol ni un estandard formal, pero es un patro àmpliament adoptat.

---

## Pregunta 2: Framework triat?

**Resposta correcta**: Flask.

**Explicacio**: Flask es minimalista, escrit en Python, i ideal per a APIs petites amb 5-20 endpoints. Es el que usa l'Hort Osona per la seva senzillesa. Alternativa: FastAPI (mes modern) o Django (mes complet pero overkill).

---

## Pregunta 3: Verb per obtenir lectura?

**Resposta correcta**: GET.

**Explicacio**: GET es el verb HTTP per obtenir recursos. No modifica res al servidor (idempotent). Es el correcte per obtenir lectures, llistes, historics. POST s'usa per crear, PUT per actualitzar, DELETE per esborrar.

---

## Pregunta 4: Que es CORS?

**Resposta correcta**: Mecanisme de seguretat del navegador per a peticions entre origens diferents.

**Explicacio**: CORS (Cross-Origin Resource Sharing) es una politica del navegador que bloqueja peticions HTTP des d'un origen (domini) a un altre. Si la PWA esta a github.io i l'API a la teva RPi, el navegador bloqueja la peticio si l'API no envia el header `Access-Control-Allow-Origin` correcte. Es una mesura de seguretat contra CSRF.

---

## Pregunta 5: Header per API key?

**Resposta correcta**: X-API-Key.

**Explicacio**: A l'Hort Osona usem el header personalitzat `X-API-Key`. Alternatives: `Authorization: Bearer <token>` (mes estandard) o cookies. Tots funcionen, pero `X-API-Key` es simple i facil de depurar amb curl. Important: NO posis l'API key al URL (queda als logs).

---

## Pregunta 6: Avantatge de FastAPI?

**Resposta correcta**: Te type hints, validacio automatica i OpenAPI.

**Explicacio**: FastAPI es mes modern que Flask. Usa type hints de Python per validar les dades d'entrada, genera OpenAPI/Swagger automaticament, i te WebSockets integrats. Es mes potent pero tambe mes complex. Per a una API petita com l'Hort Osona, Flask es perfecte.

---

## Pregunta 7: Que vol dir "stateless"?

**Resposta correcta**: Cada peticio conte tota la informacio i el servidor no recorda res.

**Explicacio**: En una API REST, el servidor no guarda l'estat de la sessio. Cada peticio es independent i conte tota la info necessaria (autenticacio, parametres, etc.). Es el que permet escalar horitzontalment: qualsevol instancia del servidor pot respondre qualsevol peticio. El contrari (stateful) es el que fan les WebSockets o les aplicacions tradicionals amb sessions PHP.

---

## Pregunta 8: Port de Flask?

**Resposta correcta**: 5000.

**Explicacio**: Flask per defecte escolta al port 5000. Es pot canviar amb `app.run(port=8080)`. En produccio, normalment es posa Gunicorn o uWSGI al davant que escolta al 8000 o 5000, i un nginx com a proxy invers al 80/443.

---

## Pregunta 9 (oberta): Per que Flask

**Resposta model**:

Triem **Flask** per l'API de l'Hort Osona per tres raons principals:

**Mida del projecte**: l'API te uns 15 endpoints organitzats en 4 recursos (sensors, sectors, calendar, alerts). Es una API petita que no justifica un framework pesat. Flask te el minim necessari i res mes.

**Experiencia de l'equip**: Flask es un dels frameworks Python mes estesos i hi ha molta documentacio, tutorials i exemples. Tothom que hagi fet Python web l'ha usat. Això redueix el temps d'aprenentatge.

**Ecosistema**: Flask te extensions per a tot el que necessitem: `flask-cors` per CORS, `flask-restful` per estructurar millor els recursos, `flask-jwt-extended` per JWT, `flask-limiter` per rate limiting, etc. L'ecosistema es madur.

**Comparacio amb alternatives**:

- **Django REST Framework**: excel·lent per a projectes grans amb admin, ORM, autenticacio, etc. Pero per a una API de 15 endpoints, es **overkill**. El codi de Django es 5-10x mes que el de Flask per la mateixa funcionalitat, i el deploy es mes pesat.

- **FastAPI**: mes modern que Flask, amb type hints i OpenAPI automatic. Ideal si comences de zero avui. Pero el nostre equip ja coneix Flask i els beneficis de FastAPI (validacio automatica) no compensen la corba d'aprenentatge per a una API tan petita.

- **Bottle**: encara mes minimalista que Flask (un sol fitxer). Per a APIs molt petites (<5 endpoints) va be. Per a 15 endpoints, comença a fer-se embolic.

**Inconvenients de Flask**: menys validacio automatica que FastAPI (cal fer-la a ma amb `marshmallow` o `pydantic`), menys OpenAPI automatic, i cal mes codi boilerplate. Pero per a la nostra mida, es perfecte.

---

## Pregunta 10 (oberta): CORS amb PWA i API en origins diferents

**Resposta model**:

**El problema**: quan la PWA a `https://hort-osona.github.io` intenta fer una peticio `fetch()` a `http://la-meva-rpi:5000/api/v1/...`, el navegador **bloqueja la peticio** per CORS. La consola del navegador mostra:

```
Access to fetch at 'http://la-meva-rpi:5000/...' from origin 'https://hort-osona.github.io'
has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present
on the requested resource.
```

Aixo es perque el navegador, per defecte, nomes permet peticions al **mateix origen** (mateix protocol, domini i port). Es una mesura de seguretat.

**La solucio amb flask-cors**:

```python
from flask_cors import CORS

# Permetre tots els origens (per desenvolupament)
CORS(app)

# Permetre origens especifics (produccio)
CORS(app, origins=["https://hort-osona.github.io", "http://localhost:*"])
```

`flask-cors` intercepta les peticions i afegeix el header `Access-Control-Allow-Origin` automaticament. Aixo indica al navegador que la API accepta peticions des d'aquell origen.

**Detalls importants**:

1. **Preflight requests**: per a peticions POST/PUT amb headers personalitzats (com `X-API-Key`), el navegador primer envia una peticio OPTIONS per preguntar "puc?". `flask-cors` les gestiona.

2. **Whitelist estricte**: en produccio, mai facis `CORS(app)` (que permet TOTS els origens). Usa una whitelist: `CORS(app, origins=["https://hort-osona.github.io"])`. Si tens multiples subdominis, pots fer `origins=["https://*.github.io"]`.

3. **Credencials**: si necessites enviar cookies, has de fer `CORS(app, supports_credentials=True)` i l'origen ha de ser explicit (no `*`).

4. **Alternatives a CORS**: si tens control del DNS, pots fer que la PWA i l'API estiguin al **mateix origen** (e.g. un proxy invers que serveixi la PWA desde la RPi mateixa). Aixo evita CORS totalment pero perd la gràcia de GitHub Pages.

A l'Hort Osona, la PWA esta a GitHub Pages i l'API a la RPi. Usem `flask-cors` amb una whitelist estricta. Tambe podem fer proxy invertit amb nginx a la RPi, que exposa `/api/` i redirigeix a Flask: aixi la PWA truca a `https://la-meva-rpi/api/...` i nomes hi ha un origen. Es la solucio mes neta per a produccio.

---

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum, sobretot la part de CORS.
- **3-4 encerts**: Repassar la diferencia entre GET/POST/PUT/DELETE.
- **0-2 encerts**: Comencem pel basic: que es una API HTTP i que es JSON.

## Que fer si has encertat totes

- Passa al **Capitol 8** (PWA amb GitHub Pages).
- Investiga GraphQL com a alternativa a REST.
- Compara OpenAPI vs GraphQL vs gRPC per a APIs IoT.
- Prova a fer WebSockets amb Flask-SocketIO per actualitzar la UI en temps real.
- Llegeix sobre autenticacio OAuth2 per a APIs publiques.
