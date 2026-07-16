# Exercici practic - M8 Cap 4: PowerToys Run

> 20-30 min - Al teu Windows

## Objectiu

Instal·lar PowerToys Run, configurar-lo, i usar-lo per accedir rapidament a les teves eines.

## Requisits

- Windows 10 o 11
- 5 min per descarregar
- 15 min per configurar

## Pas 1: Descarregar i instal·lar (5 min)

Opcio A (winget):
```powershell
winget install Microsoft.PowerToys
```

Opcio B (manual):
1. Vés a https://learn.microsoft.com/en-us/windows/powertoys/
2. Click a **Install now**
3. Executa l'instal·lador

## Pas 2: Obrir PowerToys Run (1 min)

1. PowerToys sha d'estar corrent a la safata del sistema
2. Prems **Alt+Space**
3. Hauria d'apareixer una barra de cerca al centre

## Pas 3: Provar aplicacions (5 min)

Escriu:
- `chrome` o `firefox` - obre el navegador
- `code` - obre VS Code
- `terminal` - obre Windows Terminal
- `calc` - obre la Calculadora
- `notepad` - obre el Bloc de notes

## Pas 4: Calcular (2 min)

Prems Alt+Space i escriu:
- `5*9` -> 45
- `sqrt(144)` -> 12
- `100/4` -> 25

## Pas 5: Cercar fitxers (3 min)

Escriu el nom d'un fitxer que existeixi al teu PC (per exemple, `README` o `index.html`).

PowerToys Run el trobara i el podràs obrir.

## Pas 6: Executar ordres shell (5 min)

Escriu:
- `> ipconfig` - mostra la teva IP
- `> tasklist` - llista processos
- `> ssh hortosona` - connecta a la RPi (si tens el perfil)

## Pas 7: Configurar dreceres personalitzades (5 min)

A Settings > PowerToys Run:
- Canvia la tecla d'acces si vols (per defecte Alt+Space).
- Ajusta la posicio (per defecte centre).
- Activa plugins si vols mes funcions.

## Validacio

Has acabat si:
- [ ] PowerToys instal·lat
- [ ] Alt+Space obre el llançador
- [ ] Pots obrir aplicacions
- [ ] La calculadora funciona
- [ ] Has executat una ordre shell
- [ ] Has configurat dreceres

## Per aprofundir

- Instal·la el plugin **Window Walker** per navegar finestres obertes.
- Activa **Web Search** per cercar a Internet directament.
- Crea dreceres personalitzades per al teu flux de treball.
