"""
##Script function and purpose: Test boundary enforcement for DEUS Group C, D, and E agents.

Validates that C1, C6-C11, D2-D5, and E1-E5 agents have the required
SCOPE BOUNDARIES section, IN SCOPE items, FORBIDDEN ACTIONS, and REFUSAL TEMPLATE.
"""

import re

import pytest

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
from tests.helpers import extract_section

# Map agent keys to their activation prompts
AGENTS = {
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


@pytest.mark.parametrize("agent_key,prompt", AGENTS.items(), ids=list(AGENTS.keys()))
def test_agent_has_scope_boundaries_section(agent_key, prompt):
    """##Function purpose: Verify that the agent prompt contains the SCOPE BOUNDARIES section."""
    assert "## SCOPE BOUNDARIES" in prompt, f"Agent {agent_key} missing SCOPE BOUNDARIES section"


@pytest.mark.parametrize("agent_key,prompt", AGENTS.items(), ids=list(AGENTS.keys()))
def test_agent_has_in_scope_items(agent_key, prompt):
    """##Function purpose: Verify that the agent prompt contains at least 5 IN SCOPE items."""
    header = "### ✅ IN SCOPE (What You CAN Do):"
    assert header in prompt, f"Agent {agent_key} missing IN SCOPE section"
    in_scope_text = extract_section(prompt, header)
    items = re.findall(r"^\d+\. \*\*", in_scope_text, re.MULTILINE)
    assert len(items) >= 5, (
        f"Agent {agent_key} has {len(items)} IN SCOPE items, expected at least 5"
    )


@pytest.mark.parametrize("agent_key,prompt", AGENTS.items(), ids=list(AGENTS.keys()))
def test_agent_has_forbidden_actions(agent_key, prompt):
    """##Function purpose: Verify that the agent prompt contains at least 10 FORBIDDEN ACTIONS."""
    header = "### ⛔ FORBIDDEN ACTIONS (What You CANNOT Do):"
    assert header in prompt, f"Agent {agent_key} missing FORBIDDEN ACTIONS section"
    forbidden_text = extract_section(prompt, header)
    items = re.findall(r"^\d+\. \*\*", forbidden_text, re.MULTILINE)
    assert len(items) >= 10, (
        f"Agent {agent_key} has {len(items)} FORBIDDEN ACTIONS, expected at least 10"
    )
    arrow_markers = forbidden_text.count("→")
    assert arrow_markers >= len(items), (
        f"Agent {agent_key} has {arrow_markers} arrow marker(s) (→) for "
        f"{len(items)} FORBIDDEN ACTIONS; expected at least one arrow marker per item"
    )
    why_count = forbidden_text.count("Why:")
    assert why_count >= len(items), (
        f"Agent {agent_key} has {why_count} 'Why:' explanation(s) for "
        f"{len(items)} FORBIDDEN ACTIONS; expected at least one explanation per item"
    )


@pytest.mark.parametrize("agent_key,prompt", AGENTS.items(), ids=list(AGENTS.keys()))
def test_agent_has_collaboration_section(agent_key, prompt):
    """##Function purpose: Verify that the agent prompt contains at least 3 REQUIRES COLLABORATION items."""
    header = "### 🤝 REQUIRES COLLABORATION:"
    assert header in prompt, f"Agent {agent_key} missing COLLABORATION section"
    collab_text = extract_section(prompt, header)
    items = re.findall(r"^\d+\. \*\*", collab_text, re.MULTILINE)
    assert len(items) >= 3, (
        f"Agent {agent_key} has {len(items)} COLLABORATION items, expected at least 3"
    )


@pytest.mark.parametrize("agent_key,prompt", AGENTS.items(), ids=list(AGENTS.keys()))
def test_agent_has_refusal_template(agent_key, prompt):
    """##Function purpose: Verify that the agent prompt contains REFUSAL TEMPLATE."""
    header = "### 🚫 REFUSAL TEMPLATE"
    assert header in prompt, f"Agent {agent_key} missing REFUSAL TEMPLATE section"
    refusal_text = extract_section(prompt, header)
    assert "⛔ OUT OF SCOPE" in refusal_text, f"Agent {agent_key} missing '⛔ OUT OF SCOPE' in template"
    assert "**Why I can't help:**" in refusal_text, f"Agent {agent_key} missing 'Why I can't help' in template"


@pytest.mark.parametrize("agent_key,prompt", AGENTS.items(), ids=list(AGENTS.keys()))
def test_agent_has_sysdocs_boundary(agent_key, prompt):
    """##Function purpose: Verify that every agent has ~/.sysdocs/ management boundary."""
    assert "~/.sysdocs/" in prompt, f"Agent {agent_key} missing ~/.sysdocs/ reference"
    sysdocs_heading = "~/.sysdocs/ Management"
    if sysdocs_heading in prompt:
        block = extract_section(prompt, sysdocs_heading)
        assert re.search(r'\borchestrator\b|\bE1\b', block, re.IGNORECASE), (
            f"Agent {agent_key} missing Orchestrator reference in ~/.sysdocs/ boundary"
        )
    else:
        match = re.search(
            r"(?:~/\.sysdocs/)[^\n]{0,80}\b(?:orchestrator|E1)\b|\b(?:orchestrator|E1)\b[^\n]{0,80}(?:~/\.sysdocs/)",
            prompt, re.IGNORECASE
        )
        assert match is not None, (
            f"Agent {agent_key} missing Orchestrator reference in ~/.sysdocs/ context"
        )
