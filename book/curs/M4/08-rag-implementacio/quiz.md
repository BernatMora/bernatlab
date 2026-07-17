# Qüestionari - Capitol 8: RAG - implementacio completa

> 15 preguntes · ~20 min · 7 test + 8 obertes

## Pregunta 1
Quantes fases te el pipeline RAG?

- [ ] 2
- [ ] 3
- [x] 5 (carregar, chunking, embeddings, query, generacio)
- [ ] 10

## Pregunta 2
Per que cal fer "chunking" dels documents abans d'indexar?

- [ ] Per estalviar espai
- [x] Perque els documents llargs no caben al contexte del LLM
- [ ] Per accelerar la cerca
- [ ] Per xifrar el contingut

## Pregunta 3
Quina es la mida tipica dun chunk?

- [ ] 10-50 caracters
- [x] 200-1000 caracters
- [ ] 10.000+ caracters
- [ ] 1 caracter

## Pregunta 4
Que vol dir "overlap" en chunking?

- [ ] Un error
- [x] Que dos chunks consecutius comparteixen algunes paraules per mantenir contexte
- [ ] La mida del vector
- [ ] El temps de calcul

## Pregunta 5
Quin es el primer pas dun pipeline RAG?

- [ ] Fer la consulta
- [x] Carregar i indexar els documents
- [ ] Generar la resposta
- [ ] Validar amb l'usuari

## Pregunta 6
Que retorna la funcio `collection.query()` de ChromaDB?

- [ ] El text del LLM
- [x] Els N chunks mes semblants a la pregunta
- [ ] Un missatge d'error
- [ ] La base de dades sencera

## Pregunta 7
Quin parametre controla quants chunks retorna la cerca?

- [ ] temperature
- [x] n_results
- [ ] max_tokens
- [ ] chunk_size

## Pregunta 8 (oberta)
Explica amb les teves paraules: per que es important l'ordre de les passes en un pipeline RAG? Podries, per exemple, fer la cerca ABANS d'indexar?

Pistes per respondre:
- L'indexacio ha d'estar feta abans de poder cercar.
- Si canvies els documents, cal re-indexar.
- Cada pas depen de l'anterior.
- Exemple analogic: cuinar (primer compres, despres prepares, despres cuines).

## Pregunta 9 (oberta)
Compara chunking per "caracters" vs chunking per "paragrafs" vs chunking per "seccions". Per al cas del BernatLab (fitxes de cultiu), quin tries i per que?

Pistes per respondre:
- Caracters: talla a X caracters independentment del contexte.
- Paragrafs: cada paragraf es un chunk. Manten la coherencia local.
- Seccions: cada seccio (per H2) es un chunk. Molt coherent pero variable en mida.
- Per a Hort Osona: les seccions son naturals, pero poden ser massa llargues.

## Pregunta 10 (oberta)
Quina relacio hi ha entre la mida del chunk i la qualitat de la resposta RAG? Es millor chunks petits o grans?

Pistes per respondre:
- Massa petits: poca informacio per chunk, caldrien molts.
- Massa grans: dilueixen la informacio rellevant amb contexte irrellevant.
- Sweet spot: 300-500 caracters, depen del domini.
- Trade-off: mes chunks = mes precisa la cerca pero mes cost.

## Pregunta 11 (oberta)
Si tens un document de 50 pagines i el vols indexar, quants chunks generes aproximadament? Quant trigaras? Quin cost te?

Pistes per respondre:
- Una pagina = uns 2000-3000 caracters.
- 50 pagines = 100.000-150.000 caracters.
- Amb chunks de 500 caracters: 200-300 chunks.
- Triga: 1 chunk = ~100ms d'embedding. Total: 20-30 segons.
- Cost d'emmagatzematge: negligible (uns MB).

## Pregunta 12 (oberta)
Per que cal vigilar el "context overflow" en el pas final del RAG? Que pot passar?

Pistes per respondre:
- Si passem 10 chunks de 1000 caracters = 10k caracters = ~15k tokens.
- Si el model nomes te 4k de context, es trunca.
- El LLM pot "inventar" o ignorar parts del contexte.
- Solucio: controlar n_results i mida del chunk.

## Pregunta 13 (oberta)
Com gestionaries les actualitzacions: si afegeixes un document nou a la base de coneixement cada setmana, cal re-indexar TOTS els documents o nomes el nou?

Pistes per respondre:
- Re-indexar nomes el nou: rapid pero pot perdre optimizations.
- Re-indexar tot: lent pero garantit.
- Estrategia intermedia: indexacio incremental amb un ID unic.
- ChromaDB permet afegir sense re-indexar.
- Com ho faries servir al BernatLab?

## Pregunta 14 (oberta)
Quines metriques monitoraries en un sistema RAG en produccio al BernatLab? Llista 5 amb els seus llindars d'alerta.

Pistes per respondre:
- Metrica 1: latency de la consulta (<5s per a RPi 4).
- Metrica 2: taxa d'errors de l'API (<1%).
- Metrica 3: nombre de chunks retornats amb baixa semblança (<0.5).
- Metrica 4: mida de la base de dades (<5 GB).
- Metrica 5: temps de re-indexacio (<30 min per 1000 chunks nous).

## Pregunta 15 (oberta)
Argumenta: prefereixes un RAG simple amb ChromaDB o un sistema mes sofisticat amb re-ranking i multi-query? Posa arguments per les dues bandes.

Pistes per respondre:
- Arguments RAG simple: facil de mantenir, suficient per a 80% dels casos.
- Arguments RAG sofisticat: millor qualitat, millor recall, millor per a casos edge.
- Cost: el sofisticat requereix mes models, mes temps, mes memoria.
- Tria final: defensa-la amb un cas concret del BernatLab.
