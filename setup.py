"""
Setup script para Database-Connect
"""

from setuptools import setup, find_packages
from pathlib import Path

# Leer README
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

setup(
    name="database-connect",
    version="0.1.0",
    author="Database-Connect Team",
    author_email="info@database-connect.com",
    description="Herramienta MCP para gestión inteligente de bases de datos MySQL y PostgreSQL",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tu-usuario/database-connect",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Database",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.10",
    install_requires=[
        "fastmcp>=0.2.0",
        "pymysql>=1.1.0",
        "mysql-connector-python>=8.2.0",
        "psycopg2-binary>=2.9.9",
        "python-dotenv>=1.0.0",
        "pydantic>=2.5.0",
        "pydantic-settings>=2.1.0",
        "typing-extensions>=4.9.0",
        "click>=8.1.7",
        "cryptography>=41.0.0",
        "colorlog>=6.8.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.3",
            "pytest-asyncio>=0.21.1",
            "pytest-cov>=4.1.0",
            "black>=23.12.0",
            "flake8>=6.1.0",
            "mypy>=1.7.1",
        ],
    },
    entry_points={
        "console_scripts": [
            "database-connect=src.server:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.json", "*.md"],
    },
    keywords="database mysql postgresql mcp github-copilot ai",
    project_urls={
        "Bug Reports": "https://github.com/tu-usuario/database-connect/issues",
        "Source": "https://github.com/tu-usuario/database-connect",
        "Documentation": "https://github.com/tu-usuario/database-connect#readme",
    },
)
