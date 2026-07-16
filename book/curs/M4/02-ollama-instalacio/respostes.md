# Respostes - Capitol 2: Instal·lar Ollama

> Mira les respostes DESPRES d'haver fet el qüestionari.

## Pregunta 1: Que es Ollama?

**Resposta correcta**: Un runtime local per executar LLMs a la teva maquina.

**Explicacio**: Ollama es un programa que descarrega, emmagatzema i executa LLMs localment. No es un servei de núvol (es local), no es un editor de text, ni un sistema operatiu. Es el "contenidor" dels models: tu poses el model, ell l'executa i t'ofereix una API per accedir-hi.

---

## Pregunta 2: Comanda d'instal·lacio?

**Resposta correcta**: `curl -fsSL https://ollama.com/install.sh | sh`.

**Explicacio**: L'script oficial d'Ollama detecta la teva arquitectura (amd64, arm64), descarrega el binari adequat, crea l'usuari de sistema `ollama`, configura el servei systemd i l'activa. Es la forma soportada oficialment. No esta als repositoris d'apt de Debian, per tant no es pot fer `apt install ollama`.

---

## Pregunta 3: Port per defecte?

**Resposta correcta**: 11434.

**Explicacio**: Ollama escolta al port TCP 11434 per defecte. Es pot canviar amb la variable d'entorn `OLLAMA_HOST=IP:PORT`. Es un port "exotic" (no com el 80 o 443) per evitar conflictes amb altres serveis comuns.

---

## Pregunta 4: Descarregar un model?

**Resposta correcta**: `ollama pull MODEL`.

**Explicacio**: La comanda `pull` esta inspirada en `docker pull` i `git pull`. Descarrega el model des del registre oficial d'Ollama (registry.ollama.ai) i el deixa al directori configurat. Si ja el tens, comprova si hi ha actualitzacions.

---

## Pregunta 5: Model per a RPi 4 amb 4 GB?

**Resposta correcta**: llama3.2:1b.

**Explicacio**: Els models de 70B o mes necessiten maquines amb 40+ GB de RAM. Mistral 7B quantitzat en Q4 ja ocupa uns 4-5 GB, massa just per a una RPi 4 amb 4 GB (nomes en queda per al SO). El model `llama3.2:1b` nomes ocupa ~1 GB, i el 3b uns 2.5 GB. Son els ideals per a la nostra maquina.

---

## Pregunta 6: Endpoint per a pregunta simple?

**Resposta correcta**: /api/generate.

**Explicacio**: Ollama te dos endpoints principals: `/api/generate` per a una sola pregunta amb un prompt, i `/api/chat` per a converses amb multiples missatges amb rols (system, user, assistant). Per a resums, classificacio, o extraccio, `/api/generate` es mes senzill i rapid.

---

## Pregunta 7: Llistar models?

**Resposta correcta**: `ollama list`.

**Explicacio**: La comanda `list` mostra tots els models descarregats localment amb la seva mida i data de modificacio. Es l'equivalent a `docker images`. Nomes mostra els models, no els que estan actualment carregats a memoria (per aixo existeix `ollama ps`).

---

## Pregunta 8: OLLAMA_HOST=0.0.0.0:11434?

**Resposta correcta**: El servei escolta a totes les interficies de xarxa.

**Explicacio**: Per defecte, Ollama nomes escolta a `127.0.0.1` (localhost), nomes accesible des de la propia maquina. Si poses `0.0.0.0`, escolta a TOTES les interficies (Ethernet, WiFi, Tailscale), fent-lo accessible des d'altres dispositius de la xarxa. Util si vols que la RPi sigui el "servidor d'IA" per a tota la familia.

---

## Pregunta 9 (oberta): Per que moure els models a un altre disc?

**Resposta model**:

El directori per defecte d'Ollama es a la microSD (`/usr/share/ollama/.ollama/models/`). Aixo es un problema per varies raons:

**1. Vida util de la microSD**: una targeta microSD te uns 10.000 cicles d'escriptura per cel·la. Descarregar un model de 2 GB implica escriure 2 GB seguits, i cada vegada que fas servir el model, Ollama llegeix parts. Si fas servir el LLM sovint, la SD s'erosiona mes rapid.

**2. Espai limitat**: una SD de 32 GB es queda curta rapidament. Un sol model de 7B ja ocupa 4-8 GB, i si en tens 3-4, no et queda espai per a res mes.

**3. Velocitat**: les SD son mes lentes que un SSD o disc USB 3.0. Carregar un model de 2 GB pot trigar 30 segons des de SD i 5 segons des de SSD.

**4. Confiabilitat**: si la SD es mor (i acaben morint), perds els models i has de tornar a descarregar. Si els tens en un disc extern amb backup, els recuperes.

**Recomanacio**: munta un disc SSD USB 3.0 a `/mnt/dades` i configura `OLLAMA_MODELS=/mnt/dades/ollama-models`.

---

## Pregunta 10 (oberta): Flux complet per fer una pregunta

**Resposta model**:

**Pas 1: Descarregar el model**

```bash
ollama pull llama3.2:1b
```

Aixo descarrega el model de 1B parametres de Meta (~1.3 GB). Si ja el tens, veuras "pulling manifest" i comprobara que esta al dia.

**Pas 2: Provar interactivament**

```bash
ollama run llama3.2:1b
```

Aixo obre un xat per terminal. Pots escriure preguntes i el model respon. Per sortir: `/bye`.

Exemple:

```
>>> Hola, qui ets?
Soc un model de llenguatge creat per Meta...
>>> /bye
```

**Pas 3: Cridar l'API REST**

Amb el servei Ollama engegat (ja ho esta automaticament), pots fer:

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2:1b",
  "prompt": "Quants continents hi ha?",
  "stream": false
}'
```

El JSON que enviem conte:
- `model`: el nom exacte del model a utilitzar.
- `prompt`: la pregunta o instruccio.
- `stream`: false vol dir que volem la resposta sencera de cop, no paraula a paraula.

La resposta sera un JSON amb camps com `response` (el text generat), `total_duration` (temps total), `eval_count` (tokens generats), etc. Es pot parsejar amb `jq` o qualsevol llenguatge.

**Automatitzacio**: des d'un script Python, es pot fer `requests.post('http://localhost:11434/api/generate', json={...})` i obtenir la resposta.

---

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: rellegir el resum, sobretot la seccio de l'API REST.
- **3-4 encerts**: repassa les variables d'entorn i els endpoints abans de seguir.
- **0-2 encerts**: fes l'exercici practic sencer. La millor manera d'aprendre Ollama es instal·lar-lo i provar-lo.

## Que fer si has encertat totes

- Passa al **Capitol 3** (Models locals: com triar el millor per a tu).
- O fes el **repte**: descarrega 3 models diferents i compara la velocitat de resposta amb un script cronometrat.
