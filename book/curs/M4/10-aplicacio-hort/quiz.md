# Qüestionari - Capitol 10: Aplicacio a Hort Osona

> 15 preguntes · ~20 min · 7 test + 8 obertes

## Pregunta 1
Quants documents te actualment la base de coneixement de l'Hort Osona?

- [ ] Uns 10
- [ ] Uns 30
- [x] Uns 80+
- [ ] Mes de 1000

## Pregunta 2
Quin dels seguents NO es un component de l'arquitectura final del sistema d'IA a l'Hort Osona?

- [ ] Open WebUI
- [ ] Ollama
- [ ] ChromaDB
- [x] Slack

## Pregunta 3
Quin es el model d'embeddings recomanat per a indexar els documents de l'Hort Osona?

- [ ] Llama 3.2
- [x] nomic-embed-text
- [ ] Phi-3
- [ ] CodeLlama

## Pregunta 4
Com es pot accedir al sistema d'IA de l'Hort Osona des de fora de la xarxa local?

- [ ] Port 11434 obert al router
- [x] Tailscale
- [ ] DNS public
- [ ] No es pot accedir

## Pregunta 5
Quin es el primer pas per muntar el sistema d'IA a l'Hort Osona?

- [ ] Descarregar el model
- [x] Clonar el repositori hort-osona amb la documentacio
- [ ] Configurar ChromaDB
- [ ] Instal·lar Open WebUI

## Pregunta 6
Quin avantatge te indexar els 80+ documents en un sol cop vs incrementalment?

- [ ] Es mes rapid
- [x] Es mes simple de configurar al principi
- [ ] Dona millors resultats
- [ ] Ocupa menys espai

## Pregunta 7
Quin script s'encarrega d'indexar els documents?

- [ ] open_webui.py
- [x] indexar_hort.py
- [ ] ollama_run.py
- [ ] chroma_admin.py

## Pregunta 8 (oberta)
Explica amb les teves paraules: per que la base de coneixement de l'Hort Osona es un cas d'us ideal per al RAG amb Ollama? Quines caracteristiques la fan especialment adequada?

Pistes per respondre:
- Documentacio especifica que cap model general coneix.
- Preguntes recurrents sobre cultius locals.
- Privadesa: la gent no voldria enviar les seves dades d'hort al nuvol.
- Cas d'us practic: tenir un assistent especialitzat.

## Pregunta 9 (oberta)
Imagina que un usuari pregunta al sistema: "tinc plagues de pugons als tomàquets, que puc fer?". Segueix mentalment el flux RAG: que passa des de la pregunta fins a la resposta?

Pistes per respondre:
- Pas 1: la pregunta es converteix en embedding.
- Pas 2: es busquen els 3-5 chunks mes semblants.
- Pas 3: es prepara el prompt amb el contexte.
- Pas 4: el LLM genera la resposta.
- Que tipus de chunks es trobarien? (plagues, tractaments, tomàquets).

## Pregunta 10 (oberta)
Quina relacio hi ha entre la qualitat de les respostes del sistema i la qualitat dels documents indexats? Com afectaria afegir un document mal escrit o incomplet?

Pistes per respondre:
- Si els documents son bons, les respostes son bones.
- Si els documents son dolents, el sistema pot donar informacio incorrecta.
- Cal curació dels documents abans d'indexar.
- Aplica a l'Hort Osona: quins documents son critic revisar?

## Pregunta 11 (oberta)
Com evaluaries si el sistema d'IA de l'Hort Osona es prou bo per a l'us que se li vol donar? Inventa 5 preguntes representatives amb les respostes esperades.

Pistes per respondre:
- Pregunta 1: "Quan plantar tomàquets?" -> abril-maig.
- Pregunta 2: "Com es el reg dels enciams?" -> diari pero sense entollar.
- Pregunta 3: "Quin sensor..." -> DS18B20.
- Pregunta 4: "Quan collir..." -> juliol-octubre.
- Pregunta 5: ... (inventada).

## Pregunta 12 (oberta)
Quines consequencies te afegir mes documents al sistema? Fins a quin punt es pot escalar abans que el rendiment baixi?

Pistes per respondre:
- Mes documents = mes chunks = mes embeddings.
- Mes chunks = mes calculs en cada cerca.
- ChromaDB escala be fins a 100k chunks.
- Si l'Hort Osona creix a 500-1000 documents, podria ser problematic.
- Com ho gestionaries?

## Pregunta 13 (oberta)
Argumenta: prefereixes un sistema d'IA nomes per a l'Hort Osona, o un sistema que tambe integri dades en temps real (sensors, calendaris)?

Pistes per respondre:
- Avantatges del nomes documents: simple, robust, offline.
- Avantatges d'integrar dades: respostes personalitzades, context actual.
- Limitacions: complexitat, fragilitat, necessitat de xarxa.
- Tria final: defensa-la amb un cas concret.

## Pregunta 14 (oberta)
Quin impacte te el sistema d'IA en l'aprenentatge de l'hort per part de l'usuari? Pot substituir l'experiencia humana o nomes complementar-la?

Pistes per respondre:
- El sistema pot recordar mes dades que una persona.
- Pero no pot observar el context fisic (el color de les fulles, l'olor del sol).
- L'experiencia es irremplacable.
- El sistema es un "consultor savi", no un substitut del pagès.

## Pregunta 15 (oberta)
Imagina que l'Hort Osona vol comercialitzar aquest sistema per a altres pagesos. Quines adaptacions caldria fer? Quin model de negoci tindria sentit?

Pistes per respondre:
- Adaptacions: multi-tenant, autenticacio, configuracio per hort, mes dades.
- Model de negoci: SaaS amb quota mensual, o venta del sistema + suport.
- Consideracions: privadesa, costs, competencia, escala.
- Viabilitat: es un mercat interessant? Quants pagesos hi ha?
