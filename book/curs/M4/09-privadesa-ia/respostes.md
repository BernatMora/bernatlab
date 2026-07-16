# Respostes - Capitol 9: Privadesa de la IA

## Pregunta 1: Que passa amb les dades al nuvol?

**Resposta correcta**: S'envien a l'empresa que te el model.

**Explicacio**: Quan uses ChatGPT, Claude, Gemini, etc., el texte de la teva pregunta, el contexte i la resposta viatgen als servidors d'aquesta empresa. Segons els termes del servei, poden guardar-les, analitzar-les o usar-les per entrenar futurs models. Es la diferencia fonamental amb la IA local.

---

## Pregunta 2: Millor avantatge de la IA local?

**Resposta correcta**: Les dades no surten del teu PC.

**Explicacio**: Amb Ollama, tot el proces (embedding, cerca, generacio) passa al teu maquinari. Ningun mes te acces a les teves dades. Es la diferencia entre tenir un assistent al núvol i tenir-lo a casa teva.

---

## Pregunta 3: NO es avantatge de la IA local?

**Resposta correcta**: Te els millors models del mon.

**Explicacio**: Els millors models (GPT-4, Claude Opus, Gemini Ultra) son al nuvol. La IA local te models mes petits pero suficients per a molts casos. La potencia punta encara es al nuvol.

---

## Pregunta 4: Limitacio de la IA local?

**Resposta correcta**: Menys potent (els millors models son al nuvol).

**Explicacio**: Els models mes grans i entrenats amb mes dades son al nuvol perque requereixen infraestructura cara. La RPi o un PC normal no poden correr GPT-4 ni tan sols quantitat. Pero per a molts casos, els models locals son mes que suficients.

---

## Pregunta 5: Que vol dir GDPR?

**Resposta correcta**: General Data Protection Regulation (normativa UE de privadesa).

**Explicacio**: El GDPR es la llei europea de proteccio de dades, en vigor des del 2018. Regula com les empreses poden recollir, emmagatzemar i processar dades personals. Important si vols usar serveis al nuvol amb dades de ciutadans europeus.

---

## Pregunta 6: Bona practica de privadesa local?

**Resposta correcta**: Xifrar els embeddings si s'emmagatzemen.

**Explicacio**: Encara que els embeddings son vectors numerics, poden contenir informacio sensible reconstruible. Xifrar-los o guardar-los en una particio xifrada es una bona practica. Tambe es important netejar els historials de converses periodicament.

---

## Pregunta 7 (oberta): 3 arguments per la IA local

**Resposta model**:

La IA local es la opcio mes privada per 3 motius clars:

1. **Les dades no viatgen**: amb Ollama, tot el proces passa al teu hardware. Les preguntes, els documents i les respostes mai surten del teu PC. No hi ha cap servidor extern involucrat, ni tan sols per a la fase d'entrenament del model (que ja esta fet).

2. **Control absolut**: tu decideixes que es guarda, que es borra, i qui te acces. No depens de la politica de privadesa d'una empresa que pot canviar demà. Si vols esborrar tot, ho pots fer amb un `rm -rf`. No hi ha "data retention policy" de 30 dies.

3. **Sense data breach extern**: el risc mes gran al nuvol no es l'empresa, sino els hackers. Un data breach pot exposar milions de converses. En local, nomes et pots hackejar a tu mateix (la teva RPi), i tens control sobre la seguretat.

Aixo si, la IA local te inconvenients: velocitat i potencia. Pero per a molts casos d'us personal, la privadesa compensa.

---

## Pregunta 8 (oberta): Cas on NO nuvol pero si local

**Resposta model**:

Un cas clar: un **advocat o metge amb un homelab** que vol ajudar-se amb la IA per analitzar documents.

- **Per que NO nuvol**: els documents son confidencials per llei. Enviar histologies cliniques o expedients al nuvol vulnera el secret professional i el GDPR. Si l'empresa del nuvol te un data breach, la responsabilitat es de l'advocat/metge.

- **Per que SI local**: amb Ollama a una RPi, pot indexar tots els seus documents i fer consultes sense que res surti del seu despatx. Es compliant amb GDPR per disseny.

- **Cas real**: un metge de capçalera vol consultar rapidament els seus 30 anys d'historial cliniques per trobar patrons. Amb RAG local, pot fer-ho. Al nuvol, no pot (o no hauria de poder).

L'avantatge: complir la llei I tenir l'eina. Al nuvol, son incompatibles per a dades sensibles.

---

## Pregunta 9 (oberta): Trade-off local vs nuvol

**Resposta model**:

El trade-off real es entre **privadesa** i **potencia**. No es absolut - depen molt del cas.

**L'eix del trade-off**:
- **Local**: maxima privadesa, cost zero, funciona offline, personalitzable, mes lent, menys potent.
- **Nuvol**: poca privadesa, cal pagar, cal internet, menys control, mes rapid, mes potent.

**No es absolut** perque:
- Hi ha models al nuvol que son bastant privats (self-hosted en servidors europeus).
- Hi ha models locals que son bastant potents (Mixtral, Llama 3 70B en un Mac potent).
- Es pot combinar: local per defecte, nuvol per a tasques puntuals que necessitin potencia.

**La meva recomanacio**: regla del 80/20.
- 80% de les tasques: local (consultes, embeddings, resums simples).
- 20% de les tasques: nuvol (generacio de texte complex, multimodal, raonament llarg).

Aixi tens privadesa per defecte i pots usar el nuvol nomes quan realment cal.

---

## Pregunta 10 (oberta): Correus confidencials

**Resposta model**:

Per a correus confidencials d'un client, la **regla d'or** es: **mai el nuvol, sempre local**.

**Pipeline mixt correcte**:

1. **Indexacio local (Ollama + ChromaDB)**: indexar tots els correus al teu PC/RPi. Cap embedding surt de casa.

2. **Consulta local (RAG)**: quan vulguis buscar, la consulta es local. El LLM local llegeix el contexte i respon.

3. **Anonimitzacio previa**: si vols resumir tendencies (no casos individuals), pots anonimitzar les dades i llavors enviar-les al nuvol. Pero per a casos especifics d'un client, mai.

4. **Logs locals**: guarda un registre de totes les consultes. Si hi ha una fuga, saps on ha estat.

**Exemple de decisio**:
- "Resumeix els ultims correus del client X" -> LOCAL nomes.
- "Quin es l'estil general dels correus professionals" -> LOCAL + anonimitzeu + nuvol opcional.
- "Genera una resposta formal al client X" -> LOCAL nomes.

**Bones practiques GDPR**:
- No usar APIs de tercers per a dades identificables.
- Xifrar el disc on es guarden els correus.
- Limitar l'acces fisic a la RPi.
- Netejar logs periodicament.

**Conclusio**: per a correus confidencials, la IA local es l'unica opcio etica. El nuvol es per a informacio que ja es publica o es pot anonimitzar.

---

## Què fer si has fallat moltes

- **5-8 encerts**: Reflexiona sobre quines dades personales has enviat al nuvol fins ara. Considera migrar a local.
- **3-4 encerts**: Rellegeix el resum. La clau es entendre que al nuvol **tot** va a l'empresa.
- **0-2 encerts**: Comença llegint els termes del servei d'algun LLM al nuvol que usaves. Despres torna aqui.
