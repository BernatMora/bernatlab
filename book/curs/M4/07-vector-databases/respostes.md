# Respostes - Capitol 7: Vector databases

## Pregunta 1: Que es una vector database?

**Resposta correcta**: Una base de dades optimitzada per a cerques per semblança.

**Explicacio**: Una vector database emmagatzema embeddings (vectors numerics) i permet cercar els mes semblants a un vector donat. Es diferent d'una base de dades tradicional, que cerca coincidencies exactes.

---

## Pregunta 2: Millor per a un homelab?

**Resposta correcta**: ChromaDB.

**Explicacio**: ChromaDB es la mes facil d'instal·lar, es self-hosted, es gratis, i no cal un servidor separat. Pinecone es al nuvol i cal compte. Oracle i MongoDB son bases de dades tradicionals, no vector databases.

---

## Pregunta 3: Com es guarden?

**Resposta correcta**: En un fitxer local (PersistentClient).

**Explicacio**: ChromaDB permet guardar les dades en un directori local mitjançant PersistentClient. No cal un servidor separat - tot esta en fitxers al disc.

---

## Pregunta 4: Sweet spot de chunk size?

**Resposta correcta**: 300-800 paraules.

**Explicacio**: Chunks massa petits fan que el LLM perdi context. Chunks massa grans fan que el LLM no hi capiga. 300-800 paraules es l'equilibri.

---

## Pregunta 5: Quants fragments?

**Resposta correcta**: 3-5.

**Explicacio**: k=1 perd informacio. k=10+ fa que el LLM es confongui. 3-5 es l'equilibri recomanat.

---

## Pregunta 6: Re-ranking?

**Resposta correcta**: Re-ranking (una segona cerca entre els resultats).

**Explicacio**: El re-ranking fa una segona pasada sobre els fragments ja trobats per ordenar-los millor. Es mes complex pero pot millorar la precisio. Augmentar k nomes porta mes soroll.

---

## Pregunta 7 (oberta): Per que ChromaDB i no Pinecone?

**Resposta model**:

- **Privadesa**: ChromaDB es local, Pinecone es al nuvol. Si vols privadesa, ChromaDB.
- **Cost**: ChromaDB es gratis, Pinecone cobra per us.
- **Complexitat**: ChromaDB es un sol `pip install`, Pinecone cal compte i clau API.
- **Emmagatzematge**: ChromaDB es un fitxer local, Pinecone es al núvol d'ells.

**Per a un homelab personal**, ChromaDB es la millor opcio perquè volem privadesa, cost zero, i simplicitat.

---

## Pregunta 8 (oberta): 10.000 documents

**Resposta model**:

Si cada document te ~2000 paraules:
- Amb chunk_size=500 i overlap=50, cada document genera ~4-5 chunks.
- 10.000 documents * 5 chunks = **~50.000 chunks**.

Aixo es un volum **perfectament acceptable** per a ChromaDB. Pot gestionar-ne milions. El rendiment sera bo (~100ms per cerca).

**Compte**: el temps d'indexacio pot ser llarg. Si cada chunk triga 50ms a indexar, son ~40 min. Es pot fer en background.

---

## Pregunta 9 (oberta): Quan usaries LanceDB?

**Resposta model**:

Usaria LanceDB en lloc de ChromaDB si:
- **Volum de dades molt gran** (>1M chunks). ChromaDB es mes lent a escala.
- **Necessites velocitat extrema** (<10ms per cerca). LanceDB es mes rapid.
- **Vols una sola eina** per a embeddings + cerca + analisi. LanceDB es mes integrat.
- **Acceptes mes complexitat** de setup (cal Rust, etc.).

Per a un homelab amb 10-100k chunks, ChromaDB es perfecte i mes simple.

---

## Pregunta 10 (oberta): Per que el mateix model?

**Resposta model**:

El model d'embeddings ha de ser el **mateix** per indexar i per cercar perque:

- Si els embeddings tenen **dimensions diferents** (ex: 384 vs 768), ChromaDB no pot comparar-los.
- Si el **model es diferent**, dos textos semblants tenen vectors molt diferents. La cerca fallaria.
- Si canvies el model, has de **re-indexar TOT** desde zero.

**Conclusio**: tria un model al principi (ex: `nomic-embed-text`), i no el canviis sense re-indexar.

---

## Què fer si has fallat moltes

- **5-8 encerts**: Rellegir el resum.
- **3-4 encerts**: Prova ChromaDB amb l'exercici.
- **0-2 encerts**: Comença pel basics - que es un embedding.
