@echo off
chcp 65001 >nul
color 0A
echo.
echo 🚀 Publicación Rápida - MySQL MCP Universal Server v2.2.0
echo ================================================================
echo.
echo 📦 Verificando paquete...
npm pack --dry-run
echo.
echo 🌐 Verificando estado de NPM...
npm whoami
echo.
echo 📝 Ejecutando prueba de publicación...
npm publish --dry-run
echo.
echo 🎯 ¿Proceder con la publicación real? (S/N)
set /p answer="> "
if /i "%answer%"=="S" (
    echo.
    echo 🚀 Publicando en NPM...
    npm publish
    echo.
    echo 📊 Información del paquete publicado:
    npm info mysql-mcp-universal
    echo.
    echo ✅ ¡Publicación completada!
    echo.
    echo 🔗 Enlaces importantes:
    echo NPM: https://www.npmjs.com/package/mysql-mcp-universal
    echo GitHub: https://github.com/ManuelVR461/mysql-mcp-universal
    echo.
    start https://www.npmjs.com/package/mysql-mcp-universal
) else (
    echo ❌ Publicación cancelada
)
echo.
pause
