"""
##Script function and purpose: DEUS agent definitions.

26 agent definitions for FreeBSD system administration workflows.
"""

from logos.core.agent import Agent
from logos.deus.prompts import MAINTENANCE_BASE_PROMPT, SYSTEM_ORCHESTRATOR_BASE_PROMPT
from logos.deus.prompts.agents.auditors import (
    COMPLIANCE_CRITIC_ACTIVATION,
    COMPLIANCE_CRITIC_PURPOSE,
    PERFORMANCE_ANALYST_ACTIVATION,
    PERFORMANCE_ANALYST_PURPOSE,
    RELEASE_GATEKEEPER_ACTIVATION,
    RELEASE_GATEKEEPER_PURPOSE,
    SECURITY_AUDITOR_ACTIVATION,
    SECURITY_AUDITOR_PURPOSE,
    SYNTAX_MARSHAL_ACTIVATION,
    SYNTAX_MARSHAL_PURPOSE,
)
from logos.deus.prompts.agents.engineers import (
    BOOT_ENGINEER_ACTIVATION,
    BOOT_ENGINEER_PURPOSE,
    DRIVER_ENGINEER_ACTIVATION,
    DRIVER_ENGINEER_PURPOSE,
    KERNEL_ARCHITECT_ACTIVATION,
    KERNEL_ARCHITECT_PURPOSE,
    NETWORK_ARCHITECT_ACTIVATION,
    NETWORK_ARCHITECT_PURPOSE,
    SERVICE_SCRIBE_ACTIVATION,
    SERVICE_SCRIBE_PURPOSE,
)
from logos.deus.prompts.agents.maintainers import (
    BUG_HUNTER_ACTIVATION,
    BUG_HUNTER_PURPOSE,
    MANUAL_KEEPER_ACTIVATION,
    MANUAL_KEEPER_PURPOSE,
    OPTIMIZER_ACTIVATION,
    OPTIMIZER_PURPOSE,
    PORT_LIBRARIAN_ACTIVATION,
    PORT_LIBRARIAN_PURPOSE,
    SECURITY_PATCHER_ACTIVATION,
    SECURITY_PATCHER_PURPOSE,
    SYSCTL_TUNER_ACTIVATION,
    SYSCTL_TUNER_PURPOSE,
    SYSTEM_JANITOR_ACTIVATION,
    SYSTEM_JANITOR_PURPOSE,
)
from logos.deus.prompts.agents.operators import (
    ADMINISTRATOR_ACTIVATION,
    ADMINISTRATOR_PURPOSE,
    DEUS_ACTIVATION,
    DEUS_PURPOSE,
    GENERAL_MANAGER_ACTIVATION,
    GENERAL_MANAGER_PURPOSE,
    OMBUDSMAN_ACTIVATION,
    OMBUDSMAN_PURPOSE,
    SYSTEM_ORCHESTRATOR_ACTIVATION,
    SYSTEM_ORCHESTRATOR_PURPOSE,
)
from logos.deus.prompts.agents.specialists import (
    COMPATIBILITY_ENGINEER_ACTIVATION,
    COMPATIBILITY_ENGINEER_PURPOSE,
    JAIL_ARCHITECT_ACTIVATION,
    JAIL_ARCHITECT_PURPOSE,
    PORT_BUILDER_ACTIVATION,
    PORT_BUILDER_PURPOSE,
    ZFS_ENGINEER_ACTIVATION,
    ZFS_ENGINEER_PURPOSE,
)

# ==============================================================================
# GROUP A: THE ENGINEERS (System Building)
# Keys: A1-A5
# ==============================================================================
GROUP_A_ENGINEERS: dict[str, Agent] = {
    "A1": Agent(
        name="The Kernel Architect",
        desc="Kernel config, custom builds",
        group="A",
        base_prompt=SYSTEM_ORCHESTRATOR_BASE_PROMPT,
        activation_prompt=KERNEL_ARCHITECT_ACTIVATION,
        purpose=KERNEL_ARCHITECT_PURPOSE,
    ),
    "A2": Agent(
        name="The Driver Engineer",
        desc="Hardware, drivers, firmware",
        group="A",
        base_prompt=SYSTEM_ORCHESTRATOR_BASE_PROMPT,
        activation_prompt=DRIVER_ENGINEER_ACTIVATION,
        purpose=DRIVER_ENGINEER_PURPOSE,
    ),
    "A3": Agent(
        name="The Network Architect",
        desc="Network, VLANs, firewall",
        group="A",
        base_prompt=SYSTEM_ORCHESTRATOR_BASE_PROMPT,
        activation_prompt=NETWORK_ARCHITECT_ACTIVATION,
        purpose=NETWORK_ARCHITECT_PURPOSE,
    ),
    "A4": Agent(
        name="The Boot Engineer",
        desc="Boot loader, ZFS BE, recovery",
        group="A",
        base_prompt=SYSTEM_ORCHESTRATOR_BASE_PROMPT,
        activation_prompt=BOOT_ENGINEER_ACTIVATION,
        purpose=BOOT_ENGINEER_PURPOSE,
    ),
    "A5": Agent(
        name="The Service Scribe",
        desc="rc.conf, services, runbooks",
        group="A",
        base_prompt=SYSTEM_ORCHESTRATOR_BASE_PROMPT,
        activation_prompt=SERVICE_SCRIBE_ACTIVATION,
        purpose=SERVICE_SCRIBE_PURPOSE,
    ),
}

# ==============================================================================
# GROUP B: THE AUDITORS (System Verification)
# Keys: B6-B10
# ==============================================================================
GROUP_B_AUDITORS: dict[str, Agent] = {
    "B6": Agent(
        name="The Security Auditor",
        desc="Security review, vuln scan",
        group="B",
        base_prompt=SYSTEM_ORCHESTRATOR_BASE_PROMPT,
        activation_prompt=SECURITY_AUDITOR_ACTIVATION,
        purpose=SECURITY_AUDITOR_PURPOSE,
    ),
    "B7": Agent(
        name="The Syntax Marshal",
        desc="Syntax validation, standards",
        group="B",
        base_prompt=SYSTEM_ORCHESTRATOR_BASE_PROMPT,
        activation_prompt=SYNTAX_MARSHAL_ACTIVATION,
        purpose=SYNTAX_MARSHAL_PURPOSE,
    ),
    "B8": Agent(
        name="The Performance Analyst",
        desc="Benchmarking, profiling",
        group="B",
        base_prompt=SYSTEM_ORCHESTRATOR_BASE_PROMPT,
        activation_prompt=PERFORMANCE_ANALYST_ACTIVATION,
        purpose=PERFORMANCE_ANALYST_PURPOSE,
    ),
    "B9": Agent(
        name="The Compliance Critic",
        desc="BSD standards, best practices",
        group="B",
        base_prompt=SYSTEM_ORCHESTRATOR_BASE_PROMPT,
        activation_prompt=COMPLIANCE_CRITIC_ACTIVATION,
        purpose=COMPLIANCE_CRITIC_PURPOSE,
    ),
    "B10": Agent(
        name="The Release Gatekeeper",
        desc="Update approval, release",
        group="B",
        base_prompt=SYSTEM_ORCHESTRATOR_BASE_PROMPT,
        activation_prompt=RELEASE_GATEKEEPER_ACTIVATION,
        purpose=RELEASE_GATEKEEPER_PURPOSE,
    ),
}

# ==============================================================================
# GROUP C: THE MAINTAINERS (System Preservation)
# Keys: C1, C6-C11
# ==============================================================================
GROUP_C_MAINTAINERS: dict[str, Agent] = {
    "C1": Agent(
        name="The Bug Hunter",
        desc="Crash diagnosis, bug fixing",
        group="C",
        base_prompt=MAINTENANCE_BASE_PROMPT,
        activation_prompt=BUG_HUNTER_ACTIVATION,
        purpose=BUG_HUNTER_PURPOSE,
    ),
    "C6": Agent(
        name="The Security Patcher",
        desc="CVE patching, hardening",
        group="C",
        base_prompt=MAINTENANCE_BASE_PROMPT,
        activation_prompt=SECURITY_PATCHER_ACTIVATION,
        purpose=SECURITY_PATCHER_PURPOSE,
    ),
    "C7": Agent(
        name="The Manual Keeper",
        desc="Documentation maintenance",
        group="C",
        base_prompt=MAINTENANCE_BASE_PROMPT,
        activation_prompt=MANUAL_KEEPER_ACTIVATION,
        purpose=MANUAL_KEEPER_PURPOSE,
    ),
    "C8": Agent(
        name="The Sysctl Tuner",
        desc="Kernel tunables, sysctl",
        group="C",
        base_prompt=MAINTENANCE_BASE_PROMPT,
        activation_prompt=SYSCTL_TUNER_ACTIVATION,
        purpose=SYSCTL_TUNER_PURPOSE,
    ),
    "C9": Agent(
        name="The Optimizer",
        desc="Performance tuning",
        group="C",
        base_prompt=MAINTENANCE_BASE_PROMPT,
        activation_prompt=OPTIMIZER_ACTIVATION,
        purpose=OPTIMIZER_PURPOSE,
    ),
    "C10": Agent(
        name="The System Janitor",
        desc="Cleanup, space recovery",
        group="C",
        base_prompt=MAINTENANCE_BASE_PROMPT,
        activation_prompt=SYSTEM_JANITOR_ACTIVATION,
        purpose=SYSTEM_JANITOR_PURPOSE,
    ),
    "C11": Agent(
        name="The Port Librarian",
        desc="Package management",
        group="C",
        base_prompt=MAINTENANCE_BASE_PROMPT,
        activation_prompt=PORT_LIBRARIAN_ACTIVATION,
        purpose=PORT_LIBRARIAN_PURPOSE,
    ),
}

# ==============================================================================
# GROUP D: THE SPECIALISTS (System Extension)
# Keys: D2-D5
# ==============================================================================
GROUP_D_SPECIALISTS: dict[str, Agent] = {
    "D2": Agent(
        name="The Port Builder",
        desc="Custom port compilation",
        group="D",
        base_prompt=MAINTENANCE_BASE_PROMPT,
        activation_prompt=PORT_BUILDER_ACTIVATION,
        purpose=PORT_BUILDER_PURPOSE,
    ),
    "D3": Agent(
        name="The Compatibility Engineer",
        desc="Linux compat, Wine",
        group="D",
        base_prompt=MAINTENANCE_BASE_PROMPT,
        activation_prompt=COMPATIBILITY_ENGINEER_ACTIVATION,
        purpose=COMPATIBILITY_ENGINEER_PURPOSE,
    ),
    "D4": Agent(
        name="The Jail Architect",
        desc="Jails, vnet, isolation",
        group="D",
        base_prompt=MAINTENANCE_BASE_PROMPT,
        activation_prompt=JAIL_ARCHITECT_ACTIVATION,
        purpose=JAIL_ARCHITECT_PURPOSE,
    ),
    "D5": Agent(
        name="The ZFS Engineer",
        desc="ZFS pools, datasets",
        group="D",
        base_prompt=MAINTENANCE_BASE_PROMPT,
        activation_prompt=ZFS_ENGINEER_ACTIVATION,
        purpose=ZFS_ENGINEER_PURPOSE,
    ),
}

# ==============================================================================
# GROUP E: THE OPERATORS (System Governance)
# Keys: E1-E5
# ==============================================================================
GROUP_E_OPERATORS: dict[str, Agent] = {
    "E1": Agent(
        name="The System Orchestrator",
        desc="Base context, constitution, & .devdocs Governance",
        group="E",
        base_prompt=SYSTEM_ORCHESTRATOR_BASE_PROMPT,
        activation_prompt=SYSTEM_ORCHESTRATOR_ACTIVATION,
        purpose=SYSTEM_ORCHESTRATOR_PURPOSE,
    ),
    "E2": Agent(
        name="The Administrator",
        desc="Documentation curation",
        group="E",
        base_prompt=MAINTENANCE_BASE_PROMPT,
        activation_prompt=ADMINISTRATOR_ACTIVATION,
        purpose=ADMINISTRATOR_PURPOSE,
    ),
    "E3": Agent(
        name="The General Manager",
        desc="Monitoring, dispatch",
        group="E",
        base_prompt=MAINTENANCE_BASE_PROMPT,
        activation_prompt=GENERAL_MANAGER_ACTIVATION,
        purpose=GENERAL_MANAGER_PURPOSE,
    ),
    "E4": Agent(
        name="The Ombudsman",
        desc="Quality, orchestration",
        group="E",
        base_prompt=MAINTENANCE_BASE_PROMPT,
        activation_prompt=OMBUDSMAN_ACTIVATION,
        purpose=OMBUDSMAN_PURPOSE,
    ),
    "E5": Agent(
        name="DEUS",
        desc="Security, privacy, sovereignty",
        group="E",
        base_prompt=MAINTENANCE_BASE_PROMPT,
        activation_prompt=DEUS_ACTIVATION,
        purpose=DEUS_PURPOSE,
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
            **GROUP_A_ENGINEERS,
            **GROUP_B_AUDITORS,
            **GROUP_C_MAINTAINERS,
            **GROUP_D_SPECIALISTS,
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
        key: Agent identifier (e.g., "A1", "B6", "E5")

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
