# ⚡ GUÍA RÁPIDA - MySQL MCP Universal

## 🚀 INICIO EN 3 PASOS

### 1. INSTALAR
```bash
npm install
```

### 2. CONFIGURAR VS CODE
Agregar a la configuración global de VS Code:
```json
"mcp": {
    "servers": {
        "mysql-universal": {
            "command": "node",
            "args": ["Q:\\laragon\\www\\mysql-connect\\main-universal.cjs"]
        }
    }
}
```

### 3. USAR
- Reiniciar VS Code
- Abrir GitHub Copilot Chat
- Escribir: `"Muestra las bases de datos disponibles"`

## 💡 CONSULTAS RÁPIDAS

```
"Lista las tablas de la base de datos 'mi_app'"
"Describe la tabla 'usuarios'"
"Ejecuta: SELECT * FROM productos LIMIT 5"
"Conecta al servidor remoto 192.168.1.100 y muestra las bases de datos"
```

## 🔧 HERRAMIENTAS

- **show_databases** - Lista bases de datos
- **show_tables** - Lista tablas de una BD
- **describe_table** - Estructura de tabla
- **execute_query** - Ejecuta consultas SQL

## ⚙️ CONFIGURACIÓN OPCIONAL

Crear `.env` para valores por defecto:
```env
MYSQL_HOST=127.0.0.1
MYSQL_USER=root
MYSQL_PASSWORD=tu_password
MYSQL_PORT=3306
```

**¡Listo! Ahora puedes consultar cualquier base de datos MySQL desde VS Code** 🎉
