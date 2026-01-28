"""File generation utilities for dbinit."""

from pathlib import Path
from typing import Optional


def generate_docker_compose(project_name: str, username: str, password: str) -> str:
    """Generate docker-compose.yml for PostgreSQL.
    
    Args:
        project_name: Name of the project
        username: Database username
        password: Database password
        
    Returns:
        Docker Compose file content
    """
    return f"""version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    container_name: {project_name}_postgres
    environment:
      POSTGRES_USER: {username}
      POSTGRES_PASSWORD: {password}
      POSTGRES_DB: {project_name}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U {username}"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
"""


def generate_env_file(db_type: str, username: str, password: str, project_name: str) -> str:
    """Generate .env file with database credentials.
    
    Args:
        db_type: Type of database ('postgres' or 'sqlite')
        username: Database username
        password: Database password
        project_name: Name of the project/database
        
    Returns:
        .env file content
    """
    if db_type == "postgres":
        return f"""# Database Configuration
DB_TYPE=postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME={project_name}
DB_USER={username}
DB_PASSWORD={password}

# Docker Compose Environment Variables
POSTGRES_USER={username}
POSTGRES_PASSWORD={password}
POSTGRES_DB={project_name}
"""
    elif db_type == "sqlite":
        return f"""# Database Configuration
DB_TYPE=sqlite
DB_NAME={project_name}.db
DB_USER={username}
DB_PASSWORD={password}
"""
    else:
        raise ValueError(f"Unsupported database type: {db_type}")


def generate_gitignore() -> str:
    """Generate .gitignore file.
    
    Returns:
        .gitignore file content
    """
    return """# Environment variables
.env
.env.local
.env.*.local

# Database files
*.db
*.sqlite
*.sqlite3

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Migrations (uncomment if you want to ignore migration files)
# migrations/
"""


def generate_readme(project_name: str, db_type: str, username: str) -> str:
    """Generate README.md file.
    
    Args:
        project_name: Name of the project
        db_type: Type of database
        username: Database username
        
    Returns:
        README.md file content
    """
    if db_type == "postgres":
        db_section = f"""## Database Setup

This project uses PostgreSQL running in Docker.

### Starting the Database

```bash
docker-compose up -d
```

### Stopping the Database

```bash
docker-compose down
```

### Viewing Logs

```bash
docker-compose logs -f postgres
```

### Connection Details

- Host: localhost
- Port: 5432
- Database: {project_name}
- Username: {username}
- Password: See `.env` file or run `dbinit creds --show {project_name}`
"""
    else:
        db_section = f"""## Database Setup

This project uses SQLite.

The database file will be created automatically on first connection.

### Database File Location

The SQLite database file (`{project_name}.db`) will be created in the project root directory when your application first connects to it.

**Full path:** `{project_name}.db` (in this directory)

### Connection Details

- Database file: `{project_name}.db`
- Database location: Project root directory
- Username: {username}
- Password: See `.env` file or run `dbinit creds --show {project_name}`

**Note:** The database file is automatically added to `.gitignore` to prevent accidental commits.
"""
    
    return f"""# {project_name}

Database project initialized with dbinit.

{db_section}

## Environment Variables

Database credentials are stored in the `.env` file. **Never commit this file to version control.**

To view credentials:
```bash
dbinit creds --show {project_name}
```

## Migrations

Database migrations should be placed in the `migrations/` directory.

## Development

### Connecting to the Database

**Quick Connect (Recommended):**
```python
import dbinit
import sqlite3

# Get connection info (automatically reads from .env)
conn_info = dbinit.connect()

# Access connection details (with helpful comments!)
db_path = conn_info.db_path        # Full path to SQLite database file (e.g., '/path/to/test.db')
db_username = conn_info.db_username  # Database username from .env file
db_password = conn_info.db_password  # Database password from .env file
db_name = conn_info.db_name         # Database name (e.g., 'test.db' for SQLite)

# Connect to SQLite
conn = dbinit.get_sqlite_connection()  # Returns sqlite3.Connection
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
conn.commit()
conn.close()
```

**Manual Connection:**
```python
import sqlite3
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Get database path
db_name = os.getenv("DB_NAME", "{project_name}.db")
db_path = Path(".") / db_name

# Connect (SQLite doesn't require username/password)
conn = sqlite3.connect(str(db_path))
cursor = conn.cursor()

# Use the database
cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
conn.commit()
conn.close()
```

**Using Command Line:**
```bash
# Install sqlite3 if needed (usually pre-installed on macOS/Linux)
sqlite3 {project_name}.db

# Then run SQL commands:
# .tables          # List all tables
# .schema          # Show database schema
# SELECT * FROM users;
# .quit            # Exit
```

**Using Python-dotenv:**
```bash
pip install python-dotenv
```

**Note:** SQLite doesn't enforce username/password authentication. The credentials in `.env` are stored for reference and consistency with PostgreSQL projects.

## Security Notes

- The `.env` file is automatically added to `.gitignore`
- Never share or commit database credentials
- Use strong passwords in production environments
"""


def create_migrations_directory(project_path: Path):
    """Create migrations directory with a .gitkeep file.
    
    Args:
        project_path: Path to the project directory
    """
    migrations_dir = project_path / "migrations"
    migrations_dir.mkdir(exist_ok=True)
    (migrations_dir / ".gitkeep").touch()
