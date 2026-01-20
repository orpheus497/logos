"""
##Script function and purpose: Daedelus Domain - Software Development Agents

22-agent system for AI-assisted software development workflows.
"""

##Fix: Removed undefined ALL_AGENTS import - this symbol is not defined in agents.py and not used anywhere
from logos.daedelus.agents import (
    GROUP_A_BUILDERS,
    GROUP_B_GUARDIANS,
    GROUP_C_MAINTAINERS,
    GROUP_D_WORKERS,
    GROUP_E_OPERATORS,
    get_agent,
)

__all__ = [
    "GROUP_A_BUILDERS",
    "GROUP_B_GUARDIANS",
    "GROUP_C_MAINTAINERS",
    "GROUP_D_WORKERS",
    "GROUP_E_OPERATORS",
    "get_agent",
]
