# Resum - M8 Cap 4: PowerToys Run

## Per que importa

Cada vegada que vols obrir una eina, has de:
1. Buscar-la al menu Inici.
2. Click. Esperar.
3. Obrir-la.

O pitjor: obrir PowerShell i teclejar la ruta completa.

**PowerToys Run** es com el **Spotlight del Mac** pero per Windows. Prems `Alt+Space`, escrius el que busques, i apareixen resultats. Es **rapidissim**.

## Que es PowerToys

PowerToys es un conjunt d'utilitats de Microsoft per a Windows. Inclou:
- **PowerToys Run** - Llançador d'aplicacions (el que ens interessa).
- **FancyZones** - Gestor de finestres.
- **PowerRename** - Renombrar fitxers en massa.
- **Color Picker** - Triar colors a la pantalla.
- **Keyboard Manager** - Remapejar tecles.

Tots son **gratuïts** i **open source**.

## Instal·lacio

1. Vés a https://learn.microsoft.com/en-us/windows/powertoys/
2. Click a **Install**.
3. O `winget install Microsoft.PowerToys`.
4. S'inicia automaticament.

## Us de PowerToys Run

Prems **`Alt+Space`** (configurable) i apareix una barra de cerca al centre de la pantalla.

Pots buscar:
- **Aplicacions**: escriu "chrome", "firefox", "code", "terminal", etc.
- **Fitxers**: escriu el nom (cerca a `C:\Users\<usuari>`).
- **Calculadora**: escriu "5*9" o "sqrt(144)".
- **Comandes shell**: prefix `>` per executar ordres.
- **URLs**: escriu "github.com" per obrir al navegador.
- **Finestres obertes**: si ja tens Chrome obert, escriu "chrome" i el porta al davant.

## Per a l'homelab

Configura els teus acces directe preferits:

1. Obre PowerToys Run.
2. Click a la icona d'engranatge.
3. A la pestanya **PowerToys Run**, configura el que vulguis.
4. Pots afegir **plugins** o dreceres personalitzades.

Exemples utils:
- `hortosona` -> ssh bernat@100.x.y.z
- `portainer` -> obre https://100.x.y.z:9443
- `kuma` -> obre http://100.x.y.z:3001
- `homepage` -> obre http://100.x.y.z:3000

Per a URL, pots crear dreceres personalitzades o simplement escriure-les.

## Avantatges

- **Velocitat** - 10x mes rapid que el menu Inici.
- **Calculadora** - 5*9=45 sense obrir res.
- **Cerca unificada** - Un sol lloc per a tot.
- **Gratis** - 100% open source.

## Connexions

- **M8 cap 5** - Scripts d'alies al PowerShell son complementaris.
- **M8 cap 2** - MobaXterm tambe te un llançador intern.

## Errors habituals

- **Conflite amb altres aplicacions** - Si tens Visual Studio Code, pot tenir el seu propi llançador (`Ctrl+P`). PowerToys Run es `Alt+Space` per defecte.
- **No troba aplicacions noves** - Cal reiniciar PowerToys Run.
- **Indexacio lenta al principi** - Els primers minuts pot trigar a indexar els fitxers.
