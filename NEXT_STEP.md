# ⚡ Próximo Paso: Configurar en VS Code

## 🎯 Objetivo
Conectar el servidor MCP con GitHub Copilot en VS Code para usar las 15 herramientas desde lenguaje natural.

---

## 📋 Checklist Rápido

### 1. Abrir Settings de VS Code
```
Ctrl + Shift + P → "Preferences: Open User Settings (JSON)"
```

O directamente:
```
%APPDATA%\Code\User\settings.json
```

### 2. Agregar Configuración MCP

Copia esto en tu `settings.json`:

```json
{
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
}
```

⚠️ **IMPORTANTE:** Ajusta la ruta según tu instalación.

### 3. Recargar VS Code
```
Ctrl + Shift + P → "Developer: Reload Window"
```

### 4. Probar en Copilot Chat

Abre GitHub Copilot Chat y prueba:

```
@database-connect test_server
```

Deberías ver:
```
✅ Servidor funcionando correctamente
Versión: 0.1.0
Herramientas disponibles: 15
```

---

## 🧪 Pruebas Recomendadas

### Test 1: Información del Servidor
```
@database-connect get_server_info
```

### Test 2: Listar Conexiones
```
@database-connect list_connections
```

### Test 3: Probar Conexión MySQL
```
@database-connect test_connection connection_name="mysql_local"
```

### Test 4: Ver Bases de Datos
```
@database-connect list_databases connection_name="mysql_local"
```

### Test 5: Lenguaje Natural (Sin @)

Una vez confirmado que funciona, prueba comandos naturales:

```
"Muéstrame las bases de datos disponibles"
"Lista las tablas de la base de datos mysql"
"¿Cuántas conexiones tengo configuradas?"
```

Copilot debería usar automáticamente las herramientas MCP.

---

## 🐛 Troubleshooting

### Problema: "Server not found"
**Solución:**
1. Verifica que la ruta en settings.json sea correcta
2. Ejecuta manualmente: `.\run_server.bat` (debe funcionar)
3. Revisa que Python y venv estén correctos

### Problema: "Connection refused"
**Solución:**
1. Verifica `config/settings.json`
2. Ejecuta `.\test.bat` para probar conexión
3. Asegúrate que MySQL esté corriendo

### Problema: "No tools available"
**Solución:**
1. Recarga completamente VS Code
2. Verifica que GitHub Copilot esté activo
3. Revisa logs del servidor (aparecen al ejecutar)

---

## 📖 Documentación Completa

Para más detalles, consulta:
- **VSCODE_SETUP.md** - Guía completa de configuración
- **TESTING_RESULTS.md** - Resultados de pruebas
- **SESSION_SUMMARY.md** - Resumen de esta sesión
- **README.md** - Documentación general

---

## ✅ Una vez Funcionando...

### Prueba las Herramientas CRUD:

**Insertar:**
```
"Inserta un usuario llamado Pedro con email pedro@test.com y edad 30"
```

**Consultar:**
```
"Muéstrame todos los usuarios de la tabla users"
"¿Cuántos usuarios hay en total?"
"Dame el usuario con ID 5"
```

**Actualizar:**
```
"Actualiza el email del usuario ID 3 a nuevo@email.com"
```

**Eliminar:**
```
"Elimina el usuario con ID 10"
```

---

## 🎯 Si Todo Funciona

¡Felicidades! 🎉 Tu servidor MCP está completamente operativo.

**Siguiente fase:**
- Implementar Stored Procedures (Fase 4)
- Probar PostgreSQL
- Queries avanzadas (JOINs, etc.)

---

**¿Listo para probarlo? ¡Vamos!** 🚀
