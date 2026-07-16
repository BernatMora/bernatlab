# Qüestionari - Capitol 5: Que es RAG

> 10 preguntes · ~15 min

## Pregunta 1

Que significa RAG?

- [ ] Real AI Generation
- [x] Retrieval Augmented Generation
- [ ] Rapid Algorithmic Generation
- [ ] Recursive AI Graph

## Pregunta 2

Quin es el problema principal que RAG vol resoldre?

- [ ] Fer que el LLM vagi mes rapid
- [x] Permetre al LLM respondre sobre dades que no va veure a l entrenament
- [ ] Reduir la mida del model
- [ ] Millorar la qualitat del text generat

## Pregunta 3

Quantes fases te el flux RAG?

- [ ] 2 fases
- [x] 3 fases (indexacio, query, generacio)
- [ ] 5 fases
- [ ] 7 fases

## Pregunta 4

Que es un "chunk" en el context de RAG?

- [ ] Un tipus de model d IA
- [x] Un fragment de text en que partim un document
- [ ] Un vector numeric
- [ ] Una base de dades

## Pregunta 5

Quants chunks es recomana enviar al LLM en una consulta RAG?

- [ ] Tots els que hi hagin
- [ ] Nomes 1
- [x] Entre 3 i 5
- [ ] Com a minim 20

## Pregunta 6

Quin d'aquests NO es un component d'un sistema RAG?

- [ ] Loader
- [ ] Splitter
- [x] Compilador de Python
- [ ] Embedder

## Pregunta 7

Per a que serveix l'embedding en un sistema RAG?

- [x] Convertir text en un vector numeric que representa el significat
- [ ] Decorar el text amb emojis
- [ ] Comprimir el text
- [ ] Generar la resposta final

## Pregunta 8

Quina es la regla practica que segueix aquest capitol per triar la tecnica?

- [ ] Comenca sempre per fine-tuning
- [ ] Comenca sempre per re-entrenar
- [x] Comenca per prompt engineering, afegeix RAG, i finalment fine-tuning
- [ ] Usa nomes RAG, mai prompt engineering

## Pregunta 9 (oberta)

Explica amb les teves paraules: per que RAG funciona be amb models petits? Pensa en la diferencia entre "saber moltes coses" i "tenir la informacio a la ma".

Pistes per respondre:
- Un model de 3B no pot "saber" tot sobre l Hort Osona.
- Pero si li dones els 3 parrafs rellevants, pot raonar-hi perfectament.
- Es la diferencia entre un examen sense materials i un examen amb apunts permesos.
- Com afecta la finestra de context?

## Pregunta 10 (oberta)

Vols muntar un assistent que sápiga tot sobre els teus projectes al GitHub. Tries RAG, fine-tuning o prompt engineering? Per que? Quins passos faries?

Pistes per respondre:
- Quantes dades tens? (10 repos? 100? 1000?)
- Canvien sovint? (cada setmana? cada mes?)
- Quin cost economic/temporal pots assumir?
- Amb RAG: indexaries cada repo, cada commit, cada documentacio?
- Quins avantatges te RAG vs fine-tuning en aquest cas?
