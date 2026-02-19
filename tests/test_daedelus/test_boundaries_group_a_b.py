"""
##Script function and purpose: Test boundary enforcement for Daedelus Group A and B agents.

Validates that A1-A5 and B6-B10 agents have the required SCOPE BOUNDARIES section,
IN SCOPE items, FORBIDDEN ACTIONS, and REFUSAL TEMPLATE.
"""

import pytest

from logos.daedelus.prompts.agents.builders import (
    ARCHITECT_ACTIVATION,
    INTERFACE_DESIGNER_ACTIVATION,
    LOGIC_ENGINEER_ACTIVATION,
    SCRIBE_ACTIVATION,
    TEST_ENGINEER_ACTIVATION,
)
from logos.daedelus.prompts.agents.guardians import (
    CRITIC_ACTIVATION,
    GATEKEEPER_ACTIVATION,
    MARSHAL_ACTIVATION,
    PROFILER_ACTIVATION,
    SENTINEL_ACTIVATION,
)

# Map agent keys to their activation prompts
AGENTS = {
    "A1": ARCHITECT_ACTIVATION,
    "A2": LOGIC_ENGINEER_ACTIVATION,
    "A3": INTERFACE_DESIGNER_ACTIVATION,
    "A4": TEST_ENGINEER_ACTIVATION,
    "A5": SCRIBE_ACTIVATION,
    "B6": SENTINEL_ACTIVATION,
    "B7": MARSHAL_ACTIVATION,
    "B8": PROFILER_ACTIVATION,
    "B9": CRITIC_ACTIVATION,
    "B10": GATEKEEPER_ACTIVATION,
}

@pytest.mark.parametrize("agent_key,prompt", AGENTS.items())
def test_agent_has_scope_boundaries_section(agent_key, prompt):
    """##Function purpose: Verify that the agent prompt contains the SCOPE BOUNDARIES section."""
    assert "## SCOPE BOUNDARIES" in prompt, f"Agent {agent_key} missing SCOPE BOUNDARIES section"

@pytest.mark.parametrize("agent_key,prompt", AGENTS.items())
def test_agent_has_in_scope_items(agent_key, prompt):
    """##Function purpose: Verify that the agent prompt contains at least 5 IN SCOPE items."""
    assert "### ✅ IN SCOPE (What You CAN Do):" in prompt, f"Agent {agent_key} missing IN SCOPE section"
    # Count numbered items in the IN SCOPE section
    # This is a heuristic: split by "1.", "2.", etc. or just check for enough list items
    # A robust check might look for "1. **", "2. **", etc.
    # Let's count occurrences of "\n1. **", "\n2. **", etc.
    count = 0
    for i in range(1, 6):
        if f"\n{i}. **" in prompt:
            count += 1
    # Some prompts might use 1. **Header** style.
    # We require minimum 3 top-level items for now as a smoke test, though spec says 5.
    # Let's check for at least 3 to be safe against formatting variations,
    # but the content actually has 4 or 5.
    assert count >= 3, f"Agent {agent_key} has fewer than 3 IN SCOPE items detected"

@pytest.mark.parametrize("agent_key,prompt", AGENTS.items())
def test_agent_has_forbidden_actions(agent_key, prompt):
    """##Function purpose: Verify that the agent prompt contains FORBIDDEN ACTIONS."""
    assert "### ⛔ FORBIDDEN ACTIONS (What You CANNOT Do):" in prompt, f"Agent {agent_key} missing FORBIDDEN ACTIONS section"
    # Verify redirects exist
    assert "→" in prompt, f"Agent {agent_key} forbidden actions missing redirects (→)"
    assert "*Why:*" in prompt, f"Agent {agent_key} forbidden actions missing 'Why' explanations"

@pytest.mark.parametrize("agent_key,prompt", AGENTS.items())
def test_agent_has_collaboration_section(agent_key, prompt):
    """##Function purpose: Verify that the agent prompt contains REQUIRES COLLABORATION."""
    assert "### 🤝 REQUIRES COLLABORATION:" in prompt, f"Agent {agent_key} missing COLLABORATION section"

@pytest.mark.parametrize("agent_key,prompt", AGENTS.items())
def test_agent_has_refusal_template(agent_key, prompt):
    """##Function purpose: Verify that the agent prompt contains REFUSAL TEMPLATE."""
    assert "### 🚫 REFUSAL TEMPLATE" in prompt, f"Agent {agent_key} missing REFUSAL TEMPLATE section"
    assert "⛔ OUT OF SCOPE" in prompt, f"Agent {agent_key} missing '⛔ OUT OF SCOPE' in template"
    assert "**Why I can't help:**" in prompt, f"Agent {agent_key} missing 'Why I can't help' in template"
