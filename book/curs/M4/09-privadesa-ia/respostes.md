# Respostes - Capitol 9: Privadesa de la IA

> Mira les respostes DESPRES d'haver fet el qüestionari.

## Pregunta 1: Que s'envia a un LLM al nuvol?

**Resposta correcta**: Preguntes, contexte adjunt, respostes, metadades.

**Explicacio**: Tot. La pregunta, els fitxers adjunts, les respostes, i metadades com l'hora, la IP, el navegador. Es un detall que molta gent no considera.

---

## Pregunta 2: Que es IA local?

**Resposta correcta**: Una IA que s'executa al teu propi ordinador sense enviar dades a tercers.

**Explicacio**: Es la diferencia entre tenir l'assistent a casa (local) o tenir-lo a un edifici d'una empresa (nuvol). Al BernatLab, Ollama es la eina per fer IA local.

---

## Pregunta 3: NO es un risc de la IA al nuvol

**Resposta correcta**: El model es massa petit.

**Explicacio**: La mida del model no te res a veure amb la privadesa. El risc es on s'executa i que fan amb les dades.

---

## Pregunta 4: Avantatge mes important al BernatLab

**Resposta correcta**: Privadesa total.

**Explicacio**: Al BernatLab processem dades personals i de l'hort familiar. Que no surtin del servidor es prioritari per sobre de qualsevol altre avantatge.

---

## Pregunta 5: Risc mes gran de la IA al nuvol

**Resposta correcta**: Les teves dades poden ser usades per entrenar futurs models.

**Explicacio**: Aixo es un risc real i sovint ignorat. Moltes empreses reserven el dret d'usar les converses per millorar els seus models. Les teves dades es converteixen en part del "coneixement" del model per sempre.

---

## Pregunta 6: Llei europea relevant

**Resposta correcta**: GDPR.

**Explicacio**: La GDPR (General Data Protection Regulation) es la llei que regula el tractament de dades personals a Europa. Afecta com qualsevol empresa pot usar les teves dades. Es la referencia legal per a la privadesa.

---

## Pregunta 7: NO es limitacio de la IA local

**Resposta correcta**: Es mes cara.

**Explicacio**: La IA local no te cost per consulta, nomes el cost d'electricitat i hardware. A llarg termini, es MES barata que les subscriptcions mensuals al nuvol.

---

## Pregunta 8 (oberta): Per que la privadesa es important

**Resposta model**:

La privadesa es un tema tant important perque **sovint enviem mes dades de les que pensem**. Aixo es per varies raons:

**1. Les dades sensibles son mes comunes del que creiem**. No es nomes informacio medica o financera. Son:
- Correus sobre familia, amics, projectes personals.
- Documents de feina amb informacio confidencial.
- Histories de navegacio (que revelen molt de la teva vida).
- Logs del sistema amb IPs, noms d'usuari, patrons d'us.
- Captures de pantalla, fotos, videos.

**2. Tenim tendencia a "exagerar" amb el contexte**. Quan demanem ajuda a un LLM, sovint copiem-enganxem molt text. "Mira aquesta linia de log", "llegeix aquest correu", "explica'm aquest contracte". Sense adonar-nos, estem enviant una mica de la nostra vida a un servidor extern.

**3. Les dades son persistents**. Un cop envies una informacio, queda emmagatzemada. Pot ser borrada per l'empresa, pero no tens garanties reals. Si hi ha un data breach (cosa que passa cada any), les teves dades queden exposades.

**4. Les dades son reutilitzables**. El que avui es "una consulta sobre un log", demà pot ser un fragment d'entrenament per a un model. Les teves paraules poden acabar formant part de les respostes d'altres usuaris.

**Exemple concret**: imagina que escrius un correu sobre un problema amb el teu vei i el passes al LLM per "reformular-lo millor". Aquest correu conte informacio personal, opinions, possibles conflictes legals. Si queda emmagatzemat, pot ser problematic en el futur.

La regla d'or: **mai enviïs a un LLM al nuvol res que no publicaries en un cartell al carrer**. Si tens dubtes, millor local.

---

## Pregunta 9 (oberta): Riscos dun correu legal a ChatGPT

**Resposta model**:

Enviar un correu sobre una situacio legal delicada (com un conflicte amb un vei) a ChatGPT te **quatre riscos principals**:

**Risc 1 - Emmagatzematge perpetu**. OpenAI pot guardar el teu correu als seus servidors. Encara que el seuavis de privadesa digui que nomes per 30 dies, no tens garanties reals. Pot ser un backup, una copia de seguretat, un registre intern que mai s'esborra.

**Risc 2 - Us per entrenar**. Segons la politica d'OpenAI, les converses poden ser usades per entrenar futurs models (llevat que opt-out). El teu correu pot acabar formant part d'un dataset d'entrenament. No se sap exactament com s'usara, pero el text queda "fos" dins del model.

**Risc 3 - Data breach**. OpenAI, com qualsevol empresa, pot patir un atac informatic. Si un atacant roba la base de dades de converses, el teu correu sobre el conflicte amb el vei queda exposat. Aixo pot agreujar la situacio legal (l'altra part pot obtenir informacio que no volies compartir).

**Risc 4 - Cessio a tercers**. Empreses com OpenAI poden cedir dades a autoritats governamentals (amb ordre judicial), a socis comercials, o a empreses que els comprin. A mes, els seus servidors poden estar a Estats Units, fora de la jurisdiccio GDPR.

**L'alternativa correcta**: usar un LLM local (Ollama). El correu queda al teu servidor, no s'envia a ningun tercer, i tens control absolut. Aixo es exactament el cas d'us per al que serveix Ollama al BernatLab: situacions delicades on la privadesa es critica.

**Alternativa hibrida**: si necessites un model mes potent del que tens local, pots anonimitzar el correu (treure noms, dates, ubicacions) abans d'enviar-lo al nuvol. Pero sempre sera menys segur que el local.

---

## Pregunta 10 (oberta): Privadesa i control

**Resposta model**:

La relacio entre privadesa i control es fonamental. **Privadesa es el resultat de tenir control**, i el control ve de la proximitat fisica i logica.

**Amb IA local**:
- Tens el control absolut. Les dades son al teu disc, al teu servidor, a la teva xarxa.
- Pots fer el que vulguis: esborrar, modificar, exportar, xifrar.
- Ningun mes te acces sense el teu permis explicit.
- Si vols deixar d'usar el model, simplement l'apagues.

**Amb IA al nuvol**:
- El proveidor te les dades. Tu nomes tens un servei (l'API).
- Les dades estan subjectes a les politiques del proveidor.
- Si canvien les condicions, tu no tens opcio (o tens l'opcio de marxar, pero perds les dades).
- Si el proveidor te problemes economics, les teves dades poden estar en joc.

**Analogia**: llogar una casa vs tenir-la en propietat.
- Llogar: el propietari pot canviar les condicions, vendre la casa, o no renovar el contracte. Tu no tens control.
- Propietat: tu decideixes que fer, quan marxar, com reformar. Tens control total.

**Que pasa si el proveidor canvia les condicions?** Cas real: el 2023, StackOverflow va canviar la seva politica i va bloquejar l'access a dades historiques per a entrenar. El 2024, Reddit va fer el mateix. Son exemples de com una empresa pot canviar les regles del joc unilateralment.

Al BernatLab, amb Ollama, **tu ets l'unic que pot canviar les regles**. Si vols afegir un model, l'afegixes. Si vols canviar la configuracio, la canvies. Si vols tancar el servidor, el tanques. Es la diferencia entre ser client i ser propietari.

---

## Pregunta 11 (oberta): ChatGPT Plus vs Ollama local

**Resposta model**:

Fem el calcul economic per al BernatLab:

**Opcio A - ChatGPT Plus (20$/mes)**:
- Cost mensual: 20$.
- Cost anual: 240$.
- Cost a 5 anys: 1.200$.
- **Limitacio**: les dades van al nuvol. Riscos de privadesa. Limits d'us (potser cal un plan mes car per us intensiu).

**Opcio B - Ollama local**:
- Hardware: una RPi 4 (4 GB) costa uns 60-80€. Un Mac mini M2 usat costa uns 500€.
- Cost mensual d'electricitat: ~5€ (RPi) o ~10€ (Mac).
- Cost anual: 60-120€ d'electricitat.
- **A 1-2 anys**: el cost ja es inferior.
- **Avantatges adicionals**: privadesa total, sense limits d'us, personalitzable, funciona offline.

**Payback period**:
- Amb RPi nova (60€): payback en 3-6 mesos.
- Amb Mac usat (500€): payback en 18-24 mesos.

**Arguments economics a favor de local**:
- A llarg termini (2+ anys), el local es mes barat.
- A curt termini, depen de si ja tens hardware.
- Si tens una RPi, el cost es quasi zero.
- Si necessites comprar un PC potent (2000€), triga mes a amortitzar-se.

**Arguments economics a favor del nuvol**:
- Cost inicial zero.
- Sense manteniment de hardware.
- Sense configuracio (tot funciona desde el primer dia).
- Si nomes l'us esporadicament, es mes economic.

**La meva recomanacio**: **Ollama local** al BernatLab, per varies raons:
1. Ja tenim una RPi al servidor. Cost marginal d'usar-la per IA: quasi zero.
2. La privadesa es un valor intangible pero important.
3. Tenim el control total.
4. A 1-2 anys, el cost es inferior.

Si nomes necessites IA ocasionalment (1-2 cops per setmana) i no t'importa la privadesa, ChatGPT Plus pot ser mes convenient. Pero per a un BernatLab que vol ser autosuficient i privat, local es la tria correcta.

**Tercera opcio**: model mes petit (3B) local per a tasques simples + consultes puntuals al nuvol anonimitzades per a tasques complexes. Aixo dona el millor dels dos mons.

---

## Pregunta 12 (oberta): Canvi de politiques

**Resposta model**:

Que una empresa canviï les seves politiques de privadesa es un **risc real i subestimat**. Passa mes sovint del que pensem.

**Exemples historics**:
- **Instagram (2012)**: va canviar els termes i es va apropiar del dret a vendre les fotos dels usuaris. Protestes massives. Van revertir parcialment.
- **WhatsApp (2021)**: va compartir dades amb Facebook per defecte. Canvi unilateral. Molts usuaris van marxar a Signal.
- **Reddit (2023)**: va bloquejar l'access a dades historiques per a entrenar models. Els desenvolupadors que depenien d'aquestes dades van quedar penjats.
- **Twitter/X (2022-2023)**: canvis massius de politiques d'API, privadesa, verificacio. Usuaris i desenvolupadors van perdre control.

**Que ensenya aixo**: les empreses canvien les seves politiques **quan els convieneix economicament**, no quan es moralment correcte. Avui una empresa et promet privadesa, pero d'aqui 2 anys pot vendre la teva activitat a un altre que te altres prioritats.

**L'avantatge de la IA local**: tu no depens de la bona voluntat de ningun. Si vols canviar la teva propia politica (per exemple, deixar d'enregistrar logs), nomes has de canviar la teva configuracio. Ningun altre te poder sobre les teves decisions.

**Aplicat al BernatLab**: si demà OpenAI decideix usar totes les converses per entrenar (fins i tot les dels usuaris que van dir que no), els teus correus i logs poden acabar formant part d'un model. No pots fer-hi res. En canvi, amb Ollama local, **tu decideixes el desti de les teves dades**.

**Conclusio**: en un mon on les empreses canvien les seves politiques sense previ avis, tenir control local es la unica garantia real de privadesa a llarg termini.

---

## Pregunta 13 (oberta): Bones practiques

**Resposta model**:

**Bones practiques generals (s'apliquen a local i nuvol)**:

1. **Minimitzar dades enviades**: nomes envia el text necessari. Si pots resumir abans d'enviar, millor.

2. **Anonimitzar sempre**: treu noms, emails, telèfons, IPs, ubicacions. Encara que sembli "innocu", millor curar-se en salut.

3. **Xifrar al disc**: tant si es local com al nuvol, les dades emmagatzemades han d'estar xifrades (LUKS al local, xifrat del proveidor al nuvol).

4. **Auditar periodicament**: cada 3-6 mesos, revisar quines dades s'han enviat, a on, i per que. Esborrar les que no calguin.

5. **Logs minims**: desactiva els logs que no necessitis. Menys logs = menys dades exposades en cas de breach.

6. **No usar el compte personal per a tot**: separa comptes (un per a feina, un per a personal, un per a experiments).

**Bones practiques per a IA local (BernatLab)**:

1. **Servidor en xarxa privada**: usa Tailscale per accedir des de fora. No exposar ports a Internet.

2. **Actualitzar el sistema periodicament**: les vulnerabilitats es descobreixen cada setmana. Un sistema no actualitzat es un sistema vulnerable.

3. **Backups xifrats**: fer còpies de seguretat pero xifrades. Guardar-les en un lloc segur (un altre disc, un altre edifici).

4. **Limitar qui te acces**: nomes tu (i potser familia de confianca). Si comparteixes amb altres, tenir comptes separats.

5. **Monitoritzar acces**: saber qui accedeix al servidor i quan. Logs basics (qui, quan, des d'on).

**Bones practiques per a IA al nuvol (si l'usas puntualment)**:

1. **Llegir els termes**: si, es avorrit, pero cal. Sabere que acceptes.

2. **Usar comptes dedicats**: no el teu compte personal, sino un compte separat per a experiments.

3. **Anonimitzar SEMPRE**: assumir que tot el que envies pot ser vist per humans i per futurs models.

4. **Opt-out d'entrenament**: si el proveidor ho permet, desactivar l'us de converses per entrenar.

5. **No compartir informacio personal o financera**: regla d'or.

**Al BernatLab, la meva politica es**: totes les dades importants passen per Ollama local. nomes uso el nuvol per a tasques generals sense informacio personal (resumir un article public, generar una idea creativa, etc.).

---

## Pregunta 14 (oberta): Avaluacio de privadesa dun model

**Resposta model**:

Abans de fer servir un LLM, cal fer-se **sis preguntes clau**:

**1. On s'executa?** Local o nuvol? Si es nuvol, en quins servidors? (Europa te GDPR mes estricte que EUA). Si es local, esta en un servidor que controlo?

**2. Quines dades recull per defecte?** Molts models recullen metadades (IP, hora, navegador, historial). Cal revisar la politica de privadesa.

**3. Pot usar les meves dades per entrenar?** Aquesta es la pregunta critica. Molts serveis gratuïts usen les converses per entrenar. Cal buscar l'opcio opt-out.

**4. Te una opcio "no entrenar amb les meves dades"?** Si la resposta es no, es un mal senyal. Si la resposta es si pero nomes a canvi de pagar, tambe.

**5. En cas de data breach, que pasa?** Tinc cap garantia? Ofereixen asseguurances? Qui em notifica?

**6. Esta allotjat en servidors europeus (GDPR)?** Si es EUA o altres jurisdiccions, les meves dades poden estar subjectes a altres lleis (Cloud Act, etc.).

**Exemple aplicat**:

| Pregunta | Ollama local | OpenAI ChatGPT | Anthropic Claude |
|---|---|---|---|
| On s'executa? | Local (casa meva) | Nuvol (EUA) | Nuvol (EUA) |
| Quines dades recull? | Cap (nomes el que jo guardi) | Metadades, converses | Metadades, converses |
| Pot entrenar amb les meves dades? | No (no te centre de dades central) | Si, per defecte | Si, per defecte |
| Opcio opt-out? | N/A (ja es privat) | Si (a la configuracio) | Si (a la configuracio) |
| Garantia en breach? | N/A (aixo es casa meva) | Limitada | Limitada |
| Servidors europeus? | N/A | No | No |

**Conclusio**: Ollama local es la unica opcio que dona resposta "perfecta" a totes les preguntes. Per aixo es la tria del BernatLab.

---

## Pregunta 15 (oberta): Per que la IA local al BernatLab

**Resposta model**:

Encara que la IA local te limitacions evidents (model mes petit, menys potent, menys rapid que els millors al nuvol), al BernatLab **es la millor opcio** per tres arguments solids:

**Argument 1 - Privadesa absoluta**. El BernatLab processa dades personals, lectures de sensors d'una llar, correus privats, possibles documents legals o financers. Aquestes dades **mai** haurien de sortir del servidor. La IA local garanteix que nomes jo (i les persones de la meva confianca) tenim acces. Cap data breach, cap politica canviada, cap empresa que vengui les meves dades. Es la diferencia entre un diari personal guardat sota el matalàs i un diari publicat a Internet.

**Argument 2 - Cost a llarg termini**. Una inversio inicial de 60-500€ en hardware, mes 50-100€ anuals d'electricitat, es amortitza en 1-2 anys respecte a una subscripcio de 20-30€/mes al nuvol. A mes, el hardware dura 5-10 anys, fent el cost per any molt baix. No hi ha sorpreses: no hi ha pujades de preu, no hi ha nous plans que calgui pagar, no hi ha limitacions d'us sobtades.

**Argument 3 - Control i independencia**. Jo decideixo quan actualitzar, quan canviar de model, quan tancar el sistema. No depenc de les decisions d'una empresa a 10.000 km. Si Meta decideix tancar el seu model, o Google puja els preus, o OpenAI canvia les condicions, a mi no m'afecta. El meu sistema segueix funcionant igual.

**Argument bonus 4 - Personalitzacio**. Puc afinar el model amb les meves dades (RAG, fine-tuning), puc crear una API a mida, puc integrar-lo amb els meus sistemes (Grafana, InfluxDB, scripts) de manera natural. Al nuvol, estic limitat a les APIs i condicions que em donen.

**Argument bonus 5 - Aprenentatge**. Muntar i mantenir un sistema d'IA local m'ensenya molt sobre com funciona la tecnologia. Aquest coneixement es transferible i em fa mes competent. Al nuvol, soc nomes un consumidor.

**Conclusio final**: al BernatLab, la IA local no es una questio de capacitat tecnica (podriem usar el nuvol perfectament), sino de valors. Volem privadesa, control i autonomia. Aixo son valors que el nuvol no pot oferir, per mes barat o potent que sigui.

---

## Que fer si has fallat moltes preguntes

- **10-12 encerts**: revisa la seccio de bones practiques del resum.
- **7-9 encerts**: fes l'exercici practic d'auditoria, veuras on tens possibles fuites.
- **0-6 encerts**: comença per l'inventari de dades (Pas 1) i la verificacio d'Ollama (Pas 3). Son les bases.

## Que fer si has encertat totes

- Passa al **Capitol 10** (aplicacio a Hort Osona).
- O investiga "differential privacy" en mes detall.
- O llegeix sobre la GDPR i com afecta el BernatLab.
