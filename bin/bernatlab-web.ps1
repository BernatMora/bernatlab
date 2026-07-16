# ==========================================================
# BernatLab - Acces rapid als recursos (versio amb icones)
# ==========================================================
# Menu visual amb icones Unicode/emoji per una experiencia
# mes intuïtiva. Inclou 6 URLs + opcio obrir tot.
# ==========================================================

# Configurar colors i ample de la consola
$Host.UI.RawUI.WindowTitle = "BernatLab - Menu de recursos"

# URLs amb icones
$URLs = [ordered]@{
    "1" = @{
        Icona   = "[📚]"
        Nom     = "Curs practic"
        URL     = "https://bernatmora.github.io/bernatlab/book/curs/"
        Desc    = "Tots els capitols, quiz i exercicis"
        Color   = "Cyan"
    }
    "2" = @{
        Icona   = "[🛠️]"
        Nom     = "Guia eines M8"
        URL     = "https://github.com/BernatMora/bernatlab/blob/main/book/curs/recursos/eines-m8-pas-a-pas.md"
        Desc    = "Configurar SSH, MobaXterm, perfil, etc."
        Color   = "Yellow"
    }
    "3" = @{
        Icona   = "[🌱]"
        Nom     = "Web publica BernatLab"
        URL     = "https://bernatmora.github.io/bernatlab/"
        Desc    = "La portada del projecte"
        Color   = "Green"
    }
    "4" = @{
        Icona   = "[🌿]"
        Nom     = "Web publica Hort Osona"
        URL     = "https://bernatmora.github.io/hort-osona/"
        Desc    = "El projecte public de l'hort amb sensors"
        Color   = "Magenta"
    }
    "5" = @{
        Icona   = "[💻]"
        Nom     = "Repo BernatLab (GitHub)"
        URL     = "https://github.com/BernatMora/bernatlab"
        Desc    = "El codi font del BernatLab"
        Color   = "Blue"
    }
    "6" = @{
        Icona   = "[🌾]"
        Nom     = "Repo Hort Osona (GitHub)"
        URL     = "https://github.com/BernatMora/hort-osona"
        Desc    = "El codi font d'Hort Osona"
        Color   = "DarkGreen"
    }
    "0" = @{
        Icona   = "[⚡]"
        Nom     = "OBRIR TOTES LES URLs"
        URL     = "ALL"
        Desc    = "Obre les 6 finestres alhora"
        Color   = "Red"
    }
}

# Funció per obrir una URL
function Obrir-URL {
    param([string]$Url, [string]$Nom)
    try {
        Start-Process $Url
        Write-Host "  [OK] " -NoNewline -ForegroundColor Green
        Write-Host "$Nom" -NoNewline -ForegroundColor White
        Write-Host " - Oberta al navegador" -ForegroundColor Gray
    }
    catch {
        Write-Host "  [ERROR] " -NoNewline -ForegroundColor Red
        Write-Host "$Nom" -NoNewline -ForegroundColor White
        Write-Host " - $_" -ForegroundColor Red
    }
}

# Funció per dibuixar la capçalera
function Mostrar-Capcalera {
    Clear-Host
    Write-Host ""
    Write-Host "  ╔══════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "  ║                                              ║" -ForegroundColor Cyan
    Write-Host "  ║   🌱  B E R N A T L A B  ·  M E N U  🌱   ║" -ForegroundColor Cyan
    Write-Host "  ║                                              ║" -ForegroundColor Cyan
    Write-Host "  ║   Servidor personal · Raspberry Pi · Docker  ║" -ForegroundColor DarkCyan
    Write-Host "  ║   Tailscale · IA · LoRa · Hort Osona         ║" -ForegroundColor DarkCyan
    Write-Host "  ║                                              ║" -ForegroundColor Cyan
    Write-Host "  ╚══════════════════════════════════════════════╝" -ForegroundColor Cyan
    Write-Host ""
}

# Funció per mostrar el menu amb icones
function Mostrar-Menu {
    Mostrar-Capcalera

    Write-Host "  ┌────────────────────────────────────────────┐" -ForegroundColor DarkGray
    Write-Host "  │  Recursos disponibles                      │" -ForegroundColor White
    Write-Host "  └────────────────────────────────────────────┘" -ForegroundColor DarkGray
    Write-Host ""

    foreach ($key in ($URLs.Keys | Sort-Object)) {
        $item = $URLs[$key]
        Write-Host "  " -NoNewline
        Write-Host "$($item.Icona) " -NoNewline
        Write-Host "[$key] " -NoNewline -ForegroundColor $item.Color
        Write-Host "$($item.Nom)" -NoNewline -ForegroundColor White
        Write-Host "  " -NoNewline
        Write-Host "$($item.Desc)" -ForegroundColor DarkGray
    }

    Write-Host ""
    Write-Host "  ────────────────────────────────────────────────" -ForegroundColor DarkGray
    Write-Host "  [S] " -NoNewline -ForegroundColor Yellow
    Write-Host "Sortir del menu" -ForegroundColor White
    Write-Host "  ────────────────────────────────────────────────" -ForegroundColor DarkGray
    Write-Host ""
}

# Funció per mostrar una animacio quan s'obre
function Animar-Obrint {
    param([string]$Missatge)
    Write-Host ""
    Write-Host "  ⏳ Obrint: " -NoNewline -ForegroundColor Yellow
    Write-Host "$Missatge" -ForegroundColor White
    Write-Host ""
    # Mini animacio de 3 frames
    $frames = @("[◐]", "[◓]", "[◑]", "[◒]")
    for ($i = 0; $i -lt 8; $i++) {
        $frame = $frames[$i % 4]
        Write-Host "`r  $frame " -NoNewline -ForegroundColor Cyan
        Start-Sleep -Milliseconds 150
    }
    Write-Host "`r  [✓] " -NoNewline -ForegroundColor Green
    Write-Host "Fet!                  " -ForegroundColor White
}

# Bucle principal
$sortir = $false
while (-not $sortir) {
    Mostrar-Menu
    $opcio = Read-Host "  ➤ Tria una opcio"

    if ($opcio -eq "S" -or $opcio -eq "s") {
        Clear-Host
        Write-Host ""
        Write-Host "  ┌────────────────────────────────────────────┐" -ForegroundColor Cyan
        Write-Host "  │                                            │" -ForegroundColor Cyan
        Write-Host "  │  👋  Fins aviat!                           │" -ForegroundColor Cyan
        Write-Host "  │                                            │" -ForegroundColor Cyan
        Write-Host "  │  Recorda: el BernatLab es al teu           │" -ForegroundColor DarkCyan
        Write-Host "  │  abast, sempre. 🌱                          │" -ForegroundColor DarkCyan
        Write-Host "  │                                            │" -ForegroundColor Cyan
        Write-Host "  └────────────────────────────────────────────┘" -ForegroundColor Cyan
        Write-Host ""
        $sortir = $true
        break
    }

    if ($URLs.Contains($opcio)) {
        $item = $URLs[$opcio]

        if ($item.URL -eq "ALL") {
            Animar-Obrint "TOTES les URLs (6 finestres)"
            Write-Host ""
            Write-Host "  ╔══════════════════════════════════════════╗" -ForegroundColor Yellow
            Write-Host "  ║  Obrint les 6 finestres...               ║" -ForegroundColor Yellow
            Write-Host "  ╚══════════════════════════════════════════╝" -ForegroundColor Yellow
            Write-Host ""
            $i = 1
            foreach ($key in ($URLs.Keys | Where-Object { $_ -ne "0" })) {
                $u = $URLs[$key]
                Write-Host "  [$i/6] " -NoNewline -ForegroundColor Cyan
                Obrir-URL $u.URL $u.Nom
                Start-Sleep -Seconds 1
                $i++
            }
            Write-Host ""
            Write-Host "  ╔══════════════════════════════════════════╗" -ForegroundColor Green
            Write-Host "  ║  [✓] Les 6 finestres s'han obert!        ║" -ForegroundColor Green
            Write-Host "  ╚══════════════════════════════════════════╝" -ForegroundColor Green
        }
        else {
            Animar-Obrint $item.Nom
            Write-Host ""
            Obrir-URL $item.URL $item.Nom
            Write-Host ""
            Write-Host "  ┌────────────────────────────────────────────┐" -ForegroundColor Green
            Write-Host "  │  [✓] URL oberta correctament              │" -ForegroundColor Green
            Write-Host "  └────────────────────────────────────────────┘" -ForegroundColor Green
        }

        Write-Host ""
        Write-Host "  ➤ Prem ENTER per tornar al menu..." -ForegroundColor DarkGray
        Read-Host | Out-Null
    }
    else {
        Write-Host ""
        Write-Host "  [✗] Opcio no valida: '$opcio'" -ForegroundColor Red
        Write-Host "  ➤ Tria una opcio de la llista." -ForegroundColor DarkGray
        Start-Sleep -Seconds 2
    }
}
