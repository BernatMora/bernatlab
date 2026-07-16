# Qüestionari - Capitol 3: Triar el model adequat

> 10 preguntes · ~15 min

## Pregunta 1

Que volen dir les "B" en "7B parametres"?

- [ ] Bytes
- [x] Bilions (milers de milions)
- [ ] Bits
- [ ] Bytes per segon

## Pregunta 2

Quina es la mida aproximada en RAM d'un model de 7B quantitzat en Q4?

- [ ] 1 GB
- [ ] 2 GB
- [x] 4-5 GB
- [ ] 28 GB

## Pregunta 3

Que vol dir "Q4" en quantitzacio?

- [ ] 4 cores de CPU
- [x] 4 bits per parametre (comprimit)
- [ ] 4 capes de xarxa neuronal
- [ ] Qualitat 4 sobre 5

## Pregunta 4

Quin model es el mes adequat per defecte a una RPi 4 amb 4 GB de RAM?

- [ ] llama3.1:70b
- [ ] mistral:7b quantitzat
- [x] llama3.2:3b
- [ ] mixtral:8x7b

## Pregunta 5

Quants tokens per segon es consideren un bon ritme per a xatejar?

- [ ] 1-2 t/s
- [x] 10-20 t/s
- [ ] 50-100 t/s
- [ ] 1000+ t/s

## Pregunta 6

Que fa el parametre `num_predict` a Ollama?

- [ ] Diu quantes vegades pot predir el model
- [x] Limita el maxim de tokens que pot generar en una resposta
- [ ] Indica quantes capes de xarxa te
- [ ] Es el nom del prompt

## Pregunta 7

Que fa `OLLAMA_KEEP_ALIVE=-1`?

- [ ] Descarrega el model despres de cada consulta
- [ ] Carrega el model nomes al primer usuari
- [x] Mantindra el model carregat a memoria indefinidament
- [ ] No fa res especial

## Pregunta 8

Quin d'aquests benchmarks mesura la capacitat de generar codi correcte?

- [ ] MMLU
- [x] HumanEval
- [ ] GSM8K
- [ ] HellaSwag

## Pregunta 9 (oberta)

Tens una Raspberry Pi 4 amb 4 GB de RAM. Has d'analitzar logs del sistema per detectar anomalies. Voldries un model que:
- Analitzi linies de log en catala/angles
- Suggerisca possibles causes
- Generi comandes de shell per resoldre el problema

Explica quin model triaries (entre els que hem vist), per que, i quines limitacions veuràs.

Pistes per respondre:
- Considera el volum de logs (10 linies? 10.000?).
- Com ho faries amb un model de 1B vs un de 3B?
- Que passaria amb un model que nomes "sap" angles?
- Es preferible velocitat o qualitat aqui?

## Pregunta 10 (oberta)

Descriu la diferencia entre usar un model de 7B quantitzat en Q4 i un de 7B en float32. Pensa en: mida, qualitat, RAM necessaria, cas d'us.

Pistes per respondre:
- Mida al disc: 28 GB vs 4 GB.
- RAM: quants GB ocupa cada un carregat?
- Qualitat: hi ha diferencies notaves? En quines tasques?
- Quan val la pena la versio sense comprimir?
