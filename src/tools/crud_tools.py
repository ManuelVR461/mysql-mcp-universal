"""
Herramientas CRUD (Create, Read, Update, Delete) para operaciones básicas en bases de datos.
"""

from typing import Dict, Any, List, Optional
import logging

# Imports flexibles para soportar ejecución directa y como módulo
try:
    from ..config import get_config
    from ..database.mysql_handler import MySQLHandler
    from ..database.postgres_handler import PostgreSQLHandler
except ImportError:
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    from config import get_config
    from database.mysql_handler import MySQLHandler
    from database.postgres_handler import PostgreSQLHandler

logger = logging.getLogger(__name__)


def _get_handler(connection_name: Optional[str] = None):
    """
    Función auxiliar para obtener el handler de base de datos apropiado.
    
    Args:
        connection_name: Nombre de la conexión (None = usar default)
    
    Returns:
        DatabaseHandler instance
    
    Raises:
        ValueError: Si la conexión no existe o el tipo no es soportado
    """
    config = get_config()
    conn_config = config.get_connection(connection_name)
    
    if not conn_config:
        available = list(config.list_connections().keys())
        raise ValueError(
            f"Conexión '{connection_name}' no encontrada. "
            f"Conexiones disponibles: {', '.join(available)}"
        )
    
    # Crear handler según el tipo
    if conn_config.type == 'mysql':
        return MySQLHandler(
            host=conn_config.host,
            port=conn_config.port,
            user=conn_config.user,
            password=conn_config.password,
            database=conn_config.database
        )
    elif conn_config.type in ('postgres', 'postgresql'):
        return PostgreSQLHandler(
            host=conn_config.host,
            port=conn_config.port,
            user=conn_config.user,
            password=conn_config.password,
            database=conn_config.database
        )
    else:
        raise ValueError(f"Tipo de base de datos '{conn_config.type}' no soportado")


def _build_where_clause(where_dict: Optional[Dict[str, Any]] = None) -> tuple:
    """
    Construye una cláusula WHERE desde un diccionario.
    
    Args:
        where_dict: Diccionario con condiciones {columna: valor}
    
    Returns:
        Tupla (where_clause, params)
    """
    if not where_dict:
        return "", ()
    
    conditions = []
    params = []
    
    for key, value in where_dict.items():
        conditions.append(f"{key} = %s")
        params.append(value)
    
    where_clause = " WHERE " + " AND ".join(conditions)
    return where_clause, tuple(params)


# ============================================================================
# CREATE - Operaciones de INSERT
# ============================================================================

def insert_record(
    table_name: str,
    data: Dict[str, Any],
    connection_name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Inserta un nuevo registro en una tabla.
    
    Args:
        table_name: Nombre de la tabla
        data: Diccionario con columna:valor a insertar
        connection_name: Nombre de la conexión (None = usar default)
    
    Returns:
        Dict con el resultado de la inserción
        
    Example:
        insert_record("users", {"name": "John", "email": "john@example.com"})
    """
    try:
        handler = _get_handler(connection_name)
        
        # Construir query
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        params = tuple(data.values())
        
        with handler:
            affected = handler.execute_query(query, params)
            handler.commit()
            last_id = handler.get_last_insert_id()
        
        logger.info(f"✅ Registro insertado en {table_name}")
        
        return {
            "status": "success",
            "message": f"Registro insertado en {table_name}",
            "rows_affected": affected,
            "last_insert_id": last_id,
            "data": data
        }
        
    except Exception as e:
        logger.error(f"❌ Error insertando en {table_name}: {e}")
        return {
            "status": "error",
            "error": str(e),
            "table": table_name
        }


def bulk_insert(
    table_name: str,
    records: List[Dict[str, Any]],
    connection_name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Inserta múltiples registros en una tabla.
    
    Args:
        table_name: Nombre de la tabla
        records: Lista de diccionarios con los datos
        connection_name: Nombre de la conexión (None = usar default)
    
    Returns:
        Dict con el resultado de la inserción
        
    Example:
        bulk_insert("users", [
            {"name": "John", "email": "john@example.com"},
            {"name": "Jane", "email": "jane@example.com"}
        ])
    """
    try:
        if not records:
            return {
                "status": "error",
                "error": "No hay registros para insertar"
            }
        
        handler = _get_handler(connection_name)
        
        # Usar las columnas del primer registro
        columns = ', '.join(records[0].keys())
        placeholders = ', '.join(['%s'] * len(records[0]))
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        
        # Preparar lista de parámetros
        params_list = [tuple(record.values()) for record in records]
        
        with handler:
            total_affected = handler.execute_many(query, params_list)
        
        logger.info(f"✅ {len(records)} registros insertados en {table_name}")
        
        return {
            "status": "success",
            "message": f"{len(records)} registros insertados en {table_name}",
            "rows_affected": total_affected,
            "records_count": len(records)
        }
        
    except Exception as e:
        logger.error(f"❌ Error en inserción masiva en {table_name}: {e}")
        return {
            "status": "error",
            "error": str(e),
            "table": table_name
        }


# ============================================================================
# READ - Operaciones de SELECT
# ============================================================================

def select_records(
    table_name: str,
    columns: Optional[List[str]] = None,
    where: Optional[Dict[str, Any]] = None,
    limit: Optional[int] = None,
    order_by: Optional[str] = None,
    connection_name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Selecciona registros de una tabla con filtros opcionales.
    
    Args:
        table_name: Nombre de la tabla
        columns: Lista de columnas a seleccionar (None = todas)
        where: Diccionario con filtros {columna: valor}
        limit: Número máximo de registros
        order_by: Columna para ordenar (ej: "name ASC", "id DESC")
        connection_name: Nombre de la conexión (None = usar default)
    
    Returns:
        Dict con los registros encontrados
        
    Example:
        select_records("users", columns=["name", "email"], where={"active": 1}, limit=10)
    """
    try:
        handler = _get_handler(connection_name)
        
        # Construir query
        cols = ', '.join(columns) if columns else '*'
        query = f"SELECT {cols} FROM {table_name}"
        
        # Agregar WHERE
        where_clause, params = _build_where_clause(where)
        query += where_clause
        
        # Agregar ORDER BY
        if order_by:
            query += f" ORDER BY {order_by}"
        
        # Agregar LIMIT
        if limit:
            query += f" LIMIT {limit}"
        
        with handler:
            records = handler.fetch_all(query, params if params else None)
        
        logger.info(f"✅ {len(records)} registros obtenidos de {table_name}")
        
        return {
            "status": "success",
            "table": table_name,
            "count": len(records),
            "records": records
        }
        
    except Exception as e:
        logger.error(f"❌ Error consultando {table_name}: {e}")
        return {
            "status": "error",
            "error": str(e),
            "table": table_name
        }


def get_record_by_id(
    table_name: str,
    id_value: Any,
    id_column: str = "id",
    connection_name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Obtiene un registro por su ID.
    
    Args:
        table_name: Nombre de la tabla
        id_value: Valor del ID a buscar
        id_column: Nombre de la columna ID (default: "id")
        connection_name: Nombre de la conexión (None = usar default)
    
    Returns:
        Dict con el registro encontrado
        
    Example:
        get_record_by_id("users", 42)
    """
    try:
        handler = _get_handler(connection_name)
        
        query = f"SELECT * FROM {table_name} WHERE {id_column} = %s"
        
        with handler:
            record = handler.fetch_one(query, (id_value,))
        
        if record:
            logger.info(f"✅ Registro encontrado en {table_name} con {id_column}={id_value}")
            return {
                "status": "success",
                "table": table_name,
                "found": True,
                "record": record
            }
        else:
            logger.info(f"ℹ️  No se encontró registro en {table_name} con {id_column}={id_value}")
            return {
                "status": "success",
                "table": table_name,
                "found": False,
                "message": f"No se encontró registro con {id_column}={id_value}"
            }
        
    except Exception as e:
        logger.error(f"❌ Error buscando en {table_name}: {e}")
        return {
            "status": "error",
            "error": str(e),
            "table": table_name
        }


def count_records(
    table_name: str,
    where: Optional[Dict[str, Any]] = None,
    connection_name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Cuenta registros en una tabla con filtros opcionales.
    
    Args:
        table_name: Nombre de la tabla
        where: Diccionario con filtros {columna: valor}
        connection_name: Nombre de la conexión (None = usar default)
    
    Returns:
        Dict con el conteo
        
    Example:
        count_records("users", where={"active": 1})
    """
    try:
        handler = _get_handler(connection_name)
        
        query = f"SELECT COUNT(*) as total FROM {table_name}"
        where_clause, params = _build_where_clause(where)
        query += where_clause
        
        with handler:
            result = handler.fetch_one(query, params if params else None)
        
        total = result['total'] if result else 0
        logger.info(f"✅ Conteo en {table_name}: {total} registros")
        
        return {
            "status": "success",
            "table": table_name,
            "count": total,
            "filters": where
        }
        
    except Exception as e:
        logger.error(f"❌ Error contando en {table_name}: {e}")
        return {
            "status": "error",
            "error": str(e),
            "table": table_name
        }


# ============================================================================
# UPDATE - Operaciones de UPDATE
# ============================================================================

def update_record(
    table_name: str,
    id_value: Any,
    data: Dict[str, Any],
    id_column: str = "id",
    connection_name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Actualiza un registro específico por su ID.
    
    Args:
        table_name: Nombre de la tabla
        id_value: Valor del ID del registro a actualizar
        data: Diccionario con los campos a actualizar
        id_column: Nombre de la columna ID (default: "id")
        connection_name: Nombre de la conexión (None = usar default)
    
    Returns:
        Dict con el resultado de la actualización
        
    Example:
        update_record("users", 42, {"email": "newemail@example.com", "active": 1})
    """
    try:
        handler = _get_handler(connection_name)
        
        # Construir SET clause
        set_parts = [f"{key} = %s" for key in data.keys()]
        set_clause = ", ".join(set_parts)
        
        query = f"UPDATE {table_name} SET {set_clause} WHERE {id_column} = %s"
        params = tuple(list(data.values()) + [id_value])
        
        with handler:
            affected = handler.execute_query(query, params)
            handler.commit()
        
        if affected > 0:
            logger.info(f"✅ Registro actualizado en {table_name} ({id_column}={id_value})")
            return {
                "status": "success",
                "message": f"Registro actualizado en {table_name}",
                "rows_affected": affected,
                "id": id_value,
                "updated_data": data
            }
        else:
            logger.info(f"ℹ️  No se encontró registro en {table_name} con {id_column}={id_value}")
            return {
                "status": "success",
                "message": f"No se encontró registro con {id_column}={id_value}",
                "rows_affected": 0
            }
        
    except Exception as e:
        logger.error(f"❌ Error actualizando {table_name}: {e}")
        return {
            "status": "error",
            "error": str(e),
            "table": table_name
        }


def update_records(
    table_name: str,
    data: Dict[str, Any],
    where: Dict[str, Any],
    connection_name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Actualiza múltiples registros con filtro WHERE.
    
    Args:
        table_name: Nombre de la tabla
        data: Diccionario con los campos a actualizar
        where: Diccionario con filtros {columna: valor}
        connection_name: Nombre de la conexión (None = usar default)
    
    Returns:
        Dict con el resultado de la actualización
        
    Example:
        update_records("users", {"active": 0}, {"status": "inactive"})
    """
    try:
        if not where:
            return {
                "status": "error",
                "error": "Se requiere condición WHERE para actualizar múltiples registros"
            }
        
        handler = _get_handler(connection_name)
        
        # Construir SET clause
        set_parts = [f"{key} = %s" for key in data.keys()]
        set_clause = ", ".join(set_parts)
        
        # Construir WHERE clause
        where_clause, where_params = _build_where_clause(where)
        
        query = f"UPDATE {table_name} SET {set_clause}{where_clause}"
        params = tuple(list(data.values()) + list(where_params))
        
        with handler:
            affected = handler.execute_query(query, params)
            handler.commit()
        
        logger.info(f"✅ {affected} registros actualizados en {table_name}")
        
        return {
            "status": "success",
            "message": f"{affected} registros actualizados en {table_name}",
            "rows_affected": affected,
            "updated_data": data,
            "filters": where
        }
        
    except Exception as e:
        logger.error(f"❌ Error actualizando registros en {table_name}: {e}")
        return {
            "status": "error",
            "error": str(e),
            "table": table_name
        }


# ============================================================================
# DELETE - Operaciones de DELETE
# ============================================================================

def delete_record(
    table_name: str,
    id_value: Any,
    id_column: str = "id",
    connection_name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Elimina un registro específico por su ID.
    
    Args:
        table_name: Nombre de la tabla
        id_value: Valor del ID del registro a eliminar
        id_column: Nombre de la columna ID (default: "id")
        connection_name: Nombre de la conexión (None = usar default)
    
    Returns:
        Dict con el resultado de la eliminación
        
    Example:
        delete_record("users", 42)
    """
    try:
        handler = _get_handler(connection_name)
        
        query = f"DELETE FROM {table_name} WHERE {id_column} = %s"
        
        with handler:
            affected = handler.execute_query(query, (id_value,))
            handler.commit()
        
        if affected > 0:
            logger.info(f"✅ Registro eliminado de {table_name} ({id_column}={id_value})")
            return {
                "status": "success",
                "message": f"Registro eliminado de {table_name}",
                "rows_affected": affected,
                "deleted_id": id_value
            }
        else:
            logger.info(f"ℹ️  No se encontró registro en {table_name} con {id_column}={id_value}")
            return {
                "status": "success",
                "message": f"No se encontró registro con {id_column}={id_value}",
                "rows_affected": 0
            }
        
    except Exception as e:
        logger.error(f"❌ Error eliminando de {table_name}: {e}")
        return {
            "status": "error",
            "error": str(e),
            "table": table_name
        }


def delete_records(
    table_name: str,
    where: Dict[str, Any],
    connection_name: Optional[str] = None,
    confirm: bool = False
) -> Dict[str, Any]:
    """
    Elimina múltiples registros con filtro WHERE.
    REQUIERE confirmación explícita para prevenir eliminaciones accidentales.
    
    Args:
        table_name: Nombre de la tabla
        where: Diccionario con filtros {columna: valor}
        connection_name: Nombre de la conexión (None = usar default)
        confirm: DEBE ser True para ejecutar la eliminación
    
    Returns:
        Dict con el resultado de la eliminación
        
    Example:
        delete_records("users", {"active": 0}, confirm=True)
    """
    try:
        if not where:
            return {
                "status": "error",
                "error": "Se requiere condición WHERE para eliminar múltiples registros"
            }
        
        if not confirm:
            return {
                "status": "confirmation_required",
                "message": "Esta operación requiere confirmación explícita",
                "warning": f"Se eliminarán registros de {table_name} con filtros: {where}",
                "action": "Agregar confirm=True para ejecutar"
            }
        
        handler = _get_handler(connection_name)
        
        # Primero contar cuántos se van a eliminar
        count_query = f"SELECT COUNT(*) as total FROM {table_name}"
        where_clause, params = _build_where_clause(where)
        count_query += where_clause
        
        with handler:
            result = handler.fetch_one(count_query, params)
            to_delete = result['total'] if result else 0
            
            if to_delete == 0:
                return {
                    "status": "success",
                    "message": "No se encontraron registros para eliminar",
                    "rows_affected": 0
                }
            
            # Ejecutar DELETE
            delete_query = f"DELETE FROM {table_name}{where_clause}"
            affected = handler.execute_query(delete_query, params)
            handler.commit()
        
        logger.info(f"✅ {affected} registros eliminados de {table_name}")
        
        return {
            "status": "success",
            "message": f"{affected} registros eliminados de {table_name}",
            "rows_affected": affected,
            "filters": where
        }
        
    except Exception as e:
        logger.error(f"❌ Error eliminando registros de {table_name}: {e}")
        return {
            "status": "error",
            "error": str(e),
            "table": table_name
        }
