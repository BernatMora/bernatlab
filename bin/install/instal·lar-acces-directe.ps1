# Crea un acces directe a l'escriptori del Windows
# que obre el menu del BernatLab

$ErrorActionPreference = "Stop"

# Parametres
$targetPath = "C:\Users\iadmin\bernatlab\bin\bernatlab-menu-directe.bat"
$shortcutPath = [Environment]::GetFolderPath("Desktop") + "\BernatLab.lnk"
$iconPath = "C:\Windows\System32\shell32.dll"
$iconIndex = 12  # Icona de "settings" o "tools" - provar

# Verificar que el .bat existeix
if (-not (Test-Path $targetPath)) {
    Write-Host "ERROR: No trobo el fitxer: $targetPath" -ForegroundColor Red
    Write-Host "Comprova que el BernatLab esta instal·lat correctament." -ForegroundColor Yellow
    pause
    exit 1
}

# Crear l'acces directe
try {
    $WshShell = New-Object -ComObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut($shortcutPath)
    $Shortcut.TargetPath = $targetPath
    $Shortcut.WorkingDirectory = "C:\Users\iadmin\bernatlab\bin"
    $Shortcut.IconLocation = "$iconPath,$iconIndex"
    $Shortcut.Description = "Menu del BernatLab - Acces rapid als recursos"
    $Shortcut.WindowStyle = 1  # Normal
    $Shortcut.Save()

    Write-Host ""
    Write-Host "  [OK] Acces directe creat!" -ForegroundColor Green
    Write-Host ""
    Write-Host "  Ubicacio: $shortcutPath" -ForegroundColor Cyan
    Write-Host "  Objectiu: $targetPath" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  Fes doble clic a l'acces directe per obrir el menu." -ForegroundColor White
    Write-Host ""
}
catch {
    Write-Host ""
    Write-Host "  [ERROR] No s'ha pogut crear l'acces directe" -ForegroundColor Red
    Write-Host "  $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "  Pots crear-lo manualment:" -ForegroundColor Yellow
    Write-Host "  1. Click dret a l'escriptori" -ForegroundColor Yellow
    Write-Host "  2. Nou > Acces directe" -ForegroundColor Yellow
    Write-Host "  3. Ubicacio: $targetPath" -ForegroundColor Yellow
    Write-Host ""
}

# Esperar que l'usuari llegeixi
Write-Host "Prem una tecla per continuar..." -ForegroundColor DarkGray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
