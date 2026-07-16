# Resum - Capitol 5: Que es RAG

## La idea clau

**RAG** vol dir **Retrieval Augmented Generation** (Generacio augmentada per recuperacio). Es la tecnica que permet a un LLM respondre sobre les teves dades, no nomes sobre el que va aprendre durant l'entrenament. En lloc d'entrenar un model nou (car i complicat), li dones el contexte relevant a cada pregunta. I el millor: funciona amb qualsevol LLM.

## El problema que resol

Imagina't que vols preguntar al teu LLM local: "Com es configura el sensor d'humitat del Hort Osona?". El model `llama3.2:3b` no te ni idea: aquesta informacio no es al seu entrenament. Et respondra amb bestieses o et dira que no ho sap.

Tres possibles solucions:

1. **Re-entrenar el model** amb les teves dades. Car (milers d'euros), lent (dies), i nomes per a tu.
2. **Fine-tuning**: re-entrenar nomes una mica. Mes assequible, pero encara complicat.
3. **RAG**: donar-li el contexte adequat a cada pregunta. Rapid, barat, i funciona.

RAG es, amb diferència, la mes practica. Es el que fan tots els chatbots moderns que no al·lucinen: ChatGPT amb "Browse with Bing", els assistents de documentacio, etc.

## Com funciona RAG (visio general)

El flux te tres fases:

```
1. INDEXACIO (es fa un sol cop)
   Documents -> Chunks -> Embeddings -> Vector DB

2. QUERY (cada vegada que l'usuari pregunta)
   Pregunta -> Embedding -> Cerca a Vector DB -> Top-K chunks

3. GENERACIO (L'hora de la veritat)
   Pregunta + Chunks rellevants -> LLM -> Resposta
```

Posem-ho amb un exemple de l'Hort Osona:

1. **Indexacio**: tenim 50 pagines de documentacio sobre el sistema. Les partim en chunks de 500 paraules. Calculem un embedding per cada chunk (un vector numeric que representa el significat). Els desem a ChromaDB.

2. **Query**: l'usuari pregunta "Quin sensor mesura la temperatura del sol?". Calculem l'embedding de la pregunta. Busquem a ChromaDB els 3 chunks mes semblants. Probablement trobarem un que parla del sensor DS18B20.

3. **Generacio**: enviem al LLM un prompt com:
```
Contexte: [els 3 chunks trobats]
Pregunta: Quin sensor mesura la temperatura del sol?
Respon nomes basant-te en el contexte proporcionat.
```

El LLM tindra la informacio que necessita per respondre correctament. I com que hem limitat el contexte al que es rellevant, no s'inventara res.

## Per que es tant poderós?

RAG te avantatges que cap altre tecnica pot igualar:

- **Sempre actualitzat**: si afegeixes un document nou, nomes l'has d'indexar. No cal re-entrenar res.
- **Font verificable**: pots mostrar a l'usuari "aquesta resposta ve del document X". Redueix les al·lucinacions.
- **Privadesa**: les dades mai surten del teu sistema. No entrenen cap model extern.
- **Multi-document**: pots tenir milers de documents i el model nomes veu els rellevants.
- **Barat**: nomes pagues (o gastes electricitat) per la consulta. No hi ha re-entrenament.
- **Funciona amb models petits**: un 3B amb bon RAG pot superar un 70B sense RAG.

## Les limitacions

Pero no es magia. RAG tambe te reptes:

- **Qualitat del retrieval**: si no trobem els chunks correctes, el LLM no pot respondre be.
- **Finestra de context**: nomes podem donar uns quants chunks (4-10), no tots els documents.
- **Chunking dolent**: si partim malament els documents, perdem contexte.
- **Manteniment**: cal re-indexar quan els documents canvien.
- **Cost de calcul**: generar embeddings costa temps i CPU.

## Components d'un sistema RAG

Un sistema RAG te quatre blocs principals:

1. **Loader**: carrega els documents (PDF, Markdown, HTML, text pla).
2. **Splitter**: parteix els documents en chunks (100-1000 tokens).
3. **Embedder**: converteix cada chunk en un vector numeric.
4. **Retriever**: busca els chunks mes semblants a la pregunta.
5. **Generator**: el LLM que genera la resposta final.
6. **Vector DB**: on es guarden els embeddings (ChromaDB, FAISS, LanceDB).

Als capitols 6, 7 i 8 veurem cadascun en detall.

## RAG vs Fine-tuning vs Prompt engineering

| Tecnica | Quan usar-la | Cost | Temps |
|---|---|---|---|
| **Prompt engineering** | Totes les tasques. Es la base. | 0 | 0 |
| **RAG** | El model necessita dades que no te. | Baix | Hores |
| **Fine-tuning** | Necessites un estil o comportament molt especific. | Alt | Dies |
| **Pre-entrenar** | Gairebe mai. nomes centres de recerca. | Molt alt | Mesos |

**Regla practica**: comença sempre per prompt engineering. Si no n'hi ha prou, afegeix RAG. Si encara no es suficient, considera fine-tuning. Pero el 90% dels casos es resolen amb RAG.

## Un exemple real al BernatLab

Vull fer un assistent que sàpiga tot sobre el meu hort. Com ho faria amb RAG?

1. **Reuneixo els documents**: 20 articles sobre cultius, 10 fitxers de logs, 5 manuals de sensors, 3 diagrames.
2. **Els indexo** amb un script Python que llegeix, parteix i calcula embeddings.
3. **Munto una API** que, donada una pregunta, busca els chunks i els envia a Ollama.
4. **L'usuari pregunta**: "Quan he de regar els tomàquets al març?"
5. **El sistema respon** citant fonts ("Segons el manual X, els tomàquets al març...").

Tot això es pot fer en un dia de feina. I el resultat es un assistent que sembla que "sap" tot sobre el teu hort, quan en realitat nomes te una base de dades i un LLM de 3B parametres.

## Errors comuns amb RAG

- **Chunks massa grans**: si son de 2000 tokens, el contexte no hi cap.
- **Chunks massa petits**: si son de 50 tokens, perden el significat.
- **Embedding equivocat**: no tots els embeddings serveixen per a tot.
- **No netejar el text**: caracters extranys, headers repetits, etc. perjudiquen la cerca.
- **No re-indexar**: els documents canvien pero la base queda obsoleta.
- **Massa chunks al prompt**: enviar 20 chunks al LLM l'enreda. 3-5 es lo ideal.

## Connexions amb altres capítols

- **Cap 1-4** - Base: LLMs, Ollama, models, prompts.
- **Cap 6** - Embeddings: el component magic que permet cercar per significat.
- **Cap 7** - Vector databases: on guardem els embeddings.
- **Cap 8** - Pipeline RAG complet: com muntar tot plegat.
- **Cap 9** - Privadesa: RAG local = privacitat total.
- **Cap 10** - Aplicacio: muntarem un RAG per a l'Hort Osona.
