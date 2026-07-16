#!/bin/bash
# ==========================================================
# BernatLab - Acces rapid als recursos del curs
# ==========================================================
# Obre les 3 URLs principals del BernatLab al navegador
# - Curs practic
# - Guia eines M8
# - Web publica del BernatLab
# ==========================================================

echo
echo "============================================"
echo "  BernatLab - Obrint recursos al navegador"
echo "============================================"
echo

# Detectar sistema operatiu per triar el navegador correcte
open_url() {
    local url="$1"
    if command -v xdg-open > /dev/null; then
        xdg-open "$url"  # Linux
    elif command -v open > /dev/null; then
        open "$url"       # macOS
    elif command -v start > /dev/null; then
        start "" "$url"   # Windows (Git Bash)
    else
        echo "No s'ha pogut obrir el navegador automaticament."
        echo "Obre manualment: $url"
    fi
}

# 1. Curs practic
echo "[1/3] Obrint el curs practic..."
open_url "https://bernatmora.github.io/bernatlab/book/curs/"
sleep 2

# 2. Guia eines M8 (GitHub)
echo "[2/3] Obrint la guia d'eines M8..."
open_url "https://github.com/BernatMora/bernatlab/blob/main/book/curs/recursos/eines-m8-pas-a-pas.md"
sleep 2

# 3. Web publica del BernatLab
echo "[3/3] Obrint la web publica del BernatLab..."
open_url "https://bernatmora.github.io/bernatlab/"

echo
echo "============================================"
echo "  Fet! Les 3 URLs son al teu navegador."
echo "============================================"
echo
