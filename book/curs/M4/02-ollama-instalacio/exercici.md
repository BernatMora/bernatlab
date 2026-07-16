# Exercici practic - Capitol 2: Instal·lar Ollama

> 30-45 min · Real al teu servidor

## Objectiu

Instal·lar Ollama a la teva Raspberry Pi 4 (o maquina virtual Linux), descarregar el teu primer model, i fer una consulta tant per terminal com per API REST. Tot seguint el patro "executar, verificar, documentar".

## Requisits

- Tailscale actiu
- Connexio SSH a la RPi (o terminal local)
- 30-45 minuts
- ~3 GB d'espai lliure al disc

## Pas 1: Instal·la Ollama (5 min)

Connecta't per SSH i executa:

```bash
# Descarrega i instala
curl -fsSL https://ollama.com/install.sh | sh

# Verifica
ollama --version

# Comprova que el servei esta actiu
systemctl status ollama
```

Si tot ha anat be, veuras algo com `ollama version 0.3.x` i el servei `active (running)`.

## Pas 2: Mou el directori de models (opcional pero recomanable) (5 min)

Si tens un disc de dades muntat a `/mnt/dades`, moures els models allà per no esgotar la microSD:

```bash
sudo systemctl edit ollama
```

Afegeix aquestes linies:

```ini
[Service]
Environment="OLLAMA_MODELS=/mnt/dades/ollama-models"
```

Despres:

```bash
sudo systemctl daemon-reload
sudo systemctl restart ollama
```

Verifica:

```bash
systemctl show ollama | grep OLLAMA_MODELS
```

## Pas 3: Descarrega el teu primer model (5-10 min)

```bash
# Comprova els models disponibles
ollama list
# Primer cop pot estar buit

# Descarrega un model petit (1.3 GB)
ollama pull llama3.2:1b

# Descarrega un altre per comparar
ollama pull llama3.2:3b

# Llista els models descarregats
ollama list
```

Aixo pot trigar una estona segons la connexio. Tingues paciencia.

## Pas 4: Xateja per terminal (5 min)

```bash
ollama run llama3.2:1b
```

Prova les seguents preguntes (copia-enganxa una a una):

- `Hola, qui ets?`
- `Explica'm què és una Raspberry Pi en 3 frases`
- `Escriu un script bash que compti els fitxers d'un directori`
- `Quina és la capital de la comarca d'Osona?`

Per sortir: `/bye`.

**Observa**:
- El temps que triga a respondre (hauries de veure tokens/segon al terminal).
- La qualitat de les respostes. Es prou bona?
- Que passa si li fas la mateixa pregunta dos cops? Repeteix exactament?

## Pas 5: Crida l'API REST (10 min)

Ollama escolta a `http://localhost:11434`. Prova les seguents comandes:

**Endpoint /api/generate** (pregunta simple):

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2:1b",
  "prompt": "Quants dies te un any de traspas?",
  "stream": false
}'
```

**Endpoint /api/chat** (conversa):

```bash
curl http://localhost:11434/api/chat -d '{
  "model": "llama3.2:1b",
  "messages": [
    {"role": "user", "content": "Resum en una frase que es Docker."}
  ],
  "stream": false
}'
```

**Endpoint /api/tags** (llistar models):

```bash
curl http://localhost:11434/api/tags
```

**Endpoint /api/ps** (models carregats):

```bash
curl http://localhost:11434/api/ps
```

## Pas 6: Documenta la teva experiencia (10 min)

Crea un fitxer `book/curs/M4/02-ollama-instalacio/primera-consulta.md` amb:

- Versio d'Ollama instal·lada.
- Models descarregats i mida de cada un.
- Temps de resposta mig de `llama3.2:1b` (usa `time` davant de la comanda curl).
- La teva valoracio subjectiva de la qualitat (1-5).
- Captura de pantalla o sortida copiada de les respostes.

## Validacio

Has acabat si:
- [ ] Ollama esta instal·lat i el servei esta `active (running)`.
- [ ] Has descarregat almenys un model.
- [ ] Has xatejat amb el model per terminal i has vist resposta.
- [ ] Has fet una crida a l'API REST amb `curl` i has rebut JSON.
- [ ] Has documentat la teva experiencia a `primera-consulta.md`.

## Per aprofundir

- Prova el flag `stream: true` al `/api/generate` per veure la resposta paraula a paraula.
- Investiga quina es la diferencia entre els endpoints `/api/generate` i `/api/chat`.
- Prova a canviar el model a `phi3:mini` i compara la velocitat amb `llama3.2:1b`.
- Monitora l'us de RAM durant una consulta: `watch -n 1 'free -h'`.
