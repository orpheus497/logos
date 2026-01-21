"""
##Script function and purpose: Configuration file management.

Manages persistent configuration files in ~/.logos/

##Action purpose: Provides YAML-based configuration file reading, writing, and
default generation for LOGOS identity and configuration persistence.
"""

import os
from pathlib import Path
from typing import Any

import yaml


##Function purpose: Load YAML configuration from file
def read_config(config_path: Path) -> dict[str, Any] | None:
    """
    Loads YAML configuration from file.

    Reads and parses YAML file, returning dictionary of config data. If file
    doesn't exist, returns None. Catches YAML parsing errors and returns None.

    Args:
        config_path: Path to YAML configuration file

    Returns:
        Dictionary of configuration data, or None if file doesn't exist or is invalid
    """
    ##Action purpose: Reads and parses YAML file, returning dictionary of config data
    ##Condition purpose: Check if config file exists
    if not config_path.exists():
        ##Action purpose: Return None if file doesn't exist
        return None

    try:
        ##Action purpose: Read and parse YAML file
        with config_path.open("r", encoding="utf-8") as f:
            ##Action purpose: Load YAML content as dictionary
            ##Fix: Return None for empty file instead of empty dict to preserve error distinction
            data = yaml.safe_load(f)
            return data if data is not None else None
    except (OSError, yaml.YAMLError):
        ##Error purpose: Handle YAML parsing or file I/O errors
        ##Action purpose: Return None on error (caller can handle)
        return None


##Function purpose: Write dictionary data to YAML configuration file
def write_config(config_path: Path, data: dict[str, Any]) -> bool:
    """
    Writes dictionary data to YAML configuration file.

    Serializes dictionary to YAML format and writes to file, creating parent
    directories if needed. Sets secure file permissions to prevent unauthorized
    access (0o600 for files, 0o700 for directories). Catches file I/O errors and
    returns False on failure.

    Args:
        config_path: Path to YAML configuration file
        data: Dictionary of configuration data to write

    Returns:
        True if write succeeded, False otherwise
    """
    ##Action purpose: Serializes dictionary to YAML format and writes to file,
    ##Step purpose: creating parent directories if needed, setting secure permissions
    try:
        ##Action purpose: Create parent directories if they don't exist
        config_path.parent.mkdir(parents=True, exist_ok=True)
        ##Action purpose: Set secure directory permissions (0o700 = rwx------)
        os.chmod(config_path.parent, 0o700)

        ##Action purpose: Write YAML data to file
        with config_path.open("w", encoding="utf-8") as f:
            ##Action purpose: Serialize dictionary to YAML format
            yaml.safe_dump(data, f, default_flow_style=False, sort_keys=False)

        ##Action purpose: Set secure file permissions (0o600 = rw-------)
        os.chmod(config_path, 0o600)

        ##Action purpose: Return success
        return True
    except (OSError, yaml.YAMLError):
        ##Error purpose: Handle file I/O or YAML serialization errors
        ##Action purpose: Return False on error
        return False


##Function purpose: Get default configuration directory path
def get_config_dir() -> Path:
    """
    Returns default configuration directory path.

    Returns ~/.logos/ directory path for storing configuration files.

    Returns:
        Path object pointing to ~/.logos/ directory
    """
    ##Action purpose: Return home directory + .logos subdirectory
    return Path.home() / ".logos"


##Function purpose: Get identity configuration file path
##Function purpose: Return path to identity configuration file
def get_identity_path() -> Path:
    """
    Returns path to identity configuration file.

    Returns ~/.logos/identity.yaml path for identity persistence.

    Returns:
        Path object pointing to identity.yaml file
    """
    ##Action purpose: Returns ~/.logos/identity.yaml path for identity persistence
    ##Action purpose: Return identity.yaml in config directory
    return get_config_dir() / "identity.yaml"
