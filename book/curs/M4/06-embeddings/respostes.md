# Respostes - Capitol 6: Embeddings

> Mira les respostes DESPRES d'haver fet el qüestionari.

## Pregunta 1: Que es un embedding?

**Resposta correcta**: Un vector numeric que representa el significat d'un text.

**Explicacio**: Un embedding es una llista de 384-1536 numeros que "codifica" el significat d'un text. Es el resultat de passar el text per una xarxa neuronal entrenada per aquesta tasca. Es el cor de RAG i de moltes altres aplicacions modernes.

---

## Pregunta 2: Dimensions d'un embedding?

**Resposta correcta**: 384-1536.

**Explicacio**: Els models moderns produeixen embeddings entre 384 (all-MiniLM-L6-v2) i 3072 dimensions (text-embedding-3-large). Mes dimensions permeten capturar mes subtilitat pero ocupen mes memoria. El sweet spot son 768.

---

## Pregunta 3: Que mesura la semblança cosinus?

**Resposta correcta**: El grau de semblança entre dos vectors (i per tant, entre dos textos).

**Explicacio**: La semblança cosinus es una funcio matematica que ens dona un valor entre -1 i 1 segons com d'apuntats estan dos vectors. Si apunten en la mateixa direccio (mateix significat), el valor es 1. Si son perpendiculars (gens relacionats), es 0. Si apunten en direccions oposades (significats oposats), es -1.

---

## Pregunta 4: Valor de "molt semblant"?

**Resposta correcta**: 0.85.

**Explicacio**: Per convencio, valors entre 0.7 i 0.9 es consideren "molt semblants" o quasi identics. 0.85 es el lindar habitual per considerar que dos textos parlen del mateix. Per sota de 0.5 ja son temes diferents.

---

## Pregunta 5: Model d'embeddings local?

**Resposta correcta**: nomic-embed-text.

**Explicacio**: Ollama te diversos models d'embeddings, entre ells `nomic-embed-text` (768 dimensions, 137M parametres). Es open source, bo, i funciona perfectament en local. BERT-base es un model de llenguatge general (no nomes embeddings). Stable Diffusion genera imatges. Whisper transciu audio.

---

## Pregunta 6: Llibreria Python estandard?

**Resposta correcta**: sentence-transformers.

**Explicacio**: `sentence-transformers` es la llibreria Python de referencia per generar embeddings localment. Permet usar centenars de models de HuggingFace amb una sola API. Funciona amb CPU i GPU. Es la opcio mes flexible per a qui vulgui anar mes enlla d'Ollama.

---

## Pregunta 7: Dimensions d'all-MiniLM-L6-v2?

**Resposta correcta**: 384.

**Explicacio**: El nom ja ho diu: L6 vol dir 6 capes, MiniLM es la variant petita, 6 es l'arquitectura. Les 384 dimensions el fan rapidissim pero menys preciss que models de 768+. Es ideal per a prototips i volums grans.

---

## Pregunta 8: Sweet spot per dimensions?

**Resposta correcta**: 768.

**Explicacio**: 768 dimensions es el punt d'equilibri entre qualitat, velocitat i memoria. Models de 768 (com `nomic-embed-text` o `all-mpnet-base-v2`) son molt bons i prou rapids per a la majoria d'usos. Pujar a 1024 o 1536 nomes compensa en casos especifics.

---

## Pregunta 9 (oberta): Per que els embeddings cerquen per significat?

**Resposta model**:

La diferencia fonamental es la representacio:

**Cerca tradicional per paraules** (BM25, LIKE en SQL):
- Busca coincidencies exactes de paraules.
- Si busques "rega", nomes troba textos amb la paraula "rega".
- No enten sinonims: "sistema d'aigua", "humitat del terra", "goteig" son conceptes relacionats pero no son la paraula "rega".
- Fragil: si el text diu "l'electrovàlvula s'obre" i tu busques "activar el reg", no trobaras res.

**Cerca per embeddings**:
- Cada text es converteix en un vector de 768 numeros que representa el seu significat complet.
- Textos amb significat semblant tenen vectors propers en l'espai.
- Si busques "com controlo l'aigua dels tomàquets", el sistema trobara textos que parlen de "reg automatic", "electrovàlvula", "humitat del terra", etc. - encara que cap d'ells contingui la paraula "aigua" o "tomàquets" exactament.

**Exemple concret amb l'Hort Osona**:
- Tens 1000 lectures de sensors emmagatzemades.
- L'usuari pregunta: "Quan va ploure per ultima vegada?"
- Cerca per paraules: nomes trobara les lectures que continguin "pluja" o "ploure".
- Cerca per embeddings: trobara lectures amb "humitat alta", "canvi brusc pressio", "registre del pluviometre", etc. - encara que cap digui literalment "pluja".

Es la diferencia entre un motor de cerca dels 90 i un de modern. Els embeddings entenen la intencio darrere la pregunta, no nomes les paraules.

---

## Pregunta 10 (oberta): Decissions per a 10.000 articles

**Resposta model**:

**Tria de model**: usaria `nomic-embed-text` (768 dimensions) per varies raons:

1. **Qualitat**: 768 dimensions es el sweet spot. Mes ja no aporta gaire, menys perd qualitat.
2. **Velocitat**: amb CPU de la RPi 4, calcular 10.000 embeddings trigaria 2-4 hores amb nomic-embed-text. Amb un de 1536 dimensions, trigaria 4-8 hores. No compensa.
3. **Memoria**: cada embedding ocupa 768 * 4 bytes = 3 KB. Per a 10.000 articles, son 30 MB. Cap problema.
4. **Idioma**: nomic-embed-text esta entrenat en multiples idiomes, inclos el catala (no perfecte pero acceptable).
5. **Open source**: el puc fer correr en local, sense costos d'API.
6. **Suport actiu**: mantingut per Nomic AI, actualitzacions regulars.

**Alternativa** (`mxbai-embed-large`, 1024 dimensions): nomes si la qualitat es critica i tinc temps per re-indexar.

**Estrategia per a 10.000 articles**:

1. **Pre-processament**: netejar cada article (treure HTML, headers repetits, peu de pagina).
2. **Chunking**: cada article de 1000-5000 paraules el parteixo en chunks de 500 paraules amb 50 de solapament. Aixi obtinc 20.000-100.000 chunks.
3. **Calcul en batch**: passo tots els chunks pel model en lots de 32 o 64. En una RPi 4 trigaria 6-12 hores. Millor fer-ho en batches durant la nit.
4. **Guardar a ChromaDB o FAISS**: a mes de l'embedding, guardo metadades (titol, seccio, data, url).
5. **Re-indexacio automatica**: un script que cada nit comprova si hi ha articles nous i els indexa.

**Optimitzacions**:
- Usar `float16` en lloc de `float32` per estalviar memoria (perd un xic de precisio).
- Normalitzar els vectors per accelerar la cerca.
- Considerar una indexacio jerarquica (HNSW) si la base creix.

**Cost total**: nomes electricitat. Uns 0.50 € d'electricitat per indexar els 10.000 articles. Molt mes barat que qualsevol servei comercial.

---

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: rellegir el resum, sobretot la seccio de semblança cosinus.
- **3-4 encerts**: fes l'exercici practic, veuras els valors en accio.
- **0-2 encerts**: rellegir tot el resum abans de seguir.

## Que fer si has encertat totes

- Passa al **Capitol 7** (Vector databases).
- O fes el **repte**: indexa tota la documentacio del projecte BernatLab i crea una API de cerca per significat.
