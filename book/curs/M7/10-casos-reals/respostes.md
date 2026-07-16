# Respostes - Capitol 10: Casos reals de l'Hort Osona

> Mira les respostes DESPRES d'haver fet el qüestionari.

## Pregunta 1: Llindar critic d'humitat per a tomàquet

**Resposta correcta**: 25-30%.

**Explicacio**: El tomàquet te un llindar critic d'humitat del soll al voltant del **25-30%** per a la majoria de substrats. Per sota d'aquest valor, les arrels comencen a tenir dificultats per absorbir aigua i la planta activa mecanismes de defensa (pansiment de fulles, reduccio de fotosintesi). Per sobre del 70% hi ha risc d'asfixia radicular.

A l'Hort Osona tenim sensors MiFlora que mesuren humitat. La regla es:
- **<25%**: regar ja.
- **25-40%**: condicions ideals.
- **40-60%**: una mica alt, vigilar.
- **>60%**: risc d'asfixia radicular i fongs.

---

## Pregunta 2: Proteccio contra gelada amb calor latent

**Resposta correcta**: Regar el sol al vespre abans de la gelada.

**Explicacio**: L'aigua allibera **80 calories/gram** en solidificar (calor latent de fusio). Si mulles el sol al voltant de les plantes al vespre, l'aigua al gelar-se escalfa l'aire proper **0.5-1°C**, el just per salvar les plantes d'una gelada lleugera.

Es una tecnica utilitzada pels pagesos des de fa segles. Funciona especialment be amb gelades de **radiacio** (vent en calma, cel seré). **Limitacio**: nomes protegeix fins a -2°C.

Altres tecniques de proteccio:
- **Manta termica o tela de Nadal**: protegeix fins a -3°C.
- **Ampolles d'aigua plena**: massa termica que allibera calor.
- **Ventilacio (ventiladors)**: mescla l'aire fred amb el de dalt (que es mes calent).
- **Cremar teules o bidons**: escalfa l'aire (risc d'incendi, nomes per emergencies).

---

## Pregunta 3: Millor moment per regar en zones caloroses

**Resposta correcta**: Matinades i capvespres.

**Explicacio**: Regar a les hores de menys calor redueix les perdues per **evaporacio**. A ple sol (12-16h), fins al 40% de l'aigua de reg s'evapora abans d'arribar a les arrels. Regant a les **05:00-07:00** o a les **20:00-22:00** maximitzem l'aprofitament.

A l'Hort Osona tenim el reg programat a les **06:00** (primer reg) i a les **21:00** (segon reg). D'estiu, afegim un reg curt a les **14:00** (5 min) per als sectors mes exposats al sol de tarda.

**Regar a la nit** (despres de les 22:00) pot afavorir fongs al sol i a les fulles. Per tant evitem regar amb aspersio de nit. Amb degoteig es acceptable.

---

## Pregunta 4: Estalvi d'aigua amb mulch

**Resposta correcta**: 40-60%.

**Explicacio**: El **mulch** (coberta del sol) redueix l'evaporacio un 40-60% segons el material. Els materials mes comuns:

| Material | Estalvi | Cost | Durada |
|---|---|---|---|
| Palla | 50% | 5-10€/m2 | 6-12 mesos |
| Fullaraca | 40% | 0€ | 3-6 mesos |
| Compost | 45% | 0-5€/m2 | 3-6 mesos |
| Plàstic negre | 70% | 1-2€/m2 | 1-2 anys |
| Geotextil | 60% | 3-5€/m2 | 3-5 anys |

A l'Hort Osona fem servir **palla de cereal** (10€ per 20 m2) que dura 1 any i alhora va enriquint el sol en descomposar-se.

---

## Pregunta 5: Risc de trasplantar massa aviat

**Resposta correcta**: Que una gelada tardana els mati.

**Explicacio**: A Osona, les solanacies (tomàquet, pebrot, alberginia) son molt sensibles a la gelada. Trasplantar-les abans de la darrera gelada es arriscar-se a perdre tota la collita. La data segura es **2 setmanes despres de la darrera gelada climatica** a la teva zona.

A l'Hort Osona:
- **Darrera gelada climatica** (mitjana 15 anys): 15 d'abril.
- **Trasplantament segur**: 25-30 d'abril.
- **Zona alta (900+ m)**: esperar fins al 10-15 de maig.

Si vols arriscar-te, pots trasplantar abans pero **amb proteccio** (manta termica, ampolles d'aigua, reg anti-gelada). Es una aposta: si no gelada, guanyes 2 setmanes; si gela, pots perdre 50 plantes.

---

## Pregunta 6: Sensor que cal a tots els sectors

**Resposta correcta**: Humitat del sol.

**Explicacio**: La **humitat del sol** es el parametre que mes directament indica si les plantes pateixen. Una baixada sobtada indica fallada de reg, una pujada indica pluja o excés, una davallada lenta indica sequera progressiva.

Es el sensor que **mai no hauria de faltar** a cap sector. Altres sensors son importants pero menys critics:
- **Temperatura ambient**: es pot obtenir de la web del Meteocat.
- **Lluminositat**: es pot obtenir d'una estacio meteorologica propera.
- **EC**: nomes es critica per a cultius en test o hidroponia.

A l'Hort Osona tenim sensors d'humitat a tots els sectors despres del cas 3 (la bomba d'aigua avariada).

---

## Pregunta 7: Canal per alertes critiques 24/7

**Resposta correcta**: Telegram.

**Explicacio**: **Telegram** es la opcio mes utilitzada per a alertes automatiques 24/7 perque:
- Es **gratis**.
- Es **instantani** (latencia <2s).
- Te una **API molt senzilla** (1 POST request).
- Funciona a **tot arreu** (mobil, tablet, web, desktop).
- Permet **grups** (alertes a varies persones).
- Te **botons interactius** per confirmar/rebutjar.

Alternatives:
- **Email**: lent (5-30 min), arriba al spam.
- **SMS**: car (~0.05€ per SMS), nomes per a coses molt critiques.
- **Push notifications web**: complicat de configurar per self-hosting.
- **Discord/Slack**: bona alternativa, similar a Telegram.

A l'Hort Osona usem Telegram perque es rapid, gratis i te bona API.

---

## Pregunta 8: Anys de dades per veure patrons

**Resposta correcta**: 2-3 anys.

**Explicacio**: Els patrons climatics i de cultiu tenen **variabilitat interanual**. Un any pot ser excepcionalment caloros, un altre excepcionalment fred. Per veure el patro real (no nomes l'atzar), necessites **2-3 anys** minim.

Amb 1 any de dades pots veure la **mitjana** pero no la **variabilitat**. Amb 2-3 anys pots calcular **mitjana, desviacio estandard, i extrems**. Amb 10+ anys pots fer estadistiques climatiques reals.

A l'Hort Osona portem 2 temporades. Ja tenim **patrons clars** que es repeteixen:
- Gelades tardanes: sempre a l'abril-maig.
- Onades de calor: juliol-agost.
- Pluja excessiva: octubre-novembre.
- Pugons: maig i setembre.

---

## Pregunta 9 (oberta): Cas real salvat per sensors

**Resposta model**:

**Cas**: Tomàquets pansits a la tarda de juliol.

**Escenari**: tinc 30 tomàquets al sector A. A les 14:00, quan passo per l'hort, veig que les fulles estan pansides. Em pregunto: "fa calor, es normal, o algo va malament?". Sense sensors, **no ho puc saber**. Pot ser:
- Normal (la planta es defensa de la calor).
- Estres hidric (manca d'aigua).
- Malaltia (fungica, per exemple).
- Problema d'arrels (nematodes).

**Amb sensors**:

1. **Pose un sensor d'humitat del sol** (MiFlora) al sector A, a 10 cm de profunditat.
2. **Configuro una alerta a Grafana**: si humitat <25% durant mes de 2 h, envia missatge a Telegram.
3. **Configuro una alerta a InfluxDB**: una tasca que cada hora calcula la humitat minima del dia. Si baixa del 25%, marca una alerta al log.

**La situacio abans i despres**:

**Sense sensors**:
- Dia 1: les fulles es pansen, no faig res perque "fa calor".
- Dia 2: les fulles continuen pansides, potser començo a regar mes.
- Dia 3: em dono compte que hi ha un problema pero ja he perdut 2-3 dies.
- Resultat: 20-30% menys de collita, plantes debilitades.

**Amb sensors**:
- 10:00: rebo alerta al mobil. Humitat sector A: 22% (llindar 25%).
- 10:05: vaig a l'hort, veig que la bomba funciona. El problema es que l'hora del reg es massa tard.
- 10:10: reprogramo el reg. Activo un reg curt a les 14:00.
- 10:30: problema resolt.
- Resultat: 0 perdues, plantes sanes.

**Lliço**: els sensors **no nomes mesuren, sinó que canvien el temps de reaccio**. De 2-3 dies a 30 minuts. En agricultura, això es la diferencia entre una collita normal i una perdua del 30%.

---

## Pregunta 10 (oberta): Pla d'actuacio per bomba avariada

**Resposta model**:

**Escenari**: dimarts a les 11:00, bomba d'aigua espatllada. Hort de 80 m2. Estic a 30 min de l'hort. Cal regar 4-6 L/m2 al dia = 320-480 L al dia.

**Pla d'actuacio pas a pas**:

**Minut 0**: rebo l'alerta de Telegram: "Humitat sector A: 18% < llindar 25%, tendencia: baixa desde les 09:00. Bomba no registrada encesa en 2h".

**Minut 5**: truco al meu amic que te clau de l'hort per confirmar que no es un fals positiu. Si no respon en 15 min, truco a un segon amic.

**Minut 10-30**: vaig cap a l'hort. Mentrestant, envio un missatge al grup de Telegram: "Bomba possiblement avariada, vaig cap a l'hort".

**Minut 30-60**: arribo a l'hort. Comprovo:
- La bomba s'engega pero no bomba? Problema mecanic (impulsor trencat, obstruccio).
- La bomba ni s'engega? Problema electric (fusible, disjuntor, condensador).
- Hi ha corrent al motor? Problema de fase o interruptor.

**Decisions**:

- **Si es algo simple** (fusible, disjuntor): ho arreglo en 5 min. Restableixo el reg.

- **Si es la bomba (impulsor trencat)**: 
  1. Connecto una manguera a la xarxa d'aigua del veinat (si es accessible).
  2. Reg manual amb manguera 2 cops al dia (mati i vespre), 30 min cada cop.
  3. Demano una bomba nova online o a la ferreteria.
  4. Si tinc **bomba de recanvi** guardada, la substitueixo.

- **Si es el pou** (no arriba aigua): truc al lampista.

**Cobertura de vacances**:

Si estic de vacances i rebo l'alerta, el **pla B** es:

1. **Alerta escalada**: si no rebo confirmacio en 30 min, s'envia una alerta al meu company/amic.
2. **Protocol d'actuacio per escrit**: tinc un document al GitHub del projecte que diu pas a pas que ha de fer el company.
3. **Acces remot**: el company te clau de l'hort i la clau de la caseta de la bomba.
4. **Contacte del lampista local**: tinc el telefon guardat al document.
5. **Bomba de recanvi**: la tinc comprada i guardada a la caseta, per si de cas.

**Millora llarg termini**:

Aprofito per instal·lar un **sistema de doble bomba**:
- 2 bombes en paral·lel.
- Commutacio automatica: si la bomba A falla, arranca la B.
- Sensor de corrent a cada bomba (pin GPIO).
- Alerta si les 2 bombes fallen alhora.

Cost: 400€ en material. Estalvi: una collita sencera.

---

## Que fer si has fallat moltes preguntes

- **5-8 encerts**: Rellegir el resum, sobretot els 3 casos reals.
- **3-4 encerts**: Repassar els llindars critics (humitat, temperatura) i les tecniques de proteccio.
- **0-2 encerts**: Comencem pel basic: que es un sensor, que es una alerta, com funciona Telegram.

## Que fer si has encertat totes

- **Felicitats! Has acabat el modul M7** (Hort Osona en accio).
- Passa al **modul M8** (que no es Hort Osona pero es l'extensio del curs).
- Comparteix els teus casos reals al GitHub del projecte.
- Escriu un article al teu blog sobre el teu hort.
- Experimenta amb nous sensors (vent, pluja, radiacio solar).
- Aplica el sistema a altres ambits: aiguamolls, hivernacles, camps.
