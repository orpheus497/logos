"""
##Script function and purpose: Unit tests for logos.cli.mode_select module.

Tests mode selection functionality including input validation, faction change,
and system information display.
"""

from unittest.mock import patch

from logos.cli.mode_select import (
    change_faction,
    display_faction_selection_menu,
    select_faction_for_change,
    select_mode,
)
from logos.core.identity import SystemIdentity


##Function purpose: Test select_mode valid input
def test_select_mode_valid_input():
    """##Function purpose: Verify select_mode accepts valid input.."""
    ##Action purpose: Test with valid input 'D'
    with patch("builtins.input", return_value="D"):
        result = select_mode()
        assert result == "daedelus"

    ##Action purpose: Test with valid input 'U'
    with patch("builtins.input", return_value="U"):
        result = select_mode()
        assert result == "deus"


##Function purpose: Test select_mode invalid input
def test_select_mode_invalid_input():
    """##Function purpose: Verify select_mode handles invalid input and prompts again.."""
    ##Action purpose: Test with invalid input, then valid input
    with patch("builtins.input", side_effect=["invalid", "X", "D"]):
        result = select_mode()
        ##Condition purpose: Verify eventually accepts valid input
        assert result == "daedelus"


##Function purpose: Test select_mode cancellation
def test_select_mode_cancellation():
    """##Function purpose: Verify select_mode allows cancellation.."""
    ##Action purpose: Test with quit input
    with patch("builtins.input", return_value="Q"):
        result = select_mode()
        ##Condition purpose: Verify returns None on cancellation
        assert result is None


##Function purpose: Test select_mode input validation length
def test_select_mode_input_validation_length():
    """##Function purpose: Verify select_mode validates input length.."""
    ##Action purpose: Test with input that's too long
    long_input = "a" * 100
    with patch("builtins.input", side_effect=[long_input, "D"]):
        result = select_mode()
        ##Condition purpose: Verify rejects long input, accepts valid input
        assert result == "daedelus"


##Function purpose: Test select_mode input validation control characters
def test_select_mode_input_validation_control_chars():
    """##Function purpose: Verify select_mode rejects control characters.."""
    ##Action purpose: Test with control characters
    with patch("builtins.input", side_effect=["\x00\x01", "D"]):
        result = select_mode()
        ##Condition purpose: Verify rejects control chars, accepts valid input
        assert result == "daedelus"


##Function purpose: Test select_mode input validation whitelist
def test_select_mode_input_validation_whitelist():
    """##Function purpose: Verify select_mode enforces character whitelist.."""
    ##Action purpose: Test with disallowed characters
    with patch("builtins.input", side_effect=["abc", "xyz", "D"]):
        result = select_mode()
        ##Condition purpose: Verify rejects disallowed chars, accepts valid input
        assert result == "daedelus"


##Function purpose: Test select_mode keyboard interrupt
def test_select_mode_keyboard_interrupt():
    """##Function purpose: Verify select_mode handles KeyboardInterrupt gracefully.."""
    ##Action purpose: Test with KeyboardInterrupt
    with patch("builtins.input", side_effect=KeyboardInterrupt()):
        result = select_mode()
        ##Condition purpose: Verify returns None on interrupt
        assert result is None


##Function purpose: Test display_faction_selection_menu
def test_display_faction_selection_menu():
    """##Function purpose: Verify display_faction_selection_menu displays menu without errors.."""
    ##Action purpose: Capture stdout to verify menu display
    import sys
    from io import StringIO

    ##Action purpose: Redirect stdout
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        ##Action purpose: Display faction selection menu
        display_faction_selection_menu()

        ##Action purpose: Get output
        output = sys.stdout.getvalue()

        ##Condition purpose: Verify menu contains expected elements
        assert "CHANGE FACTION" in output
        assert "Select your new faction" in output
        assert "[Q] Cancel" in output or "[Q] Quit" in output
    finally:
        ##Action purpose: Restore stdout
        sys.stdout = old_stdout


##Function purpose: Test select_faction_for_change with all 5 factions
def test_select_faction_for_change_all_factions():
    """##Function purpose: Verify select_faction_for_change accepts all 5 faction selections.."""
    ##Action purpose: Test each faction with single letter input
    faction_tests = [
        ("r", "revanchist"),
        ("d", "daedalus"),
        ("o", "orphic"),
        ("t", "technomancer"),
        ("u", "deus"),
    ]

    ##Loop purpose: Test each faction
    for input_char, expected_faction in faction_tests:
        with patch("builtins.input", return_value=input_char):
            result = select_faction_for_change()
            ##Condition purpose: Verify correct faction returned
            assert result == expected_faction, f"Input '{input_char}' should return '{expected_faction}'"


##Function purpose: Test select_faction_for_change with full faction names
def test_select_faction_for_change_full_names():
    """##Function purpose: Verify select_faction_for_change accepts full faction names.."""
    ##Action purpose: Test with full faction name
    with patch("builtins.input", return_value="revanchist"):
        result = select_faction_for_change()
        ##Condition purpose: Verify correct faction returned
        assert result == "revanchist"

    ##Action purpose: Test with another full faction name
    with patch("builtins.input", return_value="orphic"):
        result = select_faction_for_change()
        ##Condition purpose: Verify correct faction returned
        assert result == "orphic"


##Function purpose: Test select_faction_for_change cancellation
def test_select_faction_for_change_cancellation():
    """##Function purpose: Verify select_faction_for_change allows cancellation.."""
    ##Action purpose: Test with quit input
    with patch("builtins.input", return_value="q"):
        result = select_faction_for_change()
        ##Condition purpose: Verify returns None on cancellation
        assert result is None

    ##Action purpose: Test with quit full word
    with patch("builtins.input", return_value="quit"):
        result = select_faction_for_change()
        ##Condition purpose: Verify returns None on cancellation
        assert result is None


##Function purpose: Test select_faction_for_change invalid input
def test_select_faction_for_change_invalid_input():
    """##Function purpose: Verify select_faction_for_change handles invalid input and prompts again.."""
    ##Action purpose: Test with invalid input, then valid input
    with patch("builtins.input", side_effect=["invalid", "x", "r"]):
        result = select_faction_for_change()
        ##Condition purpose: Verify eventually accepts valid input
        assert result == "revanchist"


##Function purpose: Test select_faction_for_change keyboard interrupt
def test_select_faction_for_change_keyboard_interrupt():
    """##Function purpose: Verify select_faction_for_change handles KeyboardInterrupt gracefully.."""
    ##Action purpose: Test with KeyboardInterrupt
    with patch("builtins.input", side_effect=KeyboardInterrupt()):
        result = select_faction_for_change()
        ##Condition purpose: Verify returns None on interrupt
        assert result is None


##Function purpose: Test change_faction successful change
def test_change_faction_successful_change():
    """##Function purpose: Verify change_faction successfully changes faction and saves identity.."""
    ##Action purpose: Create test identity
    identity = SystemIdentity(
        hostname="testhost",
        username="testuser",
        os_name="Linux",
        os_version="5.15.0",
        faction="revanchist",
        created_at="2026-01-20T12:00:00Z",
        last_session="2026-01-20T12:00:00Z",
    )

    ##Action purpose: Mock save_identity to return success
    with patch("logos.cli.mode_select.save_identity", return_value=True), \
         patch("logos.cli.mode_select.clear_screen"), \
         patch("builtins.input", return_value="o"), \
         patch("logos.cli.mode_select.display_faction_selection_menu"), \
         patch("logos.cli.mode_select.display_error"):
        ##Action purpose: Change faction
        result = change_faction(identity)

        ##Condition purpose: Verify faction changed
        assert result is not None
        assert result.faction == "orphic"
        ##Condition purpose: Verify save was called
        assert result is identity


##Function purpose: Test change_faction all 5 factions
def test_change_faction_all_factions():
    """##Function purpose: Verify change_faction works with all 5 factions.."""
    ##Action purpose: Test each faction change
    faction_tests = [
        ("revanchist", "r", "revanchist"),
        ("daedalus", "d", "daedalus"),
        ("orphic", "o", "orphic"),
        ("technomancer", "t", "technomancer"),
        ("deus", "u", "deus"),
    ]

    ##Loop purpose: Test each faction
    for initial_faction, input_char, expected_faction in faction_tests:
        ##Action purpose: Create test identity
        identity = SystemIdentity(
            hostname="testhost",
            username="testuser",
            os_name="Linux",
            os_version="5.15.0",
            faction=initial_faction,
            created_at="2026-01-20T12:00:00Z",
            last_session="2026-01-20T12:00:00Z",
        )

        ##Action purpose: Mock dependencies
        with patch("logos.cli.mode_select.save_identity", return_value=True), \
             patch("logos.cli.mode_select.clear_screen"), \
             patch("builtins.input", return_value=input_char), \
             patch("logos.cli.mode_select.display_faction_selection_menu"), \
             patch("logos.cli.mode_select.display_error"):
            ##Action purpose: Change faction
            result = change_faction(identity)

            ##Condition purpose: Verify faction changed correctly
            assert result is not None, f"Faction change from {initial_faction} to {expected_faction} should succeed"
            assert result.faction == expected_faction, f"Faction should be {expected_faction}"


##Function purpose: Test change_faction same faction check
def test_change_faction_same_faction():
    """##Function purpose: Verify change_faction detects same faction and returns unchanged identity.."""
    ##Action purpose: Create test identity
    identity = SystemIdentity(
        hostname="testhost",
        username="testuser",
        os_name="Linux",
        os_version="5.15.0",
        faction="orphic",
        created_at="2026-01-20T12:00:00Z",
        last_session="2026-01-20T12:00:00Z",
    )

    ##Action purpose: Mock dependencies
    with patch("logos.cli.mode_select.clear_screen"), \
         patch("builtins.input", return_value="o"), \
         patch("logos.cli.mode_select.display_faction_selection_menu"), \
         patch("logos.cli.mode_select.display_error"):
        ##Action purpose: Try to change to same faction
        result = change_faction(identity)

        ##Condition purpose: Verify identity returned unchanged
        assert result is not None
        assert result.faction == "orphic"
        ##Condition purpose: Verify same identity object returned
        assert result is identity


##Function purpose: Test change_faction cancellation
def test_change_faction_cancellation():
    """##Function purpose: Verify change_faction handles cancellation correctly.."""
    ##Action purpose: Create test identity
    identity = SystemIdentity(
        hostname="testhost",
        username="testuser",
        os_name="Linux",
        os_version="5.15.0",
        faction="orphic",
        created_at="2026-01-20T12:00:00Z",
        last_session="2026-01-20T12:00:00Z",
    )

    ##Action purpose: Mock dependencies
    with patch("logos.cli.mode_select.clear_screen"), \
         patch("builtins.input", return_value="q"), \
         patch("logos.cli.mode_select.display_faction_selection_menu"), \
         patch("logos.cli.mode_select.display_error"):
        ##Action purpose: Cancel faction change
        result = change_faction(identity)

        ##Condition purpose: Verify returns None on cancellation
        assert result is None


##Function purpose: Test change_faction save failure
def test_change_faction_save_failure():
    """##Function purpose: Verify change_faction handles save failure correctly.."""
    ##Action purpose: Create test identity
    identity = SystemIdentity(
        hostname="testhost",
        username="testuser",
        os_name="Linux",
        os_version="5.15.0",
        faction="orphic",
        created_at="2026-01-20T12:00:00Z",
        last_session="2026-01-20T12:00:00Z",
    )

    ##Action purpose: Mock dependencies with save failure
    with patch("logos.cli.mode_select.save_identity", return_value=False), \
         patch("logos.cli.mode_select.clear_screen"), \
         patch("builtins.input", return_value="r"), \
         patch("logos.cli.mode_select.display_faction_selection_menu"), \
         patch("logos.cli.mode_select.display_error") as mock_error:
        ##Action purpose: Attempt faction change
        result = change_faction(identity)

        ##Condition purpose: Verify returns None on save failure
        assert result is None
        ##Condition purpose: Verify error was displayed
        assert mock_error.called


##Function purpose: Test change_faction keyboard interrupt
def test_change_faction_keyboard_interrupt():
    """##Function purpose: Verify change_faction handles KeyboardInterrupt gracefully.."""
    ##Action purpose: Create test identity
    identity = SystemIdentity(
        hostname="testhost",
        username="testuser",
        os_name="Linux",
        os_version="5.15.0",
        faction="orphic",
        created_at="2026-01-20T12:00:00Z",
        last_session="2026-01-20T12:00:00Z",
    )

    ##Action purpose: Mock dependencies
    with patch("logos.cli.mode_select.clear_screen"), \
         patch("builtins.input", side_effect=KeyboardInterrupt()), \
         patch("logos.cli.mode_select.display_faction_selection_menu"), \
         patch("logos.cli.mode_select.display_error"):
        ##Action purpose: Handle interrupt
        result = change_faction(identity)

        ##Condition purpose: Verify returns None on interrupt
        assert result is None
