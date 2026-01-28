"""CLI entry point for dbinit tool."""

import sys
import click
from pathlib import Path
from .commands import create_project, show_credentials
from .setup_wizard import run_setup_wizard, show_config
from .config import get_config_value
from .upgrade import upgrade_database_project


@click.group()
@click.version_option(version="0.2.4")
def cli():
    """dbinit - Interactive database initialization tool."""
    pass


@cli.command()
@click.argument("project", type=str)
def create(project: str):
    """Create a new database project with interactive credential setup."""
    try:
        # Interactive database type selection
        from .setup_wizard import prompt_choice
        
        click.echo("\n" + "="*60)
        click.echo("  Database Type Selection")
        click.echo("="*60)
        click.echo("\nWhich database type would you like to use?")
        
        db_options = ["PostgreSQL (via Docker)", "SQLite"]
        default_db = get_config_value("default_db_type", "postgres")
        default_idx = 1 if default_db == "postgres" else 2
        
        choice = prompt_choice(
            "Select database type:",
            db_options,
            default=default_idx
        )
        
        db = "postgres" if choice == 1 else "sqlite"
        click.echo(f"\n✓ Selected: {db_options[choice - 1]}\n")
        
        # Always run in interactive mode for better UX
        create_project(project, db.lower(), interactive=True)
    except KeyboardInterrupt:
        click.echo("\n\nOperation cancelled by user.", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"\nError: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option(
    "--show",
    is_flag=True,
    help="Show stored database credentials"
)
@click.argument("project", type=str, required=False)
def creds(show: bool, project: str):
    """Manage database credentials for a project."""
    if not show:
        click.echo("Use --show flag to display credentials.", err=True)
        sys.exit(1)
    
    if not project:
        click.echo("Error: Project name is required.", err=True)
        sys.exit(1)
    
    try:
        show_credentials(project)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option(
    "--show",
    is_flag=True,
    help="Show current configuration"
)
def setup(show: bool):
    """Run interactive setup wizard to configure dbinit."""
    if show:
        try:
            show_config()
        except Exception as e:
            click.echo(f"Error: {e}", err=True)
            sys.exit(1)
    else:
        try:
            run_setup_wizard()
        except KeyboardInterrupt:
            click.echo("\n\nSetup cancelled by user.", err=True)
            sys.exit(1)
        except Exception as e:
            click.echo(f"\nError: {e}", err=True)
            sys.exit(1)


@cli.command()
@click.argument("project", type=str)
def upgrade_db(project: str):
    """Upgrade a database project to the current dbinit version."""
    try:
        upgrade_database_project(project)
    except KeyboardInterrupt:
        click.echo("\n\nUpgrade cancelled by user.", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"\nError: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    cli()
