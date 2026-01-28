"""dbinit - Interactive database initialization tool."""

__version__ = "0.2.5"

# Import connection helpers for easy access
from .connect import connect, get_connection_info, get_sqlite_connection, get_postgres_connection_string

__all__ = [
    "__version__",
    "connect",
    "get_connection_info",
    "get_sqlite_connection",
    "get_postgres_connection_string",
]
