"""
##Script function and purpose: DEUS Domain - FreeBSD System Administration Agents

26-agent system for FreeBSD system administration workflows.
"""

##Fix: Removed undefined ALL_AGENTS import - this symbol is not defined in agents.py and not used anywhere
from logos.deus.agents import (
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
    "get_agent",
]
