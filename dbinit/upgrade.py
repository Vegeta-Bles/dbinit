"""Database upgrade utilities for dbinit."""

import json
import click
from pathlib import Path
from typing import Dict, Optional
from .config import get_config_value
from .generators import (
    generate_docker_compose,
    generate_env_file,
    generate_gitignore,
    generate_readme,
    create_migrations_directory
)


def get_project_version(project_path: Path) -> Optional[str]:
    """Get the dbinit version used to create a project.
    
    Args:
        project_path: Path to the project directory
        
    Returns:
        Version string or None if not found
    """
    version_file = project_path / ".dbinit-version"
    if version_file.exists():
        return version_file.read_text().strip()
    return None


def set_project_version(project_path: Path, version: str):
    """Set the dbinit version for a project.
    
    Args:
        project_path: Path to the project directory
        version: Version string
    """
    version_file = project_path / ".dbinit-version"
    version_file.write_text(version)


def detect_project_type(project_path: Path) -> Optional[str]:
    """Detect the database type of a project.
    
    Args:
        project_path: Path to the project directory
        
    Returns:
        'postgres' or 'sqlite' or None
    """
    # Check for docker-compose.yml (PostgreSQL)
    if (project_path / "docker-compose.yml").exists():
        return "postgres"
    
    # Check .env file
    env_file = project_path / ".env"
    if env_file.exists():
        with open(env_file, "r") as f:
            content = f.read()
            if "DB_TYPE=postgres" in content or "POSTGRES_USER" in content:
                return "postgres"
            elif "DB_TYPE=sqlite" in content:
                return "sqlite"
    
    return None


def upgrade_project(project_path: Path, current_version: str, target_version: str):
    """Upgrade a project to a new dbinit version.
    
    Args:
        project_path: Path to the project directory
        current_version: Current dbinit version
        target_version: Target dbinit version
    """
    db_type = detect_project_type(project_path)
    
    if not db_type:
        raise ValueError("Could not detect project database type. Is this a dbinit project?")
    
    click.echo(f"\nUpgrading project from dbinit {current_version} to {target_version}...")
    
    # Read existing .env to preserve credentials
    env_file = project_path / ".env"
    existing_credentials = {}
    if env_file.exists():
        with open(env_file, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    existing_credentials[key.strip()] = value.strip()
    
    # Extract credentials
    username = existing_credentials.get("DB_USER") or existing_credentials.get("POSTGRES_USER", "")
    password = existing_credentials.get("DB_PASSWORD") or existing_credentials.get("POSTGRES_PASSWORD", "")
    db_name = existing_credentials.get("DB_NAME") or existing_credentials.get("POSTGRES_DB", project_path.name)
    
    if not username or not password:
        click.echo("Warning: Could not find credentials in .env file.", err=True)
        click.echo("You may need to update credentials manually.", err=True)
        username = username or "admin"
        password = password or "changeme"
    
    # Regenerate files with current templates
    click.echo("\nRegenerating project files...")
    
    if db_type == "postgres":
        # Regenerate docker-compose.yml
        docker_compose_content = generate_docker_compose(db_name, username, password)
        (project_path / "docker-compose.yml").write_text(docker_compose_content)
        click.echo("✓ Updated docker-compose.yml")
    
    # Regenerate .env file (preserving credentials)
    env_content = generate_env_file(db_type, username, password, db_name)
    (project_path / ".env").write_text(env_content)
    click.echo("✓ Updated .env file")
    
    # Update .gitignore if needed
    gitignore_file = project_path / ".gitignore"
    if not gitignore_file.exists():
        gitignore_content = generate_gitignore()
        gitignore_file.write_text(gitignore_content)
        click.echo("✓ Added .gitignore")
    
    # Ensure migrations directory exists
    create_migrations_directory(project_path)
    click.echo("✓ Ensured migrations/ directory exists")
    
    # Update README if it's the old format
    readme_file = project_path / "README.md"
    if readme_file.exists():
        readme_content = generate_readme(db_name, db_type, username)
        readme_file.write_text(readme_content)
        click.echo("✓ Updated README.md")
    
    # Update version marker
    set_project_version(project_path, target_version)
    click.echo("✓ Updated version marker")
    
    click.echo(f"\n✓ Project upgraded successfully to dbinit {target_version}!")


def upgrade_database_project(project_name: str):
    """Upgrade a database project to the current dbinit version.
    
    Args:
        project_name: Name or path of the project to upgrade
    """
    from .config import get_default_project_path
    from .__init__ import __version__
    
    # Resolve project path
    if Path(project_name).is_absolute():
        project_path = Path(project_name)
    else:
        default_path = get_default_project_path()
        project_path = default_path / project_name
    
    if not project_path.exists():
        raise FileNotFoundError(f"Project '{project_name}' not found at {project_path}")
    
    if not project_path.is_dir():
        raise ValueError(f"'{project_name}' is not a directory")
    
    # Check if it's a dbinit project
    if not (project_path / ".env").exists():
        raise ValueError(f"'{project_name}' doesn't appear to be a dbinit project (no .env file found)")
    
    # Get current version
    current_version = get_project_version(project_path)
    target_version = __version__
    
    if current_version == target_version:
        click.echo(f"Project is already at dbinit version {target_version}. No upgrade needed.")
        return
    
    if current_version:
        click.echo(f"Current project version: {current_version}")
    else:
        click.echo("No version marker found. This appears to be an older project.")
        if not click.confirm("Proceed with upgrade?"):
            click.echo("Upgrade cancelled.")
            return
    
    click.echo(f"Target version: {target_version}")
    
    try:
        upgrade_project(project_path, current_version or "unknown", target_version)
    except Exception as e:
        click.echo(f"Error during upgrade: {e}", err=True)
        raise
