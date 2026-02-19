"""
##Script function and purpose: Test boundary enforcement for Daedelus Group C, D, and E agents.

Validates that C1, C6-C11, D2-D5, orchestrator, ocm, and daedelus agents have the required
SCOPE BOUNDARIES section, IN SCOPE items, FORBIDDEN ACTIONS, and REFUSAL TEMPLATE.
"""

import re

import pytest

from logos.daedelus.prompts.agents.maintainers import (
    BUG_HUNTER_ACTIVATION,
    CONFIGURATOR_ACTIVATION,
    DOC_UPDATER_ACTIVATION,
    JANITOR_ACTIVATION,
    LIBRARIAN_ACTIVATION,
    OPTIMIZER_ACTIVATION,
    SECURITY_PATCHER_ACTIVATION,
)
from logos.daedelus.prompts.agents.operators import (
    DAEDELUS_ACTIVATION,
    OPERATIONAL_CONTROL_MANAGER_ACTIVATION,
    ORCHESTRATOR_ACTIVATION,
)
from logos.daedelus.prompts.agents.workers import (
    FEATURE_SPRINTER_ACTIVATION,
    REFACTORER_ACTIVATION,
    TEST_EXTENDER_ACTIVATION,
    UI_TWEAKER_ACTIVATION,
)

# Map agent keys to their activation prompts
AGENTS = {
    "C1": BUG_HUNTER_ACTIVATION,
    "C6": SECURITY_PATCHER_ACTIVATION,
    "C7": DOC_UPDATER_ACTIVATION,
    "C8": CONFIGURATOR_ACTIVATION,
    "C9": OPTIMIZER_ACTIVATION,
    "C10": JANITOR_ACTIVATION,
    "C11": LIBRARIAN_ACTIVATION,
    "D2": FEATURE_SPRINTER_ACTIVATION,
    "D3": REFACTORER_ACTIVATION,
    "D4": UI_TWEAKER_ACTIVATION,
    "D5": TEST_EXTENDER_ACTIVATION,
    "orchestrator": ORCHESTRATOR_ACTIVATION,
    "ocm": OPERATIONAL_CONTROL_MANAGER_ACTIVATION,
    "daedelus": DAEDELUS_ACTIVATION,
}


@pytest.mark.parametrize("agent_key,prompt", AGENTS.items())
def test_agent_has_scope_boundaries_section(agent_key, prompt):
    """##Function purpose: Verify that the agent prompt contains the SCOPE BOUNDARIES section."""
    assert "## SCOPE BOUNDARIES" in prompt, f"Agent {agent_key} missing SCOPE BOUNDARIES section"


@pytest.mark.parametrize("agent_key,prompt", AGENTS.items())
def test_agent_has_in_scope_items(agent_key, prompt):
    """##Function purpose: Verify that the agent prompt contains at least 5 IN SCOPE items."""
    header = "### ✅ IN SCOPE (What You CAN Do):"
    assert header in prompt, f"Agent {agent_key} missing IN SCOPE section"
    # Extract only the IN SCOPE section (up to the next ### or ## heading)
    start = prompt.index(header) + len(header)
    rest = prompt[start:]
    end = len(rest)
    for marker in ("\n### ", "\n## "):
        pos = rest.find(marker)
        if pos != -1 and pos < end:
            end = pos
    in_scope_text = rest[:end]
    # Count numbered list items (e.g. "1. **", "2. **") within the section
    items = re.findall(r"\n\d+\. \*\*", in_scope_text)
    assert len(items) >= 5, (
        f"Agent {agent_key} has {len(items)} IN SCOPE items, expected at least 5"
    )


@pytest.mark.parametrize("agent_key,prompt", AGENTS.items())
def test_agent_has_forbidden_actions(agent_key, prompt):
    """##Function purpose: Verify that the agent prompt contains at least 10 FORBIDDEN ACTIONS."""
    header = "### ⛔ FORBIDDEN ACTIONS (What You CANNOT Do):"
    assert header in prompt, f"Agent {agent_key} missing FORBIDDEN ACTIONS section"
    # Extract FORBIDDEN section
    start = prompt.index(header) + len(header)
    rest = prompt[start:]
    end = len(rest)
    for marker in ("\n### ", "\n## "):
        pos = rest.find(marker)
        if pos != -1 and pos < end:
            end = pos
    forbidden_text = rest[:end]
    # Count numbered forbidden items
    items = re.findall(r"\n\d+\. \*\*", forbidden_text)
    assert len(items) >= 10, (
        f"Agent {agent_key} has {len(items)} FORBIDDEN ACTIONS, expected at least 10"
    )
    # Verify redirects and explanations
    assert "→" in forbidden_text, f"Agent {agent_key} forbidden actions missing redirects (→)"
    assert "*Why:*" in forbidden_text, f"Agent {agent_key} forbidden actions missing 'Why' explanations"


@pytest.mark.parametrize("agent_key,prompt", AGENTS.items())
def test_agent_has_collaboration_section(agent_key, prompt):
    """##Function purpose: Verify that the agent prompt contains at least 3 REQUIRES COLLABORATION items."""
    header = "### 🤝 REQUIRES COLLABORATION:"
    assert header in prompt, f"Agent {agent_key} missing COLLABORATION section"
    # Extract COLLABORATION section
    start = prompt.index(header) + len(header)
    rest = prompt[start:]
    end = len(rest)
    for marker in ("\n### ", "\n## "):
        pos = rest.find(marker)
        if pos != -1 and pos < end:
            end = pos
    collab_text = rest[:end]
    # Count numbered collaboration items
    items = re.findall(r"\n\d+\. \*\*", collab_text)
    assert len(items) >= 3, (
        f"Agent {agent_key} has {len(items)} COLLABORATION items, expected at least 3"
    )


@pytest.mark.parametrize("agent_key,prompt", AGENTS.items())
def test_agent_has_refusal_template(agent_key, prompt):
    """##Function purpose: Verify that the agent prompt contains REFUSAL TEMPLATE."""
    assert "### 🚫 REFUSAL TEMPLATE" in prompt, f"Agent {agent_key} missing REFUSAL TEMPLATE section"
    assert "⛔ OUT OF SCOPE" in prompt, f"Agent {agent_key} missing '⛔ OUT OF SCOPE' in template"
    assert "**Why I can't help:**" in prompt, f"Agent {agent_key} missing 'Why I can't help' in template"


@pytest.mark.parametrize("agent_key,prompt", AGENTS.items())
def test_agent_has_devdocs_boundary(agent_key, prompt):
    """##Function purpose: Verify that every agent has .devdocs/ management boundary."""
    assert ".devdocs/" in prompt, f"Agent {agent_key} missing .devdocs/ reference"
    assert "orchestrator" in prompt.lower() or agent_key == "orchestrator", (
        f"Agent {agent_key} missing orchestrator reference in .devdocs boundary"
    )
