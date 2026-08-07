@echo off
REM ==========================================================
REM BernatLab - Acces rapid als recursos (llanca el .ps1)
REM ==========================================================
REM Aquest .bat nomes llança el .ps1. Si vols el menu
REM interactiu, executa directament el .ps1 des de
REM PowerShell.
REM ==========================================================

setlocal

REM Comprovar que PowerShell esta disponible
where powershell >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: PowerShell no esta instal·lat.
    echo Usa bernatlab-web.bat en comptes.
    pause
    exit /b 1
)

REM Llancar el .ps1 amb la politica d'execucio bypass
powershell -ExecutionPolicy Bypass -File "%~dp0bernatlab-web.ps1"

endlocal
