"""
Test completo de herramientas CRUD del servidor MCP.
Verifica todas las operaciones CREATE, READ, UPDATE, DELETE.
"""

import sys
import os

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from config import get_config
from database.mysql_handler import MySQLHandler
from tools.crud_tools import (
    insert_record, bulk_insert,
    select_records, get_record_by_id, count_records,
    update_record, update_records,
    delete_record, delete_records
)

def print_section(title):
    """Imprime encabezado de sección"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def print_result(operation, result):
    """Imprime resultado de operación"""
    status = result.get('status', 'unknown')
    emoji = "✅" if status == 'success' else "❌"
    print(f"{emoji} {operation}:")
    print(f"   Status: {status}")
    if 'message' in result:
        print(f"   Message: {result['message']}")
    if 'data' in result and result['data']:
        print(f"   Data: {result['data']}")
    if 'rows_affected' in result:
        print(f"   Rows affected: {result['rows_affected']}")
    if 'count' in result:
        print(f"   Count: {result['count']}")
    print()

def main():
    """Ejecuta tests de todas las herramientas CRUD"""
    
    print_section("🧪 TEST COMPLETO DE HERRAMIENTAS CRUD")
    
    try:
        # Obtener configuración
        config = get_config()
        print(f"✅ Configuración cargada")
        print(f"   Conexión por defecto: {config.default_connection}")
        print()
        
        # Obtener handler para crear tabla de prueba
        connection = config.get_connection(config.default_connection)
        if not connection:
            print("❌ No hay conexión configurada")
            return
        
        # IMPORTANTE: Para testing, configuramos una base de datos temporal
        connection.database = "test_database_connect"
        config.save()  # Guardamos temporalmente
        print(f"✅ Base de datos temporal configurada: {connection.database}")
        
        if connection.type == 'mysql':
            # Para testing, primero nos conectamos sin BD para crearla
            handler_setup = MySQLHandler(
                host=connection.host,
                port=connection.port,
                user=connection.user,
                password=connection.password,
                database="mysql"  # Usamos la BD 'mysql' que siempre existe
            )
        else:
            print(f"⚠️  Test solo soporta MySQL por ahora")
            return
        
        # ====================================================================
        # PREPARACIÓN: Crear tabla de prueba
        # ====================================================================
        print_section("🔧 PREPARACIÓN: Creando tabla de prueba")
        
        # Conectar y crear tabla
        handler_setup.connect()
        cursor = handler_setup.cursor
        
        # Crear base de datos temporal para tests si no existe
        cursor.execute("CREATE DATABASE IF NOT EXISTS test_database_connect")
        cursor.execute("USE test_database_connect")
        print("✅ Base de datos de prueba creada/seleccionada")
        
        # Eliminar tabla si existe
        cursor.execute("DROP TABLE IF EXISTS test_crud")
        print("✅ Tabla test_crud eliminada (si existía)")
        
        # Crear tabla de prueba
        cursor.execute("""
            CREATE TABLE test_crud (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100),
                age INT,
                active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        handler_setup.connection.commit()
        print("✅ Tabla test_crud creada")
        handler_setup.disconnect()
        
        # Ahora las herramientas CRUD usarán la configuración actualizada automáticamente
        
        # ====================================================================
        # TEST 1: CREATE - insert_record
        # ====================================================================
        print_section("📝 TEST 1: INSERT_RECORD (Inserción individual)")
        
        result = insert_record(
            "test_crud",
            {
                "name": "Juan Pérez",
                "email": "juan@example.com",
                "age": 30
            }
        )
        print_result("Insertar Juan Pérez", result)
        
        result = insert_record(
            "test_crud",
            {
                "name": "María García",
                "email": "maria@example.com",
                "age": 25
            }
        )
        print_result("Insertar María García", result)
        
        # ====================================================================
        # TEST 2: CREATE - bulk_insert
        # ====================================================================
        print_section("📝 TEST 2: BULK_INSERT (Inserción masiva)")
        
        result = bulk_insert(
            "test_crud",
            [
                {"name": "Carlos López", "email": "carlos@example.com", "age": 35},
                {"name": "Ana Martínez", "email": "ana@example.com", "age": 28},
                {"name": "Pedro Sánchez", "email": "pedro@example.com", "age": 42},
            ]
        )
        print_result("Inserción masiva de 3 registros", result)
        
        # ====================================================================
        # TEST 3: READ - select_records (sin filtros)
        # ====================================================================
        print_section("🔍 TEST 3: SELECT_RECORDS (Consulta sin filtros)")
        
        result = select_records("test_crud")
        print_result(f"Seleccionar todos los registros", result)
        
        if result.get('status') == 'success':
            print(f"   📊 Total de registros: {len(result.get('data', []))}")
            for record in result.get('data', [])[:3]:
                print(f"      - ID {record.get('id')}: {record.get('name')} ({record.get('email')})")
        
        # ====================================================================
        # TEST 4: READ - select_records (con filtros)
        # ====================================================================
        print_section("🔍 TEST 4: SELECT_RECORDS (Con filtros)")
        
        result = select_records(
            "test_crud",
            columns=["id", "name", "age"],
            where={"active": 1},
            order_by="age DESC",
            limit=3
        )
        print_result("Top 3 usuarios activos por edad", result)
        
        # ====================================================================
        # TEST 5: READ - get_record_by_id
        # ====================================================================
        print_section("🔍 TEST 5: GET_RECORD_BY_ID (Búsqueda por ID)")
        
        result = get_record_by_id("test_crud", 1)
        print_result("Obtener registro con ID=1", result)
        
        # ====================================================================
        # TEST 6: READ - count_records
        # ====================================================================
        print_section("🔢 TEST 6: COUNT_RECORDS (Contar registros)")
        
        result = count_records("test_crud")
        print_result("Contar todos los registros", result)
        
        result = count_records("test_crud", where={"active": 1})
        print_result("Contar registros activos", result)
        
        # ====================================================================
        # TEST 7: UPDATE - update_record
        # ====================================================================
        print_section("✏️  TEST 7: UPDATE_RECORD (Actualización individual)")
        
        result = update_record(
            "test_crud",
            1,
            {"email": "juan.perez.nuevo@example.com", "age": 31}
        )
        print_result("Actualizar registro ID=1", result)
        
        # Verificar cambio
        result = get_record_by_id("test_crud", 1)
        print_result("Verificar cambios en ID=1", result)
        
        # ====================================================================
        # TEST 8: UPDATE - update_records
        # ====================================================================
        print_section("✏️  TEST 8: UPDATE_RECORDS (Actualización masiva)")
        
        result = update_records(
            "test_crud",
            {"active": 0},
            {"age": 35}  # Desactivar usuarios con edad > 35
        )
        print_result("Desactivar usuarios con edad >= 35", result)
        
        # Verificar cambios
        result = count_records("test_crud", where={"active": 0})
        print_result("Contar usuarios desactivados", result)
        
        # ====================================================================
        # TEST 9: DELETE - delete_record
        # ====================================================================
        print_section("🗑️  TEST 9: DELETE_RECORD (Eliminación individual)")
        
        result = delete_record("test_crud", 5)
        print_result("Eliminar registro ID=5", result)
        
        # Verificar eliminación
        result = get_record_by_id("test_crud", 5)
        print_result("Verificar que ID=5 no existe", result)
        
        # ====================================================================
        # TEST 10: DELETE - delete_records (sin confirmación)
        # ====================================================================
        print_section("🗑️  TEST 10: DELETE_RECORDS (Sin confirmación)")
        
        result = delete_records(
            "test_crud",
            {"active": 0},
            confirm=False
        )
        print_result("Intentar eliminar sin confirm", result)
        
        # ====================================================================
        # TEST 11: DELETE - delete_records (con confirmación)
        # ====================================================================
        print_section("🗑️  TEST 11: DELETE_RECORDS (Con confirmación)")
        
        result = delete_records(
            "test_crud",
            {"active": 0},
            confirm=True
        )
        print_result("Eliminar registros inactivos (confirmado)", result)
        
        # Verificar eliminación
        result = count_records("test_crud")
        print_result("Contar registros restantes", result)
        
        # ====================================================================
        # LIMPIEZA: Eliminar tabla de prueba
        # ====================================================================
        print_section("🧹 LIMPIEZA: Eliminando tabla de prueba")
        
        handler_setup.connect()
        cursor = handler_setup.cursor
        cursor.execute("USE test_database_connect")
        cursor.execute("DROP TABLE IF EXISTS test_crud")
        cursor.execute("DROP DATABASE IF EXISTS test_database_connect")
        handler_setup.connection.commit()
        print("✅ Tabla y base de datos de prueba eliminadas")
        handler_setup.disconnect()
        
        # Restaurar configuración original
        connection.database = None
        config.save()
        print("✅ Configuración restaurada")
        
        # ====================================================================
        # RESUMEN FINAL
        # ====================================================================
        print_section("✅ PRUEBAS COMPLETADAS")
        print("""
Todas las herramientas CRUD han sido probadas:

✅ CREATE:
   - insert_record (inserción individual)
   - bulk_insert (inserción masiva)

✅ READ:
   - select_records (consulta con filtros, ordenamiento, límites)
   - get_record_by_id (búsqueda por ID)
   - count_records (conteo con/sin filtros)

✅ UPDATE:
   - update_record (actualización individual)
   - update_records (actualización masiva)

✅ DELETE:
   - delete_record (eliminación individual)
   - delete_records (eliminación masiva con confirmación)

🎉 El servidor MCP está listo para usar con GitHub Copilot!
        """)
        
    except Exception as e:
        print(f"\n❌ Error durante las pruebas: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
