"""
##Script function and purpose: Agent alias system.

Provides built-in and user-defined aliases for agent keys.
Phase 5 implementation.

##Action purpose: Enables users to refer to agents by memorable names
(e.g., "architect" instead of "A1") for faster agent selection.
Built-in aliases cover all 50 agents across both Daedelus and DEUS domains.
"""

import logging
from typing import Any

##Action purpose: Initialize logger for alias operations
logger = logging.getLogger(__name__)


##Action purpose: Built-in Daedelus agent aliases (24 agents)
##Note: Keys are lowercase, values are uppercase agent keys
DAEDELUS_ALIASES: dict[str, str] = {
    # Group A - The Builders
    "architect": "A1",
    "logic": "A2",
    "interface": "A3",
    "test-engineer": "A4",
    "scribe": "A5",
    # Group B - The Guardians
    "sentinel": "B6",
    "security": "B6",
    "marshal": "B7",
    "profiler": "B8",
    "critic": "B9",
    "gatekeeper": "B10",
    # Group C - The Maintainers
    "bughunter": "C1",
    "bugfix": "C1",
    "secpatch": "C6",
    "docupdate": "C7",
    "configurator": "C8",
    "optimizer": "C9",
    "janitor": "C10",
    "librarian": "C11",
    # Group D - The Workers
    "sprinter": "D2",
    "feature": "D2",
    "refactor": "D3",
    "uitweak": "D4",
    "testextend": "D5",
    # Group E - The Operators
    "orchestrator": "E1",
    "ocm": "E2",
    "daedelus": "E3",
}

##Action purpose: Built-in DEUS agent aliases (26 agents)
DEUS_ALIASES: dict[str, str] = {
    # Group A - The Engineers
    "kernel": "A1",
    "driver": "A2",
    "network": "A3",
    "boot": "A4",
    "service": "A5",
    # Group B - The Auditors
    "secaudit": "B6",
    "audit": "B6",
    "syntax": "B7",
    "perf": "B8",
    "compliance": "B9",
    "release": "B10",
    # Group C - The Maintainers
    "bughunter": "C1",
    "bugfix": "C1",
    "secpatch": "C6",
    "manual": "C7",
    "sysctl": "C8",
    "optimizer": "C9",
    "janitor": "C10",
    "portlib": "C11",
    # Group D - The Specialists
    "portbuild": "D2",
    "compat": "D3",
    "jail": "D4",
    "zfs": "D5",
    # Group E - The Operators
    "orchestrator": "E1",
    "admin": "E2",
    "manager": "E3",
    "ombudsman": "E4",
    "deus": "E5",
}


##Function purpose: Resolve an alias to an agent key
def resolve_alias(alias: str, mode: str, custom_aliases: dict[str, str] | None = None) -> str | None:
    """
    Resolves an alias to an agent key for the given mode.

    Checks custom aliases first (user-defined), then built-in aliases
    for the specified mode. Returns None if alias is not recognized.

    Args:
        alias: Alias string to resolve (case-insensitive)
        mode: Current mode ("daedelus" or "deus")
        custom_aliases: Optional user-defined aliases from config

    Returns:
        Agent key string (e.g., "A1"), or None if alias not found
    """
    ##Action purpose: Normalize alias to lowercase
    normalized = alias.lower().strip()

    ##Step purpose: Check custom aliases first (user overrides)
    if custom_aliases and normalized in custom_aliases:
        resolved = custom_aliases[normalized].upper()
        logger.debug(f"Resolved custom alias '{alias}' -> '{resolved}'")
        return resolved

    ##Step purpose: Check built-in aliases for mode
    builtin_aliases = _get_builtin_aliases(mode)
    if normalized in builtin_aliases:
        resolved = builtin_aliases[normalized]
        logger.debug(f"Resolved built-in alias '{alias}' -> '{resolved}'")
        return resolved

    ##Action purpose: Return None if alias not recognized
    return None


##Function purpose: Get built-in aliases for specified mode
def _get_builtin_aliases(mode: str) -> dict[str, str]:
    """
    Returns built-in aliases for the specified mode.

    Args:
        mode: Mode string ("daedelus" or "deus")

    Returns:
        Dictionary of alias -> agent key mappings
    """
    ##Condition purpose: Return appropriate alias dict based on mode
    if mode == "daedelus":
        return DAEDELUS_ALIASES
    elif mode == "deus":
        return DEUS_ALIASES
    ##Action purpose: Return empty dict for unknown mode
    return {}


##Function purpose: Get all available aliases for display
def get_all_aliases(mode: str, custom_aliases: dict[str, str] | None = None) -> dict[str, str]:
    """
    Returns all available aliases (built-in + custom) for the given mode.

    Custom aliases take precedence over built-in ones.

    Args:
        mode: Current mode ("daedelus" or "deus")
        custom_aliases: Optional user-defined aliases from config

    Returns:
        Merged dictionary of alias -> agent key mappings
    """
    ##Action purpose: Start with built-in aliases
    aliases = dict(_get_builtin_aliases(mode))

    ##Condition purpose: Merge custom aliases if provided
    if custom_aliases:
        for alias_key, agent_key in custom_aliases.items():
            ##Action purpose: Normalize and add custom alias (overrides built-in)
            aliases[alias_key.lower().strip()] = agent_key.upper()

    return aliases


##Function purpose: Validate custom aliases from config
def validate_custom_aliases(aliases: Any) -> dict[str, str]:
    """
    Validates and normalizes custom aliases from configuration.

    Ensures aliases dict contains only string keys and string values.
    Invalid entries are logged and skipped.

    Args:
        aliases: Raw aliases value from config (expected dict[str, str])

    Returns:
        Validated dictionary of alias -> agent key mappings
    """
    ##Condition purpose: Return empty dict if not a dict
    if not isinstance(aliases, dict):
        logger.warning("Custom aliases config is not a dictionary, ignoring")
        return {}

    validated: dict[str, str] = {}
    for key, value in aliases.items():
        ##Condition purpose: Skip non-string entries
        if not isinstance(key, str) or not isinstance(value, str):
            logger.warning(f"Skipping invalid alias entry: {key!r} -> {value!r}")
            continue
        ##Action purpose: Normalize and store valid alias
        validated[key.lower().strip()] = value.upper().strip()

    return validated
