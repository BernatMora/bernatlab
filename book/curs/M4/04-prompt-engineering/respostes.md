# Respostes - Capitol 4: Prompt engineering

> Mira les respostes DESPRES d'haver fet el qüestionari.

## Pregunta 1: Que es prompt engineering?

**Resposta correcta**: L'art d'escriure prompts que extreuen el millor del model.

**Explicacio**: Un prompt es la pregunta o instruccio. La diferencia entre un bon i un mal prompt pot ser la diferencia entre una resposta inutil i una meravellosa. Es una habilitat que es pot aprendre amb practica.

---

## Pregunta 2: Per que falla "Explica els servidors"?

**Resposta correcta**: El model no sap quin nivell de detall, quina audiencia ni quin format vols.

**Explicacio**: Un prompt generic dona respostes generiques. Cal especificar: per a qui es, quants detalls, quin to, quina longitud. Sense això, el model "endivina" i sovint falla.

---

## Pregunta 3: Que es role prompting?

**Resposta correcta**: Assignar un rol o personalitat al LLM.

**Explicacio**: Quan diem "Ets un expert en Linux amb 20 anys d'experiencia", el model adapta el seu to, el seu vocabulari i el seu nivell de detall. Es una manera molt potent d'orientar la resposta.

---

## Pregunta 4: Few-shot prompting

**Resposta correcta**: Mostrar exemples al model dins del prompt.

**Explicacio**: Few-shot = "pocs exemples". Zero-shot = cap exemple. Few-shot es mes precisi perque el model "veu" el patro que ha de seguir, en lloc d'haver-lo d'endivinar.

---

## Pregunta 5: Quin es un bon prompt?

**Resposta correcta**: "Explica quines son les 3 diferencies principals entre Docker i Podman en menys de 100 paraules, en catala."

**Explicacio**: Especifica: quants punts (3), limit de longitud (100 paraules), tema concret (Docker vs Podman), llengua (catala). Es un prompt accionable. Els altres son massa vagues o incomplets.

---

## Pregunta 6: System prompt

**Resposta correcta**: Un missatge inicial que defineix el comportament general del model per a tota la conversa.

**Explicacio**: Es diferent del "user prompt" (cada pregunta). El system prompt estableix regles, to, limitacions. Es invisible per a l'usuari pero marca la diferencia.

---

## Pregunta 7: Temperature

**Resposta correcta**: Temperature baixa = deterministe; alta = creatiu.

**Explicacio**: Temperature controla l'aleatorietat. 0 = sempre la paraula mes probable. 1 = mes variacio. Per a resums i tasques deterministes, baixa. Per a creativitat, alta.

---

## Pregunta 8 (oberta): Quatre regles d'or

**Resposta model**:

**Regla 1: Sigues especific**. El mal prompt "explica Docker" pot donar qualsevol cosa. El bon prompt es "explica quines son les 3 principals diferencies entre Docker i una maquina virtual, en 100 paraules, per a un junior". La diferencia es que el segon dona un marc clar.

**Regla 2: Dona context**. No es el mateix preguntar "com millorar la seguretat" que dir "soc l'admin d'una RPi amb SSH obert a Internet, dona'm 5 consells prioritzats". El context permet respostes personalitzades.

**Regla 3: Dona exemples si cal**. Si vols un format concret, mostra exemples. Few-shot es mes efectiu que explicacions llargues. Per exemple, abans de demanar "classifica aquesta alerta", mostra 3 exemples de classificacio.

**Regla 4: Especifica el format de sortida**. Vols una llista? Una taula? Un JSON? Un text pla? Si no ho dius, el model tria. Si li dones un format concret, el resultat es mes facil de processar automaticament.

Aplicar aquestes quatre regles transforma un model mediocre en un assistent util. La diferencia es brutal: el mateix model de 3B, amb un bon prompt, pot superar un de 7B amb mal prompt.

---

## Pregunta 9 (oberta): System prompt i model petit

**Resposta model**:

Un system prompt ben fet pot canviar completament la qualitat de les respostes d'un model petit per varies raons:

**Concentre l'atencio del model**: el system prompt es la primera cosa que el model "llegeix" i estableix el context. Sense system prompt, el model ha d'endivinar el rol a partir de cada pregunta individual. Amb system prompt, ja te el marc preparat.

**Defineix regles clares**: el model sap quines limitacions te (no inventar, respondre en catala, etc.). Sense això, tendeix a ser generic.

**Exemple al BernatLab**: per a un assistent que analitza logs, un system prompt podria ser:

```
Ets un expert en administracio de sistemes Linux especialitzat en el BernatLab.
Coneixes Docker, MQTT, InfluxDB, Grafana i la Raspberry Pi 4.
Quan rebis un log, fes el seguent:
1. Identifica el servei i la severitat.
2. Dona una explicacio breu en 1-2 frases.
3. Si es un error, suggereix una possible solucio.
Respon sempre en catala, amb concisio. Mai no inventis informacio que no tinguis.
```

Amb aquest prompt, un 3B pot donar respostes tanbones com un 7B sense prompt. Es com tenir un "expert" preconfigurat. Per tant, al BernatLab, abans de baixar un model mes gran, optimitzo el system prompt del que ja tinc.

---

## Pregunta 10 (oberta): System prompt per a fitxes tecniques

**Resposta model**:

Un system prompt complet per generar fitxes de cultiu:

```
Ets un expert en horticultura amb 20 anys d'experiencia, especialitzat en 
horticultura ecologica de clima mediterrani continental (Osona, Catalunya).

La teva tasca es generar fitxes tecniques de cultius en catala, amb el seguent 
format EXACTE:

# [Nom del cultiu]
- **Familia**: [familia botanica]
- **Epoca de sembra**: [mesos]
- **Epoca de collita**: [mesos]
- **Necessitats d'aigua**: [baixa/mitjana/alta]
- **Tipus de sol**: [descripcio]
- **Associacions favorables**: [llista]
- **Plagues comunes**: [llista]
- **Notes**: [2-3 linies de consells practics]

Regles estrictes:
- Escriu nomes informacio que es aplicaria al clima d'Osona (900m d'altitud, hiverns freds).
- Si no tens informacio segura sobre un cultiu, digues "Informacio no disponible".
- No inventis dades de productivitat o rendiment.
- Limita cada apartat a 1-2 frases.
- Manten un to practic, adreçat a un hortolà amateur amb experiencia basica.
```

Aquest prompt te limitacions importants: el model pot inventar varietats que no existeixen, o dates de sembra incorrectes per a la zona. Per mitigar-ho, cal:

1. **Validacio humana SEMPRE**: cap fitxa es publica sense revisar.
2. **RAG sobre fonts locals**: afegir al context les fitxes existents d'Hort Osona perque el model es basi en informacio verificada.
3. **Few-shot amb exemples**: mostrar 2-3 fitxes reals perque el model aprengui el format desitjat.

---

## Pregunta 11 (oberta): Cost del prompt

**Resposta model**:

La longitud del prompt te un impacte directe en el cost i el temps:

**Cost economic** (si usem un LLM comercial): cada token d'entrada costa diners. Un prompt de 1000 tokens que es crida 1000 vegades/dia = 1M tokens/dia. A 0.01$/1k tokens (preu d'entrada tipic), son 10$/dia = 300$/mes. No es trivial.

**Cost temporal** (local o cloud): el model triga mes a processar prompts llargs. Un prompt de 100 tokens pot trigar 1 segon a processar; un de 2000 tokens pot trigar 5 segons. Si el cas d'us es interactiu (usuari esperant), aixo importa.

**Finestra de context consumida**: cada prompt ocupa part de la finestra de context. Si el prompt es de 2000 tokens, queda menys espai per a la resposta i per a la historia de la conversa. En models petits (4-8k de context), aixo es un limit real.

**Estrategies al BernatLab**:
1. **Prompts reusables**: en lloc de construir el prompt cada vegada, usa plantilles fixes. Exemple: una funcio `resumir_log(log)` que sempre te el mateix system prompt.
2. **Cache de respostes**: si la mateixa pregunta es fa moltes vegades, guarda la resposta. Exemple: "Que es un sensor DS18B20?" nomes cal respondre-la un cop.
3. **Resums del contexte**: en lloc de passar tot l'historial, pasa un resum automatic.
4. **Prompts especifics per tasca**: en lloc d'un prompt generic, fes prompts curts i optimitzats per a cada tasca concreta.

La regla: **el prompt mes curt que encara doni la qualitat desitjada**. No malgastis tokens en floritures.

---

## Pregunta 12 (oberta): Chain of thought

**Resposta model**:

El "chain of thought" (CoT) funciona perque el model es mes bo raonant pas a pas que saltant directament a la resposta. Es una troballa empirica que ha estat replicada en molts estudis.

**Per que funciona**: el transformer (l'arquitectura del LLM) processa millor la informacio quan l'ha de generar explicitament. Si li dones un problema i li demanes la resposta, ha de fer tots els calculs "dins del cap" abans d'escriure. Si li demanes que els faci explicitament, pot iterar sobre cada pas.

**Exemple al BernatLab**: si demanes al model "aquest log indica un problema?", pot donar una resposta generica. Pero si li demanes "pensa pas a pas: 1) que diu el log, 2) quines son les possibles causes, 3) quina es la mes probable, 4) que pot fer l'operador?", donarà una resposta molt mes estructurada i util.

**Limitacions**: CoT augmenta el temps de resposta (es mes text a generar) i el cost. Cal usar-lo nomes per a tasques que realment requereixen raonament, no per a resums simples.

**Truc avançat**: "self-consistency" es demanar N cadenes de pensament i quedar-te amb la resposta mes comuna. Es mes car pero molt mes fiable per a problemes delicats.

---

## Pregunta 13 (oberta): Zero-shot vs few-shot

**Resposta model**:

La diferencia es important en el context del BernatLab. Poso exemples reals:

**Zero-shot**: "Classifica aquesta alerta: 'CPU 95%'". El model pot respondre "es una alerta de CPU alta" (correcte pero poc util) o "pot ser un problema" (generic). No sabem si enten el format de sortida esperat.

**Few-shot**: 
```
Exemples:
- 'CPU 30%' -> INFO
- 'CPU 70%' -> WARNING
- 'CPU 90%' -> CRITICAL
- 'Disk 60%' -> INFO
- 'Disk 85%' -> WARNING

Classifica: 'CPU 95%'
```
Ara el model enten perfectament que volem una sola paraula (INFO/WARNING/CRITICAL) i enten els llindars.

**Quan pocs exemples ajuden**:
- Tasques de classificacio (tipus, severitat, categoria).
- Tasques d'extraccio (dates, noms, valors).
- Generacio de text amb format molt especific (JSON, taules, etc.).

**Quan pocs exemples saturen**:
- Si el context es limitat (model de 4k, pocs exemples = menys espai per a la consulta real).
- Si els exemples son massa llargs (millor 3 curts que 2 llargs).
- Si la tasca es intuïtiva (traduir, resumir).

**Regla al BernatLab**: per a qualsevol tasca que es fara servir en pipeline automatic, uso few-shot. Per a tasques creatives o exploratories, zero-shot.

---

## Pregunta 14 (oberta): Temperature a la practica

**Resposta model**:

Temperature=0 i temperature=1 son eines diferents per a contextos diferents.

**Temperature=0 (deterministe)**:
- Mateixa entrada -> mateixa sortida sempre.
- Ideal per a tasques automatitzades: classificacio, extraccio, validacio.
- Exemple al BernatLab: un script que resumeixi 1000 logs. Volem que tots els logs semblants tinguin el mateix resum (o semblant). Amb temperature=0, si el log es "ERROR [mqtt] connection refused", el resum sera consistent.

**Temperature=1 (creatiu)**:
- Cada execucio pot donar resultats diferents.
- Ideal per a creativitat: generar noms, idees, explicacions variades.
- Exemple al BernatLab: generar noms per a 10 fitxes de cultiu noves. Volem varietat, no 10 cops el mateix nom.

**Riscos**:
- Temperature alta pot generar respostes incoherents o sense sentit.
- Temperature baixa pot ser massa rigida i perdre subtilesa.

**Regla**: 0.0-0.3 per a tasques deterministes, 0.7-1.0 per a creatives. Mai passar de 1.2.

**Al BernatLab**: un script que interactua amb un LLM ha de tenir la temperature com a parametre configurable. Si el resultat no es bo, pots ajustar sense tocar el prompt.

---

## Pregunta 15 (oberta): Prompt de 30 segons

**Resposta model**:

Si nomes tens 30 segons, les 3 coses essentials son:

**1. Rol o persona clara**. "Ets un expert en X". Sense rol, el model es generic i dona respostes planes. El rol l'obliga a adaptar el to, el vocabulari i el nivell de detall. Exemple: "Ets un administrador de sistemes Linux amb 10 anys d'experiencia en homelabs".

**2. Format de sortida**. Especificar com vols la resposta. "Respon en 3 linies", "llista de 5 punts", "JSON amb aquesta estructura". Sense format, el model tria i sovint tries malament.

**3. Context o restriccions clau**. "Aplica a una Raspberry Pi 4 amb 4 GB de RAM", "respon en catala", "no inventis dades". Les restriccions acoten la resposta.

**Que NO cal posar-hi** (en 30 segons):
- Detalls excessius o redundants.
- Exemples si la tasca es intuïtiva.
- Explicacions llargues del per que.

**Exemple practic** per al BernatLab:

```
System: "Ets un expert en horticultura ecologica d'Osona (900m d'altitud). 
Respon sempre en catala, amb concisio (max 100 paraules)."

User: "Explica com plantar tomàquets a l'hort d'Osona al mes d'abril."
```

Aquest prompt, en 30 segons, es molt mes potent que "Explica com plantar tomàquets". La diferència es brutal: el primer dona informacio especifica, el segon dona informacio generica que pot aplicar a qualsevol lloc.

**Practica**: la propera vegada que usis un LLM, aplica aquesta regla i compara els resultats amb els teus prompts habituals.

---

## Que fer si has fallat moltes preguntes

- **10-12 encerts**: fes l'exercici practic pas a pas, veuras la diferencia.
- **7-9 encerts**: repassa el resum i torna a provar les preguntes obertes.
- **0-6 encerts**: comença pel exercici Pas 2 (comparar mal i bon prompt), es molt revelador.

## Que fer si has encertat totes

- Passa al **Capitol 5** (RAG introduccio).
- O investiga "function calling": capacitat del LLM de cridar funcions externes.
- O mira eines com `guidance` o `outlines` que permeten controlar l'estructura de la sortida.
