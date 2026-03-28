"""
##Script function and purpose: Version information module.

Provides version string for LOGOS CLI and programmatic access.
Phase 5 implementation.

##Action purpose: Single source of truth for the LOGOS version string,
used by CLI --version flag and other components that need version info.
"""

from typing import Final

##Action purpose: Version string matches pyproject.toml
VERSION: Final[str] = "0.2.0.dev0"


##Function purpose: Get the current LOGOS version string
def get_version() -> str:
    """
    Returns the current LOGOS version string.

    Returns:
        Version string (e.g., "0.2.0.dev0")
    """
    return VERSION
