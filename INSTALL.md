# 📋 Installation Guide

Complete installation instructions for MySQL MCP Universal Server across different platforms and setups.

## 🚀 Method 1: NPM Global Install (Recommended)

### Prerequisites
- Node.js 18+ installed
- VS Code with GitHub Copilot extension
- MySQL server running

### Installation Steps

1. **Install globally via NPM:**
   ```bash
   npm install -g mysql-mcp-universal
   ```

2. **Find installation path:**
   ```bash
   # Windows
   npm root -g
   # Usually: C:\Users\[User]\AppData\Roaming\npm\node_modules
   
   # macOS/Linux  
   which mysql-mcp-universal
   # Usually: /usr/local/lib/node_modules/mysql-mcp-universal
   ```

3. **Configure VS Code** (add to `settings.json`):
   ```json
   {
     "mcp": {
       "servers": {
         "mysql-universal": {
           "command": "node",
           "args": ["[PATH_FROM_STEP_2]/mysql-mcp-universal/main-universal.cjs"],
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

## 🛠️ Method 2: Local Project Install

### For development or custom setups

1. **Clone repository:**
   ```bash
   git clone https://github.com/[username]/mysql-mcp-universal.git
   cd mysql-mcp-universal
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Configure VS Code:**
   ```json
   {
     "mcp": {
       "servers": {
         "mysql-universal": {
           "command": "node", 
           "args": ["C:\\path\\to\\mysql-mcp-universal\\main-universal.cjs"],
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

## 🖥️ Platform-Specific Instructions

### Windows with Laragon

1. **Default Laragon MySQL settings:**
   ```json
   "env": {
     "MYSQL_HOST": "127.0.0.1",
     "MYSQL_USER": "root",
     "MYSQL_PASSWORD": "", 
     "MYSQL_PORT": "3306"
   }
   ```

2. **Find VS Code settings.json:**
   ```
   C:\Users\[YourUsername]\AppData\Roaming\Code\User\settings.json
   ```

### Windows with XAMPP

1. **Default XAMPP MySQL settings:**
   ```json
   "env": {
     "MYSQL_HOST": "localhost",
     "MYSQL_USER": "root",
     "MYSQL_PASSWORD": "",
     "MYSQL_PORT": "3306"
   }
   ```

### macOS with Homebrew MySQL

1. **Find MySQL credentials:**
   ```bash
   brew services list | grep mysql
   mysql_secure_installation  # Run if not done
   ```

2. **Typical configuration:**
   ```json
   "env": {
     "MYSQL_HOST": "localhost",
     "MYSQL_USER": "root", 
     "MYSQL_PASSWORD": "your_secure_password",
     "MYSQL_PORT": "3306"
   }
   ```

### Linux with Docker

1. **Run MySQL container:**
   ```bash
   docker run --name mysql-dev \
     -e MYSQL_ROOT_PASSWORD=mypassword \
     -p 3306:3306 \
     -d mysql:8.0
   ```

2. **Configuration:**
   ```json
   "env": {
     "MYSQL_HOST": "localhost",
     "MYSQL_USER": "root",
     "MYSQL_PASSWORD": "mypassword",
     "MYSQL_PORT": "3306"
   }
   ```

## 🔧 Verification Steps

### 1. Test Node.js Installation
```bash
node --version  # Should be 18.0.0 or higher
npm --version   # Should be 9.0.0 or higher
```

### 2. Test MySQL Connection
```bash
# From command line
mysql -h 127.0.0.1 -u root -p

# Or using the server directly
node main-universal.cjs
```

### 3. Test VS Code Integration
1. Open VS Code
2. Open GitHub Copilot Chat
3. Type: "Show me all databases"
4. Should return a list of your MySQL databases

## 🚨 Troubleshooting

### Common Issues

**❌ "Cannot find module" error:**
```bash
# Reinstall dependencies
npm install
```

**❌ "Connection refused" error:**
```bash
# Check if MySQL is running
# Windows (Laragon): Start Laragon services
# macOS: brew services start mysql
# Linux: sudo systemctl start mysql
```

**❌ "Access denied" error:**
- Verify username/password in settings.json
- Check MySQL user permissions:
  ```sql
  SHOW GRANTS FOR 'root'@'localhost';
  ```

**❌ VS Code doesn't recognize MCP server:**
- Restart VS Code completely
- Check settings.json syntax with JSON validator
- Verify file paths are absolute and correct

### Advanced Debugging

**Enable verbose logging:**
```json
"env": {
  "MYSQL_HOST": "127.0.0.1",
  "MYSQL_USER": "root", 
  "MYSQL_PASSWORD": "password",
  "MYSQL_PORT": "3306",
  "DEBUG": "true"
}
```

**Test server manually:**
```bash
cd /path/to/mysql-mcp-universal
node main-universal.cjs
# Should output: "Servidor MCP MySQL Universal iniciado - JavaScript"
```

## 🔄 Updating

### NPM Global Install
```bash
npm update -g mysql-mcp-universal
```

### Local Install
```bash
cd mysql-mcp-universal
git pull origin main
npm install
```

## 📞 Getting Help

If you're still having issues:

1. **Check our FAQ**: [GitHub Wiki](https://github.com/[username]/mysql-mcp-universal/wiki/FAQ)
2. **Search existing issues**: [GitHub Issues](https://github.com/[username]/mysql-mcp-universal/issues)
3. **Create new issue** with:
   - Your operating system
   - Node.js version
   - VS Code version
   - Complete error message
   - Your settings.json configuration (remove passwords!)

---

**Need help?** Join our community discussions on GitHub! 🤝
