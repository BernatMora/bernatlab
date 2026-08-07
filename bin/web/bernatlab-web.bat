@echo off
REM ==========================================================
REM BernatLab - Acces rapid als recursos del curs
REM ==========================================================
REM Obre les 3 URLs principals del BernatLab al navegador
REM - Curs practic
REM - Guia eines M8
REM - Web publica del BernatLab
REM ==========================================================

setlocal

echo.
echo ============================================
echo   BernatLab - Obrint recursos al navegador
echo ============================================
echo.

REM 1. Curs practic
echo [1/3] Obrint el curs practic...
start "" "https://bernatmora.github.io/bernatlab/book/curs/"
ping -n 3 127.0.0.1 >nul 2>&1

REM 2. Guia eines M8 (GitHub)
echo [2/3] Obrint la guia d'eines M8...
start "" "https://github.com/BernatMora/bernatlab/blob/main/book/curs/recursos/eines-m8-pas-a-pas.md"
ping -n 3 127.0.0.1 >nul 2>&1

REM 3. Web publica del BernatLab
echo [3/3] Obrint la web publica del BernatLab...
start "" "https://bernatmora.github.io/bernatlab/"

echo.
echo ============================================
echo   Fet! Les 3 URLs son al teu navegador.
echo ============================================
echo.

REM Pausa per veure la sortida
pause
endlocal
