# Script de configuracion automatica de database-connect para VS Code
# Fecha: 5 de diciembre 2025

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  CONFIGURACION AUTOMATICA DE MCP" -ForegroundColor Cyan
Write-Host "  database-connect para VS Code" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

$settingsPath = "C:\Users\mayerlin\AppData\Roaming\Code\User\settings.json"

# Verificar que existe el archivo
if (-not (Test-Path $settingsPath)) {
    Write-Host "Error: No se encontro el archivo settings.json" -ForegroundColor Red
    Write-Host "Ruta: $settingsPath" -ForegroundColor Yellow
    exit 1
}

# Crear backup
$backupPath = "$settingsPath.backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
Write-Host "[1/4] Creando backup..." -ForegroundColor Yellow
Copy-Item $settingsPath $backupPath
Write-Host "Backup creado: $backupPath" -ForegroundColor Green
Write-Host ""

# Leer configuracion actual
Write-Host "[2/4] Leyendo configuracion actual..." -ForegroundColor Yellow
$settings = Get-Content $settingsPath -Raw | ConvertFrom-Json

# Verificar estructura
if (-not $settings.'github.copilot.chat.mcpServers') {
    Write-Host "Creando propiedad github.copilot.chat.mcpServers..." -ForegroundColor Yellow
    $settings | Add-Member -NotePropertyName 'github.copilot.chat.mcpServers' -NotePropertyValue @{} -Force
}

# Agregar database-connect
Write-Host "[3/4] Agregando database-connect..." -ForegroundColor Yellow

$databaseConnectConfig = @{
    command = "C:\laragon\www\database-connect\venv\Scripts\python.exe"
    args = @("-m", "src.server")
    cwd = "C:\laragon\www\database-connect"
    env = @{}
}

$settings.'github.copilot.chat.mcpServers' | Add-Member -NotePropertyName 'database-connect' -NotePropertyValue $databaseConnectConfig -Force

# Guardar
$settings | ConvertTo-Json -Depth 10 | Set-Content $settingsPath -Encoding UTF8
Write-Host "Configuracion guardada" -ForegroundColor Green
Write-Host ""

# Verificar
Write-Host "[4/4] Verificando..." -ForegroundColor Yellow
$verify = Get-Content $settingsPath -Raw | ConvertFrom-Json

if ($verify.'github.copilot.chat.mcpServers'.'database-connect') {
    Write-Host "Verificacion exitosa!" -ForegroundColor Green
    Write-Host ""
    
    Write-Host "============================================" -ForegroundColor Cyan
    Write-Host "  CONFIGURACION COMPLETADA" -ForegroundColor Green
    Write-Host "============================================" -ForegroundColor Cyan
    Write-Host ""
    
    Write-Host "Configuracion agregada:" -ForegroundColor Cyan
    Write-Host "  - Servidor: database-connect"
    Write-Host "  - Python: C:\laragon\www\database-connect\venv\Scripts\python.exe"
    Write-Host "  - Directorio: C:\laragon\www\database-connect"
    Write-Host "  - Herramientas: 15 disponibles"
    Write-Host ""
    
    Write-Host "Proximos pasos:" -ForegroundColor Yellow
    Write-Host "  1. Recarga VS Code: Ctrl+Shift+P > Developer: Reload Window"
    Write-Host "  2. Abre Copilot Chat: Ctrl+Alt+I"
    Write-Host "  3. Prueba: @database-connect test_server"
    Write-Host ""
    
    Write-Host "Comandos de ejemplo:" -ForegroundColor Cyan
    Write-Host "  @database-connect list_connections"
    Write-Host "  @database-connect list_databases"
    Write-Host '  @database-connect select_records table_name="users"'
    Write-Host ""
    
    Write-Host "O usa lenguaje natural:" -ForegroundColor Cyan
    Write-Host "  Muestrame todas las bases de datos"
    Write-Host "  Lista las tablas de la base de datos test"
    Write-Host "  Inserta un usuario con nombre Juan"
    Write-Host ""
    
} else {
    Write-Host "Error: No se pudo verificar la configuracion" -ForegroundColor Red
    Write-Host "Restaurando backup..." -ForegroundColor Yellow
    Copy-Item $backupPath $settingsPath -Force
    Write-Host "Backup restaurado" -ForegroundColor Green
    Write-Host ""
    exit 1
}

Write-Host "Backup guardado en:" -ForegroundColor Gray
Write-Host "  $backupPath" -ForegroundColor Gray
Write-Host ""

Write-Host "Presiona Enter para continuar..." -ForegroundColor Gray
Read-Host
