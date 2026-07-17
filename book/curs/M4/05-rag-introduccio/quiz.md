# Qüestionari - Capitol 5: Que es RAG

> 15 preguntes · ~20 min · 7 test + 8 obertes

## Pregunta 1
Que significa RAG?

- [ ] Real AI Generation
- [x] Retrieval Augmented Generation
- [ ] Rapid Algorithmic Generation
- [ ] Recursive AI Graph

## Pregunta 2
Quin es el problema principal que RAG vol resoldre?

- [ ] Fer que el LLM vagi mes rapid
- [x] Permetre al LLM respondre sobre dades que no va veure a l'entrenament
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

- [ ] Un tipus de model d'IA
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

- [ ] Comença sempre per fine-tuning
- [ ] Comença sempre per re-entrenar
- [x] Comença per prompt engineering, afegeix RAG, i finalment fine-tuning
- [ ] Usa nomes RAG, mai prompt engineering

## Pregunta 9 (oberta)
Explica amb les teves paraules: per que RAG funciona be amb models petits? Pensa en la diferencia entre "saber moltes coses" i "tenir la informacio a la ma".

Pistes per respondre:
- Un model de 3B no pot "saber" tot sobre l'Hort Osona.
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

## Pregunta 11 (oberta)
Imagina que el teu hort te 50 fitxes de cultiu i vols que el LLM les "conegui" totes. Compara les 3 opcions: (a) ficar-les al prompt, (b) RAG, (c) fine-tuning.

Pistes per respondre:
- Opcio A: prompt massa llarg, no escala mes enlla de 5-10 fitxes.
- Opcio B: nomes carregues les 3-5 fitxes rellevants per cada pregunta.
- Opcio C: el model "aprèn" les fitxes, pero costa moltes hores i GPU.
- Argumenta quina es la millor per al BernatLab.

## Pregunta 12 (oberta)
Quina relacio hi ha entre la qualitat del "retrieval" i la qualitat de la resposta final? Es sempre millor amb mes chunks?

Pistes per respondre:
- Si passes 10 chunks, el LLM pot perdre's o confondre's.
- Si nomes passes 1, pot ser insuficient.
- Sweet spot: 3-5 chunks rellevants.
- Que passa si el chunk recuperat NO es realment rellevant?

## Pregunta 13 (oberta)
Per que RAG es considera una solucio "transparente" en comparacio amb el fine-tuning? Quines consequencies te per a la privadesa?

Pistes per respondre:
- En RAG, la font de la informacio es pot citar i verificar.
- En fine-tuning, el coneixement queda "fos" dins dels pesos del model.
- RAG es pot actualitzar en segons (afegir un document).
- Fine-tuning requereix re-entrenar.
- Que vol dir per a l'auditoria i la GDPR?

## Pregunta 14 (oberta)
Com evaluaries si el teu sistema RAG funciona be? Inventa 3 metriques practicables al BernatLab.

Pistes per respondre:
- Metrica 1: taxa de respostes correctes (1 si la resposta es bona, 0 si no).
- Metrica 2: temps de resposta (de la pregunta a la resposta).
- Metrica 3: percentatge de vegades que el chunk recuperat es realment rellevant.
- Amb 50 preguntes de test, pots tenir estadistiques representatives.

## Pregunta 15 (oberta)
Argumenta: prefereixes un RAG sobre una base de dades propia, o un model "monstruos" de 70B que ha vist tota Internet? Posa arguments per les dues bandes.

Pistes per respondre:
- Arguments a favor del RAG: privadesa, actualitzacio, verificable, baix cost.
- Arguments a favor del 70B: coneixement general, menys feina de preparacio, raonament mes sofisticat.
- Cas concret: assistent per a horticultura local (Osona).
- Tria final: defensa-la amb un argument practic.
