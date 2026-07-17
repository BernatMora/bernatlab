# Respostes - Capitol 7: Vector databases

> Mira les respostes DESPRES d'haver fet el qüestionari.

## Pregunta 1: Que es una vector database?

**Resposta correcta**: Una base de dades optimitzada per emmagatzemar i cercar embeddings.

**Explicacio**: Es com una base de dades tradicional pero en lloc de cercar valors exactes, cerca per semblança entre vectors. Fa servir algoritmes especialitzats (HNSW, IVF) per fer les cerques eficients.

---

## Pregunta 2: Diferencia amb base de dades tradicional

**Resposta correcta**: La tradicional cerca per valors exactes; la vector cerca per semblança.

**Explicacio**: SQL pot fer `WHERE titol = 'poma'` pero no pot fer "cerca conceptes semblants a poma". La vector DB compara vectors i retorna els mes propers. Son eines complementaries.

---

## Pregunta 3: Vector DB per a homelab

**Resposta correcta**: ChromaDB.

**Explicacio**: ChromaDB es la opcio mes facil per a un homelab: s'instal·la amb pip, guarda les dades a un fitxer local, i es perfecta per a volums petits-mitjans. Pinecone es cloud (pagament), Oracle es sobredimensionat.

---

## Pregunta 4: Limitacio de ChromaDB

**Resposta correcta**: Fins a uns 100.000 documents.

**Explicacio**: ChromaDB funciona be fins a uns 100k vectors. Per sobre, comenca a alentir-se. A partir d'1M, cal Qdrant o solucions mes serioses.

---

## Pregunta 5: Avantatge de ChromaDB

**Resposta correcta**: Es instal·la amb pip i guarda les dades a un fitxer local.

**Explicacio**: No cal un servidor separat, no cal configurar res complex. Es la rao per la que es perfecta per a homelabs. Alternatives com Qdrant requereixen un servidor Docker.

---

## Pregunta 6: Vector DB local

**Resposta correcta**: Qdrant.

**Explicacio**: Qdrant es local, open source, i escalable. Pinecone es cloud (no local), OpenAI no es una DB, Notion es una eina de productivitat.

---

## Pregunta 7: FAISS vs ChromaDB

**Resposta correcta**: FAISS es una llibreria; ChromaDB es una DB completa.

**Explicacio**: FAISS es una llibreria de Meta que cal programar (Python/C++). ChromaDB es una solucio completa amb API senzilla. Per a prototips rapids, ChromaDB. Per a maxim control, FAISS.

---

## Pregunta 8 (oberta): Per que una vector DB?

**Resposta model**:

A primera vista, guardar embeddings en un fitxer o una base de dades SQL sembla factible. Pero el problema es la **cerca**: cada vegada que fas una consulta, has de comparar el vector de la pregunta amb **tots** els vectors guardats. Si tens 1.000.000 de vectors de 768 dimensions, son 768 milions d'operacions per consulta. A 1 GFLOP/s, son 0.7 segons per consulta. Si tens 10 consultes per segon, son 7 segons totals. Inutilitzable.

Les vector databases usen **estructures de dades especialitzades** per accelerar aquesta cerca:

**HNSW (Hierarchical Navigable Small World)**: organitza els vectors en un graf multicapa. La cerca es O(log n) en lloc de O(n). Es a dir, amb 1M vectors, la cerca triga uns 20-30 comparacions (cada una a ~1ms) = 30ms. **100x mes rapid**.

**IVF (Inverted File Index)**: particiona l'espai en "cells" i nomes busca a la cell mes propera. Encara mes rapid per a volums molt grans, pero menys precissio.

**LSH (Locality-Sensitive Hashing)**: usa funcions hash que preserven la proximitat. Rapida pero menys precisa que HNSW.

A mes a mes, les vector DB ofereixen:
- **Persistencia**: guardar a disc sense perdre rendiment.
- **Metadades**: filtrar per data, autor, categoria.
- **Concurrencia**: multiples consultes simultanies.
- **Replicacio**: alta disponibilitat.

**Sense vector DB**, el RAG nomes es viable per a volums molt petits (<1k documents). Amb vector DB, podem tenir milions de chunks i respondre en milisegons. Es la diferencia entre un projecte de toy i un sistema de produccio.

---

## Pregunta 9 (oberta): Comparacio de 4 opcions

**Resposta model**:

| Eina | Facilitat | Escalabilitat | Cost | Cas al BernatLab |
|---|---|---|---|---|
| **ChromaDB** | Alta (pip install) | Fins a 100k | Gratis | Perfecte per defecte |
| **FAISS** | Baixa (cal programar) | Milions | Gratis | Si necessites maxim control |
| **Qdrant** | Mitjana (contenidor Docker) | Milions | Gratis | Si el BernatLab creix |
| **Pinecone** | Alta (cloud) | Il·limitada | Pagament per ús | NO, volem local |

**Analisi detallada**:

**ChromaDB** es la millor opcio per defecte al BernatLab. Es instal·la amb un `pip install`, guarda dades a un fitxer, i es perfecta fins a 100k chunks. La corba d'aprenentatge es minima.

**FAISS** es per a casos especials on necessites optimitzar al maxim el rendiment o treballar amb milions de vectors. Cal escriure mes codi pero tens control absolut.

**Qdrant** es quan el BernatLab creix mes enlla de 100k chunks. Es un servidor Docker amb una API REST. Escala a milions de vectors. Pero afegeix complexitat operacional.

**Pinecone** es la millor opcio cloud pero te un cost per embeddings emmagatzemats i per consultes. A mes, va contra la filosofia del BernatLab (tot local i privat).

**Tria per al BernatLab**: **ChromaDB** per defecte. Si arribem a 100k chunks i el rendiment baixa, evaluem migracio a Qdrant. La transicio es factible perque ambdues tenen APIs similars.

**Pla de migracio**:
1. Mentre <50k: ChromaDB sense preocupar-se.
2. Entre 50k-100k: monitorejar latency. Si >100ms, optimitzar.
3. >100k: evaluar Qdrant o LanceDB.

---

## Pregunta 10 (oberta): Mida i temps de cerca

**Resposta model**:

La relacio entre mida i temps depen criticament de si usem **indexacio** o no.

**Sense indexacio (cerca lineal, naive)**:
- Temps: O(n * d), on n = nombre de vectors, d = dimensions.
- De 10k a 1M (100x mes chunks): el temps es 100x mes.
- Exemple: 10k vectors a 50ms. 1M vectors a 5.000ms = 5 segons. **Inutilitzable**.

**Amb indexacio (HNSW, per defecte a ChromaDB)**:
- Temps: O(log n * d), pero amb constants mes grans.
- De 10k a 1M: el temps creix uns 2-3x, no 100x.
- Exemple: 10k vectors a 5ms. 1M vectors a 15-20ms. **Acceptable**.

**Implicacio practica al BernatLab**:

| Volum | ChromaDB latency | Recomanacio |
|---|---|---|
| <10k | <10ms | Excel·lent |
| 10k-100k | 10-50ms | Bona |
| 100k-500k | 50-200ms | Acceptable |
| 500k-1M | 200-500ms | Cal optimitzar |
| >1M | >500ms | Canviar a Qdrant/FAISS |

**Quan canviar**: si passes de 100k i la latency mitjana supera els 200ms, cal optimitzar. Les optimitzacions possibles son:
- Reduir dimensions (PCA).
- Usar quantization (compressio).
- Canviar a un algoritme mes efficient (HNSW -> IVF).
- Canviar a Qdrant.

**Al BernatLab actual**: amb 5k-10k chunks, ChromaDB es mes que suficient. Ni tan sols cal pensar en alternatives.

---

## Pregunta 11 (oberta): Optimitzacions abans de canviar

**Resposta model**:

Si tens 50k chunks i el sistema va lent, abans de canviar de vector DB, prova aquestes optimitzacions ordenades per cost-benefici:

**1. Model d'embeddings mes rapid**. Si usaves `mxbai-embed-large` (335M params), passa a `nomic-embed-text` (137M) o `all-MiniLM` (22M). El calcul d'embeddings es el coll d'ampolla mes comu. Reduir mida del model pot donar 3-5x mes velocitat amb una perdua minima de qualitat.

**2. Reduir la mida dels chunks**. Si els teus chunks son de 1000 caracters, passa a 300-500. Calcules menys embeddings i la cerca es mes rapida (vectors comparables mes petits). Pero verifica que no perds context important.

**3. Quantization**. ChromaDB pot guardar vectors en int8 en lloc de float32. Ocupa 4x menys i la cerca es 2-3x mes rapida. La perdua de qualitat es minima (<2%).

**4. Indexacio selectiva**. En lloc d'indexar tots els chunks, indexa nomes els mes importants o els mes consultats. Pots tenir dos nivells: un "hot" index amb 10k chunks importants i un "cold" amb la resta. Cerques primer al hot, si no trobes res, al cold.

**5. Mes RAM**. ChromaDB es mes rapid quan els vectors caben a RAM. Si tens 1M vectors de 768 dimensions en float32 = 3 GB. Si tens 16 GB de RAM, cap perfectament. Si nomes tens 4 GB, va a swap i es lent. Considera augmentar RAM.

**6. Canviar parametres de HNSW**. ChromaDB permet ajustar `M` (connexions per node) i `ef_construction` (cerca durant construccio). Mes alt = mes precissio pero mes lent. Cal trobar el punt just.

**Si res funciona**, llavors si: evaluar migracio a Qdrant o LanceDB. Pero sovint, una o dues optimitzacions ja resolen el problema.

---

## Pregunta 12 (oberta): Algoritmes aproximats (ANN)

**Resposta model**:

Els algoritmes ANN (Approximate Nearest Neighbors) s'usen perque **la cerca exacta es massa lenta** a volums grans. A canvi d'una petita perdua de qualitat, obtenim **100-1000x mes velocitat**.

**Per que calen algoritmes aproximats**:
- **Cerca exacta** (brute force): comparar amb tots els vectors. Garantit trobar els mes propers. O(n*d). A 1M vectors, son 768M operacions per consulta. ~1 segon. Massa lent per a una aplicacio interactiva.
- **Cerca aproximada** (HNSW, IVF): trobar els "quasi" mes propers. O(log n * d). A 1M vectors, son uns 20-30K operacions. ~5-10ms. **100x mes rapid**.

**Tipus d'algoritmes ANN**:

**HNSW (Hierarchical Navigable Small World)**:
- Organitza els vectors en un graf multicapa.
- Cerca com un "salt entre veins" fins arribar al mes proper.
- Usat per defecte a ChromaDB, Qdrant, Weaviate.
- Molt bona qualitat i velocitat.

**IVF (Inverted File Index)**:
- Parteix l'espai en N "cells" (clusters).
- Nomes busca a les cells mes properes a la consulta.
- Mes rapid que HNSW a volums molt grans, pero menys precissio.

**LSH (Locality-Sensitive Hashing)**:
- Usa funcions hash que posen vectors similars al mateix "bucket".
- Molt rapid pero menys precissio que HNSW.

**Consequencia per a la qualitat**:
- HNSW perd ~1% de recall@10 (1 de cada 100 cerques no troba el millor resultat).
- IVF pot perdre 3-5%.
- LSH pot perdre 10-15%.

**En RAG**, aquesta perdua es negligible perque:
- L'LLM ja te una certa tolerancia a errors en el contexte.
- 5 chunks aproximadament rellevants > 5 exactes pero trigant 100x mes.
- L'usuari no nota la diferencia.

**Recomanacio**: usar HNSW per defecte. Es el millor equilibri.

---

## Pregunta 13 (oberta): Metriques de rendiment

**Resposta model**:

Per avaluar si la vector DB es prou rapida, cal mesurar quatre metriques:

**1. Latencia per consulta (p50, p95, p99)**:
- p50: el 50% de les consultes son mes rapides que aquest valor.
- p95: el 95% de les consultes son mes rapides.
- p99: el 99%.
- Objectiu al BernatLab: p50 <50ms, p95 <200ms, p99 <500ms.
- Si p95 >500ms, hi ha un problema.

**2. Throughput (QPS - queries per segon)**:
- Quantes consultes pot gestionar el sistema en parallel?
- Test: 1000 consultes en 10 segons en paral·lel.
- Objectiu: >20 QPS per a una sola instancia de ChromaDB.
- Si necessitem mes, cal escalar o cambiar a Qdrant.

**3. Us de memoria**:
- Per 10k vectors de 768 dimensions en float32 = 30 MB.
- Amb HNSW: 5-10x mes (~200-300 MB per 10k vectors).
- Monitoritzar amb `htop` o `psutil`.
- Si la memoria puja sense parar, tenim un memory leak.

**4. Temps de re-indexacio**:
- Quant trigem a afegir 1000 nous chunks?
- Inclou: calcul d'embeddings + insercio a la DB.
- Objectiu: <10 min per a 1000 chunks.
- Si passa de 30 min, cal optimitzar el chunking o el model.

**Test practic al BernatLab**:

```python
import chromadb
import time
import random

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection("hort_osona")

# 100 consultes aleatories
latencies = []
for _ in range(100):
    query = f"Consulta sobre {random.choice(['tomàquets', 'enciams', 'sensors', 'reg'])}"
    inici = time.time()
    collection.query(query_texts=[query], n_results=5)
    latencies.append(time.time() - inici)

latencies.sort()
print(f"p50: {latencies[50]*1000:.1f}ms")
print(f"p95: {latencies[95]*1000:.1f}ms")
print(f"p99: {latencies[99]*1000:.1f}ms")
```

**Llindar d'alerta**: si p95 >200ms o us de memoria >500MB amb 10k vectors, cal optimitzar o canviar.

---

## Pregunta 14 (oberta): Metadades i filtres

**Resposta model**:

Eliminar metadades dels vectors te **consequencies importants** per a casos d'us reals. Al BernatLab, les metadades son molt utils.

**Que son les metadades**: informacio estructurada associada a cada vector pero separada del contingut. Exemples:
- `data_publicacio`: "2024-03-15".
- `tipus_document`: "fitxa_cultiu", "alerta", "log".
- `autor`: "Bernat", "Maria".
- `tags`: ["tomàquet", "primavera", "plaga"].

**Per que serveixen al BernatLab**:

**Cas 1 - Cerca temporal**: "mostra'm les alertes d'aquesta setmana". Filtre: `data_publicacio >= "2024-03-10"`. Sense metadades, impossible.

**Cas 2 - Cerca per tipus**: "vull nomes les fitxes de cultiu, no els logs". Filtre: `tipus_document = "fitxa_cultiu"`.

**Cas 3 - Cerca combinada**: "alertes de temperatura a l'hort sud dels ultims 7 dies". Filtres compostos: `tipus = "alerta" AND zona = "sud" AND data > NOW() - 7d`.

**Riscos de tenir metadades**:
- **Mes espai**: cada chunk te un petit extra de dades estructurades. Per a 10k chunks, son pocs KB. Per a 1M, poden ser GB.
- **Indexacio mes complexa**: ChromaDB ha d'indexar tambe les metadades per fer els filtres eficients.
- **Cal dissenyar l'esquema**: cal pensar quines metadades son utils i quines no.

**Recomanacio al BernatLab**:
- **Si**: data_publicacio, tipus_document, zona_hort, gravetat_alerta.
- **No**: text llarg, IDs interns, dades sensibles (millor xifrar-les o no guardar-les).
- **Format**: dates en ISO 8601 ("2024-03-15"), enums tancats (no strings lliures).

**Millora practica**: abans de llençar metadades, pensa si vols fer cerques temporals o per categories. Si la resposta es si, val la pena l'overhead.

---

## Pregunta 15 (oberta): ChromaDB vs Qdrant

**Resposta model**:

**Arguments a favor de ChromaDB**:
- **Simplicitat**: `pip install` i llest. No cal Docker, no cal servidor separat.
- **Suficient per a 50k chunks**: el rendiment es bo per a volums petits-mitjans.
- **Comunitat gran**: molta documentacio, exemples, integracions.
- **API senzilla**: 3 linies per fer una cerca.
- **Ideal per homelab**: poca complexitat operacional.

**Arguments a favor de Qdrant**:
- **Escalabilitat real**: pot gestionar milions de vectors sense degradacio.
- **Produccio-ready**: pensat per a aplicacions d'alta disponibilitat.
- **API rica**: filtres complexos, geo-cerca, payloads arbitraris.
- **Mes rapid a escala**: 2-5x mes rapid que ChromaDB amb 100k+ vectors.
- **Snapshots i backups**: facilitat per fer copies de seguretat.
- **Replicacio**: alta disponibilitat.

**Cas concret del BernatLab**:
- Actualment: 5k-50k chunks.
- A 6 mesos vista: pot ser 100k.
- A 1-2 anys vista: pot ser 200k+.

**Tria final**: **Qdrant**, amb un periode de transicio. Argument:

El BernatLab esta creixent. ChromaDB avui es suficient, pero d'aqui un any pot ser el coll d'ampolla. Si començo amb ChromaDB, haure de migrar a Qdrant mes endavant (cosa que sempre es dolorosa). Si començo amb Qdrant, tinc marge de creixement i la complexitat adicional es acceptable per a un homelab seriós.

**Pla de transicio**:
1. Setmana 1-2: instal·lar Qdrant amb Docker al costat de ChromaDB.
2. Setmana 3-4: indexar la mateixa col·leccio a les dues DB.
3. Comparar rendiment i qualitat.
4. Decidir: si ChromaDB aguanta el ritme, quedar-s'hi. Si no, canviar.

**Argument contrari (per ChromaDB)**: "no optimitzis prematurament". Si ChromaDB aguanta 50k-100k chunks amb bona latencia, no cal complicar-se. La complexitat operacional te un cost (updates, monitoring, backups) que no es trivial.

**Conclusio honesta**: es una decisio valida qualsevol de les dues. ChromaDB es la tria mes conservadora; Qdrant es la tria mes visionaria. Jo trio Qdrant perque vull un sistema que escali sense grans canvis, pero ChromaDB es perfectament viable per anys.

---

## Que fer si has fallat moltes preguntes

- **10-12 encerts**: repassa la seccio del resum sobre ChromaDB vs alternatives.
- **7-9 encerts**: fes l'exercici practic per veure ChromaDB en accio.
- **0-6 encerts**: comença pel Pas 2 (indexar 10 documents) i la cerca basic, es molt intuitiu.

## Que fer si has encertat totes

- Passa al **Capitol 8** (RAG implementacio completa).
- O investiga altres vector DB: Weaviate, Milvus, Vespa.
- O llegeix sobre "vector quantization" (PQ, SQ) per comprimir embeddings.
