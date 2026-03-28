"""
##Script function and purpose: CLI argument parsing.

Provides command-line argument parsing for LOGOS CLI flags including
verbose/quiet modes and version display.
Phase 5 implementation.

##Action purpose: Parses command-line arguments to configure CLI behavior
such as verbosity level, enabling users to control output detail via -v/-q flags.
"""

import argparse
from typing import Final

##Action purpose: Valid verbosity levels
VERBOSITY_QUIET: Final[str] = "quiet"
VERBOSITY_NORMAL: Final[str] = "normal"
VERBOSITY_VERBOSE: Final[str] = "verbose"

##Action purpose: Module-level verbosity state (set once by parse_args at CLI startup, read by get_verbosity)
##Note: parse_args() should only be called once per execution from main(). Tests may call
##it multiple times to reset state.
_current_verbosity: str = VERBOSITY_NORMAL


##Function purpose: Parse CLI arguments and return namespace
def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """
    Parses command-line arguments for LOGOS.

    Supports -v/--verbose and -q/--quiet flags for controlling output
    verbosity, plus --version for version display. When neither flag
    is provided, falls back to the verbosity setting in config.yaml.

    Args:
        argv: Argument list (defaults to sys.argv[1:] if None)

    Returns:
        Parsed argument namespace
    """
    parser = argparse.ArgumentParser(
        prog="logos",
        description="LOGOS — Unified AI Agent Federation CLI",
        add_help=True,
    )

    ##Action purpose: Create mutually exclusive verbosity group
    verbosity_group = parser.add_mutually_exclusive_group()
    verbosity_group.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=False,
        help="Enable verbose output (show detailed agent info, prompt stats, and system details)",
    )
    verbosity_group.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        default=False,
        help="Enable quiet output (minimal output, suppress banners and decorative elements)",
    )

    parser.add_argument(
        "--version",
        action="store_true",
        default=False,
        help="Show LOGOS version and exit",
    )

    parser.add_argument(
        "agent",
        nargs="?",
        default=None,
        help="Agent key or alias to invoke directly (e.g., A1, architect, kernel)",
    )

    args = parser.parse_args(argv)

    ##Action purpose: Set module-level verbosity based on parsed flags
    global _current_verbosity
    if args.verbose:
        _current_verbosity = VERBOSITY_VERBOSE
    elif args.quiet:
        _current_verbosity = VERBOSITY_QUIET
    else:
        ##Action purpose: Fall back to config verbosity when no CLI flag provided
        _current_verbosity = _get_config_verbosity()

    return args


##Function purpose: Read verbosity default from user config
def _get_config_verbosity() -> str:
    """
    Reads the default verbosity level from user config.

    Falls back to "normal" if the config value is missing or invalid.

    Returns:
        Verbosity level string ("quiet", "normal", or "verbose")
    """
    try:
        from logos.core.config import get_config_value, load_config

        config = load_config()
        value = get_config_value(config, "verbosity", VERBOSITY_NORMAL)
        if value in (VERBOSITY_QUIET, VERBOSITY_NORMAL, VERBOSITY_VERBOSE):
            return value
    except (ImportError, OSError, ValueError, KeyError, TypeError):
        pass
    return VERBOSITY_NORMAL


##Function purpose: Get current verbosity level
def get_verbosity() -> str:
    """
    Returns the current verbosity level.

    Returns one of: "quiet", "normal", or "verbose".
    Defaults to "normal" if parse_args has not been called.

    Returns:
        Verbosity level string
    """
    return _current_verbosity


##Function purpose: Check if output should be shown at current verbosity
def is_verbose() -> bool:
    """
    Returns True if verbose mode is active.

    Returns:
        True if verbosity is "verbose"
    """
    return _current_verbosity == VERBOSITY_VERBOSE


##Function purpose: Check if quiet mode is active
def is_quiet() -> bool:
    """
    Returns True if quiet mode is active.

    Returns:
        True if verbosity is "quiet"
    """
    return _current_verbosity == VERBOSITY_QUIET
