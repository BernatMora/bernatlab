# Quiz - Capitol 7: Vector databases

## Pregunta 1
Que es una vector database?

- [ ] Una base de dades tradicional
- [x] Una base de dades optimitzada per a cerques per semblança
- [ ] Un sistema de fitxers
- [ ] Un llenguatge de programacio

## Pregunta 2
Quina vector database es la mes recomanable per a un homelab?

- [ ] Pinecone
- [x] ChromaDB
- [ ] Oracle
- [ ] MongoDB

## Pregunta 3
Com es guarden les dades a ChromaDB?

- [ ] En un servidor remot obligatoriament
- [x] En un fitxer local (PersistentClient)
- [ ] A la RAM solament
- [ ] Al núvol de Google

## Pregunta 4
Quin es el sweet spot de chunk size per a RAG?

- [x] 300-800 paraules
- [ ] 50-100 paraules
- [ ] 2000-5000 paraules
- [ ] 1-10 paraules

## Pregunta 5
Quantes fragments retornes normalment en una cerca RAG?

- [ ] 1
- [x] 3-5
- [ ] 20-50
- [ ] 100+

## Pregunta 6
Quin metode pots usar per obtenir mes precisio en la cerca?

- [ ] Augmentar k a 100
- [x] Re-ranking (una segona cerca entre els resultats)
- [ ] Usar un embedding mes petit
- [ ] No fer res, ChromaDB ja es perfecte

## Pregunta 7 (oberta)
Per que ChromaDB es la millor opcio per a un homelab i Pinecone no?

Pistes:
- Privadesa
- Cost
- Complexitat
- Emmagatzematge

## Pregunta 8 (oberta)
Si tens 10.000 documents d'Hort Osona, quants chunks tindras? Com afectaria el rendiment?

Pistes:
- Si cada document te ~2000 paraules
- Amb chunk_size=500 i overlap=50
- Quants chunks per document?
- ChromaDB pot gestionar-ho?

## Pregunta 9 (oberta)
Explica quan usaries LanceDB en comptes de ChromaDB.

Pistes:
- Volum de dades
- Velocitat requerida
- Comunitat
- Complexitat acceptable

## Pregunta 10 (oberta)
Per que es important que el model d'embeddings sigui el mateix per indexar i per cercar?

Pistes:
- Que passa si canvies el model?
- Que passa si els embeddings son de mides diferents?
- Que passaria amb la cerca?
