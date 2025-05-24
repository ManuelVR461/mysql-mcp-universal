-- 🚀 MySQL MCP Universal - Docker Initialization Script
-- This script creates sample databases and tables for testing

-- 📝 Create sample databases
CREATE DATABASE IF NOT EXISTS sample_ecommerce;
CREATE DATABASE IF NOT EXISTS sample_blog;
CREATE DATABASE IF NOT EXISTS sample_analytics;

-- 👤 Create additional users
CREATE USER IF NOT EXISTS 'mcpuser'@'%' IDENTIFIED BY 'mcppass';
CREATE USER IF NOT EXISTS 'readonly'@'%' IDENTIFIED BY 'readonly123';

-- 🔑 Grant permissions
GRANT ALL PRIVILEGES ON *.* TO 'mcpuser'@'%';
GRANT SELECT ON *.* TO 'readonly'@'%';
FLUSH PRIVILEGES;

-- 🛍️ Sample E-commerce Database
USE sample_ecommerce;

CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    category_id INT,
    stock_quantity INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

CREATE TABLE IF NOT EXISTS customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    city VARCHAR(50),
    country VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(12,2) NOT NULL,
    status ENUM('pending', 'processing', 'shipped', 'delivered', 'cancelled') DEFAULT 'pending',
    shipping_address TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

CREATE TABLE IF NOT EXISTS order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- 📝 Sample Blog Database
USE sample_blog;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    bio TEXT,
    avatar_url VARCHAR(255),
    is_admin BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL
);

CREATE TABLE IF NOT EXISTS posts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    content LONGTEXT NOT NULL,
    excerpt TEXT,
    author_id INT NOT NULL,
    status ENUM('draft', 'published', 'archived') DEFAULT 'draft',
    featured_image VARCHAR(255),
    views_count INT DEFAULT 0,
    published_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (author_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS comments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    post_id INT NOT NULL,
    author_name VARCHAR(100) NOT NULL,
    author_email VARCHAR(100) NOT NULL,
    content TEXT NOT NULL,
    is_approved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES posts(id)
);

-- 📊 Sample Analytics Database
USE sample_analytics;

CREATE TABLE IF NOT EXISTS website_visits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    visitor_ip VARCHAR(45),
    user_agent TEXT,
    page_url VARCHAR(500),
    referrer_url VARCHAR(500),
    session_id VARCHAR(100),
    visit_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    page_load_time INT, -- milliseconds
    device_type ENUM('desktop', 'mobile', 'tablet') DEFAULT 'desktop'
);

CREATE TABLE IF NOT EXISTS conversion_events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id VARCHAR(100),
    event_type VARCHAR(50) NOT NULL,
    event_value DECIMAL(10,2),
    event_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    additional_data JSON
);

-- 🎲 Insert sample data
USE sample_ecommerce;

INSERT INTO categories (name, description) VALUES
('Electronics', 'Electronic devices and gadgets'),
('Clothing', 'Fashion and apparel'),
('Books', 'Physical and digital books'),
('Home & Garden', 'Home improvement and gardening supplies');

INSERT INTO products (name, description, price, category_id, stock_quantity) VALUES
('Smartphone X1', 'Latest smartphone with advanced features', 699.99, 1, 50),
('Wireless Headphones', 'High-quality wireless headphones', 149.99, 1, 30),
('Cotton T-Shirt', 'Comfortable cotton t-shirt', 19.99, 2, 100),
('Programming Book', 'Learn programming fundamentals', 39.99, 3, 25),
('Garden Tools Set', 'Complete set of garden tools', 89.99, 4, 15);

INSERT INTO customers (first_name, last_name, email, phone, city, country) VALUES
('John', 'Doe', 'john.doe@email.com', '+1-555-0123', 'New York', 'USA'),
('Jane', 'Smith', 'jane.smith@email.com', '+1-555-0124', 'Los Angeles', 'USA'),
('Bob', 'Johnson', 'bob.johnson@email.com', '+1-555-0125', 'Chicago', 'USA');

USE sample_blog;

INSERT INTO users (username, email, password_hash, full_name, bio) VALUES
('admin', 'admin@blog.com', 'hashed_password_123', 'Admin User', 'Site administrator'),
('writer1', 'writer1@blog.com', 'hashed_password_456', 'Alice Writer', 'Technology blogger'),
('writer2', 'writer2@blog.com', 'hashed_password_789', 'Bob Blogger', 'Lifestyle content creator');

INSERT INTO posts (title, slug, content, excerpt, author_id, status, published_at) VALUES
('Welcome to Our Blog', 'welcome-to-our-blog', 'This is our first blog post...', 'Welcome post excerpt', 1, 'published', NOW()),
('Tech Trends 2024', 'tech-trends-2024', 'Here are the latest tech trends...', 'Technology trends overview', 2, 'published', NOW()),
('Lifestyle Tips', 'lifestyle-tips', 'Improve your daily routine with these tips...', 'Daily lifestyle improvements', 3, 'draft', NULL);

-- 📊 Sample analytics data
USE sample_analytics;

INSERT INTO website_visits (visitor_ip, page_url, device_type, page_load_time) VALUES
('192.168.1.100', '/home', 'desktop', 1200),
('192.168.1.101', '/products', 'mobile', 1800),
('192.168.1.102', '/about', 'tablet', 1500),
('192.168.1.103', '/contact', 'desktop', 900);

-- ✅ Verification queries
SELECT '🎉 Sample databases created successfully!' as message;
SELECT 'sample_ecommerce' as database_name, COUNT(*) as table_count FROM information_schema.tables WHERE table_schema = 'sample_ecommerce'
UNION ALL
SELECT 'sample_blog', COUNT(*) FROM information_schema.tables WHERE table_schema = 'sample_blog'  
UNION ALL
SELECT 'sample_analytics', COUNT(*) FROM information_schema.tables WHERE table_schema = 'sample_analytics';

-- 📝 Show sample data counts
SELECT 
    'sample_ecommerce' as database_name,
    'products' as table_name,
    (SELECT COUNT(*) FROM sample_ecommerce.products) as row_count
UNION ALL
SELECT 'sample_blog', 'posts', (SELECT COUNT(*) FROM sample_blog.posts)
UNION ALL  
SELECT 'sample_analytics', 'website_visits', (SELECT COUNT(*) FROM sample_analytics.website_visits);

SELECT '🚀 MySQL MCP Universal Docker setup complete!' as final_message;
