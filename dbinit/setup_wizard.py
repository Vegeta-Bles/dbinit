"""Interactive setup wizard for dbinit configuration."""

import os
import shutil
import subprocess
import click
from pathlib import Path
from .config import (
    load_config,
    save_config,
    get_config_value,
    set_config_value,
    get_default_project_path
)
from .commands import create_project, prompt_credentials
from .validators import validate_password_strength
import getpass
import re


def detect_available_editors():
    """Detect available text editors on the system.
    
    Returns:
        List of tuples (name, command, available)
    """
    editors = [
        ("VS Code", "code", "code"),
        ("VS Code (Insiders)", "code-insiders", "code-insiders"),
        ("Sublime Text", "subl", "subl"),
        ("Atom", "atom", "atom"),
        ("Vim", "vim", "vim"),
        ("Nano", "nano", "nano"),
        ("Emacs", "emacs", "emacs"),
        ("Nvim (Neovim)", "nvim", "nvim"),
        ("PyCharm", "pycharm", "pycharm"),
        ("IntelliJ IDEA", "idea", "idea"),
    ]
    
    available = []
    for name, command, check_cmd in editors:
        # Check if command exists
        result = subprocess.run(
            ["which", check_cmd],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            available.append((name, command))
    
    # Add $EDITOR if set
    if os.environ.get("EDITOR"):
        editor_cmd = os.environ.get("EDITOR")
        if editor_cmd not in [cmd for _, cmd in available]:
            available.append(("$EDITOR", editor_cmd))
    
    # Always add custom option
    available.append(("Custom (enter command)", None))
    
    return available


def prompt_choice(prompt_text: str, options: list, default: int = None) -> int:
    """Prompt user to choose from numbered options.
    
    Args:
        prompt_text: Text to display before options
        options: List of option strings
        default: Default option index (1-based)
        
    Returns:
        Selected option index (1-based)
    """
    click.echo(f"\n{prompt_text}")
    for i, option in enumerate(options, 1):
        marker = " (default)" if default and i == default else ""
        click.echo(f"  {i}. {option}{marker}")
    
    while True:
        try:
            choice = click.prompt(
                f"\n  Select option (1-{len(options)})",
                default=default or 1,
                type=int
            )
            if 1 <= choice <= len(options):
                return choice
            else:
                click.echo(f"  Please enter a number between 1 and {len(options)}.", err=True)
        except (ValueError, click.Abort):
            click.echo("  Invalid input. Please enter a number.", err=True)


def run_setup_wizard():
    """Run the interactive setup wizard."""
    click.echo("\n" + "="*60)
    click.echo("  dbinit Setup Wizard")
    click.echo("="*60 + "\n")
    
    click.echo("This wizard will help you configure dbinit and create your first database.")
    click.echo("You can skip any step by pressing Enter to use defaults.\n")
    
    config = load_config()
    
    # 1. Default project path
    click.echo("=" * 60)
    click.echo("1. Default Project Path")
    click.echo("=" * 60)
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
    
    # 2. Default database type (with numbered choices)
    click.echo("\n" + "=" * 60)
    click.echo("2. Default Database Type")
    click.echo("=" * 60)
    click.echo("   Which database type do you use most often?")
    current_db = get_config_value("default_db_type", "postgres")
    
    db_options = ["PostgreSQL", "SQLite"]
    default_db_idx = 1 if current_db == "postgres" else 2
    
    choice = prompt_choice(
        "   Select database type:",
        db_options,
        default=default_db_idx
    )
    
    db_type = "postgres" if choice == 1 else "sqlite"
    config["default_db_type"] = db_type
    
    # 3. Docker Compose command (with numbered choices)
    click.echo("\n" + "=" * 60)
    click.echo("3. Docker Compose Command")
    click.echo("=" * 60)
    click.echo("   Which Docker Compose command should be used?")
    current_compose_cmd = get_config_value("docker_compose_cmd", "docker-compose")
    
    compose_options = ["docker compose (v2)", "docker-compose (v1)"]
    default_compose_idx = 1 if current_compose_cmd == "docker compose" else 2
    
    choice = prompt_choice(
        "   Pick which command we should use:",
        compose_options,
        default=default_compose_idx
    )
    
    compose_cmd = "docker compose" if choice == 1 else "docker-compose"
    config["docker_compose_cmd"] = compose_cmd
    
    # 4. Editor selection (with detection)
    click.echo("\n" + "=" * 60)
    click.echo("4. Default Editor")
    click.echo("=" * 60)
    click.echo("   Which editor should be used for opening project files?")
    
    available_editors = detect_available_editors()
    current_editor = get_config_value("default_editor", os.environ.get("EDITOR", "nano"))
    
    if not available_editors:
        # Fallback if no editors detected
        editor = click.prompt(
            "\n   Enter editor command",
            default=current_editor,
            type=str
        )
    else:
        editor_names = [name for name, _ in available_editors]
        
        # Find current editor in list
        default_editor_idx = None
        for i, (name, cmd) in enumerate(available_editors, 1):
            if cmd == current_editor or name == current_editor:
                default_editor_idx = i
                break
        
        choice = prompt_choice(
            "   Select editor:",
            editor_names,
            default=default_editor_idx or 1
        )
        
        selected_name, selected_cmd = available_editors[choice - 1]
        
        if selected_cmd is None:  # Custom option
            editor = click.prompt(
                "\n   Enter editor command",
                default=current_editor,
                type=str
            )
        else:
            editor = selected_cmd
    
    config["default_editor"] = editor
    
    # 5. Auto-start database
    click.echo("\n" + "=" * 60)
    click.echo("5. Auto-start Database")
    click.echo("=" * 60)
    click.echo("   Should databases automatically start after creation?")
    current_auto_start = get_config_value("auto_start_db", True)
    click.echo(f"   Current: {'Yes' if current_auto_start else 'No'}")
    
    auto_start = click.confirm(
        "\n   Auto-start database after creation?",
        default=current_auto_start
    )
    config["auto_start_db"] = auto_start
    
    # Save configuration
    save_config(config)
    
    # Summary
    click.echo("\n" + "="*60)
    click.echo("  Configuration Summary")
    click.echo("="*60)
    click.echo(f"\n  Default Project Path: {config['default_project_path']}")
    click.echo(f"  Default Database Type: {config['default_db_type']}")
    click.echo(f"  Docker Compose Command: {config['docker_compose_cmd']}")
    click.echo(f"  Default Editor: {config['default_editor']}")
    click.echo(f"  Auto-start Database: {'Yes' if config['auto_start_db'] else 'No'}")
    click.echo("\n" + "="*60)
    click.echo("\n✓ Configuration saved successfully!")
    
    # 6. Create initial database project
    click.echo("\n" + "="*60)
    click.echo("6. Create Your First Database Project")
    click.echo("="*60)
    
    if click.confirm("\n   Would you like to create a database project now?"):
        # Get project name
        project_name = click.prompt(
            "\n   Enter project name",
            type=str
        )
        
        if not project_name.strip():
            click.echo("   Project name cannot be empty. Skipping project creation.")
        else:
            # Use configured database type
            db_type = config["default_db_type"]
            
            click.echo(f"\n   Creating project '{project_name}' with {db_type} database...")
            
            try:
                create_project(project_name, db_type)
                click.echo("\n✓ Setup complete! Your database project is ready.")
            except Exception as e:
                click.echo(f"\n   Error creating project: {e}", err=True)
                click.echo("   Configuration saved. You can create a project later with:")
                click.echo(f"   dbinit create <project-name> --db {db_type}")
    else:
        click.echo("\n   Skipping project creation.")
        click.echo("   You can create a project later with:")
        click.echo(f"   dbinit create <project-name> --db {config['default_db_type']}")
    
    click.echo("\n" + "="*60)
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
