# Quiz - Capitol 10: Aplicacio a Hort Osona

## Pregunta 1
Quants documents te aproximadament la base de coneixement d'Hort Osona?

- [ ] 10
- [ ] 30
- [x] 76
- [ ] 500

## Pregunta 2
Quines tres eines formen el sistema complet de l'Hort Osona?

- [ ] Open WebUI, Ollama, InfluxDB
- [x] Open WebUI, Ollama, ChromaDB
- [ ] Open WebUI, Grafana, Ollama
- [ ] Telegram, Ollama, InfluxDB

## Pregunta 3
Quina ordre serveix per clonar el repositori d'Hort Osona?

- [x] git clone https://github.com/BernatMora/hort-osona.git
- [ ] git pull hort-osona
- [ ] curl https://github.com/hort-osona
- [ ] wget hort-osona.tar.gz

## Pregunta 4
Quin es el model d'embeddings que es fa servir a l'exemple d'indexacio?

- [ ] llama3.2
- [x] nomic-embed-text
- [ ] mistral
- [ ] gemma

## Pregunta 5
Quin es el valor per defecte de k a la funcio `ask_hort`?

- [ ] 1
- [ ] 3
- [x] 5
- [ ] 10

## Pregunta 6
Quina pregunta NO esta entre les proves suggerides?

- [ ] Com es planta el tomàquet a Osona?
- [ ] Quines plagues pateix l'enciam al juliol?
- [ ] Quan s'ha de sembrar la carbassa?
- [x] Quin es el preu del quilo de mongetes?

## Pregunta 7 (oberta)
Descriu l'arquitectura completa del sistema Hort Osona amb les 4 parts principals. Que fa cada una?

Pistes:
- Open WebUI (frontend)
- Ollama (LLM)
- ChromaDB (vector store)
- Script d'indexacio
- Flux de dades

## Pregunta 8 (oberta)
Explica el flux d'una consulta a l'Hort Osona des que l'usuari escriu la pregunta fins que rep la resposta.

Pistes:
- Embedding de la pregunta
- Cerca a ChromaDB
- Prompt amb contexte
- Generacio del LLM
- Fonts

## Pregunta 9 (oberta)
Quines limitacions te el sistema actual? Com les podries millorar?

Pistes:
- Qualitat dels embeddings
- Velocitat a la RPi
- Cobertura de documents
- Catalan del LLM

## Pregunta 10 (oberta)
Imagina que vols afegir el sistema a Telegram. Quins canvis caldria fer?

Pistes:
- API de Telegram
- On corre cada part
- Temps real
- Limitacions
