"""
##Script function and purpose: First-time setup wizard.

Handles initial system scan, faction selection, and identity creation.
Phase 4 implementation.

##Action purpose: Guides new users through initial LOGOS setup including system
scanning, faction selection, and identity persistence for future sessions.
"""

from logos.cli.layouts import display_error, display_first_run_wizard
from logos.core.factions import FACTIONS
from logos.core.identity import create_identity, save_identity, scan_system
from logos.core.terminal import clear_screen
from logos.core.validation import validate_input


##Function purpose: Get faction options for selection
def get_faction_options() -> list[tuple[str, str, str]]:
    """
    ##Function purpose: Builds faction selection options list.

    ##Action purpose: Creates list of (key, name, description) tuples for all
    5 available factions with their modifiers.

    Returns:
        List of (faction_key, faction_name, description) tuples
    """
    ##Action purpose: All 5 factions are selectable with their own modifiers
    selectable_factions = ["revanchist", "daedalus", "orphic", "technomancer", "deus"]
    options = []

    ##Loop purpose: Build options list from all selectable factions
    for key in selectable_factions:
        faction = FACTIONS.get(key)
        ##Condition purpose: Skip if faction not found
        if faction:
            ##Action purpose: Create option tuple with key, name, and philosophy
            options.append((key, faction.name, faction.philosophy))

    ##Action purpose: Return options list
    return options


##Function purpose: Handle faction selection input
def select_faction() -> str | None:
    """
    ##Function purpose: Prompts user for faction selection.

    ##Action purpose: Displays faction options and handles user input to select
    a faction, validating input and returning faction key.

    Returns:
        Faction key string, or None if cancelled
    """
    ##Fix: Removed unused function call - get_faction_options() was called but return value discarded.
    ##Note: Faction options are already displayed by display_first_run_wizard() before this function is called.

    ##Loop purpose: Display options and handle input until valid selection
    while True:
        try:
            ##Action purpose: Get user input
            choice = input("\nSelect faction (r/d/o/t/u/q): ").strip().lower()

            ##Action purpose: Validate input for security
            is_valid, error = validate_input(choice, max_length=20, allowed_chars="rdotuqexi")
            if not is_valid:
                ##Action purpose: Display validation error and prompt again
                print(f"Invalid input: {error}")
                continue

            ##Condition purpose: Map input to faction key
            if choice in ["r", "revanchist"]:
                return "revanchist"
            elif choice in ["d", "daedalus"]:
                return "daedalus"
            elif choice in ["o", "orphic"]:
                return "orphic"
            elif choice in ["t", "technomancer"]:
                return "technomancer"
            elif choice in ["u", "deus"]:
                return "deus"
            elif choice in ["q", "quit", "exit"]:
                ##Action purpose: Allow user to cancel
                return None
            else:
                ##Action purpose: Invalid input, prompt again
                print(
                    "Invalid selection. Please enter 'r' (Revanchist), 'd' (Daedalus), 'o' (Orphic), 't' (Technomancer), 'u' (Deus), or 'q' (Quit)"
                )
        except (EOFError, KeyboardInterrupt):
            ##Error purpose: Handle Ctrl+C or EOF (user interruption)
            return None


##Function purpose: Run the complete first-run setup wizard
def run_first_run_wizard() -> bool:
    """
    Runs the complete first-run setup wizard.

    Orchestrates system scanning, faction selection, and identity creation
    for new LOGOS users.

    Returns:
        True if wizard completed successfully, False if cancelled
    """
    ##Action purpose: Orchestrates system scanning, faction selection, and
    ##Step purpose: identity creation for new LOGOS users
    try:
        ##Action purpose: Clear screen for clean start
        clear_screen()

        ##Action purpose: Scan system for identity information
        system_data = scan_system()
        ##Condition purpose: Check if scan succeeded
        if system_data is None:
            ##Action purpose: Display error if scan failed
            display_error("Failed to scan system", "Could not gather system information. Please try again.")
            return False

        ##Action purpose: Prepare system info dict for display
        system_info = {
            "hostname": system_data.get("hostname", "Unknown"),
            "username": system_data.get("username", "Unknown"),
            "os_name": system_data.get("os_name", "Unknown"),
            "os_version": system_data.get("os_version", ""),
        }

        ##Action purpose: Get faction options
        factions = get_faction_options()

        ##Action purpose: Display first-run wizard UI
        display_first_run_wizard(system_info, factions)

        ##Action purpose: Get faction selection from user
        faction_key = select_faction()
        ##Condition purpose: Check if user cancelled
        if faction_key is None:
            ##Action purpose: Return False if cancelled
            return False

        ##Action purpose: Create identity with scanned data and selected faction
        identity = create_identity(faction_key, system_data)
        ##Condition purpose: Check if identity creation succeeded
        if identity is None:
            ##Action purpose: Display error if creation failed
            display_error("Failed to create identity", "Could not create identity configuration. Please try again.")
            return False

        ##Action purpose: Save identity to persistent storage
        success = save_identity(identity)
        ##Condition purpose: Check if save succeeded
        if not success:
            ##Action purpose: Display error if save failed
            display_error("Failed to save identity", "Could not save identity configuration. Please check permissions.")
            return False

        ##Action purpose: Return success
        return True

    except KeyboardInterrupt:
        ##Error purpose: Handle Ctrl+C gracefully (user interruption)
        print("\n\nFirst-run wizard cancelled.")
        return False
    except (OSError, ValueError, KeyError) as e:
        ##Error purpose: Handle specific expected errors (file I/O, validation, key lookup)
        display_error("Error in first-run wizard", str(e))
        return False
    except Exception as e:
        ##Error purpose: Handle unexpected errors (graceful CLI degradation)
        display_error("Unexpected error in first-run wizard", str(e))
        return False
