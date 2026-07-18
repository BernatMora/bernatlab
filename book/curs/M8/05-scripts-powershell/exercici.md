# Exercici practic - M8 Cap 5: Scripts d'alies PowerShell

> 20-30 min - Al teu Windows

## Objectiu

Crear un fitxer de funcions PowerShell amb alies per accedir rapidament al BernatLab.

## Requisits

- Windows amb PowerShell
- Tailscale actiu
- 20-30 min

## Pas 1: Crear el directori bin (2 min)

```powershell
mkdir C:\Users\usuari\bin -Force
```

Aquesta carpeta sera el teu "directori d'eines personals".

## Pas 2: Crear el fitxer bernatlab.ps1 (10 min)

```powershell
notepad C:\Users\usuari\bin\bernatlab.ps1
```

Copia tot el contingut del resum i desa.

## Pas 3: Crear el $PROFILE (5 min)

```powershell
# Comprovar si existeix
Test-Path $PROFILE

# Si no existeix, crear-lo
if (!(Test-Path $PROFILE)) {
    New-Item -Path $PROFILE -ItemType File -Force
}

# Afegir el dot-source
Add-Content $PROFILE "`n. C:\Users\usuari\bin\bernatlab.ps1"
```

## Pas 4: Recarregar el perfil (2 min)

Tanca i obre PowerShell. O:

```powershell
. $PROFILE
```

## Pas 5: Provar els alies (5 min)

```powershell
# Provar un alies
kuma
# Hauria d'obrir Uptime Kuma al navegador

# Provar-ne un altre
portainer
# Hauria d'obrir Portainer

# Provar SSH
sshbl
# Hauria de connectar a la RPi (sense password, gracies al capitol 1)
```

## Pas 6: Verificar que el perfil es carrega sempre (3 min)

Tanca PowerShell, obre una finestra nova, i escriu:

```powershell
Get-Alias kuma
# Hauria de mostrar: Alias kuma -> bl-kuma
```

Si funciona, el perfil es carrega correctament.

## Validacio

Has acabat si:
- [ ] El fitxer bernatlab.ps1 existeix
- [ ] El $PROFILE existeix i conte el dot-source
- [ ] Els alies funcionen
- [ ] `sshbl` connecta sense password
- [ ] Els serveis web s'obren al navegador

## Per aprofundir

- Afegeix funcions per fer deploys o backups.
- Sincronitza el fitxer amb Git per usar a altres PCs.
- Crea funcions amb parametres (per exemple, `bl-logs -name X`).
