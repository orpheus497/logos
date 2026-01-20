"""
##Script function and purpose: Unit tests for logos.core.factions module.

Tests faction system including dataclass, FACTIONS dictionary, and modifier application.
"""

import pytest
from logos.core.factions import Faction, FACTIONS, apply_faction_modifiers


##Function purpose: Test FACTIONS dictionary completeness
def test_factions_dictionary():
    """
    ##Function purpose: Verify all 5 factions are defined in FACTIONS dictionary.
    """
    ##Condition purpose: Verify all expected factions exist
    expected_factions = ['daedelus', 'deus', 'revanchist', 'orphic', 'technomancer']
    
    ##Loop purpose: Check each expected faction
    for faction_name in expected_factions:
        assert faction_name in FACTIONS
        assert isinstance(FACTIONS[faction_name], Faction)


##Function purpose: Test Faction dataclass attributes
def test_faction_attributes():
    """
    ##Function purpose: Verify Faction dataclass has all required attributes.
    """
    ##Action purpose: Get a faction
    orphic = FACTIONS['orphic']
    
    ##Condition purpose: Verify all attributes exist
    assert hasattr(orphic, 'name')
    assert hasattr(orphic, 'philosophy')
    assert hasattr(orphic, 'autonomy_level')
    assert hasattr(orphic, 'modifiers')
    
    ##Condition purpose: Verify attribute types
    assert isinstance(orphic.name, str)
    assert isinstance(orphic.philosophy, str)
    assert isinstance(orphic.autonomy_level, str)
    assert isinstance(orphic.modifiers, dict)


##Function purpose: Test baseline factions have no modifiers
def test_baseline_factions():
    """
    ##Function purpose: Verify baseline factions (daedelus, deus) have no modifiers.
    """
    ##Condition purpose: Verify daedelus has no modifiers
    assert len(FACTIONS['daedelus'].modifiers) == 0
    
    ##Condition purpose: Verify deus has no modifiers
    assert len(FACTIONS['deus'].modifiers) == 0


##Function purpose: Test modifier factions
def test_modifier_factions():
    """
    ##Function purpose: Verify modifier factions have modifiers defined.
    """
    ##Condition purpose: Verify revanchist has modifiers
    assert len(FACTIONS['revanchist'].modifiers) > 0
    
    ##Condition purpose: Verify orphic has modifiers
    assert len(FACTIONS['orphic'].modifiers) > 0
    
    ##Condition purpose: Verify technomancer has modifiers
    assert len(FACTIONS['technomancer'].modifiers) > 0


##Function purpose: Test apply_faction_modifiers with baseline
def test_apply_faction_modifiers_baseline():
    """
    ##Function purpose: Verify baseline factions return unchanged prompt.
    """
    ##Action purpose: Create base prompt
    base_prompt = "You are an AI assistant."
    
    ##Action purpose: Apply daedelus faction (no modifiers)
    result = apply_faction_modifiers(base_prompt, FACTIONS['daedelus'])
    
    ##Condition purpose: Verify prompt unchanged
    assert result == base_prompt
    
    ##Action purpose: Apply deus faction (no modifiers)
    result = apply_faction_modifiers(base_prompt, FACTIONS['deus'])
    
    ##Condition purpose: Verify prompt unchanged
    assert result == base_prompt


##Function purpose: Test apply_faction_modifiers with modifiers
def test_apply_faction_modifiers_with_modifiers():
    """
    ##Function purpose: Verify modifier factions append protocol block.
    """
    ##Action purpose: Create base prompt
    base_prompt = "You are an AI assistant."
    
    ##Action purpose: Apply orphic faction (has modifiers)
    result = apply_faction_modifiers(base_prompt, FACTIONS['orphic'])
    
    ##Condition purpose: Verify prompt is extended
    assert len(result) > len(base_prompt)
    assert "FACTION PROTOCOL" in result
    assert "The Orphics" in result
    assert "Philosophy" in result
    assert "Autonomy Level" in result
    assert "Behavioral Modifiers" in result


##Function purpose: Test modifier formatting
def test_modifier_formatting():
    """
    ##Function purpose: Verify modifiers are formatted correctly in output.
    """
    ##Action purpose: Apply revanchist faction
    base_prompt = "Test"
    result = apply_faction_modifiers(base_prompt, FACTIONS['revanchist'])
    
    ##Condition purpose: Verify all modifiers are included
    for key in FACTIONS['revanchist'].modifiers.keys():
        assert key in result
    
    ##Condition purpose: Verify markdown bullet format
    assert "- " in result


##Function purpose: Test autonomy levels
def test_autonomy_levels():
    """
    ##Function purpose: Verify all factions have valid autonomy levels.
    """
    ##Action purpose: Valid autonomy levels
    valid_levels = ['minimal', 'balanced', 'maximum']
    
    ##Loop purpose: Check each faction
    for faction in FACTIONS.values():
        ##Condition purpose: Verify autonomy level is valid
        assert faction.autonomy_level in valid_levels
