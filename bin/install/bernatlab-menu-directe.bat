@echo off
REM ==========================================================
REM BernatLab Menu - Acces directe al menu visual
REM ==========================================================
REM Aquest .bat es pot posar a l'escriptori com a acceso
REM directe per obrir el menu del BernatLab rapidament.
REM ==========================================================

REM Anar al directori bin del BernatLab
cd /d "C:\Users\iadmin\bernatlab\bin"

REM Llancar el menu PowerShell amb la politica d'execucio adequada
start "BernatLab Menu" powershell -ExecutionPolicy Bypass -NoExit -File "C:\Users\iadmin\bernatlab\bin\bernatlab-web.ps1"

REM Aquest start obra una finestra de PowerShell nova amb el menu.
REM Quan surts del menu (opcio S), la finestra es tanca sola
REM gracies al -NoExit (manten la consola oberta si cal).
