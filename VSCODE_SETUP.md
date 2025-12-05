# 🔧 Configuración de VS Code para database-connect MCP

Este documento explica cómo configurar GitHub Copilot en VS Code para usar la herramienta **database-connect**.

---

## ✅ Requisitos Previos

1. **VS Code** instalado
2. **GitHub Copilot** (extensión instalada y activa)
3. **Python 3.10+** instalado
4. **database-connect** configurado (ver README.md)

---

## 📋 Pasos de Configuración

### 1. Abrir Configuración de Usuario de VS Code

Hay dos formas:

**Opción A:** Usar interfaz gráfica
- `Ctrl + Shift + P` → "Preferences: Open User Settings (JSON)"

**Opción B:** Ruta directa
- Ir a: `%APPDATA%\Code\User\settings.json` (Windows)
- O: `~/.config/Code/User/settings.json` (Linux)
- O: `~/Library/Application Support/Code/User/settings.json` (Mac)

### 2. Agregar Configuración MCP

Agregar este bloque al archivo `settings.json`:

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

> **⚠️ IMPORTANTE:** Ajusta la ruta `c:\\laragon\\www\\database-connect\\run_server.bat` según donde instalaste el proyecto.

**Para Linux/Mac:**

```json
{
  "github.copilot.chat.mcp.servers": {
    "database-connect": {
      "command": "/bin/bash",
      "args": [
        "-c",
        "cd /ruta/a/database-connect && source venv/bin/activate && python src/server.py"
      ],
      "env": {},
      "disabled": false
    }
  }
}
```

### 3. Recargar VS Code

- Cierra y vuelve a abrir VS Code
- O ejecuta: `Ctrl + Shift + P` → "Developer: Reload Window"

---

## ✅ Verificación

### 1. Comprobar que el servidor está disponible

Abre **GitHub Copilot Chat** en VS Code y escribe:

```
@database-connect test_server
```

Deberías recibir:

```
✅ Servidor funcionando correctamente
Versión: 0.1.0
Herramientas disponibles: 15
```

### 2. Ver información del servidor

```
@database-connect get_server_info
```

Deberías ver:

```json
{
  "status": "success",
  "server": {
    "name": "database-connect",
    "version": "0.1.0",
    "description": "Herramienta MCP para gestión de bases de datos"
  },
  "capabilities": {
    "databases": ["MySQL", "PostgreSQL"],
    "features": ["CRUD", "Consultas", "Gestión de Conexiones"]
  },
  "tools_count": 15
}
```

### 3. Listar conexiones configuradas

```
@database-connect list_connections
```

---

## 🛠️ Herramientas Disponibles

Una vez configurado, tienes acceso a **15 herramientas**:

### 🔗 Gestión de Conexiones (6 herramientas)
1. `test_server` - Verificar que el servidor funciona
2. `get_server_info` - Información del servidor
3. `list_connections` - Ver conexiones configuradas
4. `test_connection` - Probar conectividad a BD
5. `list_databases` - Listar bases de datos disponibles
6. `list_tables` - Listar tablas de una base de datos

### 📝 Operaciones CRUD (9 herramientas)

**CREATE (Inserción):**
- `insert_record` - Insertar un registro
- `bulk_insert` - Insertar múltiples registros

**READ (Consulta):**
- `select_records` - Consultar con filtros/límites/ordenamiento
- `get_record_by_id` - Buscar registro por ID
- `count_records` - Contar registros

**UPDATE (Actualización):**
- `update_record` - Actualizar un registro
- `update_records` - Actualizar múltiples registros

**DELETE (Eliminación):**
- `delete_record` - Eliminar un registro
- `delete_records` - Eliminación masiva (con confirmación)

---

## 💬 Ejemplos de Uso con Copilot

### Modo Explícito (Con @database-connect)

```
👤 @database-connect list_tables connection_name="mysql_local"

🤖 Mostrando tablas de la base de datos...
```

### Modo Natural (Sin @)

GitHub Copilot detectará automáticamente cuándo usar la herramienta:

```
👤 "Muéstrame todos los usuarios de la tabla users"

🤖 [Usa automáticamente select_records]
Aquí están los usuarios:
...
```

```
👤 "¿Cuántos productos hay?"

🤖 [Usa count_records]
Hay 1,245 productos en la base de datos.
```

```
👤 "Inserta un nuevo cliente llamado Juan Pérez con email juan@example.com"

🤖 [Usa insert_record]
✅ Cliente insertado correctamente (ID: 42)
```

---

## 🐛 Solución de Problemas

### Problema 1: "Server not found" o "Command failed"

**Solución:**
1. Verifica que la ruta en `settings.json` sea correcta
2. Prueba ejecutar manualmente: `.\run_server.bat`
3. Revisa que el venv esté activado

### Problema 2: "Connection refused" al intentar conectar a BD

**Solución:**
1. Verifica `config/settings.json`
2. Ejecuta `.\test.bat` para probar conexión
3. Asegúrate que MySQL/PostgreSQL estén corriendo

### Problema 3: Las herramientas no aparecen en Copilot

**Solución:**
1. Recarga VS Code completamente (`Developer: Reload Window`)
2. Verifica que GitHub Copilot esté activo
3. Comprueba logs del servidor: los logs aparecen en terminal al ejecutar

### Problema 4: Python no se encuentra

**Solución:**
1. Verifica instalación de Python: `python --version`
2. Asegúrate que Python esté en PATH
3. Reinstala venv: `python -m venv venv`

---

## 📊 Logs y Debugging

### Ver logs del servidor

El servidor genera logs automáticamente cuando se ejecuta:

```bash
# Ejecutar servidor en modo debug
.\run_server.bat
```

Los logs mostrarán:
- ✅ Conexiones exitosas
- ❌ Errores de SQL
- 📝 Consultas ejecutadas (si `log_queries: true` en config)
- 🔧 Información de debugging

### Activar log de queries

En `config/settings.json`:

```json
{
  "settings": {
    "log_queries": true
  }
}
```

---

## 🔒 Seguridad

⚠️ **ADVERTENCIAS DE SEGURIDAD:**

1. **NO compartas** el archivo `config/settings.json` (contiene contraseñas)
2. **NO hagas commit** de `config/settings.json` en Git (ya está en `.gitignore`)
3. **Usa variables de entorno** para producción en lugar de contraseñas hardcodeadas
4. **Las operaciones DELETE requieren confirmación** (`confirm=True`) para prevenir eliminaciones accidentales

---

## 📚 Más Recursos

- **README.md** - Documentación general del proyecto
- **QUICKSTART.md** - Guía de inicio rápido
- **ROADMAP.md** - Plan de desarrollo futuro
- **STATUS.md** - Estado actual del proyecto

---

## 🆘 Soporte

Si encuentras problemas:

1. Revisa este documento completo
2. Ejecuta `.\test.bat` para diagnósticos
3. Revisa los logs del servidor
4. Verifica la configuración de `config/settings.json`
5. Consulta el archivo STATUS.md para problemas conocidos

---

**¡Listo!** 🎉 Ahora puedes usar GitHub Copilot para interactuar con tus bases de datos usando lenguaje natural.
