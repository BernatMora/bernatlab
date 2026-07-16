# Respostes - Capitol 3: Triar el model adequat

> Mira les respostes DESPRES d'haver fet el qüestionari.

## Pregunta 1: Que son les "B"?

**Resposta correcta**: Bilions (milers de milions).

**Explicacio**: En angles, "B" es l'abreviacio de "Billion", que vol dir 1.000.000.000 (mil milions). Un model de "7B" te set mil milions de parametres. Aixo es mes que els 8 GB d'una RPi 4, per això cal quantitzar.

---

## Pregunta 2: RAM d'un 7B en Q4?

**Resposta correcta**: 4-5 GB.

**Explicacio**: 7B parametres en float32 = 7.000.000.000 * 4 bytes = 28 GB. En Q4, son 7.000.000.000 * 0.5 bytes = 3.5 GB. Afegint overhead del runtime d'Ollama, acabem als 4-5 GB reals. Per tant, NO cap en una RPi 4 de 4 GB.

---

## Pregunta 3: Que vol dir "Q4"?

**Resposta correcta**: 4 bits per parametre (comprimit).

**Explicacio**: "Q4" es una quantitzacio de 4 bits. Cada parametre, en lloc d'ocupar 32 bits, nomes en gasta 4. Es perd una mica de precisio pero el model continua funcionant be per a la majoria de tasques. Es l'estandard de facto per a models locals.

---

## Pregunta 4: Model per defecte a RPi 4?

**Resposta correcta**: llama3.2:3b.

**Explicacio**: De les opcions donades, nomes `llama3.2:3b` es realista per a una RPi 4 amb 4 GB. El 70B necessita 40 GB. El mistral 7B quantitzat ocupa ~5 GB. Mixtral 8x7B es encara mes gran. El 3B ofereix bona qualitat amb 2.5 GB de RAM, deixant 1.5 GB per al sistema.

---

## Pregunta 5: Tokens per segon ideals?

**Resposta correcta**: 10-20 t/s.

**Explicacio**: A partir de 20 t/s la experiencia de lectura es molt bona. Entre 10-20 t/s es acceptable. Per sota de 5 t/s es fa pesat. El model de 1B en RPi pot arribar a 30+ t/s, mentre que el de 3B va a 10-15 t/s.

---

## Pregunta 6: Que fa `num_predict`?

**Resposta correcta**: Limita el maxim de tokens que pot generar en una resposta.

**Explicacio**: `num_predict` (abans `max_tokens`) es un parametre que talla la resposta del model quan ha generat N tokens. Util quan vols respostes curtes i vols estalviar temps. Per defecte, el model pot generar fins a 2048 tokens.

---

## Pregunta 7: Que fa `OLLAMA_KEEP_ALIVE=-1`?

**Resposta correcta**: Mantindra el model carregat a memoria indefinidament.

**Explicacio**: Amb `-1`, el model es queda carregat a RAM per sempre. Es la opcio mes rapida (no cal recarregar) pero gasta RAM constantment. Per defecte, Ollama descarrega el model als 5 min. Amb `0`, descarrega inmediatament.

---

## Pregunta 8: Benchmark per a codi?

**Resposta correcta**: HumanEval.

**Explicacio**: HumanEval es el benchmark estandard per mesurar la capacitat d'un model de generar codi Python correcte. Consta de 164 problemes de programacio. Un model de 7B bo pot obtenir el 30-50%. MMLU es per a coneixements generals, GSM8K per a matematiques, HellaSwag per a sentit comu.

---

## Pregunta 9 (oberta): Quin model per a logs?

**Resposta model**:

Per aquesta tasca, jo triaria **`llama3.2:3b`** per les seguents raons:

**Arguments a favor**:
- **Volum de logs**: els logs normals son 100-1000 linies, perfectament dins la finestra de context del 3B. No cal un model gran.
- **Idioma**: tant `llama3.2:1b` com `3b` entenen catala i angles. Gemma2 tambe. `Mistral` nomes angles.
- **Velocitat vs qualitat**: el 1B es rapid pero tendeix a generar respostes massa curtes o massa basiques. El 3B troba un bon equilibri.
- **Recomanacio practica**: el 3B es el model que millor "raona" dins del hardware limitat de la RPi 4.

**Limitacions que veuràs**:
- **Catala no perfecte**: els models petits no sempre mantenen el catala correcte. Si la linia de log es molt tecnica en angles, pot traduir-la malament.
- **Codi generat limitat**: si li demanes "com resoldre aquesta anomalia", el 3B donara un suggeriment basic pero no un script sofisticat. Cal complementar amb plantilles pre-fetes.
- **Verificacio sempre necessaria**: el 3B pot inventar-se el significat d'un log ("error de permisos" quan realment es un timeout). Cal revisar.
- **No es deterministic**: la mateixa pregunta pot donar respostes diferents. Cal validar-les.

**Alternativa**: si volem velocitat maxima i logs simples, el 1B es acceptable. Si volem mes profunditat pero tenim paciencia, podem provar el `phi3:mini` (3.8B) que es bo raonant.

---

## Pregunta 10 (oberta): Diferencia 7B Q4 vs 7B float32

**Resposta model**:

**Mida al disc**:
- **Float32**: 7B parametres * 4 bytes = 28 GB al disc. Un model nomes ocupa mes que molts portatils antics.
- **Q4**: 7B parametres * 0.5 bytes = 3.5 GB. Cap a qualsevol lloc.

**RAM necessaria**:
- **Float32**: necessita 28 GB de RAM per carregar el model. Impossibles a la majoria de cases.
- **Q4**: nomes 4-5 GB. Perfecte per a un PC amb 16 GB o un Mac M1.

**Diferencies de qualitat**:
- **Float32**: maxima fidelitat. Es el que s'ha usat per entrenar.
- **Q4**: perdua de ~3-5% en benchmarks tipics. Imperceptible per a la majoria d'usos (xat, resum, codi basic). Es nota mes en tasques de raonament numeric.

**Casos d'us**:
- **Float32**: centres de recerca, servidors dedicats a IA, training posterior del model. No es per a nosaltres.
- **Q4**: 99% dels casos, incloent servidors personals, chatbots, RAG local, scripting assistit.

**Conclusio**: Q4 es l'estandard de facto avui. A no ser que tinguis una maquina de 50.000 € o estiguis fent recerca, no té sentit la versio sense comprimir. I encara existeixen quantitzacions mes agresives (Q2, Q3) per a hardware encara mes limitat, amb perdues mes evidents de qualitat.

---

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: rellegir el resum, sobretot la taula de models.
- **3-4 encerts**: repassa els conceptes de quantitzacio i num_predict.
- **0-2 encerts**: fes l'exercici practic, veuras les diferencies en primera persona.

## Que fer si has encertat totes

- Passa al **Capitol 4** (Prompt engineering).
- O fes el **repte**: descarrega un model de codi com `codellama:7b` i compara amb `llama3.2:3b` generant scripts.
