# Validar i pujar els canvis des del Mac

## Quan arribis a casa, obre el Terminal del Mac i fes:

### 1. Comprova si tens el repo

```bash
ls ~/Documents/ 2>/dev/null
ls ~/Desktop/ 2>/dev/null
ls ~/Projects/ 2>/dev/null
ls ~/repos/ 2>/dev/null
```

Veuràs si tens una carpeta anomenada "bernatlab" o similar en algun lloc.

### 2. Si el tens, ves al directori

```bash
cd ~/Documents/bernatlab
# o
cd ~/Projects/bernatlab
# o on sigui que el tinguis
```

### 3. Comprova l'estat

```bash
git status
```

Si tens canvis sense commit, veuras una llista.
Si esta net, veuras "nothing to commit, working tree clean".

### 4. Mira els ultims commits

```bash
git log --oneline -10
```

Aixo et dira quins commits tens localment.

### 5. Comprova si hi ha canvis no pujats

```bash
git status
```

Si veus "Your branch is ahead of 'origin/main' by X commits", tens commits
per pujar.

## Si NO tens el repo al Mac, cal clonar-lo

```bash
# Des de qualsevol directori
cd ~/Documents
git clone https://github.com/BernatMora/bernatlab.git
cd bernatlab

# Despres copia aqui els canvis que vas fer
```

## Si els canvis son a fitxers solts (no al repo)

Tens varies opcions:

### Opcio A: Copiar els fitxers al repo i fer commit

1. Clona el repo (si no el tens)
2. Copia els fitxers modificats al lloc correcte:
   ```bash
   cp /ronda/als/fitxers/canviats/* ~/Documents/bernatlab/
   ```
3. Comprova quins canvis hi ha amb `git status`
4. Fes commit i push:
   ```bash
   git add .
   git commit -m "Descripcio dels canvis"
   git push origin main
   ```

### Opcio B: Enviarmels a mi per correu/Telegram

Si els canvis son petits, pots:
- Adjuntar els fitxers al correu
- Enviar-me'ls per Telegram
- I jo els integro al repo

## Que necessito saber

Quan estiguis a casa i hagis fet les comprovacions, enviem:

1. **On tens el repo** (o si no el tens)
2. **Quins canvis tens** (`git status`)
3. **Quins commits nous** tens (`git log`)
4. **Quins fitxers has modificat** (noms)

I llavors podem decidir entre:
- Tu puges els canvis i m'ho dius per validarlos
- M'envies els fitxers i jo els pujo
- Em dius que fer i t'ajudo pas a pas

## Mentrestant, puc fer coses

Si vols que prepari alguna cosa per quan arribis:

1. **Crear un script de validacio** que compari el que tens al Mac amb el que hi ha a GitHub
2. **Preparar les instruccions detallades** per pujar canvis
3. **Fer canvis jo des daqui** (pero no veig res per fer perque no veig els teus canvis)

Què prefereixes?
