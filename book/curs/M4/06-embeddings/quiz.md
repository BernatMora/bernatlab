# Qüestionari - Capitol 6: Embeddings

> 15 preguntes · ~20 min · 7 test + 8 obertes

## Pregunta 1
Que es un embedding?

- [ ] Un tipus de base de dades
- [x] Un vector numeric que representa el significat d'un text
- [ ] Un model d'IA per generar text
- [ ] Un sistema operatiu

## Pregunta 2
Quantes dimensions te habitualment un embedding modern?

- [ ] 10-20
- [ ] 50-100
- [x] 384, 768, 1024 o 1536
- [ ] 1.000.000+

## Pregunta 3
Que vol dir que dos embeddings son "propers"?

- [ ] Que tenen el mateix nombre de digits
- [x] Que els vectors corresponents son similars (mateixa direccio)
- [ ] Que els textos tenen la mateixa longitud
- [ ] Que les paraules son iguals

## Pregunta 4
Quina es la metrica estandard per comparar embeddings?

- [ ] Distancia euclidea
- [ ] Manhattan distance
- [x] Semblança cosinus
- [ ] Distancia de Hamming

## Pregunta 5
Quin rang te la semblança cosinus?

- [ ] 0 a 100
- [x] -1 a 1
- [ ] 0 a 1
- [ ] -100 a 100

## Pregunta 6
Quin model d'embeddings es bo per defecte a Ollama?

- [ ] llama3.2
- [x] nomic-embed-text
- [ ] mistral
- [ ] phi3

## Pregunta 7
Quina es la diferencia entre "el gat menja peix" i "el moix menja peix" en termes d'embedding?

- [ ] Son completament diferents
- [x] Son molt semblants perque volen dir el mateix
- [ ] Son identics nomes si les paraules son identiques
- [ ] Es impossible comparar-los

## Pregunta 8 (oberta)
Explica amb les teves paraules: que representa cada dimensio d'un embedding de 768 numeros? Es una dimensio = una paraula? Un concepte?

Pistes per respondre:
- No, una dimensio no es una paraula concreta.
- Cada dimensio captura algun aspecte del significat.
- Es mes semblant a "components abstractes" que a paraules.
- Aixo te implicacions per entendre com funciona el model.

## Pregunta 9 (oberta)
Per que creus que la semblança cosinus es mes util que la distancia euclidea per comparar embeddings? Dona exemples concrets al BernatLab.

Pistes per respondre:
- Cosinus mesura l'angle (direccio), no la distancia.
- Dos textos de longitud diferent poden ser similars.
- Exemple: "el gat menja" i "el gat menja peix" son similars encara que tinguin longituds diferents.
- Quan la euclidea falla i la cosinus encerta.

## Pregunta 10 (oberta)
Si el model d'embeddings canvia (per exemple passes de `nomic-embed-text` a `mxbai-embed-large`), cal re-indexar tots els documents? Per que?

Pistes per respondre:
- Si, cal re-indexar.
- Cada model te el seu propi "espai vectorial".
- Embeddings del mateix text amb models diferents NO son comparables.
- Aixo es un cost important a considerar quan es tria model.

## Pregunta 11 (oberta)
Compara "Word2Vec" (antic) i "Sentence Transformers" (modern) en quant a capacitat. Per que el primer ha quedat obsolet?

Pistes per respondre:
- Word2Vec: un embedding per paraula, no enten contexte.
- Sentence Transformers: embedding per frase, enten contexte.
- Exemple: "bank" en "river bank" vs "bank account" - Word2Vec no diferencia.
- Els models moderns entenen polisemia i contexte.

## Pregunta 12 (oberta)
Quina relacio hi ha entre la mida del model d'embeddings i la qualitat dels resultats? Es sempre millor un model mes gran?

Pistes per respondre:
- Fins a cert punt, mes gran = millor.
- Pero mes gran = mes lent i mes memoria.
- Sweet spot: 100-500M parametres per a la majoria d'usos.
- Aplica al BernatLab: quin model tries i per que.

## Pregunta 13 (oberta)
Imagina que vols comparar el contingut de 1.000 correus per trobar temes comuns. Com ho faries amb embeddings? Quin cost computacional tindria?

Pistes per respondre:
- Calcular 1.000 embeddings: pocs segons amb nomic-embed-text.
- Calcular 1.000.000 de semblances (tots amb tots): 1M * 768 dimensions = 768M operacions.
- A 1 mil milio per segon, son uns 0.7 segons. Trivial.
- Clustering: k-means o DBSCAN per grup tematics.

## Pregunta 14 (oberta)
Quines consequencies te usar embeddings amb texts molt curts (1-2 paraules) o molt llargs (>1000 paraules)? Com ho gestionaries?

Pistes per respondre:
- Text molt curt: poques dimensions capturades, menys precissio.
- Text molt llarg: truncar pot perdre informacio important.
- Estrategia: truncar a 512 tokens (max habitual), o fer chunking.
- Aplica al BernatLab: noms de sensors vs descripcions llargues.

## Pregunta 15 (oberta)
Argumenta: prefereixes calcular embeddings al núvol (OpenAI text-embedding-3) o local (Ollama + nomic-embed-text) al BernatLab? Posa arguments per les dues bandes.

Pistes per respondre:
- Arguments núvol: qualitat lleugerament millor, no cal hardware.
- Arguments local: privadesa, cost zero, disponibilitat.
- Cas concret: el BernatLab processa logs i dades personals.
- Tria final: defensa-la amb un argument practic.
