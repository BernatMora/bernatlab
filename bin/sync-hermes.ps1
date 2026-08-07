# Sincronitza Hermes entre Windows i Mac via iCloud
# Us:
#   .\sync-hermes.ps1 -Direction push   # Copia del Windows al iCloud
#   .\sync-hermes.ps1 -Direction pull   # Copia del iCloud al Windows (mode lectura)

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet('push', 'pull')]
    [string]$Direction
)

$hermesDir = "$env:LOCALAPPDATA\hermes"
$icloudDir = "$env:USERPROFILE\iCloudDrive\hermes"

# Crear la carpeta iCloud si no existeix
if (!(Test-Path $icloudDir)) {
    New-Item -ItemType Directory -Path $icloudDir -Force | Out-Null
    Write-Host "[OK] Creat directori iCloud: $icloudDir" -ForegroundColor Cyan
}

function Show-Header {
    Write-Host ""
    Write-Host "================================================" -ForegroundColor Cyan
    Write-Host "  Hermes Sync - Windows <-> iCloud" -ForegroundColor Cyan
    Write-Host "================================================" -ForegroundColor Cyan
    Write-Host ""
}

function Push-To-Cloud {
    Show-Header
    Write-Host "[PUSH] Copiant del Windows al iCloud..." -ForegroundColor Yellow
    Write-Host ""

    $filesToSync = @(
        @{ Name = "state.db"; Size = "(gran)" },
        @{ Name = "config.yaml"; Size = "(petit)" },
        @{ Name = "projects.db"; Size = "(gran)" },
        @{ Name = "kanban.db"; Size = "(gran)" },
        @{ Name = "auth.json"; Size = "(secret - no sincronitzar)" }
    )

    $synced = 0
    $skipped = 0

    foreach ($f in $filesToSync) {
        $name = $f.Name
        $src = Join-Path $hermesDir $name
        $dst = Join-Path $icloudDir $name

        if (!(Test-Path $src)) {
            Write-Host "  [SKIP] $name no existeix al Windows" -ForegroundColor DarkGray
            $skipped++
            continue
        }

        # Saltar auth.json (secret)
        if ($name -eq "auth.json") {
            Write-Host "  [SKIP] $name es secret - no es sincronitza" -ForegroundColor DarkYellow
            $skipped++
            continue
        }

        $size = (Get-Item $src).Length
        $sizeMB = [math]::Round($size / 1MB, 2)

        try {
            Copy-Item $src $dst -Force
            Write-Host "  [OK] $name ($sizeMB MB)" -ForegroundColor Green
            $synced++
        }
        catch {
            Write-Host "  [ERR] $name : $_" -ForegroundColor Red
        }
    }

    # Sincronitzar tambe memories i skills (són petits i utils)
    $dirsToSync = @("memories", "skills")

    foreach ($dir in $dirsToSync) {
        $src = Join-Path $hermesDir $dir
        $dst = Join-Path $icloudDir $dir

        if (!(Test-Path $src)) {
            Write-Host "  [SKIP] $dir/ no existeix" -ForegroundColor DarkGray
            continue
        }

        try {
            Copy-Item $src $dst -Recurse -Force
            $count = (Get-ChildItem $src -Recurse -File).Count
            Write-Host "  [OK] $dir/ ($count fitxers)" -ForegroundColor Green
            $synced++
        }
        catch {
            Write-Host "  [ERR] $dir/ : $_" -ForegroundColor Red
        }
    }

    Write-Host ""
    Write-Host "================================================" -ForegroundColor Cyan
    Write-Host "  Sincronitzats: $synced | Saltats: $skipped" -ForegroundColor Cyan
    Write-Host "================================================" -ForegroundColor Cyan
    Write-Host ""
}

function Pull-From-Cloud {
    Show-Header
    Write-Host "[PULL] Copiant del iCloud al Windows..." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "ATENCIO: Aixo sobreescriura el teu state.db!" -ForegroundColor Red
    Write-Host ""

    $confirm = Read-Host "Continuar? (s/n)"
    if ($confirm -ne "s") {
        Write-Host "Cancelat." -ForegroundColor Yellow
        return
    }

    # Primer fer backup del que tenim
    $backupDir = Join-Path $hermesDir "backups\pre-pull-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
    New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
    Write-Host "[BACKUP] Fent backup a $backupDir..." -ForegroundColor Cyan
    Copy-Item "$hermesDir\state.db" "$backupDir\state.db" -Force

    # Despres copiar
    $src = Join-Path $icloudDir "state.db"
    $dst = Join-Path $hermesDir "state.db"

    if (!(Test-Path $src)) {
        Write-Host "[ERR] No sha trobat state.db al iCloud" -ForegroundColor Red
        return
    }

    Copy-Item $src $dst -Force
    $size = (Get-Item $dst).Length
    $sizeMB = [math]::Round($size / 1MB, 2)

    Write-Host ""
    Write-Host "================================================" -ForegroundColor Cyan
    Write-Host "  state.db importat ($sizeMB MB)" -ForegroundColor Green
    Write-Host "================================================" -ForegroundColor Cyan
    Write-Host ""
}

# Main
switch ($Direction) {
    "push" { Push-To-Cloud }
    "pull" { Pull-From-Cloud }
}
