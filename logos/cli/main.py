"""
##Script function and purpose: Main CLI entry point.

Unified CLI that handles first-run, mode selection, and agent selection.
Phase 5 implementation.

##Action purpose: Orchestrates the complete LOGOS CLI workflow including first-run
detection, identity loading, mode selection, and agent selection with full integration
of identity, faction, and prompt composition systems. Supports -v/--verbose and
-q/--quiet flags for controlling output verbosity.
"""

import signal
import sys

from logos.cli.args import is_quiet, parse_args
from logos.cli.first_run import run_first_run_wizard
from logos.cli.layouts import display_error
from logos.cli.mode_select import run_mode_selection
from logos.core.identity import get_identity_path, load_identity
from logos.core.terminal import clear_screen


##Function purpose: Signal handler for SIGINT (Ctrl+C) to allow graceful exit
def _signal_handler(signum, frame):
    """
    Handles SIGINT signal (Ctrl+C) gracefully.

    Raises KeyboardInterrupt to allow proper cleanup and graceful exit
    handling throughout the application.
    """
    ##Action purpose: Raise KeyboardInterrupt for consistent handling
    raise KeyboardInterrupt("Interrupted by user (Ctrl+C)")


##Function purpose: Check if this is first run by checking for identity file
def is_first_run() -> bool:
    """
    Determines if this is the user's first run of LOGOS.

    Checks for existence of identity configuration file to determine
    if user has completed first-run wizard.

    Returns:
        True if identity file doesn't exist (first run), False otherwise
    """
    ##Action purpose: Get identity file path
    identity_path = get_identity_path()
    ##Condition purpose: Check if identity file exists
    return not identity_path.exists()


##Function purpose: Main CLI entry point that orchestrates the LOGOS workflow
def main() -> int:
    """
    Main CLI entry point that orchestrates the LOGOS workflow.

    Parses CLI arguments, routes user to first-run wizard or mode selection
    based on whether identity exists, handling all errors gracefully.
    Supports -v/--verbose and -q/--quiet flags.

    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    ##Action purpose: Register signal handler for Ctrl+C (SIGINT)
    signal.signal(signal.SIGINT, _signal_handler)

    ##Action purpose: Parse CLI arguments (sets verbosity level)
    args = parse_args()

    ##Condition purpose: Handle --version flag
    if args.version:
        from logos.core.version import get_version

        print(f"LOGOS {get_version()}")
        return 0

    try:
        ##Action purpose: Clear screen for clean start (skip in quiet mode)
        if not is_quiet():
            clear_screen()

        ##Condition purpose: Check if this is first run
        if is_first_run():
            ##Action purpose: Run first-run wizard for new users
            result = run_first_run_wizard()
            ##Condition purpose: Check if wizard completed successfully
            if not result:
                ##Action purpose: Exit if wizard was cancelled or failed
                return 1
            ##Action purpose: Clear screen after first-run
            clear_screen()

        ##Action purpose: Load identity for returning users
        identity = load_identity()
        ##Condition purpose: Check if identity loaded successfully
        if identity is None:
            ##Action purpose: Display error if identity couldn't be loaded
            display_error(
                "Failed to load identity configuration",
                "Please run first-run wizard again or check ~/.logos/identity.yaml",
            )
            return 1

        ##Action purpose: Run main mode selection loop
        return run_mode_selection(identity)

    except KeyboardInterrupt:
        ##Error purpose: Handle Ctrl+C gracefully (user interruption)
        print("\n\nExiting LOGOS...")
        ##Action purpose: Restore default signal handler before exit
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        return 0
    except (OSError, ValueError, FileNotFoundError) as e:
        ##Error purpose: Handle specific expected errors (file I/O, validation, missing files)
        display_error("Error occurred", str(e))
        return 1
    except Exception as e:
        ##Error purpose: Handle unexpected errors (graceful CLI degradation)
        display_error("Unexpected error occurred", str(e))
        return 1


##Function purpose: Entry point when run as module
if __name__ == "__main__":
    ##Action purpose: Register signal handler for Ctrl+C at module level
    signal.signal(signal.SIGINT, _signal_handler)
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        ##Error purpose: Handle Ctrl+C at module level (user interruption)
        print("\nExiting LOGOS...")
        ##Action purpose: Restore default signal handler before exit
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        sys.exit(0)
