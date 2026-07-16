# Respostes - Capitol 5: Que es RAG

> Mira les respostes DESPRES d'haver fet el qüestionari.

## Pregunta 1: Que significa RAG?

**Resposta correcta**: Retrieval Augmented Generation.

**Explicacio**: Son les inicials en angles de "Generacio Augmentada per Recuperacio". El model "recupera" contexte rellevant d'una base de dades i l'afegeix al seu prompt abans de generar la resposta. Es la tecnica estandard per fer chatbots sobre dades propies.

---

## Pregunta 2: Problema que RAG resol?

**Resposta correcta**: Permetre al LLM respondre sobre dades que no va veure a l'entrenament.

**Explicacio**: Els LLMs nomes "saben" el que van aprendre durant l'entrenament. Si tens dades noves (o privades, com les de l'Hort Osona), el model no pot respondre sobre elles. RAG li dona el contexte rellevant a cada consulta, com si obrissis el llibre just abans de l'examen.

---

## Pregunta 3: Quantes fases te RAG?

**Resposta correcta**: 3 fases (indexacio, query, generacio).

**Explicacio**:
- **Indexacio**: un sol cop. Documents -> chunks -> embeddings -> vector DB.
- **Query**: cada pregunta. Pregunta -> embedding -> cerca -> top-K chunks.
- **Generacio**: prompt + chunks -> LLM -> resposta.

---

## Pregunta 4: Que es un chunk?

**Resposta correcta**: Un fragment de text en que partim un document.

**Explicacio**: Els documents llargs (100 pagines) no caben a la finestra de context. Els partim en trossos (chunks) de 200-1000 tokens. Cada chunk es indexat per separat i pot ser recuperat individualment.

---

## Pregunta 5: Quants chunks al LLM?

**Resposta correcta**: Entre 3 i 5.

**Explicacio**: Cada chunk ocupa 200-1000 tokens. Si n'enviem 20, omplim la finestra de context. Amb 3-5 tenim prou contexte per respondre be sense saturar el model. Es el sweet spot entre cobertura i eficiencia.

---

## Pregunta 6: Quin NO es un component de RAG?

**Resposta correcta**: Compilador de Python.

**Explicacio**: Els components son Loader (carrega docs), Splitter (parteix), Embedder (vectoritza), Retriever (cerca), Generator (LLM), Vector DB (emmagatzema). Un compilador de Python no te res a veure amb RAG.

---

## Pregunta 7: Per a que serveix l'embedding?

**Resposta correcta**: Convertir text en un vector numeric que representa el significat.

**Explicacio**: Un embedding es una llista de 384-1536 numeros que representa el significat d'un text. Textos amb significat semblant tenen vectors propers. Es el que permet "cercar per significat" en lloc de "cercar per paraules exactes". Es el cor de RAG.

---

## Pregunta 8: Regla practica?

**Resposta correcta**: Comença per prompt engineering, afegeix RAG, i finalment fine-tuning.

**Explicacio**: Prompt engineering es gratis i rapid. Si no n'hi ha prou, afegeix RAG per donar contexte. Si encara cal un comportament molt especific, considera fine-tuning. Pero el 90% dels casos es resolen amb RAG.

---

## Pregunta 9 (oberta): Per que RAG funciona be amb models petits?

**Resposta model**:

La clau esta en entendre la diferencia entre dues coses que semblen iguals pero no ho son:

**"Saber moltes coses"**: un model de 70B parametres ha memoritzat (dins del que cap) molts coneixements durant l'entrenament. Pot respondre sobre historia, ciencia, codi... pero nomes sobre el que va llegir.

**"Tenir la informacio a la ma"**: un model de 3B amb RAG nomes ha memoritzat patrons basics de llenguatge. Pero si li dones els 3 paragrafs rellevants, pot raonar-hi perfectament.

Es la diferencia entre un examen a l'escola i un examen amb llibre obert:
- **Sense llibre**: nomes passa qui ha estudiat molt. Cal un "cervell gran" (model gran).
- **Amb llibre**: tothom pot trobar la resposta si sap on mirar. Nomes cal saber llegir i raonar (model petit + bon retrieval).

I aqui esta la gracia de RAG: el "saber llegir" es molt mes facil d'aconseguir (un 3B ja en te) que el "saber-ho tot" (cal un 70B o mes). A mes, el llibre es pot actualitzar cada dia. El cervell, no.

**Limitacio**: si el llibre es molt gran (10 milions de pagines) i la pregunta es ambigua, costa trobar el paragraf correcte. Pero per a la majoria de casos reals, 3-5 chunks son suficients.

**Conclusio**: un 3B amb bon RAG pot superar un 70B sense RAG. Es la democratitzacio de la IA: ja no cal tenir el model mes gran, sino el millor contexte.

---

## Pregunta 10 (oberta): Assistent per a projectes GitHub

**Resposta model**:

Tria: **RAG**, sens dubte. I ara explico el per que i els passos.

**Per que RAG i no fine-tuning?**
- **Volum de dades**: un repo amb 1000 commits i 50 fitxers de documentacio es perfecte per a RAG. No cal re-entrenar res.
- **Canvis frequents**: els repos canvien cada setmana. Amb RAG, nomes cal re-indexar els fitxers nous. Amb fine-tuning, caldria re-entrenar constantment.
- **Cost**: un fine-tuning costa centenars d'euros i dies. RAG es pot muntar en una tarda.
- **Font verificable**: puc dir "aquesta resposta ve del fitxer README del projecte X, linia 23". Amb fine-tuning, no se sap d'on ha tret la resposta.
- **Privadesa**: el meu codi no surt del meu servidor. Cap empresa externa no el veu.

**Passos que faria**:

1. **Recollir els documents**:
   - Tots els `README.md`, `CHANGELOG.md`, fitxers de documentacio.
   - Issues i PRs importants (com a text pla).
   - Comentaris de les funcions principals (docstrings).
   - Resums de releases (git tags).

2. **Preparar els fitxers**:
   - Netejar codi (treure imports, sintaxi irrelevant).
   - Mantenir estructura (titols, seccions, exemples).
   - Convertir a Markdown si cal.

3. **Indexar amb RAG**:
   - Chunking per seccions (200-500 tokens).
   - Embeddings amb `nomic-embed-text` o similar.
   - Guardar a ChromaDB o FAISS.

4. **API de consulta**:
   - Endpoint `/api/ask` que rep una pregunta.
   - Calcula embedding, busca top-3-5 chunks.
   - Constrou el prompt amb contexte.
   - Crida Ollama amb `llama3.2:3b` o similar.

5. **Frontend** (opcional):
   - Una web senzilla amb un quadre de text.
   - Mostra la resposta i els chunks utilitzats (per verificar).

6. **Re-indexacio automatica**:
   - Un cron job que cada nit comprova si hi ha canvis als repos.
   - Si n'hi ha, re-indexa nomes els fitxers modificats.

**Alternativa fine-tuning**: nomes si el model ha d'aprendre un estil de resposta molt especific ("respon sempre amb un to irònic", "sempre cita 3 alternatives"). Pero per a "saber sobre el meu projecte", RAG es imbatible.

---

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: rellegir el resum, sobretot el diagrama de les 3 fases.
- **3-4 encerts**: practica amb l'exercici, veuras el flux en accio.
- **0-2 encerts**: torna a llegir el resum sencer abans de seguir.

## Que fer si has encertat totes

- Passa al **Capitol 6** (Embeddings, el cor de RAG).
- O fes el **repte**: indexa la documentacio del BernatLab i crea un assistent que t'ajudi a recordar on has ficat cada cosa.
