# Capítol 35 — Com triar el millor model: mida, velocitat, qualitat, català

> *"Triar un model d'IA és com triar una eina: la clau no és la que té més prestacions, sinó la que s'adapta a la feina."*

## 35.1 Què mesura un "bon" model

Hi ha quatre dimensions que importen:

1. **Mida** (quantitat de paràmetres). Més paràmetres = més savi però més lent i pesat. Es mesura en mil milions de paràmetres (B). Exemples: 1B, 3B, 7B, 13B, 70B.

2. **Velocitat** (tokens per segon). Quants tokens pot generar per segon. Un Mac M1 amb un model 7B genera ~20-30 tokens/s. Un model 70B genera 2-5 tokens/s.

3. **Qualitat** (precisió, raonament, coneixement). En general, com més gran el model, millor la qualitat. Però hi ha models petits que són excel·lents en tasques específiques.

4. **Català** (suport lingüístic). Alguns models parlen millor català que d'altres. Cal validar amb proves reals.

## 35.2 Models recomanats el 2026

Aquesta llista canvia cada mes. Però a data de juliol 2026, els models locals més interessants per al BernatLab són:

### Models petits (1B-4B) — per a Mac amb 8-16 GB de RAM

| Model | Mida | Qualitat | Català | Ús recomanat |
|---|---|---|---|---|
| **gemma3:2b** | 1.6 GB | Bona per a tasques simples | Acceptable | Comandes ràpides, resums curts |
| **gemma3:4b** | 3.1 GB | Bona | Bona | Primera opció per a 8-16 GB |
| **phi3:mini** | 2.3 GB | Excel·lent per a la mida | Acceptable | Raonament, codi |
| **llama3.2:3b** | 2.0 GB | Bona | Bona | Alternativa a gemma3 |
| **qwen2.5:3b** | 1.9 GB | Bona | Molt bona | Multilingüe |

### Models mitjans (7B-14B) — per a Mac amb 24-32 GB de RAM

| Model | Mida | Qualitat | Català | Ús recomanat |
|---|---|---|---|---|
| **gemma3:12b** | 8.1 GB | Molt bona | Molt bona | Recomanat per a 16-32 GB |
| **llama3.2:11b** | 6.9 GB | Molt bona | Bona | Alternativa |
| **mistral:7b** | 4.1 GB | Bona | Bona | Clàssic |
| **mixtral:8x7b** | 26 GB | Excel·lent | Bona | Si tens 32 GB |
| **qwen2.5:14b** | 8.7 GB | Molt bona | Excel·lent | El millor en català |

### Models grans (30B-70B) — per a Mac amb 64+ GB o PC amb GPU

| Model | Mida | Qualitat | Català | Ús recomanat |
|---|---|---|---|---|
| **llama3.1:70b** | 40 GB | Excel·lent | Molt bona | Si tens molta RAM |
| **gemma3:27b** | 17 GB | Excel·lent | Excel·lent | Bon equilibri |
| **qwen2.5:32b** | 19 GB | Excel·lent | Excel·lent | El millor en català |
| **deepseek-r1:32b** | 19 GB | Excel·lent | Bona | Raonament complex |

## 35.3 Com triar segons el teu hardware

### MacBook Air M1/M2 amb 8 GB

- Limita't a models d'1-3B.
- Recomanació: `gemma3:2b` o `phi3:mini`.
- Compromís: qualitat baixa però usable per a consultes curtes.

### MacBook Pro M2/M3 amb 16 GB

- Models de 4-8B funcionen bé.
- Recomanació: `gemma3:4b` per defecte, `llama3.2:11b` si necessites més.
- Bon equilibri velocitat/qualitat.

### MacBook Pro M3 Max/M4 amb 32-64 GB

- Models de 14-27B funcionen bé.
- Recomanació: `gemma3:12b` o `qwen2.5:14b` per defecte.
- Qualitat alta, velocitat acceptable.

### Mac Studio M2 Ultra amb 64-192 GB

- Models de 30-70B funcionen.
- Recomanació: `gemma3:27b` o `llama3.1:70b`.
- Qualitat màxima.

### Raspberry Pi 4 amb 4-8 GB

- Només models d'1-2B.
- Recomanació: `gemma3:2b` o `phi3:mini`.
- Útil només per a comandes molt senzilles.

### PC amb GPU NVIDIA RTX 3060+ (8 GB VRAM)

- Models de 7-13B amb quantització (tècnica que redueix la mida del model comprimits els pesos en menys bits, amb pèrdua mínima de qualitat).
- Recomanació: `mistral:7b-q4` (q4 vol dir quantització de 4 bits).
- Molt bona velocitat si tens CUDA ben configurat.

## 35.4 Què és la quantització

Els models venen en diverses mides segons la quantització. Per exemple:

- `gemma3:12b` (8.1 GB) — versió completa, 16 bits per paràmetre.
- `gemma3:12b-q4_K_M` (5.5 GB) — quantitzat a 4 bits, qualitat gairebé idèntica.
- `gemma3:12b-q8_0` (7.5 GB) — quantitzat a 8 bits, qualitat excel·lent.

La regla és senzilla: **amb la quantització Q4_K_M tens el millor equilibri mida/qualitat**. Q8 és lleugerament millor però ocupa més. Q2 i Q3 són massa agressives (perden qualitat notable).

Per descarregar una versió quantitzada:

```bash
ollama pull gemma3:12b-q4_K_M
```

## 35.5 Com avaluar el català

El català varia molt entre models. Comprovacions pràctiques:

1. **Cultura general**. Pregunta: "Qui va escriure 'La plaça del Diamant'?" Si respon "Mercè Rodoreda", perfecte.

2. **Varietats dialectals**. Pregunta: "Com es diu 'mongeta' a Osona?" Si respon amb termes locals, encara millor.

3. **Termes tècnics**. Pregunta: "Què és el mildiu del tomàquet?" Si dóna una resposta correcta i completa, endavant.

4. **Generació de text**. Demana-li que escrigui un correu o una recepta. Mira si l'estil és natural.

5. **Codi**. Si vols que t'ajudi amb Python o scripts, avalua la qualitat del codi.

Fes una llista de 10 preguntes representatives i avalua cada model. Al cap de 2-3 dies tindràs clar quin és el millor per a tu.

## 35.6 Com canviar de model fàcilment

Pots tenir molts models descarregats alhora i canviar segons la tasca:

```bash
# Llista els que tens
ollama list

# Per defecte usa el millor
ollama run qwen2.5:14b "..."

# Per a resums ràpids, un de més petit
ollama run gemma3:4b "Resumeix: ..."
```

Si vols que el teu sistema sempre usi un model concret per defecte, crea un alias:

```bash
# Crea un alias "assistent" apuntant al millor model
ollama cp gemma3:12b assistent

# Ara pots fer
ollama run assistent "Hola"
```

Això és útil quan configures l'API al Cap 39: simplement fas servir el nom de l'alias.

## 35.7 El cas especial: el català

El català és un idioma amb menys recursos que l'anglès o el castellà, però la situació ha millorat molt. Al 2026, els millors models en català són:

- **qwen2.5** (Alibaba): entrenat explícitament en molts idiomes, català inclòs.
- **gemma3** (Google): bon català, sobretot en les versions 12B+.
- **llama3.1** (Meta): bon català en versions grans.

Els pitjors en català solen ser:

- Models antics (llama2, mistral v1).
- Models massa petits (<3B) de qualsevol família.
- Models entrenats només en anglès.

Si el català és crític (i per a tu ho és), tria `qwen2.5:14b` o `gemma3:12b-q4_K_M`. Són els millors equilibris.

## 35.8 Com optimitzar la velocitat

Algunes tècniques per accelerar la resposta:

1. **Reduir el context**. Per defecte, Ollama carrega 2048 tokens. Si la teva consulta és curta, pots posar `num_ctx 1024`.

2. **Usar quantització Q4_K_M**. És el punt òptim.

3. **Tancar altres aplicacions**. El Mac comparteix RAM entre totes les aplicacions. Si tens Chrome amb 50 pestanyes, l'Ollama va més lent.

4. **Pre-escalfar el model**. La primera resposta és lenta perquè carrega el model a RAM. Després va ràpid.

5. **Servir vs conversar**. Si vols velocitat màxima, usa l'API HTTP (Cap 39) en lloc del mode conversa.

## 35.9 Les meves recomanacions finals

Per al teu cas (Mac, Osona, hort, català):

- **Si tens 16 GB**: comença amb `gemma3:4b` per explorar, puja a `gemma3:12b-q4_K_M` quan vulguis més qualitat.
- **Si tens 32 GB**: directament `gemma3:12b` o `qwen2.5:14b`.
- **Si tens 64 GB**: `qwen2.5:32b` per a la màxima qualitat en català.
- **Per a resums ràpids**: `gemma3:4b` sempre va bé.
- **Per a tasques complexes**: puja a 12B o 14B.

## 35.10 Prova pràctica: 3 models, 5 preguntes

Per comparar models, fes aquesta prova:

```bash
# Descarrega 3 models
ollama pull gemma3:4b
ollama pull gemma3:12b
ollama pull qwen2.5:14b

# Crea un script de proves
cat > test-models.sh << 'EOF'
#!/bin/bash
MODELS=("gemma3:4b" "gemma3:12b" "qwen2.5:14b")
QUESTIONS=(
  "Quan he de sembrar carbasses a la comarca d'Osona?"
  "Explica'm què és el mildiu del tomàquet i com tractar-lo de forma ecològica"
  "Fes-me'n un resum de 5 línies sobre el calendari lunar aplicat a l'hort"
  "Quines associacions de cultius són bones per a un hort petit de 100 m²?"
  "Com puc fer compost amb restes de cuina si visc en un pis?"
)
for m in "${MODELS[@]}"; do
  echo "===== $m ====="
  for q in "${QUESTIONS[@]}"; do
    echo "Q: $q"
    ollama run "$m" "$q" 2>/dev/null | head -10
    echo "---"
  done
done
EOF

chmod +x test-models.sh
./test-models.sh > resultats.txt
```

Llegeix els resultats i tria el model que t'agradi més. No hi ha una resposta única — depèn de les teves prioritats.

## 35.11 Quan actualitzar el model

Els models s'actualitzen sovint. Bones pràctiques:

- **Cada 3-6 mesos**, mira si n'hi ha un de millor.
- **Descarrega'l i prova'l** sense eliminar l'antic.
- **Compara** amb les teves 5-10 preguntes representatives.
- **Substitueix** quan el nou sigui clarament millor.

## 35.12 Resum

Hem après a triar un model segons el hardware, la mida, la velocitat, i el català. Hem vist els millors models del 2026, com quantitzar, com avaluar la qualitat, i hem donat una recomanació concreta per al teu cas. Al proper capítol veurem com funcionen els embeddings i les bases vectorials, la base tècnica del RAG que muntarem al Cap 37.

## 35.13 Exercicis pràctics

1. Comprova el teu hardware (xip, RAM).
2. Descarrega 2-3 models recomanats per al teu hardware.
3. Fes la prova pràctica de 5 preguntes i avalua les respostes.
4. Crea un Modelfile "assistent-hort" amb el millor model.
5. Documenta al README quin model has triat i per què.
6. Compara el rendiment amb i sense quantització Q4.
7. Comparteix les teves impressions al README del projecte.

Paraules clau: **model, paràmetres, B, mil milions, tokens, tokens per segon, velocitat, qualitat, català, gemma3, qwen2.5, llama3, mistral, mixtral, deepseek, phi3, quantització, Q4_K_M, Q8, 16 bits, 4 bits, 8 bits, GGUF, GPTQ, AWQ, MLX, Apple Silicon, Metal, CUDA, VRAM, RAM, context, num_ctx, temperature, sampling, top-k, top-p, determinisme, seed, MODelfile, alias, registre, registry, benchmark, MMLU, IFEval, MT-Bench, AReQA, pàgina d'avaluació, leaderboard, Open LLM Leaderboard, LMSYS, Hugging Face, comparació, decisió, prova pràctica, benchmark personalitzat, actualització, manteniment**.
