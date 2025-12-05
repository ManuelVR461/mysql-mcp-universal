"""Script para listar bases de datos disponibles"""
from src.config import get_config
from src.database.mysql_handler import MySQLHandler

config = get_config()
conn = config.get_connection('mysql_local')

handler = MySQLHandler(
    host=conn.host,
    port=conn.port,
    user=conn.user,
    password=conn.password,
    database=conn.database
)

try:
    handler.connect()
    databases = handler.list_databases()
    
    print("\n" + "="*50)
    print("   BASES DE DATOS DISPONIBLES")
    print("="*50)
    
    for i, db in enumerate(databases, 1):
        print(f"{i:2d}. {db}")
    
    print("\n" + "="*50)
    print(f"Total: {len(databases)} bases de datos")
    print("="*50)
    
finally:
    handler.disconnect()
