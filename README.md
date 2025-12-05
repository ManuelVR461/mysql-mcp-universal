# 🗄️ Database-Connect

**Herramienta MCP para GitHub Copilot - Gestión Inteligente de Bases de Datos**

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![FastMCP](https://img.shields.io/badge/FastMCP-0.2.0+-green.svg)](https://github.com/modelcontextprotocol/fastmcp)

## 📋 Descripción

**Database-Connect** es una herramienta MCP (Model Context Protocol) que permite a GitHub Copilot interactuar directamente con bases de datos MySQL y PostgreSQL mediante lenguaje natural. 

Imagina poder decirle a Copilot: *"Muéstrame los usuarios registrados hoy"* o *"Actualiza el stock del producto con ID 42"* y que se ejecute automáticamente en tu base de datos. Eso es Database-Connect.

## ✨ Características Principales

### 🎯 Operaciones CRUD Completas
- **CREATE**: Insertar registros individuales o en lote
- **READ**: Consultas simples y avanzadas con filtros
- **UPDATE**: Actualizar registros por ID o condiciones
- **DELETE**: Eliminar datos de forma segura con confirmación

### 🚀 Operaciones Avanzadas
- **JOINs**: Consultas entre múltiples tablas
- **Agregaciones**: COUNT, SUM, AVG, MAX, MIN con GROUP BY
- **Transacciones**: Múltiples operaciones atómicas con rollback
- **DDL**: Crear, modificar y eliminar tablas

### 📦 Gestión de Procedimientos Almacenados
- Listar y ejecutar stored procedures
- Crear y eliminar procedimientos
- Ejecutar funciones definidas por usuario
- Soporte para parámetros IN/OUT

### 🔐 Seguridad Integrada
- Prevención de SQL Injection mediante prepared statements
- Confirmación para operaciones destructivas
- Encriptación de credenciales
- Auditoría de operaciones críticas

### ⚙️ Configuración Flexible
- Soporte para múltiples conexiones
- Perfiles de conexión (desarrollo, producción, testing)
- Interfaz de configuración en VS Code
- Cambio de conexión en tiempo real

## 🚀 Inicio Rápido

### Requisitos Previos
- Python 3.10 o superior
- Visual Studio Code
- GitHub Copilot (suscripción activa)
- MySQL 8.0+ o PostgreSQL 12+ (al menos uno)

### Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/database-connect.git
cd database-connect

# 2. Crear y activar entorno virtual
python -m venv venv

# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt
```

### Configuración Inicial

1. **Configurar conexión a base de datos:**

Editar archivo `config/settings.json`:

```json
{
  "connections": {
    "mi_mysql": {
      "type": "mysql",
      "host": "localhost",
      "port": 3306,
      "user": "root",
      "password": "tu_password",
      "database": null
    }
  },
  "default_connection": "mi_mysql"
}
```

2. **Probar la conexión:**

```bash
# Windows:
.\test.bat

# Linux/Mac o manualmente:
python test_connection.py
```

3. **La configuración MCP ya está lista en `.vscode/settings.json`** - No necesitas hacer nada más.

4. **Recargar VS Code** para que detecte el servidor MCP.

### Uso Rápido (Windows)

```bash
# Probar conexión
.\test.bat

# Iniciar servidor MCP
.\run_server.bat

# Activar entorno virtual para desarrollo
.\activate.bat
```

## 💬 Ejemplos de Uso

Una vez configurado, puedes usar Copilot Chat con comandos naturales:

### Consultas Básicas
```
👤 "Muéstrame todos los usuarios de la tabla users"
🤖 [Ejecuta: SELECT * FROM users]

👤 "¿Cuántos productos hay en stock?"
🤖 [Ejecuta: SELECT COUNT(*) FROM products WHERE stock > 0]

👤 "Dame el usuario con email john@example.com"
🤖 [Ejecuta: SELECT * FROM users WHERE email = 'john@example.com']
```

### Operaciones de Modificación
```
👤 "Inserta un nuevo usuario llamado María con email maria@example.com"
🤖 [Ejecuta: INSERT INTO users (name, email) VALUES ('María', 'maria@example.com')]

👤 "Actualiza el precio del producto ID 5 a 99.99"
🤖 [Ejecuta: UPDATE products SET price = 99.99 WHERE id = 5]

👤 "Elimina los usuarios inactivos"
🤖 ⚠️ Esta operación eliminará X registros. ¿Confirmas? (S/N)
```

### Consultas Avanzadas
```
👤 "Muéstrame el total de ventas por categoría"
🤖 [Ejecuta: SELECT category, SUM(amount) FROM sales GROUP BY category]

👤 "Dame los pedidos de hoy con información del cliente"
🤖 [Ejecuta: SELECT o.*, c.name FROM orders o 
     INNER JOIN customers c ON o.customer_id = c.id 
     WHERE DATE(o.created_at) = CURDATE()]
```

### Procedimientos Almacenados
```
👤 "Lista todos los procedimientos almacenados"
🤖 [Muestra lista de stored procedures]

👤 "Ejecuta el procedimiento calculate_discount con parámetro 100"
🤖 [Ejecuta: CALL calculate_discount(100)]
```

## 🛠️ Herramientas Disponibles

Database-Connect proporciona estas herramientas MCP:

### Gestión de Conexiones
- `test_database_connection` - Probar conexión a base de datos
- `list_databases` - Listar bases de datos disponibles
- `get_connection_status` - Estado de conexiones activas

### Operaciones CRUD
- `insert_record` - Insertar un registro
- `bulk_insert` - Insertar múltiples registros
- `select_records` - Seleccionar registros con filtros
- `get_record_by_id` - Obtener registro por ID
- `count_records` - Contar registros
- `update_record` - Actualizar un registro
- `update_records` - Actualizar múltiples registros
- `delete_record` - Eliminar un registro
- `delete_records` - Eliminar múltiples registros

### Consultas Avanzadas
- `execute_custom_query` - Ejecutar SQL personalizado
- `execute_join_query` - Consultas con JOINs
- `execute_aggregate_query` - Consultas con agregaciones
- `execute_transaction` - Ejecutar transacción

### Gestión de Estructura
- `list_tables` - Listar tablas
- `get_table_schema` - Obtener esquema de tabla
- `get_table_info` - Información detallada de tabla
- `create_table` - Crear tabla
- `alter_table` - Modificar tabla
- `drop_table` - Eliminar tabla

### Procedimientos Almacenados
- `list_stored_procedures` - Listar procedimientos
- `get_procedure_definition` - Ver código del procedimiento
- `execute_stored_procedure` - Ejecutar procedimiento
- `create_stored_procedure` - Crear procedimiento
- `drop_stored_procedure` - Eliminar procedimiento

## 📚 Documentación Completa

- [**Guía de Instalación**](docs/INSTALLATION.md) - Instalación detallada paso a paso
- [**Guía del Usuario**](docs/USER_GUIDE.md) - Ejemplos y casos de uso
- [**Referencia API**](docs/API_REFERENCE.md) - Documentación completa de herramientas
- [**Roadmap**](ROADMAP.md) - Plan de desarrollo detallado
- [**Contribuir**](CONTRIBUTING.md) - Guía para contribuidores

## 🔒 Seguridad

Database-Connect toma la seguridad muy en serio:

- ✅ **SQL Injection**: Prevención mediante prepared statements
- ✅ **Credenciales**: Nunca se exponen en logs o errores
- ✅ **Confirmación**: Operaciones destructivas requieren confirmación
- ✅ **Validación**: Todos los inputs son validados
- ✅ **Auditoría**: Registro de operaciones críticas

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor lee [CONTRIBUTING.md](CONTRIBUTING.md) para detalles sobre nuestro código de conducta y proceso de pull requests.

## 📝 Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 🌟 Características Futuras

Próximas versiones incluirán:
- Soporte para SQLite y MongoDB
- Exportación de datos (CSV, JSON, Excel)
- Query builder visual
- Migrations manager
- Backup/restore automático
- Performance monitoring

## 📞 Soporte

¿Necesitas ayuda? 
- 🐛 [Reportar un bug](https://github.com/tu-usuario/database-connect/issues)
- 💡 [Solicitar una característica](https://github.com/tu-usuario/database-connect/issues)
- 📧 Email: soporte@database-connect.com

## 👏 Agradecimientos

- [FastMCP](https://github.com/modelcontextprotocol/fastmcp) - Framework MCP
- [GitHub Copilot](https://github.com/features/copilot) - IA Assistant
- La comunidad de desarrolladores Python

---

**Desarrollado con ❤️ para hacer la gestión de bases de datos más intuitiva y productiva.**

⭐ Si este proyecto te resulta útil, ¡considera darle una estrella en GitHub!
