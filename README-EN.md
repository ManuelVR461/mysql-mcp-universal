# 🚀 MySQL MCP Universal Server

[![npm version](https://badge.fury.io/js/mysql-mcp-universal.svg)](https://badge.fury.io/js/mysql-mcp-universal)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Node.js Version](https://img.shields.io/badge/node-%3E%3D18.0.0-brightgreen.svg)](https://nodejs.org/)

**The easiest way to connect GitHub Copilot to any MySQL database instantly!**

Transform your VS Code into a powerful database explorer with AI assistance. No complex setup, no limitations - just pure MySQL connectivity magic! ✨

## 🎯 What is this?

MySQL MCP Universal Server is a **Model Context Protocol (MCP)** server that enables **GitHub Copilot** in VS Code to:

- 🔗 Connect to **ANY MySQL database** (local or remote)
- 🗄️ Explore database structures naturally with AI
- 📊 Execute SQL queries through conversation
- 🔄 Switch between multiple databases dynamically
- 🚀 Work with Laragon, XAMPP, Docker, Cloud databases...

## ⚡ Quick Start (3 steps!)

### 1. Install
```bash
npm install -g mysql-mcp-universal
```

### 2. Configure VS Code
Add to your VS Code `settings.json` (`Ctrl+Shift+P` → "Open User Settings JSON"):

```json
{
  "mcp": {
    "servers": {
      "mysql-universal": {
        "command": "node",
        "args": ["C:\\Users\\[YourUser]\\AppData\\Roaming\\npm\\node_modules\\mysql-mcp-universal\\main-universal.cjs"],
        "env": {
          "MYSQL_HOST": "127.0.0.1",
          "MYSQL_USER": "root", 
          "MYSQL_PASSWORD": "your_password",
          "MYSQL_PORT": "3306"
        }
      }
    }
  }
}
```

### 3. Use with GitHub Copilot!
Open GitHub Copilot Chat in VS Code and try:

💬 **"Show me all databases"**  
💬 **"List tables in my_project database"**  
💬 **"Describe the users table structure"**  
💬 **"Execute: SELECT * FROM products WHERE price > 100"**

## 🌟 Core Features

| Feature | Description | Example |
|---------|-------------|---------|
| 🌐 **Universal Connection** | Connect to any MySQL server | Local, remote, cloud, Docker |
| 🔀 **Dynamic Parameters** | Different credentials per query | Multiple servers in one session |
| 🧠 **AI Integration** | Natural language database exploration | "Show me the biggest tables" |
| ⚡ **Smart Caching** | Connection pooling with health checks | Automatic reconnection |
| 🛠️ **Zero Config** | Works out of the box | Just install and go! |

## 📚 Available Tools

### `show_databases`
Lists all databases on a MySQL server
```
💬 "What databases are available on 192.168.1.100?"
```

### `show_tables` 
Shows all tables in a specific database
```
💬 "List all tables in the 'ecommerce' database"
```

### `describe_table`
Displays table structure and column details
```
💬 "Show me the structure of the 'orders' table"
```

### `execute_query`
Runs custom SQL queries safely
```
💬 "Count how many active users we have: SELECT COUNT(*) FROM users WHERE status='active'"
```

## 🔧 Advanced Usage

### Multiple Server Connections
```
💬 "Connect to production server 10.0.0.5 port 3307 user 'readonly' and show databases"
💬 "Now connect to dev server localhost and compare table structures"
```

### Complex Queries
```
💬 "In the sales database, find the top 5 customers by revenue this month"
💬 "Show me table relationships in the inventory database"
💬 "Generate a report of daily sales for the last week"
```

### Environment Variables (.env)
```env
MYSQL_HOST=127.0.0.1
MYSQL_USER=root
MYSQL_PASSWORD=secret123
MYSQL_PORT=3306
```

## 🖥️ Platform Support

| Platform | Status | Notes |
|----------|--------|--------|
| Windows | ✅ Fully Supported | Tested with Laragon, XAMPP |
| macOS | ✅ Fully Supported | Homebrew MySQL, Docker |
| Linux | ✅ Fully Supported | Native MySQL, Docker containers |

## 🎨 Use Cases

### For Developers
- **Database Schema Exploration**: Understand unfamiliar databases quickly
- **Quick Data Analysis**: Get insights without leaving your code editor  
- **SQL Learning**: Practice queries with AI assistance
- **Multi-Environment Work**: Dev, staging, production databases

### For Data Analysts
- **Ad-hoc Queries**: Natural language to SQL conversion
- **Data Discovery**: Find relevant tables and columns easily
- **Report Generation**: Quick data exports and summaries

### For DevOps
- **Database Monitoring**: Check table sizes, row counts
- **Schema Validation**: Compare structures across environments
- **Maintenance Tasks**: Routine database operations

## 🛡️ Security Features

- ✅ **Connection Encryption**: Supports SSL/TLS
- ✅ **Credential Isolation**: Each query can use different credentials
- ✅ **Safe Query Execution**: Built-in SQL injection prevention
- ✅ **No Persistent Storage**: Credentials never saved to disk
- ✅ **Connection Timeouts**: Automatic cleanup of idle connections

## 🚨 Requirements

- **Node.js** 18.0.0 or higher
- **VS Code** with GitHub Copilot extension
- **MySQL Server** 5.7+ or MariaDB 10.3+
- **Network Access** to your MySQL server

## 🤝 Contributing

We love contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Development Setup
```bash
git clone https://github.com/[username]/mysql-mcp-universal.git
cd mysql-mcp-universal
npm install
npm start
```

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- **Model Context Protocol** team for the amazing framework
- **GitHub Copilot** for AI integration possibilities  
- **MySQL Community** for the robust database engine
- **VS Code Team** for the extensible editor platform

## 📞 Support

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/[username]/mysql-mcp-universal/issues)
- 💡 **Feature Requests**: [GitHub Discussions](https://github.com/[username]/mysql-mcp-universal/discussions)
- 📖 **Documentation**: [GitHub Wiki](https://github.com/[username]/mysql-mcp-universal/wiki)

---

**Made with ❤️ for the VS Code community**

*Transform your database workflow with AI - one query at a time!* 🚀
