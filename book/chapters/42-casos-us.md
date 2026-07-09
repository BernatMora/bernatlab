# Capítol 42 — 10 consultes reals a l'assistent Hort Osona

> *"Ja tens l'eina. Ara veurem què li pots preguntar per començar a treure'n profit des del primer dia."*

## 42.1 Com usar aquest capítol

Aquest capítol és diferent dels altres. No és teoria ni pràctica, sinó **exemples reals** de consultes que pots fer a l'assistent Hort Osona un cop estigui muntat (Caps 33-41).

Cada consulta inclou:

- La **pregunta exacta** que pots escriure o dictar.
- El **context** (per què és útil).
- La **resposta esperada** (orientativa — dependrà del model que usis).
- Els **documents** que el RAG hauria de recuperar.

Al final tens un **prompt de benvinguda** que pots personalitzar.

## 42.2 Consulta 1: el calendari de sembra del mes

**Pregunta**: "Què he de sembrar aquest mes a l'hort d'Osona?"

**Context**: cada mes hi ha sembres òptimes. Vols saber-les sense haver de cercar per totes les fitxes.

**Resposta esperada** (orientativa):

> Aquest mes a la comarca d'Osona (zona mitjana, ~600 m d'altitud), pots sembrar:
>
> 1. **Enciam, escarola, ruca** (tolerant al fred).
> 2. **Pèsols, faves** (lleguminoses que volen temperatures fresques).
> 3. **Espinac, bleda** (hoja verda de cicle curt).
> 4. **Rave, pastanaga** (d'arrel, cicle ràpid).
> 5. **All, ceba tendra** (bulbs que es cullen a l'estiu).
>
> Consulta la fitxa de sembra per a cada cultiu al calendari d'Hort Osona. Recorda que aquesta llista és per a la zona d'Osona; altres zones poden variar 2-4 setmanes.

**Fonts esperades**: `calendari-sembra.md`, `pla-mensual.md`, fitxes individuals dels cultius esmentats.

## 42.3 Consulta 2: diagnòstic d'una plaga

**Pregunta**: "Les fulles del tomàquet tenen taques grogues amb un pols blanc a sota. Què és i què puc fer?"

**Context**: detectes un problema a la planta i vols consell ràpid.

**Resposta esperada**:

> Pel que descrius, és probable que sigui **míldiu** (*Phytophora infestans*), un fong que afecta tomàquets i patates, especialment amb humitat alta. Confirma mirant si:
>
> 1. Les taques s'escampen ràpidament.
> 2. A sota hi ha una mena de pelussa blanca.
> 3. Les tiges també es taquen.
>
> **Tractament ecològic**:
>
> - **Preventiu**: sulfat de coure (0.3-0.5%) o decocció de cua de cavall.
> - **Curatiu**: infusió d'all o purí d'ortiga.
> - **Eliminar** fulles afectades i cremar-les (no compostar).
> - **Ventilació**: esporgar les plantes per millorar la circulació d'aire.
> - **Evitar** reg per aspersió; millor reg per degoteig.
>
> Si la infecció és greu, és possible que hagis de sacrificar la planta. Consulta la fitxa de plagues per a més detalls.

**Fonts esperades**: `gestio-plagues.md`, `fitxa-tomaque.md`, `practiques-avancades.md`.

## 42.4 Consulta 3: associacions de cultius

**Pregunta**: "Vull fer un hort de 100 m² amb tomàquets, enciams i pastanagues. Quines associacions em recomanes?"

**Context**: estàs planificant un hort nou i vols optimitzar l'espai.

**Resposta esperada**:

> Per a un hort de 100 m² amb tomàquets, enciams i pastanagues, et recomano:
>
> **Associacions positives** (ajuden mútuament):
>
> 1. **Tomàquet + alfàbrega**: l'alfàbrega repel·la els mosquits i millora el gust del tomàquet.
> 2. **Enciam + pastanaga**: l'enciam ombreja el sòl, mantenint la humitat que la pastanaga necessita.
> 3. **Tomàquet + ceba/all**: la ceba repel·la plagues del tomàquet.
>
> **Rotació recomanada** (any següent):
>
> - On hi havia tomàquet, plantar lleguminoses (faves, pèsols) per fixar nitrogen.
> - On hi havia enciam, plantar brassicàcies (col, rave).
> - On hi havia pastanaga, plantar tomàquet.
>
> **Disposició suggested**:
>
> ```
> [Tomàquets 60m²]  [Enciams 20m²]  [Pastanagues 20m²]
> [Alfàbrega intercalada]  [Ceba intercalada]
> ```
>
> Consulta la guia d'associacions per a més combinacions.

**Fonts esperades**: `associacions-rotacions.md`, `croquis-hort.md`, fitxes individuals.

## 42.5 Consulta 4: com fer compost casolà

**Pregunta**: "Com puc fer compost a casa amb restes de cuina si visc en un pis?"

**Context**: vols compost però no tens jardí.

**Resposta esperada**:

> Per fer compost en un pis, la millor opció és un **composter domèstic** tipus **Bokashi** (fermentació anaeròbica en galleda tancada) o un **composter de balcó** amb cucs.
>
> **Opció 1: Bokashi** (recomanada per a pisos):
>
> 1. Compra una galleda Bokashi (~30 €).
> 2. Afegeix restes de cuina (fruita, verdura, pa, marro de cafè).
> 3. Escampa una capa de micelis Bokashi cada 2 cm de restes.
> 4. Premsa per expulsar l'aire.
> 5. Tanca la tapa. Cada 2-3 dies, obre la vàlvula per escórrer el líquid (dilueix 1:100 en aigua i usa com a adob líquid).
> 6. En 2-4 setmanes, el compost estarà fermentat.
>
> **Opció 2: Vermicompostador amb cucs** (per a balcons):
>
> 1. Compra un vermicompostador (~50 €).
> 2. Afegeix restes vegetals (no carn ni làctics).
> 3. Els cucs (Eisenia foetida) les transformen en humus.
> 4. Cada 3-6 mesos, recull l'humus del compartiment inferior.
>
> **Important**:
>
> - No posis carn, peix, làctics, ni olis.
> - Evita cítrics en grans quantitats (els cucs no els toleren).
> - Mantén humit però no enxarcat.
>
> Consulta la fitxa de compost per a més detalls.

**Fonts esperades**: `compost.md`, `practiques-avancades.md`.

## 42.6 Consulta 5: poda de fruiters

**Pregunta**: "Quan i com he de podar els meus presseguers de 5 anys?"

**Context**: tens fruiters joves i vols podar correctament.

**Resposta esperada**:

> Els **presseguers** (*Prunus persica*) es poden a **final d'hivern o inici de primavera**, quan ja no hi ha risc de gelades fortes però abans que brotin.
>
> **Objectius de la poda**:
>
> 1. **Eliminar branques mortes o malaltes**.
> 2. **Obrir la capçada** perquè entri llum i aire.
> 3. **Renovar branques fructíferes** (el presseguer fructifica en branques de l'any anterior).
>
> **Tipus de branques a distingir**:
>
> - **Brindilles** (curtes, amb borrons arrodonits): fructifiquen.
> - **Branques mixtes** (mitjanes): fructifiquen parcialment.
> - **Brots d'aigua** (llargs i verticals): no fructifiquen, treure.
>
> **Passos**:
>
> 1. **Eines**: tisores de poda netes i afilades, serra petita per branques grosses.
> 2. **Cortes a 45°**, just per sobre d'un borró que miri cap a fora.
> 3. **Eliminar** brots d'aigua, branques creuades, xucladors.
> 4. **Deixar** 3-4 branques principals ben distribuïdes.
> 5. **Aplica pasta segelladora** en talls grans.
>
> **Consell**: la primera poda en arbres joves és la més important. Defineix bé l'estructura els primers 3 anys.

**Fonts esperades**: `fruiters-guia-completa.md`, `practiques-avancades.md`.

## 42.7 Consulta 6: reg durant la calor

**Pregunta**: "Estem passant una onada de calor a 38 °C. Com he de regar l'hort?"

**Context**: temps extrem, vols evitar pèrdues.

**Resposta esperada**:

> Amb temperatures superiors a 35 °C, cal ajustar el reg:
>
> **Horari**:
>
> - Rega **primerenca del matí** (6-9 h) o al **vespre** (20-22 h).
> - **Mai** al migdia (l'aigua s'evapora i pot cremar les fulles).
>
> **Freqüència**:
>
> - Hortalisses de fruit (tomàquet, pebrot, albergínia): **cada 1-2 dies**.
> - Hortalisses d'arrel (pastanaga, rave): **cada 2-3 dies**.
> - Hortalisses de fulla (enciam, espinac): **diari**.
> - Fruiters: **setmanal** amb reg profund.
>
> **Quantitat**:
>
> - 10-15 litres per m² en regs profunds.
> - 5-8 litres per m² en regs de manteniment.
>
> **Tècniques d'estalvi**:
>
> - **Encoixinat** (mulching, cobrir el sòl amb palla, fullaraca, o plàstic) redueix l'evaporació un 50-70%.
> - **Reg per degoteig**: més eficient que l'aspersió.
> - **Reg subterrani**: tubs perforats sota la superfície.
>
> **Senyals d'estrès hídric**:
>
> - Fulles pansides al matí (no pas al migdia, és normal).
> - Color verd pàl·lid o groguenc.
> - Fruits petits o amb cremades solars.
>
> Consulta la fitxa de reg per a cada cultiu.

**Fonts esperades**: `reg-fertilitzacio.md`, fitxes individuals.

## 42.8 Consulta 7: control del pugó

**Pregunta**: "Tinc molt de pugó a les faves. Com ho combatre sense productes químics?"

**Context**: plaga comuna, vols solució ecològica.

**Resposta esperada**:

> El **pugó** a les faves és molt comú a la primavera. Combatre'l de forma ecològica:
>
> **Tractaments directes**:
>
> 1. **Sabó potàssic**: 10-15 ml per litre d'aigua. Polvoritza al matí o al vespre. Repetir cada 5-7 dies.
> 2. **Infusió d'all**: 50 g d'all picat per litre d'aigua, deixa reposar 24 h, filtra i polvoritza.
> 3. **Purí d'ortiga**: fermenta 1 kg d'ortigues en 10 L d'aigua durant 1-2 setmanes. Dilueix 1:10.
> 4. **Oli de neem**: 5 ml per litre. Molt eficaç, però car.
>
> **Control biològic**:
>
> - **Marietes** (Coccinellidae): mengen 50-100 pugons al dia. **No les matis!**
> - **Crysoperla** (crisopa): les larves mengen molts pugons.
> - **Sírfids**: les larves són depredadores.
>
> Per afavorir aquests insectes, planta **flors** al voltant de l'hort: calèndula, caps d'ase, alfalfa, facèlia.
>
> **Prevenció**:
>
> - **Evitar** l'excés de nitrogen (adobs massa rics atrauen pugons).
> - **Rotació** de cultius.
> - **Eliminar** herbes hoste (com la corretjola).
>
> Si la infestació és molt forta, poda les parts més afectades i crema-les.

**Fonts esperades**: `gestio-plagues.md`, `practiques-avancades.md`.

## 42.9 Consulta 8: guardar llavors

**Pregunta**: "Com guardo les llavors dels tomàquets per sembrar l'any vinent?"

**Context**: vols autosuficiència.

**Resposta esperada**:

> Per guardar llavors de tomàquet per sembrar l'any vinent:
>
> **1. Tria les millors plantes**:
>
> - Les més sanes, productives, i representatives de la varietat.
> - No agafis llavors de plantes híbrides (F1): la descendència no serà fidel.
>
> **2. Extracció de llavors** (per tomàquets):
>
> 1. Talla el tomàquet madur per la meitat.
> 2. Buida les llavors amb el gel en un colador.
> 3. Frega-les suaument per separar la polpa.
> 4. Deixa-les fermentar 2-4 dies en un got amb aigua (per eliminar la capa gelatinosa).
> 5. Renteu-les bé.
> 6. Escampar-les en un paper o plàtic per assecar-les (7-10 dies).
>
> **3. Assecatge i emmagatzematge**:
>
> - Asseca-les en un lloc ventilat, sense sol directe.
> - Guardar-les en un **pot de vidre** o **sobre de paper** en un lloc **fresc, sec i fosc**.
> - Afegeix un **dessecant** (gel de sílice) per evitar humitat.
> - Durada: 4-6 anys (depenent de la varietat).
>
> **4. Etiqueta sempre**:
>
> - Nom de la varietat.
> - Data de collita.
> - Procedència (any, lloc).
>
> **5. Prova de germinació** (opcional):
>
> - 10 llavors en un paper humit.
> - 7-14 dies.
> - Si germinen >7, la llavor és bona.
>
> Consulta la guia de llavors per a més detalls.

**Fonts esperades**: `guardar-llavors.md`.

## 42.10 Consulta 9: trasplantar tomàquets

**Pregunta**: "Quan i com trasplanto les plantes de tomàquet del planter al camp?"

**Context**: arriba el moment del trasplantament.

**Resposta esperada**:

> El trasplantament del tomàquet es fa a la **primavera**, quan ja no hi ha risc de gelades i el sòl està a **15-18 °C** com a mínim. A Osona, sol ser entre **finals d'abril i mitjans de maig**.
>
> **Passos**:
>
> **1. Enduriment** (7-10 dies abans):
>
> - Surt les plantes al balcó o fora, gradualment (1 h, 2 h, mig dia, dia sencer).
> - Evita sol directe les primeres hores.
> - Redueix el reg per estrès controlat.
>
> **2. Preparació del sòl**:
>
> - Llaura o cavar la terra a 30 cm de fondària.
> - Incorpora compost madur (5-10 L/m²).
> - Nivella i marca les línies de plantació.
>
> **3. Distàncies**:
>
> - Entre plantes: **50-60 cm**.
> - Entre línies: **80-100 cm**.
>
> **4. Trasplantament** (al vespre o dia ennuvolat):
>
> 1. Rega el planter 1-2 h abans.
> 2. Fes forats de la mida del test.
> 3. Treu la planta amb el pa de terra intacte.
> 4. Col·loca-la al forat, fins a les primeres fulles.
> 5. Omple amb terra, premsant suaument.
> 6. Rega abundantment.
>
> **5. Cura post-trasplantament**:
>
> - Rega diàriament la primera setmana.
> - Protegeix del sol directe els primers 2-3 dies (tela d'ombra o campana).
> - Col·loca tutors si la varietat ho necessita.
>
> **Senyals d'estrès**: fulles pansides que es recuperen al vespre és normal. Si no es recuperen, rega més.

**Fonts esperades**: `calendari-sembra.md`, `fitxa-tomaque.md`, `practiques-avancades.md`.

## 42.11 Consulta 10: elaboració d'una conserva

**Pregunta**: "Com faig conserva de tomàquet per a tot l'any?"

**Context**: tens excedent de tomàquets i vols conservar-los.

**Resposta esperada**:

> Per fer conserva de tomàquet casolana:
>
> **Ingredients**:
>
> - 5 kg de tomàquets madurs.
> - 1 ceba gran (opcional).
> - 1 cullerada de sal.
> - 1 cullerada de sucre (opcional, per reduir acidesa).
> - 1 cullerada d'oli d'oliva.
> - Alfàbrega fresca (opcional).
>
> **Passos**:
>
> 1. **Rentar** i **tallar** els tomàquets a quarts.
> 2. **Bullir** 30-45 minuts a foc lent, tapats, fins que es desfacin.
> 3. **Triturar** amb batedora o passar pel passapures.
> 4. **Colar** per eliminar llavors i pell (opcional, segons el gust).
> 5. **Coure** 20-30 minuts més, afegint sal, sucre, ceba picada, alfàbrega.
> 6. **Provar** i rectificar de sal.
> 7. **Envasar** en pots de vidre esterilitzats.
> 8. **Tapar** i **bullir al bany maria** 30 minuts per segellar.
> 9. **Deixar refredar** i guardar en lloc fresc i fosc.
>
> **Durada**: 1-2 anys si es conserva correctament.
>
> **Consells**:
>
> - Esterilitza els pots al forn a 120 °C 15 min.
> - Assegura't que la tapa fa "click" quan es refreda (bona soldadura).
> - Si una tapa no fa "click", guardar a la nevera i consumir aviat.
>
> **ATENCIÓ**: un pot mal soldat pot desenvolupar **botulisme** (perill mortal). Si el tomàquet fa mala olor, color estrany, o gas en obrir-lo, llença'l.

**Fonts esperades**: `conserves.md`, `fitxa-tomaque.md`.

## 42.12 Prompt de benvinguda personalitzat

Quan configuris el teu assistent, pots personalitzar el system prompt:

```
Ets l'assistent Hort Osona. Coneixes les 76 fitxes de cultius del
projecte BernatLab i les guies d'horticultura ecològica de la comarca
d'Osona.

CARACTERÍSTIQUES:
- Respon SEMPRE en català.
- Sigues pràctic i directe, sense floritures.
- Dona consells adaptats a la comarca d'Osona (zona mitjana, ~600 m,
  clima continental).
- Prioritza mètodes ecològics i sostenibles.
- Si no saps la resposta, digues "No tinc prou informació a les
  fitxes d'Hort Osona. Consulta la fitxa corresponent o pregunta al
  fòrum".
- Cita sempre les fonts al final de la resposta.

ESTIL:
- Frases curtes.
- Llistes numerades quan hi ha diversos punts.
- Negreta per termes clau.
- Màxim 10-15 línies per resposta (o menys).
```

Aquest prompt personalitzat es posa a la configuració d'Ollama (Cap 34) o a la variable d'entorn del backend.

## 42.13 Consells finals

1. **Pregunta amb context**. "Com plantar carbasses?" és menys útil que "Com plantar carbasses en un hort de 50 m² a Osona amb sòl argilós?".

2. **Confirma les respostes**. El model pot inventar coses. Si una recomanació et sembla estranya, consulta la fitxa original.

3. **Fes-lo servir sovint**. Com més el facis servir, més aprendràs a formular bones preguntes.

4. **Ensenya'l a la família**. Si comparteixes l'hort amb algú, ensenya'ls a usar l'assistent. Així tothom hi contribueix.

5. **Documenta les respostes bones**. Si el model dóna una resposta excel·lent, guarda-la. Pot servir d'inspiració per a futures consultes.

## 42.14 Resum

Aquest capítol ha presentat 10 consultes reals que pots fer a l'assistent Hort Osona: el calendari de sembra, diagnòstic de plagues, associacions, compost, poda, reg, plagues, guardar llavors, trasplantar, i conserves. Cada consulta ha mostrat la pregunta, el context, la resposta esperada, i les fonts. També hem vist un prompt de benvinguda personalitzat per configurar el teu assistent.

Aquest és l'últim capítol del Mòdul 4. Ara tens tot el que necessites per tenir un assistent d'IA local potent, privadesa garantida, i totalment integrat amb el teu hort. Comença amb una pregunta senzilla i experimenta!

## 42.15 Exercicis pràctics

1. Tria 3 de les 10 consultes d'aquest capítol i fes-les al teu assistent (quan estigui muntat).
2. Avalua la qualitat de les respostes i compara-les amb les respostes esperades.
3. Personalitza el system prompt amb les teves pròpies instruccions.
4. Documenta al README les 5 millors respostes que has obtingut.
5. Comparteix les consultes útils amb família o veïns.

Paraules clau: **consultes, exemples, casos d'ús, calendari de sembra, plagues, associacions, compost, poda, reg, conserves, llavors, trasplantament, hort Osona, comarca d'Osona, primavera, estiu, tardor, hivern, calendari lunar, rotació, conreu associat, planter, hivernacle, microclima, adob, fertilitzant, nitrogen, fòsfor, potassi, reg per degoteig, aspersió, encoixinat, mulching, conserves, fermentació, lactofermentació, oli d'oliva, alfàbrega, sajolida, farigola, orenga, plantes aromàtiques, plantes medicinals, infusions, decoccions, maceracions, ungüents, cremes, tintures, remeieres, saviesa popular, transmissió, aprenentatge, oralitat, etnografia, memòria oral**.
