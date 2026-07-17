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

## Pregunta 7: Hardware minim per LLM petit?

**Resposta correcta**: Uns 4 GB de RAM i CPU ARM/x86.

**Explicacio**: Un model de 1B-3B parametres quantitzat en Q4 ocupa entre 1 i 2 GB de RAM. Per tant, una Raspberry Pi 4 amb 4 GB de RAM el pot fer correr. Es lent, pero funciona. Un model de 7B ja en necessita uns 4-5 GB, i a partir d'aqui la cosa es complica amb CPU sola.

---

## Pregunta 8 (oberta): "Saber" vs "semblar que sap"

**Resposta model**:

Un LLM no te cap base de coneixements estructurada a dins. El que te son milers de milions de parametres numerics que representen patrons estadistics sobre com les paraules es combinen en els textos que ha vist. Per tant, quan li preguntes "quants habitants te Vic?", el que fa es construir la resposta que estadisticament es mes semblant a les respostes que ha vist sobre aquesta mena de preguntes.

La diferencia entre "saber" i "semblar que sap" es subtil pero fonamental. Un huma que "sap" alguna cosa pot raonar-hi, pot dir quan no esta segur, pot consultar altres fonts. Un LLM nomes pot generar text que soni a veritat. Si el patro l'enganya, generara bestieses amb un to perfectament normal.

Per aixo, sempre cal tractar les respostes d'un LLM com la resposta d'un becari molt llest pero molt confiat: pot encertar-la o pot inventar-se-la. Tu sempre has de verificar abans de fer-ne cas.

---

## Pregunta 9 (oberta): Avantatges i riscos d'un LLM local per a logs

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

## Pregunta 10 (oberta): Per que importa "prediu la paraula seguent"

**Resposta model**:

Sabent que un LLM nomes "prediu la paraula seguent" podem anticipar dos tipus de fallades molt comuns en entorns de produccio.

**Cas 1 - Dades inventades**: li pots preguntar "quin es el port per defecte de la teva API?" i el model et respondra "8080" o "3000" perque son els ports mes comuns que ha vist. Pero el teu servei real corre al 8765. El model no "mentix" per malicia: simplement no te manera de saber que el teu cas es diferent. Per tant, validacio humana SEMPRE.

**Cas 2 - Comandes obsoletes**: si li preguntes "com instal·lo Docker al Ubuntu?", pot retornar-te una comanda que era correcta fa 5 anys pero que avui falla. Aixo passa perque a l'entrenament va veure molts exemples antics, i estadisticament aquesta es la "comanda mes semblant" a la pregunta.

La lliço es clara: la responsabilitat sempre es de l'operador. El LLM es una eina d'assistència que pot accelerar la feina, pero mai ha de ser l'ultima paraula. Al BernatLab, on un error pot deixar el servidor caigut o exposar una porta a Internet, el principi es: "el LLM proposa, l'humà disposa".

---

## Pregunta 11 (oberta): Analogia per a no tecnics

**Resposta model**:

Una bona analogia es la del "becari molt llest que ha llegit tot Internet pero que no ha sortit mai de la biblioteca". Aquest becari sap moltes coses perque les ha vistes escrites, pero no ha verificat si son certes, no enten el context actual de la teva empresa, i s'inventa respostes quan no troba la informacio exacta. A mes, si li dones molt de text per llegir, oblida el principi i nomes recorda el final.

Una analogia que NO funciona be es la del "amic savi que sempre t'aconsella be". Un amic pot dir "no ho se" o "deixa'm que ho miri". Un LLM no sap dir "no ho se" de manera natural: sempre genera la resposta mes probable, encara que sigui incorrecta.

Una tercera analogia que pot funcionar: el "cuiner de tapes que ha menjat a mil restaurants". Sap com sonen els plats, com es combinen els ingredients, i pot inventar receptes noves. Pero si li demanes una recepta concreta d'un restaurant que no ha visitat, te la inventara amb molta gracia i poca fidelitat.

El punt clau es transmetre que **el LLM es un generador de text plausible, no una font de veritat**. Tothom ho enten quan li poses l'exemple del becari: mai no confiaries en un becari sense revisar la seva feina. Doncs amb el LLM, igual.

---

## Pregunta 12 (oberta): Finestra de context i 50.000 logs

**Resposta model**:

El problema es greu. Un log tipic ocupa uns 100-200 caracters. Aixo son uns 30-60 tokens per linia. Per tant, 50.000 logs ocupen uns 1.5M-3M tokens. Cap model actual (ni tan sols els de 200k) pot processar-ho d'una sola vegada. Si ho intentessim, el model nomes veuria els ultims 5-10% dels logs i ignoraria la resta.

Tinc quatre strategies possibles per al BernatLab:

1. **Finestra lliscant**: passo nomes els ultims 1.000-5.000 logs amb la pregunta "troba anomalies respecte el patro habitual". Es rapid pero perdo la visio de setmanes.

2. **Resum previ amb un script**: un script Python agrupa els logs per hora, calcula metrics (errors per hora, pics de CPU, etc.) i genera un resum de 2.000 tokens que SI cap al context. Llavors passo aquest resum al LLM.

3. **Resum previ amb un altre model**: un model rapid (3B) resumeix blocs de 10.000 logs en parrafs curts, i despres un model mes gran (7B-13B) raona sobre els resums. Pipeline de dos nivells.

4. **Chunks + cerca semantica**: vectoritzo els logs (RAG) i nomes paso al LLM els mes rellevants per la pregunta. Es la solucio mes elegant pero mes complexe.

Al BernatLab jo faria una combinacio: un script que calcula metrics diaries (errrors, memoria, latencia) i un RAG per quan necessiti buscar patrons específics. D'aquesta manera el LLM nomes treballa amb informacio ja processada, que es on es fort.

---

## Pregunta 13 (oberta): Quan NO fer servir un LLM

**Resposta model**:

Hi ha tres casos clars al BernatLab on un LLM es una mala idea:

**1. Comptar alertes**: "Quantes alertes de temperatura >30 graus he tingut aquest mes?" Això es una consulta SQL directa: `SELECT COUNT(*) FROM alerts WHERE metric = 'temp' AND value > 30 AND timestamp > NOW() - INTERVAL '30 days'`. Un LLM tardaria 10 segons a "generar" la resposta i probablement s'equivocaria. Una consulta SQL tarda 0.001 segons i es exacta.

**2. Detectar logins sospitosos**: volem saber "aquest login a les 3 de la matinada desde una IP rara es valid?". Això requereix consistencia: la mateixa entrada ha de donar sempre la mateixa sortida. Un LLM es probabilistic i podria classificar el mateix login de manera diferent dues vegades seguides. Una regla `fail2ban` o un script amb llista negra d'IPs es deterministic.

**3. Generar el backup**: xifrar la base de dades i copiar-la a un bucket S3. Això ha de ser 100% fiable, reproduible i verificable. Si el LLM falla un caracter al xifrar, el backup queda corrupte. Un script `borgbackup` o `restic` amb la comanda correcta es infinitament mes fiable.

El denominador comu: **determinisme, velocitat i fiabilitat**. Els LLMs son eines creatives i de raonament, no eines de backoffice. Per a tasques critiques de produccio, sempre una solucio tradicional.

---

## Pregunta 14 (oberta): Data de tall i seguretat

**Resposta model**:

La data de tall te implicacions molt serioses per a la seguretat. Si el teu model es de principis de 2024 i al març de 2025 es publica un CVE critic a OpenSSL, el teu model no en sabra res. Si li preguntes "es segur el meu servidor amb OpenSSL 3.0.2?", et dira "si, es una versio estable" perque es el que ha vist mes vegades. No sap que hi ha una vulnerabilitat nova.

Això es un risc real perque pot generar falses sensacions de seguretat. L'operador huma pot pensar "el LLM m'ha dit que tot esta be, no m'amoïno" i no actualitzar. Es el pitjor dels mons: ni tan sols sabent que el model te limits, confiem en la seva sortida.

La solucio al BernatLab es **mai preguntar-li al LLM sobre CVEs o vulnerabilitats actuals**. En canvi, cal:

- Mantenir un sistema automatitzat de comprovacio de versions (Dependabot, Trivy, npm audit).
- Usar el LLM nomes per a tasques creatives: redactar scripts, explicar conceptes, generar documentacio.
- Si cal usar el LLM per qüestions de seguretat, combinar-lo amb RAG sobre documentacio actualitzada del proveidor (per exemple, els release notes de Debian).

La regla es: **per a temes de seguretat, fonts primaries sempre**. El LLM es un assistent, no un auditor.

---

## Pregunta 15 (oberta): Local 3B vs núvol 70B

**Resposta model**:

Després de pensar-ho, **la meva eleccio es LLM local de 3B per al BernatLab**. Argumento a continuacio.

**Arguments a favor del local 3B**:
- **Privadesa**: el BernatLab gestiona dades personals (logs d'acces, sensors de l'hort familiar). Cap d'aquestes dades hauria de sortir del meu servidor. El núvol obligaria a anonimitzar tot abans d'enviar, i sempre hi ha el risc d'oblidar algun detall.
- **Cost**: un cop tens el model descarregat, el cost marginal per consulta es zero. El núvol cobra per token, i amb l'us que en faria (revisar logs, generar scripts, fer preguntes) la factura pujaria ràpid.
- **Independencia**: no depenc de que un proveidor extern estigui operatiu, ni de que canviï les condicions del servei, ni de que una fallada global de cloud m'afecti.
- **Aprenentatge**: entendre com fer anar un LLM local emenya habilitats transferibles.

**Arguments a favor del núvol 70B**:
- **Qualitat de resposta**: un 70B es notablement millor que un 3B en raonament complex, seguiment d'instruccions llargues i evitar al·lucinacions.
- **Velocitat**: el núvol te GPUs potents. El local a la RPi 4 pot trigar 30 segons a generar un paràgraf. El núvol respon en 2 segons.
- **Finestra de context mes ampla**: alguns models al núvol arriben a 200k-1M tokens. El local 3B sol tenir 4k-8k.

**La decisio**: per al BernatLab, on la privadesa i el cost son prioritaris i les tasques son relativament simples (revisar logs curts, generar scripts petits, respondre preguntes sobre documentacio), el 3B local es suficient. Si en un futur necessito raonament complex per a tasques puntuals, puc fer una consulta esporadica al núvol amb dades ben anonimitzades. Pero el gruix de l'us ha de ser local.

Aixo es el que fa el BernatLab: privacitat per defecte, núvol nomes quan es estrictament necessari.

---

## Que fer si has fallat moltes preguntes

- **10-12 encerts**: rellegir el resum amb atencio, sobretot les seccions de "com funciona" i "limitacions".
- **7-9 encerts**: repassa els conceptes de "finestra de context" i "al·lucinacions" abans de seguir.
- **0-6 encerts**: llegir el resum dues vegades, fer l'exercici practic del Pas 2-3, i tornar-ho a provar.

## Que fer si has encertat totes

- Passa al **Capitol 2** (Ollama, instal·lacio).
- O fes l'**exercici practic** per consolidar el que saps.
- O investiga: quants parametres te el model "llama3.2:1b" que provarem al cap següent?
