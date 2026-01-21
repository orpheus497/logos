"""
##Script function and purpose: Architectural type definitions.

Provides type-safe enums and dataclasses for mode values, agent groups, UI contexts,
and error handling patterns.
Phase 3 architectural improvements.

##Action purpose: Replaces primitive strings and tuples with type-safe structures
to improve maintainability and reduce errors.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Generic, TypeVar

from logos.core.agent import Agent

##Action purpose: Type variables for Result type generics
T = TypeVar("T")  # Success value type
E = TypeVar("E", bound=str)  # Error type (typically str)


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


##Class purpose: Success result container for Result type pattern
@dataclass(frozen=True)
class Ok(Generic[T]):
    """
    ##Class purpose: Success result container.

    Represents a successful operation result. Used in Result type pattern
    for explicit error handling with type safety.

    ##Action purpose: Provides type-safe container for successful operation results,
    replacing None returns and tuple-based success/failure patterns.
    """

    value: T  # The successful result value


##Class purpose: Error result container for Result type pattern
@dataclass(frozen=True)
class Err(Generic[E]):
    """
    ##Class purpose: Error result container.

    Represents a failed operation result. Used in Result type pattern
    for explicit error handling with type safety.

    ##Action purpose: Provides type-safe container for error results,
    preserving error messages and context in a structured way.
    """

    error: E  # The error message or error object


##Action purpose: Result type alias for explicit error handling
##Note: Result type pattern provides better error handling than None returns or tuples
##Usage: Result[T, E] where T is success type, E is error type (default: str)
##Fix: Use modern Python 3.10+ union syntax instead of Union type
Result = Ok[T] | Err[E]
