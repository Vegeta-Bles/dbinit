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
        click.echo(f"  # Database is already running")
        compose_cmd = get_config_value("docker_compose_cmd", "docker-compose")
        click.echo(f"  # To stop: {compose_cmd} down")
        click.echo(f"  # To start: {compose_cmd} up -d")
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
