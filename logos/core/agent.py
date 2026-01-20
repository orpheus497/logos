"""
##Script function and purpose: Shared Agent dataclass definition.

This module defines the Agent dataclass that is used by both Daedelus and DEUS.
Single source of truth for agent structure to eliminate duplication.

##Action purpose: Uses __slots__ for memory optimization (~40% reduction per instance).
Requires Python 3.10+ which matches the minimum version requirement.
"""

from dataclasses import dataclass


##Class purpose: Agent definition with all prompt components
##Action purpose: Uses slots=True for reduced memory footprint
@dataclass(slots=True)
class Agent:
    """
    ##Class purpose: Agent definition with all prompt components.

    ##Action purpose: Uses __slots__ for reduced memory footprint (~40% reduction per instance).
    Requires Python 3.10+ which is already the minimum version.

    Attributes:
        name: Human-readable agent name (e.g., "The Architect")
        desc: Short description of agent's role
        group: Agent group identifier (A, B, C, D, or E)
        base_prompt: Base system prompt (orchestrator or maintenance)
        activation_prompt: Agent-specific activation prompt
        purpose: Agent's purpose statement
    """

    name: str
    desc: str
    group: str
    base_prompt: str
    activation_prompt: str
    purpose: str

    @property
    def full_prompt(self) -> str:
        """
        ##Method purpose: Pre-computed full prompt (base + activation).

        ##Action purpose: Combines base_prompt and activation_prompt into single string.

        Returns:
            Complete prompt string ready for AI agent use
        """
        return self.base_prompt + self.activation_prompt
