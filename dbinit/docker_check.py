"""Docker detection and installation instructions."""

import platform
import subprocess
import click


def check_docker_installed() -> bool:
    """Check if Docker is installed and available.
    
    Returns:
        True if Docker is installed, False otherwise
    """
    try:
        result = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def get_docker_install_command() -> str:
    """Get Docker installation command for the current platform.
    
    Returns:
        Installation command string
    """
    system = platform.system().lower()
    
    if system == "darwin":  # macOS
        return "brew install --cask docker"
    elif system == "linux":
        # Check for common package managers
        try:
            # Check for apt (Debian/Ubuntu)
            subprocess.run(["which", "apt-get"], capture_output=True, check=True)
            return "sudo apt-get update && sudo apt-get install -y docker.io docker-compose"
        except (FileNotFoundError, subprocess.CalledProcessError):
            try:
                # Check for yum (RHEL/CentOS)
                subprocess.run(["which", "yum"], capture_output=True, check=True)
                return "sudo yum install -y docker docker-compose"
            except (FileNotFoundError, subprocess.CalledProcessError):
                try:
                    # Check for dnf (Fedora)
                    subprocess.run(["which", "dnf"], capture_output=True, check=True)
                    return "sudo dnf install -y docker docker-compose"
                except (FileNotFoundError, subprocess.CalledProcessError):
                    return "Install Docker from https://docs.docker.com/get-docker/"
    elif system == "windows":
        return "Install Docker Desktop from https://www.docker.com/products/docker-desktop"
    else:
        return "Install Docker from https://docs.docker.com/get-docker/"


def warn_if_docker_not_installed():
    """Warn user if Docker is not installed.
    
    Shows a warning message with installation instructions.
    """
    if not check_docker_installed():
        install_cmd = get_docker_install_command()
        
        click.echo("\n" + "⚠️ " * 30)
        click.echo("  WARNING: Docker is not installed on your system", err=True)
        click.echo("⚠️ " * 30 + "\n", err=True)
        click.echo("PostgreSQL projects require Docker to run.", err=True)
        click.echo("Install Docker with:", err=True)
        click.echo(f"  {install_cmd}", err=True)
        click.echo("\nAlternatively, visit: https://docs.docker.com/get-docker/", err=True)
        click.echo("\nYou can still create the project, but you'll need Docker", err=True)
        click.echo("installed to start the database container.\n", err=True)
        
        return False
    return True
