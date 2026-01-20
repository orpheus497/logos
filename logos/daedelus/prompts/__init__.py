"""
##Script function and purpose: Daedelus prompt system.

Base prompts and agent activation prompts for Daedelus domain.
"""

from logos.daedelus.prompts.base_maintenance import MAINTENANCE_BASE_PROMPT
from logos.daedelus.prompts.base_orchestrator import ORCHESTRATOR_BASE_PROMPT

__all__ = ["ORCHESTRATOR_BASE_PROMPT", "MAINTENANCE_BASE_PROMPT"]
