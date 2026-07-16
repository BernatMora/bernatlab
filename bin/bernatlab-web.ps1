# ==========================================================
# BernatLab - Acces rapid als recursos (versio completa)
# ==========================================================
# Obre URLs al navegador per defecte amb un menu interactiu
# - Curs practic
# - Guia eines M8
# - Web publica del BernatLab
# - Hort Osona
# - Repo BernatLab
# - Repo Hort Osona
# - Totes les URLs de cop
# ==========================================================

# URLs
$URLs = [ordered]@{
    "1" = @{
        Nom = "Curs practic"
        URL = "https://bernatmora.github.io/bernatlab/book/curs/"
        Desc = "El curs amb tots els capitols, quiz i exercicis"
    }
    "2" = @{
        Nom = "Guia eines M8"
        URL = "https://github.com/BernatMora/bernatlab/blob/main/book/curs/recursos/eines-m8-pas-a-pas.md"
        Desc = "Document pas a pas per configurar SSH, MobaXterm, etc."
    }
    "3" = @{
        Nom = "Web publica BernatLab"
        URL = "https://bernatmora.github.io/bernatlab/"
        Desc = "La portada del projecte BernatLab"
    }
    "4" = @{
        Nom = "Web publica Hort Osona"
        URL = "https://bernatmora.github.io/hort-osona/"
        Desc = "El projecte public de l'hort amb sensors i dades"
    }
    "5" = @{
        Nom = "Repo BernatLab (GitHub)"
        URL = "https://github.com/BernatMora/bernatlab"
        Desc = "El codi font del BernatLab"
    }
    "6" = @{
        Nom = "Repo Hort Osona (GitHub)"
        URL = "https://github.com/BernatMora/hort-osona"
        Desc = "El codi font d'Hort Osona"
    }
    "0" = @{
        Nom = "Obrir TOTES les URLs"
        URL = "ALL"
        Desc = "Obre les 6 finestres alhora"
    }
}

# Funcio per obrir una URL al navegador per defecte
function Obrir-URL {
    param([string]$Url)
    try {
        Start-Process $Url
        Write-Host "  Oberta: $Url" -ForegroundColor Green
    }
    catch {
        Write-Host "  Error obrint: $Url" -ForegroundColor Red
        Write-Host "  $_" -ForegroundColor Red
    }
}

# Funcio per mostrar el menu
function Mostrar-Menu {
    Clear-Host
    Write-Host ""
    Write-Host "============================================" -ForegroundColor Cyan
    Write-Host "  BernatLab - Acces rapid als recursos" -ForegroundColor Cyan
    Write-Host "============================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Tria quina URL vols obrir:" -ForegroundColor White
    Write-Host ""

    foreach ($key in $URLs.Keys | Sort-Object) {
        $item = $URLs[$key]
        Write-Host "  [$key] " -NoNewline -ForegroundColor Yellow
        Write-Host "$($item.Nom)" -NoNewline -ForegroundColor White
        Write-Host " - $($item.Desc)" -ForegroundColor Gray
    }

    Write-Host ""
    Write-Host "  [S] Sortir" -ForegroundColor Yellow
    Write-Host ""
    $opcio = Read-Host "Opcio"
    return $opcio
}

# Bucle principal
$sortir = $false
while (-not $sortir) {
    $opcio = Mostrar-Menu

    if ($opcio -eq "S" -or $opcio -eq "s") {
        $sortir = $true
        Write-Host ""
        Write-Host "Fins aviat!" -ForegroundColor Cyan
        break
    }

    if ($URLs.Contains($opcio)) {
        $item = $URLs[$opcio]
        Write-Host ""
        if ($item.URL -eq "ALL") {
            Write-Host "Obrint TOTES les URLs..." -ForegroundColor Yellow
            Write-Host ""
            foreach ($key in ($URLs.Keys | Where-Object { $_ -ne "0" })) {
                $u = $URLs[$key].URL
                Write-Host "[$key] " -NoNewline -ForegroundColor Yellow
                Obrir-URL $u
                Start-Sleep -Seconds 1
            }
        }
        else {
            Write-Host "Obrint: $($item.Nom)..." -ForegroundColor Yellow
            Write-Host ""
            Obrir-URL $item.URL
        }
        Write-Host ""
        Write-Host "Fet!" -ForegroundColor Green
        Write-Host ""
        Read-Host "Prem ENTER per tornar al menu (o Ctrl+C per sortir)"
    }
    else {
        Write-Host ""
        Write-Host "Opcio no valida: '$opcio'" -ForegroundColor Red
        Start-Sleep -Seconds 2
    }
}
