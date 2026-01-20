"""
##Script function and purpose: Unit tests for logos.cli.mode_select module.

Tests mode selection functionality including input validation.
"""

import pytest
from unittest.mock import patch
from logos.cli.mode_select import select_mode


##Function purpose: Test select_mode valid input
def test_select_mode_valid_input():
    """
    ##Function purpose: Verify select_mode accepts valid input.
    """
    ##Action purpose: Test with valid input 'D'
    with patch('builtins.input', return_value='D'):
        result = select_mode()
        assert result == "daedelus"
    
    ##Action purpose: Test with valid input 'U'
    with patch('builtins.input', return_value='U'):
        result = select_mode()
        assert result == "deus"


##Function purpose: Test select_mode invalid input
def test_select_mode_invalid_input():
    """
    ##Function purpose: Verify select_mode handles invalid input and prompts again.
    """
    ##Action purpose: Test with invalid input, then valid input
    with patch('builtins.input', side_effect=['invalid', 'X', 'D']):
        result = select_mode()
        ##Condition purpose: Verify eventually accepts valid input
        assert result == "daedelus"


##Function purpose: Test select_mode cancellation
def test_select_mode_cancellation():
    """
    ##Function purpose: Verify select_mode allows cancellation.
    """
    ##Action purpose: Test with quit input
    with patch('builtins.input', return_value='Q'):
        result = select_mode()
        ##Condition purpose: Verify returns None on cancellation
        assert result is None


##Function purpose: Test select_mode input validation length
def test_select_mode_input_validation_length():
    """
    ##Function purpose: Verify select_mode validates input length.
    """
    ##Action purpose: Test with input that's too long
    long_input = "a" * 100
    with patch('builtins.input', side_effect=[long_input, 'D']):
        result = select_mode()
        ##Condition purpose: Verify rejects long input, accepts valid input
        assert result == "daedelus"


##Function purpose: Test select_mode input validation control characters
def test_select_mode_input_validation_control_chars():
    """
    ##Function purpose: Verify select_mode rejects control characters.
    """
    ##Action purpose: Test with control characters
    with patch('builtins.input', side_effect=['\x00\x01', 'D']):
        result = select_mode()
        ##Condition purpose: Verify rejects control chars, accepts valid input
        assert result == "daedelus"


##Function purpose: Test select_mode input validation whitelist
def test_select_mode_input_validation_whitelist():
    """
    ##Function purpose: Verify select_mode enforces character whitelist.
    """
    ##Action purpose: Test with disallowed characters
    with patch('builtins.input', side_effect=['abc', 'xyz', 'D']):
        result = select_mode()
        ##Condition purpose: Verify rejects disallowed chars, accepts valid input
        assert result == "daedelus"


##Function purpose: Test select_mode keyboard interrupt
def test_select_mode_keyboard_interrupt():
    """
    ##Function purpose: Verify select_mode handles KeyboardInterrupt gracefully.
    """
    ##Action purpose: Test with KeyboardInterrupt
    with patch('builtins.input', side_effect=KeyboardInterrupt()):
        result = select_mode()
        ##Condition purpose: Verify returns None on interrupt
        assert result is None
