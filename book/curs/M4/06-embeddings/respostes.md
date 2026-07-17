# Respostes - Capitol 6: Embeddings

> Mira les respostes DESPRES d'haver fet el qüestionari.

## Pregunta 1: Que es un embedding?

**Resposta correcta**: Un vector numeric que representa el significat d'un text.

**Explicacio**: Un embedding es una llista de numeros que captura el significat del text. Es la manera que tenen les maquines de "mesurar" la semblança entre textos de forma matematica.

---

## Pregunta 2: Dimensions tipiques

**Resposta correcta**: 384, 768, 1024 o 1536.

**Explicacio**: Depen del model. Els petits tenen 384 (all-MiniLM), els mitjans 768 (nomic-embed-text, BERT base), els grans 1024-1536 (mxbai-embed-large, OpenAI text-embedding-3).

---

## Pregunta 3: Embeddings "propers"

**Resposta correcta**: Que els vectors son similars (mateixa direccio).

**Explicacio**: Dos texts amb significat semblant tindran vectors que apunten en la mateixa direccio (angle petit). Es pot mesurar amb la semblança cosinus.

---

## Pregunta 4: Metrica estandard

**Resposta correcta**: Semblança cosinus.

**Explicacio**: Cosinus mesura l'angle entre dos vectors. Es la metrica estandard per a embeddings perque es independent de la magnitud (norma) del vector.

---

## Pregunta 5: Rang de la semblança cosinus

**Resposta correcta**: -1 a 1.

**Explicacio**: -1 = vectors oposats. 0 = perpendiculars (no relacionats). 1 = identics. En embeddings de text, els valors habituals son 0.5-0.95.

---

## Pregunta 6: Model d'embeddings a Ollama

**Resposta correcta**: nomic-embed-text.

**Explicacio**: Es el mes popular per a RAG. 137M parametres, 768 dimensions, bona relacio qualitat/velocitat. mxbai-embed-large es lleugerament millor pero mes lent.

---

## Pregunta 7: "Gat" vs "moix"

**Resposta correcta**: Son molt semblants perque volen dir el mateix.

**Explicacio**: Un bon model d'embeddings enten sinonims i variants. "Gat" i "moix" son la mateixa cosa al diccionari. Els seus embeddings estaran a prop. Aixo es el que permet cerques per significat.

---

## Pregunta 8 (oberta): Que representa cada dimensio?

**Resposta model**:

Cada dimensio d'un embedding de 768 numeros **no te una correspondencia directa amb una paraula o concepte**. Es mes aviat una "component abstracta" del significat.

Pensa-ho aixi: si representessim un color amb 3 dimensions (RGB), cada dimensio es un color basic (vermell, verd, blau). Però el significat d'un text es molt mes ric. Les 768 dimensions son com "components de significat" que el model ha descobert automaticament durant l'entrenament.

Per exemple, podria ser que:
- La dimensio 23 capturi "animat vs inanimat".
- La dimensio 156 capturi "positiu vs negatiu".
- La dimensio 421 capturi "accio culinaria".

Pero **no podem saber exactament que captura cada dimensio sense analisi detallat**. Es una caixa negra. Aixo es una limitacio important: podem usar els embeddings pero no podem interpretar-los directament.

Aixo te implicacions:
- **No podem depurar** per que un embedding ha sortit d'una manera concreta.
- **No podem controlar** quines dimensions son mes importants per a la nostra tasca.
- **Podem confiar** en les propietats agregades (semblança entre textos) sense entendre la mecanica interna.

A la practica, els embeddings son eines opaques pero molt utils. Els usem per la seva potencia, no per la seva interpretabilitat.

---

## Pregunta 9 (oberta): Per que cosinus i no euclidea?

**Resposta model**:

La semblança cosinus es mes util que la distancia euclidea per **tres raons principals**:

**1. Es independent de la magnitud**. Dos textos poden ser "similars" en significat pero tenir longituds diferents. Per exemple, "el gat" i "el gat menja peix" son similars, pero el segon te mes paraules. La distancia euclidia entre els seus embeddings seria gran nomes per la diferencia de "magnitud", no per la diferencia de significat. La cosinus nomes mira l'angle, ignorant la magnitud.

**2. Es el que els models d'embeddings "volen"**. Quan entrenem un model d'embeddings, sovint normalitzem els vectors a norma 1 i optimitzem per semblança cosinus. Per tant, **la metrica per la qual sha optimitzat es la cosinus**. Usar euclidia seria com mesurar amb un regle la temperatura.

**3. Cas practic al BernatLab**: 
- "Alerta: CPU al 95%" vs "CPU 95%, posibles problemas" - similars semanticament, distancia euclidia gran.
- "Hola" vs "Adeu" - un sol token cadascun pero son oposats semanticament. La cosinus donara valor negatiu o proper a 0, l'euclidia donara valor petit (perque els vectors son petits). Confus.

**Excepcio**: la euclidia es pot usar en alguns contextos (com clustering k-means) on la magnitud tambe te significat. Pero per a la majoria d'usos RAG, cosinus es la opcio correcta.

---

## Pregunta 10 (oberta): Cal re-indexar si canvio el model?

**Resposta model**:

**Si, absolutament cal re-indexar tots els documents** quan canvies de model d'embeddings. I aixo te un cost important que cal considerar.

**Per que**: cada model te el seu propi "espai vectorial". Els embeddings son sequences de numeros que nomes tenen sentit **dins del model que les ha generat**. Si passes un text pel model A i pel model B, els dos vectors representen el mateix text pero en "idiomes" diferents. No es poden comparar.

**Consequences practiques**:
- Si tens 10.000 chunks indexats amb `nomic-embed-text` i vols canviar a `mxbai-embed-large`, cal:
  1. Re-llegir tots els 10.000 chunks.
  2. Calcular el nou embedding per cada un amb el nou model.
  3. Esborrar la base de dades vella.
  4. Carregar la nova.
  
  **Cost estimat**: 10.000 chunks * 0.1s per chunk = 1.000 segons = 17 minuts. No es molt, pero cal planificar.

- **A mes, durant la transicio**: el sistema RAG no pot funcionar (no hi ha base de dades). Cal un temps d'indisponibilitat.

- **Risc**: si hi ha un error durant la re-indexacio, pots perdre dades.

**Recomanacio**: tria el model d'embeddings amb cura desde el principi. Un canvi es car. Si vols provar un model nou, fes-ho en un entorn de test separat, no en produccio.

**Excepcio**: alguns models nous son "compatibles" amb versions anteriors (per exemple, les noves versions de nomic-embed-text). En aquest cas, la re-indexacio es opcional. Pero sempre verifica.

**Al BernatLab**: un cop triat `nomic-embed-text`, em comprometo a mantenir-lo. nomes canviare si un altre model es clarament 2x millor i val la pena el cost de re-indexar.

---

## Pregunta 11 (oberta): Word2Vec vs Sentence Transformers

**Resposta model**:

**Word2Vec (2013)**: genera un embedding per **paraula**. Es entrena mirant quines paraules apareixen juntes en textos. Limitation fonamental: **ignora el contexte**. La paraula "bank" te el mateix embedding tant si es "river bank" (marge del riu) com "bank account" (compte bancari).

**Sentence Transformers (2019+)**: genera un embedding per **frase o paragraf**. Usa arquitectures com BERT o similars que entenen el contexte. Per tant:
- "I went to the bank to deposit money" -> un embedding.
- "I sat on the river bank" -> un embedding diferent.
- Les dues frases tenen la paraula "bank" pero embeddings molt diferents perque el contexte es diferent.

**Per que Word2Vec ha quedat obsolet**:
- No enten polisemia (paraules amb multiples significats).
- No enten sintaxi (l'ordre de les paraules).
- No captura relacions complexes entre paraules.

**Exemple al BernatLab**:
- Amb Word2Vec: "sensor" sempre te el mateix embedding, tant si es "sensor de temperatura" com "sensor de presencia".
- Amb Sentence Transformers: les dues frases tindran embeddings diferents, i la cerca sera molt mes precisa.

**Limitacio dels Sentence Transformers**: son mes lents i ocupen mes memoria que Word2Vec. Però la diferencia de qualitat val infinit la pena.

**Conclusio**: al BernatLab, sempre uso Sentence Transformers (o mes moderns). Word2Vec nomes te sentit historic o per a aplicacions molt especifiques on el contexte no importa.

---

## Pregunta 12 (oberta): Mida del model d'embeddings

**Resposta model**:

La relacio entre mida i qualitat **es similar a la dels LLMs**: mes gran = millor, pero amb rendiments decreixents.

**Punts de referència**:
- **all-MiniLM (22M params, 384 dim)**: rapidissim, qualitat acceptable. Bo per a volums molt alts o hardware modest.
- **nomic-embed-text (137M params, 768 dim)**: bon equilibri. Es el "sweet spot" per a la majoria.
- **mxbai-embed-large (335M params, 1024 dim)**: millor qualitat pero mes lent. Bo per a aplicacions on la precisio es critica.
- **OpenAI text-embedding-3-large (>1B params, 3072 dim)**: el millor disponible comercialment, pero te cost economic.

**Mes gran sempre es millor?** No exactament. A partir de certa mida, els guanys son marginals. La diferencia entre MiniLM i nomic-embed es molt notable. La diferencia entre nomic-embed i mxbai-embed es mes subtil. La diferencia entre mxbai-embed i un de 500M es negligible per a la majoria d'usos.

**Consideracions al BernatLab**:
- **Si la base de dades es petita** (<10k chunks): `nomic-embed-text` es perfecte. Qualitat alta, rapid.
- **Si la base de dades es gran** (>100k chunks): `all-MiniLM` pot ser mes rapid i ocupar menys memoria, amb qualitat acceptable.
- **Si necessites la millor precisio**: `mxbai-embed-large`, assumint el cost en temps i memoria.
- **Si el hardware es limitat** (RPi 4, 4 GB): `all-MiniLM` es la opcio realista.

**Sweet spot recomanat**: `nomic-embed-text` per defecte. Es el que uso al BernatLab.

---

## Pregunta 13 (oberta): Clustering de correus amb embeddings

**Resposta model**:

Per comparar 1.000 correus i trobar temes comuns, el flux amb embeddings seria:

**Pas 1: Calcular embeddings**. 1.000 correus * 0.05s per correu amb nomic-embed-text = 50 segons. Trivial. Emmagatzemar els 1.000 vectors de 768 dimensions en un array NumPy ocupa uns 3 MB.

**Pas 2: Matriu de semblances**. Calcular 1.000 * 1.000 = 1.000.000 de semblances cosinus. Amb NumPy vectoritzat, son uns 2-5 segons. Trivial.

**Pas 3: Clustering**. Aplicar k-means o DBSCAN per agrupar correus similars:
- K-means: cal especificar K. Bones practiques: K=5-10 temes. Triga uns segons.
- DBSCAN: no cal K, troba el nombre de grups automaticament. Pot trigar una mica mes.

**Pas 4: Extreure temes**. Per cada grup, puc:
- Calcular l'embedding promig (centroide).
- Trobar el correu mes proper al centroide (el mes "representatiu" del grup).
- Usar el titol o primeres paraules d'aquest correu com a "etiqueta" del tema.
- O usar un LLM per generar un titol descriptiu del grup.

**Cost total**: menys d'un minut per a 1.000 correus. Aplicat a 10.000 correus, son uns 5-10 minuts. Aplicat a 100.000, son 1-2 hores. Encara factible.

**Cas practic al BernatLab**:
- 1.000 correus d'alertes de l'hort: puc veure si hi ha patrons (temperatura, plagues, errors del sistema).
- 1.000 correus de notificacions: agrupar per tipus (backup OK, alerta de seguretat, etc.).
- 1.000 correus personals: detectar els temes recurrents (subscripcions, familia, feina).

**Limitacio important**: la semblança cosinus nomes captura semblança semantica. Dos correus poden ser semanticament similars pero tenir intents diferents. Per exemple, dos correus sobre "temperatura" poden ser un d'informatiu i un d'alerta critica. El clustering no distingueix aixo nomes amb embeddings. Caldria un altre senyal (urgencia, remitent, etc.).

---

## Pregunta 14 (oberta): Limitacions amb texts curts i llargs

**Resposta model**:

**Texts molt curts (1-2 paraules)**:
- Poca informacio per capturar. Un model entrenat amb frases de 10+ paraules pot no funcionar be amb paraules soles.
- Exemple: "tomàquet" - el model pot retornar un embedding generic, sense context.
- Aplica al BernatLab: noms de sensors ("DS18B20") poden no ser ben representats.
- **Solucio**: afegir contexte manualment. "DS18B20 (sensor de temperatura del sol)" donara un embedding millor que "DS18B20" sol.

**Texts molt llargs (>1000 paraules)**:
- La majoria de models tenen un limit de ~512 tokens d'entrada (uns 1000 caracters).
- Si passes mes, el text es trunca. La primera part queda, la resta es perd.
- Pitjor encara: la informacio important pot estar al final i es perd.
- **Solucio 1**: truncar a 512 tokens. Pero pot perdre info.
- **Solucio 2 (millor)**: chunking. Parteixo el text llarg en fragments de 200-500 paraules i indexo cada un per separat.

**Estrategia al BernatLab**:
- Per a "noms" (sensors, plantes, persones): afegir contexte. "Sensor DS18B20 que mesura la temperatura del sol a 5cm de profunditat".
- Per a "descripcions" (logs, articles): chunking. Parteixo en paragrafs o seccions.
- Per a "consultes" (preguntes de l'usuari): normalment curtes, no cal fer res.

**Monitoreig**: val la pena revisar periodicament els chunks que es generen. Si veig que molts son trencats o incomplets, cal ajustar l'estrategia de chunking.

---

## Pregunta 15 (oberta): Local vs núvol

**Resposta model**:

**Arguments a favor del núvol (OpenAI text-embedding-3)**:
- **Qualitat**: el model d'OpenAI es dels millors. Bona cobertura de llenguatges, bona captura de nuances.
- **No cal hardware**: no consumes RAM ni CPU local. 
- **Rapidesa**: el núvol te GPUs dedicades. Pot ser mes rapid que el local.
- **Models sempre actualitzats**: cada vegada que vols provar un model millor, nomes canvies de parametre.

**Arguments a favor del local (Ollama + nomic-embed-text)**:
- **Privadesa total**: els textos mai surten del meu servidor.
- **Cost zero per consulta**: un cop descarregat el model, cada embedding es "gratis".
- **Sense limits de quota**: puc fer tants embeddings com vulgui.
- **Funciona offline**: sense Internet, igual funciona.
- **Cas d'ús al BernatLab**: processem logs de l'hort, correus personals, documents interns. Tot queda local.

**Tria final**: **local amb Ollama + nomic-embed-text**. Argument principal: **la privadesa i el cost zero superen la lleugera perdua de qualitat**.

A mes, la diferencia de qualitat entre nomic-embed-text i text-embedding-3 es notable pero no abismal. Per al 90% dels casos, el local es mes que suficient. Per al 10% on cal maxima qualitat, puc fer una consulta puntual al núvol amb dades anonimitzades.

**Consideracio estrategica**: a mes, confio en que els models locals milloraran amb el temps. El que avui es una diferencia del 10% podria ser nomes un 3% d'aqui un any. Apostar pel local es una inversio a llarg termini.

**Cas concret al BernatLab**: si vull comparar 1.000 correus per temes, fer-ho local em costa 0€. Al núvol, amb $0.0001 per 1k tokens, son uns $0.10. No es molt, pero sumat a centenars de consultes diaries, podria ser uns quants euros al mes. Al llarg de l'any, son 50-100€ que estalvio.

---

## Que fer si has fallat moltes preguntes

- **10-12 encerts**: repassa la seccio del resum sobre semblança cosinus i les seves propietats.
- **7-9 encerts**: fes l'exercici practic Pas 2-3 per veure les semblances en accio.
- **0-6 encerts**: comença pel Pas 2 (calcular un embedding) i veuras com funciona de manera intuïtiva.

## Que fer si has encertat totes

- Passa al **Capitol 7** (vector databases).
- O investiga "ColBERT" i altres models d'embeddings amb mes granularitat.
- O explora "embedding quantization" per comprimir els vectors sense perdre qualitat.
