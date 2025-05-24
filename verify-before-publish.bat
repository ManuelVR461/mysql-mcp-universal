@echo off
echo 🔍 Verificando MySQL MCP Universal Server antes de publicar...
echo.

:: Verificar Node.js
echo ✅ Verificando Node.js...
node --version
if %errorlevel% neq 0 (
    echo ❌ Error: Node.js no está instalado o no está en PATH
    pause
    exit /b 1
)

:: Verificar NPM
echo ✅ Verificando NPM...
npm --version
if %errorlevel% neq 0 (
    echo ❌ Error: NPM no está disponible
    pause
    exit /b 1
)

:: Verificar dependencias
echo ✅ Verificando dependencias...
if not exist "node_modules" (
    echo 📦 Instalando dependencias...
    npm install
    if %errorlevel% neq 0 (
        echo ❌ Error al instalar dependencias
        pause
        exit /b 1
    )
)

:: Verificar archivo principal
echo ✅ Verificando archivo principal...
if not exist "main-universal.cjs" (
    echo ❌ Error: main-universal.cjs no encontrado
    pause
    exit /b 1
)

:: Probar sintaxis del servidor
echo ✅ Verificando sintaxis del servidor...
node -c main-universal.cjs
if %errorlevel% neq 0 (
    echo ❌ Error de sintaxis en main-universal.cjs
    pause
    exit /b 1
)

:: Ejecutar tests
echo ✅ Ejecutando tests...
npm test
if %errorlevel% neq 0 (
    echo ❌ Tests fallaron
    pause
    exit /b 1
)

:: Verificar archivos necesarios
echo ✅ Verificando archivos necesarios...
set required_files=README.md LICENSE package.json main-universal.cjs .env.example

for %%f in (%required_files%) do (
    if not exist "%%f" (
        echo ❌ Archivo requerido no encontrado: %%f
        pause
        exit /b 1
    )
)

:: Verificar estructura del package.json
echo ✅ Verificando package.json...
node -e "
const pkg = require('./package.json');
const required = ['name', 'version', 'description', 'main', 'author', 'license'];
for (const field of required) {
    if (!pkg[field]) {
        console.log('❌ Campo requerido faltante en package.json:', field);
        process.exit(1);
    }
}
console.log('✅ package.json válido');
"
if %errorlevel% neq 0 (
    echo ❌ Error en package.json
    pause
    exit /b 1
)

:: Verificar tamaño del paquete
echo ✅ Verificando tamaño del paquete...
npm pack --dry-run
if %errorlevel% neq 0 (
    echo ❌ Error al empaquetar
    pause
    exit /b 1
)

:: Verificar login de NPM
echo ✅ Verificando login de NPM...
npm whoami >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  No estás logueado en NPM
    echo    Ejecuta: npm login
    pause
    exit /b 1
)

echo.
echo 🎉 ¡Todas las verificaciones pasaron!
echo.
echo 📋 Checklist final antes de publicar:
echo    ✅ Código probado y funcionando
echo    ✅ Documentación actualizada
echo    ✅ Versión incrementada en package.json
echo    ✅ CHANGELOG.md actualizado
echo    ✅ Logueado en NPM
echo.
echo 🚀 Para publicar ejecuta:
echo    npm publish --access public
echo.
pause
