"""
Gestión de conexiones a bases de datos.
Proporciona una interfaz unificada para MySQL y PostgreSQL.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Tuple
import logging
from contextlib import contextmanager

logger = logging.getLogger(__name__)


class DatabaseHandler(ABC):
    """
    Clase base abstracta para manejadores de bases de datos.
    Define la interfaz común para todos los tipos de bases de datos.
    """
    
    def __init__(self, host: str, port: int, user: str, password: str, database: Optional[str] = None):
        """
        Inicializa el manejador de base de datos.
        
        Args:
            host: Host del servidor de base de datos
            port: Puerto de conexión
            user: Usuario de la base de datos
            password: Contraseña del usuario
            database: Nombre de la base de datos (opcional)
        """
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self._is_connected = False
        
        logger.info(f"Inicializando manejador para {self.__class__.__name__}")
    
    @abstractmethod
    def connect(self) -> None:
        """Establece conexión con la base de datos"""
        pass
    
    @abstractmethod
    def disconnect(self) -> None:
        """Cierra la conexión con la base de datos"""
        pass
    
    @abstractmethod
    def execute_query(self, query: str, params: Optional[tuple] = None) -> int:
        """
        Ejecuta una consulta que modifica datos (INSERT, UPDATE, DELETE).
        
        Args:
            query: Consulta SQL
            params: Parámetros de la consulta (opcional)
        
        Returns:
            Número de filas afectadas
        """
        pass
    
    @abstractmethod
    def fetch_one(self, query: str, params: Optional[tuple] = None) -> Optional[Dict[str, Any]]:
        """
        Ejecuta una consulta y devuelve un solo resultado.
        
        Args:
            query: Consulta SQL
            params: Parámetros de la consulta (opcional)
        
        Returns:
            Diccionario con el resultado o None
        """
        pass
    
    @abstractmethod
    def fetch_all(self, query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """
        Ejecuta una consulta y devuelve todos los resultados.
        
        Args:
            query: Consulta SQL
            params: Parámetros de la consulta (opcional)
        
        Returns:
            Lista de diccionarios con los resultados
        """
        pass
    
    @abstractmethod
    def begin_transaction(self) -> None:
        """Inicia una transacción"""
        pass
    
    @abstractmethod
    def commit(self) -> None:
        """Confirma la transacción actual"""
        pass
    
    @abstractmethod
    def rollback(self) -> None:
        """Revierte la transacción actual"""
        pass
    
    @abstractmethod
    def get_last_insert_id(self) -> Optional[int]:
        """
        Obtiene el ID del último registro insertado.
        
        Returns:
            ID del último insert o None
        """
        pass
    
    @property
    def is_connected(self) -> bool:
        """Indica si hay una conexión activa"""
        return self._is_connected
    
    def ensure_connected(self) -> None:
        """Asegura que existe una conexión activa, reconectando si es necesario"""
        if not self.is_connected:
            logger.info("Reconectando a la base de datos...")
            self.connect()
    
    @contextmanager
    def transaction(self):
        """
        Context manager para ejecutar operaciones en una transacción.
        
        Example:
            with handler.transaction():
                handler.execute_query("INSERT INTO users ...")
                handler.execute_query("UPDATE stats ...")
        """
        self.ensure_connected()
        self.begin_transaction()
        try:
            yield self
            self.commit()
            logger.info("✅ Transacción completada exitosamente")
        except Exception as e:
            self.rollback()
            logger.error(f"❌ Error en transacción, rollback ejecutado: {e}")
            raise
    
    def execute_many(self, query: str, params_list: List[tuple]) -> int:
        """
        Ejecuta una consulta múltiples veces con diferentes parámetros.
        
        Args:
            query: Consulta SQL
            params_list: Lista de tuplas con parámetros
        
        Returns:
            Número total de filas afectadas
        """
        total_affected = 0
        with self.transaction():
            for params in params_list:
                affected = self.execute_query(query, params)
                total_affected += affected
        return total_affected
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Prueba la conexión a la base de datos.
        
        Returns:
            Dict con información sobre la conexión
        """
        try:
            self.connect()
            
            # Ejecutar query simple de prueba
            result = self.fetch_one("SELECT 1 as test")
            
            info = {
                "status": "connected",
                "host": self.host,
                "port": self.port,
                "user": self.user,
                "database": self.database,
                "test_query": result is not None
            }
            
            logger.info(f"✅ Conexión exitosa: {self.host}:{self.port}")
            return info
            
        except Exception as e:
            logger.error(f"❌ Error al probar conexión: {e}")
            return {
                "status": "error",
                "error": str(e),
                "host": self.host,
                "port": self.port
            }
    
    def __enter__(self):
        """Soporte para context manager"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Cierra conexión al salir del context manager"""
        self.disconnect()
        return False
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(host={self.host}, port={self.port}, user={self.user}, database={self.database})"


class ConnectionPool:
    """
    Pool de conexiones para reutilizar conexiones a bases de datos.
    """
    
    def __init__(self, max_connections: int = 5):
        """
        Inicializa el pool de conexiones.
        
        Args:
            max_connections: Número máximo de conexiones en el pool
        """
        self.max_connections = max_connections
        self._pools: Dict[str, List[DatabaseHandler]] = {}
        logger.info(f"Pool de conexiones inicializado (max: {max_connections})")
    
    def get_connection(self, connection_name: str, handler_class, **kwargs) -> DatabaseHandler:
        """
        Obtiene una conexión del pool o crea una nueva.
        
        Args:
            connection_name: Nombre de la conexión
            handler_class: Clase del manejador (MySQLHandler o PostgreSQLHandler)
            **kwargs: Argumentos para crear el manejador
        
        Returns:
            DatabaseHandler: Instancia del manejador
        """
        # Crear pool para esta conexión si no existe
        if connection_name not in self._pools:
            self._pools[connection_name] = []
        
        pool = self._pools[connection_name]
        
        # Buscar conexión disponible
        for handler in pool:
            if handler.is_connected:
                logger.debug(f"Reutilizando conexión existente: {connection_name}")
                return handler
        
        # Crear nueva conexión si hay espacio
        if len(pool) < self.max_connections:
            handler = handler_class(**kwargs)
            handler.connect()
            pool.append(handler)
            logger.info(f"Nueva conexión creada en pool: {connection_name} ({len(pool)}/{self.max_connections})")
            return handler
        
        # Si el pool está lleno, usar la primera disponible
        logger.warning(f"Pool lleno para {connection_name}, reutilizando conexión")
        return pool[0]
    
    def close_all(self, connection_name: Optional[str] = None) -> None:
        """
        Cierra todas las conexiones de un pool o de todos los pools.
        
        Args:
            connection_name: Nombre de la conexión (None para cerrar todas)
        """
        if connection_name:
            if connection_name in self._pools:
                for handler in self._pools[connection_name]:
                    handler.disconnect()
                self._pools[connection_name].clear()
                logger.info(f"Pool cerrado: {connection_name}")
        else:
            for name, pool in self._pools.items():
                for handler in pool:
                    handler.disconnect()
                pool.clear()
            self._pools.clear()
            logger.info("Todos los pools cerrados")
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas de los pools.
        
        Returns:
            Dict con estadísticas
        """
        stats = {
            "total_pools": len(self._pools),
            "max_connections": self.max_connections,
            "pools": {}
        }
        
        for name, pool in self._pools.items():
            stats["pools"][name] = {
                "total_connections": len(pool),
                "active_connections": sum(1 for h in pool if h.is_connected)
            }
        
        return stats


# Instancia global del pool de conexiones
_connection_pool: Optional[ConnectionPool] = None


def get_connection_pool(max_connections: int = 5) -> ConnectionPool:
    """
    Obtiene la instancia global del pool de conexiones (singleton).
    
    Args:
        max_connections: Número máximo de conexiones por pool
    
    Returns:
        ConnectionPool: Instancia del pool
    """
    global _connection_pool
    if _connection_pool is None:
        _connection_pool = ConnectionPool(max_connections)
    return _connection_pool
