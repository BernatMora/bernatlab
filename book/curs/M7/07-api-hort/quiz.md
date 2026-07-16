# Qüestionari - Capitol 7: API REST per a l'Hort Osona

> 10 preguntes · ~15 min

## Pregunta 1
Que vol dir REST?

- [ ] Rapid Easy Service Technology
- [x] Representational State Transfer
- [ ] Remote Endpoint Service Type
- [ ] Real-time Event Streaming Transfer

## Pregunta 2
Quin framework Python hem triat per a l'API de l'Hort Osona?

- [ ] Django
- [x] Flask
- [ ] FastAPI
- [ ] Bottle

## Pregunta 3
Quin verb HTTP s'usa per obtenir una lectura d'un sensor?

- [x] GET
- [ ] POST
- [ ] PUT
- [ ] DELETE

## Pregunta 4
Que es CORS?

- [x] Un mecanisme de seguretat del navegador per a peticions entre origens diferents
- [ ] Un protocol de xarxa
- [ ] Un sistema d'autenticacio
- [ ] Un tipus de base de dades

## Pregunta 5
Quin header HTTP fem servir per enviar la clau de l'API?

- [ ] Authorization: Bearer
- [x] X-API-Key
- [ ] API-Token
- [ ] Cookie

## Pregunta 6
Quin es l'avantatge de FastAPI respecte Flask?

- [ ] Es mes lleuger
- [x] Te type hints, validacio automatica i OpenAPI
- [ ] Funciona sense Python
- [ ] Es mes estable

## Pregunta 7
Que vol dir que una API es "stateless"?

- [ ] Que nomes te GET
- [x] Que cada peticio conte tota la informacio necessaria i el servidor no recorda res
- [ ] Que nomes retorna dades
- [ ] Que nomes accepta peticions en text pla

## Pregunta 8
Quin port escolta el servidor Flask per defecte?

- [ ] 80
- [ ] 8080
- [x] 5000
- [ ] 3000

## Pregunta 9 (oberta)
Explica per que triem Flask i no Django o FastAPI per a l'API de l'Hort Osona. Quins avantatges i inconvenients te cada opcio?

Pistes per respondre:
- Flask: minimalista, ideal per a APIs de 5-20 endpoints.
- Django: complet pero overkill, ve amb admin i ORM.
- FastAPI: modern amb type hints, OpenAPI automatic.
- El criteri es: mida del projecte, experiencia de l'equip, ecosistema.

## Pregunta 10 (oberta)
La teva PWA esta a `https://hort-osona.github.io` i l'API a `http://la-meva-rpi:5000`. Explica el problema de CORS i com el soluciones amb `flask-cors`.

Pistes per respondre:
- CORS bloqueja peticions des d'un origen diferent.
- El navegador verifica el header `Access-Control-Allow-Origin`.
- `flask-cors` configura aquest header automaticament.
- Pots limitar els origens permesos (whitelist).
