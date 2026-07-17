# Qüestionari - Capitol 3: Triar el model adequat

> 15 preguntes · ~20 min · 7 test + 8 obertes

## Pregunta 1
Que vol dir "7B parametres" en un LLM?

- [ ] Set mil milions de documents amb que sha entrenat
- [x] Set mil milions de pesos numerics que el model ha après
- [ ] Set mil bits d'informacio
- [ ] Set mil preguntes que pot respondre

## Pregunta 2
Quina quantitzacio es la mes comuna als models d'Ollama per defecte?

- [ ] Q8 (8 bits)
- [x] Q4 (4 bits)
- [ ] Q2 (2 bits)
- [ ] Float32

## Pregunta 3
Quina es la regla aproximada de RAM que necessita un model?

- [ ] 1 GB per parametre
- [x] Uns 0.5-0.7 GB per mil milions de parametres en Q4
- [ ] 10 GB per parametre
- [ ] No importa la RAM

## Pregunta 4
Quin d'aquests models NO es especialitzat en codi?

- [ ] CodeLlama
- [ ] CodeGemma
- [x] Llama 3.2
- [ ] DeepSeek Coder

## Pregunta 5
Quin model es el sweet spot recomanat per a una RPi 4 amb 4 GB?

- [ ] mistral:7b
- [x] llama3.2:3b
- [ ] llama3.1:70b
- [ ] phi3:medium

## Pregunta 6
Que significa "tokens per segon" (t/s)?

- [ ] El temps que triga el model a carregar-se
- [x] La velocitat a la que el model genera text
- [ ] La mida del model
- [ ] La quantitat de memoria que usa

## Pregunta 7
Quin model d'Ollama NO serveix per generar text, nomes per embeddings?

- [ ] llama3.2
- [x] nomic-embed-text
- [ ] phi3:mini
- [ ] gemma2:2b

## Pregunta 8 (oberta)
Explica amb les teves paraules: que es la quantitzacio i per que es important? Pensa en la diferencia entre "emmagatzemar un nombre amb maxima precisio" i "emmagatzemar-lo de forma mes compacta".

Pistes per respondre:
- Un float32 ocupa 32 bits (4 bytes) per numero.
- Un Q4 nomes 4 bits: 8x menys espai.
- Que es perd en la conversio? Precisio numerica.
- Per que serveix igual per a LLMs?

## Pregunta 9 (oberta)
Per que hi ha tants models diferents (Llama, Mistral, Phi, Gemma, Qwen)? No n'hi ha prou amb un de "perfecte"? Argumenta la resposta.

Pistes per respondre:
- Cada empresa te la seva recerca i la seva filosofia.
- Els models tenen punts forts diferents: velocitat, raonament, multilingüe, codi.
- La competicio es beneficiosa: cada versio es millor que l'anterior.
- Que passaria si nomes hi hagues un model?

## Pregunta 10 (oberta)
Al BernatLab tens una RPi 4 amb 4 GB. Has de triar entre `llama3.2:1b`, `llama3.2:3b` i `phi3:mini`. Escriu un cas d'us concret per a cadascun, justificant la tria.

Pistes per respondre:
- `llama3.2:1b`: tasques simples i rapides (traduccions curtes, resums).
- `llama3.2:3b`: equilibri (revisar logs, generar scripts petits).
- `phi3:mini`: raonament mes complex (analisi de dades, debugging).
- Que pèrdua de qualitat assumes amb cada tria?

## Pregunta 11 (oberta)
Quina relacio hi ha entre la mida d'un model i la qualitat de les seves respostes? Es sempre mes gran = millor? Posa exemples.

Pistes per respondre:
- Fins a un punt, mes parametres = mes capacitat.
- Pero mes enlla de 70B, els guanys son marginals.
- Un model ben entrenat de 7B pot superar un de mal entrenat de 13B.
- Que compte mes: la mida o la qualitat de l'entrenament?

## Pregunta 12 (oberta)
Si tens 8 GB de RAM al servidor, pots correr un model de 13B? Explica el calcul i les consideracions.

Pistes per respondre:
- El model de 13B en Q4 ocupa uns 8-10 GB.
- El sistema operatiu necessita 1-2 GB.
- Total: 9-12 GB, mes que els 8 disponibles.
- Solucions: swap, quantitzar mes, o triar un model de 7B.

## Pregunta 13 (oberta)
Explica per que els models especialitzats (CodeLlama, Phi-3) existeixen i quan val la pena usar-los al BernatLab.

Pistes per respondre:
- Els models especialitzats son entrenats (o afinats) amb dades especifiques.
- CodeLlama ha vist milions de repositoris de codi.
- Per a "revisar logs" un model general es bo.
- Per a "generar un script Python" un model de codi es millor.

## Pregunta 14 (oberta)
Com evaluaries si un model es prou bo per a una tasca concreta al BernatLab? Descriu un metode practic amb exemples.

Pistes per respondre:
- Pas 1: defineix 5-10 preguntes representatives de la tasca.
- Pas 2: passa-les al model i puntua les respostes (1-5).
- Pas 3: compara amb un model de referencia (o amb el "ideal").
- Pas 4: si la mitjana es >4, el model serveix.
- Exemple concret: "explica aquest log" amb 10 logs reals.

## Pregunta 15 (oberta)
Imagina que d'aqui un any els models son 10x mes petits pero igual de bons. Com canviara la teva estrategia al BernatLab?

Pistes per respondre:
- Nous models mes eficients permetran correr 13B o 30B a la RPi.
- O fer servir el mateix 3B pero a molt mes velocitat.
- Cas d'us nous: veu en temps real, analisi continu de logs.
- Quines capacitats noves desbloquegaries?
