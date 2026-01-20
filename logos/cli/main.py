"""
##Script function and purpose: Main CLI entry point.

Unified CLI that handles first-run, mode selection, and agent selection.
Phase 4 implementation.

##Action purpose: Orchestrates the complete LOGOS CLI workflow including first-run
detection, identity loading, mode selection, and agent selection with full integration
of identity, faction, and prompt composition systems.
"""

import sys

from logos.cli.first_run import run_first_run_wizard
from logos.cli.layouts import display_error
from logos.cli.mode_select import run_mode_selection
from logos.core.identity import get_identity_path, load_identity
from logos.core.terminal import clear_screen


##Function purpose: Check if this is first run by checking for identity file
def is_first_run() -> bool:
    """
    ##Function purpose: Determines if this is the user's first run of LOGOS.

    ##Action purpose: Checks for existence of identity configuration file to determine
    if user has completed first-run wizard.

    Returns:
        True if identity file doesn't exist (first run), False otherwise
    """
    ##Action purpose: Get identity file path
    identity_path = get_identity_path()
    ##Condition purpose: Check if identity file exists
    return not identity_path.exists()


##Function purpose: Main CLI entry point
def main() -> int:
    """
    ##Function purpose: Main CLI entry point that orchestrates the LOGOS workflow.

    ##Action purpose: Routes user to first-run wizard or mode selection based on
    whether identity exists, handling all errors gracefully.

    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    try:
        ##Action purpose: Clear screen for clean start
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
        ##Action purpose: Handle Ctrl+C gracefully
        print("\n\nExiting LOGOS...")
        return 0
    except Exception as e:
        ##Action purpose: Handle unexpected errors
        display_error("Unexpected error occurred", str(e))
        return 1


##Function purpose: Entry point when run as module
if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nExiting LOGOS...")
        sys.exit(0)
