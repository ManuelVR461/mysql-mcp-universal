"""
Script para probar las herramientas MCP directamente
"""
from src.server import (
    test_server,
    get_server_info,
    list_databases,
    list_tables
)

print("\n" + "="*60)
print("  PROBANDO HERRAMIENTAS MCP DATABASE-CONNECT")
print("="*60)

# 1. Test del servidor
print("\n[1] Test del servidor:")
result = test_server()
print(f"  Status: {result['status']}")
print(f"  Mensaje: {result['message']}")
print(f"  Versión: {result['version']}")

# 2. Información del servidor
print("\n[2] Información del servidor:")
info = get_server_info()
print(f"  Nombre: {info['server_name']}")
print(f"  Conexiones: {info['total_connections']}")
print(f"  Conexión por defecto: {info['default_connection']}")
print(f"  Estado: {info['status']}")

# 3. Listar bases de datos
print("\n[3] Bases de datos disponibles:")
dbs = list_databases()
print(f"  Total: {len(dbs['databases'])}")
for i, db in enumerate(dbs['databases'], 1):
    print(f"    {i:2d}. {db}")

# 4. Listar tablas de una base de datos
print("\n[4] Tablas en 'test_mcp_health':")
tables = list_tables(database_name='test_mcp_health')
if tables['status'] == 'success':
    print(f"  Total tablas: {len(tables['tables'])}")
    for table in tables['tables']:
        print(f"    - {table}")
else:
    print(f"  {tables['message']}")

print("\n" + "="*60)
print("  ✅ PRUEBAS COMPLETADAS")
print("="*60)
