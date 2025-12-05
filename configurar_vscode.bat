@echo off
REM Script para agregar database-connect a VS Code settings.json
REM Creado: 5 de diciembre 2025

echo.
echo ============================================
echo   CONFIGURACION AUTOMATICA DE MCP
echo   database-connect para VS Code
echo ============================================
echo.

set SETTINGS_FILE=C:\Users\mayerlin\AppData\Roaming\Code\User\settings.json
set BACKUP_FILE=%SETTINGS_FILE%.backup_%date:~-4,4%%date:~-7,2%%date:~-10,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set BACKUP_FILE=%BACKUP_FILE: =0%

echo [1/4] Creando backup...
copy "%SETTINGS_FILE%" "%BACKUP_FILE%" >nul
if %errorlevel% equ 0 (
    echo ✓ Backup creado: %BACKUP_FILE%
) else (
    echo × Error creando backup
    pause
    exit /b 1
)

echo.
echo [2/4] Agregando configuracion database-connect...

powershell -ExecutionPolicy Bypass -Command ^
"$settingsPath = '%SETTINGS_FILE%'; ^
$settings = Get-Content $settingsPath -Raw | ConvertFrom-Json; ^
if (-not $settings.'github.copilot.chat.mcpServers') { ^
    Write-Host '× No se encontro github.copilot.chat.mcpServers' -ForegroundColor Red; ^
    exit 1 ^
}; ^
if ($settings.'github.copilot.chat.mcpServers'.'database-connect') { ^
    Write-Host '! database-connect ya existe, actualizando...' -ForegroundColor Yellow ^
}; ^
$settings.'github.copilot.chat.mcpServers' | Add-Member -NotePropertyName 'database-connect' -NotePropertyValue @{ ^
    command = 'C:\laragon\www\database-connect\venv\Scripts\python.exe'; ^
    args = @('-m', 'src.server'); ^
    cwd = 'C:\laragon\www\database-connect'; ^
    env = @{} ^
} -Force; ^
$settings | ConvertTo-Json -Depth 10 | Set-Content $settingsPath; ^
Write-Host '✓ Configuracion agregada exitosamente' -ForegroundColor Green"

if %errorlevel% equ 0 (
    echo ✓ database-connect configurado correctamente
) else (
    echo × Error configurando database-connect
    echo.
    echo Restaurando backup...
    copy "%BACKUP_FILE%" "%SETTINGS_FILE%" /Y >nul
    echo ✓ Backup restaurado
    pause
    exit /b 1
)

echo.
echo [3/4] Verificando configuracion...
powershell -ExecutionPolicy Bypass -Command ^
"$settings = Get-Content '%SETTINGS_FILE%' -Raw | ConvertFrom-Json; ^
if ($settings.'github.copilot.chat.mcpServers'.'database-connect') { ^
    Write-Host '✓ database-connect encontrado en configuracion' -ForegroundColor Green; ^
    $config = $settings.'github.copilot.chat.mcpServers'.'database-connect'; ^
    Write-Host '  Command: ' $config.command; ^
    Write-Host '  CWD: ' $config.cwd ^
} else { ^
    Write-Host '× database-connect NO encontrado' -ForegroundColor Red; ^
    exit 1 ^
}"

if %errorlevel% neq 0 (
    echo × Verificacion fallida
    pause
    exit /b 1
)

echo.
echo [4/4] Configuracion completada
echo.
echo ============================================
echo   ✓ CONFIGURACION EXITOSA
echo ============================================
echo.
echo Proximos pasos:
echo   1. Reinicia VS Code (o presiona Ctrl+Shift+P ^> "Developer: Reload Window")
echo   2. Abre GitHub Copilot Chat (Ctrl+Alt+I)
echo   3. Prueba: @database-connect test_server
echo.
echo Backup guardado en:
echo   %BACKUP_FILE%
echo.
pause
