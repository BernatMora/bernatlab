# Scripts del BernatLab

Aquesta carpeta conté scripts per accedir rapidament als recursos del BernatLab.

## Fitxers disponibles

| Script | Sistema | Us |
|---|---|---|
| `bernatlab-web.bat` | Windows (CMD/PowerShell) | Obre les 3 URLs principals sense menu |
| `bernatlab-web-menu.bat` | Windows (CMD) | Llança el menu PowerShell |
| `bernatlab-web.ps1` | Windows (PowerShell) | **Menu interactiu complet** amb 6 URLs |
| `bernatlab-web.sh` | Linux / Mac / Git Bash | Obre les 3 URLs principals sense menu |

## Recomanacio

**PowerShell** (millor opcio per a Windows):
```powershell
cd C:\Users\iadmin\bernatlab\bin
.\bernatlab-web.ps1
```

Mostra un menu amb totes les opcions:
1. Curs practic
2. Guia eines M8
3. Web publica BernatLab
4. Web publica Hort Osona
5. Repo BernatLab (GitHub)
6. Repo Hort Osona (GitHub)
0. Obrir TOTES les URLs
S. Sortir

## Notes

- Si PowerShell bloqueja l'execucio del .ps1, executa primer:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

- Si vols afegir mes URLs, edita el fitxer `.ps1` i afegeix-les al hash `$URLs`.

- Si vols crear una versio `.bat` amb menu, pots fer-ho pero sera mes limitat.
