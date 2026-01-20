"""
##Script function and purpose: Unit tests for logos.core.terminal module.

Tests terminal utility functions including screen clearing.
"""

import sys
from io import StringIO

from logos.core.terminal import clear_screen


##Function purpose: Test clear_screen output
def test_clear_screen():
    """##Function purpose: Verify clear_screen outputs correct ANSI escape codes.."""
    ##Action purpose: Capture stdout
    captured_output = StringIO()
    original_stdout = sys.stdout

    try:
        sys.stdout = captured_output

        ##Action purpose: Call clear_screen
        clear_screen()

        ##Action purpose: Get output
        output = captured_output.getvalue()

        ##Condition purpose: Verify ANSI escape sequence is present
        assert "\033[2J" in output or "\x1b[2J" in output
    finally:
        ##Action purpose: Restore stdout
        sys.stdout = original_stdout
