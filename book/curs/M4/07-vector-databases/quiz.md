# Qüestionari - Capitol 7: Vector databases

> 15 preguntes · ~20 min · 7 test + 8 obertes

## Pregunta 1
Que es una "vector database"?

- [ ] Una base de dades tradicional
- [x] Una base de dades optimitzada per emmagatzemar i cercar embeddings
- [ ] Un sistema operatiu
- [ ] Un model d'IA

## Pregunta 2
Quina diferencia hi ha entre una base de dades tradicional i una de vectors?

- [ ] Son exactament igual
- [x] La tradicional cerca per valors exactes; la vector cerca per semblança
- [ ] La vector nomes guarda text
- [ ] La tradicional es mes nova

## Pregunta 3
Quina vector database es recomana per a un homelab petit?

- [ ] Pinecone
- [x] ChromaDB
- [ ] Oracle
- [ ] MongoDB

## Pregunta 4
Quina es la limitacio aproximada de ChromaDB?

- [ ] 100 documents
- [x] Fins a uns 100.000 documents (per a mes, cal alternatives)
- [ ] 1 milio de documents
- [ ] Sense limits

## Pregunta 5
Quin avantatge te ChromaDB per a un homelab?

- [ ] Requereix un servidor separat
- [x] Es instal·la amb pip i guarda les dades a un fitxer local
- [ ] Cal contractar un servei cloud
- [ ] Nomes funciona a Windows

## Pregunta 6
Quina d'aquestes es una base de dades de vectors local?

- [ ] Pinecone
- [x] Qdrant
- [ ] OpenAI
- [ ] Notion

## Pregunta 7
Quina es la diferencia entre "FAISS" i "ChromaDB"?

- [ ] Son sinonims
- [x] FAISS es una llibreria de Meta (cal programar mes); ChromaDB es una DB completa (mes facil)
- [ ] FAISS nomes funciona a Mac
- [ ] ChromaDB nomes serveix per a text

## Pregunta 8 (oberta)
Explica amb les teves paraules: per que necessitem una "vector database" i no podem simplement guardar els embeddings en un fitxer de text o una base de dades SQL?

Pistes per respondre:
- Calcular la semblança entre un vector de consulta i 1 milio de vectors es costós.
- Les vector DB usen estructures especials (HNSW, IVF) per accelerar la cerca.
- Sense elles, cada consulta trigaria segons o minuts.
- Exemples concrets: cerca k-NN en O(n) vs O(log n).

## Pregunta 9 (oberta)
Compara ChromaDB, FAISS, Qdrant i Pinecone segons quatre criteris: facilitat d'us, escalabilitat, cost i cas d'us al BernatLab. Fes una taula i raona la tria.

Pistes per respondre:
- ChromaDB: facil, limitat a 100k, gratis, ideal per homelab.
- FAISS: programmatic, scalable, gratis, cal mes feina.
- Qdrant: production-ready, scalable, gratis, mes complex.
- Pinecone: cloud, facil, de pagament, no es local.
- Tria per al BernatLab: defensa-la.

## Pregunta 10 (oberta)
Quina relacio hi ha entre la mida de la base de dades de vectors i el temps de cerca? Si passes de 10.000 a 1.000.000 de chunks, que passa?

Pistes per respondre:
- En estructura naive, la cerca es O(n): 100x mes chunks = 100x mes temps.
- Amb indexacio (HNSW), es O(log n): 100x mes chunks = ~2x mes temps.
- ChromaDB usa indexacio per defecte.
- Aplica al BernatLab: quan cal canviar de ChromaDB a Qdrant?

## Pregunta 11 (oberta)
Imagina que tens 50.000 chunks al ChromaDB i el sistema va lent. Quines optimitzacions pots fer ABANS de canviar a una altre base de dades?

Pistes per respondre:
- Optimitzacio 1: usar un model d'embeddings mes rapid (all-MiniLM en lloc de mxbai).
- Optimitzacio 2: reduir la mida dels chunks (200 caracters en lloc de 1000).
- Optimitzacio 3: usar quantization (compressio dels vectors).
- Optimitzacio 4: nomes indexar els chunks mes importants, no tots.
- Optimitzacio 5: augmentar la RAM del servidor.

## Pregunta 12 (oberta)
Per que les vector databases usen algoritmes aproximats (ANN) en lloc de cerques exactes? Quines consequencies te per a la qualitat?

Pistes per respondre:
- Cerca exacta: comparar amb tots els n vectors. O(n). Lenta.
- ANN (Approximate Nearest Neighbors): troba els "quasi" mes propers. O(log n). Rapida.
- Aplica: HNSW, IVF, LSH.
- Perd un 1-5% de qualitat pero guanya 100x en velocitat.
- En la majoria de casos RAG, la perdua es acceptable.

## Pregunta 13 (oberta)
Com evaluaries si la teva vector database es prou rapida per a l'us que en fas al BernatLab? Descriu un metode amb metriques concretes.

Pistes per respondre:
- Metrica 1: latency per consulta (objectiu: <100ms per检索).
- Metrica 2: throughput (consultes per segon en parallel).
- Metrica 3: us de memoria (per 10k vectors).
- Test: 1000 consultes aleatories, mesurar latencies.
- Llindar: si >50% de consultes passen de 200ms, cal optimitzar.

## Pregunta 14 (oberta)
Quines consequencies te eliminar metadades dels vectors? Pensa en el cas del BernatLab: vols poder filtrar per "data" o "tipus de document".

Pistes per respondre:
- ChromaDB permet guardar metadades juntament amb cada vector.
- Filtres: "cerca nomes entre els documents publicats despres de 2024".
- Us: alerting, segmentacio, personalitzacio.
- Riscos: mes metadades = mes espai.
- Al BernatLab: quines metadades son utils?

## Pregunta 15 (oberta)
Argumenta: prefereixes ChromaDB (facil, local, limitat) o Qdrant (mes complex, mes potent, local) per al BernatLab? Posa arguments per les dues bandes.

Pistes per respondre:
- Arguments ChromaDB: simplicitat, suficient per a 50k chunks, comunitat gran.
- Arguments Qdrant: escalabilitat, produccio-ready, API rica, mes rapid en escales grans.
- Cas concret: el BernatLab te 5k-50k chunks actuals i pot pujar a 100k.
- Tria final: defensa-la amb un argument practic i un pla de migracio si cal.
