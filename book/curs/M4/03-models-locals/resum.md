# Resum - Capitol 3: Triar el model adequat

## La idea clau

No tots els models valen per a tot. Un model de 70B parametres donara respostes impressionants pero necessita un servidor de 50.000 euros. Un de 1B es rapid pero sembla tonto. La gracia esta en trobar el **punt just**: el model mes petit que et dona la qualitat que necessites pel teu hardware.

## Que vol dir "X B parametres"?

Els parametres son els numeros que el model ha après durant l'entrenament. Mes parametres = mes capacitat (fins a un punt). Mes parametres = mes RAM i mes lent.

Referencies rapides:
- **1B parametres**: ~2 GB en RAM (quantitzat Q4). Molt basic, pero valid.
- **3B**: ~2.5 GB en RAM. Serveix per a feines simples.
- **7B**: ~4-5 GB en RAM. Bona qualitat, sweet spot per a molts casos.
- **13B**: ~8 GB. Notable.
- **30B**: ~18 GB. Excel·lent pero ja cal maquina potent.
- **70B**: ~40 GB. Nomes amb GPU.

**La regla**: cada 2x parametres necessita ~2x mes RAM.

## Que es la quantitzacio?

Els models s'entrenen en **float32** (32 bits per numero). Pero per executar-los en hardware modest, es poden comprimir a:

- **Q8 (8 bits)**: ocupacio ~25% del original, perdua minima de qualitat.
- **Q4 (4 bits)**: ocupacio ~12.5% del original, perdua moderada. La mes comuna.
- **Q2 (2 bits)**: ocupacio ~6%, perdua important. Nomes per a hardware molt limitat.

**Exemple**: un model de 7B en float32 ocupa 28 GB. En Q4, nomes 4 GB. La diferència de qualitat es petita per a la majoria d'usos.

A Ollama, la majoria de models ja venen quantitzats en Q4_0 per defecte. Es el millor equilibri.

## Quin model triar per a la RPi 4 (4 GB)?

| Model | Mida | RAM | Velocitat | Qualitat |
|---|---|---|---|---|
| `llama3.2:1b` | 1.3 GB | ~1.2 GB | 30+ t/s | Basica |
| `llama3.2:3b` | 2.0 GB | ~2.5 GB | 10-15 t/s | Bona |
| `phi3:mini` (3.8B) | 2.3 GB | ~3 GB | 8-12 t/s | Molt bona |
| `gemma2:2b` | 1.6 GB | ~1.8 GB | 20+ t/s | Bona |
| `mistral:7b` | 4.1 GB | ~5 GB | No a RPi 4 | Excel·lent |

`t/s` vol dir "tokens per segon". Un bon ritme per a xatejar es 10-20 t/s. Per sota de 5 t/s es fa pesat.

**Recomanacio per a la RPi 4**:
- **Per defecte**: `llama3.2:3b` (bon equilibri).
- **Si necessites velocitat**: `llama3.2:1b`.
- **Si necessites qualitat i tens paciencia**: `phi3:mini`.

## Models especialitzats

A mes dels models generals, n'hi ha d'especialitzats:

- **CodeLlama / CodeGemma**: optimitzats per a codi. Bona opcio si vols generar scripts.
- **Mistral / Llama**: generals, bons per a xat i resums.
- **Phi-3**: optimitzat per a raonament logic i matematiques.
- **Llama 3.2 Vision**: pot processar imatges. Requereix mes memoria.
- **Nomic-Embed / MXBAI-Embed**: nomes per a embeddings (cap. 6), no generen text.

## Com avaluar la qualitat d'un model

A banda de proves subjectives, hi ha benchmarks estandard:

- **MMLU**: coneixements generals (historia, ciencia, etc.).
- **HumanEval**: generar codi Python correcte.
- **GSM8K**: problemes matematics de primaria.
- **HellaSwag**: sentit comu.

Per a les nostres necessitats al BernatLab, els mes utils son **HumanEval** (scripts shell/Python) i **GSM8K** (interpretar dades numeriques de sensors).

**En la practica**: proba el model amb les teves preguntes tipiques. Si falla, puja de mida. Si va lent, baixa de mida.

## Com canviar de model a Ollama

Ollama permet tenir multiples models instal·lats i triar quin fer servir per consulta:

```bash
# Llistar models
ollama list

# Usar un o un altre en una consulta
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2:1b",
  "prompt": "...",
  "stream": false
}'

curl http://localhost:11434/api/generate -d '{
  "model": "phi3:mini",
  "prompt": "...",
  "stream": false
}'
```

Pots tenir **un model carregat a la vegada** (els petits) o **diversos** (si tens RAM). Ollama els carrega sota demanda.

## Estrategies per a hardware limitat

Si la teva RPi va molt justa de RAM:

- **Usa models mes petits** (1B-3B).
- **Limita la longitud maxima** amb el parametre `num_predict`:
  ```json
  {"model": "llama3.2:3b", "prompt": "...", "num_predict": 200}
  ```
  Aixi el model no genera mes de 200 tokens.
- **Limita la finestra de context** amb `num_ctx`:
  ```json
  {"num_ctx": 2048}
  ```
- **Usa swap al disc** (lent pero pot salvar la vida).
- **Configura OLLAMA_MAX_LOADED_MODELS=1** per carregar nomes un a la vegada.

## Quant triga un model a carregar?

- **1B en Q4**: 1-3 segons (des de SSD).
- **3B en Q4**: 3-8 segons.
- **7B en Q4**: 8-20 segons.
- **13B en Q4**: 15-40 segons.

Un cop carregat, les respostes es generen a uns 5-30 tokens per segon en una RPi 4 (depen del model).

**Configurar `OLLAMA_KEEP_ALIVE`** per evitar recarregar:
- `"5m"`: 5 minuts (per defecte).
- `"1h"`: 1 hora (per a usos recurrents).
- `"-1"`: sempre carregat.
- `"0"`: descarrega inmediatament despres de cada consulta.

## Connexions amb altres capítols

- **Cap 2** - Com instalar i fer anar Ollama amb aquests models.
- **Cap 4** - Un cop triat el model, com parlar-hi be.
- **Cap 5-8** - RAG: els models petits poden fer molt si els dones contexte relevant.
- **Cap 9** - Com afecta la tria de model a la privadesa.
- **Cap 10** - Aplicacio concreta a l'Hort Osona: quin model hem triat i per que.
