@echo off
cd /d "%~dp0"

if exist "KanbanFlutuante.exe" (
    start "" "KanbanFlutuante.exe"
    exit
)

if exist "dist\KanbanFlutuante.exe" (
    start "" "dist\KanbanFlutuante.exe"
    exit
)

if exist "dist\KanbanFlutuante\KanbanFlutuante.exe" (
    cd "dist\KanbanFlutuante"
    start "" "KanbanFlutuante.exe"
    exit
)

echo [ERRO] O executavel KanbanFlutuante.exe nao foi encontrado nesta pasta.
pause
