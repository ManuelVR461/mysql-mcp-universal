# 🚀 MySQL MCP Universal Server - Docker Image
FROM node:18-alpine

# 📋 Metadata
LABEL maintainer="MySQL MCP Universal Community"
LABEL description="Universal MySQL MCP Server for GitHub Copilot integration"
LABEL version="2.0.1"

# 🔧 Install dependencies for MySQL connectivity
RUN apk add --no-cache \
    mysql-client \
    bash \
    curl

# 👤 Create non-root user for security
RUN addgroup -g 1001 -S mcp && \
    adduser -S mcp -u 1001 -G mcp

# 📁 Set working directory
WORKDIR /app

# 📦 Copy package files
COPY package*.json ./

# 🏗️ Install Node.js dependencies
RUN npm ci --only=production && \
    npm cache clean --force

# 📋 Copy application files
COPY main-universal.cjs ./
COPY .env.example ./.env

# 🔒 Set correct permissions
RUN chown -R mcp:mcp /app
USER mcp

# 🌐 Expose port (for health checks)
EXPOSE 3000

# ✅ Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD node -e "console.log('MySQL MCP Universal Server is healthy')" || exit 1

# 🔧 Environment variables with defaults
ENV MYSQL_HOST=127.0.0.1
ENV MYSQL_PORT=3306
ENV MYSQL_USER=root
ENV MYSQL_PASSWORD=""

# 🚀 Start the server
CMD ["node", "main-universal.cjs"]
