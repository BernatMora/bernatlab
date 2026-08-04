# Capítol 32 — Proves de camp, cobertura i resolució de problemes

> *"El dia que posis el node al camp, vindrà una de dues coses: funcionarà o no funcionarà. Aquest capítol és per si no funciona."*

## 32.1 Per què les proves de camp són essencials

En telecomunicacions, hi ha una regla no escrita: **el laboratori menteix, el camp diu la veritat**. Pots tenir el sistema perfectament configurat al taller, amb RSSI de -50 dBm i SNR de 12 dB, i quan el posis al camp amb un arbre al mig, pluja, i un angle d'antena lleugerament diferent, tot canvia.

Per això, les proves de camp són fonamentals. Hem de validar:

1. **Cobertura**: el node arriba al gateway?
2. **Qualitat del senyal**: amb quin RSSI / SNR?
3. **Fiabilitat**: arriba sempre, o hi ha pèrdues?
4. **Banda i data rate**: SF7 funciona, o cal SF9?
5. **Durada de la bateria**: aguanta 1 mes, 3 mesos, 1 any?

## 32.2 Material per a les proves

Per fer proves de camp, necessitem:

- Un node LoRa (Heltec LoRa 32 V3, per exemple).
- Un gateway funcionant (la Raspberry amb Concentratord).
- Un portàtil amb el monitor sèrie del node.
- Accés a la consola de TTN.
- Una brúixola (per orientar l'antena).
- Un mapa o paper mil·limetrat (per dibuixar la cobertura).
- Un multímetre (per mesurar el voltatge de la bateria).
- Un cable SMA-SMA curt (per connectar l'antena temporalment).
- Una persona al camp (tu, amb el node).
- Una persona a la Raspberry (tu, mirant la consola).
- O tots dos alhora, amb un telèfon per comunicar-se.

## 32.3 Procediment general de proves

Un procediment sistemàtic per validar la cobertura:

1. **Configura el node** amb un codi que transmet cada 10 segons. Això ens permetrà veure ràpidament si funciona.
2. **Col·loca el node a la posició final** (o el més a prop possible).
3. **Mira la consola de TTN**. Hauries de veure els uplink.
4. **Anota RSSI i SNR** de cada transmissió.
5. **Espera 5-10 minuts** i compta quantes transmissions has rebut.
6. **Calcula el percentatge de pèrdua** = (transmissions enviades - transmissions rebudes) / transmissions enviades.
7. **Mou el node** a una altra posició i repeteix.

A la pràctica, fes un mapa de la zona amb les lectures:

```
         Nord
          ↑
          
[Node]    Posició 1: RSSI -65, SNR 9.5, pèrdua 0%
          
          Posició 2: RSSI -85, SNR 6.0, pèrdua 5%
          
[Gateway] Posició 3: RSSI -55, SNR 11.0, pèrdua 0%
```

## 32.4 Mètriques clau

A la consola de TTN, podem veure per a cada uplink:

- **RSSI**: potència del senyal rebut. Valors típics:
  - **> -80 dBm**: excel·lent.
  - **-80 a -100 dBm**: bo.
  - **-100 a -110 dBm**: acceptable.
  - **< -110 dBm**: pobre, probablement problemes.
- **SNR**: relació senyal-soroll. Valors típics:
  - **> 10 dB**: excel·lent.
  - **5-10 dB**: bo.
  - **0-5 dB**: acceptable.
  - **< 0 dB**: al límit, problemes.
- **Spread Factor**: el data rate usat.
- **Bandwidth**: amplada de banda del canal.
- **Frequency**: canal usat.

A més, podem veure la **distribució** al llarg del temps: si RSSI baixa gradualment, pot ser un problema (bateria, antena, obstacle). Si baixa sobtadament, pot ser un canvi a l'entorn (un arbre ha crescut, una persona passa per allà).

## 32.5 Paràmetres a ajustar

Si els resultats no són bons, podem ajustar:

### Spreading Factor (SF)

Si volem més abast, pujem SF. Com més alt, més lent però més robust:

- **SF7**: ràpid, curt abast. Per a distàncies curtes amb bona visió.
- **SF9**: bon equilibri. Recomanat per defecte.
- **SF11-SF12**: per a casos extrems. Triga molt i té límit de duty cycle.

A la pràctica, podem començar amb SF7, i si no arriba, pujar a SF9, SF10, etc.

### Potència de transmissió

A la consola de TTN, podem veure quina potència està fent servir el node. Podem forçar-la:

- A la consola del node, secció "Network Layer → ADR", podem desactivar ADR.
- A la secció "Network Layer → Transmit Power", podem posar un valor fix (per exemple, 14 dBm).

Si el node té bona visió i està a prop, podem baixar a 8 dBm per estalviar bateria. Si tenim obstacles, pujar a 14 dBm.

### Posició de l'antena

L'antena ha d'estar:

- **Vertical** (per a polarització vertical, l'estàndard a EU868).
- **Amb visió directa** al gateway (sense arbres, edificis, muntanyes al mig).
- **Com més amunt millor** (teulada, torre, pal).
- **A 1/4 d'ona del terra** (8.6 cm a 868 MHz) o múltiples d'aquesta distància.

A la pràctica, una antena a 3 metres d'alçada amb visió directa pot cobrir 5-10 km. Una antena a 1 metre d'alçada al costat d'un edifici, 100 metres.

## 32.6 Optimització de l'antena

A vegades, una bona antena marca la diferència. Algunes millores:

- **Antena més gran** (1/2 ona en lloc de 1/4 ona): +3 dB de guany.
- **Antena de fibra de vidre** amb guany de 5-6 dBi en lloc de 2 dBi: +3 dB.
- **Antena Yagi direccional**: 8-10 dBi, però perd l'omnidireccionalitat.
- **Posició allunyada de metalls**: les estructures metàl·liques absorbeixen el senyal.
- **Cable coaxial de qualitat**: LMR-200 o LMR-400, no RG-58.

A 868 MHz, cada 6 dB de millora equivalen a doblar la distància. Així que +6 dB d'antena = 2x distància.

## 32.7 Resolució de problemes habituals

### El node no es connecta al gateway (no apareix a TTN)

Causes possibles:

1. **Antena no connectada**: revisa-la.
2. **Identificadors incorrectes** (DevEUI, AppEUI, AppKey): comprova'ls.
3. **Freqüència incorrecta**: el node ha d'estar a EU868.
4. **Gateway apagat o no connectat**: revisa la consola de TTN.
5. **Distància massa gran**: apropa el node temporalment.
6. **Problema d'alimentació**: el node es reinicia constantment.

### El node es connecta però perd molts missatges

Causes possibles:

1. **RSSI baix**: problema de cobertura. Mou el node o el gateway.
2. **SNR baix**: interferències. Canvia de canal o SF.
3. **Bateria baixa**: el node no pot transmetre amb prou potència.
4. **Antena mal orientada**: prova altres posicions.

### El node consumeix massa bateria

Causes possibles:

1. **Deep sleep no funciona**: el node està sempre actiu.
2. **Transmissions massa sovint**: cada 5 min és poc, cada 10 segons és massa.
3. **Wi-Fi o Bluetooth activats**: consumeixen molta energia.
4. **Bateria defectuosa**: canviar-la.
5. **Temperatura extrema**: la bateria dura menys a temperatures baixes.

### El gateway no rep transmissions

Causes possibles:

1. **Concentratord no connectat**: revisa els logs.
2. **SPI mal configurat**: revisa els pins.
3. **Freqüència del gateway diferent del node**: han de coincidir.
4. **Antena del gateway mal connectada**: revisa-la.
5. **Problema d'Internet**: revisa que la Raspberry tingui connectivitat.

## 32.8 Tests automatitzats

Per validar el sistema de forma regular, podem fer tests automatitzats:

```bash
# Test 1: el gateway està connectat?
curl -s http://100.x.y.z:3001/ | grep -q "concentratord" && echo "Gateway OK" || echo "Gateway FALL"

# Test 2: les últimes dades del node
influx query '
  from(bucket: "hort-osona")
  |> range(start: -1h)
  |> filter(fn: (r) => r._measurement == "sensor_lora")
  |> count()
' --org bernatlab --token TOKEN
```

A Uptime Kuma, afegim un test que comprova que rebem dades cada 15 minuts. Si no, alerta.

## 32.9 Documents i bitàcoles

Cada vegada que anem al camp, val la pena portar una **bitàcola**:

- Data i hora.
- Posició del node (coordenades GPS si és possible).
- RSSI / SNR.
- Pèrdues de paquets.
- Voltatge de la bateria.
- Condicions meteorològiques (pluja, vent, etc.).
- Notes (obstacles nous, arbres que han crescut, etc.).

Amb el temps, aquesta bitàcola ens permetrà veure patrons i prendre decisions informades (on posar el gateway, quina antena fer servir, etc.).

## 32.10 Quan el problema és l'entorn

A vegades, la cobertura no és bona perquè l'entorn és difícil:

- **Bosc dens**: els arbres absorbeixen el senyal, sobretot amb fulla (a l'estiu, més pèrdua que a l'hivern).
- **Edificis**: formigó, metall, vidre amb revestiment metàl·lic són hostils.
- **Muntanyes**: difícil salvar-les sense repetidors.
- **Interferències**: altres sistemes a 868 MHz poden molestar.

Solucions:

- **Moure el gateway** a una posició millor (teulada, torre, etc.).
- **Afegir un segon gateway** en una posició intermèdia.
- **Augmentar l'alçada de l'antena**.
- **Canviar a una antena més direccional**.
- **Usar SF més alt** per a més robustesa.

## 32.11 Quan afegir un segon gateway

Si la zona és gran o hi ha obstacles, un sol gateway pot no ser suficient. Afegir-ne un segon:

- **Rep la mateixa transmissió** (LoRaWAN és broadcast, tots els gateways reben).
- **Millora la cobertura** (redundància).
- **Permet triangular** (a partir del RSSI i temps d'arribada, podem localitzar el node).

A la pràctica, un segon gateway és útil quan:

- La zona té més de 5 km².
- Hi ha obstacles grans (muntanyes, edificis alts).
- Volem molta fiabilitat (sempre volem cobertura).

Al BernatLab, podem afegir un segon gateway a la Raspberry del camp, o a casa d'un veí, o a qualsevol punt amb electricitat i Internet.

## 32.12 Pla de proves per a Hort Osona

Per validar el sistema a Hort Osona, podem fer aquestes proves en ordre:

### Dia 1: proves al taller

1. Connectar el node amb el sensor.
2. Verificar que el node arrenca correctament.
3. Verificar que es connecta a TTN.
4. Mirar els primers uplinks.
5. Mesurar el consum en deep sleep.

### Dia 2: proves a curta distància

1. Posar el node a 10 metres del gateway.
2. Verificar que arriba amb bon RSSI.
3. Comptar transmissions durant 10 minuts.
4. Moure el node a 50 metres, 100 metres, etc.

### Dia 3: proves al camp

1. Portar el node a l'hort (245 metres de casa).
2. Posar-lo a la posició final.
3. Verificar que arriba al gateway de casa.
4. Mesurar RSSI / SNR.
5. Si cal, moure'l fins trobar una bona posició.
6. Deixar-lo 24 hores i veure com es comporta.

### Dia 4: proves de bateria

1. Carregar la bateria al màxim.
2. Posar el node a la posició final amb el deep sleep activat.
3. Cada dia, mirar el voltatge de la bateria.
4. Estimar quants dies dura.

### Dia 5: proves de cobertura

1. Portar el node a diferents punts de l'hort i del voltant.
2. Fer un mapa de cobertura.
3. Identificar zones mortes.
4. Decidir si cal un segon gateway o una antena millor.

### Dia 6: proves de llarg termini

1. Deixar el node en producció 1 setmana.
2. Mirar les gràfiques d'estabilitat (RSSI, SNR al llarg del temps).
3. Documentar el comportament.
4. Ajustar el que calgui.

## 32.13 Manteniment continu

Un cop el sistema estigui en producció, cal mantenir-lo:

- **Cada setmana**: mirar les gràfiques d'estabilitat (RSSI, SNR, bateria).
- **Cada mes**: netejar l'antena del node (pols, brutícia).
- **Cada trimestre**: revisar la bateria, substituir-la si cal.
- **Cada any**: revisar l'estat de la caixa estanca, substituir segells si cal.

## 32.14 Quan re-emplaçar

De vegades, malgrat tots els esforços, una posició no funciona. Si:

- El node perd > 50% de transmissions malgrat SF alt i antena bona.
- El node consumeix la bateria en menys d'1 setmana.
- El node es desconnecta del gateway aleatòriament.

Cal:

- Considerar una **altra posició** (a 50 metres hi ha vegades 30 dB de diferència).
- Considerar un **segon gateway** més a prop.
- Considerar **canviar la tecnologia** (per exemple, NB-IoT si tenim cobertura 4G).

## 32.15 Resum

En aquest capítol hem après a fer proves de camp: com validar la cobertura, com mesurar la qualitat del senyal, com resoldre problemes, quan afegir un segon gateway, i quin pla de proves seguir. Hem après que el laboratori menteix i el camp diu la veritat, i que cal validar tot amb dades reals.

Aquest és l'últim capítol del Mòdul 3. Si tens el LoRa a les mans, comença pel pla del dia 1 (taller), segueix amb el dia 2-3 (curta distància i camp), i no passis al dia 4-5 (bateria i cobertura) fins que tot funcioni bé. Quan tinguis el node en producció 24/7, podem començar el **Mòdul 4 (IA local amb Ollama)** o afegir un segon node al camp.

## 32.16 Exercicis pràctics

1. Fes un mapa de cobertura a 50, 100, 200, 500 metres del gateway.
2. Mesura el consum de corrent del node en deep sleep.
3. Comprova el voltatge de la bateria cada dia durant una setmana.
4. Documenta els RSSI / SNR a cada posició.
5. Fes proves amb SF7, SF9, SF11. Compara la cobertura.
6. Si tens un segon gateway disponible, configura'l i veu com millora la cobertura.
7. Escriu un runbook de resolució de problemes basat en les teves experiències.
8. Comparteix les conclusions al README del projecte.

Paraules clau: **proves de camp, cobertura, RSSI, SNR, packet loss, FSPL, LOS, NLOS, visió directa, antena, polarització, guany, dBi, VSWR, gateway, Concentratord, SX1302, node, deep sleep, bateria, SF, BW, CR, TX power, ADR, propagació, atenuació, interferències, pluja, arbres, edificis, muntanyes, mapa, bitàcola, runbook**.
