"""
##Script function and purpose: Unit tests for logos.cli.first_run module.

Tests first-run wizard functionality including input validation.
"""

from unittest.mock import patch

from logos.cli.first_run import get_faction_options, select_faction


##Function purpose: Test get_faction_options
def test_get_faction_options():
    """##Function purpose: Verify get_faction_options returns correct options.."""
    ##Action purpose: Get faction options
    options = get_faction_options()

    ##Condition purpose: Verify options structure
    assert isinstance(options, list)
    assert len(options) == 3  # revanchist, orphic, technomancer

    ##Condition purpose: Verify each option is a tuple
    for option in options:
        assert isinstance(option, tuple)
        assert len(option) == 3  # (key, name, description)


##Function purpose: Test select_faction valid input
def test_select_faction_valid_input():
    """##Function purpose: Verify select_faction accepts valid input.."""
    ##Action purpose: Test with valid input 'r'
    with patch("builtins.input", return_value="r"):
        result = select_faction()
        assert result == "revanchist"

    ##Action purpose: Test with valid input 'o'
    with patch("builtins.input", return_value="o"):
        result = select_faction()
        assert result == "orphic"

    ##Action purpose: Test with valid input 't'
    with patch("builtins.input", return_value="t"):
        result = select_faction()
        assert result == "technomancer"


##Function purpose: Test select_faction invalid input
def test_select_faction_invalid_input():
    """##Function purpose: Verify select_faction handles invalid input and prompts again.."""
    ##Action purpose: Test with invalid input, then valid input
    with patch("builtins.input", side_effect=["invalid", "x", "r"]):
        result = select_faction()
        ##Condition purpose: Verify eventually accepts valid input
        assert result == "revanchist"


##Function purpose: Test select_faction cancellation
def test_select_faction_cancellation():
    """##Function purpose: Verify select_faction allows cancellation.."""
    ##Action purpose: Test with quit input
    with patch("builtins.input", return_value="q"):
        result = select_faction()
        ##Condition purpose: Verify returns None on cancellation
        assert result is None


##Function purpose: Test select_faction input validation length
def test_select_faction_input_validation_length():
    """##Function purpose: Verify select_faction validates input length.."""
    ##Action purpose: Test with input that's too long
    long_input = "a" * 100
    with patch("builtins.input", side_effect=[long_input, "r"]):
        result = select_faction()
        ##Condition purpose: Verify rejects long input, accepts valid input
        assert result == "revanchist"


##Function purpose: Test select_faction input validation control characters
def test_select_faction_input_validation_control_chars():
    """##Function purpose: Verify select_faction rejects control characters.."""
    ##Action purpose: Test with control characters
    with patch("builtins.input", side_effect=["\x00\x01", "r"]):
        result = select_faction()
        ##Condition purpose: Verify rejects control chars, accepts valid input
        assert result == "revanchist"


##Function purpose: Test select_faction input validation whitelist
def test_select_faction_input_validation_whitelist():
    """##Function purpose: Verify select_faction enforces character whitelist.."""
    ##Action purpose: Test with disallowed characters
    with patch("builtins.input", side_effect=["abc", "xyz", "r"]):
        result = select_faction()
        ##Condition purpose: Verify rejects disallowed chars, accepts valid input
        assert result == "revanchist"


##Function purpose: Test select_faction keyboard interrupt
def test_select_faction_keyboard_interrupt():
    """##Function purpose: Verify select_faction handles KeyboardInterrupt gracefully.."""
    ##Action purpose: Test with KeyboardInterrupt
    with patch("builtins.input", side_effect=KeyboardInterrupt()):
        result = select_faction()
        ##Condition purpose: Verify returns None on interrupt
        assert result is None
