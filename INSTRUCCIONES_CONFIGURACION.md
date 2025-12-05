# 📝 Instrucciones de Configuración - VS Code MCP

## ✅ Backup Creado
Se ha creado un backup de tu configuración:
- **Ubicación:** `C:\Users\mayerlin\AppData\Roaming\Code\User\settings.json.backup_20251205_003640`

## 🔧 Configuración a Agregar

Acabas de abrir el archivo `settings.json` de VS Code. Ahora debes:

### Opción 1: Si ya tienes la propiedad `github.copilot.chat.mcp.servers`

Busca la línea que dice:
```json
"github.copilot.chat.mcp.servers": {
```

Y **DENTRO** de ese objeto, agrega:
```json
"database-connect": {
  "command": "cmd.exe",
  "args": [
    "/c",
    "c:\\laragon\\www\\database-connect\\run_server.bat"
  ],
  "env": {},
  "disabled": false
}
```

**Ejemplo completo:**
```json
"github.copilot.chat.mcp.servers": {
  "fastmcp-mysql": {
    "command": "C:\\laragon\\www\\mysql-connect\\venv\\Scripts\\python.exe",
    ...
  },
  "database-connect": {
    "command": "cmd.exe",
    "args": [
      "/c",
      "c:\\laragon\\www\\database-connect\\run_server.bat"
    ],
    "env": {},
    "disabled": false
  }
}
```

### Opción 2: Si NO tienes la propiedad `github.copilot.chat.mcp.servers`

Agrega esto en cualquier parte del archivo (recomendado al final antes del último `}`):
```json
,
"github.copilot.chat.mcp.servers": {
  "database-connect": {
    "command": "cmd.exe",
    "args": [
      "/c",
      "c:\\laragon\\www\\database-connect\\run_server.bat"
    ],
    "env": {},
    "disabled": false
  }
}
```

## ⚠️ IMPORTANTE: Cuidado con las Comas

- Si agregas en medio del archivo, asegúrate que la línea anterior tenga una coma `,` al final
- Si agregas al final, la línea anterior NO debe tener coma
- JSON es muy estricto con la sintaxis

## ✅ Verificación

Después de guardar:
1. **Recarga VS Code:** Presiona `Ctrl + Shift + P` → "Developer: Reload Window"
2. **Abre Copilot Chat:** Presiona `Ctrl + Alt + I` (o el atajo que uses)
3. **Prueba:** Escribe `@database-connect test_server`

### Resultado Esperado:
```
✅ Servidor funcionando correctamente
Versión: 0.1.0
Herramientas disponibles: 15
```

## 🔍 Solución de Problemas

### Si ves error de JSON:
1. Verifica que todas las comas estén correctas
2. Verifica que todos los paréntesis `{}` y corchetes `[]` estén balanceados
3. Usa el formateador de VS Code: `Ctrl + Shift + P` → "Format Document"

### Si el servidor no aparece:
1. Verifica que la ruta sea correcta: `c:\laragon\www\database-connect\run_server.bat`
2. Prueba ejecutar manualmente: Abre cmd y ejecuta `c:\laragon\www\database-connect\run_server.bat`
3. Revisa que el venv esté activado y las dependencias instaladas

### Si necesitas restaurar el backup:
```powershell
Copy-Item "C:\Users\mayerlin\AppData\Roaming\Code\User\settings.json.backup_20251205_003640" "C:\Users\mayerlin\AppData\Roaming\Code\User\settings.json" -Force
```

## 📞 Siguiente Paso

Una vez configurado y verificado, puedes probar comandos como:
- `@database-connect list_connections` - Ver conexiones disponibles
- `@database-connect list_databases` - Ver bases de datos
- `@database-connect select_records table_name="users"` - Consultar registros

O en **lenguaje natural**:
- "Muéstrame todas las bases de datos disponibles"
- "Lista las tablas de la base de datos test"
- "Inserta un usuario llamado Test con email test@example.com"

¡Éxito! 🚀
