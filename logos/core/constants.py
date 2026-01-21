"""
##Script function and purpose: Shared constants module.

Single source of truth for magic strings, color codes, and agent groups.
Supports both Daedelus and DEUS domain agent group naming conventions.

##Action purpose: Addresses P1-002 (magic strings everywhere) by centralizing
color codes, agent groups, and other constants.
"""

from typing import Final


class Colors:
    """
    ##Class purpose: ANSI color codes for terminal output.

    Provides consistent color codes used across both Daedelus and DEUS domains.
    """

    RED: Final[str] = "\033[91m"
    GREEN: Final[str] = "\033[92m"
    YELLOW: Final[str] = "\033[93m"
    BLUE: Final[str] = "\033[94m"
    MAGENTA: Final[str] = "\033[95m"
    CYAN: Final[str] = "\033[96m"
    WHITE: Final[str] = "\033[97m"
    RESET: Final[str] = "\033[0m"
    BOLD: Final[str] = "\033[1m"


class AgentGroups:
    """
    ##Class purpose: Agent group identifiers with unique prefixes.

    Supports both Daedelus and DEUS naming conventions:
    - Daedelus: BUILDERS, GUARDIANS, MAINTAINERS, WORKERS, OPERATORS
    - DEUS: ENGINEERS, AUDITORS, MAINTAINERS, SPECIALISTS, OPERATORS

    Both use the same group letter prefixes (A, B, C, D, E).
    """

    # Daedelus domain groups
    BUILDERS: Final[str] = "A"  # Group A: Creation agents (Daedelus)
    GUARDIANS: Final[str] = "B"  # Group B: Review agents (Daedelus)
    MAINTAINERS: Final[str] = "C"  # Group C: Maintenance agents (both)
    WORKERS: Final[str] = "D"  # Group D: Extension agents (Daedelus)
    OPERATORS: Final[str] = "E"  # Group E: Orchestration agents (both)

    # DEUS domain groups (aliases for same letters)
    ENGINEERS: Final[str] = "A"  # Group A: System Building (DEUS)
    AUDITORS: Final[str] = "B"  # Group B: System Verification (DEUS)
    SPECIALISTS: Final[str] = "D"  # Group D: System Extension (DEUS)

    # Common groups (same in both domains)
    # MAINTAINERS = "C" (already defined above)
    # OPERATORS = "E" (already defined above)


##Action purpose: Menu display configuration - default separator width
##Condition purpose: Use different widths for different domains if needed
##Note: Daedelus uses 60, DEUS uses 70. Default is 60 (Daedelus value).
##Domains can override this constant if needed for their specific UI requirements.
SEPARATOR_WIDTH: Final[int] = 60  # Default (Daedelus), DEUS uses 70


class UILayout:
    """
    ##Class purpose: UI layout constants for consistent terminal interface dimensions.

    Centralizes all hardcoded layout values to improve maintainability and allow
    easy configuration changes.
    """

    ##Action purpose: Faction logo display dimensions
    LOGO_WIDTH: Final[int] = 20  # Width of each faction logo (standardized, increased for better visibility)
    LOGO_SPACING: Final[int] = 3  # Space between logos in display
    LOGO_HEIGHT: Final[int] = 6  # Standardized logo height (all logos are 6 lines tall)

    ##Action purpose: Standard display width for CLI screens
    DISPLAY_WIDTH: Final[int] = 100  # Standard width for CLI display screens (increased to prevent prompt cutoff)
    PROMPT_PADDING: Final[int] = 4  # Padding for prompt text wrapping (width - PROMPT_PADDING)
