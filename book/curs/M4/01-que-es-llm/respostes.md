# Respostes - Capitol 1: Que es un LLM

> Mira les respostes DESPRES d'haver fet el qüestionari.

## Pregunta 1: Que significa LLM?

**Resposta correcta**: Large Language Model.

**Explicacio**: Son les inicials en angles. En catala seria "Model de Llenguatge Gran". No te res a veure amb "Local" o "Logical": la paraula clau es "Large" (gran), per la quantitat de parametres i dades amb que ha estat entrenat.

---

## Pregunta 2: Com "aprèn" un LLM?

**Resposta correcta**: Ajustant milers de milions de numeros a partir de molt text.

**Explicacio**: Un LLM es una xarxa neuronal amb milers de milions de parametres (nombres). Durant l'entrenament, el model llegeix textos i va ajustant aquests numeros per encertar la paraula seguent. No hi ha cap regla escrita a ma per un enginyer: tot es "descobert" estadisticament.

---

## Pregunta 3: Que es una "al·lucinacio"?

**Resposta correcta**: Una resposta inventada que sona a verdadera pero no te fonament.

**Explicacio**: Els LLMs no consulten cap base de dades. Generen paraules seguint patrons estadistics. Si el patro els porta cap a una resposta que no es correcta pero "sona" coherent, l'escriuen amb total conviccio. Es el perill mes gran d'usar LLMs: mai no els donis crèdit sense verificar.

---

## Pregunta 4: Mida de la finestra de context?

**Resposta correcta**: Entre 4.000 i 128.000 tokens.

**Explicacio**: Un "token" es aproximadament 0.75 paraules. Els models moderns poden processar entre 4k (models petits) i 128k-200k (models grans) tokens en una sola conversa. Si passes d'aquest limit, el model "oblida" el principi del text.

---

## Pregunta 5: Quin NO es un LLM?

**Resposta correcta**: InfluxDB.

**Explicacio**: Llama 3 (Meta), Mistral i GPT-4 (OpenAI) son tots LLMs. InfluxDB es una base de dades de series temporals que fem servir al BernatLab per guardar lectures de sensors. No te res a veure amb llenguatge natural.

---

## Pregunta 6: Diferencia entre IA i LLM?

**Resposta correcta**: LLM es un tipus especific d'IA entrenat per a llenguatge.

**Explicacio**: "IA" es el paraigua gran. Dins hi ha moltes coses: sistemes experts, jocs, visio per computador, xarxes neuronals, etc. Un LLM es nomes un tipus: el que treballa amb text i ha estat entrenat amb milers de milions de documents.

---

## Pregunta 7: Per a que NO utilitzaries un LLM?

**Resposta correcta**: Donar-te el preu exacte de l'IBEX35 d'ahir sense verificar.

**Explicacio**: Els preus de borsa canvien cada segon i depenen de dades externes en temps real. Un LLM nomes pot fer calculs estadistics sobre el que va aprendre durant l'entrenament. Pot inventar-se un preu amb tota la cara. En canvi, resumir, generar codi o traduir son tasques on el LLM es fort perque son patrons apresos del text.

---

## Pregunta 8: Hardware minim per LLM petit?

**Resposta correcta**: Uns 4 GB de RAM i CPU ARM/x86.

**Explicacio**: Un model de 1B-3B parametres quantitzat en Q4 ocupa entre 1 i 2 GB de RAM. Per tant, una Raspberry Pi 4 amb 4 GB de RAM el pot fer correr. Es lent, pero funciona. Un model de 7B ja en necessita uns 4-5 GB, i a partir d'aqui la cosa es complica amb CPU sola.

---

## Pregunta 9 (oberta): "Saber" vs "semblar que sap"

**Resposta model**:

Un LLM no te cap base de coneixements estructurada a dins. El que te son milers de milions de parametres numerics que representen patrons estadistics sobre com les paraules es combinen en els textos que ha vist. Per tant, quan li preguntes "quants habitants te Vic?", el que fa es construir la resposta que estadisticament es mes semblant a les respostes que ha vist sobre aquesta mena de preguntes.

La diferencia entre "saber" i "semblar que sap" es subtil pero fonamental. Un huma que "sap" alguna cosa pot raonar-hi, pot dir quan no esta segur, pot consultar altres fonts. Un LLM nomes pot generar text que soni a veritat. Si el patro l'enganya, generara bestieses amb un to perfectament normal.

Per aixo, sempre cal tractar les respostes d'un LLM com la resposta d'un becari molt llest pero molt confiat: pot encertar-la o pot inventar-se-la. Tu sempre has de verificar abans de fer-ne cas.

---

## Pregunta 10 (oberta): Avantatges i riscos d'un LLM local per a logs

**Resposta model**:

**3 avantatges**:
- **Privadesa total**: els logs poden contenir informacio sensible (IPs, noms d'usuari, intents d'intrusio). Si el model es local, les dades no surten mai del teu servidor. Si fos al núvol, estaries enviant aquesta informacio a tercers.
- **Cost zero per consulta**: un cop tens el model descarregat, cada consulta es "gratis" (nomes gasta electricitat). No hi ha factura per token com amb OpenAI.
- **Disponibilitat 24/7**: no depens de que un servei extern estigui operatiu. Si tens internet o no, el teu model local respon igual.

**3 riscos**:
- **Al·lucinacions en interpretacio**: el model pot interpretar malament una linia de log i donar-te un diagnostic erroni. Cal contrastar.
- **Limitacio de context**: si tens 10.000 linies de log, el model nomes en llegira les ultimes 4k-128k tokens. Es perd informacio important de l'inici.
- **Rendiment a la RPi 4**: la Raspberry es modesta. Analitzar logs grans pot trigar minutos, durant els quals el servidor va mes lent. Cal tenir-ho en compte i potser fer-ho en horari de baixa carrega.

**Dades dels logs que NO hauries de compartir amb un model extern**: contrasenyes (encara que estiguin hashed), adreces IP internes, noms d'usuari, informacio personal de clients, registres d'acces amb ubicacio. Per aixo, model local.

---

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: rellegir el resum amb atencio, sobretot les seccions de "com funciona" i "limitacions".
- **3-4 encerts**: repassa els conceptes de "finestra de context" i "al·lucinacions" abans de seguir.
- **0-2 encerts**: llegir el resum dues vegades, fer l'exercici practic del Pas 2-3, i tornar-ho a provar.

## Que fer si has encertat totes

- Passa al **Capitol 2** (Ollama, instal·lacio).
- O fes l'**exercici practic** per consolidar el que saps.
- O investiga: quants parametres te el model "llama3.2:1b" que provarem al cap següent?
