# 🧪 Guía de Prueba del Servidor MCP database-connect

## ✅ Estado Actual
- **Configuración:** ✅ Completada
- **Servidor:** ✅ Funcionando
- **Python:** ✅ C:\laragon\www\database-connect\venv\Scripts\python.exe
- **Herramientas:** ✅ 15 disponibles

---

## 📝 PASO 1: Recargar VS Code

**IMPORTANTE:** VS Code necesita recargar para detectar la nueva configuración.

### Opción A: Comando de Recarga
1. Presiona `Ctrl + Shift + P`
2. Escribe: `reload window`
3. Selecciona: **"Developer: Reload Window"**
4. Presiona Enter

### Opción B: Reiniciar VS Code
1. Cierra VS Code completamente
2. Vuelve a abrirlo

---

## 📝 PASO 2: Abrir GitHub Copilot Chat

### Si tienes el panel lateral:
- Presiona `Ctrl + Alt + I`
- O haz clic en el ícono de Copilot en la barra lateral

### Si no aparece:
1. Presiona `Ctrl + Shift + P`
2. Escribe: `copilot chat`
3. Selecciona: **"GitHub Copilot: Open Chat"**

---

## 📝 PASO 3: Verificar que el Servidor Está Disponible

En el chat de Copilot, escribe:

```
@database-connect
```

**Resultado esperado:**
Debería aparecer `@database-connect` como una sugerencia/autocompletado.

Si NO aparece:
- Espera 10-15 segundos (el servidor tarda en iniciar)
- Recarga nuevamente VS Code
- Verifica que Copilot esté activo (ícono en la barra inferior)

---

## 📝 PASO 4: Prueba Básica del Servidor

### Test 1: Verificar que el servidor funciona
Escribe en el chat:
```
@database-connect test_server
```

**✅ Resultado esperado:**
```json
{
  "status": "ok",
  "message": "Database-Connect MCP Server is running",
  "version": "0.1.0",
  "features": ["MySQL Support", "PostgreSQL Support", "CRUD Operations", ...]
}
```

---

## 📝 PASO 5: Pruebas de Herramientas

### Test 2: Información del servidor
```
@database-connect get_server_info
```

**✅ Verás:**
- Nombre del servidor
- Versión
- Total de conexiones configuradas
- Herramientas disponibles

---

### Test 3: Listar conexiones
```
@database-connect list_connections
```

**✅ Verás:**
```json
{
  "total": 2,
  "default": "mysql_local",
  "connections": {
    "mysql_local": {
      "type": "mysql",
      "host": "localhost",
      "port": 3306,
      ...
    }
  }
}
```

---

### Test 4: Probar conexión MySQL
```
@database-connect test_connection connection_name="mysql_local"
```

**✅ Resultado exitoso:**
```json
{
  "status": "connected",
  "host": "localhost",
  "port": 3306,
  "user": "root",
  "test_query": true
}
```

**❌ Si falla:**
- Verifica que MySQL esté corriendo (Laragon)
- Revisa las credenciales en `config/settings.json`

---

### Test 5: Listar bases de datos
```
@database-connect list_databases
```

**✅ Verás:**
Lista de todas tus bases de datos MySQL disponibles.

---

### Test 6: Listar tablas de una base de datos
```
@database-connect list_tables database="mysql"
```

**✅ Verás:**
Lista de tablas de la base de datos especificada.

---

## 📝 PASO 6: Pruebas con Lenguaje Natural

**¡ESTO ES LO GENIAL!** No necesitas usar comandos explícitos.

### Test 7: Pregunta en lenguaje natural
```
Muéstrame todas las bases de datos disponibles en mi servidor MySQL local
```

**Copilot debería:**
1. Detectar que necesita usar `@database-connect`
2. Llamar automáticamente a `list_databases`
3. Mostrarte el resultado formateado

---

### Test 8: Consultas más complejas
```
¿Cuántas tablas tiene la base de datos information_schema?
```

**Copilot hará:**
1. `list_tables` para obtener las tablas
2. Contar los resultados
3. Responder con el número

---

### Test 9: Operación de inserción (si tienes una tabla de prueba)
```
Inserta un registro en la tabla test_users con nombre "Juan Pérez" y email "juan@example.com"
```

**Copilot usará:**
`insert_record` automáticamente

---

## 🔍 Solución de Problemas

### Problema 1: "@database-connect" no aparece

**Soluciones:**
1. Espera 15-20 segundos después de recargar VS Code
2. Verifica que GitHub Copilot esté activo (ícono en barra inferior)
3. Revisa la salida del servidor:
   ```powershell
   Get-Process python | Where-Object {$_.CommandLine -like "*src.server*"}
   ```
4. Cierra y reabre VS Code completamente

---

### Problema 2: Error "Connection refused"

**Soluciones:**
1. Verifica que MySQL esté corriendo:
   ```cmd
   mysql -u root -e "SELECT 1"
   ```
2. Revisa `config/settings.json`:
   - Host correcto
   - Puerto correcto (3306 para MySQL)
   - Credenciales válidas

---

### Problema 3: El servidor no responde

**Verificación manual:**
1. Abre terminal en el proyecto
2. Ejecuta:
   ```cmd
   .\run_server.bat
   ```
3. Debería mostrar logs de inicio
4. Si hay errores, léelos y repórtalos

---

### Problema 4: Error de Python/dependencias

**Solución:**
```cmd
.\activate.bat
pip install -r requirements.txt
```

---

## 🎉 Pruebas Avanzadas

### Una vez que todo funcione, prueba:

1. **CRUD completo:**
   ```
   Crea una tabla llamada test_copilot con columnas id, nombre y email
   Inserta 3 registros de prueba
   Muéstrame todos los registros
   Actualiza el email del registro con id=1
   Elimina el registro con id=3
   ```

2. **Consultas complejas:**
   ```
   Muéstrame los primeros 10 usuarios ordenados por fecha de creación
   ¿Cuántos productos hay con precio mayor a 100?
   Lista las tablas que contienen la palabra "user" en su nombre
   ```

3. **Análisis de datos:**
   ```
   Analiza la estructura de la tabla users
   ¿Qué columnas tiene la tabla products?
   Dame estadísticas sobre la tabla orders
   ```

---

## ✅ Checklist de Verificación

- [ ] VS Code recargado
- [ ] Copilot Chat abierto
- [ ] `@database-connect` aparece en autocompletado
- [ ] `test_server` responde OK
- [ ] `list_connections` muestra conexiones
- [ ] `test_connection` conecta a MySQL
- [ ] `list_databases` muestra bases de datos
- [ ] Lenguaje natural funciona
- [ ] Operaciones CRUD funcionan

---

## 📞 Siguiente Paso

Una vez que todas las pruebas pasen, puedes:

1. **Usar el servidor normalmente** en tu desarrollo diario
2. **Agregar más conexiones** en `config/settings.json`
3. **Explorar las 15 herramientas** disponibles
4. **Integrar con tu flujo de trabajo**

---

## 💡 Comandos Útiles de Referencia

### Gestión (6 herramientas):
- `test_server` - Verificar servidor
- `get_server_info` - Info completa
- `list_connections` - Ver conexiones
- `test_connection` - Probar conexión
- `list_databases` - Listar BDs
- `list_tables` - Listar tablas

### CRUD (9 herramientas):
- `insert_record` - Insertar uno
- `bulk_insert` - Insertar varios
- `select_records` - Consultar
- `get_record_by_id` - Buscar por ID
- `count_records` - Contar
- `update_record` - Actualizar uno
- `update_records` - Actualizar varios
- `delete_record` - Eliminar uno
- `delete_records` - Eliminar varios (requiere confirm=True)

---

**¡Éxito con las pruebas! 🚀**

Si encuentras algún problema, revisa los logs del servidor o consulta `VSCODE_SETUP.md` para más detalles.
