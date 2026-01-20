"""Interactive setup wizard for dbinit configuration."""

import os
import click
from pathlib import Path
from .config import (
    load_config,
    save_config,
    get_config_value,
    set_config_value,
    get_default_project_path
)


def run_setup_wizard():
    """Run the interactive setup wizard."""
    click.echo("\n" + "="*60)
    click.echo("  dbinit Setup Wizard")
    click.echo("="*60 + "\n")
    
    click.echo("This wizard will help you configure dbinit settings.")
    click.echo("You can skip any step by pressing Enter to use defaults.\n")
    
    config = load_config()
    
    # 1. Default project path
    click.echo("1. Default Project Path")
    click.echo("   Where should new database projects be created?")
    current_default = get_config_value("default_project_path")
    if current_default:
        click.echo(f"   Current: {current_default}")
    else:
        default_path = str(get_default_project_path())
        click.echo(f"   Default: {default_path}")
    
    project_path = click.prompt(
        "\n   Enter path (or press Enter for default)",
        default=current_default or str(get_default_project_path()),
        type=str
    )
    
    # Validate and expand path
    try:
        expanded_path = Path(project_path).expanduser()
        if not expanded_path.exists():
            if click.confirm(f"   Path '{expanded_path}' doesn't exist. Create it?"):
                expanded_path.mkdir(parents=True, exist_ok=True)
            else:
                click.echo("   Using current directory instead.")
                expanded_path = Path.cwd()
        config["default_project_path"] = str(expanded_path)
    except Exception as e:
        click.echo(f"   Error with path: {e}. Using default.", err=True)
        config["default_project_path"] = str(get_default_project_path())
    
    # 2. Default database type
    click.echo("\n2. Default Database Type")
    click.echo("   Which database type do you use most often?")
    current_db = get_config_value("default_db_type", "postgres")
    click.echo(f"   Current: {current_db}")
    
    db_type = click.prompt(
        "\n   Enter database type (postgres/sqlite)",
        default=current_db,
        type=click.Choice(["postgres", "sqlite"], case_sensitive=False)
    )
    config["default_db_type"] = db_type.lower()
    
    # 3. Auto-start database
    click.echo("\n3. Auto-start Database")
    click.echo("   Should databases automatically start after creation?")
    current_auto_start = get_config_value("auto_start_db", True)
    click.echo(f"   Current: {'Yes' if current_auto_start else 'No'}")
    
    auto_start = click.confirm(
        "\n   Auto-start database after creation?",
        default=current_auto_start
    )
    config["auto_start_db"] = auto_start
    
    # 4. Docker Compose path
    click.echo("\n4. Docker Compose Command")
    click.echo("   Which command should be used for Docker Compose?")
    current_compose_cmd = get_config_value("docker_compose_cmd", "docker-compose")
    click.echo(f"   Current: {current_compose_cmd}")
    click.echo("   Options: 'docker-compose' or 'docker compose' (v2)")
    
    compose_cmd = click.prompt(
        "\n   Enter command",
        default=current_compose_cmd,
        type=str
    )
    config["docker_compose_cmd"] = compose_cmd
    
    # 5. Editor preference
    click.echo("\n5. Default Editor")
    click.echo("   Which editor should be used for opening project files?")
    current_editor = get_config_value("default_editor", os.environ.get("EDITOR", "nano"))
    click.echo(f"   Current: {current_editor}")
    
    editor = click.prompt(
        "\n   Enter editor command",
        default=current_editor,
        type=str
    )
    config["default_editor"] = editor
    
    # Save configuration
    save_config(config)
    
    # Summary
    click.echo("\n" + "="*60)
    click.echo("  Configuration Summary")
    click.echo("="*60)
    click.echo(f"\n  Default Project Path: {config['default_project_path']}")
    click.echo(f"  Default Database Type: {config['default_db_type']}")
    click.echo(f"  Auto-start Database: {'Yes' if config['auto_start_db'] else 'No'}")
    click.echo(f"  Docker Compose Command: {config['docker_compose_cmd']}")
    click.echo(f"  Default Editor: {config['default_editor']}")
    click.echo("\n" + "="*60)
    click.echo("\n✓ Configuration saved successfully!")
    click.echo("\nYou can run 'dbinit setup' again anytime to update these settings.")
    click.echo("Configuration file location: ~/.dbinit/config.json\n")


def show_config():
    """Display current configuration."""
    config = load_config()
    
    if not config:
        click.echo("No configuration found. Run 'dbinit setup' to configure.")
        return
    
    click.echo("\n" + "="*60)
    click.echo("  Current dbinit Configuration")
    click.echo("="*60 + "\n")
    
    click.echo(f"  Default Project Path: {config.get('default_project_path', 'Not set')}")
    click.echo(f"  Default Database Type: {config.get('default_db_type', 'Not set')}")
    click.echo(f"  Auto-start Database: {'Yes' if config.get('auto_start_db', True) else 'No'}")
    click.echo(f"  Docker Compose Command: {config.get('docker_compose_cmd', 'docker-compose')}")
    click.echo(f"  Default Editor: {config.get('default_editor', 'Not set')}")
    click.echo(f"\n  Config File: ~/.dbinit/config.json")
    click.echo()
