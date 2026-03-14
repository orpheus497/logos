"""
##Script function and purpose: Integration tests for agent boundary enforcement across domains.

Verifies that all 50 agents (24 Daedelus + 26 DEUS) load correctly,
have non-empty prompts, contain required boundary sections, and maintain
cross-domain consistency in agent key structure.
"""

import pytest

from logos.core.agent import Agent
from logos.daedelus import get_agent as dae_get_agent
from logos.deus import get_agent as deus_get_agent

DAEDELUS_KEYS = [
    "A1",
    "A2",
    "A3",
    "A4",
    "A5",
    "B6",
    "B7",
    "B8",
    "B9",
    "B10",
    "C1",
    "C6",
    "C7",
    "C8",
    "C9",
    "C10",
    "C11",
    "D2",
    "D3",
    "D4",
    "D5",
    "E1",
    "E2",
    "E3",
]

DEUS_KEYS = [
    "A1",
    "A2",
    "A3",
    "A4",
    "A5",
    "B6",
    "B7",
    "B8",
    "B9",
    "B10",
    "C1",
    "C6",
    "C7",
    "C8",
    "C9",
    "C10",
    "C11",
    "D2",
    "D3",
    "D4",
    "D5",
    "E1",
    "E2",
    "E3",
    "E4",
    "E5",
]

SHARED_KEYS = sorted(set(DAEDELUS_KEYS) & set(DEUS_KEYS))


class TestAllAgentsLoad:
    """Verify every registered agent loads and has required fields."""

    @pytest.mark.parametrize("key", DAEDELUS_KEYS)
    def test_daedelus_agent_loads(self, key):
        """##Function purpose: Verify each Daedelus agent key resolves to a non-None Agent instance."""
        agent = dae_get_agent(key)
        assert agent is not None, f"Daedelus agent {key} returned None"
        assert isinstance(agent, Agent)

    @pytest.mark.parametrize("key", DEUS_KEYS)
    def test_deus_agent_loads(self, key):
        """##Function purpose: Verify each DEUS agent key resolves to a non-None Agent instance."""
        agent = deus_get_agent(key)
        assert agent is not None, f"DEUS agent {key} returned None"
        assert isinstance(agent, Agent)

    @pytest.mark.parametrize("key", DAEDELUS_KEYS)
    def test_daedelus_agent_has_nonempty_prompt(self, key):
        """##Function purpose: Verify each Daedelus agent has a non-empty full_prompt."""
        agent = dae_get_agent(key)
        assert agent.full_prompt.strip(), f"Daedelus {key} has empty full_prompt"

    @pytest.mark.parametrize("key", DEUS_KEYS)
    def test_deus_agent_has_nonempty_prompt(self, key):
        """##Function purpose: Verify each DEUS agent has a non-empty full_prompt."""
        agent = deus_get_agent(key)
        assert agent.full_prompt.strip(), f"DEUS {key} has empty full_prompt"

    def test_daedelus_agent_count(self):
        """##Function purpose: Verify exactly 24 Daedelus agents are registered and loadable."""
        loaded = [k for k in DAEDELUS_KEYS if dae_get_agent(k) is not None]
        assert len(loaded) == 24, f"Expected 24 Daedelus agents, got {len(loaded)}"

    def test_deus_agent_count(self):
        """##Function purpose: Verify exactly 26 DEUS agents are registered and loadable."""
        loaded = [k for k in DEUS_KEYS if deus_get_agent(k) is not None]
        assert len(loaded) == 26, f"Expected 26 DEUS agents, got {len(loaded)}"


class TestAgentFieldIntegrity:
    """Verify agent dataclass fields are populated correctly."""

    @pytest.mark.parametrize("key", DAEDELUS_KEYS)
    def test_daedelus_fields_nonempty(self, key):
        """##Function purpose: Verify each Daedelus agent has non-empty name, desc, group, and purpose fields."""
        agent = dae_get_agent(key)
        assert agent.name.strip(), f"Daedelus {key} has empty name"
        assert agent.desc.strip(), f"Daedelus {key} has empty desc"
        assert agent.group.strip(), f"Daedelus {key} has empty group"
        assert agent.purpose.strip(), f"Daedelus {key} has empty purpose"

    @pytest.mark.parametrize("key", DEUS_KEYS)
    def test_deus_fields_nonempty(self, key):
        """##Function purpose: Verify each DEUS agent has non-empty name, desc, group, and purpose fields."""
        agent = deus_get_agent(key)
        assert agent.name.strip(), f"DEUS {key} has empty name"
        assert agent.desc.strip(), f"DEUS {key} has empty desc"
        assert agent.group.strip(), f"DEUS {key} has empty group"
        assert agent.purpose.strip(), f"DEUS {key} has empty purpose"

    @pytest.mark.parametrize("key", DAEDELUS_KEYS)
    def test_daedelus_group_matches_key(self, key):
        """##Function purpose: Verify each Daedelus agent's group field matches the first letter of its key."""
        agent = dae_get_agent(key)
        expected_group = key[0].upper()
        assert agent.group.upper() == expected_group, (
            f"Daedelus {key} group is '{agent.group}', expected '{expected_group}'"
        )

    @pytest.mark.parametrize("key", DEUS_KEYS)
    def test_deus_group_matches_key(self, key):
        """##Function purpose: Verify each DEUS agent's group field matches the first letter of its key."""
        agent = deus_get_agent(key)
        expected_group = key[0].upper()
        assert agent.group.upper() == expected_group, (
            f"DEUS {key} group is '{agent.group}', expected '{expected_group}'"
        )


class TestCrossDomainConsistency:
    """Verify structural consistency between Daedelus and DEUS agents."""

    @pytest.mark.parametrize("key", SHARED_KEYS)
    def test_shared_keys_exist_in_both_domains(self, key):
        """##Function purpose: Verify each shared agent key resolves successfully in both Daedelus and DEUS."""
        dae = dae_get_agent(key)
        deus = deus_get_agent(key)
        assert dae is not None, f"Shared key {key} missing from Daedelus"
        assert deus is not None, f"Shared key {key} missing from DEUS"

    @pytest.mark.parametrize("key", SHARED_KEYS)
    def test_shared_agents_have_same_group(self, key):
        """##Function purpose: Verify shared keys map to the same group letter in both domains."""
        dae = dae_get_agent(key)
        deus = deus_get_agent(key)
        assert dae.group.upper() == deus.group.upper(), (
            f"Key {key}: Daedelus group='{dae.group}' vs DEUS group='{deus.group}'"
        )

    @pytest.mark.parametrize("key", SHARED_KEYS)
    def test_shared_agents_have_distinct_names(self, key):
        """##Function purpose: Verify shared-key agents have domain-specific names (except known exceptions)."""
        dae = dae_get_agent(key)
        deus = deus_get_agent(key)
        shared_name_keys = {"C1", "C6", "C9"}
        assert dae.name != deus.name or key in shared_name_keys, (
            f"Key {key}: both domains share name '{dae.name}' — expected domain-specific names"
        )

    @pytest.mark.parametrize("key", SHARED_KEYS)
    def test_shared_agents_have_distinct_prompts(self, key):
        """##Function purpose: Verify shared-key agents have domain-specific prompts (not identical content)."""
        dae = dae_get_agent(key)
        deus = deus_get_agent(key)
        assert dae.full_prompt != deus.full_prompt, (
            f"Key {key}: Daedelus and DEUS have identical full_prompt (should be domain-specific)"
        )


class TestBoundaryPresenceIntegration:
    """Verify all agents have SCOPE BOUNDARIES across both domains."""

    @pytest.mark.parametrize("key", DAEDELUS_KEYS)
    def test_daedelus_has_scope_boundaries(self, key):
        """##Function purpose: Verify each Daedelus agent prompt contains the SCOPE BOUNDARIES section."""
        agent = dae_get_agent(key)
        assert "## SCOPE BOUNDARIES" in agent.full_prompt, f"Daedelus {key} ({agent.name}) missing SCOPE BOUNDARIES"

    @pytest.mark.parametrize("key", DEUS_KEYS)
    def test_deus_has_scope_boundaries(self, key):
        """##Function purpose: Verify each DEUS agent prompt contains the SCOPE BOUNDARIES section."""
        agent = deus_get_agent(key)
        assert "## SCOPE BOUNDARIES" in agent.full_prompt, f"DEUS {key} ({agent.name}) missing SCOPE BOUNDARIES"

    @pytest.mark.parametrize("key", DAEDELUS_KEYS)
    def test_daedelus_has_refusal_template(self, key):
        """##Function purpose: Verify each Daedelus agent prompt includes a REFUSAL TEMPLATE section."""
        agent = dae_get_agent(key)
        assert "REFUSAL TEMPLATE" in agent.full_prompt, f"Daedelus {key} ({agent.name}) missing REFUSAL TEMPLATE"

    @pytest.mark.parametrize("key", DEUS_KEYS)
    def test_deus_has_refusal_template(self, key):
        """##Function purpose: Verify each DEUS agent prompt includes a REFUSAL TEMPLATE section."""
        agent = deus_get_agent(key)
        assert "REFUSAL TEMPLATE" in agent.full_prompt, f"DEUS {key} ({agent.name}) missing REFUSAL TEMPLATE"

    @pytest.mark.parametrize("key", DAEDELUS_KEYS)
    def test_daedelus_has_devdocs_reference(self, key):
        """##Function purpose: Verify each Daedelus agent prompt references the .devdocs/ governance folder."""
        agent = dae_get_agent(key)
        assert ".devdocs/" in agent.full_prompt, f"Daedelus {key} ({agent.name}) missing .devdocs/ reference"

    @pytest.mark.parametrize("key", DEUS_KEYS)
    def test_deus_has_docs_reference(self, key):
        """##Function purpose: Verify each DEUS agent prompt references .sysdocs/ or .devdocs/ governance folder."""
        agent = deus_get_agent(key)
        has_sysdocs = ".sysdocs/" in agent.full_prompt
        has_devdocs = ".devdocs/" in agent.full_prompt
        assert has_sysdocs or has_devdocs, f"DEUS {key} ({agent.name}) missing .sysdocs/ or .devdocs/ reference"


class TestCaseInsensitiveLookup:
    """Verify get_agent supports case-insensitive keys."""

    @pytest.mark.parametrize("variant", ["a1", "A1"])
    def test_daedelus_case_insensitive(self, variant):
        """##Function purpose: Verify get_agent accepts lowercase and uppercase Daedelus key variants."""
        agent = dae_get_agent(variant)
        assert agent is not None

    @pytest.mark.parametrize("variant", ["e5", "E5"])
    def test_deus_case_insensitive(self, variant):
        """##Function purpose: Verify get_agent accepts lowercase and uppercase DEUS key variants."""
        agent = deus_get_agent(variant)
        assert agent is not None

    def test_invalid_key_returns_none_daedelus(self):
        """##Function purpose: Verify an unrecognized key returns None from Daedelus get_agent."""
        assert dae_get_agent("Z99") is None

    def test_invalid_key_returns_none_deus(self):
        """##Function purpose: Verify an unrecognized key returns None from DEUS get_agent."""
        assert deus_get_agent("Z99") is None
