"""
##Script function and purpose: Test Linux-specific OS instructions for all 26 DEUS agents.

Validates that every DEUS agent prompt contains the OS-SPECIFIC INSTRUCTIONS
section with a Linux subsection providing platform-appropriate commands and paths.
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
def test_agent_has_os_specific_section(agent_key, prompt):
    """##Function purpose: Verify each DEUS agent has an OS-SPECIFIC INSTRUCTIONS section."""
    assert "OS-SPECIFIC INSTRUCTIONS" in prompt, (
        f"Agent {agent_key} missing OS-SPECIFIC INSTRUCTIONS section"
    )


@pytest.mark.parametrize("agent_key,prompt", ALL_DEUS_AGENTS.items(), ids=list(ALL_DEUS_AGENTS.keys()))
def test_agent_has_linux_subsection(agent_key, prompt):
    """##Function purpose: Verify each DEUS agent has a Linux subsection in OS-SPECIFIC INSTRUCTIONS."""
    assert "### Linux" in prompt, (
        f"Agent {agent_key} missing Linux subsection in OS-SPECIFIC INSTRUCTIONS"
    )


@pytest.mark.parametrize("agent_key,prompt", ALL_DEUS_AGENTS.items(), ids=list(ALL_DEUS_AGENTS.keys()))
def test_linux_section_has_content(agent_key, prompt):
    """##Function purpose: Verify the Linux subsection contains substantive content (at least 3 items)."""
    linux_idx = prompt.find("### Linux")
    assert linux_idx != -1, f"Agent {agent_key} missing ### Linux header"
    # Extract text between ### Linux and the next ### or ## header
    after_linux = prompt[linux_idx + len("### Linux"):]
    next_header = len(after_linux)
    for marker in ["### FreeBSD", "## "]:
        idx = after_linux.find(marker)
        if idx != -1 and idx < next_header:
            next_header = idx
    linux_content = after_linux[:next_header]
    # Count bullet points (lines starting with -)
    bullets = [line for line in linux_content.split("\n") if line.strip().startswith("- ")]
    assert len(bullets) >= 3, (
        f"Agent {agent_key} Linux section has {len(bullets)} items, expected at least 3"
    )


@pytest.mark.parametrize("agent_key,prompt", ALL_DEUS_AGENTS.items(), ids=list(ALL_DEUS_AGENTS.keys()))
def test_linux_section_before_end_of_task(agent_key, prompt):
    """##Function purpose: Verify OS-SPECIFIC INSTRUCTIONS appear before END-OF-TASK PROTOCOL."""
    os_idx = prompt.find("OS-SPECIFIC INSTRUCTIONS")
    eot_idx = prompt.find("END-OF-TASK PROTOCOL")
    assert os_idx != -1, f"Agent {agent_key} missing OS-SPECIFIC INSTRUCTIONS"
    assert eot_idx != -1, f"Agent {agent_key} missing END-OF-TASK PROTOCOL"
    assert os_idx < eot_idx, (
        f"Agent {agent_key} OS-SPECIFIC INSTRUCTIONS must appear before END-OF-TASK PROTOCOL"
    )
