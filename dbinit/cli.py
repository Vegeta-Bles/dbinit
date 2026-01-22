"""CLI entry point for dbinit tool."""

import sys
import click
from pathlib import Path
from .commands import create_project, show_credentials
from .setup_wizard import run_setup_wizard, show_config
from .config import get_config_value
from .upgrade import upgrade_database_project


@click.group()
@click.version_option(version="0.2.2")
def cli():
    """dbinit - Interactive database initialization tool."""
    pass


@cli.command()
@click.argument("project", type=str)
@click.option(
    "--db",
    type=click.Choice(["postgres", "sqlite"], case_sensitive=False),
    required=False,
    help="Database type: postgres or sqlite (defaults to configured preference)"
)
def create(project: str, db: str):
    """Create a new database project with interactive credential setup."""
    try:
        # Use configured default if --db not provided
        if db is None:
            db = get_config_value("default_db_type", "postgres")
            click.echo(f"Using default database type: {db}")
        
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
