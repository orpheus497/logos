"""
##Script function and purpose: Unit tests for logos.core.factions module.

Tests faction system including dataclass, FACTIONS dictionary, and modifier application.
"""

from logos.core.factions import FACTIONS, Faction, apply_faction_modifiers


##Function purpose: Test FACTIONS dictionary completeness
def test_factions_dictionary():
    """##Function purpose: Verify all 5 factions are defined in FACTIONS dictionary.."""
    ##Condition purpose: Verify all expected factions exist (5 factions per Constitution v2.0)
    expected_factions = ["revanchist", "daedalus", "orphic", "technomancer", "deus"]

    ##Loop purpose: Check each expected faction
    for faction_name in expected_factions:
        assert faction_name in FACTIONS
        assert isinstance(FACTIONS[faction_name], Faction)


##Function purpose: Test Faction dataclass attributes
def test_faction_attributes():
    """##Function purpose: Verify Faction dataclass has all required attributes.."""
    ##Action purpose: Get a faction
    orphic = FACTIONS["orphic"]

    ##Condition purpose: Verify all attributes exist
    assert hasattr(orphic, "name")
    assert hasattr(orphic, "philosophy")
    assert hasattr(orphic, "autonomy_level")
    assert hasattr(orphic, "modifiers")

    ##Condition purpose: Verify attribute types
    assert isinstance(orphic.name, str)
    assert isinstance(orphic.philosophy, str)
    assert isinstance(orphic.autonomy_level, str)
    assert isinstance(orphic.modifiers, dict)


##Function purpose: Test all factions have modifiers
def test_all_factions_have_modifiers():
    """##Function purpose: Verify all factions have modifiers defined (per Constitution v2.0).."""
    ##Loop purpose: Check each faction has modifiers
    for faction_name, faction in FACTIONS.items():
        ##Condition purpose: Verify faction has modifiers (all 5 factions now have modifiers)
        assert len(faction.modifiers) > 0, f"Faction {faction_name} should have modifiers"


##Function purpose: Test specific faction modifiers
def test_specific_faction_modifiers():
    """##Function purpose: Verify specific factions have expected modifiers.."""
    ##Condition purpose: Verify revanchist has teaching mode
    assert "teaching_mode" in FACTIONS["revanchist"].modifiers
    assert FACTIONS["revanchist"].modifiers["teaching_mode"] is True

    ##Condition purpose: Verify daedalus has monitoring required
    assert "monitoring_required" in FACTIONS["daedalus"].modifiers
    assert FACTIONS["daedalus"].modifiers["monitoring_required"] is True

    ##Condition purpose: Verify orphic has multiple options
    assert "multiple_options" in FACTIONS["orphic"].modifiers
    assert FACTIONS["orphic"].modifiers["multiple_options"] is True

    ##Condition purpose: Verify technomancer has batch operations
    assert "batch_operations" in FACTIONS["technomancer"].modifiers
    assert FACTIONS["technomancer"].modifiers["batch_operations"] is True

    ##Condition purpose: Verify deus has no human input required
    assert "no_human_input_required" in FACTIONS["deus"].modifiers
    assert FACTIONS["deus"].modifiers["no_human_input_required"] is True


##Function purpose: Test apply_faction_modifiers with all factions
def test_apply_faction_modifiers_all_factions():
    """##Function purpose: Verify all factions append protocol block (all have modifiers now).."""
    ##Action purpose: Create base prompt
    base_prompt = "You are an AI assistant."

    ##Loop purpose: Test all factions append modifiers
    for faction_name, faction in FACTIONS.items():
        ##Action purpose: Apply faction
        result = apply_faction_modifiers(base_prompt, faction)

        ##Condition purpose: Verify prompt is extended with faction protocol
        assert len(result) > len(base_prompt)
        assert "FACTION PROTOCOL" in result
        assert faction.name in result
        assert "Philosophy" in result
        assert "Autonomy Level" in result
        assert "Behavioral Modifiers" in result


##Function purpose: Test apply_faction_modifiers with modifiers
def test_apply_faction_modifiers_with_modifiers():
    """##Function purpose: Verify modifier factions append protocol block.."""
    ##Action purpose: Create base prompt
    base_prompt = "You are an AI assistant."

    ##Action purpose: Apply orphic faction (has modifiers)
    result = apply_faction_modifiers(base_prompt, FACTIONS["orphic"])

    ##Condition purpose: Verify prompt is extended
    assert len(result) > len(base_prompt)
    assert "FACTION PROTOCOL" in result
    assert "The Orphics" in result
    assert "Philosophy" in result
    assert "Autonomy Level" in result
    assert "Behavioral Modifiers" in result


##Function purpose: Test modifier formatting
def test_modifier_formatting():
    """##Function purpose: Verify modifiers are formatted correctly in output.."""
    ##Action purpose: Apply revanchist faction
    base_prompt = "Test"
    result = apply_faction_modifiers(base_prompt, FACTIONS["revanchist"])

    ##Condition purpose: Verify all modifiers are included
    for key in FACTIONS["revanchist"].modifiers.keys():
        assert key in result

    ##Condition purpose: Verify markdown bullet format
    assert "- " in result


##Function purpose: Test autonomy levels
def test_autonomy_levels():
    """##Function purpose: Verify all factions have valid autonomy levels (per Constitution v2.0).."""
    ##Action purpose: Valid autonomy levels (5 levels: minimal, low, balanced, high, maximum)
    valid_levels = ["minimal", "low", "balanced", "high", "maximum"]

    ##Loop purpose: Check each faction
    for faction_name, faction in FACTIONS.values():
        ##Condition purpose: Verify autonomy level is valid
        assert faction.autonomy_level in valid_levels, (
            f"Faction {faction_name} has invalid autonomy level: {faction.autonomy_level}"
        )

    ##Condition purpose: Verify specific autonomy levels match Constitution
    assert FACTIONS["revanchist"].autonomy_level == "minimal"
    assert FACTIONS["daedalus"].autonomy_level == "low"
    assert FACTIONS["orphic"].autonomy_level == "balanced"
    assert FACTIONS["technomancer"].autonomy_level == "high"
    assert FACTIONS["deus"].autonomy_level == "maximum"
