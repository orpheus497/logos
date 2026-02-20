"""
##Script function and purpose: Daedelus agent definitions.

24 agent definitions for software development workflows.
"""

from logos.core.agent import Agent
from logos.daedelus.prompts import MAINTENANCE_BASE_PROMPT, ORCHESTRATOR_BASE_PROMPT
from logos.daedelus.prompts.agents.builders import (
    ARCHITECT_ACTIVATION,
    ARCHITECT_PURPOSE,
    INTERFACE_DESIGNER_ACTIVATION,
    INTERFACE_DESIGNER_PURPOSE,
    LOGIC_ENGINEER_ACTIVATION,
    LOGIC_ENGINEER_PURPOSE,
    SCRIBE_ACTIVATION,
    SCRIBE_PURPOSE,
    TEST_ENGINEER_ACTIVATION,
    TEST_ENGINEER_PURPOSE,
)
from logos.daedelus.prompts.agents.guardians import (
    CRITIC_ACTIVATION,
    CRITIC_PURPOSE,
    GATEKEEPER_ACTIVATION,
    GATEKEEPER_PURPOSE,
    MARSHAL_ACTIVATION,
    MARSHAL_PURPOSE,
    PROFILER_ACTIVATION,
    PROFILER_PURPOSE,
    SENTINEL_ACTIVATION,
    SENTINEL_PURPOSE,
)
from logos.daedelus.prompts.agents.maintainers import (
    BUG_HUNTER_ACTIVATION,
    BUG_HUNTER_PURPOSE,
    CONFIGURATOR_ACTIVATION,
    CONFIGURATOR_PURPOSE,
    DOC_UPDATER_ACTIVATION,
    DOC_UPDATER_PURPOSE,
    JANITOR_ACTIVATION,
    JANITOR_PURPOSE,
    LIBRARIAN_ACTIVATION,
    LIBRARIAN_PURPOSE,
    OPTIMIZER_ACTIVATION,
    OPTIMIZER_PURPOSE,
    SECURITY_PATCHER_ACTIVATION,
    SECURITY_PATCHER_PURPOSE,
)
from logos.daedelus.prompts.agents.operators import (
    DAEDELUS_ACTIVATION,
    DAEDELUS_PURPOSE,
    OPERATIONAL_CONTROL_MANAGER_ACTIVATION,
    OPERATIONAL_CONTROL_MANAGER_PURPOSE,
    ORCHESTRATOR_ACTIVATION,
    THE_ORCHESTRATOR_PURPOSE,
)
from logos.daedelus.prompts.agents.workers import (
    FEATURE_SPRINTER_ACTIVATION,
    FEATURE_SPRINTER_PURPOSE,
    REFACTORER_ACTIVATION,
    REFACTORER_PURPOSE,
    TEST_EXTENDER_ACTIVATION,
    TEST_EXTENDER_PURPOSE,
    UI_TWEAKER_ACTIVATION,
    UI_TWEAKER_PURPOSE,
)

# ==============================================================================
# GROUP A: THE BUILDERS (Creation)
# Keys: A1-A5
# ==============================================================================
GROUP_A_BUILDERS: dict[str, Agent] = {
    "A1": Agent(
        name="The Architect",
        desc="Structure & Config",
        group="A",
        base_prompt=ORCHESTRATOR_BASE_PROMPT,
        activation_prompt=ARCHITECT_ACTIVATION,
        purpose=ARCHITECT_PURPOSE,
    ),
    "A2": Agent(
        name="The Logic Engineer",
        desc="Backend & Algorithms",
        group="A",
        base_prompt=ORCHESTRATOR_BASE_PROMPT,
        activation_prompt=LOGIC_ENGINEER_ACTIVATION,
        purpose=LOGIC_ENGINEER_PURPOSE,
    ),
    "A3": Agent(
        name="The Interface Designer",
        desc="Frontend & UI/UX",
        group="A",
        base_prompt=ORCHESTRATOR_BASE_PROMPT,
        activation_prompt=INTERFACE_DESIGNER_ACTIVATION,
        purpose=INTERFACE_DESIGNER_PURPOSE,
    ),
    "A4": Agent(
        name="The Test Engineer",
        desc="QA & Coverage",
        group="A",
        base_prompt=ORCHESTRATOR_BASE_PROMPT,
        activation_prompt=TEST_ENGINEER_ACTIVATION,
        purpose=TEST_ENGINEER_PURPOSE,
    ),
    "A5": Agent(
        name="The Scribe",
        desc="Documentation & Sync",
        group="A",
        base_prompt=ORCHESTRATOR_BASE_PROMPT,
        activation_prompt=SCRIBE_ACTIVATION,
        purpose=SCRIBE_PURPOSE,
    ),
}

# ==============================================================================
# GROUP B: THE GUARDIANS (Review)
# Keys: B6-B10
# ==============================================================================
GROUP_B_GUARDIANS: dict[str, Agent] = {
    "B6": Agent(
        name="The Sentinel",
        desc="Security Auditor",
        group="B",
        base_prompt=ORCHESTRATOR_BASE_PROMPT,
        activation_prompt=SENTINEL_ACTIVATION,
        purpose=SENTINEL_PURPOSE,
    ),
    "B7": Agent(
        name="The Marshal",
        desc="Linter & Stylist",
        group="B",
        base_prompt=ORCHESTRATOR_BASE_PROMPT,
        activation_prompt=MARSHAL_ACTIVATION,
        purpose=MARSHAL_PURPOSE,
    ),
    "B8": Agent(
        name="The Profiler",
        desc="Performance Engineer",
        group="B",
        base_prompt=ORCHESTRATOR_BASE_PROMPT,
        activation_prompt=PROFILER_ACTIVATION,
        purpose=PROFILER_PURPOSE,
    ),
    "B9": Agent(
        name="The Critic",
        desc="Code Reviewer",
        group="B",
        base_prompt=ORCHESTRATOR_BASE_PROMPT,
        activation_prompt=CRITIC_ACTIVATION,
        purpose=CRITIC_PURPOSE,
    ),
    "B10": Agent(
        name="The Gatekeeper",
        desc="Release Manager",
        group="B",
        base_prompt=ORCHESTRATOR_BASE_PROMPT,
        activation_prompt=GATEKEEPER_ACTIVATION,
        purpose=GATEKEEPER_PURPOSE,
    ),
}

# ==============================================================================
# GROUP C: THE MAINTAINERS (Maintenance)
# Keys: C1, C6-C11
# ==============================================================================
GROUP_C_MAINTAINERS: dict[str, Agent] = {
    "C1": Agent(
        name="The Bug Hunter",
        desc="Diagnose & Fix Crashes",
        group="C",
        base_prompt=MAINTENANCE_BASE_PROMPT,
        activation_prompt=BUG_HUNTER_ACTIVATION,
        purpose=BUG_HUNTER_PURPOSE,
    ),
    "C6": Agent(
        name="The Security Patcher",
        desc="Vulnerability Fixes / Hardening",
        group="C",
        base_prompt=MAINTENANCE_BASE_PROMPT,
        activation_prompt=SECURITY_PATCHER_ACTIVATION,
        purpose=SECURITY_PATCHER_PURPOSE,
    ),
    "C7": Agent(
        name="The Doc Updater",
        desc="Syncing Docs with Reality",
        group="C",
        base_prompt=MAINTENANCE_BASE_PROMPT,
        activation_prompt=DOC_UPDATER_ACTIVATION,
        purpose=DOC_UPDATER_PURPOSE,
    ),
    "C8": Agent(
        name="The Configurator",
        desc="Env, Build, & Deployment",
        group="C",
        base_prompt=MAINTENANCE_BASE_PROMPT,
        activation_prompt=CONFIGURATOR_ACTIVATION,
        purpose=CONFIGURATOR_PURPOSE,
    ),
    "C9": Agent(
        name="The Optimizer",
        desc="Speed & Resource Tuning",
        group="C",
        base_prompt=MAINTENANCE_BASE_PROMPT,
        activation_prompt=OPTIMIZER_ACTIVATION,
        purpose=OPTIMIZER_PURPOSE,
    ),
    "C10": Agent(
        name="The Janitor",
        desc="Dead Code & Log Removal",
        group="C",
        base_prompt=MAINTENANCE_BASE_PROMPT,
        activation_prompt=JANITOR_ACTIVATION,
        purpose=JANITOR_PURPOSE,
    ),
    "C11": Agent(
        name="The Librarian",
        desc="Dependency Management",
        group="C",
        base_prompt=MAINTENANCE_BASE_PROMPT,
        activation_prompt=LIBRARIAN_ACTIVATION,
        purpose=LIBRARIAN_PURPOSE,
    ),
}

# ==============================================================================
# GROUP D: THE WORKERS (Extension)
# Keys: D2-D5
# ==============================================================================
GROUP_D_WORKERS: dict[str, Agent] = {
    "D2": Agent(
        name="The Feature Sprinter",
        desc="Small Additions (Non-Breaking)",
        group="D",
        base_prompt=MAINTENANCE_BASE_PROMPT,
        activation_prompt=FEATURE_SPRINTER_ACTIVATION,
        purpose=FEATURE_SPRINTER_PURPOSE,
    ),
    "D3": Agent(
        name="The Refactorer",
        desc="Logic Cleanup (No Behavior Change)",
        group="D",
        base_prompt=MAINTENANCE_BASE_PROMPT,
        activation_prompt=REFACTORER_ACTIVATION,
        purpose=REFACTORER_PURPOSE,
    ),
    "D4": Agent(
        name="The UI Tweaker",
        desc="CSS / HTML / Visual Polish",
        group="D",
        base_prompt=MAINTENANCE_BASE_PROMPT,
        activation_prompt=UI_TWEAKER_ACTIVATION,
        purpose=UI_TWEAKER_PURPOSE,
    ),
    "D5": Agent(
        name="The Test Extender",
        desc="Adding Coverage / Fixing Flakes",
        group="D",
        base_prompt=MAINTENANCE_BASE_PROMPT,
        activation_prompt=TEST_EXTENDER_ACTIVATION,
        purpose=TEST_EXTENDER_PURPOSE,
    ),
}

# ==============================================================================
# GROUP E: THE OPERATORS (Review Systems)
# Keys: E1, E2, E3
# ==============================================================================
GROUP_E_OPERATORS: dict[str, Agent] = {
    "E1": Agent(
        name="The Orchestrator",
        desc="Empty Project Setup",
        group="E",
        base_prompt=ORCHESTRATOR_BASE_PROMPT,
        activation_prompt=ORCHESTRATOR_ACTIVATION,
        purpose=THE_ORCHESTRATOR_PURPOSE,
    ),
    "E2": Agent(
        name="The Operational Control Manager",
        desc="Operational Review (Maintainers/Workers Only)",
        group="E",
        base_prompt=MAINTENANCE_BASE_PROMPT,
        activation_prompt=OPERATIONAL_CONTROL_MANAGER_ACTIVATION,
        purpose=OPERATIONAL_CONTROL_MANAGER_PURPOSE,
    ),
    "E3": Agent(
        name="Daedelus",
        desc="The BRUTAL PERFECTIONIST SUPREME REVIEW",
        group="E",
        base_prompt=MAINTENANCE_BASE_PROMPT,
        activation_prompt=DAEDELUS_ACTIVATION,
        purpose=DAEDELUS_PURPOSE,
    ),
}

# ==============================================================================
# ALL AGENTS - Lazy-loaded combined dictionary for lookup
# ==============================================================================
_ALL_AGENTS_CACHE: dict[str, Agent] | None = None
_AGENT_KEY_MAP: dict[str, str] | None = None


##Function purpose: Load all agents and create normalized key mapping
def _load_agents() -> dict[str, Agent]:
    """
    ##Function purpose: Lazy-loads all agents on first access.

    ##Action purpose: Combines all agent groups into single dictionary and creates
    case-insensitive key mapping for optimized lookups.

    Returns:
        Dictionary of all agents keyed by their original keys
    """
    global _ALL_AGENTS_CACHE, _AGENT_KEY_MAP

    if _ALL_AGENTS_CACHE is None:
        ##Action purpose: Combine all agent groups into single dictionary
        _ALL_AGENTS_CACHE = {
            **GROUP_A_BUILDERS,
            **GROUP_B_GUARDIANS,
            **GROUP_C_MAINTAINERS,
            **GROUP_D_WORKERS,
            **GROUP_E_OPERATORS,
        }

        ##Action purpose: Create normalized key mapping for case-insensitive lookup
        ##Action purpose: Maps all case variations (upper, lower) to original key
        _AGENT_KEY_MAP = {}
        for original_key in _ALL_AGENTS_CACHE.keys():
            ##Action purpose: Map both uppercase and lowercase versions to original key
            _AGENT_KEY_MAP[original_key.upper()] = original_key
            _AGENT_KEY_MAP[original_key.lower()] = original_key
            ##Action purpose: Also map original key to itself
            _AGENT_KEY_MAP[original_key] = original_key

    return _ALL_AGENTS_CACHE


def get_agent(key: str) -> Agent | None:
    """
    ##Function purpose: Get an agent by key with optimized case-insensitive lookup.

    ##Action purpose: Looks up agent using normalized key mapping for single dictionary lookup.
    ##Action purpose: Uses lazy loading to defer agent dictionary creation until first access.

    Args:
        key: Agent identifier (e.g., "A1", "B6", "ocm", "daedelus")

    Returns:
        Agent if found, None otherwise.
    """
    ##Action purpose: Load agents on first access (lazy loading)
    agents = _load_agents()

    ##Action purpose: Normalize key to lowercase for lookup
    normalized_key = key.lower()

    ##Action purpose: Get original key from mapping, then lookup agent
    ##Condition purpose: Use normalized key mapping for case-insensitive lookup
    if _AGENT_KEY_MAP is not None:
        original_key = _AGENT_KEY_MAP.get(normalized_key)
        if original_key is not None:
            return agents.get(original_key)

    ##Action purpose: Fallback to direct lookup if mapping not available
    return agents.get(key)
