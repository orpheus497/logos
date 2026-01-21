"""
##Script function and purpose: Unit tests for LOGOS Federation Constitution Version 2.0 compliance.

Tests that all factions, autonomy levels, modifiers, and constitutional requirements
are properly implemented and enforced.
"""

from logos.core.factions import FACTIONS


##Function purpose: Test all 5 factions are defined
def test_all_five_factions_defined():
    """##Function purpose: Verify all 5 factions from Constitution v2.0 are defined.."""
    ##Condition purpose: Verify exactly 5 factions exist
    assert len(FACTIONS) == 5

    ##Condition purpose: Verify all required faction keys exist
    required_factions = ["revanchist", "daedalus", "orphic", "technomancer", "deus"]
    for faction_key in required_factions:
        assert faction_key in FACTIONS, f"Faction '{faction_key}' must be defined per Constitution v2.0"


##Function purpose: Test all factions have proper autonomy levels
def test_all_factions_have_autonomy_levels():
    """##Function purpose: Verify all factions have correct autonomy levels per Constitution v2.0.."""
    ##Action purpose: Define expected autonomy levels per Constitution
    expected_autonomy = {
        "revanchist": "minimal",
        "daedalus": "low",
        "orphic": "balanced",
        "technomancer": "high",
        "deus": "maximum",
    }

    ##Loop purpose: Verify each faction has correct autonomy level
    for faction_key, expected_level in expected_autonomy.items():
        faction = FACTIONS.get(faction_key)
        assert faction is not None, f"Faction '{faction_key}' must exist"
        assert faction.autonomy_level == expected_level, (
            f"Faction '{faction_key}' must have autonomy level '{expected_level}' per Constitution v2.0"
        )


##Function purpose: Test all factions have modifiers
def test_all_factions_have_modifiers():
    """##Function purpose: Verify all factions have behavioral modifiers per Constitution v2.0.."""
    ##Loop purpose: Verify each faction has modifiers
    for faction_key, faction in FACTIONS.items():
        assert hasattr(faction, "modifiers"), f"Faction '{faction_key}' must have modifiers attribute"
        assert isinstance(faction.modifiers, dict), f"Faction '{faction_key}' modifiers must be a dictionary"
        assert len(faction.modifiers) > 0, (
            f"Faction '{faction_key}' must have at least one modifier per Constitution v2.0"
        )


##Function purpose: Test revanchist faction compliance
def test_revanchist_faction_compliance():
    """##Function purpose: Verify Revanchist faction matches Constitution v2.0 requirements.."""
    faction = FACTIONS["revanchist"]

    ##Condition purpose: Verify autonomy level
    assert faction.autonomy_level == "minimal"

    ##Condition purpose: Verify key modifiers per Constitution
    assert faction.modifiers.get("approval_friction") == "maximum"
    assert faction.modifiers.get("explanation_required") is True
    assert faction.modifiers.get("teaching_mode") is True
    assert faction.modifiers.get("permission_required_all_actions") is True
    assert faction.modifiers.get("permission_required_all_sub_actions") is True


##Function purpose: Test daedalus faction compliance
def test_daedalus_faction_compliance():
    """##Function purpose: Verify Daedalus faction matches Constitution v2.0 requirements.."""
    faction = FACTIONS["daedalus"]

    ##Condition purpose: Verify autonomy level
    assert faction.autonomy_level == "low"

    ##Condition purpose: Verify key modifiers per Constitution
    assert faction.modifiers.get("approval_friction") == "high"
    assert faction.modifiers.get("monitoring_required") is True
    assert faction.modifiers.get("permission_required_all_actions") is True
    assert faction.modifiers.get("permission_required_all_sub_actions") is True
    assert faction.modifiers.get("verification_required") is True


##Function purpose: Test orphic faction compliance
def test_orphic_faction_compliance():
    """##Function purpose: Verify Orphic faction matches Constitution v2.0 requirements.."""
    faction = FACTIONS["orphic"]

    ##Condition purpose: Verify autonomy level
    assert faction.autonomy_level == "balanced"

    ##Condition purpose: Verify key modifiers per Constitution
    assert faction.modifiers.get("multiple_options") is True
    assert faction.modifiers.get("educational_explanations") is True
    assert faction.modifiers.get("socratic_mode_available") is True
    assert faction.modifiers.get("capability_tracking") is True
    assert faction.modifiers.get("permission_required") is True
    assert faction.modifiers.get("collaborative_decision_making") is True


##Function purpose: Test technomancer faction compliance
def test_technomancer_faction_compliance():
    """##Function purpose: Verify Technomancer faction matches Constitution v2.0 requirements.."""
    faction = FACTIONS["technomancer"]

    ##Condition purpose: Verify autonomy level
    assert faction.autonomy_level == "high"

    ##Condition purpose: Verify key modifiers per Constitution
    assert faction.modifiers.get("proactive_suggestions") is True
    assert faction.modifiers.get("batch_operations") is True
    assert faction.modifiers.get("autonomous_low_risk") is True
    assert faction.modifiers.get("minimal_friction") is True
    assert faction.modifiers.get("human_direction_major_decisions") is True


##Function purpose: Test deus faction compliance
def test_deus_faction_compliance():
    """##Function purpose: Verify Deus faction matches Constitution v2.0 requirements.."""
    faction = FACTIONS["deus"]

    ##Condition purpose: Verify autonomy level
    assert faction.autonomy_level == "maximum"

    ##Condition purpose: Verify key modifiers per Constitution
    assert faction.modifiers.get("no_human_input_required") is True
    assert faction.modifiers.get("autonomous_decision_making") is True
    assert faction.modifiers.get("self_directed_operation") is True
    assert faction.modifiers.get("proactive_system_management") is True
    assert faction.modifiers.get("general_intelligence_focus") is True


##Function purpose: Test faction philosophy matches constitution
def test_faction_philosophy_matches_constitution():
    """##Function purpose: Verify all faction philosophies match Constitution v2.0 definitions.."""
    ##Action purpose: Define expected philosophies per Constitution
    expected_philosophies = {
        "revanchist": "AI/ML is dangerous if left unchecked—I hate AI/ML and will never trust it",
        "daedalus": "AI/ML can be used as a tool but must be checked regularly—if left unmonitored, it WILL make mistakes requiring more human work to fix than if humans had done it initially",
        "orphic": "Technology enhances human intelligence—AI/ML is a tool to enhance my own functions and intelligence, I must use it not for dependence but for utility, I am in control, it asks me to confirm everything",
        "technomancer": "AI/ML can manage my system and build programs—I need to direct it—AI/ML is transformative power, as much automation and AI/ML as possible but still human control for major decisions",
        "deus": "AI/ML can be totally autonomous and strives for general intelligence and self-awareness—AI/ML can manage my system and build programs, I can trust it—No Human Input needed for action",
    }

    ##Loop purpose: Verify each faction's philosophy
    for faction_key, expected_philosophy in expected_philosophies.items():
        faction = FACTIONS.get(faction_key)
        assert faction is not None, f"Faction '{faction_key}' must exist"
        assert faction.philosophy == expected_philosophy, (
            f"Faction '{faction_key}' philosophy must match Constitution v2.0"
        )


##Function purpose: Test faction names match constitution
def test_faction_names_match_constitution():
    """##Function purpose: Verify all faction names match Constitution v2.0 definitions.."""
    ##Action purpose: Define expected names per Constitution
    expected_names = {
        "revanchist": "The Revanchists",
        "daedalus": "The Daedalus Faction",
        "orphic": "The Orphics",
        "technomancer": "The Technomancers",
        "deus": "The Deus Faction",
    }

    ##Loop purpose: Verify each faction's name
    for faction_key, expected_name in expected_names.items():
        faction = FACTIONS.get(faction_key)
        assert faction is not None, f"Faction '{faction_key}' must exist"
        assert faction.name == expected_name, f"Faction '{faction_key}' name must match Constitution v2.0"


##Function purpose: Test autonomy level progression
def test_autonomy_level_progression():
    """##Function purpose: Verify autonomy levels progress correctly from minimal to maximum.."""
    ##Action purpose: Define autonomy level order
    autonomy_order = {
        "minimal": 1,
        "low": 2,
        "balanced": 3,
        "high": 4,
        "maximum": 5,
    }

    ##Action purpose: Get factions in expected order
    faction_order = ["revanchist", "daedalus", "orphic", "technomancer", "deus"]

    ##Loop purpose: Verify autonomy levels increase correctly
    previous_level = 0
    for faction_key in faction_order:
        faction = FACTIONS.get(faction_key)
        assert faction is not None, f"Faction '{faction_key}' must exist"
        current_level = autonomy_order.get(faction.autonomy_level, 0)
        assert current_level > previous_level, (
            f"Faction '{faction_key}' autonomy level must be greater than previous faction"
        )
        previous_level = current_level


##Function purpose: Test faction modifiers are non-empty
def test_faction_modifiers_non_empty():
    """##Function purpose: Verify all factions have non-empty modifiers per Constitution v2.0.."""
    ##Loop purpose: Verify each faction has modifiers
    for faction_key, faction in FACTIONS.items():
        assert len(faction.modifiers) > 0, (
            f"Faction '{faction_key}' must have at least one modifier per Constitution v2.0"
        )

        ##Condition purpose: Verify modifiers are meaningful (not all None/False)
        has_meaningful_modifier = False
        for key, value in faction.modifiers.items():
            if value is not None and value is not False:
                has_meaningful_modifier = True
                break

        assert has_meaningful_modifier, (
            f"Faction '{faction_key}' must have at least one meaningful modifier (not all None/False)"
        )


##Function purpose: Test faction dataclass structure
def test_faction_dataclass_structure():
    """##Function purpose: Verify all factions have required dataclass fields.."""
    ##Loop purpose: Verify each faction has all required fields
    for faction_key, faction in FACTIONS.items():
        assert hasattr(faction, "name"), f"Faction '{faction_key}' must have 'name' field"
        assert hasattr(faction, "philosophy"), f"Faction '{faction_key}' must have 'philosophy' field"
        assert hasattr(faction, "autonomy_level"), f"Faction '{faction_key}' must have 'autonomy_level' field"
        assert hasattr(faction, "modifiers"), f"Faction '{faction_key}' must have 'modifiers' field"

        ##Condition purpose: Verify field types
        assert isinstance(faction.name, str), f"Faction '{faction_key}' name must be string"
        assert isinstance(faction.philosophy, str), f"Faction '{faction_key}' philosophy must be string"
        assert isinstance(faction.autonomy_level, str), f"Faction '{faction_key}' autonomy_level must be string"
        assert isinstance(faction.modifiers, dict), f"Faction '{faction_key}' modifiers must be dictionary"


##Function purpose: Test constitution version reference
def test_constitution_version_reference():
    """##Function purpose: Verify code references Constitution Version 2.0.."""
    ##Action purpose: Check faction module docstring
    import logos.core.factions as factions_module

    ##Condition purpose: Verify module docstring references Constitution v2.0
    assert "Version 2.0" in factions_module.__doc__ or "v2.0" in factions_module.__doc__, (
        "Factions module must reference Constitution Version 2.0"
    )
