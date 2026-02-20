"""
##Script function and purpose: Test boundary enforcement for Daedelus Group A and B agents.

Validates that A1-A5 and B6-B10 agents have the required SCOPE BOUNDARIES section,
IN SCOPE items, FORBIDDEN ACTIONS, and REFUSAL TEMPLATE.
"""

import re

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
from tests.helpers import extract_section

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
    """##Function purpose: Verify that the agent prompt contains at least 3 IN SCOPE items."""
    # Group A-B agents use ≥3 IN SCOPE categories (most have 4); Group C-E uses ≥5.
    # This reflects the original prompt structure where A-B agents have fewer, broader categories.
    header = "### ✅ IN SCOPE (What You CAN Do):"
    assert header in prompt, f"Agent {agent_key} missing IN SCOPE section"
    in_scope_text = extract_section(prompt, header)
    items = re.findall(r"(?:^|\n)\d+\. \*\*", in_scope_text)
    assert len(items) >= 3, (
        f"Agent {agent_key} has {len(items)} IN SCOPE items, expected at least 3"
    )

@pytest.mark.parametrize("agent_key,prompt", AGENTS.items())
def test_agent_has_forbidden_actions(agent_key, prompt):
    """##Function purpose: Verify that the agent prompt contains at least 10 FORBIDDEN ACTIONS with redirects."""
    # Group A-B uses the same ≥10 FORBIDDEN ACTIONS threshold as Group C-E.
    header = "### ⛔ FORBIDDEN ACTIONS (What You CANNOT Do):"
    assert header in prompt, f"Agent {agent_key} missing FORBIDDEN ACTIONS section"
    forbidden_text = extract_section(prompt, header)
    items = re.findall(r"(?:^|\n)\d+\. \*\*", forbidden_text)
    assert len(items) >= 10, (
        f"Agent {agent_key} has {len(items)} FORBIDDEN ACTIONS, expected at least 10"
    )
    redirects = forbidden_text.count("→")
    assert redirects >= len(items), (
        f"Agent {agent_key} has {redirects} redirects, expected at least {len(items)} (one per forbidden action)"
    )
    why_count = forbidden_text.count("Why:")
    assert why_count >= len(items), (
        f"Agent {agent_key} has {why_count} 'Why:' explanations, expected at least {len(items)} (one per forbidden action)"
    )

@pytest.mark.parametrize("agent_key,prompt", AGENTS.items())
def test_agent_has_collaboration_section(agent_key, prompt):
    """##Function purpose: Verify that the agent prompt contains REQUIRES COLLABORATION."""
    assert "### 🤝 REQUIRES COLLABORATION:" in prompt, f"Agent {agent_key} missing COLLABORATION section"

@pytest.mark.parametrize("agent_key,prompt", AGENTS.items())
def test_agent_has_refusal_template(agent_key, prompt):
    """##Function purpose: Verify that the agent prompt contains REFUSAL TEMPLATE."""
    header = "### 🚫 REFUSAL TEMPLATE"
    assert header in prompt, f"Agent {agent_key} missing REFUSAL TEMPLATE section"
    refusal_text = extract_section(prompt, header)
    assert "⛔ OUT OF SCOPE" in refusal_text, f"Agent {agent_key} missing '⛔ OUT OF SCOPE' in refusal template"
    assert "**Why I can't help:**" in refusal_text, f"Agent {agent_key} missing 'Why I can't help' in refusal template"