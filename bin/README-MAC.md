# BernatLab - Scripts per a Mac

Aquesta carpeta conte scripts per accedir rapidament als recursos del BernatLab des del **Mac**.

## Fitxers disponibles

| Script | Sistema | Us |
|---|---|---|
| `bernatlab-web-mac.sh` | **Mac (recomanat)** | Menu grafic complet amb 10 URLs |
| `bernatlab-web.sh` | Linux / Mac basic | Obre 3 URLs principals (antic) |
| `bernatlab-web.bat` | Windows CMD | Obre 3 URLs (antic) |
| `bernatlab-web.ps1` | Windows PowerShell | Menu complet amb icones |
| `bernatlab-menu-directe.bat` | Windows | Wrapper per llancar el .ps1 |

## Recomanacio per a Mac

**Usa `bernatlab-web-mac.sh`** - es el mes complet.

### Primer us: instal·lacio

1. **Descarrega el fitxer** a la teva carpeta de projectes (o on vulguis):
   ```bash
   cd ~/Documents
   curl -O https://raw.githubusercontent.com/BernatMora/bernatlab/main/bin/bernatlab-web-mac.sh
   ```

2. **Fes-lo executable**:
   ```bash
   chmod +x bernatlab-web-mac.sh
   ```

3. **Executa'l**:
   ```bash
   ./bernatlab-web-mac.sh
   ```

### Us habitual

```bash
# Obrir el menu
./bernatlab-web-mac.sh

# Obrir totes les URLs de cop
./bernatlab-web-mac.sh all

# Obrir nomes les de l'Hort Osona
./bernatlab-web-mac.sh hort
```

### Afegir al PATH (opcional)

Per poder executar-lo des de qualsevol lloc:

1. Copia'l a una carpeta que ja esta al PATH:
   ```bash
   cp bernatlab-web-mac.sh /usr/local/bin/bernatlab
   chmod +x /usr/local/bin/bernatlab
   ```

2. Ara pots executar-lo des de qualsevol lloc:
   ```bash
   bernatlab
   bernatlab all
   bernatlab hort
   ```

### Crear un acces directe a l'escriptori (opcional)

1. Obre **Automator** (cerca'l amb Spotlight: `Cmd+Espai`)
2. Selecciona **"Application"**
3. Busca **"Run Shell Script"**
4. Escriu:
   ```bash
   /path/to/bernatlab-web-mac.sh
   ```
5. Guarda com a "BernatLab.app" a l'escriptori

Ara tens una icona a l'escriptori que obre el menu quan fas doble clic.

## Caracteristiques del menu

- 10 URLs organitzades per categoria
- Icones per a cada recurs
- Colors al terminal
- Deteccion automatica de macOS / Linux / Windows
- Modes especials: `all` (obert tot) i `hort` (nomes Hort Osona)

## URLs disponibles

| # | Nom | Categoria |
|---|---|---|
| 1 | Curs practic | Documentacio |
| 2 | Guia eines M8 | Documentacio |
| 3 | Web publica BernatLab | Projecte |
| 4 | Web publica Hort Osona | Projecte |
| 5 | Repo BernatLab | GitHub |
| 6 | Repo Hort Osona | GitHub |
| 7 | PROJECT_STATE | Documentacio |
| 8 | Handoff sessio 2026-07-17 | Documentacio |
| 9 | Glossari | Documentacio |
| 10 | Guia primer dia RPi | Documentacio |

## Solucio de problemes

### Si dona error "Permission denied"

```bash
chmod +x bernatlab-web-mac.sh
```

### Si l'ordre `open` no funciona

Assegura't que estas a macOS, no a Linux. Prova:
```bash
which open
# Ha de retornar: /usr/bin/open
```

### Si vols afegir mes URLs

Edita el fitxer i afegeix una linia a la seccio `URLS`:
```bash
URLS[11_nom]="El meu nou recurs"
URLS[11_url]="https://example.com"
```

Despres actualitza el bucle `for i in {1..10}` per incloure `11`.

## Personalitzacio

Si vols canviar les URLs per defecte, edita les linies que comencen amb `URLS[N_url]=` al principi de l'script.
