# English Step

Web per practicar vocabulari anglès cada dia, pensada per a l'iPhone. C1 per defecte; C2 per posar-s'hi a prova, B2+ per refrescar i B2 opcional. 184 expressions amb definició en anglès, significat en català i frase d'exemple, en vuit temes: Engineering, Music, Health, Gardening, AI, Work, Technology i Everyday.

## Cinc modes de pràctica

Targetes, test de significat, escolta i escriu, construcció de frases i parelles. L'àudio fa servir la veu anglesa del dispositiu (text-to-speech). El progrés es desa al `localStorage` del navegador; no se sincronitza entre dispositius, però es pot exportar i importar com a fitxer JSON des de "View progress".

Repàs espaiat: les respostes correctes tornen al cap d'1, 3, 7, 14 i 30 dies; les fallades tornen 3 targetes més endavant dins la mateixa tanda. "Recordada" vol dir dues respostes correctes seguides.

## Publicació

Forma part del BernatLab i es publica amb el GitHub Pages del repositori a `/english/`. A l'iPhone: obrir-la a Safari → Compartir → Afegir a la pantalla d'inici.

## Afegir paraules o temes

A `content.js`, afegeix files al final del nivell que toqui (B2, B2+, C1, C2) amb el format:

```js
["paraula","traducció catalana","definició en anglès","Frase d'exemple.","Tema"]
```

No insereixis files al mig ni n'esborris: l'identificador de cada targeta (i el progrés desat) depèn de la seva posició. El desplegable de temes es genera sol. Després, puja el número de `CACHE` a `sw.js` (p. ex. `english-step-v3`) perquè els mòbils rebin la versió nova.

## Sense connexió

`sw.js` desa l'app al mòbil després de la primera visita. Quan hi ha xarxa sempre baixa la versió més nova; sense cobertura fa servir la còpia desada.

## Desenvolupament local

Sense dependències ni compilació:

```bash
python -m http.server --directory english 8000
```

- Vocabulari: `content.js`
- Interacció: `app.js`
- Disseny: `style.css`

Provat en navegador d'escriptori. Falta verificar-ho en un iPhone real (sobretot l'àudio de Safari).
