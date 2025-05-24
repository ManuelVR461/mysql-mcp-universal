# Changelog

Todas las mejoras notables de este proyecto serán documentadas en este archivo.

## [2.0.1] - 2024-12-23

### 🎉 Primera versión pública
- **NUEVA FUNCIONALIDAD**: Servidor MCP Universal para MySQL
- **NUEVA FUNCIONALIDAD**: Conectividad dinámica a cualquier servidor MySQL
- **NUEVA FUNCIONALIDAD**: 4 herramientas MCP integradas:
  - `show_databases` - Lista todas las bases de datos
  - `show_tables` - Lista tablas de una base de datos
  - `describe_table` - Muestra estructura de tablas
  - `execute_query` - Ejecuta consultas SQL personalizadas

### ✨ Características principales
- Soporte para servidores MySQL locales y remotos
- Parámetros de conexión dinámicos por consulta
- Sistema de caché inteligente de conexiones
- Integración perfecta con GitHub Copilot en VS Code
- Configuración simple y rápida

### 🛠️ Optimizaciones
- Proyecto limpio con solo archivos esenciales
- Documentación completa y clara
- Scripts de inicio automatizados
- Manejo robusto de errores

### 📦 Dependencias
- `@modelcontextprotocol/sdk`: ^1.11.5
- `dotenv`: ^16.5.0
- `mysql2`: ^3.14.1

### 🎯 Compatibilidad
- Node.js 18+
- VS Code con GitHub Copilot
- MySQL 5.7+, MySQL 8.0+, MariaDB

---

## Próximas versiones planificadas

### [2.1.0] - Planificado
- Soporte para SSL/TLS
- Pool de conexiones configurable
- Métricas de rendimiento

### [2.2.0] - Planificado
- Soporte para PostgreSQL
- Interfaz web opcional
- Backup automático de configuraciones

---

**Formato basado en [Keep a Changelog](https://keepachangelog.com/)**
