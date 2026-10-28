@echo off
title Kanban Flutuante - Sistema de Avisos
cd /d "%~dp0"

where pythonw >nul 2>&1
if %errorlevel% equ 0 (
    start "" pythonw.exe main.py
    exit
)

where pyw >nul 2>&1
if %errorlevel% equ 0 (
    start "" pyw.exe main.py
    exit
)

where python >nul 2>&1
if %errorlevel% equ 0 (
    start "" python.exe main.py
    exit
)

if exist "KanbanFlutuante.exe" (
    start "" "KanbanFlutuante.exe"
    exit
)

if exist "dist\KanbanFlutuante.exe" (
    start "" "dist\KanbanFlutuante.exe"
    exit
)

if exist "dist\KanbanFlutuante\KanbanFlutuante.exe" (
    cd dist\KanbanFlutuante
    start "" "KanbanFlutuante.exe"
    exit
)

echo [ERRO] O Python nao foi encontrado no sistema e o executavel nao existe nesta pasta!
echo.
echo Para resolver:
echo 1. Instale o Python marcando a opcao "Add Python to PATH", OU
echo 2. Execute o arquivo "KanbanFlutuante.exe".
echo.
pause
