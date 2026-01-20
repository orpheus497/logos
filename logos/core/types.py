"""
##Script function and purpose: Architectural type definitions.

Provides type-safe enums and dataclasses for mode values, agent groups, and UI contexts.
Phase 3 architectural improvements.

##Action purpose: Replaces primitive strings and tuples with type-safe structures
to improve maintainability and reduce errors.
"""

from dataclasses import dataclass
from enum import Enum

from logos.core.agent import Agent


class Mode(str, Enum):
    """
    ##Class purpose: Type-safe mode enumeration.

    Replaces string literals ("daedelus", "deus") with type-safe enum values
    to prevent typos and improve IDE support.
    """

    DAEDELUS = "daedelus"
    DEUS = "deus"

    def __str__(self) -> str:
        """
        ##Method purpose: Return string value for backward compatibility.

        ##Action purpose: Returns the enum value as a string to maintain
        compatibility with code expecting string mode values.
        """
        return self.value


@dataclass
class AgentGroup:
    """
    ##Class purpose: Agent group data structure.

    Replaces tuple structure with named dataclass for better type safety
    and maintainability.
    """

    id: str  # Group identifier (A, B, C, D, E)
    name: str  # Display name (e.g., "THE BUILDERS")
    category: str  # Category description (e.g., "Creation")
    purpose: str  # Purpose description
    color: str  # ANSI color code from Colors class
    agents: dict[str, Agent]  # Dictionary of agents in this group


@dataclass
class WelcomeScreenContext:
    """
    ##Class purpose: Context data for welcome screen display.

    Replaces long parameter list with structured dataclass to improve
    function signature clarity and extensibility.
    """

    username: str | None = None
    hostname: str | None = None
    faction: str | None = None  # Display name
    faction_key: str | None = None  # Faction identifier
    os_info: str | None = None
    last_session: str | None = None
    faction_prompt_counts: dict[str, int] | None = None
