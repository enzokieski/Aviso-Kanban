@echo off
title Kanban Flutuante - Sistema de Avisos
cd /d "%~dp0"

where pythonw >nul 2>&1
if %errorlevel% equ 0 (
    start "" pythonw.exe main.py
    exit
)

where python >nul 2>&1
if %errorlevel% equ 0 (
    start "" python.exe main.py
    exit
)

echo [ERRO] Python nao foi encontrado no sistema!
echo Por favor, instale o Python ou adicione-o ao PATH do Windows.
pause

