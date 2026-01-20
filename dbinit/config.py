"""Configuration management for dbinit."""

import json
import os
from pathlib import Path
from typing import Dict, Optional


def get_config_dir() -> Path:
    """Get the configuration directory for dbinit.
    
    Returns:
        Path to the configuration directory
    """
    config_dir = Path.home() / ".dbinit"
    config_dir.mkdir(exist_ok=True)
    return config_dir


def get_config_file() -> Path:
    """Get the path to the configuration file.
    
    Returns:
        Path to config.json
    """
    return get_config_dir() / "config.json"


def load_config() -> Dict:
    """Load configuration from file.
    
    Returns:
        Dictionary containing configuration settings
    """
    config_file = get_config_file()
    if config_file.exists():
        try:
            with open(config_file, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def save_config(config: Dict):
    """Save configuration to file.
    
    Args:
        config: Dictionary containing configuration settings
    """
    config_file = get_config_file()
    with open(config_file, "w") as f:
        json.dump(config, f, indent=2)


def get_config_value(key: str, default: any = None) -> any:
    """Get a configuration value.
    
    Args:
        key: Configuration key
        default: Default value if key doesn't exist
        
    Returns:
        Configuration value or default
    """
    config = load_config()
    return config.get(key, default)


def set_config_value(key: str, value: any):
    """Set a configuration value.
    
    Args:
        key: Configuration key
        value: Value to set
    """
    config = load_config()
    config[key] = value
    save_config(config)


def get_default_project_path() -> Path:
    """Get the default path for creating projects.
    
    Returns:
        Path object for default project directory
    """
    default_path = get_config_value("default_project_path")
    if default_path:
        return Path(default_path).expanduser()
    
    # Default to ~/projects or current directory
    projects_dir = Path.home() / "projects"
    if projects_dir.exists():
        return projects_dir
    return Path.cwd()
