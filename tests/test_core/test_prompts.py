"""
##Script function and purpose: Unit tests for logos.core.prompts module.

Tests prompt composition functions including identity context, complete prompts, and agent lookup.
"""

from unittest.mock import MagicMock, patch

from logos.core.identity import create_identity, scan_system
from logos.core.prompts import (
    build_agent_prompt_from_key,
    build_complete_prompt,
    build_identity_context,
)


##Function purpose: Test build_identity_context
def test_build_identity_context():
    """##Function purpose: Verify build_identity_context creates formatted context block.."""
    ##Action purpose: Create identity
    scan = scan_system()
    identity = create_identity("orphic", scan)
    identity.total_sessions = 5
    identity.last_mode = "daedelus"
    identity.last_agent = "A2"

    ##Action purpose: Build context
    context = build_identity_context(identity)

    ##Condition purpose: Verify context contains required fields
    assert "SYSTEM IDENTITY" in context
    assert identity.username in context
    assert identity.hostname in context
    assert identity.os_name in context
    assert identity.os_version in context
    assert identity.faction in context
    assert str(identity.total_sessions) in context
    assert identity.last_mode in context
    assert identity.last_agent in context


##Function purpose: Test build_identity_context without session info
def test_build_identity_context_no_session():
    """##Function purpose: Verify build_identity_context works without session info.."""
    ##Action purpose: Create identity without session info
    scan = scan_system()
    identity = create_identity("technomancer", scan)

    ##Action purpose: Build context
    context = build_identity_context(identity)

    ##Condition purpose: Verify context contains basic info
    assert "SYSTEM IDENTITY" in context
    assert identity.username in context
    assert identity.faction in context

    ##Condition purpose: Verify no session info in context
    assert "Last mode" not in context
    assert "Last agent" not in context


##Function purpose: Test build_complete_prompt without context
def test_build_complete_prompt_no_context():
    """##Function purpose: Verify build_complete_prompt works without identity or faction.."""
    ##Action purpose: Build prompt without context
    agent_prompt = "You are an AI assistant."
    result = build_complete_prompt(agent_prompt)

    ##Condition purpose: Verify prompt unchanged
    assert result == agent_prompt


##Function purpose: Test build_complete_prompt with identity
def test_build_complete_prompt_with_identity():
    """##Function purpose: Verify build_complete_prompt adds identity context.."""
    ##Action purpose: Create identity
    scan = scan_system()
    identity = create_identity("orphic", scan)

    ##Action purpose: Build prompt with identity
    agent_prompt = "You are an AI assistant."
    result = build_complete_prompt(agent_prompt, identity=identity)

    ##Condition purpose: Verify prompt extended
    assert len(result) > len(agent_prompt)
    assert "SYSTEM IDENTITY" in result
    assert identity.username in result


##Function purpose: Test build_complete_prompt with faction
def test_build_complete_prompt_with_faction():
    """##Function purpose: Verify build_complete_prompt applies faction modifiers.."""
    ##Action purpose: Build prompt with faction
    agent_prompt = "You are an AI assistant."
    result = build_complete_prompt(agent_prompt, faction_name="orphic")

    ##Condition purpose: Verify prompt extended with faction modifiers
    assert len(result) > len(agent_prompt)
    assert "FACTION PROTOCOL" in result
    assert "The Orphics" in result


##Function purpose: Test build_complete_prompt with both
def test_build_complete_prompt_with_both():
    """##Function purpose: Verify build_complete_prompt combines identity and faction.."""
    ##Action purpose: Create identity
    scan = scan_system()
    identity = create_identity("revanchist", scan)

    ##Action purpose: Build prompt with both
    agent_prompt = "You are an AI assistant."
    result = build_complete_prompt(agent_prompt, identity=identity, faction_name="revanchist")

    ##Condition purpose: Verify both added
    assert "SYSTEM IDENTITY" in result
    assert "FACTION PROTOCOL" in result
    assert identity.username in result
    assert "The Revanchists" in result


##Function purpose: Test build_complete_prompt invalid faction
def test_build_complete_prompt_invalid_faction():
    """##Function purpose: Verify build_complete_prompt handles invalid faction gracefully.."""
    ##Action purpose: Build prompt with invalid faction
    agent_prompt = "You are an AI assistant."
    result = build_complete_prompt(agent_prompt, faction_name="nonexistent")

    ##Condition purpose: Verify prompt unchanged (faction not found)
    assert result == agent_prompt


##Function purpose: Test build_agent_prompt_from_key daedelus
def test_build_agent_prompt_from_key_daedelus():
    """##Function purpose: Verify build_agent_prompt_from_key works with daedelus domain.."""
    ##Action purpose: Mock get_agent function
    mock_agent = MagicMock()
    mock_agent.full_prompt = "Base prompt + Activation prompt"

    with patch("logos.core.prompts.get_agent", return_value=mock_agent):
        with patch("logos.daedelus.agents.get_agent", return_value=mock_agent):
            ##Action purpose: Create identity
            scan = scan_system()
            identity = create_identity("orphic", scan)

            ##Action purpose: Build prompt from key
            result = build_agent_prompt_from_key("A1", "daedelus", identity)

            ##Condition purpose: Verify prompt built
            assert result is not None
            assert "Base prompt" in result


##Function purpose: Test build_agent_prompt_from_key deus
def test_build_agent_prompt_from_key_deus():
    """##Function purpose: Verify build_agent_prompt_from_key works with deus domain.."""
    ##Action purpose: Mock get_agent function
    mock_agent = MagicMock()
    mock_agent.full_prompt = "Base prompt + Activation prompt"

    with patch("logos.core.prompts.get_agent", return_value=mock_agent):
        with patch("logos.deus.agents.get_agent", return_value=mock_agent):
            ##Action purpose: Create identity
            scan = scan_system()
            identity = create_identity("technomancer", scan)

            ##Action purpose: Build prompt from key
            result = build_agent_prompt_from_key("A1", "deus", identity)

            ##Condition purpose: Verify prompt built
            assert result is not None
            assert "Base prompt" in result


##Function purpose: Test build_agent_prompt_from_key invalid domain
def test_build_agent_prompt_from_key_invalid_domain():
    """##Function purpose: Verify build_agent_prompt_from_key returns None for invalid domain.."""
    ##Action purpose: Build prompt with invalid domain
    result = build_agent_prompt_from_key("A1", "invalid", None)

    ##Condition purpose: Verify returns None
    assert result is None


##Function purpose: Test build_agent_prompt_from_key agent not found
def test_build_agent_prompt_from_key_agent_not_found():
    """##Function purpose: Verify build_agent_prompt_from_key returns None when agent not found.."""
    ##Action purpose: Mock get_agent to return None
    with patch("logos.daedelus.agents.get_agent", return_value=None):
        ##Action purpose: Build prompt from key
        result = build_agent_prompt_from_key("INVALID", "daedelus", None)

        ##Condition purpose: Verify returns None
        assert result is None


##Function purpose: Test build_agent_prompt_from_key without identity
def test_build_agent_prompt_from_key_no_identity():
    """##Function purpose: Verify build_agent_prompt_from_key works without identity.."""
    ##Action purpose: Mock get_agent function
    mock_agent = MagicMock()
    mock_agent.full_prompt = "Base prompt + Activation prompt"

    with patch("logos.daedelus.agents.get_agent", return_value=mock_agent):
        ##Action purpose: Build prompt without identity
        result = build_agent_prompt_from_key("A1", "daedelus", None)

        ##Condition purpose: Verify prompt built without identity context
        assert result is not None
        assert "Base prompt" in result
        assert "SYSTEM IDENTITY" not in result
