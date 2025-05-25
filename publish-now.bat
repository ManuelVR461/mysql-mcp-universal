@echo off
echo.
echo 🚀 MySQL MCP Universal Server - Publicación Final
echo ================================================
echo.
echo 📦 Versión actual: 2.2.0
echo 🎯 ¿Deseas publicar en NPM? (S/N)
set /p respuesta="> "

if /i "%respuesta%"=="S" (
    echo.
    echo 🚀 Publicando...
    npm publish
    if %ERRORLEVEL% EQU 0 (
        echo.
        echo ✅ ¡PUBLICACIÓN EXITOSA!
        echo.
        echo 🔗 Tu paquete está disponible en:
        echo https://www.npmjs.com/package/mysql-mcp-universal
        echo.
        echo 📖 Documentación:
        echo https://github.com/ManuelVR461/mysql-mcp-universal
        echo.
        start https://www.npmjs.com/package/mysql-mcp-universal
    ) else (
        echo ❌ Error en la publicación
    )
) else (
    echo ❌ Publicación cancelada
)
echo.
pause
