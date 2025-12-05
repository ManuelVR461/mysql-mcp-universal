@echo off
REM Script de verificacion rapida del servidor MCP
echo.
echo ============================================
echo   VERIFICACION RAPIDA - database-connect
echo ============================================
echo.

echo [1/3] Verificando Python y venv...
if exist "venv\Scripts\python.exe" (
    echo   ✓ Python encontrado
    venv\Scripts\python.exe --version
) else (
    echo   × Python no encontrado en venv
    goto error
)
echo.

echo [2/3] Verificando dependencias...
venv\Scripts\python.exe -c "import fastmcp, pymysql, pydantic; print('  ✓ Dependencias OK')" 2>nul
if %errorlevel% neq 0 (
    echo   × Faltan dependencias
    echo   Ejecuta: pip install -r requirements.txt
    goto error
)
echo.

echo [3/3] Probando inicio del servidor...
echo   (Esto puede tardar 2-3 segundos...)
venv\Scripts\python.exe -c "from src.config import get_config; config = get_config(); print('  ✓ Configuracion cargada'); print(f'  ✓ Conexiones: {len(config.list_connections())}'); print(f'  ✓ Default: {config.default_connection}')" 2>nul
if %errorlevel% neq 0 (
    echo   × Error cargando configuracion
    goto error
)
echo.

echo ============================================
echo   ✓ VERIFICACION EXITOSA
echo ============================================
echo.
echo El servidor esta listo para usar.
echo.
echo Proximos pasos:
echo   1. Recarga VS Code (si no lo has hecho)
echo   2. Abre Copilot Chat (Ctrl+Alt+I)
echo   3. Escribe: @database-connect test_server
echo.
goto end

:error
echo.
echo ============================================
echo   × VERIFICACION FALLIDA
echo ============================================
echo.
echo Revisa los errores arriba.
echo Consulta GUIA_PRUEBAS.md para solucion de problemas.
echo.
exit /b 1

:end
pause
