# 🚀 MySQL MCP Universal Server

[![npm version](https://badge.fury.io/js/mysql-mcp-universal.svg)](https://badge.fury.io/js/mysql-mcp-universal)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Node.js](https://img.shields.io/badge/node-%3E%3D18.0.0-brightgreen.svg)](https://nodejs.org/)

**🌟 ¡La forma más fácil de conectar GitHub Copilot a cualquier base de datos MySQL al instante!**

Servidor MCP (Model Context Protocol) que permite a GitHub Copilot conectarse a **cualquier base de datos MySQL** en **cualquier servidor** (local o remoto).

📖 **[English Documentation](README-EN.md)** | **[Guía de Instalación](INSTALL.md)** | **[Guía Rápida](GUIA-RAPIDA.md)**

## ⚡ Instalación Rápida

1. **Instalar dependencias:**
   ```bash
   npm install
   ```

2. **Configurar VS Code globalmente:**
   Agregar a `C:\Users\[usuario]\AppData\Roaming\Code\User\settings.json`:
   ```json
   "mcp": {
       "servers": {
           "mysql-universal": {
               "command": "node",
               "args": ["Q:\\laragon\\www\\mysql-connect\\main-universal.cjs"],
               "env": {
                   "MYSQL_HOST": "127.0.0.1",
                   "MYSQL_USER": "root",
                   "MYSQL_PASSWORD": "tu_password",
                   "MYSQL_PORT": "3306"
               }
           }
       }
   }
   ```

3. **Reiniciar VS Code**

## 🎯 Uso Inmediato

Abre GitHub Copilot Chat en VS Code y prueba:

- `"Muestra las bases de datos disponibles"`
- `"Lista las tablas de la base de datos 'mi_proyecto'"`
- `"Describe la estructura de la tabla 'usuarios'"`
- `"Ejecuta: SELECT * FROM productos LIMIT 10"`

## 🌟 Características

- ✅ **Universal**: Conecta a cualquier servidor MySQL
- ✅ **Flexible**: Parámetros dinámicos por consulta
- ✅ **Inteligente**: Cache de conexiones automático
- ✅ **Simple**: Sin configuración compleja

## 🔧 Herramientas Disponibles

| Herramienta | Descripción | Parámetros |
|-------------|-------------|------------|
| `show_databases` | Lista todas las bases de datos | host, port, user, password (opcionales) |
| `show_tables` | Lista tablas de una BD | database (requerido), conexión (opcional) |
| `describe_table` | Estructura de una tabla | table_name, database (requeridos), conexión (opcional) |
| `execute_query` | Ejecuta consultas SQL | query, database (requeridos), conexión (opcional) |

## 📝 Ejemplos Avanzados

```
# Servidor remoto
"Conecta al servidor 192.168.1.100 puerto 3307 usuario 'admin' y muestra las bases de datos"

# Múltiples operaciones
"Lista las tablas de 'produccion' en localhost y las de 'desarrollo' en servidor remoto"

# Consultas específicas
"En la base de datos 'ventas', ejecuta: SELECT COUNT(*) FROM pedidos WHERE fecha >= '2024-01-01'"
```

## ⚙️ Configuración Opcional (.env)

```env
MYSQL_HOST=127.0.0.1
MYSQL_USER=root
MYSQL_PASSWORD=123456
MYSQL_PORT=3306
```

*Nota: Las variables de entorno son valores por defecto. Cada consulta puede usar parámetros diferentes.*

## 🚀 Inicio del Servidor

```bash
# Opción 1: Script automatizado
start-universal.bat

# Opción 2: Comando directo
node main-universal.cjs
```

## 📁 Archivos del Proyecto

- `main-universal.cjs` - Servidor principal (CommonJS)
- `package.json` - Dependencias del proyecto
- `.env` - Variables de entorno por defecto
- `start-universal.bat` - Script de inicio
- `README.md` - Esta documentación

## ⚠️ Requisitos

- Node.js 18 o superior
- MySQL Server ejecutándose
- Laragon o servidor MySQL local/remoto

---
**© 2024-2025 MySQL MCP Universal Server v2.0.1**
