"""
Script de prueba para verificar el funcionamiento del servidor.
"""

import sys
import os

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import get_config
from src.database.mysql_handler import MySQLHandler

def test_config():
    """Prueba la carga de configuración"""
    print("=" * 70)
    print("🔧 PRUEBA 1: Cargando configuración")
    print("=" * 70)
    
    config = get_config()
    connections = config.list_connections()
    
    print(f"✅ Configuración cargada")
    print(f"📊 Total conexiones: {len(connections)}")
    print(f"🔧 Conexión por defecto: {config.default_connection}")
    print()
    
    for name, info in connections.items():
        print(f"  • {name}:")
        print(f"    - Tipo: {info['type']}")
        print(f"    - Host: {info['host']}:{info['port']}")
        print(f"    - Usuario: {info['user']}")
        print(f"    - Base de datos: {info['database']}")
        print(f"    - Activa: {info['active']}")
        print(f"    - Por defecto: {info['is_default']}")
    print()


def test_mysql_connection():
    """Prueba la conexión a MySQL"""
    print("=" * 70)
    print("🔌 PRUEBA 2: Conexión a MySQL")
    print("=" * 70)
    
    config = get_config()
    mysql_config = config.get_connection('mysql_local')
    
    if not mysql_config:
        print("❌ No se encontró la conexión mysql_local")
        return False
    
    if mysql_config.type != 'mysql':
        print("❌ La conexión no es de tipo MySQL")
        return False
    
    print(f"📝 Intentando conectar a {mysql_config.host}:{mysql_config.port}")
    
    try:
        handler = MySQLHandler(
            host=mysql_config.host,
            port=mysql_config.port,
            user=mysql_config.user,
            password=mysql_config.password,
            database=mysql_config.database
        )
        
        result = handler.test_connection()
        
        if result['status'] == 'connected':
            print("✅ Conexión exitosa!")
            print(f"   Host: {result['host']}")
            print(f"   Puerto: {result['port']}")
            print(f"   Usuario: {result['user']}")
            print(f"   Base de datos: {result.get('database', 'N/A')}")
            
            # Probar consulta
            version = handler.get_server_version()
            print(f"   Versión MySQL: {version}")
            
            # Listar bases de datos
            databases = handler.list_databases()
            print(f"   Total bases de datos: {len(databases)}")
            
            handler.disconnect()
            return True
        else:
            print(f"❌ Error en conexión: {result.get('error', 'Unknown')}")
            return False
            
    except Exception as e:
        print(f"❌ Excepción: {e}")
        return False
    finally:
        print()


def main():
    """Ejecuta todas las pruebas"""
    print()
    print("╔" + "=" * 68 + "╗")
    print("║" + " DATABASE-CONNECT - PRUEBAS INICIALES ".center(68) + "║")
    print("╚" + "=" * 68 + "╝")
    print()
    
    try:
        # Prueba 1: Configuración
        test_config()
        
        # Prueba 2: Conexión MySQL
        mysql_ok = test_mysql_connection()
        
        # Resumen
        print("=" * 70)
        print("📊 RESUMEN DE PRUEBAS")
        print("=" * 70)
        print(f"✅ Configuración: OK")
        print(f"{'✅' if mysql_ok else '❌'} Conexión MySQL: {'OK' if mysql_ok else 'FALLÓ'}")
        print()
        
        if mysql_ok:
            print("🎉 ¡Todas las pruebas pasaron exitosamente!")
            print()
            print("📝 Próximos pasos:")
            print("   1. Configurar tus credenciales MySQL en config/settings.json")
            print("   2. Iniciar el servidor: python -m src.server")
            print("   3. Probar las herramientas MCP desde Copilot")
        else:
            print("⚠️  Algunas pruebas fallaron")
            print()
            print("🔧 Asegúrate de:")
            print("   1. Tener MySQL instalado y en ejecución")
            print("   2. Configurar las credenciales correctas en config/settings.json")
            print("   3. El usuario tenga permisos de acceso")
        
        print()
        
    except Exception as e:
        print(f"❌ Error general: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
