@echo off
setlocal enabledelayedexpansion

echo 🚀 Script de Publicación Automatizada - MySQL MCP Universal Server
echo ================================================================
echo.

:: Verificar si estamos en la carpeta correcta
if not exist "package.json" (
    echo ❌ Error: No se encontró package.json en la carpeta actual
    echo    Asegúrate de ejecutar este script desde la carpeta del proyecto
    pause
    exit /b 1
)

:: Leer versión actual del package.json
for /f "tokens=2 delims=:, " %%a in ('findstr "version" package.json') do (
    set current_version=%%a
    set current_version=!current_version:"=!
    set current_version=!current_version: =!
)

echo 📦 Versión actual: %current_version%
echo.

:: Preguntar tipo de release
echo ¿Qué tipo de release quieres hacer?
echo 1. Patch (bug fixes)     - 2.0.1 → 2.0.2
echo 2. Minor (new features)  - 2.0.1 → 2.1.0  
echo 3. Major (breaking)      - 2.0.1 → 3.0.0
echo 4. Personalizada
echo.
set /p release_type="Selecciona (1-4): "

:: Incrementar versión según el tipo
if "%release_type%"=="1" (
    npm version patch
    set version_type=patch
) else if "%release_type%"=="2" (
    npm version minor
    set version_type=minor
) else if "%release_type%"=="3" (
    npm version major
    set version_type=major
) else if "%release_type%"=="4" (
    set /p custom_version="Ingresa la nueva versión (ej: 2.0.2): "
    npm version !custom_version!
    set version_type=custom
) else (
    echo ❌ Opción inválida
    pause
    exit /b 1
)

if %errorlevel% neq 0 (
    echo ❌ Error al actualizar versión
    pause
    exit /b 1
)

:: Leer nueva versión
for /f "tokens=2 delims=:, " %%a in ('findstr "version" package.json') do (
    set new_version=%%a
    set new_version=!new_version:"=!
    set new_version=!new_version: =!
)

echo ✅ Nueva versión: %new_version%
echo.

:: Ejecutar verificaciones
echo 🔍 Ejecutando verificaciones...
call verify-before-publish.bat
if %errorlevel% neq 0 (
    echo ❌ Las verificaciones fallaron
    echo    Corrige los errores antes de continuar
    pause
    exit /b 1
)

echo.
echo 📝 Actualizar CHANGELOG.md manualmente antes de continuar
echo    Agrega las nuevas características y cambios
pause

:: Git commit y tag
echo 📝 Creando commit y tag de Git...
git add .
git commit -m "🚀 Release v%new_version%"
git tag -a "v%new_version%" -m "Release version %new_version%"

if %errorlevel% neq 0 (
    echo ❌ Error en Git operations
    pause
    exit /b 1
)

:: Confirmar publicación
echo.
echo ⚠️  ATENCIÓN: Estás a punto de publicar a NPM
echo    Versión: %new_version%
echo    Tipo: %version_type%
echo.
set /p confirm="¿Continuar con la publicación? (s/N): "
if /i not "%confirm%"=="s" (
    echo ❌ Publicación cancelada
    pause
    exit /b 1
)

:: Publicar a NPM
echo 📦 Publicando a NPM...
npm publish --access public

if %errorlevel% neq 0 (
    echo ❌ Error al publicar a NPM
    pause
    exit /b 1
)

:: Push a Git
echo 📤 Subiendo cambios a Git...
git push origin main
git push origin --tags

if %errorlevel% neq 0 (
    echo ❌ Error al subir a Git
    echo    El paquete se publicó en NPM pero hay problemas con Git
    pause
    exit /b 1
)

:: Información post-publicación
echo.
echo 🎉 ¡Publicación exitosa!
echo ========================
echo.
echo 📦 NPM Package: https://www.npmjs.com/package/mysql-mcp-universal
echo 🐙 GitHub Release: https://github.com/ManuelVR461/mysql-mcp-universal/releases/tag/v%new_version%
echo.
echo 📋 Próximos pasos:
echo    1. Crear GitHub Release en la web interface
echo    2. Actualizar documentación si es necesario
echo    3. Anunciar en redes sociales y comunidades
echo    4. Monitorear issues y feedback
echo.
echo 📊 Verificar publicación:
echo    npm info mysql-mcp-universal
echo.

:: Abrir URLs relevantes
echo ¿Quieres abrir las URLs relevantes? (s/N):
set /p open_urls=""
if /i "%open_urls%"=="s" (
    start https://www.npmjs.com/package/mysql-mcp-universal
    start https://github.com/ManuelVR461/mysql-mcp-universal
)

echo ✅ ¡Proceso completado exitosamente!
pause
