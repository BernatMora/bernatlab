# Quiz - Capitol 8: RAG - implementacio completa

## Pregunta 1
Quants passos te el pipeline RAG basic?

- [ ] 2
- [ ] 3
- [x] 5
- [ ] 10

## Pregunta 2
Quin es el primer pas d'un pipeline RAG?

- [ ] Enviar la pregunta al LLM
- [ ] Calcular l'embedding de la pregunta
- [x] Calcular l'embedding de la pregunta
- [ ] Guardar a ChromaDB

## Pregunta 3
Quin model d'embeddings recomana el capitol per usar amb Ollama?

- [ ] llama3.2
- [x] nomic-embed-text
- [ ] mistral
- [ ] gpt-4

## Pregunta 4
Quin es el sweet spot de chunk size segons el capitol?

- [x] 300-800 paraules
- [ ] 50-100 paraules
- [ ] 2000-5000 paraules
- [ ] 1-10 paraules

## Pregunta 5
Quants fragments (k) es recomanen retornar a la cerca?

- [ ] 1
- [x] 3-5
- [ ] 20-50
- [ ] 100+

## Pregunta 6
Que pasa si no passes `path=` a `PersistentClient`?

- [ ] ChromaDB llenca un error
- [x] Les dades es perden al tancar
- [ ] Es guarden a la RAM nomes
- [ ] Es guarden al núvol

## Pregunta 7 (oberta)
Descriu els 5 passos del pipeline RAG amb les teves paraules. Per que cal cadascu?

Pistes:
- Quin problema resol l'embedding de la pregunta?
- Per que cal ChromaDB i no un grep?
- Per que cal posar el contexte al prompt?
- Que pasa si el LLM no te contexte?
- Que pasa si no retornem respostes clares?

## Pregunta 8 (oberta)
Explica que pasa si barreges dos models d'embeddings diferents (un per indexar, un altre per cercar). Com ho detectaries?

Pistes:
- Dimensions dels vectors
- Resultats de la cerca
- Comprovacions que faries
- Com ho solucionaries

## Pregunta 9 (oberta)
Per a un homelab amb Hort Osona, k=3 o k=5? Raona la resposta.

Pistes:
- Mida dels fragments
- Temps de resposta
- Qualitat vs velocitat
- Tokens disponibles al LLM

## Pregunta 10 (oberta)
Quines optimitzacions aplicaries al pipeline si la RPi va lenta?

Pistes:
- Chunk size
- k mes petit
- Model mes petit
- Cache d'embeddings
- Streaming
