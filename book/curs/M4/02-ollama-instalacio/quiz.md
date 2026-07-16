# Qüestionari - Capitol 2: Instal·lar Ollama

> 10 preguntes · ~15 min

## Pregunta 1

Que es Ollama?

- [ ] Un servei de núvol per a models d'IA
- [x] Un runtime local per executar LLMs a la teva maquina
- [ ] Un editor de text amb inteligencia artificial
- [ ] Un sistema operatiu

## Pregunta 2

Quina es la comanda per instalar Ollama a Linux arm64?

- [ ] `apt install ollama`
- [x] `curl -fsSL https://ollama.com/install.sh | sh`
- [ ] `docker pull ollama`
- [ ] `pip install ollama`

## Pregunta 3

A quin port escolta per defecte el servidor d'Ollama?

- [ ] 80
- [ ] 443
- [ ] 8080
- [x] 11434

## Pregunta 4

Quina comanda fa servir Ollama per descarregar un model?

- [x] `ollama pull MODEL`
- [ ] `ollama download MODEL`
- [ ] `ollama fetch MODEL`
- [ ] `ollama get MODEL`

## Pregunta 5

Quin d'aquests models es mes petit i podria correr be a una RPi 4 amb 4 GB?

- [x] llama3.2:1b
- [ ] llama3.1:70b
- [ ] mistral:7b (quantitzat)
- [ ] mixtral:8x7b

## Pregunta 6

Quin endpoint de l'API d'Ollama serveix per fer una pregunta simple (no conversa)?

- [x] /api/generate
- [ ] /api/chat
- [ ] /api/ask
- [ ] /api/completion

## Pregunta 7

Quina comanda llista els models descarregats?

- [ ] `ollama ls`
- [x] `ollama list`
- [ ] `ollama models`
- [ ] `ollama show`

## Pregunta 8

Que passa si poses `OLLAMA_HOST=0.0.0.0:11434` al servei systemd?

- [ ] El servei nomes escolta al localhost
- [x] El servei escolta a totes les interficies de xarxa
- [ ] El servei es desactiva
- [ ] El servei falla per error de configuracio

## Pregunta 9 (oberta)

Per que es important configurar `OLLAMA_MODELS=/mnt/dades/ollama-models` en comptes de deixar el directori per defecte? Pensa en quin es el problema de la microSD.

Pistes per respondre:
- La microSD te vida util limitada per les escriptures.
- Els models son fitxers grans (1-10 GB).
- Descarregar i actualitzar models implica moltes escriptures.
- Que passa si la SD es mor?

## Pregunta 10 (oberta)

Descriu el flux complet, des de la terminal, per fer una pregunta a un LLM local amb Ollama: descarrega, execucio interactiva, i comanda curl per cridar l'API. Escriu els 3 passos amb les comandes.

Pistes per respondre:
- Pas 1: descarregar el model amb `ollama pull`.
- Pas 2: provar interactivament amb `ollama run`.
- Pas 3: cridar l'API REST amb `curl`.
- Quin JSON has d'enviar a `/api/generate`?
