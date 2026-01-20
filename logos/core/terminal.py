"""
##Script function and purpose: Shared terminal utilities.

Terminal operations (screen clearing, colors, etc.) used by both domains.
Uses ANSI escape codes for cross-platform compatibility without shell execution risk.

##Action purpose: Addresses shell injection risk (P0-003) by using ANSI escape codes
instead of os.system() calls.
"""


def clear_screen() -> None:
    """
    ##Function purpose: Clear the terminal screen using ANSI escape codes.

    ##Action purpose: Uses ANSI escape sequences for cross-platform compatibility
    without shell execution risk.

    ##Step purpose:
    - ESC[2J clears the entire screen
    - ESC[H moves cursor to home position (top-left)
    """
    ##Action purpose: Print ANSI escape sequence to clear screen and reset cursor
    print("\033[2J\033[H", end="", flush=True)
