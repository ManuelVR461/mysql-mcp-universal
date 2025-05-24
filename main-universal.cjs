// Servidor MCP Universal MySQL - Versión simplificada para testing
const dotenv = require("dotenv");
const { Server } = require("@modelcontextprotocol/sdk/server/index.js");
const { StdioServerTransport } = require("@modelcontextprotocol/sdk/server/stdio.js");
const { 
  CallToolRequestSchema,
  ListToolsRequestSchema,
} = require("@modelcontextprotocol/sdk/types.js");
const mysql = require("mysql2/promise");

// Cargar variables de entorno
dotenv.config();

// Servidor MCP Universal MySQL
const server = new Server({
  name: "MySQL-Universal-Connect",
  version: "2.0.0"
}, {
  capabilities: {
    tools: {}
  }
});

console.log("Servidor MCP MySQL Universal iniciado - JavaScript");

// Configuración por defecto
const defaultConfig = {
  host: process.env.MYSQL_HOST || '127.0.0.1',
  user: process.env.MYSQL_USER || 'root',
  password: process.env.MYSQL_PASSWORD || '',
  port: parseInt(process.env.MYSQL_PORT || '3306'),
  connectTimeout: 10000,
  acquireTimeout: 10000,
  timeout: 10000
};

// Caché de conexiones
const connectionCache = new Map();

// Función para crear clave única para el caché de conexiones
function createConnectionKey(host, port, user, database) {
  return `${host}:${port}:${user}:${database || 'no-db'}`;
}

// Función para conectar a MySQL con parámetros dinámicos
async function connectToDatabase(params = {}) {
  const config = {
    host: params.host || defaultConfig.host,
    port: params.port || defaultConfig.port,
    user: params.user || defaultConfig.user,
    password: params.password || defaultConfig.password,
    database: params.database,
    connectTimeout: defaultConfig.connectTimeout,
    acquireTimeout: defaultConfig.acquireTimeout,
    timeout: defaultConfig.timeout
  };

  const connectionKey = createConnectionKey(config.host, config.port, config.user, config.database);
  
  // Intentar reutilizar conexión existente
  if (connectionCache.has(connectionKey)) {
    const existingConnection = connectionCache.get(connectionKey);
    try {
      // Verificar si la conexión sigue activa
      await existingConnection.ping();
      return existingConnection;
    } catch (error) {
      // Si la conexión falló, eliminarla del caché
      connectionCache.delete(connectionKey);
    }
  }

  // Crear nueva conexión
  const connection = await mysql.createConnection(config);
  connectionCache.set(connectionKey, connection);
  
  return connection;
}

// Definir las herramientas disponibles
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "show_databases",
      description: "Muestra todas las bases de datos disponibles en el servidor MySQL",
      inputSchema: {
        type: "object",
        properties: {
          host: { type: "string", description: "Dirección del servidor MySQL (por defecto: 127.0.0.1)" },
          port: { type: "number", description: "Puerto del servidor MySQL (por defecto: 3306)" },
          user: { type: "string", description: "Usuario de MySQL (por defecto: root)" },
          password: { type: "string", description: "Contraseña de MySQL" }
        }
      }
    },
    {
      name: "show_tables",
      description: "Muestra todas las tablas de una base de datos específica",
      inputSchema: {
        type: "object",
        properties: {
          database: { type: "string", description: "Nombre de la base de datos" },
          host: { type: "string", description: "Dirección del servidor MySQL (por defecto: 127.0.0.1)" },
          port: { type: "number", description: "Puerto del servidor MySQL (por defecto: 3306)" },
          user: { type: "string", description: "Usuario de MySQL (por defecto: root)" },
          password: { type: "string", description: "Contraseña de MySQL" }
        },
        required: ["database"]
      }
    },
    {
      name: "describe_table",
      description: "Muestra la estructura de una tabla específica",
      inputSchema: {
        type: "object",
        properties: {
          table_name: { type: "string", description: "Nombre de la tabla a describir" },
          database: { type: "string", description: "Nombre de la base de datos" },
          host: { type: "string", description: "Dirección del servidor MySQL (por defecto: 127.0.0.1)" },
          port: { type: "number", description: "Puerto del servidor MySQL (por defecto: 3306)" },
          user: { type: "string", description: "Usuario de MySQL (por defecto: root)" },
          password: { type: "string", description: "Contraseña de MySQL" }
        },
        required: ["table_name", "database"]
      }
    },
    {
      name: "execute_query",
      description: "Ejecuta una consulta SQL en una base de datos específica",
      inputSchema: {
        type: "object",
        properties: {
          query: { type: "string", description: "La consulta SQL a ejecutar" },
          database: { type: "string", description: "Nombre de la base de datos" },
          host: { type: "string", description: "Dirección del servidor MySQL (por defecto: 127.0.0.1)" },
          port: { type: "number", description: "Puerto del servidor MySQL (por defecto: 3306)" },
          user: { type: "string", description: "Usuario de MySQL (por defecto: root)" },
          password: { type: "string", description: "Contraseña de MySQL" }
        },
        required: ["query", "database"]
      }
    }
  ]
}));

// Manejar las llamadas a las herramientas
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    switch (name) {
      case "show_databases": {
        const db = await connectToDatabase({
          host: args?.host,
          port: args?.port,
          user: args?.user,
          password: args?.password
        });
        const [databases] = await db.execute("SHOW DATABASES");
        
        return {
          content: [
            {
              type: "text",
              text: `Bases de datos disponibles en ${args?.host || defaultConfig.host}:${args?.port || defaultConfig.port}:\n${JSON.stringify(databases, null, 2)}`
            }
          ]
        };
      }

      case "show_tables": {
        const db = await connectToDatabase({
          host: args?.host,
          port: args?.port,
          user: args?.user,
          password: args?.password,
          database: args?.database
        });
        const [tables] = await db.execute("SHOW TABLES");
        
        return {
          content: [
            {
              type: "text",
              text: `Tablas en la base de datos '${args?.database}':\n${JSON.stringify(tables, null, 2)}`
            }
          ]
        };
      }

      case "describe_table": {
        const db = await connectToDatabase({
          host: args?.host,
          port: args?.port,
          user: args?.user,
          password: args?.password,
          database: args?.database
        });
        const [columns] = await db.execute(`DESCRIBE \`${args?.table_name}\``);
        
        return {
          content: [
            {
              type: "text",
              text: `Estructura de la tabla '${args?.table_name}' en la base de datos '${args?.database}':\n${JSON.stringify(columns, null, 2)}`
            }
          ]
        };
      }

      case "execute_query": {
        const db = await connectToDatabase({
          host: args?.host,
          port: args?.port,
          user: args?.user,
          password: args?.password,
          database: args?.database
        });
        const queryResult = await db.execute(args?.query);
        
        return {
          content: [
            {
              type: "text",
              text: `Consulta ejecutada en '${args?.database}':\nQuery: ${args?.query}\n\nResultado:\n${JSON.stringify(queryResult[0], null, 2)}`
            }
          ]
        };
      }

      default:
        throw new Error(`Herramienta desconocida: ${name}`);
    }
  } catch (error) {
    return {
      content: [
        {
          type: "text",
          text: `Error: ${error.message}\nStack: ${error.stack}`
        }
      ],
      isError: true
    };
  }
});

// Manejar cierre graceful del servidor
process.on('SIGINT', async () => {
  console.log('Cerrando conexiones de base de datos...');
  for (const [key, connection] of connectionCache) {
    try {
      await connection.end();
    } catch (error) {
      console.error(`Error cerrando conexión ${key}:`, error);
    }
  }
  connectionCache.clear();
  process.exit(0);
});

// Iniciar el servidor
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.log("Servidor MCP MySQL Universal iniciado - Puede conectarse a cualquier base de datos MySQL");
}

main().catch(console.error);
