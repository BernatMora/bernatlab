# Respostes - Capitol 10: Casos reals

## Pregunta 1: Condicio gelada?

**Resposta correcta**: Temperatura < 2 graus durant 30 min.

**Explicacio**: 2 graus es el llindar conservador. Si baixa de 2 graus durant 30 min seguits, vol dir que pot arribar a 0 graus. 30 min es el temps minim per evitar falses lectures puntuals.

## Pregunta 2: Com s'evita gelada amb reg?

**Resposta correcta**: Aigua + gel allibera calor latent.

**Explicacio**: L'aigua en gelar-se allibera 334 kJ/kg. Si mulles les plantes just abans de la gelada, l'aigua es gelara pero alliberara calor que mantindra la planta a 0 graus en lloc de per sota.

## Pregunta 3: Condicio per regar?

**Resposta correcta**: Humitat < 30% i sense pluja recent.

**Explicacio**: 30% es el llindar tipic per a la majoria de cultius. La condicio "sense pluja" evita regar innecessariament quan plourà aviat.

## Pregunta 4: Eina per deteccio de plagues?

**Resposta correcta**: TensorFlow Lite amb model entrenat.

**Explicacio**: TensorFlow Lite es pot executar a la RPi amb un model entrenat amb imatges de plagues. YOLOv8-nano es la opcio mes popular actualment.

## Pregunta 5: Que es la PID?

**Resposta correcta**: Un algoritme de control.

**Explicacio**: PID (Proporcional Integral Derivatiu) es un algoritme de control que ajusta una variable d'entrada per mantenir una sortida propera al valor desitjat. Usat en controls climatics, robotics, etc.

## Pregunta 6: Risc mes gran?

**Resposta correcta**: Massa falses alertes (fatiga).

**Explicacio**: Si tens moltes falses alertes, comences a ignorar-les. Es el que es diu "alert fatigue". Cal calibrar be les regles.

## Pregunta 7 (oberta): Per que el sistema NO substitueix el pages?

**Resposta model**:

- **Sensors poden fallar**: la pila es gastara, el sensor s'humitejara, el cable es trencara. Sense dades, no hi ha sistema.
- **Calibratge**: cada sensor s'ha de calibrar. Si esta mal calibrat, les lectures son incorrectes.
- **Experiencia humana**: un pages sap que una fulla es posa groga perque ha vist mil cops. La maquina no.
- **Casos imprevistos**: una pedregada, un animal que entra, una malaltia nova. El sistema no pot preveure tot.
- **Motivacio**: el pages te passio pel que fa. La maquina nomes executa regles.

## Pregunta 8 (oberta): Com evitar falses alertes?

**Resposta model**:

- **Debounce**: esperar X temps abans d'alertar. Ex: 30 min per sota de 2 graus, no nomes un instant.
- **Multi-sensor**: confirmar amb 2 sensors. Si nomes 1 ho diu, pot ser error.
- **Hysteresis**: no alerta fins passar el llindar, pero no desactives fins baixar mes.
- **Horaris**: no alertar certes coses a certes hores (ex: no "temperatura baixa" de dia).
- **Aprenentatge**: ajustar thresholds segons l'experiencia.
- **Cancellacio automatica**: si l'alerta es resol sola en 5 min, no cal mantenir-la.

## Pregunta 9 (oberta): Cas mes facil?

**Resposta model**:

El **cas 1 (gelada)** es el mes facil per començar perque:
- Nomes necessita un sensor de temperatura (DHT22, ~3 EUR).
- La condicio es simple (T < 2 graus).
- L'alerta es clara (al mati si la nit ha fet fred).
- L'impacte es alt (evitar perdua de collita).
- La implementacio es 1-2 hores amb Node-RED.

El **cas 4 (collita)** es el segon mes facil pero requereix una bascula.

## Pregunta 10 (oberta): Altres casos?

**Resposta model**:

Algunes idees:
- **Control del compost**: sensor de temperatura al compost per saber quan esta llest.
- **Nivell d'aigua del pou**: sensor ultrasonic per saber quan omplir.
- **Vent**: anemometre per detectar dies de vent fort.
- **Obertura automatica d'hivernacle**: servo per obrir finestres segons temperatura.
- **Pollinitzacio**: registrar quan floreixen les plantes vs. quan arriben les abelles.

## Que fer si has fallat moltes

- **5-8 encerts**: Rellegir el resum.
- **3-4 encerts**: Implementa el cas 1 (gelada) com a minim.
- **0-2 encerts**: Comença amb una alerta simple de temperatura.
