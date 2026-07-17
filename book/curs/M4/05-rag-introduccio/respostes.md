# Respostes - Capitol 5: Que es RAG

> Mira les respostes DESPRES d'haver fet el qüestionari.

## Pregunta 1: Que significa RAG?

**Resposta correcta**: Retrieval Augmented Generation.

**Explicacio**: Son les inicials en angles. "Retrieval" = recuperar (cercar), "Augmented" = augmentat (millorat), "Generation" = generacio. Es a dir, generacio de text augmentada amb recuperacio d'informacio. Fa referencia a un sistema que primer cerca informacio rellevant i despres genera una resposta basada en aquesta informacio.

---

## Pregunta 2: Problema que RAG resol

**Resposta correcta**: Permetre al LLM respondre sobre dades que no va veure a l'entrenament.

**Explicacio**: Un LLM nomes sap el que ha vist durant l'entrenament. Si volem que respongui sobre dades noves (els nostres documents, la nostra base de coneixement), cal un mecanisme per injectar aquesta informacio al prompt. RAG es aquest mecanisme.

---

## Pregunta 3: Fases del flux RAG

**Resposta correcta**: 3 fases (indexacio, query, generacio).

**Explicacio**: Indexacio = partir documents en chunks i calcular embeddings. Query = cercar els chunks mes rellevants per una pregunta. Generacio = passar els chunks al LLM perque generi la resposta final. Tots els sistemes RAG segueixen aquest esquema basic.

---

## Pregunta 4: Que es un chunk?

**Resposta correcta**: Un fragment de text en que partim un document.

**Explicacio**: Els documents llargs no es poden passar sencers al LLM (limits de context, cost). Els partim en fragments mes petits (chunks), normalment de 200-1000 caracters, que son prou petits per entrar al context i prou grans per contenir informacio coherent.

---

## Pregunta 5: Quants chunks enviar al LLM?

**Resposta correcta**: Entre 3 i 5.

**Explicacio**: Si nomes 1, pot ser insuficient. Si 10, el LLM es perd o confon. Sweet spot: 3-5 chunks que el sistema de cerca considera mes rellevants. Aixo dona context suficient sense saturar.

---

## Pregunta 6: Component que NO es de RAG

**Resposta correcta**: Compilador de Python.

**Explicacio**: Un sistema RAG te: Loader (carrega documents), Splitter (parteix en chunks), Embedder (calcula embeddings), Vector Store (guarda els vectors), Retriever (cerca per semblança), LLM (genera la resposta). Un compilador de Python no hi te res a veure.

---

## Pregunta 7: Per a que serveix l'embedding?

**Resposta correcta**: Convertir text en un vector numeric que representa el significat.

**Explicacio**: Un embedding es una llista de numeros (vector) que captura el significat del text. Dues frases amb significat semblant tindran vectors propers, i es pot fer la inversa: trobar els textos mes semblants a una pregunta comparant els seus vectors.

---

## Pregunta 8: Regla practica

**Resposta correcta**: Comença per prompt engineering, afegeix RAG, i finalment fine-tuning.

**Explicacio**: Es la jerarquia de cost i complexitat. Prompt engineering es gratis. RAG es cost mitja (has d'indexar documents). Fine-tuning es el mes car (cal GPU i hores d'entrenament). Sempre comença pel mes simple.

---

## Pregunta 9 (oberta): RAG i models petits

**Resposta model**:

RAG funciona be amb models petits perque **separa el "saber" del "raonar"**. Un model de 3B no pot memoritzar tota la informacio sobre l'Hort Osona, pero pot raonar perfectament sobre els 3-5 fragments que li passem.

Es la diferencia entre un examen sense materials (on has de recordar-ho tot) i un examen amb apunts permesos (on nomes cal que entenguis i sintetitzis). El model de 3B es excel·lent en la segona tasca.

**Com afecta la finestra de context**: si la finestra es petita (4k tokens), nomes podem passar 2-3 chunks petits. Si es mes gran (8k-32k), podem passar mes context. Per tant:
- RPi 4 amb model 3B (4-8k context): 2-3 chunks curts, funciona per a consultes simples.
- Mac M2 amb model 7B (8-16k context): 5-7 chunks mes llargs, funciona per a consultes complexes.
- Servidor potent amb model 13B+ (32k+ context): 10+ chunks, excel·lent per a questions complexes.

**Al BernatLab**: RAG amb un model 3B dona resultats sorprenentment bons per a consultes simples. Es la combinacio ideal entre privadesa, cost i qualitat.

---

## Pregunta 10 (oberta): RAG, fine-tuning o prompt engineering?

**Resposta model**:

Per a un assistent que ha de "saber" tot sobre els meus projectes al GitHub, **triaria RAG**. Argumento a continuacio.

**Per que no fine-tuning**: fine-tuning requereix un dataset massiu (milers de examples de pregunta-resposta), una GPU potent (hores de calcul), i el resultat es un model que sha "fos" amb el coneixement. Si un repo canvia, cal re-entrenar. El cost economic es alt i el manteniment es complexe.

**Per que no nomes prompt engineering**: ficar tota la informacio al prompt nomes es viable si tens pocs projectes. Si tens 10 repos amb 50 fitxers cadascun, son 500 fitxers. Impossible ficar-ho en un prompt.

**Per que RAG**:
- **Indexacio automatica**: un script llegeix cada repo, el parteix en chunks, calcula embeddings, i els guarda. Es pot fer diariament o quan hi hagi canvis (webhook).
- **Cerca rapida**: quan pregunto, nomes es carreguen els 3-5 chunks mes rellevants.
- **Sempre actualitzat**: nomes cal re-indexar per incorporar canvis.
- **Font verificable**: puc citar el fitxer i la linia exacta.
- **Funciona amb qualsevol model**: 3B local, 7B, 70B al núvol, el que sigui.

**Passos que faria**:
1. Clonar tots els repos a `/home/bernat/projects/`.
2. Escriure un script Python que recorri cada `.md`, `.txt`, `.py` i els indexi.
3. Usar ChromaDB o similar per emmagatzemar els embeddings.
4. Muntar un script que faci la consulta i passi els resultats al LLM.
5. Actualitzacio automatica: cada nit, revisar si hi ha commits nous i re-indexar nomes aquells fitxers.

---

## Pregunta 11 (oberta): Tres opcions per a 50 fitxes

**Resposta model**:

Analitzem les tres opcions per a 50 fitxes de cultiu:

**Opcio A - Ficar-les al prompt**: nomes viable si el model te una finestra de context gegant (32k+ tokens) i nomes 5-10 fitxes. Amb 50 fitxes de 500 paraules = 25.000 paraules = 35.000 tokens. Imposable en models petits, prohibitiu en costos. A mes, cada pregunta ha de carregar les 50 fitxes, la qual cosa multiplica el cost.

**Opcio B - RAG**: 
- Cost d'indexacio: 1 cop (unes hores).
- Cost per consulta: nomes els 3-5 chunks rellevants (1-2k tokens).
- Escalable: podem afegir mes fitxes sense augmentar el cost per consulta.
- **Veredicte: la millor opcio per al BernatLab**.

**Opcio C - Fine-tuning**:
- Cal un dataset d'entrenament: almenys 1000 parelles pregunta-resposta.
- Cal una GPU potent (no es pot fer a la RPi 4).
- Hores o dies d'entrenament.
- Resultat: el model "memoritza" les fitxes, pero perd flexibilitat.
- **Veredicte: overkill per a 50 fitxes. Es justifica a partir de milers de documents o d'un cas d'us molt especific**.

**Conclusio**: al BernatLab, RAG es la opcio correcta. Si un dia tens 5000 fitxes, podries considerar fine-tuning. Per a 50, RAG es mes que suficient.

---

## Pregunta 12 (oberta): Qualitat del retrieval

**Resposta model**:

La qualitat del retrieval (cerca) es critica perque **la resposta nomes pot ser tan bona com els chunks que passes al LLM**. Si el sistema retorna un chunk irrellevant, el LLM generarà una resposta incorrecta o inventada.

**Per que mes chunks no es sempre millor**:
- Si passes 10 chunks, el LLM ha de discriminar qual es relevant. Es feina addicional que pot confondre.
- Mes tokens = mes cost i mes lent.
- "Lost in the middle": els models tendeixen a parar mes atencio al principi i al final del contexte, ignorant el que esta al mig.
- Si el sistema de cerca retorna molts chunks "poc rellevants", el LLM es pot deixar portar per ells.

**Que passa si el chunk recuperat NO es realment rellevant**:
- **Cas 1 (chunk tangencial)**: el LLM pot intentar connectar-lo amb la pregunta i donar una resposta forçada pero incorrecta.
- **Cas 2 (chunk sense relacio)**: el LLM pot inventar una resposta que "soni" be pero no te res a veure amb el chunk.
- **Cas 3 (chunk rellevant pero ambigu)**: la resposta es valida pero parcial, no completa.

**Solucions**:
- **Re-ranking**: un model mes petit reordena els top-20 chunks i tria els 3-5 millors.
- **Filtratge per llindar**: nomes passar chunks amb semblança > 0.6.
- **Expansio de la consulta**: cercar la pregunta + variants per augmentar el recall.
- **Multi-query**: fer 3 cerques amb versions diferents de la pregunta i combinar resultats.

Al BernatLab, monitoro sovint quins chunks retorna el sistema per preguntes representatives. Si veig chunks irrellevants, ajusto l'splitting o el model d'embeddings.

---

## Pregunta 13 (oberta): RAG i privadesa

**Resposta model**:

RAG es considerat una solucio "transparente" perque **la informacio utilitzada per generar la resposta es pot citar i verificar**. Aixo te consequencies profundes:

**Contrast amb fine-tuning**: en fine-tuning, el coneixement queda fos dins dels milers de milions de pesos del model. Es impossible saber exactament que ha "memoritzat" el model ni d'on ha sortit una resposta concreta. Es una caixa negra.

En RAG, puc dir a l'usuari: "aquesta resposta es basa en el document X, pagines 12-15". L'usuari pot verificar la font. Si la font es incorrecta, podem corregir el document. Si la font es bona pero la resposta es dolenta, sabem que el problema es del LLM, no de les dades.

**Consequencies per a la privadesa**:
- **Auditoria facil**: en complir GDPR, puc demostrar quines dades personals s'han usat per generar cada resposta.
- **Retirada de dades**: si un usuari demana que les seves dades siguin esborrades, nomes cal esborrar els documents que les contenen. El model no te res a esborrar perque no les ha memoritzat.
- **Control d'acces**: puc restringir quins documents son visibles per a cada usuari o consulta.
- **Consistencia**: tothom que faci la mateixa pregunta reb la mateixa resposta (si els chunks son els mateixos), cosa que es important per a tracte igualitari.

Això fa RAG especialment atractiu per a aplicacions amb dades personals o sensibles, com ara l'hort familiar (amb ubicacio, sistema de seguretat, etc.) o una base de coneixement corporativa.

---

## Pregunta 14 (oberta): Metriques per avaluar el RAG

**Resposta model**:

Tres metriques practicables al BernatLab:

**Metrica 1 - Taxa d'encert en el top-k (Recall@k)**: preparo un dataset de 50 preguntes amb la resposta esperada (puc generar-lo jo o usar un LLM per crear-lo). Per cada pregunta, miro si el chunk correcte esta en els top-5 retornats. Calculcuo el percentatge. Si es >80%, el sistema RAG funciona be. Si es <50%, cal millorar l'embedding o el chunking.

Exemple:
- Pregunta: "Quan es planten els tomàquets?"
- Chunk esperat: seccio "Tomàquets" del manual.
- Si el chunk esta en els top-5: 1. Si no: 0.

**Metrica 2 - Temps de resposta de cap a cap**: medeixo el temps des de que envio la pregunta fins que rebo la resposta. Objectiu: <5 segons per a una bona experiencia d'us. Si passa de 10, l'usuari es frustrara.

Descomposo el temps:
- Calcular embedding de la pregunta: ~100ms.
- Cercar a la vector DB: ~50ms.
- Generar resposta al LLM: 1-5 segons (depen del model).
- Total: 1.5-5.5 segons.

Si el LLM es lent, potser cal un model mes petit o un chunking mes efficient.

**Metrica 3 - Qualitat de la resposta final (humana o LLM-as-judge)**: per a 20-30 respostes, un huma (jo) puntua cada resposta de l'1 al 5. Criteris:
- 5: correcta, completa, cita el contexte.
- 4: correcta pero li manca detall.
- 3: parcialment correcta.
- 2: resposta pero no util.
- 1: no ha respost o ha inventat.

Alternativa: usar un LLM mes potent com a "judge" (LLaMA 3.1 70B o GPT-4) per puntuar les respostes. Es mes rapid pero menys fiable que un huma.

**Conclusio**: amb 50 preguntes de test, 3 metriques clares i una hora de feina, puc avaluar si el meu RAG funciona. Si totes tres metriques son bones, puc posar el sistema en produccio amb confiança.

---

## Pregunta 15 (oberta): RAG vs 70B

**Resposta model**:

**Arguments a favor del RAG**:
- **Privadesa**: les dades es queden al meu servidor. Un 70B al núvol obligaria a enviar-les a tercers.
- **Actualitzacio**: afegir un document nou triga 1 segon. Re-entrenar un 70B triga setmanes.
- **Verificable**: puc citar les fonts. Un 70B no pot.
- **Cost economic**: un 70B al núvol costa diners per token. RAG nomes paga electricitat.
- **Cas d'ús local**: per a horticultura a Osona, la informacio especifica no es a Internet. Cap 70B l'ha vista.

**Arguments a favor del 70B**:
- **Coneixement general**: un 70B sap molt sobre temes generals, no cal preparar res.
- **Raonament sofisticat**: pot raonar sobre problemes complexos millor que un 3B.
- **Multilingüe real**: pot parlar molts idiomes amb fluidesa.
- **Menys feina de preparacio**: no cal indexar res, nomes usar el model.
- **Cas d'ús general**: per a preguntes generals (no especifiques d'Osona), es molt competent.

**Tria final per al BernatLab**: **RAG sobre 3B local**. Per que? Perque el 80% de les meves preguntes son sobre l'Hort Osona, cosa especifica que un 70B no coneix. Per al 20% restant (preguntes generals), puc usar el model 3B o complementar amb alguna consulta al núvol anonimitzada.

Si nomes fes preguntes generals, el 70B tindria mes sentit. Pero al BernatLab, on la especialitzacio importa, RAG es imbatible en relacio qualitat-cost-privadesa.

A mes, RAG em dona un avantatge competitiu que un 70B mai tindra: el coneixement **actualitzat** del meu hort, els meus logs, les meves plantes. Cap quantitat de parametres pot substituir la informacio especifica i local.

---

## Que fer si has fallat moltes preguntes

- **10-12 encerts**: repassa el resum i fes l'exercici practic del Pas 3-6.
- **7-9 encerts**: llegeix l'apartat de limitacions del resum i torna a provar.
- **0-6 encerts**: comença per entendre quines son les tres fases (indexacio, query, generacio) amb un exemple simple.

## Que fer si has encertat totes

- Passa al **Capitol 6** (embeddings, en profunditat).
- O investiga "hybrid search": combinar cerca per paraules clau (BM25) amb cerca semantica.
- O mira eines com `langchain` o `llamaindex` que simplifiquen la construccio de RAG.
