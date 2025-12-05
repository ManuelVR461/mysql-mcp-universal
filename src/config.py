"""
Gestión de configuración del servidor.
Lee y valida configuración de conexiones a bases de datos.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional
import os
import logging
from pydantic import BaseModel, Field, field_validator

logger = logging.getLogger(__name__)


class DatabaseConnection(BaseModel):
    """Modelo de configuración de conexión a base de datos"""
    type: str = Field(..., description="Tipo de base de datos: mysql o postgres")
    host: str = Field(default="localhost", description="Host del servidor")
    port: int = Field(..., description="Puerto de conexión")
    user: str = Field(..., description="Usuario de la base de datos")
    password: str = Field(default="", description="Contraseña")
    database: Optional[str] = Field(None, description="Nombre de la base de datos")
    active: bool = Field(default=True, description="Si la conexión está activa")
    description: Optional[str] = Field(None, description="Descripción de la conexión")
    
    @field_validator('type')
    @classmethod
    def validate_type(cls, v):
        if v.lower() not in ['mysql', 'postgres', 'postgresql']:
            raise ValueError(f"Tipo de base de datos no soportado: {v}")
        return v.lower()
    
    @field_validator('port')
    @classmethod
    def validate_port(cls, v):
        if v < 1 or v > 65535:
            raise ValueError(f"Puerto inválido: {v}")
        return v


class ServerSettings(BaseModel):
    """Configuración general del servidor"""
    pool_size: int = Field(default=5, ge=1, le=20)
    pool_timeout: int = Field(default=30, ge=5, le=300)
    query_timeout: int = Field(default=60, ge=5, le=600)
    enable_logging: bool = Field(default=True)
    log_queries: bool = Field(default=False)
    confirm_destructive_operations: bool = Field(default=True)


class Config:
    """
    Gestiona la configuración del servidor Database-Connect.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Inicializa el gestor de configuración.
        
        Args:
            config_path: Ruta al archivo de configuración JSON
        """
        if config_path is None:
            config_path = os.getenv('DB_CONFIG_PATH', 'config/settings.json')
        
        self.config_path = Path(config_path)
        self._connections: Dict[str, DatabaseConnection] = {}
        self._default_connection: Optional[str] = None
        self._settings: ServerSettings = ServerSettings()
        
        if self.config_path.exists():
            self.load()
        else:
            logger.warning(f"Archivo de configuración no encontrado: {self.config_path}")
    
    def load(self) -> None:
        """Carga la configuración desde el archivo JSON"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Cargar conexiones
            connections_data = data.get('connections', {})
            for name, conn_data in connections_data.items():
                try:
                    self._connections[name] = DatabaseConnection(**conn_data)
                    logger.info(f"✅ Conexión '{name}' cargada: {conn_data['type']}@{conn_data['host']}")
                except Exception as e:
                    logger.error(f"❌ Error cargando conexión '{name}': {e}")
            
            # Cargar conexión por defecto
            self._default_connection = data.get('default_connection')
            
            # Cargar configuración del servidor
            settings_data = data.get('settings', {})
            self._settings = ServerSettings(**settings_data)
            
            logger.info(f"📋 Configuración cargada exitosamente desde {self.config_path}")
            logger.info(f"📊 Total conexiones: {len(self._connections)}")
            logger.info(f"🔧 Conexión por defecto: {self._default_connection}")
            
        except json.JSONDecodeError as e:
            logger.error(f"❌ Error al parsear JSON: {e}")
            raise
        except Exception as e:
            logger.error(f"❌ Error al cargar configuración: {e}")
            raise
    
    def save(self) -> None:
        """Guarda la configuración al archivo JSON"""
        try:
            # Crear directorio si no existe
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            
            data = {
                "connections": {
                    name: conn.dict() 
                    for name, conn in self._connections.items()
                },
                "default_connection": self._default_connection,
                "settings": self._settings.dict()
            }
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"💾 Configuración guardada en {self.config_path}")
            
        except Exception as e:
            logger.error(f"❌ Error al guardar configuración: {e}")
            raise
    
    def get_connection(self, name: Optional[str] = None) -> Optional[DatabaseConnection]:
        """
        Obtiene una configuración de conexión por nombre.
        
        Args:
            name: Nombre de la conexión. Si es None, usa la conexión por defecto.
        
        Returns:
            DatabaseConnection o None si no existe
        """
        if name is None:
            name = self._default_connection
        
        if name is None:
            logger.warning("No hay conexión por defecto configurada")
            return None
        
        return self._connections.get(name)
    
    def add_connection(self, name: str, connection: DatabaseConnection) -> None:
        """
        Añade una nueva conexión.
        
        Args:
            name: Nombre de la conexión
            connection: Configuración de la conexión
        """
        self._connections[name] = connection
        logger.info(f"➕ Conexión '{name}' añadida")
    
    def remove_connection(self, name: str) -> bool:
        """
        Elimina una conexión.
        
        Args:
            name: Nombre de la conexión
        
        Returns:
            True si se eliminó, False si no existía
        """
        if name in self._connections:
            del self._connections[name]
            logger.info(f"🗑️  Conexión '{name}' eliminada")
            return True
        return False
    
    def list_connections(self) -> Dict[str, Dict[str, Any]]:
        """
        Lista todas las conexiones disponibles.
        
        Returns:
            Dict con información de todas las conexiones
        """
        return {
            name: {
                "type": conn.type,
                "host": conn.host,
                "port": conn.port,
                "user": conn.user,
                "database": conn.database,
                "active": conn.active,
                "description": conn.description,
                "is_default": name == self._default_connection
            }
            for name, conn in self._connections.items()
        }
    
    @property
    def default_connection(self) -> Optional[str]:
        """Obtiene el nombre de la conexión por defecto"""
        return self._default_connection
    
    @default_connection.setter
    def default_connection(self, name: str) -> None:
        """Establece la conexión por defecto"""
        if name not in self._connections:
            raise ValueError(f"Conexión '{name}' no existe")
        self._default_connection = name
        logger.info(f"🔧 Conexión por defecto establecida: {name}")
    
    @property
    def settings(self) -> ServerSettings:
        """Obtiene la configuración del servidor"""
        return self._settings


# Instancia global de configuración
_config_instance: Optional[Config] = None


def get_config() -> Config:
    """
    Obtiene la instancia global de configuración (singleton).
    
    Returns:
        Config: Instancia de configuración
    """
    global _config_instance
    if _config_instance is None:
        _config_instance = Config()
    return _config_instance
