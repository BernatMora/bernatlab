# Exercici practic - Capitol 9: Calendari de sembra

> 30-45 min - Aplicat al teu Hort Osona

## Objectiu

Crear el calendari de sembra del teu hort per la propera temporada.

## Pas 1: Inventari de cultius (5 min)

Llista els 10-15 cultius que vols fer. Exemples:
- Tomàquet, pebrot, albergínia, carbassa, cogombre, mongeta, pèsol, enciam, bleda, pastanaga, rave, col, espinac, all, ceba.

## Pas 2: Definir les dates de sembra (10 min)

Per a cada cultiu, busca:
- **Data de sembra en hivernacle** (si la vols avançar)
- **Data de trasplantament** (si conreen a partir de planter)
- **Data de sembra directa** (a terra)
- **Data de collita esperada**

Fonts:
- Calendari Osona (Ruralcat, Infojardín)
- Experiència pròpia
- Llocs locals (pagesos de la zona)

## Pas 3: Crear el fitxer del calendari (10 min)

Crea un fitxer `calendari-sembra-2026.md` amb la informacio estructurada. Exemple:

| Cultiu | Sembra hivernacle | Trasplantament | Sembra directa | Collita |
|---|---|---|---|---|
| Tomàquet | Març | Maig | - | Juliol-Octubre |
| Enciam | Febrer | Abril | Agost | Maig-Novembre |
| Mongeta | - | - | Abril-Maig | Juny-Setembre |

## Pas 4: Validar amb l'hort real (10 min)

Mira el que tens plantat ara. Compara amb el calendari. Ajusta dates.

## Pas 5: Documentar-ho al repo (5 min)

```bash
cd ~/bernatlab/projects/hort-osona
cp ~/calendari-sembra-2026.md plans-mensuals/
git add plans-mensuals/calendari-sembra-2026.md
git commit -m "Afegeix calendari de sembra 2026"
git push
```

## Validacio

Has acabat si:
- [ ] Tens una llista de 10-15 cultius
- [ ] Totes les dates estan definides
- [ ] Has validat amb l'hort real
- [ ] El fitxer esta al repo
