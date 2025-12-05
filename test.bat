@echo off
REM Script para ejecutar tests
echo ======================================
echo   EJECUTANDO PRUEBAS
echo ======================================
echo.
call venv\Scripts\activate.bat
python test_connection.py
