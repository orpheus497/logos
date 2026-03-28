"""
##Script function and purpose: User-level configuration file support.

Manages user preferences via ~/.logos/config.yaml configuration file.
Phase 5 implementation.

##Action purpose: Provides configuration loading, validation, and default generation
for user-customizable LOGOS settings including default mode, display preferences,
clipboard behavior, and agent aliases.
"""

from pathlib import Path
from typing import Any

from logos.core.persistence import get_config_dir, read_config, write_config

##Action purpose: Configuration file name constant
CONFIG_FILENAME = "config.yaml"

##Action purpose: Default configuration values
DEFAULT_CONFIG: dict[str, Any] = {
    "default_mode": None,  # None = ask each time; "daedelus" or "deus" (reserved for future use)
    "clipboard": {
        "enabled": True,  # Whether to auto-copy prompts to clipboard
        "show_preview": False,  # Whether to show prompt preview before copying
        "preview_lines": 10,  # Number of lines to show in preview (first + last)
    },
    "recent_agents": {
        "enabled": True,  # Track recent agent selections
        "max_count": 10,  # Maximum number of recent agents to track
    },
    "aliases": {},  # Custom user-defined aliases (e.g., {"arch": "A1"})
    "verbosity": "normal",  # "quiet", "normal", or "verbose"
}


##Function purpose: Get configuration file path
def get_config_path() -> Path:
    """
    Returns path to user configuration file.

    Returns ~/.logos/config.yaml path for user preferences.

    Returns:
        Path object pointing to config.yaml file
    """
    ##Action purpose: Return config.yaml in config directory
    return get_config_dir() / CONFIG_FILENAME


##Function purpose: Load user configuration with defaults
def load_config() -> dict[str, Any]:
    """
    Loads user configuration, merging with defaults.

    Reads ~/.logos/config.yaml if it exists and merges with default values.
    Missing keys are filled from defaults. Invalid or missing file returns
    full defaults.

    Returns:
        Dictionary of merged configuration values
    """
    ##Action purpose: Start with copy of defaults
    config = _deep_copy_dict(DEFAULT_CONFIG)

    ##Action purpose: Read user config file
    config_path = get_config_path()
    user_config = read_config(config_path)

    ##Condition purpose: Merge user config if loaded successfully
    if user_config is not None and isinstance(user_config, dict):
        ##Action purpose: Deep merge user config over defaults
        config = _deep_merge(config, user_config)

    return config


##Function purpose: Save configuration to file
def save_config(config: dict[str, Any]) -> bool:
    """
    Saves configuration to ~/.logos/config.yaml.

    Writes current configuration state to disk with secure permissions.

    Args:
        config: Dictionary of configuration values to save

    Returns:
        True if save succeeded, False otherwise
    """
    ##Action purpose: Write config to file
    config_path = get_config_path()
    return write_config(config_path, config)


##Function purpose: Get a specific configuration value by dotted path
def get_config_value(config: dict[str, Any], key_path: str, default: Any = None) -> Any:
    """
    Gets a configuration value by dotted key path.

    Supports nested key access using dot notation (e.g., "clipboard.enabled").

    Args:
        config: Configuration dictionary
        key_path: Dot-separated key path (e.g., "clipboard.show_preview")
        default: Default value if key not found

    Returns:
        Configuration value, or default if not found
    """
    ##Action purpose: Navigate nested config using dotted path
    keys = key_path.split(".")
    current = config

    for key in keys:
        ##Condition purpose: Check if key exists at current level
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            ##Action purpose: Return default if key path not found
            return default

    return current


##Function purpose: Deep merge two dictionaries
def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """
    Deep merges override dictionary into base dictionary.

    Recursively merges nested dictionaries. Non-dict values in override
    replace values in base.

    Args:
        base: Base dictionary (defaults)
        override: Override dictionary (user values)

    Returns:
        Merged dictionary
    """
    ##Action purpose: Create copy to avoid mutating base
    result = _deep_copy_dict(base)

    for key, value in override.items():
        ##Condition purpose: Recursively merge nested dicts
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        else:
            ##Action purpose: Override value directly
            result[key] = value

    return result


##Function purpose: Deep copy a dictionary (simple types only)
def _deep_copy_dict(d: dict[str, Any]) -> dict[str, Any]:
    """
    Creates a deep copy of a dictionary with simple types.

    Handles nested dicts and lists (including nested dicts/lists within lists).
    Suitable for YAML-compatible data (strings, ints, floats, bools, None,
    lists, dicts).

    Args:
        d: Dictionary to copy

    Returns:
        Deep copy of the dictionary
    """
    result: dict[str, Any] = {}
    for key, value in d.items():
        if isinstance(value, dict):
            result[key] = _deep_copy_dict(value)
        elif isinstance(value, list):
            result[key] = _deep_copy_list(value)
        else:
            result[key] = value
    return result


##Function purpose: Deep copy a list (simple types only)
def _deep_copy_list(lst: list[Any]) -> list[Any]:
    """
    Creates a deep copy of a list with simple types.

    Handles nested dicts and lists within list elements.

    Args:
        lst: List to copy

    Returns:
        Deep copy of the list
    """
    result: list[Any] = []
    for item in lst:
        if isinstance(item, dict):
            result.append(_deep_copy_dict(item))
        elif isinstance(item, list):
            result.append(_deep_copy_list(item))
        else:
            result.append(item)
    return result
