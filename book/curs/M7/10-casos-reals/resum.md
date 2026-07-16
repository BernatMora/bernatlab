# Resum - Capitol 10: Casos reals de l'Hort Osona

## La idea clau

Aquest capitol es el **resum practic** de tot el modul M7. Veurem **3 casos reals** que han passat a l'Hort Osona (o horts similars) i com els sensors, el calendari, les alertes i la PWA han ajudat a **detectar, diagnosticar i resoldre** problemes reals. Son exemples d'**enginyeria aplicada**: no nomes tenir dades, sino **actuar** en consequencia.

Els 3 casos:
1. **Deteccio de gelada tardana** (abril 2025) - salvar 40 tomàquets.
2. **Optimitzacio del reg** (juliol 2025) - estalvi de 30% d'aigua.
3. **Alerta de bomba d'aigua avariada** (setembre 2025) - evitar perdua de cultiu.

## Cas 1: Gelada tardana del 19 d'abril de 2025

**Context**: el 18 d'abril de 2025 el pronostic del temps anunciava temperatures negatives per la matinada. La previsio deia -2°C a 850 m. A l'Hort Osona tenim **30 plantes de tomàquet** trasplantades feia 3 dies (massa aviat, error de calcul) i **10 pebrots** que encara eren al viver.

**El que van veure els sensors**:

A les 22:00 el sensor de temperatura exterior marcava 6°C i queia 0.5°C/h. A les 02:00 marcava 1.2°C. A les 04:30 marcava -0.8°C. A les 06:00 marcava -1.5°C. La previsio s'havia complert.

**El que va fer el sistema**:

1. L'script `gelada_watch.py` que tenia a la RPi va comparar la previsio del Meteocat (API oberta) amb la tendencia de les ultimes 4 hores. Va enviar una **alerta a Telegram** a les 22:00: "Risc de gelada en 6 hores, temperatura actual 6°C i baixant".

2. Vaig rebre l'alerta al mobil i vaig anar a l'hort. Vaig cobrir els tomàquets amb **manta termica** (tela de 30 g/m2) i vaig posar **ampolles d'aigua plena** als pebros del viver. Tambe vaig regar abundantment el sol (reg anti-gelada).

3. A les 06:00, quan el sol va sortir, vaig retirar les mantes. **Cap planta morta**. Les fulles d'alguns tomàquets tenien una mica de marques pero van rebrotar en 2 setmanes.

**Lliçons apreses**:

- **Les alertes automatiques salven collites**. Sense l'alerta, hauria descobert la gelada al mati quan ja era tard.
- **Trasplantar massa aviat es arriscat**. Hauria d'haver esperat fins a finals d'abril o principis de maig. El calendari aconsellava 25 d'abril, vaig plantar el 16 d'abril (precipiti perque feia bon temps).
- **La manta termica val or**. 20€ gastats, 30 plantes salvades.
- **El reg anti-gelada funciona** pero nomes si ja hi ha un sistema de reg instal·lat.

**Millora al sistema**:

Despres d'aquest cas vaig afegir:
- **Doble font de previsio**: Meteocat + OpenWeather (amb API key) per validar.
- **Alerta a les 18:00** del dia anterior si la previsio es <2°C per la matinada.
- **Test de coberta automatic**: un script que recomana "cobrir amb manta" vs "no cal" segons el risc.
- **Sondeig de T a 5 cm i a 50 cm**: la T a 5 cm es la que pateix la planta, no la T a 2 m del sensor.

## Cas 2: Optimitzacio del reg (juliol 2025)

**Context**: juliol es el mes mes caloros a Osona (T maximes 32-36°C). Els tomàquets i pebrots necessiten 4-6 L/m2 al dia. L'hort te 80 m2 de superficie, pero no tota la superficie es rega igual. Tenim sensors MiFlora als sectors A i C pero no als sectors B i D. El reg es per degoteig amb un programador a 2 zones.

**Problema detectat**: les plantes del sector A (tomàquets) es pansien a les 14:00 tot i tenir reg programat a les 06:00 i a les 20:00. Les fulles es pansien pero es recuperen al vespre. Les plantes del sector C (pebrots) estan perfectes. La diferencia? El sector A te **molta mes exposicio al sol de tarda**.

**Analisi amb sensors**:

Mirant les dades d'humitat del sector A al llarg de juliol:

- **00:00 - 06:00**: humitat puja de 35% a 65% (reg automatic de les 06:00, pero abans ja pujava per la nit).
- **06:00 - 10:00**: humitat baixa de 65% a 50% (matinada, baixa evapotranspiracio).
- **10:00 - 16:00**: humitat baixa de 50% a 28% (sol fort, T 30-35°C, evapotranspiracio maxima).
- **16:00 - 20:00**: humitat baixa de 28% a 22% (tarda calorosa).
- **20:00 - 24:00**: humitat puja de 22% a 35% (reg automatic de les 20:00, baixa evapotranspiracio).

**Conclusio**: les plantes del sector A pateixen **estres hidric a la tarda**. L'humitat baixa de 22% al vespre, per sota del llindar critic (25-30% per a tomàquet). Les fulles es pansien com a mecanisme de defensa (perden turgencia).

**Solucio implementada**:

1. **Reg curt a les 14:00** (5 min, 0.5 L/m2) per humitejar el soll a la zona radicular. No es reg abundant, es un "refresc".
2. **Mulch de palla** de 5 cm al sector A. Redueix l'evaporacio un 40-60%. Cost: 10€ per 20 m2. Es va aplicar al juliol.
3. **Augmentar el temps de reg del mati i del vespre** un 20% per compensar.
4. **Moure el reg automatic a les 05:00 i 21:00** (hora menys calorosa).

**Resultats despres de la optimitzacio**:

- Humitat minima del sector A: de 22% a 35% (millora de 13 punts).
- Cap planta pansida a la tarda.
- **Consum d'aigua**: de 5.2 L/m2/dia a 3.6 L/m2/dia (estalvi del 30%).
- **Collita**: 18% mes de tomàquets (menys estrés = mes fruits).

**Lliçons apreses**:

- **Mesurar es clau**. Sense els sensors del sector A, hauries regat "a ull" i hauries continuat igual.
- **Mulch es la inversio mes rendible** d'un hort. Costa poc i estalvia molta aigua.
- **L'hora del reg importa**. Regar a ple sol es perdre aigua per evaporacio.
- **Comparar sectors** (A vs C) ajuda a entendre les diferencies locals.

**Millora al sistema**:

Despres d'aquest cas vaig afegir sensors al sector B (encara no) i un **alerta d'humitat baixa** al Grafana: si humitat <25% durant mes de 2 h, envia una notificacio.

## Cas 3: Bomba d'aigua avariada (setembre 2025)

**Context**: el 12 de setembre de 2025 a les 11:00, el sector A i B es queden sense reg. Les plantes comencen a pansir-se. A les 15:00 rebo una **alerta de Telegram** del sistema de monitoratge: "Humitat sector A: 18% (llindar critic 25%). Tendencia: baixa desde les 09:00".

**Investigacio**:

1. Reviso la bomba d'aigua (electrobomba de 0.5 HP que porta l'aigua del pou a la cisterna). Esta engegada pero no bomba aigua. **S'ha espatllat**.
2. Tinc **2 alternatives**: (a) comprar una bomba nova (200€, 3 dies d'espera) o (b) regar manualment amb una manguera connectada a la xarxa d'aigua del veinat.
3. Decideixo **regar manualment** durant 3 dies. Cada mati i cada tarda, 30 min amb manguera.

**L'impacte al sistema**:

- **Sense sensors** hauria trigat mes a detectar el problema. Hauria vist les plantes pansides a la tarda del primer dia, pero hauria pensat "fa calor, es normal".
- **L'alerta automatica** va reduir el temps de reaccio de ~6h a <1h.
- **Les plantes del sector A** (que tenien sensors) van rebre aigua manual 2h despres de l'avaria. Van aguantar be.
- **Les plantes del sector C** (que tambe tenien sensors) tenien un nivell d'humitat mes alt perque estan a la sombra i van aguantar fins que vaig poder regar-les al vespre.
- **El sector D** (sense sensors) va passar 8h sense reg. Es va perdre un 20% de la collita de col de Bruxelles (que son molt sensibles).

**Lliçons apreses**:

- **Alertes automatiques salven collites**. Pero nomes si el sistema es robust.
- **Cal sensors a TOTS els sectors**, no nomes a alguns. Si el sector D hagues tingut sensor, hauria actuat abans.
- **Cal un pla B per a la bomba**. Ara tinc una **bomba de recanvi** comprada i guardada.
- **L'hortola ha d'estar disponible** per actuar quan arriba l'alerta. Si estic de vacances, el sistema ha d'avisar algu mes.

**Millora al sistema**:

Despres d'aquest cas:
- **Sensors d'humitat a tots els sectors** (no nomes A i C).
- **Alerta escalada**: si no rebo confirmacio de la primera alerta en 30 min, envia una segona alerta al meu company.
- **Indicador de "bomba activa"**: pin GPIO que llegeix el corrent de la bomba. Si el corrent es zero pero el programador diu "ON", algo no va be.
- **Registre de regs**: cada reg queda registrat a InfluxDB. Si no hi ha registre, es que la bomba no ha funcionat.

## Comportament general del sistema

Ara que porto **2 anys amb l'Hort Osona** automatitzat, el patro es clar:

1. **Els sensors recullen dades** (temperatura, humitat, EC, llum).
2. **InfluxDB les emmagatzema** a llarg termini.
3. **Grafana mostra els grafics** de tendencia.
4. **Les alertes de Telegram avisen** quan algo va malament.
5. **El calendari recorda** les feines de cada setmana.
6. **La PWA ho integra tot** en una sola interficie.

Aixi es un **circuit tancat**: detectar -> alertar -> actuar -> mesurar -> aprendre.

## Patrons que es repeteixen

Despres de 2 anys he vist patrons que es repeteixen:

- **Gelades tardanes**: sempre a l'abril-maig. Cal estar preparat.
- **Onades de calor**: juliol-agost. Cal anticipar regs.
- **Pluja excessiva**: octubre-novembre. Cal drenatge.
- **Plaques de pugons**: maig i setembre. Cal tractament preventiu.
- **Bolqueda d'enciams**: juny-juliol. Cal canviar a varietats resistents.

Tots aquests patrons son **previsibles** si tens 2-3 anys de dades. El calendari es pot **ajustar** any rere any segons l'observacio.

## Connexions amb altres capitols

- **M7 Cap 1** - Les dades que recollim son la base de tot.
- **M7 Cap 2** - Els sensors MiFlora detecten els canvis d'humitat.
- **M7 Cap 4** - L'arquitectura permet rebre alertes en temps real.
- **M7 Cap 6** - InfluxDB guarda l'historic que permet veure patrons.
- **M7 Cap 7** - L'API exposa les dades per a la PWA.
- **M7 Cap 8** - La PWA mostra els grafics i les alertes.
- **M7 Cap 9** - El calendari ens recorda les feines.

## Conclusio

Aquest modul ha estat un viatge: hem passat de **dades** (cap 1) a **casos reals** (cap 10). L'objectiu final es que la tecnologia **servesqui a l'hortola**, no al reves. Els sensors son una eina, no una finalitat. Si gracies a ells pots dormir mes tranquil, estalviar aigua, o salvar una collita, ja ha valgut la pena.
