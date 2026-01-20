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

### Connection Details

- Database file: `{project_name}.db`
- Username: {username}
- Password: See `.env` file or run `dbinit creds --show {project_name}`
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

1. Load environment variables from `.env`:
   ```bash
   export $(cat .env | xargs)
   ```

2. Connect to the database using your preferred database client or ORM.

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
