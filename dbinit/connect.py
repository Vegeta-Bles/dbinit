"""Easy database connection helpers for dbinit projects."""

import os
import sqlite3
from pathlib import Path
from typing import Optional, Dict, Any
try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False


def load_project_env(project_path: Optional[Path] = None) -> Dict[str, str]:
    """Load environment variables from .env file in project directory.
    
    Args:
        project_path: Path to project directory. If None, uses current directory.
        
    Returns:
        Dictionary of environment variables
    """
    if project_path is None:
        project_path = Path.cwd()
    
    env_file = project_path / ".env"
    env_vars = {}
    
    if env_file.exists():
        with open(env_file, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    env_vars[key.strip()] = value.strip()
    
    # Also try loading with python-dotenv if available
    if DOTENV_AVAILABLE:
        load_dotenv(env_file)
        # Merge with os.environ (dotenv takes precedence)
        for key in ["DB_TYPE", "DB_NAME", "DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT"]:
            if key in os.environ:
                env_vars[key] = os.environ[key]
    
    return env_vars


def get_connection_info(project_path: Optional[Path] = None) -> Dict[str, Any]:
    """Get database connection information from .env file.
    
    Args:
        project_path: Path to project directory. If None, uses current directory.
        
    Returns:
        Dictionary with connection info:
        - db_type: 'sqlite' or 'postgres'
        - db_path: Path to SQLite file (for SQLite)
        - db_name: Database name
        - db_user: Username
        - db_password: Password
        - db_host: Host (for PostgreSQL)
        - db_port: Port (for PostgreSQL)
    """
    env_vars = load_project_env(project_path)
    
    db_type = env_vars.get("DB_TYPE", "sqlite")
    db_name = env_vars.get("DB_NAME", "")
    db_user = env_vars.get("DB_USER", "")
    db_password = env_vars.get("DB_PASSWORD", "")
    
    result = {
        "db_type": db_type,
        "db_name": db_name,
        "db_user": db_user,
        "db_password": db_password,
    }
    
    if db_type == "sqlite":
        # For SQLite, resolve the database file path
        if project_path is None:
            project_path = Path.cwd()
        
        db_file = db_name if db_name else "database.db"
        db_path = project_path / db_file
        result["db_path"] = str(db_path.absolute())
    else:
        # For PostgreSQL
        result["db_host"] = env_vars.get("DB_HOST", "localhost")
        result["db_port"] = env_vars.get("DB_PORT", "5432")
    
    return result


def connect(project_path: Optional[Path] = None):
    """Get database connection information.
    
    Returns a simple object with connection attributes for easy access.
    
    Args:
        project_path: Path to project directory. If None, uses current directory.
        
    Returns:
        ConnectionInfo object with attributes:
        - db_path (SQLite only)
        - db_username
        - db_password
        - db_name
        - db_type
        - db_host (PostgreSQL only)
        - db_port (PostgreSQL only)
        
    Example:
        >>> import dbinit
        >>> conn_info = dbinit.connect()
        >>> print(conn_info.db_path)
        >>> print(conn_info.db_username)
    """
    info = get_connection_info(project_path)
    
    class ConnectionInfo:
        """Simple connection info object with easy-to-understand attributes."""
        def __init__(self, info_dict: Dict[str, Any]):
            self.db_type = info_dict.get("db_type", "sqlite")  # Database type: 'sqlite' or 'postgres'
            self.db_name = info_dict.get("db_name", "")  # Database name (e.g., 'test.db' for SQLite, 'mydb' for PostgreSQL)
            self.db_username = info_dict.get("db_user", "")  # Database username (from .env file)
            self.db_password = info_dict.get("db_password", "")  # Database password (from .env file)
            
            if self.db_type == "sqlite":
                self.db_path = info_dict.get("db_path", "")  # Full path to SQLite database file (e.g., '/path/to/test.db')
            else:
                self.db_host = info_dict.get("db_host", "localhost")  # PostgreSQL host (usually 'localhost')
                self.db_port = info_dict.get("db_port", "5432")  # PostgreSQL port (usually 5432)
        
        def __repr__(self):
            if self.db_type == "sqlite":
                return f"ConnectionInfo(db_type='sqlite', db_path='{self.db_path}', db_username='{self.db_username}')"
            else:
                return f"ConnectionInfo(db_type='postgres', db_host='{self.db_host}', db_name='{self.db_name}', db_username='{self.db_username}')"
    
    return ConnectionInfo(info)


def get_sqlite_connection(project_path: Optional[Path] = None) -> sqlite3.Connection:
    """Get a SQLite connection object.
    
    Args:
        project_path: Path to project directory. If None, uses current directory.
        
    Returns:
        sqlite3.Connection object
        
    Raises:
        ValueError: If project is not SQLite type
    """
    info = get_connection_info(project_path)
    
    if info["db_type"] != "sqlite":
        raise ValueError(f"Project is not SQLite type (found: {info['db_type']})")
    
    db_path = info.get("db_path", "")
    if not db_path:
        raise ValueError("Could not determine SQLite database path")
    
    return sqlite3.connect(db_path)


def get_postgres_connection_string(project_path: Optional[Path] = None) -> str:
    """Get PostgreSQL connection string.
    
    Args:
        project_path: Path to project directory. If None, uses current directory.
        
    Returns:
        PostgreSQL connection string
        
    Raises:
        ValueError: If project is not PostgreSQL type
    """
    info = get_connection_info(project_path)
    
    if info["db_type"] != "postgres":
        raise ValueError(f"Project is not PostgreSQL type (found: {info['db_type']})")
    
    user = info.get("db_user", "")
    password = info.get("db_password", "")
    host = info.get("db_host", "localhost")
    port = info.get("db_port", "5432")
    db_name = info.get("db_name", "")
    
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
