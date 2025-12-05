"""
Database-Connect MCP Server
Servidor principal que expone herramientas MCP para gestión de bases de datos
"""

from fastmcp import FastMCP
import logging
from pathlib import Path
import sys
import os
from typing import Optional, Dict, Any

# Importar módulos propios
from .config import get_config
from .database.mysql_handler import MySQLHandler
from .database.postgres_handler import PostgreSQLHandler
from .database.connection import get_connection_pool
from .tools import crud_tools

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Crear instancia del servidor MCP
mcp = FastMCP("database-connect")

# ============================================================================
# HERRAMIENTAS DE PRUEBA Y CONEXIÓN
# ============================================================================

@mcp.tool()
def test_server() -> dict:
    """
    Prueba básica del servidor MCP.
    
    Esta herramienta verifica que el servidor Database-Connect está funcionando correctamente.
    No requiere parámetros y simplemente devuelve un mensaje de confirmación.
    
    Returns:
        dict: Estado del servidor y mensaje de confirmación
        
    Example:
        >>> test_server()
        {'status': 'ok', 'message': 'Database-Connect MCP Server is running', 'version': '0.1.0'}
    """
    logger.info("Test server called")
    return {
        "status": "ok",
        "message": "Database-Connect MCP Server is running",
        "version": "0.1.0",
        "features": [
            "MySQL Support",
            "PostgreSQL Support",
            "CRUD Operations",
            "Stored Procedures",
            "Advanced Queries"
        ]
    }


@mcp.tool()
def get_server_info() -> dict:
    """
    Obtiene información detallada del servidor MCP.
    
    Proporciona información sobre el estado del servidor, conexiones disponibles,
    herramientas registradas y configuración actual.
    
    Returns:
        dict: Información completa del servidor
        
    Example:
        >>> get_server_info()
        {'server_name': 'database-connect', 'version': '0.1.0', ...}
    """
    logger.info("Getting server info")
    
    # Obtener configuración
    config = get_config()
    connections = config.list_connections()
    
    # Obtener estadísticas del pool
    pool = get_connection_pool()
    pool_stats = pool.get_stats()
    
    return {
        "server_name": "database-connect",
        "version": "0.1.0",
        "description": "Herramienta MCP para gestión de bases de datos",
        "config_file": str(config.config_path),
        "config_exists": config.config_path.exists(),
        "supported_databases": ["MySQL", "PostgreSQL"],
        "total_connections": len(connections),
        "default_connection": config.default_connection,
        "pool_stats": pool_stats,
        "status": "ready"
    }


# ============================================================================
# HERRAMIENTAS DE GESTIÓN DE CONEXIONES
# ============================================================================

@mcp.tool()
def list_connections() -> dict:
    """
    Lista todas las conexiones de base de datos configuradas.
    
    Muestra información sobre todas las conexiones disponibles incluyendo
    tipo de base de datos, host, puerto, usuario y estado.
    
    Returns:
        dict: Diccionario con información de todas las conexiones
        
    Example:
        >>> list_connections()
        {
            'total': 2,
            'default': 'mysql_local',
            'connections': {
                'mysql_local': {'type': 'mysql', 'host': 'localhost', ...},
                'postgres_prod': {'type': 'postgres', ...}
            }
        }
    """
    logger.info("Listando conexiones")
    config = get_config()
    connections = config.list_connections()
    
    return {
        "total": len(connections),
        "default": config.default_connection,
        "connections": connections
    }


@mcp.tool()
def test_connection(connection_name: Optional[str] = None) -> dict:
    """
    Prueba una conexión a base de datos.
    
    Intenta conectarse a la base de datos especificada y ejecuta una consulta
    simple para verificar que la conexión funciona correctamente.
    
    Args:
        connection_name: Nombre de la conexión a probar. Si es None, usa la conexión por defecto.
    
    Returns:
        dict: Resultado de la prueba con información de la conexión
        
    Example:
        >>> test_connection("mysql_local")
        {'status': 'connected', 'host': 'localhost', 'port': 3306, ...}
    """
    logger.info(f"Probando conexión: {connection_name or 'default'}")
    
    try:
        config = get_config()
        conn_config = config.get_connection(connection_name)
        
        if not conn_config:
            return {
                "status": "error",
                "error": f"Conexión '{connection_name}' no encontrada",
                "available_connections": list(config.list_connections().keys())
            }
        
        # Crear handler según el tipo
        if conn_config.type == 'mysql':
            handler = MySQLHandler(
                host=conn_config.host,
                port=conn_config.port,
                user=conn_config.user,
                password=conn_config.password,
                database=conn_config.database
            )
        elif conn_config.type in ('postgres', 'postgresql'):
            handler = PostgreSQLHandler(
                host=conn_config.host,
                port=conn_config.port,
                user=conn_config.user,
                password=conn_config.password,
                database=conn_config.database
            )
        else:
            return {
                "status": "error",
                "error": f"Tipo de base de datos '{conn_config.type}' no soportado"
            }
        
        # Probar conexión
        result = handler.test_connection()
        handler.disconnect()
        
        return result
        
    except Exception as e:
        logger.error(f"Error probando conexión: {e}")
        return {
            "status": "error",
            "error": str(e)
        }


@mcp.tool()
def list_databases(connection_name: Optional[str] = None) -> dict:
    """
    Lista todas las bases de datos disponibles en el servidor.
    
    Conecta al servidor de base de datos y obtiene la lista de todas
    las bases de datos disponibles.
    
    Args:
        connection_name: Nombre de la conexión a usar. Si es None, usa la conexión por defecto.
    
    Returns:
        dict: Lista de bases de datos y información de la conexión
        
    Example:
        >>> list_databases()
        {
            'connection': 'mysql_local',
            'total': 5,
            'databases': ['mysql', 'information_schema', 'testdb', ...]
        }
    """
    logger.info(f"Listando bases de datos: {connection_name or 'default'}")
    
    try:
        config = get_config()
        conn_config = config.get_connection(connection_name)
        
        if not conn_config:
            return {
                "status": "error",
                "error": f"Conexión '{connection_name}' no encontrada"
            }
        
        # Crear handler
        if conn_config.type == 'mysql':
            handler = MySQLHandler(
                host=conn_config.host,
                port=conn_config.port,
                user=conn_config.user,
                password=conn_config.password,
                database=conn_config.database
            )
        elif conn_config.type in ('postgres', 'postgresql'):
            handler = PostgreSQLHandler(
                host=conn_config.host,
                port=conn_config.port,
                user=conn_config.user,
                password=conn_config.password,
                database=conn_config.database
            )
        else:
            return {
                "status": "error",
                "error": f"Tipo de base de datos '{conn_config.type}' no soportado"
            }
        
        # Listar bases de datos
        with handler:
            databases = handler.list_databases()
        
        return {
            "connection": connection_name or config.default_connection,
            "total": len(databases),
            "databases": databases
        }
        
    except Exception as e:
        logger.error(f"Error listando bases de datos: {e}")
        return {
            "status": "error",
            "error": str(e)
        }


@mcp.tool()
def list_tables(connection_name: Optional[str] = None, database: Optional[str] = None) -> dict:
    """
    Lista todas las tablas de una base de datos.
    
    Obtiene la lista de todas las tablas disponibles en la base de datos especificada.
    Si no se especifica base de datos, usa la configurada en la conexión.
    
    Args:
        connection_name: Nombre de la conexión a usar. Si es None, usa la conexión por defecto.
        database: Nombre de la base de datos. Si es None, usa la de la conexión.
    
    Returns:
        dict: Lista de tablas y información de la base de datos
        
    Example:
        >>> list_tables()
        {
            'connection': 'mysql_local',
            'database': 'testdb',
            'total': 10,
            'tables': ['users', 'products', 'orders', ...]
        }
    """
    logger.info(f"Listando tablas: {connection_name or 'default'} / {database or 'default'}")
    
    try:
        config = get_config()
        # Crear handler
        if conn_config.type == 'mysql':
            handler = MySQLHandler(
                host=conn_config.host,
                port=conn_config.port,
                user=conn_config.user,
                password=conn_config.password,
                database=database or conn_config.database
            )
        elif conn_config.type in ('postgres', 'postgresql'):
            handler = PostgreSQLHandler(
                host=conn_config.host,
                port=conn_config.port,
                user=conn_config.user,
                password=conn_config.password,
                database=database or conn_config.database
            )
        else:
            return {
                "status": "error",
                "error": f"Tipo de base de datos '{conn_config.type}' no soportado"
            }
        
        # Listar tablas
        with handler:
            tables = handler.list_tables()
            return {
                "status": "error",
                "error": f"Tipo de base de datos '{conn_config.type}' no soportado aún"
            }
        
        # Listar tablas
        with handler:
            tables = handler.list_tables()
        
        return {
            "connection": connection_name or config.default_connection,
            "database": database or conn_config.database,
            "total": len(tables),
            "tables": tables
        }
        
    except Exception as e:
        logger.error(f"Error listando tablas: {e}")
        return {
            "status": "error",
            "error": str(e)
        }


# ============================================================================
# HERRAMIENTAS CRUD - CREATE (INSERT)
# ============================================================================

@mcp.tool()
def insert_record(
    table_name: str,
    data: dict,
    connection_name: Optional[str] = None
) -> dict:
    """
    Inserta un nuevo registro en una tabla de la base de datos.
    
    Esta herramienta permite agregar un nuevo registro con los datos especificados.
    Usa prepared statements para prevenir SQL injection.
    
    Args:
        table_name: Nombre de la tabla donde insertar
        data: Diccionario con los datos a insertar {columna: valor}
        connection_name: Nombre de la conexión (opcional, usa default si no se especifica)
    
    Returns:
        dict: Resultado con estado, filas afectadas y último ID insertado
        
    Example:
        >>> insert_record("users", {"name": "María García", "email": "maria@example.com", "age": 28})
        {
            "status": "success",
            "message": "Registro insertado en users",
            "rows_affected": 1,
            "last_insert_id": 15,
            "data": {"name": "María García", "email": "maria@example.com", "age": 28}
        }
    """
    logger.info(f"📝 Insertando registro en {table_name}")
    return crud_tools.insert_record(table_name, data, connection_name)


@mcp.tool()
def bulk_insert(
    table_name: str,
    records: list,
    connection_name: Optional[str] = None
) -> dict:
    """
    Inserta múltiples registros en una tabla de forma eficiente.
    
    Usa una transacción para insertar todos los registros. Si uno falla,
    se revierten todos los cambios (atomicidad).
    
    Args:
        table_name: Nombre de la tabla donde insertar
        records: Lista de diccionarios con los datos a insertar
        connection_name: Nombre de la conexión (opcional)
    
    Returns:
        dict: Resultado con cantidad de registros insertados
        
    Example:
        >>> bulk_insert("products", [
        ...     {"name": "Laptop", "price": 899.99, "stock": 5},
        ...     {"name": "Mouse", "price": 29.99, "stock": 50},
        ...     {"name": "Teclado", "price": 79.99, "stock": 25}
        ... ])
        {
            "status": "success",
            "message": "3 registros insertados en products",
            "rows_affected": 3,
            "records_count": 3
        }
    """
    logger.info(f"📝 Inserción masiva en {table_name}: {len(records)} registros")
    return crud_tools.bulk_insert(table_name, records, connection_name)


# ============================================================================
# HERRAMIENTAS CRUD - READ (SELECT)
# ============================================================================

@mcp.tool()
def select_records(
    table_name: str,
    columns: Optional[list] = None,
    where: Optional[dict] = None,
    limit: Optional[int] = None,
    order_by: Optional[str] = None,
    connection_name: Optional[str] = None
) -> dict:
    """
    Consulta registros de una tabla con filtros, ordenamiento y límites opcionales.
    
    Herramienta flexible para realizar consultas SELECT con múltiples opciones.
    
    Args:
        table_name: Nombre de la tabla a consultar
        columns: Lista de columnas a seleccionar (None = todas las columnas)
        where: Filtros como diccionario {columna: valor} (se unen con AND)
        limit: Número máximo de registros a devolver
        order_by: Ordenamiento (ej: "name ASC", "created_at DESC")
        connection_name: Nombre de la conexión (opcional)
    
    Returns:
        dict: Lista de registros encontrados
        
    Examples:
        >>> # Obtener todos los usuarios
        >>> select_records("users")
        
        >>> # Obtener solo nombre y email de usuarios activos
        >>> select_records("users", columns=["name", "email"], where={"active": 1})
        
        >>> # Top 10 productos más caros
        >>> select_records("products", limit=10, order_by="price DESC")
        
        >>> # Órdenes de un cliente específico
        >>> select_records("orders", where={"customer_id": 42, "status": "completed"})
    """
    logger.info(f"🔍 Consultando {table_name}")
    return crud_tools.select_records(table_name, columns, where, limit, order_by, connection_name)


@mcp.tool()
def get_record_by_id(
    table_name: str,
    id_value: Any,
    id_column: str = "id",
    connection_name: Optional[str] = None
) -> dict:
    """
    Obtiene un registro específico por su ID.
    
    Busca y devuelve un único registro identificado por su clave primaria.
    
    Args:
        table_name: Nombre de la tabla
        id_value: Valor del ID a buscar
        id_column: Nombre de la columna que contiene el ID (default: "id")
        connection_name: Nombre de la conexión (opcional)
    
    Returns:
        dict: Registro encontrado o mensaje si no existe
        
    Examples:
        >>> # Buscar usuario por ID
        >>> get_record_by_id("users", 42)
        
        >>> # Buscar producto por código
        >>> get_record_by_id("products", "PROD-123", id_column="product_code")
    """
    logger.info(f"🔍 Buscando en {table_name} donde {id_column}={id_value}")
    return crud_tools.get_record_by_id(table_name, id_value, id_column, connection_name)


@mcp.tool()
def count_records(
    table_name: str,
    where: Optional[dict] = None,
    connection_name: Optional[str] = None
) -> dict:
    """
    Cuenta el número de registros en una tabla con filtros opcionales.
    
    Útil para obtener estadísticas sin cargar todos los datos.
    
    Args:
        table_name: Nombre de la tabla
        where: Filtros opcionales {columna: valor}
        connection_name: Nombre de la conexión (opcional)
    
    Returns:
        dict: Cantidad de registros
        
    Examples:
        >>> # Total de usuarios
        >>> count_records("users")
        {"status": "success", "table": "users", "count": 1523}
        
        >>> # Usuarios activos
        >>> count_records("users", where={"active": 1})
        {"status": "success", "table": "users", "count": 1204, "filters": {"active": 1}}
        
        >>> # Órdenes pendientes
        >>> count_records("orders", where={"status": "pending"})
    """
    logger.info(f"🔢 Contando registros en {table_name}")
    return crud_tools.count_records(table_name, where, connection_name)


# ============================================================================
# HERRAMIENTAS CRUD - UPDATE
# ============================================================================

@mcp.tool()
def update_record(
    table_name: str,
    id_value: Any,
    data: dict,
    id_column: str = "id",
    connection_name: Optional[str] = None
) -> dict:
    """
    Actualiza un registro específico identificado por su ID.
    
    Modifica los campos especificados de un único registro.
    
    Args:
        table_name: Nombre de la tabla
        id_value: Valor del ID del registro a actualizar
        data: Diccionario con los campos a actualizar {columna: nuevo_valor}
        id_column: Nombre de la columna ID (default: "id")
        connection_name: Nombre de la conexión (opcional)
    
    Returns:
        dict: Resultado de la actualización
        
    Examples:
        >>> # Actualizar email de usuario
        >>> update_record("users", 42, {"email": "nuevo@example.com"})
        
        >>> # Actualizar múltiples campos
        >>> update_record("products", 10, {
        ...     "price": 149.99,
        ...     "stock": 25,
        ...     "updated_at": "2025-12-05"
        ... })
        
        >>> # Actualizar por código personalizado
        >>> update_record("items", "ITEM-999", {"status": "discontinued"}, id_column="item_code")
    """
    logger.info(f"✏️  Actualizando registro en {table_name} ({id_column}={id_value})")
    return crud_tools.update_record(table_name, id_value, data, id_column, connection_name)


@mcp.tool()
def update_records(
    table_name: str,
    data: dict,
    where: dict,
    connection_name: Optional[str] = None
) -> dict:
    """
    Actualiza múltiples registros que cumplan con los filtros especificados.
    
    Permite actualizar varios registros a la vez usando condiciones WHERE.
    REQUIERE filtros para prevenir actualizaciones accidentales de toda la tabla.
    
    Args:
        table_name: Nombre de la tabla
        data: Diccionario con los campos a actualizar {columna: nuevo_valor}
        where: Filtros REQUERIDOS {columna: valor}
        connection_name: Nombre de la conexión (opcional)
    
    Returns:
        dict: Cantidad de registros actualizados
        
    Examples:
        >>> # Desactivar usuarios inactivos
        >>> update_records("users", {"active": 0}, {"last_login": None})
        
        >>> # Aplicar descuento a categoría
        >>> update_records("products", {"discount": 10}, {"category": "electronics"})
        
        >>> # Actualizar estado de órdenes antiguas
        >>> update_records("orders", {"status": "archived"}, {"year": 2020})
    """
    logger.info(f"✏️  Actualización masiva en {table_name}")
    return crud_tools.update_records(table_name, data, where, connection_name)


# ============================================================================
# HERRAMIENTAS CRUD - DELETE
# ============================================================================

@mcp.tool()
def delete_record(
    table_name: str,
    id_value: Any,
    id_column: str = "id",
    connection_name: Optional[str] = None
) -> dict:
    """
    Elimina un registro específico identificado por su ID.
    
    Elimina permanentemente un único registro de la tabla.
    
    Args:
        table_name: Nombre de la tabla
        id_value: Valor del ID del registro a eliminar
        id_column: Nombre de la columna ID (default: "id")
        connection_name: Nombre de la conexión (opcional)
    
    Returns:
        dict: Confirmación de eliminación
        
    Examples:
        >>> # Eliminar usuario
        >>> delete_record("users", 42)
        {"status": "success", "message": "Registro eliminado de users", "rows_affected": 1}
        
        >>> # Eliminar por código personalizado
        >>> delete_record("temp_data", "TEMP-123", id_column="temp_id")
    """
    logger.info(f"🗑️  Eliminando registro de {table_name} ({id_column}={id_value})")
    return crud_tools.delete_record(table_name, id_value, id_column, connection_name)


@mcp.tool()
def delete_records(
    table_name: str,
    where: dict,
    connection_name: Optional[str] = None,
    confirm: bool = False
) -> dict:
    """
    Elimina múltiples registros que cumplan con los filtros especificados.
    
    ⚠️ OPERACIÓN DESTRUCTIVA: Requiere confirmación explícita (confirm=True).
    Primero ejecuta sin confirm para ver cuántos registros se eliminarán.
    
    Args:
        table_name: Nombre de la tabla
        where: Filtros REQUERIDOS {columna: valor}
        connection_name: Nombre de la conexión (opcional)
        confirm: DEBE ser True para ejecutar la eliminación
    
    Returns:
        dict: Confirmación o solicitud de confirmación
        
    Examples:
        >>> # Paso 1: Ver cuántos registros se eliminarían
        >>> delete_records("logs", {"created_at": "2020-01-01"})
        {
            "status": "confirmation_required",
            "message": "Esta operación requiere confirmación explícita",
            "warning": "Se eliminarán registros de logs con filtros: {'created_at': '2020-01-01'}",
            "action": "Agregar confirm=True para ejecutar"
        }
        
        >>> # Paso 2: Confirmar y ejecutar
        >>> delete_records("logs", {"created_at": "2020-01-01"}, confirm=True)
        {"status": "success", "message": "145 registros eliminados de logs", "rows_affected": 145}
    """
    logger.info(f"🗑️  Eliminación masiva en {table_name} (confirm={confirm})")
    return crud_tools.delete_records(table_name, where, connection_name, confirm)


# ============================================================================
# INICIALIZACIÓN Y PUNTO DE ENTRADA
# ============================================================================

def main():
    """
    Función principal para iniciar el servidor MCP.
    """
    try:
        logger.info("=" * 70)
        logger.info("🗄️  DATABASE-CONNECT MCP SERVER v0.1.0")
        logger.info("=" * 70)
        logger.info("Iniciando servidor MCP...")
        logger.info(f"Python: {sys.version}")
        logger.info(f"Working directory: {os.getcwd()}")

        
        # Verificar configuración
        config_path = os.getenv('DB_CONFIG_PATH', 'config/settings.json')
        logger.info(f"Config path: {config_path}")
        
        if not Path(config_path).exists():
            logger.warning(f"⚠️  Archivo de configuración no encontrado: {config_path}")
            logger.warning("El servidor iniciará pero necesitará configuración")
        else:
            logger.info("✅ Archivo de configuración encontrado")
        
        # Iniciar servidor
        logger.info("🚀 Servidor MCP listo y esperando conexiones...")
        logger.info("=" * 70)
        
        # FastMCP maneja automáticamente la comunicación stdio
        mcp.run()
        
    except Exception as e:
        logger.error(f"❌ Error al iniciar servidor: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
