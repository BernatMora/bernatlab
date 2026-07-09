# Capítol 34 — Ollama al Mac: instal·lació i primera conversa

> *"Instal·lar Ollama al Mac és com obrir una ampolla de vi: cinc minuts, i ja tens alguna cosa valuosa a la mà."*

## 34.1 Què és Ollama

**Ollama** (ollama.com) és una aplicació gratuïta i de codi obert que permet executar models d'IA localment amb una sola comanda. Està disponible per a macOS, Linux i Windows. La va crear Jeffrey Morgan i l'equip d'Ollama, i s'ha convertit en l'estàndard de facto per a IA local.

Ollama fa quatre coses:

1. **Descarrega models** d'un registre central (similar a Docker Hub, però per a models).
2. **Executa models** al teu hardware, optimitzant per a Apple Silicon (Metal), NVIDIA (CUDA) o CPU.
3. **Serveix una API local** (a `http://localhost:11434`) compatible amb la d'OpenAI.
4. **Gestiona la memòria** alliberant RAM quan no uses el model.

## 34.2 Instal·lació al Mac

### Mètode 1: descarregar de la web (recomanat)

1. Vés a https://ollama.com/download/mac.
2. Descarrega el `.dmg`.
3. Obre'l i arrossega Ollama a la carpeta Aplicacions.
4. Executa Ollama. Apareixerà una icona de camell a la barra de menú.

### Mètode 2: Homebrew (si el tens)

```bash
brew install ollama
```

### Mètode 3: comanda directa

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Aquest mètode funciona a macOS, Linux i WSL. A Windows, descarrega l'instal·lador de la web.

## 34.3 Verificar la instal·lació

Obre un terminal i comprova:

```bash
ollama --version
```

Hauries de veure alguna cosa com `ollama version 0.5.7` (o superior). Si no, afegeix Ollama al PATH:

```bash
# Si usaves Homebrew:
export PATH="/usr/local/bin:$PATH"

# Si vas instal·lar manualment, crea un enllaç simbòlic:
sudo ln -s /Applications/Ollama.app/Contents/Resources/ollama /usr/local/bin/ollama
```

## 34.4 Descarregar el primer model

El primer pas és descarregar un model. Ollama ofereix molts. Per començar, recomano **gemma3:4b** (Google, 4 mil milions de paràmetres, ~3 GB):

```bash
ollama pull gemma3:4b
```

Això descarrega el model. Pot trigar entre 2 i 10 minuts segons la teva connexió.

Quan acabi, verifica:

```bash
ollama list
```

Hauries de veure:

```
NAME           ID          SIZE      MODIFIED
gemma3:4b      ...         3.1 GB    2 minutes ago
```

## 34.5 Primera conversa

Ara pots parlar amb el model. Prova:

```bash
ollama run gemma3:4b "Hola, qui ets?"
```

Hauries de rebre una resposta en qüestió de segons. Si tot funciona, ja tens IA local al Mac.

Per sortir, escriu `/bye` o prem `Ctrl+D`.

## 34.6 Comandes bàsiques d'Ollama

| Comanda | Què fa |
|---|---|
| `ollama pull <model>` | Descarrega un model |
| `ollama run <model>` | Inicia una conversa |
| `ollama list` | Llista els models descarregats |
| `ollama rm <model>` | Esborra un model |
| `ollama ps` | Mostra els models que s'estan executant |
| `ollama show <model>` | Mostra els detalls d'un model |
| `ollama cp <src> <dst>` | Copia un model amb un altre nom |
| `ollama stop <model>` | Atura un model en execució |

## 34.7 Modes d'ús

### Mode conversa (REPL)

Quan executes `ollama run <model>`, entres en mode conversa. Pots escriure qualsevol cosa i el model et respon. Per mantenir el context (que el model recordi el que has dit), continua en la mateixa sessió.

Per començar una conversa nova, obre una altra finestra de terminal.

### Mode script (un sol prompt)

```bash
ollama run gemma3:4b "Explica'm què és un embedding en 3 frases"
```

Això envia el prompt, rep la resposta, i surt.

### Mode API

Ollama escolta a `http://localhost:11434` quan està en marxa. Pots enviar peticions HTTP:

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "gemma3:4b",
  "prompt": "Què és un cogombre?",
  "stream": false
}'
```

Això retorna JSON amb la resposta. Veurem com integrar-ho al Cap 39.

## 34.8 Com fer bones preguntes

La clau per treure profit d'un model local és **fer bones preguntes**. Algunes pautes:

1. **Sigues específic**. "Explica el compostatge" és vague. "Explica el compostatge en climes humits amb palla i restes de cuina" és millor.

2. **Dona context**. "Sóc a Osona, tinc un hort de 200 m² amb tomàquets i carbasses. Quina varietat de carbassa em recomanes?" és millor que "Quina carbassa plantar?".

3. **Demana format concret**. "Fes-me'n una llista de 5 punts" o "Explica-m'ho en 3 paràgrafs".

4. **Demana verificació**. "Si no saps la resposta, digue-m'ho. No inventis informació." Els models tendeixen a inventar-se coses (les anomenem "al·lucinacions").

5. **Posa exemples**. "Vull un correu com aquest: 'Benvolgut veí, ...'". El model imitarà l'estil.

## 34.9 Configuració avançada: system prompt

Quan executes un model, Ollama permet passar un **system prompt** (instruccions de sistema, missatges inicials que condicionen tot el comportament del model) que canvia el comportament. Per exemple:

```bash
ollama run gemma3:4b "
Ets un expert en horticultura ecològica a la comarca d'Osona.
Respon sempre en català.
Sigues pràctic i directe, sense floritures.
Si no saps una resposta concreta, recomana consultar les fitxes locals.
"
```

El model respondrà seguint aquestes instruccions fins que tanquis la sessió.

## 34.10 Persistència de la configuració: Modelfiles

Si vols que el system prompt estigui sempre disponible, pots crear un **Modelfile**:

```bash
# Crea un fitxer anomenat Modelfile-hort
cat > Modelfile-hort << 'EOF'
FROM gemma3:4b
SYSTEM """
Ets l'assistent Hort Osona. Coneixes les 76 fitxes de cultius del projecte
BernatLab. Respon sempre en català. Sigues pràctic. Si no saps una resposta,
digues "Consulta la fitxa corresponent a Hort Osona" i no inventis.
"""
PARAMETER temperature 0.3
PARAMETER num_ctx 4096
EOF

# Crea un model personalitzat
ollama create hort-osona -f Modelfile-hort

# Usa'l
ollama run hort-osona "Quan he de sembrar tomàquets?"
```

Això és molt potent: pots tenir múltiples "personalitats" del mateix model base, cadascuna optimitzada per una tasca.

## 34.11 El primer model: què esperar

Amb gemma3:4b (4B paràmetres, ~3 GB):

- Velocitat: 20-50 tokens/segon en un Mac M1 amb 16 GB.
- Català: acceptable, no perfecte.
- Raonament: limitat, però útil per a resums i consultes senzilles.
- Memòria: 3-4 GB de RAM ocupats.

Per a tasques més complexes (raonament llarg, codi, multilingüe avançat), necessitaràs models més grans. Això ho veurem al Cap 35.

## 34.12 Primers problemes i solucions

**Problema 1: el model no descarrega**.

Comprova la connexió: `curl -I https://ollama.com`. Si funciona, mira l'espai lliure: `df -h`. Necessites almenys 5 GB.

**Problema 2: el model respon en anglès**.

El model és multilingüe, però tendeix a l'anglès. Força el català amb un system prompt explícit: "Respon SEMPRE en català, encara que et preguntin en un altre idioma."

**Problema 3: el Mac s'escalfa molt**.

Els models consumeixen molta CPU/GPU. És normal. Si et molesta, redueix el context (paràmetre `num_ctx`) o usa un model més petit.

**Problema 4: la resposta és molt lenta**.

Si tens molts programes oberts, tanca'ls. Si el model és massa gran per al teu Mac, descarrega'n un de més petit (gemma3:2b o phi3:mini).

**Problema 5: "address already in use"**.

El port 11434 està ocupat. Probablement tens una altra instància d'Ollama corrent. Tanca-la i reobre.

## 34.13 Compartir el Mac amb la Raspberry

Si vols que la Raspberry accedeixi a Ollama al Mac, cal fer dues coses:

1. **Permetre connexions externes**. Per defecte, Ollama només escolta a `localhost`. Per canviar-ho:

```bash
# Atura Ollama
pkill ollama

# Inicia'l escoltant a totes les interfícies
OLLAMA_HOST=0.0.0.0:11434 ollama serve &
```

2. **Assegurar que la Raspberry pot arribar al Mac**. Si tens Tailscale configurat, simplement:

```bash
# Des de la Raspberry
curl http://<mac-tailscale-ip>:11434/api/tags
```

Si funciona, veuràs la llista de models.

Per a ús continu, pots crear un servei launchd (gestor de serveis automàtic de macOS) que mantingui Ollama en marxa i escoltant a la xarxa Tailscale.

## 34.14 Resum

Hem après a instal·lar Ollama al Mac, descarregar el primer model (gemma3:4b), mantenir una conversa, configurar system prompts i Modelfiles, i compartir Ollama amb la Raspberry via Tailscale. Al proper capítol veurem com triar el millor model per a les nostres necessitats: mida, velocitat, qualitat, i especialment el català.

## 34.15 Exercicis pràctics

1. Instal·la Ollama al Mac seguint els passos.
2. Descarrega `gemma3:4b` i `gemma3:12b` (si tens RAM).
3. Fes-li 5 preguntes relacionades amb l'hort i avalua la qualitat de les respostes.
4. Crea un Modelfile anomenat `hort-osona` amb un system prompt útil.
5. Configura Ollama per escoltar a `0.0.0.0:11434` i comprova que la Raspberry pot accedir-hi.
6. Fes una llista de 5 tasques que voldries que l'assistent pogués fer.
7. Documenta al README el model que uses, el Modelfile, i les primeres impressions.

Paraules clau: **Ollama, install, descarregar, model, gemma3, phi3, llama, mistral, terminal, REPL, API, system prompt, Modelfile, temperature, num_ctx, paràmetres, català, Tailscale, 0.0.0.0, 11434, curl, JSON, streaming, Mac, Apple Silicon, M1, M2, M3, M4, Metal, MLX, launchd, dimonis, daemon, xarxa local, pkill, kill, process, foreground, background, model base, custom model, etiqueta, tag, registre, registry, Docker Hub, anàleg, semàntica, token, tokenització, vocabulari, context window, max tokens, longitud màxima, prompt, response, generation, sampling, top-k, top-p, temperature, seed, determinisme, randomness, creatividad, precissió, al·lucinació, inventar, verificar, fact-checking, font fiable, citació, referència**.
