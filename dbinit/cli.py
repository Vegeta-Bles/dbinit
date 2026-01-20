"""CLI entry point for dbinit tool."""

import sys
import click
from pathlib import Path
from .commands import create_project, show_credentials


@click.group()
@click.version_option(version="0.1.1")
def cli():
    """dbinit - Interactive database initialization tool."""
    pass


@cli.command()
@click.argument("project", type=str)
@click.option(
    "--db",
    type=click.Choice(["postgres", "sqlite"], case_sensitive=False),
    required=True,
    help="Database type: postgres or sqlite"
)
def create(project: str, db: str):
    """Create a new database project with interactive credential setup."""
    try:
        create_project(project, db.lower())
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


if __name__ == "__main__":
    cli()
