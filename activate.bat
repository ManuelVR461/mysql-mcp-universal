@echo off
REM Script para activar el entorno virtual en Windows
echo Activando entorno virtual...
call venv\Scripts\activate.bat
echo.
echo ✅ Entorno virtual activado
echo.
echo Comandos disponibles:
echo   python test_connection.py  - Probar conexión
echo   python -m src.server       - Iniciar servidor MCP
echo   pytest tests/              - Ejecutar tests
echo   deactivate                 - Desactivar entorno virtual
echo.
