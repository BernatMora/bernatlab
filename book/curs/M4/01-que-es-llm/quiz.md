# Qüestionari - Capitol 1: Que es un LLM

> 15 preguntes · ~20 min · 7 test + 8 obertes

## Pregunta 1
Que significa LLM?

- [ ] Long Learning Machine
- [x] Large Language Model
- [ ] Local Language Module
- [ ] Logical Linguistic Model

## Pregunta 2
Com "aprèn" un LLM?

- [ ] Llegint un manual de regles escrit per humans
- [x] Ajustant milers de milions de numeros a partir de molt text
- [ ] Copiant respostes d'una base de dades
- [ ] Preguntant a Internet en temps real

## Pregunta 3
Que es una "al·lucinacio" en un LLM?

- [ ] Un error de memoria RAM
- [ ] Un somni que te el model quan no treballa
- [x] Una resposta inventada que sona a verdadera pero no te fonament
- [ ] Una imatge generada per error

## Pregunta 4
Quina es la mida aproximada de la finestra de context tipica d'un LLM modern?

- [ ] 100 paraules
- [ ] 1.000 paraules
- [x] Entre 4.000 i 128.000 tokens
- [ ] Infinita

## Pregunta 5
Quin d'aquests NO es un LLM?

- [ ] Llama 3
- [ ] Mistral
- [ ] GPT-4
- [x] InfluxDB

## Pregunta 6
Quina es la diferencia principal entre "IA" i "LLM"?

- [ ] Son sinonims
- [x] LLM es un tipus especific d'IA entrenat per a llenguatge
- [ ] La IA es mes moderna que el LLM
- [ ] LLM nomes funciona en local

## Pregunta 7
Quin hardware minim necessita un LLM petit (1B-3B) per correr en local?

- [ ] 32 GB de RAM i una GPU NVIDIA
- [x] Uns 4 GB de RAM i CPU ARM/x86
- [ ] 256 MB de RAM
- [ ] Només una microSD

## Pregunta 8 (oberta)
Explica amb les teves paraules: per que un LLM pot semblar que "sap" coses tot i no tenir cap base de dades a dins? Quina es la diferencia entre "saber" i "semblar que sap"?

Pistes per respondre:
- Pensa en el mecanisme d'entrenament: que ha fet amb els textos?
- Com genera les respostes, paraula a paraula o per comprensio?
- Que vol dir que "prediu la paraula seguent"?

## Pregunta 9 (oberta)
Imagina que vols muntar un assistent al BernatLab que t'ajudi a entendre els logs del sistema. Quins avantatges i quins riscos tindria fer-ho amb un LLM local? Escriu 3 avantatges i 3 riscos.

Pistes per respondre:
- Avantatges: privadesa, cost, disponibilitat, personalitzacio.
- Riscos: al·lucinacions, limitacions de context, idioma del model, hardware.
- Concret: quines dades dels logs NO hauries de compartir amb un model extern?

## Pregunta 10 (oberta)
Per que creus que es important entendre que un LLM nomes "prediu la paraula seguent" abans de posar-lo a produccio al BernatLab? Posa dos exemples concrets on aquesta limitacio podries portar-te problemes.

Pistes per respondre:
- Cas 1: el model et dona una IP o un port que "sona" be pero no es correcte.
- Cas 2: el model et recomana una comanda perillosa perque l'ha vist en exemples obsolets.
- Que te aixo a veure amb la responsabilitat de l'operador huma?

## Pregunta 11 (oberta)
Quina analogia de la vida quotidiana triaries per explicar a una persona no tecnica que es un LLM? Explica-la amb detall, asegurant-te que l'analogia no es presta a confusions.

Pistes per respondre:
- Que NO ha de tenir l'analogia: la persona no ha de creure que el LLM "pensa" o "entén".
- Possibles analogies: el becari molt llest, l'estadistic obsessionat, el cuiner que replica receptes.
- Quins punts febles te la teva analogia?

## Pregunta 12 (oberta)
Relaciona el concepte de "finestra de context" amb el BernatLab concret. Si tens un LLM que vols que analitzi els logs d'una setmana sencera (uns 50.000 logs), que passara i com ho solucionaries?

Pistes per respondre:
- Quants tokens ocupa una linia de log tipica?
- Quina es la finestra del model que tens pensat fer servir?
- Estrategia 1: passar nomes els ultims N logs.
- Estrategia 2: resumir previament amb un altre model o un script.
- Estrategia 3: dividir la setmana en blocs i fer N consultes.

## Pregunta 13 (oberta)
Per a que NO faries servir un LLM en el context del BernatLab? Dona tres exemples concrets i justifica per que una eina tradicional (script, alerta, base de dades) es millor.

Pistes per respondre:
- Exemple 1: comptar quantes alertes de temperatura has tingut aquest mes.
- Exemple 2: decidir si un login es valid o no.
- Exemple 3: generar el backup encriptat de la base de dades.
- Que tenen en comu aquests tres casos? Determinisme, fiabilitat, velocitat.

## Pregunta 14 (oberta)
Quin impacte te la "data de tall" de l'entrenament d'un LLM al seu us al BernatLab? Si vols preguntar-li sobre una versio nova de Docker o un CVE recent, que pot passar?

Pistes per respondre:
- La data de tall es la data fins a la qual el model ha vist exemples.
- Si el model es de fa 2 anys, no sap res de les ultimes vulnerabilitats.
- Això es un risc de seguretat? Per que?
- Complementar amb RAG o documentacio propia pot ser la solucio.

## Pregunta 15 (oberta)
Argumenta la teva posicio: prefereixes un LLM local de 3B o un de 70B al núvol per al teu homelab? Pesa arguments a favor i en contra, i finalment defensa una opcio.

Pistes per respondre:
- Arguments pel local: privadesa, cost, disponibilitat, personalitzacio.
- Arguments pel núvol: qualitat, velocitat, finestra mes gran.
- Cas concret: el BernatLab genera dades sensibles (logs, sensors, configuracio).
- Tria final: justifica-la.
