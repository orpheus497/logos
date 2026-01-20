"""
##Script function and purpose: DEUS Domain - FreeBSD System Administration Agents

26-agent system for FreeBSD system administration workflows.
"""

from logos.deus.agents import (
    ALL_AGENTS,
    GROUP_A_ENGINEERS,
    GROUP_B_AUDITORS,
    GROUP_C_MAINTAINERS,
    GROUP_D_SPECIALISTS,
    GROUP_E_OPERATORS,
    get_agent,
)

__all__ = [
    "GROUP_A_ENGINEERS",
    "GROUP_B_AUDITORS",
    "GROUP_C_MAINTAINERS",
    "GROUP_D_SPECIALISTS",
    "GROUP_E_OPERATORS",
    "ALL_AGENTS",
    "get_agent",
]
