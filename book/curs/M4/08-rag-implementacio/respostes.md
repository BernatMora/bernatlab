# Respostes - Capitol 8: RAG - implementacio completa

## Pregunta 1: Quants passos te el pipeline RAG?

**Resposta correcta**: 5.

**Explicacio**: El pipeline RAG te 5 passos basics: (1) generar l'embedding de la pregunta, (2) cercar els fragments mes semblants a ChromaDB, (3) preparar el prompt amb el contexte, (4) enviar al LLM, (5) retornar la resposta. Tots son necessaris - si en falles un, el sistema no funciona.

---

## Pregunta 2: Primer pas del pipeline?

**Resposta correcta**: Calcular l'embedding de la pregunta.

**Explicacio**: Abans de poder cercar res, cal traduir la pregunta a un vector numeric. Si no, ChromaDB no pot comparar-la amb els embeddings dels documents. Es l'inici de tot.

---

## Pregunta 3: Model d'embeddings?

**Resposta correcta**: nomic-embed-text.

**Explicacio**: `nomic-embed-text` es bo, rapid, te 768 dimensions, i es pot descarregar amb `ollama pull nomic-embed-text`. Es l'estandard recomanat per a homelab. `llama3.2` es per a generar text, no per a embeddings.

---

## Pregunta 4: Sweet spot de chunk size?

**Resposta correcta**: 300-800 paraules.

**Explicacio**: Chunks massa petits fan que el LLM perdi contexte. Chunks massa grans fan que hi hagi massa texte irrelevant. 300-800 es l'equilibri que funciona be per a la majoria de casos.

---

## Pregunta 5: Quants fragments retornar?

**Resposta correcta**: 3-5.

**Explicacio**: k=1 perd contexte, k=10+ fa que el LLM es confongui amb masses fragments. 3-5 es el sweet spot: prou contexte per respondre, no tant que saturi el prompt.

---

## Pregunta 6: Que pasa sense `path=`?

**Resposta correcta**: Les dades es perden al tancar.

**Explicacio**: ChromaDB, per defecte, nomes te les dades a memoria. Si no passes `path=./chroma_db` al `PersistentClient`, quan tanquis el script tot desapareix. Es l'error mes comu del capitol.

---

## Pregunta 7 (oberta): Descriu els 5 passos

**Resposta model**:

El pipeline RAG te 5 passos que cal entendre be perque tots son essencials:

1. **Embedding de la pregunta**: transformem el texte de la pregunta en un vector numeric. Aixi podem comparar-lo matematicament amb els vectors dels documents. Si no fessim això, no podriem fer cap cerca.

2. **Cerca a ChromaDB**: donat el vector de la pregunta, busquem els K vectors mes propers (mes semblants). ChromaDB fa la cerca de forma eficient. Si no cerquem, no tenim contexte.

3. **Preparar el prompt**: ajuntem el contexte trobat amb la pregunta de l'usuari en un prompt ben estructurat. Cal dir al LLM que nomes usi aquella informacio per evitar que inventi coses.

4. **Enviar al LLM**: el LLM llegeix el prompt i genera una resposta coherent basada en el contexte. Sense contexte, el LLM nomes pot inventar.

5. **Retornar la resposta**: donem la resposta a l'usuari, idealment amb les fonts perque pugui verificar.

Si falla qualsevol pas, el sistema no funciona be: sense embedding no cerquem, sense cerca no tenim contexte, sense contexte el LLM inventa, etc.

---

## Pregunta 8 (oberta): Mescles de models d'embeddings

**Resposta model**:

Si barreges dos models d'embeddings, **la cerca falla silenciosament**:

- **Dimensions diferents**: si un model te 384 dimensions i l'altre 768, ChromaDB pot donar un error o retornar resultats random. Es el primer senyal.

- **Vectors inconsistents**: encara que les dimensions coincideixin, dos models entrenats de forma diferent produeixen vectors NO comparables. "Tomàquet" pot ser [0.1, 0.5, ...] en un model i [0.9, -0.3, ...] en un altre per al mateix significat. La cerca retorna coses sense sentit.

**Com ho detectaries**:

- Resultats de cerca random o buits quan n'hauries de tenir.
- Distancies totes molt similars (perque els vectors son d'espais diferents).
- Comparar manualment els embeddings de la mateixa frase amb dos models - han de ser molt diferents.

**Solucio**: triar UN sol model al principi (ex: `nomic-embed-text`), i **re-indexar tot** si vols canviar. No es pot fer una transicio parcial.

---

## Pregunta 9 (oberta): k=3 o k=5 per a Hort Osona?

**Resposta model**:

Per a un cas d'horticultura amb fragments curts (300-500 paraules), recomano **k=3 o k=5 depen del cas**:

- **k=3** si els fragments son **temàticament clars** (una fitxa de cultiu toca un sol tema) i la pregunta es especifica ("quan es sembra el calçot?"). Menys contexte = menys confusio = resposta mes enfocada.

- **k=5** si la pregunta es **oberta o pot tocar varies subtemes** ("quines plantes son bones companyes?"). Mes contexte = mes probabilitat de trobar la resposta.

**Truc**: per a Hort Osona, que te 76 fitxes curtes, k=3 funciona be per defecte. Si la resposta es pobra, puja a k=5. Mai k>7 perque el LLM es perd.

**Compte amb la velocitat**: la RPi es lenta. k=3 es mes rapid que k=5 perque el prompt es mes petit.

---

## Pregunta 10 (oberta): Optimitzacions per a RPi lenta

**Resposta model**:

Si la RPi va lenta, pots optimitzar en varies capes:

1. **Model mes petit**: canviar `llama3.2` (3B) per `phi3:mini` (2.3B) o `gemma:2b`. Es 2-3x mes rapid amb perdua minima de qualitat.

2. **Embedding mes rapid**: `all-minilm` (22M params) en comptes de `nomic-embed-text` (137M). Es 5x mes rapid.

3. **k mes petit**: passar de k=5 a k=3. El prompt es mes petit, el LLM triga menys.

4. **Chunks mes petits**: 300 paraules en lloc de 500. Mes chunks, pero cada un es mes rapid d'embedir.

5. **Cache d'embeddings**: guardar els embeddings a disc per no recalcular. ChromaDB ja ho fa, pero pots afegir una capa propia.

6. **Streaming**: mostrar la resposta paraula a paraula. L'usuari veu progres nomes comença.

7. **Limitar tokens de sortida**: afegir `options={"num_predict": 200}` al LLM. Limita la longitud de la resposta.

8. **Filtrar abans de cercar**: si saps que la pregunta es sobre tomàquets, primer filtra a ChromaDB per `source=*tomàquet*` i nomes cerca dins.

Combinant 2-3 d'aquestes, la RPi pot anar 5x mes rapid.

---

## Què fer si has fallat moltes

- **5-8 encerts**: Repassa el resum i l'exercici practic. El codi es la clau per entendre el pipeline.
- **3-4 encerts**: Torna a fer l'exercici pas a pas, observant cada sortida. El debugging es on s'aprenen les coses.
- **0-2 encerts**: Comença pel basics: que es un embedding (cap 6) i ChromaDB (cap 7). Despres torna aqui.
