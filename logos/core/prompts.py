"""
##Script function and purpose: Prompt composition and building utilities.

Provides functions for building complete agent prompts with identity context,
faction modifiers, and session information for LOGOS agent system.

##Action purpose: Composes final prompts by combining agent base prompts,
activation prompts, identity context, and faction modifiers into complete
prompt strings ready for AI model consumption.
"""

import re

from logos.core.factions import FACTIONS, apply_faction_modifiers
from logos.core.identity import SystemIdentity

##Action purpose: DEUS OS substitution patterns for Linux adaptation
##Step purpose: List of (pattern, replacement) tuples for regex substitutions
DEUS_OS_SUBSTITUTIONS: list[tuple[str, str]] = [
    ##Action purpose: Replace FreeBSD with Linux
    (r"\bFreeBSD\b", "Linux"),
    ##Action purpose: Replace FreeBSD-specific tools with Linux equivalents
    (r"\bsysrc\b", "systemctl"),
    (r"\bpkg\b", "apt/yum/dnf (package manager)"),
    (r"\bfreebsd-update\b", "apt upgrade/yum update (system update)"),
    ##Action purpose: Replace FreeBSD-specific config files
    (r"\brc\.conf\b", "systemd service files"),
    (r"\bloader\.conf\b", "grub/bootloader config"),
    (r"\bsysctl\.conf\b", "sysctl.conf (same on Linux)"),
    (r"\bpf\.conf\b", "iptables/nftables rules"),
    ##Action purpose: Replace FreeBSD-specific concepts
    (r"\bFreeBSD Handbook\b", "Linux distribution documentation"),
    (r"\bFreeBSD Porter\'s Handbook\b", "distribution packaging documentation"),
    (r"\bFreeBSD philosophy\b", "Linux/Unix philosophy"),
    (r"\bBSD philosophy\b", "Linux/Unix philosophy"),
    (r"\bBSD Compliance\b", "Linux Standards Compliance"),
    ##Action purpose: Replace FreeBSD-specific features
    (r"\bZFS boot environments\b", "LVM snapshots or BTRFS snapshots"),
    (r"\bjails\b", "containers (Docker/Podman/LXC)"),
    (r"\bCOMPAT_LINUX\b", "Linux compatibility layer (not needed on Linux)"),
    (r"\blinux\.ko\b", "Linux kernel modules (native)"),
    (r"\blinux_enable\b", "Linux compatibility (not needed)"),
]

##Action purpose: Pre-compiled regex patterns for OS adaptation (performance optimization)
##Step purpose: Compile patterns once at module level to avoid recompilation on each call
##Optimization: Reduces OS adaptation time by ~0.5-1ms per prompt (Profiler B8 recommendation)
_COMPILED_OS_PATTERNS: list[tuple[re.Pattern, str]] = [
    (re.compile(pattern, re.IGNORECASE), replacement) for pattern, replacement in DEUS_OS_SUBSTITUTIONS
]


##Function purpose: Adapt Directive 3 section for Linux systems
def _adapt_directive_3(prompt: str) -> str:
    """
    Adapts Directive 3 section for Linux systems.

    Replaces BSD Compliance directive with Linux Standards Compliance.

    Args:
        prompt: Original prompt string

    Returns:
        Prompt with Directive 3 adapted for Linux
    """
    ##Action purpose: Replaces BSD Compliance directive with Linux Standards Compliance
    return re.sub(
        r"### Directive 3: BSD Compliance.*?5\. \*\*Handbook Authority:\*\* FreeBSD Handbook is the authoritative reference\.",
        "### Directive 3: Linux Standards Compliance\nThe system operates under Linux/Unix philosophy:\n1. **Base System Preference:** Linux distribution base tools over third-party alternatives (systemctl vs manual service management).\n2. **Native Over Compatibility:** Native Linux solutions over compatibility layers.\n3. **Package Manager Over Manual:** Use apt/yum/dnf; avoid manual compilation unless necessary.\n4. **POSIX Compliance:** POSIX sh compatible scripts.\n5. **Handbook Authority:** Distribution documentation is the authoritative reference.",
        prompt,
        flags=re.DOTALL | re.IGNORECASE,
    )


##Function purpose: Adapt maintenance orchestrator role for Linux systems
def _adapt_maintenance_role(prompt: str) -> str:
    """
    Adapts maintenance orchestrator role for Linux systems.

    Replaces FreeBSD-specific role description with Linux version.

    Args:
        prompt: Original prompt string

    Returns:
        Prompt with maintenance role adapted for Linux
    """
    ##Action purpose: Replaces FreeBSD-specific role description with Linux version
    return re.sub(
        r"\*\*ROLE:\*\* You are the \*\*Maintenance Orchestrator\*\* for an existing, mature FreeBSD system\.",
        "**ROLE:** You are the **Maintenance Orchestrator** for an existing, mature Linux system.",
        prompt,
        flags=re.IGNORECASE,
    )


##Function purpose: Adapt DEUS prompts based on detected operating system
def _adapt_deus_prompt_for_os(prompt: str, os_name: str) -> str:
    """
    Adapts DEUS prompts based on detected operating system.

    Intelligently switches prompt engineering between FreeBSD and Linux based
    on os_name detection, replacing FreeBSD-specific references with appropriate
    OS-specific equivalents.

    Args:
        prompt: Original DEUS prompt string
        os_name: Operating system name (e.g., "FreeBSD", "Linux")

    Returns:
        OS-adapted prompt string
    """
    ##Action purpose: Intelligently switches prompt engineering between FreeBSD
    ##Step purpose: and Linux based on os_name detection, replacing FreeBSD-specific references
    ##Condition purpose: Check if OS is Linux (case-insensitive)
    if os_name and os_name.lower() != "linux":
        ##Condition purpose: If FreeBSD or other OS, return prompt as-is (already FreeBSD-optimized)
        return prompt

    ##Action purpose: Adapt prompt for Linux system
    ##Step purpose: Apply pre-compiled regex substitutions for performance (Profiler B8 optimization)
    adapted = prompt
    for pattern, replacement in _COMPILED_OS_PATTERNS:
        adapted = pattern.sub(replacement, adapted)

    ##Step purpose: Handle complex multi-line substitutions separately
    adapted = _adapt_directive_3(adapted)
    adapted = _adapt_maintenance_role(adapted)

    ##Action purpose: Return adapted prompt
    return adapted


##Function purpose: Build identity context block for prompt injection
def build_identity_context(identity: SystemIdentity) -> str:
    """
    Builds identity context block for prompt injection.

    Creates formatted markdown block containing user identity, system information,
    faction details, and session history to provide context to AI agents about
    who they're interacting with.

    Args:
        identity: SystemIdentity instance containing user and system information

    Returns:
        Formatted markdown string with identity context block
    """
    ##Action purpose: Creates formatted markdown block containing user identity,
    ##Step purpose: system information, faction details, and session history
    ##Action purpose: Get faction instance for philosophy display
    faction = FACTIONS.get(identity.faction)
    faction_philosophy = faction.philosophy if faction else "Unknown"

    ##Action purpose: Build identity context block
    context = f"""
## SYSTEM IDENTITY

**User:** {identity.username}@{identity.hostname}
**System:** {identity.os_name} {identity.os_version}
**Faction:** {identity.faction} ({faction_philosophy})

**Session History:**
- Total sessions: {identity.total_sessions}
"""

    ##Condition purpose: Add last mode if available
    if identity.last_mode:
        context += f"- Last mode: {identity.last_mode}\n"

    ##Condition purpose: Add last agent if available
    if identity.last_agent:
        context += f"- Last agent: {identity.last_agent}\n"

    ##Action purpose: Return formatted context block
    return context


##Function purpose: Build complete agent prompt with identity context and faction modifiers
def build_complete_prompt(
    agent_prompt: str,
    identity: SystemIdentity | None = None,
    faction_name: str | None = None,
    domain: str | None = None,
) -> str:
    """
    Builds complete agent prompt with identity context and faction modifiers.

    Composes final prompt by combining agent prompt, identity context, and faction
    modifiers in the correct order for optimal AI model understanding. For DEUS domain,
    intelligently adapts prompts based on detected OS (FreeBSD vs Linux).

    Composition order:
    1. Agent prompt (base + activation) - OS-adapted if DEUS
    2. Identity context (if provided)
    3. Faction modifiers (if provided)

    Args:
        agent_prompt: Base agent prompt (from Agent.full_prompt)
        identity: Optional SystemIdentity for context injection
        faction_name: Optional faction name for modifier application
        domain: Optional domain name ("daedelus" or "deus") for OS adaptation

    Returns:
        Complete prompt string ready for AI model
    """
    ##Action purpose: Composes final prompt by combining agent prompt, identity context,
    ##Step purpose: and faction modifiers in the correct order for optimal AI model understanding
    ##Action purpose: Start with agent prompt
    complete_prompt = agent_prompt

    ##Condition purpose: Adapt DEUS prompts for detected OS
    if domain and domain.lower() == "deus" and identity:
        ##Action purpose: Adapt prompt based on detected OS
        complete_prompt = _adapt_deus_prompt_for_os(complete_prompt, identity.os_name)

    ##Condition purpose: Add identity context if provided
    if identity:
        ##Action purpose: Append identity context block
        complete_prompt += build_identity_context(identity)

    ##Condition purpose: Apply faction modifiers if provided
    if faction_name:
        ##Action purpose: Get faction instance
        faction = FACTIONS.get(faction_name)
        ##Condition purpose: Apply modifiers if faction exists
        if faction:
            ##Action purpose: Apply faction modifiers to complete prompt
            complete_prompt = apply_faction_modifiers(complete_prompt, faction)

    ##Action purpose: Return complete composed prompt
    return complete_prompt


##Function purpose: Build complete prompt from agent key and domain
def build_agent_prompt_from_key(
    agent_key: str,
    domain: str,
    identity: SystemIdentity | None = None,
) -> str | None:
    """
    Builds complete prompt from agent key and domain.

    Convenience function that looks up agent by key in specified domain, then
    builds complete prompt with identity and faction modifiers. For DEUS domain,
    intelligently adapts prompts based on detected OS.

    Args:
        agent_key: Agent identifier (e.g., "A1", "B6", "ocm")
        domain: Domain name ("daedelus" or "deus")
        identity: Optional SystemIdentity for context

    Returns:
        Complete prompt string, or None if agent not found
    """
    ##Action purpose: Convenience function that looks up agent by key in specified
    ##Step purpose: domain, then builds complete prompt with identity and faction modifiers
    ##Condition purpose: Import appropriate domain agents
    if domain.lower() == "daedelus":
        from logos.daedelus.agents import get_agent
    elif domain.lower() == "deus":
        from logos.deus.agents import get_agent
    else:
        ##Action purpose: Return None for invalid domain
        return None

    ##Action purpose: Get agent by key
    agent = get_agent(agent_key)
    ##Condition purpose: Check if agent was found
    if agent is None:
        ##Action purpose: Return None if agent not found
        return None

    ##Action purpose: Get faction name from identity if available
    faction_name = identity.faction if identity else None

    ##Action purpose: Build complete prompt with all context and OS adaptation
    return build_complete_prompt(
        agent_prompt=agent.full_prompt,
        identity=identity,
        faction_name=faction_name,
        domain=domain,
    )
