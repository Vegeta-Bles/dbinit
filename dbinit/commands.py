"""Command implementations for dbinit."""

import os
import re
import shutil
import subprocess
import getpass
from pathlib import Path
from typing import Tuple, Optional
import click
from .validators import validate_password_strength
from .config import get_config_value, get_default_project_path
from .generators import (
    generate_docker_compose,
    generate_env_file,
    generate_gitignore,
    generate_readme,
    create_migrations_directory
)


def prompt_credentials() -> Tuple[str, str]:
    """Interactively prompt for database username and password.
    
    Returns:
        Tuple of (username, password)
    """
    click.echo("\n=== Database Credentials Setup ===\n")
    
    # Prompt for username
    while True:
        username = click.prompt("Database username", type=str)
        if username.strip():
            username = username.strip()
            # Basic validation: alphanumeric and underscore only
            if re.match(r'^[a-zA-Z0-9_]+$', username):
                break
            else:
                click.echo("Username must contain only letters, numbers, and underscores.", err=True)
        else:
            click.echo("Username cannot be empty.", err=True)
    
    # Prompt for password with strength validation
    while True:
        password = getpass.getpass("Database password: ")
        if not password:
            click.echo("Password cannot be empty.", err=True)
            continue
        
        validation_result = validate_password_strength(password)
        if not validation_result["valid"]:
            click.echo(f"Password validation failed: {validation_result['message']}", err=True)
            continue
        
        # Confirm password
        password_confirm = getpass.getpass("Confirm password: ")
        if password != password_confirm:
            click.echo("Passwords do not match. Please try again.", err=True)
            continue
        
        break
    
    return username, password


def create_project(project_name: str, db_type: str, interactive: bool = True):
    """Create a new database project.
    
    Args:
        project_name: Name of the project
        db_type: Type of database ('postgres' or 'sqlite')
        interactive: Whether to run in interactive/guided mode
    """
    from .__init__ import __version__
    
    if interactive:
        click.echo("\n" + "="*60)
        click.echo("  dbinit Project Creation Wizard")
        click.echo("="*60)
        click.echo(f"\nWelcome! Let's set up your '{project_name}' database project.")
        click.echo(f"Database type: {db_type.upper()}\n")
    
    # Use configured default path if project name is relative
    if not Path(project_name).is_absolute():
        default_path = get_default_project_path()
        project_path = default_path / project_name
    else:
        project_path = Path(project_name)
    
    # Check if project already exists
    if project_path.exists():
        if interactive:
            click.echo(f"⚠️  Directory '{project_name}' already exists.")
        if not click.confirm(f"Overwrite existing directory?"):
            click.echo("Operation cancelled.")
            return
        # Remove existing directory
        shutil.rmtree(project_path)
    
    # Create project directory
    project_path.mkdir(parents=True, exist_ok=True)
    
    if interactive:
        click.echo(f"\n📁 Creating project directory: {project_path}")
    
    click.echo(f"\nCreating project '{project_name}' with {db_type} database...")
    
    # Get credentials
    if interactive:
        click.echo("\n" + "-"*60)
        click.echo("  Step 1: Database Credentials")
        click.echo("-"*60)
    username, password = prompt_credentials()
    
    # Generate project files
    if interactive:
        click.echo("\n" + "-"*60)
        click.echo("  Step 2: Generating Project Files")
        click.echo("-"*60)
    click.echo("\nGenerating project files...")
    
    if db_type == "postgres":
        # Generate docker-compose.yml
        docker_compose_content = generate_docker_compose(project_name, username, password)
        (project_path / "docker-compose.yml").write_text(docker_compose_content)
        
        # Generate .env file
        env_content = generate_env_file(db_type, username, password, project_name)
        (project_path / ".env").write_text(env_content)
        
        # Start the database (if auto-start is enabled)
        auto_start = get_config_value("auto_start_db", True)
        if auto_start:
            from .docker_check import check_docker_installed, get_docker_install_command
            
            # Check Docker before attempting to start
            if not check_docker_installed():
                click.echo("\n⚠️  Skipping auto-start: Docker is not installed.", err=True)
                install_cmd = get_docker_install_command()
                click.echo(f"Install Docker with: {install_cmd}", err=True)
                click.echo("After installing Docker, start the database with:", err=True)
                compose_cmd = get_config_value("docker_compose_cmd", "docker-compose")
                click.echo(f"  cd {project_path} && {compose_cmd} up -d", err=True)
            else:
                click.echo("\nStarting database container...")
                compose_cmd = get_config_value("docker_compose_cmd", "docker-compose")
                try:
                    # Handle both "docker-compose" and "docker compose" (v2)
                    if compose_cmd == "docker compose":
                        cmd = ["docker", "compose", "up", "-d"]
                    else:
                        cmd = [compose_cmd, "up", "-d"]
                    
                    subprocess.run(
                        cmd,
                        cwd=project_path,
                        check=True,
                        capture_output=True
                    )
                    click.echo("✓ Database container started successfully!")
                except subprocess.CalledProcessError as e:
                    click.echo(f"Warning: Failed to start database container: {e}", err=True)
                    click.echo(f"You can start it manually with: {compose_cmd} up -d", err=True)
                except FileNotFoundError:
                    click.echo("Warning: docker-compose not found. Please install Docker Compose.", err=True)
                    install_cmd = get_docker_install_command()
                    click.echo(f"Install Docker with: {install_cmd}", err=True)
                    click.echo(f"You can start the database later with: {compose_cmd} up -d", err=True)
        else:
            click.echo("\nSkipping auto-start (disabled in configuration).")
            compose_cmd = get_config_value("docker_compose_cmd", "docker-compose")
            click.echo(f"Start manually with: cd {project_path} && {compose_cmd} up -d")
    
    elif db_type == "sqlite":
        # For SQLite, just create the .env file
        env_content = generate_env_file(db_type, username, password, project_name)
        (project_path / ".env").write_text(env_content)
        click.echo("✓ SQLite database will be created on first connection.")
    
    # Generate .gitignore
    gitignore_content = generate_gitignore()
    (project_path / ".gitignore").write_text(gitignore_content)
    
    # Create migrations directory
    create_migrations_directory(project_path)
    
    # Generate README.md
    readme_content = generate_readme(project_name, db_type, username)
    (project_path / "README.md").write_text(readme_content)
    
    # Save version marker
    from .__init__ import __version__
    (project_path / ".dbinit-version").write_text(__version__)
    
    if interactive:
        click.echo("\n" + "="*60)
        click.echo("  ✓ Project Created Successfully!")
        click.echo("="*60)
    else:
        click.echo(f"\n✓ Project '{project_name}' created successfully!")
    
    click.echo(f"\n📦 Project Location: {project_path}")
    click.echo(f"\n🚀 Next Steps:")
    click.echo(f"  cd {project_path.name}")
    if db_type == "postgres":
        from .docker_check import check_docker_installed
        if check_docker_installed():
            click.echo(f"  # Database is already running")
            compose_cmd = get_config_value("docker_compose_cmd", "docker-compose")
            click.echo(f"  # To stop: {compose_cmd} down")
            click.echo(f"  # To start: {compose_cmd} up -d")
        else:
            compose_cmd = get_config_value("docker_compose_cmd", "docker-compose")
            click.echo(f"  # Install Docker first, then start with: {compose_cmd} up -d")
    elif db_type == "sqlite":
        db_file = f"{project_name}.db"
        click.echo(f"  # Database file: {db_file} (created on first connection)")
        click.echo(f"  # Database location: {project_path / db_file}")
    click.echo(f"  # View credentials: dbinit creds --show {project_name}")
    click.echo(f"  # Upgrade project: dbinit upgrade-db {project_name}")


def show_credentials(project_name: str):
    """Show stored credentials for a project.
    
    Args:
        project_name: Name of the project
    """
    project_path = Path(project_name)
    env_file = project_path / ".env"
    
    if not project_path.exists():
        raise FileNotFoundError(f"Project '{project_name}' does not exist.")
    
    if not env_file.exists():
        raise FileNotFoundError(f"No .env file found in project '{project_name}'.")
    
    # Read and parse .env file
    env_vars = {}
    with open(env_file, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                env_vars[key.strip()] = value.strip()
    
    click.echo(f"\n=== Credentials for project '{project_name}' ===\n")
    
    if "DB_USER" in env_vars:
        click.echo(f"Username: {env_vars['DB_USER']}")
    if "POSTGRES_USER" in env_vars:
        click.echo(f"Username: {env_vars['POSTGRES_USER']}")
    
    if "DB_PASSWORD" in env_vars:
        click.echo(f"Password: {env_vars['DB_PASSWORD']}")
    if "POSTGRES_PASSWORD" in env_vars:
        click.echo(f"Password: {env_vars['POSTGRES_PASSWORD']}")
    
    if "DB_NAME" in env_vars:
        click.echo(f"Database: {env_vars['DB_NAME']}")
    if "POSTGRES_DB" in env_vars:
        click.echo(f"Database: {env_vars['POSTGRES_DB']}")
    
    click.echo()


def add_row_to_table(project_name: str, table_name: str, data: tuple):
    """Add a row to a database table.
    
    Args:
        project_name: Name or path of the project
        table_name: Name of the table to insert into
        data: Tuple of key=value pairs (e.g., ("name=John Doe", "email=john@example.com"))
    """
    import json
    import shlex
    from .connect import connect, get_connection_info
    
    # Find project directory
    project_path = Path(project_name)
    if not project_path.is_absolute():
        default_path = get_default_project_path()
        project_path = default_path / project_name
    
    if not project_path.exists():
        raise FileNotFoundError(f"Project '{project_name}' does not exist.")
    
    env_file = project_path / ".env"
    if not env_file.exists():
        raise FileNotFoundError(f"No .env file found in project '{project_name}'.")
    
    # Parse data from key=value pairs
    row_data = {}
    for item in data:
        if "=" not in item:
            raise ValueError(f"Invalid data format: '{item}'. Expected format: key=value")
        
        key, value = item.split("=", 1)
        key = key.strip()
        value = value.strip()
        
        # Remove quotes if present
        if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
            value = value[1:-1]
        
        # Try to parse as JSON (for numbers, booleans, etc.)
        try:
            value = json.loads(value)
        except (json.JSONDecodeError, ValueError):
            # Keep as string if not valid JSON
            pass
        
        row_data[key] = value
    
    if not row_data:
        raise ValueError("No data provided. Use format: key=value")
    
    # Connect to database
    try:
        conn = connect(project_path)
        # Check if psycopg2 is not installed (connect returns string instead of connection)
        if isinstance(conn, str):
            raise ImportError(
                "psycopg2 is required for PostgreSQL databases. "
                "Install it with: pip install psycopg2-binary"
            )
    except ImportError:
        raise
    except Exception as e:
        raise ConnectionError(f"Failed to connect to database: {e}")
    
    try:
        cursor = conn.cursor()
        
        # Get database type
        info = get_connection_info(project_path)
        db_type = info.get("db_type", "sqlite")
        
        # Build INSERT statement
        columns = list(row_data.keys())
        values = list(row_data.values())
        
        if db_type == "sqlite":
            placeholders = ", ".join(["?" for _ in columns])
        else:  # postgres
            placeholders = ", ".join(["%s" for _ in columns])
        
        columns_str = ", ".join(columns)
        insert_sql = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"
        
        # Execute insert
        try:
            cursor.execute(insert_sql, values)
            conn.commit()
            click.echo(f"✓ Successfully added row to '{table_name}' table")
        except Exception as e:
            conn.rollback()
            raise ValueError(f"Failed to insert row: {e}")
        
    finally:
        conn.close()
