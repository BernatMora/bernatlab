# Resum - Capitol 2: Instal·lar Ollama, primers passos

## La idea clau

**Ollama** es un programa que et permet tenir LLMs funcionant al teu servidor amb quatre comandes. Es el "Docker dels models": descarregues, executes, i tens un API REST llest per cridar. I esta fet en Go, es rapidissim, i funciona igual a Mac, Linux, Windows i Raspberry Pi.

## Que es Ollama exactament?

Ollama es un **runtime** per a LLMs. Pensa-ho com el `dockerd` del món dels models: una vegada l'instales, pots fer:

- `ollama pull llama3.2` -> descarrega un model.
- `ollama run llama3.2` -> xateja amb el model per terminal.
- `ollama serve` -> exposa un API REST al port 11434.

Aquest API REST es la part clau per al BernatLab: podem cridar el LLM des de qualsevol script Python, Node, o shell sense reinventar la roda.

## Instal·lacio a la Raspberry Pi 4

A Debian 13 (arm64), la instal·lacio es tan simple com:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Aixo:
1. Descarrega el binari d'Ollama optimitzat per arm64.
2. Crea un usuari de sistema `ollama`.
3. Activa un servei systemd (`ollama.service`).
4. Configura el directori `/usr/share/ollama/.ollama` per guardar els models.

**Verifica la instal·lacio**:

```bash
ollama --version
# Hauria de dir algo com: ollama version 0.3.x

systemctl status ollama
# Hauria d'estar "active (running)"
```

## Els primers models

Ollama ve amb un catàleg de models al seu registre (similar al Docker Hub). Els mes interessants per a la RPi 4 son:

- **`llama3.2:1b`**: 1.3 GB de descarrega, ~1 GB de RAM en executar. Petit pero sorprenentment competent.
- **`llama3.2:3b`**: 2.0 GB de descarrega, ~2.5 GB de RAM. Bona qualitat per a textes curts.
- **`phi3:mini`**: 2.3 GB, optimitzat per a raonament.
- **`gemma2:2b`**: 1.6 GB, alternativa de Google.
- **`mistral:7b`**: 4.1 GB, pero massa per a 4 GB de RAM (cal swap o maquina mes potent).

**Com descarregar-los**:

```bash
ollama pull llama3.2:1b
ollama pull llama3.2:3b
```

## Xatejar per terminal

La forma mes rapida de provar-ho:

```bash
ollama run llama3.2:1b
```

Ara escriu el que vulguis. Per sortir, escriu `/bye`. Prova coses com:

- "Explica'm què és una Raspberry Pi en 3 frases"
- "Escriu un script en bash que compti fitxers d'un directori"
- "Tradueix al català: 'The quick brown fox jumps over the lazy dog'"

## L'API REST: la part interessant

Aqui es on Ollama brilla per al BernatLab. Un cop el servei esta actiu, pots cridar el LLM des de qualsevol lloc:

```bash
# Pregunta simple
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2:1b",
  "prompt": "Quina es la capital de Catalunya?",
  "stream": false
}'
```

Tambe te un endpoint de xat (mes convenient per a converses):

```bash
curl http://localhost:11434/api/chat -d '{
  "model": "llama3.2:1b",
  "messages": [
    {"role": "user", "content": "Hola, qui ets?"}
  ],
  "stream": false
}'
```

I un endpoint d'embeddings (que veurem al cap. 6):

```bash
curl http://localhost:11434/api/embeddings -d '{
  "model": "llama3.2:1b",
  "prompt": "Hola món"
}'
```

## Estructura de directoris

Ollama desa els models a:

- **Models descarregats**: `/usr/share/ollama/.ollama/models/` (a Linux) o `%LOCALAPPDATA%\Ollama\models\` (a Windows).
- **Configuracio del servei**: `/etc/systemd/system/ollama.service` (a Linux).
- **Logs**: `journalctl -u ollama` (a Linux).

**Atencio**: aquests fitxers son grans. Un model de 7B ocupa uns 4-8 GB. Assegura't de tenir espai al disc.

## Configuracio basica del servei

Pots ajustar el comportament d'Ollama editant el servei systemd:

```bash
sudo systemctl edit ollama
```

Afegeix, per exemple:

```ini
[Service]
Environment="OLLAMA_HOST=0.0.0.0:11434"
Environment="OLLAMA_MODELS=/mnt/dades/ollama-models"
Environment="OLLAMA_KEEP_ALIVE=10m"
```

Aixo fa que:
- Escolti a totes les interficies (no nomes localhost).
- Guardi els models a un disc de dades (no a la microSD).
- Mantingui el model carregat 10 minuts despres de la ultima consulta (accelera consultes seguides).

Despres:

```bash
sudo systemctl daemon-reload
sudo systemctl restart ollama
```

## Comandes essentials

| Comanda | Funcio |
|---|---|
| `ollama --version` | Versio instal·lada |
| `ollama list` | Models descarregats |
| `ollama pull MODEL` | Descarregar un model |
| `ollama run MODEL` | Xatejar per terminal |
| `ollama rm MODEL` | Esborrar un model |
| `ollama ps` | Models carregats a memoria |
| `ollama show MODEL` | Info detallada d'un model |
| `ollama serve` | Engegar el servidor API |

## Connexions amb altres capítols

- **Cap 1** - Que es un LLM, quina diferencia hi ha amb Ollama.
- **Cap 3** - Com triar el model correcte segons la teva maquina.
- **Cap 4** - Com fer prompts que funcionin be amb aquests models.
- **Cap 5-8** - RAG: com fer que el LLM consulti les teves dades a traves de l'API d'Ollama.
- **Cap 9** - Privadesa: Ollama es local, pero cal configurar be l'acces.
- **Cap 10** - Aplicacio concreta a l'Hort Osona.
