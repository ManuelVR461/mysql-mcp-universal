"""
Manejador de conexiones MySQL.
"""

import pymysql
from pymysql.cursors import DictCursor
from typing import List, Dict, Any, Optional
import logging
from .connection import DatabaseHandler

logger = logging.getLogger(__name__)


class MySQLHandler(DatabaseHandler):
    """
    Manejador específico para bases de datos MySQL.
    Utiliza PyMySQL para la conexión.
    """
    
    def __init__(self, host: str, port: int, user: str, password: str, database: Optional[str] = None):
        """
        Inicializa el manejador MySQL.
        
        Args:
            host: Host del servidor MySQL
            port: Puerto de conexión (típicamente 3306)
            user: Usuario de MySQL
            password: Contraseña del usuario
            database: Nombre de la base de datos (opcional)
        """
        super().__init__(host, port, user, password, database)
        self.cursor = None
    
    def connect(self) -> None:
        """Establece conexión con MySQL"""
        try:
            self.connection = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                cursorclass=DictCursor,
                charset='utf8mb4',
                autocommit=False
            )
            self.cursor = self.connection.cursor()
            self._is_connected = True
            logger.info(f"✅ Conexión MySQL establecida: {self.host}:{self.port}/{self.database or 'sin BD'}")
            
        except pymysql.Error as e:
            self._is_connected = False
            logger.error(f"❌ Error conectando a MySQL: {e}")
            raise
    
    def disconnect(self) -> None:
        """Cierra la conexión con MySQL"""
        try:
            if self.cursor:
                self.cursor.close()
                self.cursor = None
            
            if self.connection:
                self.connection.close()
                self.connection = None
            
            self._is_connected = False
            logger.info(f"🔌 Conexión MySQL cerrada: {self.host}:{self.port}")
            
        except Exception as e:
            logger.error(f"❌ Error cerrando conexión MySQL: {e}")
    
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
                affected = self.cursor.execute(query, params)
            else:
                affected = self.cursor.execute(query)
            
            logger.debug(f"Query ejecutado: {query[:100]}... | Filas afectadas: {affected}")
            return affected
            
        except pymysql.Error as e:
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
            logger.debug(f"Fetch one: {query[:100]}... | Resultado: {'Encontrado' if result else 'None'}")
            return result
            
        except pymysql.Error as e:
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
            logger.debug(f"Fetch all: {query[:100]}... | Resultados: {len(results)} filas")
            return results
            
        except pymysql.Error as e:
            logger.error(f"❌ Error en fetch_all: {e}")
            raise
    
    def begin_transaction(self) -> None:
        """Inicia una transacción"""
        self.ensure_connected()
        try:
            self.connection.begin()
            logger.debug("🔄 Transacción iniciada")
        except pymysql.Error as e:
            logger.error(f"❌ Error iniciando transacción: {e}")
            raise
    
    def commit(self) -> None:
        """Confirma la transacción actual"""
        if self.connection:
            try:
                self.connection.commit()
                logger.debug("✅ Transacción confirmada (commit)")
            except pymysql.Error as e:
                logger.error(f"❌ Error en commit: {e}")
                raise
    
    def rollback(self) -> None:
        """Revierte la transacción actual"""
        if self.connection:
            try:
                self.connection.rollback()
                logger.debug("↩️  Transacción revertida (rollback)")
            except pymysql.Error as e:
                logger.error(f"❌ Error en rollback: {e}")
                raise
    
    def get_last_insert_id(self) -> Optional[int]:
        """
        Obtiene el ID del último registro insertado.
        
        Returns:
            ID del último insert o None
        """
        if self.cursor:
            return self.cursor.lastrowid
        return None
    
    def list_databases(self) -> List[str]:
        """
        Lista todas las bases de datos disponibles.
        
        Returns:
            Lista de nombres de bases de datos
        """
        results = self.fetch_all("SHOW DATABASES")
        return [row['Database'] for row in results]
    
    def list_tables(self, database: Optional[str] = None) -> List[str]:
        """
        Lista todas las tablas de una base de datos.
        
        Args:
            database: Nombre de la base de datos (usa la actual si es None)
        
        Returns:
            Lista de nombres de tablas
        """
        if database:
            query = f"SHOW TABLES FROM `{database}`"
        else:
            query = "SHOW TABLES"
        
        results = self.fetch_all(query)
        
        # La clave del diccionario varía según la base de datos
        if results:
            key = list(results[0].keys())[0]
            return [row[key] for row in results]
        return []
    
    def get_table_schema(self, table_name: str) -> List[Dict[str, Any]]:
        """
        Obtiene el esquema de una tabla.
        
        Args:
            table_name: Nombre de la tabla
        
        Returns:
            Lista con información de las columnas
        """
        query = f"DESCRIBE `{table_name}`"
        return self.fetch_all(query)
    
    def get_server_version(self) -> str:
        """
        Obtiene la versión del servidor MySQL.
        
        Returns:
            Versión del servidor
        """
        result = self.fetch_one("SELECT VERSION() as version")
        return result['version'] if result else "Unknown"
