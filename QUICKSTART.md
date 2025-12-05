# Guía de Inicio Rápido - Database-Connect

## ✅ Checklist de Instalación

### 1️⃣ Verificar Requisitos
- [ ] Python 3.10+ instalado (`python --version`)
- [ ] VS Code instalado
- [ ] GitHub Copilot activo
- [ ] MySQL o PostgreSQL funcionando

### 2️⃣ Instalación del Proyecto

```bash
# Navegar al directorio
cd c:\laragon\www\database-connect

# Crear entorno virtual (si no existe)
python -m venv venv

# Activar entorno virtual
# Windows CMD:
venv\Scripts\activate.bat
# Windows PowerShell:
.\venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 3️⃣ Configuración de Base de Datos

Editar `config/settings.json`:

```json
{
  "connections": {
    "mysql_local": {
      "type": "mysql",
      "host": "localhost",
      "port": 3306,
      "user": "root",
      "password": "",
      "database": null,
      "active": true,
      "description": "MySQL local"
    }
  },
  "default_connection": "mysql_local",
  "settings": {
    "pool_size": 5,
    "pool_timeout": 30,
    "query_timeout": 60,
    "enable_logging": true,
    "log_queries": false,
    "confirm_destructive_operations": true
  }
}
```

**Notas:**
- `database: null` conecta al servidor sin seleccionar una BD específica
- `password: ""` para contraseña vacía
- Puedes añadir múltiples conexiones

### 4️⃣ Probar la Instalación

```bash
# Opción 1: Usando script
.\test.bat

# Opción 2: Manual
python test_connection.py
```

**Resultado esperado:**
```
✅ Configuración: OK
✅ Conexión MySQL: OK
🎉 ¡Todas las pruebas pasaron exitosamente!
```

### 5️⃣ Configurar VS Code (Ya está hecho ✅)

El archivo `.vscode/settings.json` ya está configurado correctamente:
- Usa el Python del venv
- Registra el servidor MCP
- Configura las variables de entorno

**Solo necesitas:** Recargar VS Code (Ctrl+Shift+P → "Reload Window")

### 6️⃣ Iniciar el Servidor MCP

```bash
# Opción 1: Script automático
.\run_server.bat

# Opción 2: Manual
venv\Scripts\activate
python -m src.server
```

**El servidor debe mostrar:**
```
======================================================================
🗄️  DATABASE-CONNECT MCP SERVER v0.1.0
======================================================================
✅ Archivo de configuración encontrado
🚀 Servidor MCP listo y esperando conexiones...
```

### 7️⃣ Usar desde Copilot

Abre Copilot Chat en VS Code y prueba:

```
"Lista mis conexiones de base de datos"
"Prueba la conexión mysql_local"
"Muéstrame las bases de datos disponibles"
"Lista las tablas de la base de datos mysql"
```

---

## 🎯 Scripts de Utilidad

### Windows

| Script | Descripción | Comando |
|--------|-------------|---------|
| `activate.bat` | Activa el entorno virtual | `.\activate.bat` |
| `test.bat` | Ejecuta pruebas de conexión | `.\test.bat` |
| `run_server.bat` | Inicia el servidor MCP | `.\run_server.bat` |

### Manual

```bash
# Activar venv
.\venv\Scripts\activate

# Probar conexión
python test_connection.py

# Iniciar servidor
python -m src.server

# Ejecutar tests unitarios (cuando estén disponibles)
pytest tests/

# Formatear código
black src/ tests/

# Linting
flake8 src/ tests/

# Type checking
mypy src/
```

---

## 🔧 Solución de Problemas

### "No se puede conectar a MySQL"
- ✅ Verifica que MySQL está corriendo: `mysql -u root -p`
- ✅ Revisa host, puerto y credenciales en `config/settings.json`
- ✅ Verifica que el firewall no bloquea el puerto 3306

### "ModuleNotFoundError"
- ✅ Asegúrate de haber activado el venv: `.\venv\Scripts\activate`
- ✅ Reinstala dependencias: `pip install -r requirements.txt`

### "El servidor MCP no aparece en Copilot"
- ✅ Recarga VS Code: Ctrl+Shift+P → "Reload Window"
- ✅ Verifica `.vscode/settings.json` tiene la configuración correcta
- ✅ Revisa que la ruta al venv es correcta

### "Access denied for user"
- ✅ Verifica el usuario y password en `config/settings.json`
- ✅ Asegúrate que el usuario tiene permisos en MySQL

---

## 📁 Estructura del Proyecto

```
database-connect/
├── venv/                    # Entorno virtual (no se sube a git)
├── src/                     # Código fuente
│   ├── server.py           # Servidor MCP principal
│   ├── config.py           # Gestión de configuración
│   └── database/           # Manejadores de BD
├── config/
│   └── settings.json       # Configuración de conexiones
├── tests/                   # Tests (pendiente)
├── activate.bat            # Script de activación
├── test.bat                # Script de pruebas
├── run_server.bat          # Script para iniciar servidor
├── requirements.txt        # Dependencias Python
└── README.md               # Documentación principal
```

---

## 🎓 Siguientes Pasos

Una vez todo funcione:

1. **Explora las herramientas disponibles:**
   - Pregúntale a Copilot: "¿Qué puedes hacer con database-connect?"

2. **Revisa la documentación:**
   - `ROADMAP.md` - Plan completo de desarrollo
   - `STATUS.md` - Estado actual del proyecto

3. **Contribuye:**
   - Lee `CONTRIBUTING.md` (cuando esté disponible)
   - Reporta bugs o sugiere mejoras

---

## 💡 Consejos

- **Usa `database: null`** en la configuración para conectar al servidor sin BD específica
- **Activa logging** poniendo `log_queries: true` en settings para debug
- **Mantén actualizado** el venv: `pip install --upgrade -r requirements.txt`
- **Crea un backup** de `config/settings.json` con tus conexiones

---

¿Problemas? Abre un issue en GitHub o consulta la documentación completa en el README.md
