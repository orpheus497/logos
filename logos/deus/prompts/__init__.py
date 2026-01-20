"""
##Script function and purpose: DEUS prompt system.

Base prompts and agent activation prompts for DEUS domain.
"""

from logos.deus.prompts.base_maintenance import MAINTENANCE_BASE_PROMPT
from logos.deus.prompts.base_system_orchestrator import SYSTEM_ORCHESTRATOR_BASE_PROMPT

__all__ = ["SYSTEM_ORCHESTRATOR_BASE_PROMPT", "MAINTENANCE_BASE_PROMPT"]
