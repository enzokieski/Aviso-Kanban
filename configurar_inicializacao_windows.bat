@echo off
chcp 65001 >nul
title Configurar Inicialização com o Windows - Kanban Flutuante
cd /d "%~dp0"

set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "SHORTCUT_PATH=%STARTUP_FOLDER%\KanbanFlutuante.vbs"

echo ========================================================
echo     CONFIGURAÇÃO DE INICIALIZAÇÃO - KANBAN FLUTUANTE
echo ========================================================
echo.
echo 1. Iniciar automaticamente ao ligar o Windows
echo 2. Desativar inicialização automática
echo 3. Sair
echo.
set /p opt="Escolha uma opção (1, 2 ou 3): "

if "%opt%"=="1" (
    copy /y "%~dp0iniciar_kanban.vbs" "%SHORTCUT_PATH%" >nul
    echo.
    echo [OK] O Kanban foi configurado para iniciar junto com o Windows!
    echo Arquivo copiado para a pasta Inicializar.
    echo.
    pause
    exit
)

if "%opt%"=="2" (
    if exist "%SHORTCUT_PATH%" (
        del /f /q "%SHORTCUT_PATH%"
        echo.
        echo [OK] Inicialização automática removida com sucesso.
    ) else (
        echo.
        echo [INFO] O Kanban já não estava configurado para iniciar automaticamente.
    )
    echo.
    pause
    exit
)

exit

