"""
##Script function and purpose: Test FreeBSD-specific OS instructions for all 26 DEUS agents.

Validates that every DEUS agent prompt contains the OS-SPECIFIC INSTRUCTIONS
section with a FreeBSD subsection providing platform-appropriate commands and paths.
"""

import pytest

from logos.deus.prompts.agents.auditors import (
    COMPLIANCE_CRITIC_ACTIVATION,
    PERFORMANCE_ANALYST_ACTIVATION,
    RELEASE_GATEKEEPER_ACTIVATION,
    SECURITY_AUDITOR_ACTIVATION,
    SYNTAX_MARSHAL_ACTIVATION,
)
from logos.deus.prompts.agents.engineers import (
    BOOT_ENGINEER_ACTIVATION,
    DRIVER_ENGINEER_ACTIVATION,
    KERNEL_ARCHITECT_ACTIVATION,
    NETWORK_ARCHITECT_ACTIVATION,
    SERVICE_SCRIBE_ACTIVATION,
)
from logos.deus.prompts.agents.maintainers import (
    BUG_HUNTER_ACTIVATION,
    MANUAL_KEEPER_ACTIVATION,
    OPTIMIZER_ACTIVATION,
    PORT_LIBRARIAN_ACTIVATION,
    SECURITY_PATCHER_ACTIVATION,
    SYSCTL_TUNER_ACTIVATION,
    SYSTEM_JANITOR_ACTIVATION,
)
from logos.deus.prompts.agents.operators import (
    ADMINISTRATOR_ACTIVATION,
    DEUS_ACTIVATION,
    GENERAL_MANAGER_ACTIVATION,
    OMBUDSMAN_ACTIVATION,
    SYSTEM_ORCHESTRATOR_ACTIVATION,
)
from logos.deus.prompts.agents.specialists import (
    COMPATIBILITY_ENGINEER_ACTIVATION,
    JAIL_ARCHITECT_ACTIVATION,
    PORT_BUILDER_ACTIVATION,
    ZFS_ENGINEER_ACTIVATION,
)

ALL_DEUS_AGENTS = {
    "A1": KERNEL_ARCHITECT_ACTIVATION,
    "A2": DRIVER_ENGINEER_ACTIVATION,
    "A3": NETWORK_ARCHITECT_ACTIVATION,
    "A4": BOOT_ENGINEER_ACTIVATION,
    "A5": SERVICE_SCRIBE_ACTIVATION,
    "B6": SECURITY_AUDITOR_ACTIVATION,
    "B7": SYNTAX_MARSHAL_ACTIVATION,
    "B8": PERFORMANCE_ANALYST_ACTIVATION,
    "B9": COMPLIANCE_CRITIC_ACTIVATION,
    "B10": RELEASE_GATEKEEPER_ACTIVATION,
    "C1": BUG_HUNTER_ACTIVATION,
    "C6": SECURITY_PATCHER_ACTIVATION,
    "C7": MANUAL_KEEPER_ACTIVATION,
    "C8": SYSCTL_TUNER_ACTIVATION,
    "C9": OPTIMIZER_ACTIVATION,
    "C10": SYSTEM_JANITOR_ACTIVATION,
    "C11": PORT_LIBRARIAN_ACTIVATION,
    "D2": PORT_BUILDER_ACTIVATION,
    "D3": COMPATIBILITY_ENGINEER_ACTIVATION,
    "D4": JAIL_ARCHITECT_ACTIVATION,
    "D5": ZFS_ENGINEER_ACTIVATION,
    "E1": SYSTEM_ORCHESTRATOR_ACTIVATION,
    "E2": ADMINISTRATOR_ACTIVATION,
    "E3": GENERAL_MANAGER_ACTIVATION,
    "E4": OMBUDSMAN_ACTIVATION,
    "E5": DEUS_ACTIVATION,
}


@pytest.mark.parametrize("agent_key,prompt", ALL_DEUS_AGENTS.items(), ids=list(ALL_DEUS_AGENTS.keys()))
def test_agent_has_freebsd_subsection(agent_key, prompt):
    """##Function purpose: Verify each DEUS agent has a FreeBSD subsection in OS-SPECIFIC INSTRUCTIONS."""
    assert "### FreeBSD" in prompt, (
        f"Agent {agent_key} missing FreeBSD subsection in OS-SPECIFIC INSTRUCTIONS"
    )


@pytest.mark.parametrize("agent_key,prompt", ALL_DEUS_AGENTS.items(), ids=list(ALL_DEUS_AGENTS.keys()))
def test_freebsd_section_has_content(agent_key, prompt):
    """##Function purpose: Verify the FreeBSD subsection contains substantive content (at least 3 items)."""
    freebsd_idx = prompt.find("### FreeBSD")
    assert freebsd_idx != -1, f"Agent {agent_key} missing ### FreeBSD header"
    # Extract text between ### FreeBSD and the next ## header
    after_freebsd = prompt[freebsd_idx + len("### FreeBSD"):]
    next_header = len(after_freebsd)
    for marker in ["## "]:
        idx = after_freebsd.find(marker)
        if idx != -1 and idx < next_header:
            next_header = idx
    freebsd_content = after_freebsd[:next_header]
    # Count bullet points (lines starting with -)
    bullets = [line for line in freebsd_content.split("\n") if line.strip().startswith("- ")]
    assert len(bullets) >= 3, (
        f"Agent {agent_key} FreeBSD section has {len(bullets)} items, expected at least 3"
    )


@pytest.mark.parametrize("agent_key,prompt", ALL_DEUS_AGENTS.items(), ids=list(ALL_DEUS_AGENTS.keys()))
def test_freebsd_section_after_linux_section(agent_key, prompt):
    """##Function purpose: Verify FreeBSD section follows Linux section (consistent ordering)."""
    linux_idx = prompt.find("### Linux")
    freebsd_idx = prompt.find("### FreeBSD")
    assert linux_idx != -1, f"Agent {agent_key} missing ### Linux header"
    assert freebsd_idx != -1, f"Agent {agent_key} missing ### FreeBSD header"
    assert linux_idx < freebsd_idx, (
        f"Agent {agent_key} ### Linux should appear before ### FreeBSD"
    )


@pytest.mark.parametrize("agent_key,prompt", ALL_DEUS_AGENTS.items(), ids=list(ALL_DEUS_AGENTS.keys()))
def test_freebsd_section_before_end_of_task(agent_key, prompt):
    """##Function purpose: Verify FreeBSD section appears before END-OF-TASK PROTOCOL."""
    freebsd_idx = prompt.find("### FreeBSD")
    eot_idx = prompt.find("END-OF-TASK PROTOCOL")
    assert freebsd_idx != -1, f"Agent {agent_key} missing ### FreeBSD header"
    assert eot_idx != -1, f"Agent {agent_key} missing END-OF-TASK PROTOCOL"
    assert freebsd_idx < eot_idx, (
        f"Agent {agent_key} ### FreeBSD must appear before END-OF-TASK PROTOCOL"
    )
