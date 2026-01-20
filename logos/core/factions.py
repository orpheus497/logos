"""
##Script function and purpose: Faction system definitions and modifiers.

Defines factions (Revanchist, Orphic, Technomancer) and applies behavioral modifiers.
Phase 3 implementation.

##Action purpose: Provides faction-based behavioral modification system that affects
both Daedelus and DEUS agent behaviors consistently based on user's philosophical choice.
"""

from dataclasses import dataclass
from typing import Any


##Class purpose: Faction definition with philosophy and behavioral modifiers
@dataclass
class Faction:
    """
    ##Class purpose: Represents a philosophical faction that modifies agent behavior.

    ##Action purpose: Encapsulates faction name, philosophy, autonomy level, and
    behavioral modifiers that affect how agents interact with users.

    Attributes:
        name: Human-readable faction name
        philosophy: Core philosophical statement of the faction
        autonomy_level: Level of AI autonomy ("minimal", "balanced", "maximum")
        modifiers: Dictionary of behavioral modifier key-value pairs
    """

    name: str
    philosophy: str
    autonomy_level: str  # "minimal", "balanced", "maximum"
    modifiers: dict[str, Any]


##Action purpose: Faction definitions dictionary - single source of truth for all factions
FACTIONS: dict[str, Faction] = {
    ##Action purpose: Daedelus default faction - neutral baseline
    "daedelus": Faction(name="Daedelus", philosophy="The craft is paramount", autonomy_level="balanced", modifiers={}),
    ##Action purpose: DEUS default faction - neutral baseline
    "deus": Faction(name="Deus", philosophy="User sovereignty is paramount", autonomy_level="balanced", modifiers={}),
    ##Action purpose: Revanchist faction - maximum human control, teaching focus
    "revanchist": Faction(
        name="The Revanchists",
        philosophy="Human cognition must remain primary",
        autonomy_level="minimal",
        modifiers={
            "approval_friction": "maximum",
            "explanation_required": True,
            "teaching_mode": True,
            "batch_operations": False,
        },
    ),
    ##Action purpose: Orphic faction - collaborative, educational, balanced
    "orphic": Faction(
        name="The Orphics",
        philosophy="Technology enhances human intelligence",
        autonomy_level="balanced",
        modifiers={
            "multiple_options": True,
            "educational_explanations": True,
            "socratic_mode_available": True,
            "capability_tracking": True,
        },
    ),
    ##Action purpose: Technomancer faction - maximum AI autonomy, proactive
    "technomancer": Faction(
        name="The Technomancers",
        philosophy="AI is transformative power",
        autonomy_level="maximum",
        modifiers={
            "proactive_suggestions": True,
            "batch_operations": True,
            "autonomous_low_risk": True,
            "minimal_friction": True,
        },
    ),
}


##Function purpose: Apply faction-specific modifiers to agent prompts
def apply_faction_modifiers(prompt: str, faction: Faction) -> str:
    """
    ##Function purpose: Appends faction protocol block to agent prompts.

    ##Action purpose: Injects faction-specific behavioral modifiers into prompts
    to ensure consistent behavior across Daedelus and DEUS domains based on user's
    philosophical choice.

    ##Condition purpose: If faction has no modifiers, return prompt unchanged.
    ##Action purpose: Otherwise, append formatted faction protocol block.

    Args:
        prompt: Base agent prompt string
        faction: Faction instance to apply modifiers from

    Returns:
        Prompt string with faction protocol block appended (if modifiers exist)
    """
    ##Condition purpose: Check if faction has behavioral modifiers
    if not faction.modifiers:
        ##Action purpose: Return prompt unchanged for factions without modifiers
        return prompt

    ##Action purpose: Build faction protocol header
    modifier_text = f"""
## FACTION PROTOCOL: {faction.name}

Philosophy: {faction.philosophy}
Autonomy Level: {faction.autonomy_level}

Behavioral Modifiers:
"""

    ##Loop purpose: Iterate through all modifier key-value pairs
    for key, value in faction.modifiers.items():
        ##Action purpose: Format each modifier as a bullet point
        modifier_text += f"- {key}: {value}\n"

    ##Action purpose: Append faction protocol to base prompt
    return prompt + modifier_text
