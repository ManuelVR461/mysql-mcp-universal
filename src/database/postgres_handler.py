"""
Manejador de conexiones PostgreSQL.
"""

import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Dict, Any, Optional
import logging
from .connection import DatabaseHandler

logger = logging.getLogger(__name__)


class PostgreSQLHandler(DatabaseHandler):
    """
    Manejador específico para bases de datos PostgreSQL.
    Utiliza psycopg2 para la conexión.
    """
    
    def __init__(self, host: str, port: int, user: str, password: str, database: Optional[str] = None):
        """
        Inicializa el manejador PostgreSQL.
        
        Args:
            host: Host del servidor PostgreSQL
            port: Puerto de conexión (típicamente 5432)
            user: Usuario de PostgreSQL
            password: Contraseña del usuario
            database: Nombre de la base de datos (opcional)
        """
        super().__init__(host, port, user, password, database)
        self.cursor = None
    
    def connect(self) -> None:
        """Establece conexión con PostgreSQL"""
        try:
            # Construir string de conexión
            conn_params = {
                'host': self.host,
                'port': self.port,
                'user': self.user,
                'password': self.password,
            }
            
            if self.database:
                conn_params['database'] = self.database
            
            self.connection = psycopg2.connect(
                **conn_params,
                cursor_factory=RealDictCursor
            )
            self.cursor = self.connection.cursor()
            self._is_connected = True
            logger.info(f"✅ Conexión PostgreSQL establecida: {self.host}:{self.port}/{self.database or 'sin BD'}")
            
        except psycopg2.Error as e:
            self._is_connected = False
            logger.error(f"❌ Error conectando a PostgreSQL: {e}")
            raise
    
    def disconnect(self) -> None:
        """Cierra la conexión con PostgreSQL"""
        try:
            if self.cursor:
                self.cursor.close()
                self.cursor = None
            
            if self.connection:
                self.connection.close()
                self.connection = None
            
            self._is_connected = False
            logger.info(f"🔌 Conexión PostgreSQL cerrada: {self.host}:{self.port}")
            
        except Exception as e:
            logger.error(f"❌ Error cerrando conexión PostgreSQL: {e}")
    
    def execute_query(self, query: str, params: Optional[tuple] = None) -> int:
        """
        Ejecuta una consulta que modifica datos.
        
        Args:
            query: Consulta SQL
            params: Parámetros de la consulta (opcional)
        
        Returns:
            Número de filas afectadas
        """
        self.ensure_connected()
        
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            affected = self.cursor.rowcount
            logger.debug(f"Query ejecutado: {query[:100]}... | Filas afectadas: {affected}")
            return affected
            
        except psycopg2.Error as e:
            logger.error(f"❌ Error ejecutando query: {e}")
            raise
    
    def fetch_one(self, query: str, params: Optional[tuple] = None) -> Optional[Dict[str, Any]]:
        """
        Ejecuta una consulta y devuelve un solo resultado.
        
        Args:
            query: Consulta SQL
            params: Parámetros de la consulta (opcional)
        
        Returns:
            Diccionario con el resultado o None
        """
        self.ensure_connected()
        
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            result = self.cursor.fetchone()
            # Convertir RealDictRow a dict normal
            if result:
                result = dict(result)
            
            logger.debug(f"Fetch one: {query[:100]}... | Resultado: {'Encontrado' if result else 'None'}")
            return result
            
        except psycopg2.Error as e:
            logger.error(f"❌ Error en fetch_one: {e}")
            raise
    
    def fetch_all(self, query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """
        Ejecuta una consulta y devuelve todos los resultados.
        
        Args:
            query: Consulta SQL
            params: Parámetros de la consulta (opcional)
        
        Returns:
            Lista de diccionarios con los resultados
        """
        self.ensure_connected()
        
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            results = self.cursor.fetchall()
            # Convertir RealDictRow a dict normal
            results = [dict(row) for row in results]
            
            logger.debug(f"Fetch all: {query[:100]}... | Resultados: {len(results)} filas")
            return results
            
        except psycopg2.Error as e:
            logger.error(f"❌ Error en fetch_all: {e}")
            raise
    
    def begin_transaction(self) -> None:
        """Inicia una transacción"""
        self.ensure_connected()
        # PostgreSQL inicia transacciones automáticamente
        # Solo necesitamos asegurarnos de no estar en autocommit
        try:
            self.connection.autocommit = False
            logger.debug("🔄 Transacción iniciada")
        except psycopg2.Error as e:
            logger.error(f"❌ Error iniciando transacción: {e}")
            raise
    
    def commit(self) -> None:
        """Confirma la transacción actual"""
        if self.connection:
            try:
                self.connection.commit()
                logger.debug("✅ Transacción confirmada (commit)")
            except psycopg2.Error as e:
                logger.error(f"❌ Error en commit: {e}")
                raise
    
    def rollback(self) -> None:
        """Revierte la transacción actual"""
        if self.connection:
            try:
                self.connection.rollback()
                logger.debug("↩️  Transacción revertida (rollback)")
            except psycopg2.Error as e:
                logger.error(f"❌ Error en rollback: {e}")
                raise
    
    def get_last_insert_id(self) -> Optional[int]:
        """
        Obtiene el ID del último registro insertado.
        En PostgreSQL, usar RETURNING id en el INSERT.
        
        Returns:
            ID del último insert o None
        """
        # En PostgreSQL se usa RETURNING en el INSERT
        # Esta función es más un placeholder
        return None
    
    def list_databases(self) -> List[str]:
        """
        Lista todas las bases de datos disponibles.
        
        Returns:
            Lista de nombres de bases de datos
        """
        query = """
            SELECT datname 
            FROM pg_database 
            WHERE datistemplate = false
            ORDER BY datname
        """
        results = self.fetch_all(query)
        return [row['datname'] for row in results]
    
    def list_tables(self, database: Optional[str] = None, schema: str = 'public') -> List[str]:
        """
        Lista todas las tablas de un esquema.
        
        Args:
            database: Nombre de la base de datos (no usado, debe conectarse antes)
            schema: Nombre del esquema (por defecto 'public')
        
        Returns:
            Lista de nombres de tablas
        """
        query = """
            SELECT tablename 
            FROM pg_tables 
            WHERE schemaname = %s
            ORDER BY tablename
        """
        results = self.fetch_all(query, (schema,))
        return [row['tablename'] for row in results]
    
    def get_table_schema(self, table_name: str, schema: str = 'public') -> List[Dict[str, Any]]:
        """
        Obtiene el esquema de una tabla.
        
        Args:
            table_name: Nombre de la tabla
            schema: Nombre del esquema (por defecto 'public')
        
        Returns:
            Lista con información de las columnas
        """
        query = """
            SELECT 
                column_name,
                data_type,
                character_maximum_length,
                column_default,
                is_nullable,
                ordinal_position
            FROM information_schema.columns
            WHERE table_schema = %s 
            AND table_name = %s
            ORDER BY ordinal_position
        """
        return self.fetch_all(query, (schema, table_name))
    
    def get_server_version(self) -> str:
        """
        Obtiene la versión del servidor PostgreSQL.
        
        Returns:
            Versión del servidor
        """
        result = self.fetch_one("SELECT version() as version")
        return result['version'] if result else "Unknown"
    
    def list_schemas(self) -> List[str]:
        """
        Lista todos los esquemas disponibles.
        
        Returns:
            Lista de nombres de esquemas
        """
        query = """
            SELECT schema_name 
            FROM information_schema.schemata
            WHERE schema_name NOT IN ('pg_catalog', 'information_schema')
            ORDER BY schema_name
        """
        results = self.fetch_all(query)
        return [row['schema_name'] for row in results]
