#!/bin/bash
# ==========================================================
# BernatLab - Menu rapid (optimitzat per macOS)
# ==========================================================
# Menu grafic per obrir les URLs principals del projecte
# al navegador. Optimitzat per Mac pero funciona a Linux.
#
# Us:
#   ./bernatlab-web-mac.sh           (menu)
#   ./bernatlab-web-mac.sh all       (obre totes les URLs)
#   ./bernatlab-web-mac.sh hort      (obre nomes les de l'hort)
#
# ==========================================================

# Detectar sistema operatiu
detect_os() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    elif [[ "$OSTYPE" == "msys"* ]] || [[ "$OSTYPE" == "win32" ]]; then
        echo "windows"
    else
        echo "unknown"
    fi
}

# Obrir una URL al navegador per defecte
open_url() {
    local url="$1"
    local nom="$2"
    local os=$(detect_os)

    case "$os" in
        macos)
            # macOS: usa 'open' que es perfecte
            open "$url" 2>/dev/null
            ;;
        linux)
            # Linux: prova varies opcions
            if command -v xdg-open > /dev/null; then
                xdg-open "$url" 2>/dev/null
            elif command -v gnome-open > /dev/null; then
                gnome-open "$url" 2>/dev/null
            else
                echo "  [!] No s'ha pogut obrir automaticament: $url"
                return 1
            fi
            ;;
        windows)
            # Windows (Git Bash)
            start "" "$url" 2>/dev/null
            ;;
        *)
            echo "  [!] Sistema no reconegut. Obre manualment: $url"
            return 1
            ;;
    esac

    if [ $? -eq 0 ]; then
        echo "  [OK] $nom"
    else
        echo "  [ERR] $nom"
    fi
    return 0
}

# Colors (funcionen a Mac i Linux amb terminal compatible)
if [ -t 1 ]; then
    BOLD='\033[1m'
    GREEN='\033[0;32m'
    YELLOW='\033[0;33m'
    BLUE='\033[0;34m'
    CYAN='\033[0;36m'
    NC='\033[0m' # No Color
else
    BOLD=''
    GREEN=''
    YELLOW=''
    BLUE=''
    CYAN=''
    NC=''
fi

# URLs del BernatLab
declare -A URLS
URLS[1_nom]="Curs practic"
URLS[1_url]="https://bernatmora.github.io/bernatlab/book/curs/"

URLS[2_nom]="Guia eines M8"
URLS[2_url]="https://github.com/BernatMora/bernatlab/blob/main/book/curs/recursos/eines-m8-pas-a-pas.md"

URLS[3_nom]="Web publica BernatLab"
URLS[3_url]="https://bernatmora.github.io/bernatlab/"

URLS[4_nom]="Web publica Hort Osona"
URLS[4_url]="https://bernatmora.github.io/hort-osona/"

URLS[5_nom]="Repo BernatLab (GitHub)"
URLS[5_url]="https://github.com/BernatMora/bernatlab"

URLS[6_nom]="Repo Hort Osona (GitHub)"
URLS[6_url]="https://github.com/BernatMora/hort-osona"

URLS[7_nom]="PROJECT_STATE"
URLS[7_url]="https://github.com/BernatMora/bernatlab/blob/main/PROJECT_STATE.md"

URLS[8_nom]="Handoff sessio 2026-07-17"
URLS[8_url]="https://github.com/BernatMora/bernatlab/blob/main/book/handoff-sessio-2026-07-17.md"

URLS[9_nom]="Glossari"
URLS[9_url]="https://bernatmora.github.io/bernatlab/book/glossari.html"

URLS[10_nom]="Guia primer dia RPi"
URLS[10_url]="https://bernatmora.github.io/bernatlab/book/primer-dia-rpi.html"

# Funcio per mostrar el menu
show_menu() {
    clear
    echo
    echo -e "${CYAN}╔══════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║                                              ║${NC}"
    echo -e "${CYAN}║   🌱  B E R N A T L A B  ·  M A C  🌱      ║${NC}"
    echo -e "${CYAN}║                                              ║${NC}"
    echo -e "${CYAN}║   Servidor personal · Raspberry Pi · Docker  ║${NC}"
    echo -e "${CYAN}║   Tailscale · IA · LoRa · Hort Osona         ║${NC}"
    echo -e "${CYAN}║                                              ║${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════════╝${NC}"
    echo

    # Mostrar info del sistema
    local os=$(detect_os)
    local os_name=""
    case "$os" in
        macos) os_name="macOS $(sw_vers -productVersion 2>/dev/null || echo '?')" ;;
        linux) os_name="Linux" ;;
        windows) os_name="Windows" ;;
        *) os_name="Desconegut" ;;
    esac
    echo -e "  ${BLUE}Sistema:${NC} $os_name"
    echo -e "  ${BLUE}Directori:${NC} $(pwd)"
    echo

    echo -e "${BOLD}Tria quina URL vols obrir:${NC}"
    echo

    for i in {1..10}; do
        local key="${i}_nom"
        local nom="${URLS[$key]}"
        if [ -n "$nom" ]; then
            local emoji="📄"
            case $i in
                1) emoji="📚" ;;
                2) emoji="🛠️" ;;
                3) emoji="🌱" ;;
                4) emoji="🌿" ;;
                5) emoji="💻" ;;
                6) emoji="🌾" ;;
                7) emoji="📊" ;;
                8) emoji="📋" ;;
                9) emoji="📖" ;;
                10) emoji="🚀" ;;
            esac
            echo -e "  ${YELLOW}[$i]${NC} $emoji  ${BOLD}$nom${NC}"
        fi
    done

    echo
    echo -e "  ${YELLOW}[A]${NC} ⚡  ${BOLD}OBRIR TOTES LES URLs${NC}"
    echo -e "  ${YELLOW}[H]${NC} 🌿  ${BOLD}OBRIR NOMES HORT OSONA${NC}"
    echo -e "  ${YELLOW}[S]${NC} 👋  Sortir"
    echo
}

# Obrir totes les URLs
open_all() {
    echo
    echo -e "${CYAN}╔══════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║  Obrint TOTES les URLs...                    ║${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════════╝${NC}"
    echo

    local i=1
    for idx in {1..10}; do
        local key_nom="${idx}_nom"
        local key_url="${idx}_url"
        local nom="${URLS[$key_nom]}"
        local url="${URLS[$key_url]}"
        if [ -n "$nom" ] && [ -n "$url" ]; then
            echo "[$i/10] Obrint $nom..."
            open_url "$url" "$nom"
            sleep 1
            i=$((i+1))
        fi
    done

    echo
    echo -e "${GREEN}[OK] Totes les URLs obertes!${NC}"
    echo
}

# Obrir nomes les de l'Hort Osona
open_hort() {
    echo
    echo -e "${CYAN}╔══════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║  Obrint URLs d'Hort Osona...                 ║${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════════╝${NC}"
    echo

    open_url "${URLS[4_url]}" "${URLS[4_nom]}"
    sleep 1
    open_url "${URLS[6_url]}" "${URLS[6_nom]}"
    sleep 1

    echo
    echo -e "${GREEN}[OK] URLs d'Hort Osona obertes!${NC}"
    echo
}

# Bucle principal
main() {
    # Si passa un argument, executar directament
    if [ -n "$1" ]; then
        case "$1" in
            all)
                open_all
                exit 0
                ;;
            hort)
                open_hort
                exit 0
                ;;
            *)
                echo "Us: $0 [all|hort]"
                echo "Sense arguments: mostra el menu"
                exit 1
                ;;
        esac
    fi

    # Menu interactiu
    while true; do
        show_menu
        read -p "  Tria una opcio: " opcio

        case "$opcio" in
            [1-9]|10)
                if [ -n "${URLS[${opcio}_nom]}" ]; then
                    echo
                    echo "Obrint: ${URLS[${opcio}_nom]}..."
                    open_url "${URLS[${opcio}_url]}" "${URLS[${opcio}_nom]}"
                    echo
                    read -p "Prem ENTER per tornar al menu..."
                else
                    echo
                    echo -e "${YELLOW}[!] Opcio no valida${NC}"
                    sleep 1
                fi
                ;;
            [Aa])
                open_all
                read -p "Prem ENTER per tornar al menu..."
                ;;
            [Hh])
                open_hort
                read -p "Prem ENTER per tornar al menu..."
                ;;
            [Ss])
                clear
                echo
                echo -e "${CYAN}  👋 Fins aviat! Recorda: el BernatLab es sempre aqui. 🌱${NC}"
                echo
                exit 0
                ;;
            *)
                echo
                echo -e "${YELLOW}[!] Opcio no valida: '$opcio'${NC}"
                sleep 1
                ;;
        esac
    done
}

# Executar
main "$@"
