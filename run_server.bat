@echo off
REM Script para iniciar el servidor MCP
echo ======================================
echo   DATABASE-CONNECT MCP SERVER
echo ======================================
echo.
call venv\Scripts\activate.bat
python -m src.server
