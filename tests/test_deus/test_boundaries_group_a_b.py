"""
##Script function and purpose: Test boundary enforcement for DEUS Group A and B agents.

Validates that A1-A5 and B6-B10 agents have the required
SCOPE BOUNDARIES section, IN SCOPE items, FORBIDDEN ACTIONS, and REFUSAL TEMPLATE.
"""

import re

import pytest

from logos.deus.prompts.agents.engineers import (
    KERNEL_ARCHITECT_ACTIVATION,
    DRIVER_ENGINEER_ACTIVATION,
    NETWORK_ARCHITECT_ACTIVATION,
    BOOT_ENGINEER_ACTIVATION,
    SERVICE_SCRIBE_ACTIVATION,
)
from logos.deus.prompts.agents.auditors import (
    SECURITY_AUDITOR_ACTIVATION,
    SYNTAX_MARSHAL_ACTIVATION,
    PERFORMANCE_ANALYST_ACTIVATION,
    COMPLIANCE_CRITIC_ACTIVATION,
    RELEASE_GATEKEEPER_ACTIVATION,
)
from tests.helpers import extract_section

# Map agent keys to their activation prompts
AGENTS = {
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
}


@pytest.mark.parametrize("agent_key,prompt", AGENTS.items(), ids=list(AGENTS.keys()))
def test_agent_has_scope_boundaries_section(agent_key, prompt):
    """##Function purpose: Verify that the agent prompt contains the SCOPE BOUNDARIES section."""
    assert "## SCOPE BOUNDARIES" in prompt, f"Agent {agent_key} missing SCOPE BOUNDARIES section"


@pytest.mark.parametrize("agent_key,prompt", AGENTS.items(), ids=list(AGENTS.keys()))
def test_agent_has_in_scope_items(agent_key, prompt):
    """##Function purpose: Verify that the agent prompt contains at least 3 IN SCOPE items."""
    header = "### ✅ IN SCOPE (What You CAN Do):"
    assert header in prompt, f"Agent {agent_key} missing IN SCOPE section"
    in_scope_text = extract_section(prompt, header)
    items = re.findall(r"^\d+\. \*\*", in_scope_text, flags=re.MULTILINE)
    assert len(items) >= 3, (
        f"Agent {agent_key} has {len(items)} IN SCOPE items, expected at least 3"
    )


@pytest.mark.parametrize("agent_key,prompt", AGENTS.items(), ids=list(AGENTS.keys()))
def test_agent_has_forbidden_actions(agent_key, prompt):
    """##Function purpose: Verify that the agent prompt contains at least 10 FORBIDDEN ACTIONS with redirects."""
    header = "### ⛔ FORBIDDEN ACTIONS (What You CANNOT Do):"
    assert header in prompt, f"Agent {agent_key} missing FORBIDDEN ACTIONS section"
    forbidden_text = extract_section(prompt, header)
    items = re.findall(r"^\d+\. \*\*", forbidden_text, flags=re.MULTILINE)
    assert len(items) >= 10, (
        f"Agent {agent_key} has {len(items)} FORBIDDEN ACTIONS, expected at least 10"
    )
    redirects = forbidden_text.count("→")
    assert redirects >= len(items), (
        f"Agent {agent_key} has {redirects} redirects, expected at least {len(items)}"
    )
    why_count = forbidden_text.count("Why:")
    assert why_count >= len(items), (
        f"Agent {agent_key} has {why_count} 'Why:' explanations, expected at least {len(items)}"
    )


@pytest.mark.parametrize("agent_key,prompt", AGENTS.items(), ids=list(AGENTS.keys()))
def test_agent_has_collaboration_section(agent_key, prompt):
    """##Function purpose: Verify that the agent prompt contains REQUIRES COLLABORATION."""
    assert "### 🤝 REQUIRES COLLABORATION:" in prompt, f"Agent {agent_key} missing COLLABORATION section"


@pytest.mark.parametrize("agent_key,prompt", AGENTS.items(), ids=list(AGENTS.keys()))
def test_agent_has_refusal_template(agent_key, prompt):
    """##Function purpose: Verify that the agent prompt contains REFUSAL TEMPLATE."""
    header = "### 🚫 REFUSAL TEMPLATE"
    assert header in prompt, f"Agent {agent_key} missing REFUSAL TEMPLATE section"
    refusal_text = extract_section(prompt, header)
    assert "⛔ OUT OF SCOPE" in refusal_text, f"Agent {agent_key} missing '⛔ OUT OF SCOPE' in refusal template"
    assert "**Why I can't help:**" in refusal_text, f"Agent {agent_key} missing 'Why I can't help' in refusal template"


@pytest.mark.parametrize("agent_key,prompt", AGENTS.items(), ids=list(AGENTS.keys()))
def test_agent_has_sysdocs_boundary(agent_key, prompt):
    """##Function purpose: Verify that every agent has ~/.sysdocs/ management boundary."""
    assert "~/.sysdocs/" in prompt, f"Agent {agent_key} missing ~/.sysdocs/ reference"
    assert re.search(
        r"(?:~/.sysdocs/[^\n]{0,80}(?:orchestrator|E1))|(?:(?:orchestrator|E1)[^\n]{0,80}~/.sysdocs/)",
        prompt, re.IGNORECASE
    ), f"Agent {agent_key} missing Orchestrator/E1 reference in ~/.sysdocs/ context"
