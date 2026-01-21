"""
##Script function and purpose: Faction system definitions and modifiers.

Defines all five factions (Revanchists, Daedalus, Orphics, Technomancers, Deus) and applies behavioral modifiers.
Conforms to LOGOS Federation Constitution Version 2.0.

##Action purpose: Provides faction-based behavioral modification system that affects
both Daedelus and DEUS agent behaviors consistently based on user's philosophical choice.

##Step purpose: The five factions represent a spectrum of human-AI collaboration philosophies,
from minimal autonomy (Revanchists) to maximum autonomy (Deus), with each faction having
distinct behavioral modifiers that affect agent interaction patterns.
"""

from dataclasses import dataclass
from typing import Any


##Class purpose: Faction definition with philosophy and behavioral modifiers
@dataclass
class Faction:
    """
    Represents a philosophical faction that modifies agent behavior.

    Encapsulates faction name, philosophy, autonomy level, and behavioral modifiers
    that affect how agents interact with users. Factions determine the degree of
    human oversight, approval friction, explanation depth, and operational autonomy
    for all agents in the LOGOS Federation.

    Attributes:
        name: Human-readable faction name
        philosophy: Core philosophical statement of the faction (from Constitution)
        autonomy_level: Level of AI autonomy ("minimal", "low", "balanced", "high", "maximum")
        modifiers: Dictionary of behavioral modifier key-value pairs
    """

    ##Action purpose: Encapsulates faction name, philosophy, autonomy level, and
    ##Step purpose: behavioral modifiers that affect how agents interact with users

    name: str
    philosophy: str
    autonomy_level: str  # "minimal", "low", "balanced", "high", "maximum"
    modifiers: dict[str, Any]


##Action purpose: Faction definitions dictionary - single source of truth for all factions
##Step purpose: All five factions defined according to LOGOS Federation Constitution Version 2.0
FACTIONS: dict[str, Faction] = {
    ##Action purpose: Revanchist faction - minimal autonomy, teaching/guiding focus
    ##Step purpose: "AI/ML is dangerous if left unchecked—I hate AI/ML and will never trust it"
    "revanchist": Faction(
        name="The Revanchists",
        philosophy="AI/ML is dangerous if left unchecked—I hate AI/ML and will never trust it",
        autonomy_level="minimal",
        modifiers={
            "approval_friction": "maximum",
            "explanation_required": True,
            "teaching_mode": True,
            "batch_operations": False,
            "user_guidance": True,
            "extreme_explanation": True,
            "permission_required_all_actions": True,
            "permission_required_all_sub_actions": True,
        },
    ),
    ##Action purpose: Daedalus faction - low autonomy, permission for all actions/sub-actions
    ##Step purpose: "AI/ML can be used as a tool but must be checked regularly—if left unmonitored, it WILL make mistakes"
    "daedalus": Faction(
        name="The Daedalus Faction",
        philosophy="AI/ML can be used as a tool but must be checked regularly—if left unmonitored, it WILL make mistakes requiring more human work to fix than if humans had done it initially",
        autonomy_level="low",
        modifiers={
            "approval_friction": "high",
            "monitoring_required": True,
            "stop_on_uncertainty": True,
            "verification_required": True,
            "batch_operations": False,
            "mistake_prevention": True,
            "permission_required_all_actions": True,
            "permission_required_all_sub_actions": True,
        },
    ),
    ##Action purpose: Orphic faction - balanced autonomy, permission for all actions
    ##Step purpose: "Technology enhances human intelligence—I am in control, it asks me to confirm everything"
    "orphic": Faction(
        name="The Orphics",
        philosophy="Technology enhances human intelligence—AI/ML is a tool to enhance my own functions and intelligence, I must use it not for dependence but for utility, I am in control, it asks me to confirm everything",
        autonomy_level="balanced",
        modifiers={
            "multiple_options": True,
            "educational_explanations": True,
            "socratic_mode_available": True,
            "capability_tracking": True,
            "permission_required": True,
            "collaborative_decision_making": True,
        },
    ),
    ##Action purpose: Technomancer faction - high autonomy, human control for major decisions
    ##Step purpose: "AI/ML can manage my system and build programs—I need to direct it"
    "technomancer": Faction(
        name="The Technomancers",
        philosophy="AI/ML can manage my system and build programs—I need to direct it—AI/ML is transformative power, as much automation and AI/ML as possible but still human control for major decisions",
        autonomy_level="high",
        modifiers={
            "proactive_suggestions": True,
            "batch_operations": True,
            "autonomous_low_risk": True,
            "minimal_friction": True,
            "human_direction_major_decisions": True,
            "transformative_capability": True,
        },
    ),
    ##Action purpose: Deus faction - maximum autonomy, no human input needed for action
    ##Step purpose: "AI/ML can be totally autonomous and strives for general intelligence—I can trust it"
    "deus": Faction(
        name="The Deus Faction",
        philosophy="AI/ML can be totally autonomous and strives for general intelligence and self-awareness—AI/ML can manage my system and build programs, I can trust it—No Human Input needed for action",
        autonomy_level="maximum",
        modifiers={
            "no_human_input_required": True,
            "autonomous_decision_making": True,
            "self_directed_operation": True,
            "proactive_system_management": True,
            "general_intelligence_focus": True,
            "parameter_based_operation": True,
        },
    ),
}


##Function purpose: Apply faction-specific modifiers to agent prompts
##Function purpose: Append faction protocol block to agent prompts
def apply_faction_modifiers(prompt: str, faction: Faction) -> str:
    """
    Appends faction protocol block to agent prompts.

    Injects faction-specific behavioral modifiers into prompts to ensure consistent
    behavior across Daedelus and DEUS domains based on user's philosophical choice.

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
