# Respostes - Capitol 8: RAG - implementacio completa

> Mira les respostes DESPRES d'haver fet el qüestionari.

## Pregunta 1: Fases del pipeline RAG

**Resposta correcta**: 5 (carregar, chunking, embeddings, query, generacio).

**Explicacio**: Un pipeline RAG te cinc passes principals: carregar els documents, partir-los en chunks, calcular embeddings i indexar, fer la cerca quan arriba una pregunta, i generar la resposta amb el LLM. Es poden simplificar o ampliar, pero aixo es el flux basic.

---

## Pregunta 2: Per que cal chunking?

**Resposta correcta**: Perque els documents llargs no caben al contexte del LLM.

**Explicacio**: Un model de 3B te una finestra de 4-8k tokens. Un document de 50 pagines ocupa desenes de milers de tokens. Cal partir-lo en fragments petits que càpiguen al contexte.

---

## Pregunta 3: Mida tipica del chunk

**Resposta correcta**: 200-1000 caracters.

**Explicacio**: Depen del cas pero el sweet spot es 300-500. Massa petit perd contexte. Massa gran dilueix la informacio.

---

## Pregunta 4: Overlap

**Resposta correcta**: Que dos chunks consecutius comparteixen algunes paraules.

**Explicacio**: L'overlap (10-20% de la mida del chunk) garanteix que una idea que esta al limit de dos chunks no es perdi. Es una xarxa de seguretat.

---

## Pregunta 5: Primer pas del pipeline

**Resposta correcta**: Carregar i indexar els documents.

**Explicacio**: Sense documents indexats, no podem cercar res. Es el "preparacio del rebost" abans de poder cuinar.

---

## Pregunta 6: Que retorna `collection.query()`

**Resposta correcta**: Els N chunks mes semblants a la pregunta.

**Explicacio**: Es una cerca per semblança. Retorna els IDs, els textos, les metadades i les distancies. Tu tries quants vols amb `n_results`.

---

## Pregunta 7: Parametre n_results

**Resposta correcta**: n_results.

**Explicacio**: Controla quants chunks retorna la cerca. El valor optimitza entre context complet (mes chunks) i precisio (menys pero mes rellevants). Sweet spot: 3-5.

---

## Pregunta 8 (oberta): Ordre de les passes

**Resposta model**:

L'ordre es importantissim perque **cada pas depen de l'anterior**, com en una cadena de muntatge.

**Si intentessim fer la cerca ABANS d'indexar**, obtindriem un error: "la col·leccio esta buida". No hi ha res a cercar. Analogia: si vols cuinar una sopa, primer necessites tenir ingredients a la nevera. No pots cuinar-la al supermercat.

L'ordre logic es:

1. **Carregar** els documents: llegir els fitxers del disc i carregar-los a memoria. Sense aixo, no tenim res a processar.

2. **Chunking**: partir els documents en fragments. Sense chunks, no podem indexar de manera eficient ni cercar amb precissio.

3. **Calcul d'embeddings** (indexacio): convertir cada chunk a un vector numeric. Sense embeddings, ChromaDB no pot fer cerca per semblança.

4. **Emmagatzematge** dels vectors: persistir a ChromaDB. Si nomes calculem els embeddings pero no els guardem, els perdem en tancar el programa.

5. **Consulta** (query): rebre la pregunta de l'usuari. Aquest es el moment en que el sistema comença a "treballar" per a l'usuari.

6. **Cerca** dels chunks rellevants: comparar l'embedding de la pregunta amb tots els embeddings guardats. Retorna els top-N.

7. **Generacio** de la resposta: passar els chunks al LLM amb el prompt adequat per obtenir la resposta final.

**Consequencia practica**: si canvien els documents (per exemple, afegeixes una nova fitxa de cultiu), cal tornar a executar els passos 1-4 per aquesta nova fitxa. Es pot fer incrementalment ( nomes els nous) o re-indexar tot.

---

## Pregunta 9 (oberta): Estrategies de chunking

**Resposta model**:

**Chunking per caracters**:
- Simplement talla a X caracters.
- Pro: simple, predictable.
- Contres: talla paraules, talla idees, perd contexte.
- Us: nomes per a proves molt basiques.

**Chunking per paragrafs**:
- Cada paragraf es un chunk.
- Pro: mante la coherencia local (cada paragraf tracta un tema).
- Contres: mida variable (un paragraf pot ser 50 caracters o 500).
- Us: be per a articles, blogs, correus.

**Chunking per seccions**:
- Cada seccio (H1, H2, H3) es un chunk.
- Pro: mante l'estructura del document, cada seccio es tematicament coherent.
- Contres: seccions poden ser molt llargues o molt curtes.
- Us: **ideal per a fitxes tecniques i manuals**, com les de l'Hort Osona.

**Per a l'Hort Osona (fitxes de cultiu)**:
- Les fitxes tenen estructura clara: ## Sembrament, ## Reg, ## Varietats, etc.
- Cada seccio es un tema atomica.
- Aixo es perfecte per a chunking per seccions.
- Si una seccio es massa llarga (>1500 caracters), la parteixo per paragrafs.

**Recomanacio final**: chunking **jerarquic**. Primer per seccions. Si alguna seccio passa de 1500 caracters, la parteixo per paragrafs. D'aquesta manera mantenim l'estructura tematica sense chunks massa grans.

---

## Pregunta 10 (oberta): Mida del chunk i qualitat

**Resposta model**:

La relacio es **no linial** amb un sweet spot clar.

**Chunks massa petits (<200 caracters)**:
- Poca informacio per chunk. Un chunk pot contenir nomes una frase.
- Calen molts chunks per cobrir un tema.
- Problema: el LLM pot perdre la "visio de conjunt".
- Exemple: un chunk de 100 caracters sobre tomàquets potser nomes es la frase "Els tomàquets necessiten sol directe". Sense contexte addicional.

**Chunks massa grans (>1500 caracters)**:
- Massa informacio. Inclou contexte irrellevant.
- Si pas 5 chunks de 2000 caracters al LLM, son 10k tokens. Molts per a un 3B.
- A mes, la informacio rellevant queda "diluida" en molt texte.
- Exemple: un chunk de 2000 caracters sobre tomàquets pot incloure pargrafs sobre plagues, reg, recol·leccio. Si la pregunta es nomes sobre sembrament, el 80% del contexte es irrellevant.

**Sweet spot (300-500 caracters)**:
- Cada chunk conte un concepte o subtema complet.
- Nomes calen 3-5 chunks per cobrir una pregunta.
- 3 chunks * 500 caracters = 1500 caracters = ~2.5k tokens. Perfecte per a models 3B.
- Bona relacio senyal/soroll.

**Aplica al BernatLab**:
- Fitxes de cultiu: chunks de 300-500 caracters (1-2 paragrafs).
- Logs: chunks individuals (1 log per chunk).
- Correus: 1 correu per chunk.
- Articles llargs: 1-2 paragrafs per chunk.

**Monitoritzacio**: val la pena provar diferents mides amb el teu cas concret i mesurar la qualitat de les respostes.

---

## Pregunta 11 (oberta): 50 pagines, chunks i cost

**Resposta model**:

Fem el calcul per un document de 50 pagines.

**Mida**:
- Una pagina tipica (lletra normal, 11pt, marges estandard) = 250-300 paraules = ~1500-2000 caracters.
- 50 pagines = 75.000-100.000 paraules = 450.000-600.000 caracters.
- Aixo es aproximadament un llibre curt.

**Chunks (amb 500 caracters per chunk)**:
- 450.000 / 500 = 900 chunks.
- 600.000 / 500 = 1.200 chunks.
- **Promig: ~1.000 chunks**.

**Temps**:
- Calcular un embedding amb `nomic-embed-text` en una RPi 4: ~100-200ms.
- 1.000 chunks * 150ms = **150 segons = 2.5 minuts**.
- En un Mac M2 o servidor potent: ~20-30 segons.

**Cost economic (núvol)**:
- 1.000 chunks * 500 caracters = 500.000 caracters = ~750.000 tokens.
- OpenAI text-embedding-3: $0.00002 per 1k tokens = $0.015.
- **Menys de 2 centims per indexar 50 pagines**. Trivial.

**Cost d'emmagatzematge**:
- 1.000 vectors de 768 dimensions en float32 = 3 MB.
- Amb metadades i index HNSW: ~15-20 MB.
- **Trivial en qualsevol sistema modern**.

**Conclusio**: indexar 50 pagines es molt assequible. Fins i tot un llibre sencer (300 pagines = 6.000 chunks) trigaria uns 15 minuts i ocuparia 100 MB. 

**Al BernatLab**: podem indexar tota la base de coneixement de l'Hort Osona (unes 50-100 pagines) en menys de 5 minuts. I podem actualitzar-la cada setmana sense cost apreciable.

---

## Pregunta 12 (oberta): Context overflow

**Resposta model**:

El "context overflow" es un dels problemes mes comuns en RAG i pot tenir consequencies greus.

**Que passa**:
- El model te una finestra de context limitada (4k, 8k, 32k, etc.).
- Si passem mes text del que cap, el model trunca o ignora parts.
- Aixo pot passar de manera "silenciosa" (sense error) pero la resposta es dolenta.

**Senyals d'alerta**:
- El LLM comença a donar respostes incompletes o sense sentit.
- El LLM "inventa" informacio que no es al contexte.
- El LLM ignora la pregunta i respon sobre un altre tema.

**Exemple numeric**:
- Model 3B amb finestra de 4k tokens (~6k caracters).
- 10 chunks de 1.000 caracters = 10k caracters = ~15k tokens. **Overflow!**
- El model trunca a 6k caracters = nomes 6 chunks. Perdem 4 chunks.
- Pitjor encara: potser els 4 chunks que es perden son els mes rellevants!

**Solucions**:
1. **Controlar n_results**: nomes 3-5 chunks, no 10.
2. **Limitar mida del chunk**: 300-500 caracters en lloc de 1000+.
3. **Resumir el contexte abans**: un model petit fa un resum de 5 chunks en un de 1k tokens, que es pasa al model gran.
4. **Usar un model amb mes finestra**: els nous 3B ja tenen 8-16k de context.
5. **Re-ranking**: nomes passar els 2-3 millors chunks, no els 5.

**Al BernatLab**: com que uso un 3B amb 4-8k de context, vigilo que el total no passi de 3-4k tokens. Si passa, retallo chunks o canvio a un model amb mes finestra.

---

## Pregunta 13 (oberta): Actualitzacions incrementals

**Resposta model**:

La gestio d'actualitzacions es un tema practic molt important al BernatLab. Si cada setmana afegeixo un document, com ho gestiono?

**Opcio A: Re-indexar tot**:
- Cada vegada que hi ha un canvi, torno a indexar tots els documents.
- Pro: senzill, garantit, sempre coherent.
- Contres: lent si tens molts documents. 1000 chunks = 2-3 min. 10.000 = 20-30 min.

**Opcio B: Indexacio incremental**:
- Calculo embeddings nomes pels documents nous o modificats.
- Els afegixo a la col·leccio existent.
- Pro: rapid (1-2 segons per chunk).
- Contres: cal gestionar IDs, evitar duplicats, gestionar eliminacions.

**Estrategia al BernatLab**:

Usaria la **Opcio B (incremental)** amb un parell de millores:

1. **ID unic basat en hash**: per a cada document, calculo un hash del contingut. Si el hash canvia, es un document nou o modificat. Si es nou, l'afegeixo. Si es modificat, l'esborro i l'afegeixo de nou.

2. **Deteccio d'eliminacions**: comparo la llista actual de fitxers amb la llista anterior. Els que ja no existeixen, els elimino de la DB.

3. **Script nocturn**: un cron que cada nit revisa si hi ha canvis i actualitza nomes aquells.

4. **Re-indexacio completa setmanal**: per seguretat, un cop per setmana re-indexo tot. Es una "neteja de primavera" que garanteix consistencia.

**Exemple de script**:

```python
import os
import hashlib
from pathlib import Path

def hash_file(path):
    return hashlib.md5(path.read_bytes()).hexdigest()

# Obtenir estat actual dels fitxers
estat_actual = {}
for f in Path('./documents').rglob('*.md'):
    estat_actual[str(f)] = hash_file(f)

# Comparar amb l'estat anterior (guardat a un fitxer)
estat_anterior = carregar_estat_anterior()  # del fitxer

# Afegir nous i modificats
for path, hash in estat_actual.items():
    if path not in estat_anterior or estat_anterior[path] != hash:
        indexar_document(path)

# Eliminar els que ja no existeixen
for path in estat_anterior:
    if path not in estat_actual:
        eliminar_document(path)

guardar_estat(estat_actual)
```

Aixo es la base d'un sistema RAG que escala i es mantingui sol.

---

## Pregunta 14 (oberta): Metriques en produccio

**Resposta model**:

Cinc metriques essentials per un sistema RAG en produccio al BernatLab:

**1. Latencia de la consulta** (p95):
- Temps desde que l'usuari envia la pregunta fins que rep la resposta.
- Objectiu: <5 segons a la RPi 4.
- Alerta: si p95 >10 segons, hi ha un problema.
- Com medir: instrumentar el codi amb timestamps.

**2. Taxa d'errors**:
- Percentatge de consultes que fallen (excepcio, timeout, etc.).
- Objectiu: <1%.
- Alerta: si puja a 5%, algo esta trencat.
- Com medir: comptar errors vs total de consultes.

**3. Qualitat del retrieval** (relevance score):
- Distribucio de les semblances dels top-3 chunks retornats.
- Si la semblança mitjana baixa de 0.5, el sistema probablement no troba informacio rellevant.
- Alerta: si >30% de les consultes tenen semblança <0.4, cal revisar.
- Com medir: guardar les semblances de cada consulta.

**4. Mida de la base de dades**:
- Quant ocupa la DB al disc.
- Objectiu: <5 GB.
- Alerta: si passa de 8 GB en un sistema de 32 GB, cal netejar.
- Com medir: `du -sh ./chroma_db`.

**5. Temps de re-indexacio**:
- Quant trigem a afegir 1000 chunks nous.
- Objectiu: <30 min per a 1000 chunks.
- Alerta: si passa de 60 min, cal optimitzar.
- Com medir: instrumentar el procés d'indexacio.

**Implementacio**: un script Python que cada 5 minuts exporta aquestes metriques a un fitxer CSV o les envia a InfluxDB. Despres Grafana pot visualitzar-les i crear alertes automaticament.

**Exemple de sistema d'alertes**:

```python
# Pseudocodi
if latency_p95 > 10:
    alerta("RAG lent, revisar embeddings o model")
if error_rate > 0.05:
    alerta("Massa errors, revisar logs")
if avg_relevance < 0.5:
    alerta("Chunks irrellevants, revisar indexacio")
```

---

## Pregunta 15 (oberta): RAG simple vs sofisticat

**Resposta model**:

**Arguments a favor del RAG simple (ChromaDB, cerca basica)**:
- **Simplicitat operacional**: menys components, menys coses que poden fallar.
- **Suficient per al 80% dels casos**: la majoria de preguntes son simples i el RAG basic les respon be.
- **Menys cost**: no cal un model de re-ranking (que es un model addicional).
- **Menys memoria**: sense re-ranking, nomes cal el model d'embeddings i el LLM.
- **Facil de debug**: menys components, mes facil trobar on falla.

**Arguments a favor del RAG sofisticat (re-ranking + multi-query)**:
- **Millor recall**: el re-ranking millora 5-10% el percentatge de chunks rellevants trobats.
- **Millor per a casos edge**: preguntes complexes, ambigües, multi-tematica.
- **Robustesa**: el multi-query captura mes variacions de la pregunta.
- **Molt relevant per a dominis especialitzats**: medicina, legal, etc.

**Cost del sofisticat**:
- Model de re-ranking: 100-500M parametres adicionals, ~500MB de RAM.
- Multi-query: 2-3x mes cerques per consulta, ~3x mes latencia.
- Mes complexitat: mes codi, mes testing, mes manteniment.

**Tria final per al BernatLab**: **RAG simple** per defecte, amb un pla de sofisticacio si cal. Argument:

El 80% de les preguntes al BernatLab son simples ("quan plantar X?", "com regar Y?"). El RAG simple les respon perfectament. Per al 20% restant (preguntes complexes), puc millorar el prompt o afegir un pas de re-ranking nomes per a aquestes.

**Pla d'evolucio**:
1. Comencar amb RAG simple (ChromaDB, 3-5 chunks, LLM 3B).
2. Mesurar la qualitat amb un dataset de test.
3. Si la qualitat es bona (>80% d'encerts), quedar-s'hi.
4. Si la qualitat es justa, considerar re-ranking.
5. Multi-query nomes si veig que moltes preguntes fallen per "no trobar el chunk correcte".

**Alternativa**: el re-ranking es pot fer **a la carta**. En lloc d'aplicar-lo sempre, l'aplico nomes quan la semblança del top chunk es baixa (<0.6). Es un "fallback" sofisticat nomes per als casos diffcils.

---

## Que fer si has fallat moltes preguntes

- **10-12 encerts**: repassa el resum i fes l'exercici practic pas a pas.
- **7-9 encerts**: posa especial atencio al Pas 5 (avaluacio qualitativa) per entendre que funciona i que no.
- **0-6 encerts**: comença pel Pas 2-3 (crear documents i indexar), es la base de tot.

## Que fer si has encertat totes

- Passa al **Capitol 9** (privadesa de la IA).
- O investiga "agentic RAG": un sistema que pot decidir quan cal fer cerca, quan no, quan cal mes informacio.
- O implementa un sistema de feedback per millorar el RAG amb l'us.
