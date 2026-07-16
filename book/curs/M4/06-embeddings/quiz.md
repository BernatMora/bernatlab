# Qüestionari - Capitol 6: Embeddings

> 10 preguntes · ~15 min

## Pregunta 1

Que es un embedding?

- [ ] Un tipus de LLM
- [x] Un vector numeric que representa el significat d un text
- [ ] Un sistema operatiu
- [ ] Un protocol de xarxa

## Pregunta 2

Quantes dimensions te normalment un embedding modern?

- [ ] 10-50
- [x] 384-1536
- [ ] 10000+
- [ ] Nomes 1

## Pregunta 3

Que mesura la "semblança cosinus"?

- [ ] La distancia geografica entre dues ciutats
- [x] El grau de semblança entre dos vectors (i per tant, entre dos textos)
- [ ] El temps que triga un model a generar text
- [ ] La mida d un fitxer

## Pregunta 4

Quin valor de semblança cosinus indica "molt semblant"?

- [ ] 0.0
- [ ] 0.2
- [x] 0.85
- [ ] -0.5

## Pregunta 5

Quin d'aquests es un model d'embeddings local disponible a Ollama?

- [ ] BERT-base
- [x] nomic-embed-text
- [ ] Stable Diffusion
- [ ] Whisper

## Pregunta 6

Quina llibreria Python es l'estandard per a embeddings locals?

- [ ] requests
- [ ] flask
- [x] sentence-transformers
- [ ] matplotlib

## Pregunta 7

Quantes dimensions te l'embedding del model all-MiniLM-L6-v2?

- [ ] 128
- [x] 384
- [ ] 768
- [ ] 1536

## Pregunta 8

Quin es el "sweet spot" recomanat per a dimensions d'embedding?

- [ ] 50
- [ ] 128
- [x] 768
- [ ] 10000

## Pregunta 9 (oberta)

Per que els embeddings permeten "cercar per significat" en lloc de "cercar per paraules exactes"? Dona un exemple concret amb l'Hort Osona.

Pistes per respondre:
- Explica el mecanisme: vectors propers = significat semblant.
- Pensa en una cerca tradicional: buscar "rega" nomes trobara la paraula "rega".
- Amb embeddings: buscar "com controlo l aigua dels tomàquets" pot trobar un text que parla de "sistema de reg automatic".
- Això es important per a l'Hort Osona: tenim 100 lectures de sensors amb paraules tecniques que l'usuari pot no recordar exactament.

## Pregunta 10 (oberta)

Has d'indexar 10.000 articles de documentacio tecnica. Quines decisions prendries sobre quin model d'embeddings fer servir i per que? Pensa en qualitat, velocitat, memoria i idioma.

Pistes per respondre:
- Qualitat: com mes alt millor, pero fins a un punt.
- Velocitat: sense GPU, 10.000 textos poden trigar molt.
- Memoria: cada embedding ocupa memoria (768 floats = 3 KB per text).
- Idioma: catala? angles? barreja?
- Quin model especific triaries (nomic, mxbai, bge)?
- Quant trigaries? Com ho optimitzaries?
