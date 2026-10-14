# N=1 · Calibratge personal

Una pàgina web (un sol fitxer) per **esbrinar què et funciona a tu**, amb mesura
objectiva i experiment a cegues. No és un reproductor de freqüències més: és
l'instrument de mesura que al NeuroWave li falta.

## Per què existeix

El NeuroWave 3.0 et fa valorar la sessió amb "claredat mental de l'1 al 10".
Això és una impressió, i a més la saps: si creus que avui toca "el bo", el teu
cap esbiaixa la resposta.

I la recerca diu que els efectes de l'estimulació auditiva rítmica són **reals
però modestos, molt dependents dels paràmetres i diferents per a cada persona**.
Un estudi de 2025 amb 80 persones i 16 configuracions va trobar que el cervell
sí que s'enganxa a la freqüència, però que el benefici només apareix amb
combinacions concretes. Un altre va trobar que escoltar-los a casa empitjorava
el rendiment en tasques estandarditzades, tant si hi creies com si no.

Conclusió: **ningú no t'ho pot dir. Ho has de mesurar tu, sobre tu.**

## Com funciona (3 passos, ~12 minuts)

1. **Mesura prèvia** — com has dormit, energia i claredat mental (1-10).
2. **Escolta** — 5 a 20 minuts de la portadora que triïs (200 Hz, la del
   NeuroWave). L'aplicació t'assigna a l'atzar una de dues versions i **no et
   diu quina és**: una porta un batec de 7 Hz i l'altra no. Les dues sonen
   pràcticament igual.
3. **Test de vigilància** — 60 a 180 segons. Surt un cercle vermell en un moment
   impredictible i cliques tan de pressa com pots. En surt el **temps de reacció
   en mil·lisegons**, els **lapsus** (més de 355 ms) i les sortides falses.

Al final et revela quina versió has fet, i quan hi ha prou sessions **et diu si
la diferència és real o pot ser casualitat** — amb el número al davant.

## El que fa que sigui útil i no un joguet

- **És cec.** No saps el braç mentre el fas. Això mata l'efecte de saber què
  estàs prenent, que és el més difícil de matar de tots.
- **Mesura objectiva.** Mil·lisegons, no impressions. El test PVT és el mateix
  que es fa servir en recerca sobre son i atenció.
- **Et diu quan NO sap.** Amb poques sessions no inventa cap conclusió: diu que
  encara és aviat. Un resultat negatiu és un resultat.
- **Sap quan la mesura no val.** Si canvies de pestanya, el navegador alenteix
  els temporitzadors i el test deixa de ser fiable: en aquell cas **cancel·la i
  t'ho diu**, en comptes de desar una mesura falsa.
- **L'estadística és honesta.** Prova de permutació sobre la mediana, que no
  assumeix cap distribució i funciona amb poques dades.

## Ús

Obre `n1-calibratge.html` amb el navegador. No cal servidor ni instal·lar res.
Funciona des de qualsevol ordinador, i les dades es queden al teu navegador
(`localStorage`). Per passar-les a un altre ordinador: **Còpia de seguretat
(JSON)** i després **Restaura**.

**No canviïs de pestanya mentre dures el test.** El compte enrere es pot
interrompre, però el test no: si la pàgina deixa d'estar visible, es cancel·la.

## Quan tindràs una resposta

Un efecte de 5-10 ms amb 6 sessions per versió **no es veu**: calen setmanes
(20-40 sessions). Al principi l'aplicació t'ho recordarà. És normal.

## Proves

```bash
npm install jsdom          # només per a les proves
node test_stats.js         # 7 proves de l'estadística
N1_FILE=n1-calibratge.html node test_app2.js   # 51 comprovacions de l'aplicació
```

Cobreixen: la mediana, la prova de permutació (taxa d'error i potència), el
motor d'àudio cec (que la diferència entre orelles sigui la del braç assignat),
el motor del test (que compti bé els temps i els lapsus), el càlcul del
resultat, l'estadística integrada, la persistència, l'equilibri de
l'aleatorització i que res peti amb dades corruptes o buides.

## Estendre'l

Un cop el mètode funciona, hi pots posar **qualsevol cosa**: respirar 4-7-8
abans de la feina, el cafè, l'hora del dia, els 10 minuts de guitarra. La
màquina no és per a l'àudio — és per esbrinar què et funciona a tu. Per fer-ho,
canvia els dos braços a `ARMS` (nom i batec) i deixa'ls cecs.

## Límits (llegeix-ho)

- **Mesura relativa, no absoluta.** El navegador té una latència pròpia
  (10-70 ms segons el sistema). El número absolut no és comparable amb cap
  aparell de laboratori. El que val és la **diferència entre les dues versions
  en el teu mateix ordinador**.
- **No és cap eina mèdica.** No diagnostica res ni substitueix ningú.
- **No s'ha de fer servir amb antecedents d'epilèpsia o convulsions.**
