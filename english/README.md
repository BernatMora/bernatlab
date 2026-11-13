# English Step

Web per practicar vocabulari anglès cada dia, pensada per a l'iPhone. C1 per defecte; C2 per posar-s'hi a prova, B2+ per refrescar i B2 opcional. 64 expressions inicials amb definició en anglès, significat en català i frase d'exemple.

## Cinc modes de pràctica

Targetes, test de significat, escolta i escriu, construcció de frases i parelles. L'àudio fa servir la veu anglesa del dispositiu (text-to-speech). El progrés es desa al `localStorage` del navegador; no se sincronitza entre dispositius.

Repàs espaiat: les respostes correctes tornen al cap d'1, 3, 7, 14 i 30 dies; les fallades tornen abans. "Recordada" vol dir dues respostes correctes seguides.

## Publicació

Forma part del BernatLab i es publica amb el GitHub Pages del repositori a `/english/`. A l'iPhone: obrir-la a Safari → Compartir → Afegir a la pantalla d'inici.

## Desenvolupament local

Sense dependències ni compilació:

```bash
python -m http.server --directory english 8000
```

- Vocabulari: `content.js`
- Interacció: `app.js`
- Disseny: `style.css`

Provat en navegador d'escriptori. Falta verificar-ho en un iPhone real (sobretot l'àudio de Safari).
