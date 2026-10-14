# 🧪 N=1 — Calibratge personal

Una pàgina web d'un sol fitxer per **esbrinar què et funciona a tu**, amb mesura
objectiva i experiment a cegues.

No és un reproductor de freqüències més: és **l'instrument de mesura que al
NeuroWave 3.0 li falta**. El NeuroWave valora les sessions amb una impressió
("claredat mental de l'1 al 10"), i una impressió no és una mesura.

## El problema que resol

La recerca sobre estimulació auditiva rítmica diu tres coses incòmodes:

1. L'efecte és **real però modest** (meta-anàlisi de 2019: mida de l'efecte 0,45).
2. Depèn **molt dels paràmetres**. Un estudi de 2025 amb 80 persones i 16
   configuracions va confirmar que el cervell s'enganxa a la freqüència, però
   que el benefici només apareix amb combinacions concretes de freqüència,
   portadora, soroll i moment.
3. **És individual.** Un altre estudi va trobar que escoltar-los a casa
   empitjorava el rendiment, tant si hi creies com si no — possiblement perquè
   una freqüència genèrica interfereix amb el ritme natural de cada cervell.

Conclusió: **ningú no t'ho pot dir. Ho has de mesurar tu, sobre tu.** Les apps
venen presets fixos i la recerca estudia grups, no persones.

## Com funciona (3 passos, ~12 minuts)

1. **Mesura prèvia** — com has dormit, energia i claredat mental (1-10).
2. **Escolta** — 5 a 20 minuts d'una portadora (200 Hz per defecte, la del
   NeuroWave). L'aplicació t'assigna a l'atzar una de dues versions i **no et
   diu quina és**: una porta un batec de 7 Hz i l'altra no. Les dues sonen
   pràcticament igual.
3. **Test de vigilància (PVT)** — 60 a 180 segons. Surt un cercle vermell en un
   moment impredictible i cliques tan de pressa com pots. En surt el **temps de
   reacció en mil·lisegons**, els **lapsus** (>355 ms) i les sortides falses.

Al final revela quina versió has fet, i amb prou sessions diu si la diferència
és real o pot ser casualitat.

## Les decisions de disseny que importen

| Decisió | Per què |
|---|---|
| **Braç cec** | Si saps que avui toca "el bo", el cap esbiaixa la valoració. Amagant-ho, la mesura és vàlida. És la raó de ser del projecte. |
| **Mesura objectiva (PVT)** | Mil·lisegons, no impressions. És el test que es fa servir en recerca sobre son i atenció. |
| **Prova de permutació sobre la mediana** | No assumeix cap distribució i funciona amb poques dades. |
| **Branca "encara és aviat"** | Amb menys de 8 sessions no conclou res. Un resultat negatiu és un resultat. |
| **Cancel·la si la pàgina no és visible** | Veuràs per què a sota. |

## Verificat, no suposat

Té 51 comprovacions automàtiques de l'aplicació i 7 de l'estadística. Dues
**fallades reals es van trobar mesurant, no llegint el codi**:

1. **L'aleatorització estava trencada.** El `blockStart` era una variable local
   que es perdia en descartar una sessió, i la segona de cada parell anava
   sempre al mateix braç (9-vs-3 en comptes de 6-vs-6). Hauria invalidat
   l'experiment sencer. Ara es compta el que realment s'ha desat.
2. **Si canvies de pestanya, el test es penjava en silenci.** El navegador
   congela els temporitzadors a 1 cop per segon i atura el
   `requestAnimationFrame` del tot (documentat per Chrome). Un test fet així
   genera dades escombraries. Ara es detecta amb `visibilitychange` i es
   cancel·la la sessió en comptes de desar una mesura falsa.

## Ús

**Des de qualsevol aparell de la xarxa (Tailscale):**
`http://100.115.134.76:8088/n1.html`

**A la feina, sense Tailscale:** el fitxer és **autocontingut** (cap font, cap
imatge ni script extern). Te'l pots enviar per correu o desar-lo en un llapis i
obrir-lo amb doble clic. No cal servidor.

**No canviïs de pestanya mentre dura el test.** El compte enrere es pot
interrompre, però el test no.

## On viuen les dades

Al `localStorage` del navegador on l'obres (clau `cal_n1_v1`), mai al servidor.
Per moure-les entre ordinadors: **Còpia de seguretat (JSON)** i **Restaura**.

> **Important per a la validesa:** fes servir sempre **el mateix ordinador i amb
> auriculars**. La latència del navegador és diferent a cada màquina (10-70 ms),
> i si canvies de màquina a mig camí la diferència que mesuris pot ser de
> l'ordinador i no del batec.

## Quan tindràs una resposta

Un efecte de 5-10 ms amb 6 sessions per versió **no es veu**. Calen setmanes
(20-40 sessions). Al principi l'aplicació t'ho recordarà.

## Estructura

```
n1-calibratge/
├── n1-calibratge.html      ← l'aplicació (un sol fitxer, sense dependències)
├── LLEGIU-ME.md            ← el mateix resum, en text
└── README.md               ← aquest fitxer
```

Les proves són a la RPi, a `~/neurowave/n1/` (`test_stats.js`, `test_app2.js`).
Cal `jsdom`. Van juntes perquè depenen de la versió del fitxer.

## Estendre'l a altres coses

Un cop el mètode funciona, hi pots posar **qualsevol cosa**: respirar 4-7-8
abans de la feina, el cafè, l'hora del dia, els 10 minuts de guitarra. La
màquina no és per a l'àudio — és per esbrinar què et funciona a tu.

Per fer-ho, canvia els dos braços a `ARMS` (nom i batec) i deixa'ls cecs.

## Límits

- **Mesura relativa, no absoluta.** El número absolut no és comparable amb cap
  aparell de laboratori. El que val és la diferència entre els dos braços en el
  **teu mateix ordinador**.
- **No és cap eina mèdica.** No diagnostica res ni substitueix ningú. És un
  experiment sobre tu, per a tu.
- **No s'ha de fer servir amb antecedents d'epilèpsia o convulsions.**
