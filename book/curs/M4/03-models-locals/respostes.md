# Respostes - Capitol 3: Triar el model adequat

> Mira les respostes DESPRES d'haver fet el qüestionari.

## Pregunta 1: Que vol dir 7B parametres?

**Resposta correcta**: Set mil milions de pesos numerics que el model ha après.

**Explicacio**: Els parametres son els numeros que defineixen el comportament del model. Son el que sha ajustat durant l'entrenament per minimitzar l'error en la prediccio de la paraula seguent. Com mes parametres, mes capacitat (fins a un punt).

---

## Pregunta 2: Quantitzacio mes comuna

**Resposta correcta**: Q4 (4 bits).

**Explicacio**: Es el millor equilibri entre mida i qualitat. Els models d'Ollama ja venen quantitzats en Q4_0 per defecte. La perdua de qualitat respecte a Q8 o float32 es minima per a la majoria d'usos.

---

## Pregunta 3: Regla de RAM

**Resposta correcta**: Uns 0.5-0.7 GB per mil milions de parametres en Q4.

**Explicacio**: 7B en Q4 = 7 * 0.5 = 3.5 GB. 13B en Q4 = 13 * 0.5 = 6.5 GB. 70B en Q4 = 35 GB. Es una regla aproximada: el sistema operatiu tambe en necessita, i hi ha overhead.

---

## Pregunta 4: Model NO especialitzat en codi

**Resposta correcta**: Llama 3.2.

**Explicacio**: CodeLlama i CodeGemma son variants optimitzades per a codi. DeepSeek Coder tambe. Llama 3.2 es un model general que pot fer codi, pero no esta especialitzat.

---

## Pregunta 5: Sweet spot per a RPi 4 amb 4 GB

**Resposta correcta**: llama3.2:3b.

**Explicacio**: Ocupa uns 2.5 GB, deixa marge per al sistema, i dona bona qualitat. 7B no cap. 1B es massa basic per a la majoria de tasques.

---

## Pregunta 6: Que son tokens per segon?

**Resposta correcta**: La velocitat a la que el model genera text.

**Explicacio**: Es la metrica estandard per mesurar el rendiment d'un LLM. 10-20 t/s es un bon ritme per a xatejar. Per sota de 5 t/s es fa pesat. A la RPi esperem 5-15 t/s amb models petits.

---

## Pregunta 7: Model nomes per embeddings

**Resposta correcta**: nomic-embed-text.

**Explicacio**: Els models d'embeddings nomes converteixen text a vectors. No generen text. S'utilitzen per a RAG. Llama, Phi i Gemma son models generatius.

---

## Pregunta 8 (oberta): Que es la quantitzacio?

**Resposta model**:

La quantitzacio es el proces de reduir la precisio numerica d'un model per estalviar espai i memoria. En el context dels LLMs, això vol dir passar de numeros en coma flotant de 32 bits (float32) a representacions mes simples en 4, 8 o 2 bits.

Pensa-ho aixi: si tens un numero com 0.123456789, en float32 ocupes 32 bits i tens molta precisio. Si el redondeges a 0.12, nomes necessites 4 bits. El resultat es una mica menys precís, pero en el context d'un model amb milers de milions de parametres, aquesta perdua es negligible: els patrons generals es mantenen, nomes perden els detalls mes subtils.

**Per que es important?** Per dos motius:
- **Espai en disc**: un model de 7B en float32 ocupa 28 GB. En Q4, nomes 4 GB. A la RPi amb 32 GB de disc, aixo es la diferencia entre tenir un model o no.
- **RAM en execucio**: carregar un float32 de 7B necesitaria 28 GB de RAM. En Q4, nomes 4 GB. Permet que el model corri en maquines modestes.

El truc es trobar el punt on la perdua de qualitat es acceptable. Q4 es considera el sweet spot: el model perd un 5-10% de qualitat pero ocupa 8x menys. Q2 perd un 30% de qualitat pero ocupa 16x menys (massa). Q8 perd nomes 1-2% pero nomes estalvia 4x (insuficient per justificar).

---

## Pregunta 9 (oberta): Per que tants models?

**Resposta model**:

Hi ha tants models per varies raons:

**Raons tecniques**: cada empresa (Meta, Google, Microsoft, Mistral AI, Alibaba...) te la seva recerca, les seves dades d'entrenament i la seva arquitectura. Uns prioritzen la velocitat, uns la qualitat, uns el multilingüisme, uns el raonament. Es impossible que un sol model sigui el millor en tot.

**Raons economiques**: cada empresa vol el seu propi model per no dependre d'altres (pensa en la competencia entre OpenAI, Anthropic, Google). Tambe hi ha estrategies de "open source" per guanyar comunitat (Meta amb Llama) o models tancats com a producte comercial (OpenAI).

**Raons d'optimitzacio**: un model pot estar optimitzat per una tasca especifica (codi, matematiques, conversacio). Un model general ha de ser competent en tot pero no excel·lent en res. Els especialitzats (CodeLlama, Phi-3) son excel·lents en el seu ambit.

**Que passaria si nomes hi hagues un model?** Monopoli tecnologic. Preus alts. Poca innovacio. Risc de bloqueig (si l'empresa canvia les condicions, tothom queda penjat). Per tant, la diversidad es bona per a l'ecosistema.

Al BernatLab, la diversidad tambe ens beneficia: podem triar el millor model per a cada tasca, i si un falla o deixa de mantenir-se, tenim alternatives.

---

## Pregunta 10 (oberta): Cas d'us per a cada model

**Resposta model**:

**`llama3.2:1b` per a resums d'una sola linia**: quan rebo una alerta del BernatLab i vull un resum rapid del log associat. Exemple: "Resumeix aquesta linia: 'ERROR [mqtt] connection refused'". El 1B es rapid (30 t/s), no necessita molta memoria, i per a resums simples es perfecte. Qualitat: 3/5, pero per a aixo n'hi ha prou.

**`llama3.2:3b` per a generar scripts curts**: quan necessito un script de 10-20 linies per a una tasca concreta. Exemple: "Genera un script bash que miri l'us de disc i m'avisi si passa del 80%". El 3B enten prou be la sintaxi i les comandes de Linux. Qualitat: 4/5.

**`phi3:mini` per a analisi de logs complexes**: quan tinc un problema rare i necessito entendre la sequencia d'esdeveniments. Exemple: "Analitza aquestes 20 linies de log i explica que ha passat abans del crash". Phi-3 esta optimitzat per raonament logic i segueix cadenes d'esdeveniments millor que els altres. Qualitat: 4.5/5.

La perdua de qualitat que assumeixo: amb el 1B, accepto que algunes respostes seran massa basiques o generiques. Amb el 3B, ocasionalment hi haurà errors subtils en comandes llargues. Amb el phi3, el temps d'espera es mes alt (10 t/s vs 30 del 1B) i l'us de RAM es mes gran.

Si nomes pogues tenir UN model, triaria el 3B. Pero tenir tres models especialitzats et dona la flexibilitat d'optimitzar per a cada tasca.

---

## Pregunta 11 (oberta): Mida i qualitat

**Resposta model**:

La relacio entre mida i qualitat NO es linial. Fins a cert punt, mes parametres = millor. Pero mes enlla d'un llindar, els guanys son decreixents.

**Fins a 7B**: cada augment de mida te un impacte clar. La diferència entre 1B i 3B es molt notable. Entre 3B i 7B tambe.

**Entre 7B i 13B**: la diferencia encara es notable, pero menor. A partir d'aqui, un 13B es sol ser "suficient" per a la majoria de tasques.

**Entre 13B i 70B**: la diferencia es subtil. Un 70B pot raonar millor en problemes molt complexos, pero per a resums, traduccio o scripts, la diferencia es minima. A mes, un 70B necessita 40 GB de RAM, cosa que nomes esta disponible en servidors amb GPU.

**Excepcions importants**:
- Un model ben entrenat de 7B pot superar un de mal entrenat de 70B. La qualitat de l'entrenament (dades, tecnica) compte mes que la mida pura.
- Per a tasques especialitzades (codi, matematiques), un model de 3B optimitzat pot superar un general de 13B.

**Al BernatLab**: el sweet spot es 3B-7B. Per sobre de 13B, els costos (RAM, temps) no es justifiquen per a les tasques que fem. La regla: tria el model mes petit que doni la qualitat minima acceptable per a la teva tasca.

---

## Pregunta 12 (oberta): RPi amb 8 GB i model 13B

**Resposta model**:

Amb 8 GB de RAM, intentar un model de 13B es complicat. Fem el calcul:

- Model 13B en Q4: 13 * 0.5 = 6.5 GB de RAM.
- Sistema operatiu Debian: 0.5-1 GB.
- Altres serveis (InfluxDB, Grafana, Mosquitto, etc.): 1-2 GB.
- Total estimat: 8-9.5 GB.

Per tant, estas just al limit o lleugerament per sobre. El que pot passar:

1. **Funciona amb swap lent**: Linux mourà parts del model a la swap (microSD). Es funcional pero pot trigar 5-10x mes.
2. **OOM kill**: el kernel pot matar processos per alliberar memoria. Si mata Ollama, el model es descarrega. Si mata un altre servei, tens una incidencia greu.
3. **Sistema inestable**: amb la RAM al limit, tot va lent. La RPi pot trigar 30 segons a respondre a interaccions basiques.

**Solucions**:
- **Triar un model de 7B**: 4 GB de RAM, perfecte per a 8 GB totals. La perdua de qualitat es acceptable.
- **Augmentar swap a 16 GB**: permet que el model carregui, pero es lent.
- **Quantitzar a Q2 o Q3**: el 13B en Q2 ocupa ~3 GB pero perd molta qualitat.
- **Servidor extern**: si necessites el 13B, considera un servidor cloud amb GPU.

**Recomanacio**: quedar-se amb 7B. La diferencia de qualitat amb 13B no compensa el risc d'inestabilitat. A la RPi 4, menys es mes.

---

## Pregunta 13 (oberta): Models especialitzats

**Resposta model**:

Els models especialitzats existeixen per una rao simple: un model entrenat amb dades especifiques supera un model general en la seva area. CodeLlama, per exemple, sha entrenat amb milions de repositoris de GitHub, documentacio tecnica, i StackOverflow. Per tant, enten patrons de codi molt millor que un model general.

**Quan val la pena usar-los al BernatLab**:

**Si per aixo**: el model general es bo. Llama 3.2, Mistral o Gemma 2 poden revisar logs, generar scripts simples, o respondre preguntes generals. La diferencia amb un especialitzat es marginal.

**Si per aixo altre**: el model especialitzat es netament millor.
- Generar un script Python de 50+ linies: CodeLlama o DeepSeek Coder.
- Analisi matematica o logica complexa: Phi-3.
- Processar imatges: Llama 3.2 Vision.
- Embeddings (RAG): nomic-embed o mxbai-embed.

**Regla practica**: al BernatLab tinc un model general (`llama3.2:3b`) que es el que faig servir el 80% del temps. nomes baixo a models especialitzats quan la tasca es clarament millor amb ells. Mantenir models especialitzats ocupa espai i memoria que potser no val la pena.

**Concret**: si vull generar un script Python complex, baixo `codellama:7b` temporalment. Si vull fer embeddings, baixo `nomic-embed-text`. Per a la resta, el model general.

---

## Pregunta 14 (oberta): Metode d'avaluacio

**Resposta model**:

Un metode practic per evaluar un model es el que es coneix com a "evaluacio per tasca" o "task-based evaluation". Consta de quatre passos:

**Pas 1: Definir 5-10 preguntes representatives**. Penso en les tasques reals que vull que el model faci. Per al BernatLab, podrien ser:
- "Explica aquesta linia de log: '...'".
- "Genera un script bash que ... ".
- "Resumeix aquest correu d'alerta: '...'".
- "Que pot estar causant aquest error: '...'".

**Pas 2: Passar les preguntes al model i puntuar**. Per a cada pregunta, dono una puntuacio de l'1 al 5 segons criteris clars:
- 5: resposta correcta, completa, ben estructurada.
- 4: correcta pero li manca algun detall.
- 3: parcialment correcta.
- 2: incorrecta pero amb estructura valida.
- 1: brossa completa.

**Pas 3: Comparar amb un model de referencia o amb el "ideal"**. Si ja tens un model que usaves, compara. Si no, pots comparar la resposta del model amb la que tu hauries donat.

**Pas 4: Decidir**. Si la mitjana es >4, el model es acceptable. Si es 3-4, pot millorar amb un prompt millor. Si es <3, cal un altre model o una altre estrategia.

**Exemple concret al BernatLab**: evaluo `llama3.2:3b` amb 10 logs reals. Puntue cada explicacio. Si la mitjana es 3.5, vol dir que el model es just per aixo. Si es 4.2, es bo. Si es 2.5, nomes em serveix per a les preguntes mes simples.

Aquest metode es mes realista que mirar rankings de benchmarks generals. El que importa es com es comporta en les TEVES tasques, no en tasques generics.

---

## Pregunta 15 (oberta): El futur dels models petits

**Resposta model**:

Si d'aqui un any els models son 10x mes petits pero igual de bons (o millors), el panorama canviara drastament al BernatLab:

**Capacitat desblocat**: podria correr un model de 30B a la RPi 4 amb 4 GB. O fer servir un 70B en una estacio de treball. La qualitat que ara nomes esta disponible al núvol estara disponible localment.

**Cas d'us nous**:
- **Analisi continu de logs en temps real**: en lloc de resumir logs un cop al dia, podria tenir un agent que vigili constantment.
- **Assistent de veu**: podria transcriure audio, entendre'l, i respondre, tot en local i en temps real.
- **Visio per computador**: analitzar les imatges dels sensors de l'hort per detectar plagues o malalties automaticament.
- **Generacio de codi a temps real**: mentre escric un script, el LLM em suggereix fragments.

**Canvi d'estrategia**: ara prioritzem models petits (1-3B) per limitacio de hardware. Si els models son 10x mes eficients, prioritzem models mes grans (7-13B) per a millor qualitat, mantenint el consum de RAM igual.

**Impacte economic**: si els models locals son prou bons, deixem de pagar subscriptcions a ChatGPT, Claude, etc. La IA de qualitat es "gratis" en termes economics (nomes electricitat).

**Risc**: la dependencia total d'un sol proveidor (Ollama, Meta, etc.) augmenta. Cal mantenir-se informat de nous models i tenir plans B.

Al BernatLab, la promesa es clara: tenir un assistent potent a casa, sense dependre del núvol, i poder automatitzar molt mes del que avui es possible.

---

## Que fer si has fallat moltes preguntes

- **10-12 encerts**: repassa la taula de models del resum i les mides de RAM.
- **7-9 encerts**: fes l'exercici practic i observa directament les diferencies entre models.
- **0-6 encerts**: comença descarregant dos models (1B i 3B) i comparant les respostes a la mateixa pregunta.

## Que fer si has encertat totes

- Passa al **Capitol 4** (prompt engineering).
- O prova un model especialitzat: `ollama pull codellama:7b` i compara amb un general.
- O investiga nous models recents: `qwen2.5`, `gemma2:9b` (si tens RAM).
