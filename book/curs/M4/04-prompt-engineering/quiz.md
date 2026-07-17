# Qüestionari - Capitol 4: Prompt engineering

> 15 preguntes · ~20 min · 7 test + 8 obertes

## Pregunta 1
Que es prompt engineering?

- [ ] Una eina per entrenar LLMs
- [x] L'art d'escriure prompts que extreuen el millor del model
- [ ] Un llenguatge de programacio especific per a IA
- [ ] Un sistema operatiu per a models

## Pregunta 2
Quin es el problema d'un prompt generic com "Explica els servidors"?

- [ ] Es massa llarg
- [x] El model no sap quin nivell de detall, quina audiencia ni quin format vols
- [ ] Es massa tecnic
- [ ] Cap, funciona igual de be

## Pregunta 3
Que es el "role prompting"?

- [ ] Una tecnica per canviar el rol del sistema operatiu
- [x] Assignar un rol o personalitat al LLM (ex. "Ets un expert en Linux amb 20 anys d'experiencia")
- [ ] Un sistema per validar respostes
- [ ] Un metode per entrenar el model

## Pregunta 4
Quina es la tecnica de "few-shot prompting"?

- [ ] Entrenar el model amb poques dades
- [x] Mostrar exemples al model dins del prompt per ensenyar-li el format desitjat
- [ ] Fer poques preguntes al model
- [ ] Usar nomes un model petit

## Pregunta 5
Quin d'aquests es un bon prompt?

- [ ] "Explica Docker."
- [x] "Explica quines son les 3 diferencies principals entre Docker i Podman en menys de 100 paraules, en catala."
- [ ] "Docker?"
- [ ] "Fes alguna cosa amb servidors"

## Pregunta 6
Que vol dir "system prompt"?

- [ ] Un prompt que nomes l'admin pot veure
- [x] Un missatge inicial que defineix el comportament general del model per a tota la conversa
- [ ] Una actualitzacio del sistema
- [ ] Un prompt automatic

## Pregunta 7
Quina es la diferencia entre "temperature=0" i "temperature=1"?

- [ ] Es el mateix
- [x] Temperature baixa = respostes mes deterministes; alta = mes creatives i aleatories
- [ ] Temperature alta = mes rapid
- [ ] Temperature baixa = mes llarg

## Pregunta 8 (oberta)
Explica amb les teves paraules: quines son les 4 regles d'or d'un bon prompt? Posa un exemple de "mal prompt" i la seva versio "bona" per a cada regla.

Pistes per respondre:
- Regla 1: sigues especific (no "explica X", sino "explica X en N paraules, per a Y audiencia").
- Regla 2: dona context (qui ets, que necessites).
- Regla 3: dona exemples si cal (few-shot).
- Regla 4: especifica el format de sortida (llista, taula, JSON, prosa).

## Pregunta 9 (oberta)
Per que creus que un system prompt ben fet pot canviar completament la qualitat de les respostes d'un model de 3B? Dona un exemple concret aplicat al BernatLab.

Pistes per respondre:
- El system prompt estableix el "personatge" i les regles del model.
- Un 3B amb un bon system prompt pot superar un 7B sense system prompt.
- Exemple: un prompt que diu "sempre respon en catala, sigues concis, cita la font si la tens".
- Aixo es el que fan els "agents" d'IA per especialitzar models petits.

## Pregunta 10 (oberta)
Imagina que vols que el LLM t'ajudi a generar fitxes tecniques de cultius per a l'Hort Osona. Escriu un system prompt complet que faries servir, justificant cada part.

Pistes per respondre:
- Qui es el model (expert en horticultura?).
- Quin format ha de tenir la sortida (titols, apartats, longitud).
- Quin to (tecnic, planer, en catala).
- Que NO ha de fer (inventar dades, opinions politiques).
- Aixo te limitacions? Com les mitigaries?

## Pregunta 11 (oberta)
Quina relacio hi ha entre la longitud del prompt i el cost (o temps) de cada consulta? Si el BernatLab fa 1.000 consultes al dia, com afecta un prompt llarg?

Pistes per respondre:
- Cada token del prompt es procesat i compta.
- Un prompt de 500 tokens = 500 tokens de "cost" d'entrada.
- Si la consulta es llarga, el model triga mes a respondre.
- Estratègies: prompts curts, prompts reusables, cache de respostes.

## Pregunta 12 (oberta)
Experimenta amb el "chain of thought" (pas a pas): si li demanes al model "tinc 64 pomes i en dono la quarta part al meu vei, quantes me'n queden?", pot fallar. Pero si li dius "pas a pas", millora. Per que?

Pistes per respondre:
- El model es mes bo raonant pas a pas que amb el resultat directe.
- "Chain of thought" l'obliga a exterioritzar el raonament.
- Aplica a tasques complexes: analisi de logs, debugging, calculs.
- Aplica aixo al BernatLab: com ho faries servir?

## Pregunta 13 (oberta)
Compara el "zero-shot" (sense exemples) i el "few-shot" (amb exemples) per a una tasca concreta al BernatLab. Posa exemples reals.

Pistes per respondre:
- Zero-shot: "Classifica aquesta alerta: 'CPU > 90%'".
- Few-shot: mostrar 3 exemples de classificacio (info, warning, critical) abans.
- Quan pocs exemples ajuden? Quan saturen el context?
- Regla: few-shot nomes si la tasca es molt especifica.

## Pregunta 14 (oberta)
Quines consequencies te usar "temperature=0" en un script automatitzat al BernatLab? I "temperature=1"? Posa exemples.

Pistes per respondre:
- temperature=0: respostes consistents, bones per a tasques repetitives.
- temperature=1: respostes variades, bones per a creativitat.
- Cas 1: resumir logs automaticament -> temperature=0.
- Cas 2: generar varietats de noms per a fitxes -> temperature=1.
- Riscos: temperatures altes poden generar respostes incoherents.

## Pregunta 15 (oberta)
Si nomes tens 30 segons per escriure un prompt al LLM, quines son les 3 coses que SI o SI hi posaries? Argumenta la resposta.

Pistes per respondre:
- Element essencial 1: rol/persona del model.
- Element essencial 2: format de la sortida esperat.
- Element essencial 3: context o restriccions clau.
- Que NO cal posar-hi? (detalls excessius, informacio redundant).
- Practica: escriu un prompt seguint aquesta regla per a una tasca del BernatLab.
