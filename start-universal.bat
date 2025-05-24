@echo off
echo 🚀 MYSQL MCP UNIVERSAL SERVER
echo =============================
echo.

cd /d "Q:\laragon\www\mysql-connect"

echo 🔍 Verificando archivos...
if not exist "main-universal.cjs" (
    echo ❌ main-universal.cjs NO encontrado
    goto :error
)

if not exist "package.json" (
    echo ❌ package.json NO encontrado  
    goto :error
)

echo ✅ Archivos verificados
echo.

echo 🔧 Verificando dependencias...
if not exist "node_modules" (
    echo 📦 Instalando dependencias...
    npm install
    if errorlevel 1 goto :error
)

echo ✅ Dependencias listas
echo.

echo 🚀 Iniciando servidor...
echo ⚠️  Presiona Ctrl+C para detener
echo.

node main-universal.cjs

goto :end

:error
echo.
echo ❌ ERROR: No se pudo iniciar el servidor
echo.
echo 🔧 Verificaciones:
echo    • Node.js debe estar instalado
echo    • MySQL debe estar ejecutándose
echo    • Las dependencias deben estar instaladas (npm install)
echo.
pause
goto :end

:end
