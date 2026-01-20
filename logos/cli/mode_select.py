"""
##Script function and purpose: Mode selection interface.

Allows user to choose between Daedelus and DEUS modes.
Phase 4 implementation.

##Action purpose: Provides mode selection interface with identity context display
and routes to appropriate agent selection based on user's mode choice.
"""

from logos.cli.agent_select import run_agent_selection
from logos.cli.layouts import display_error, display_faction_statistics, display_mode_selection, display_welcome_screen
from logos.core.factions import FACTIONS
from logos.core.identity import SystemIdentity
from logos.core.terminal import clear_screen
from logos.core.validation import validate_input


##Function purpose: Format last session info for display
def format_last_session(identity: SystemIdentity) -> str | None:
    """
    ##Function purpose: Formats last session information for display.

    ##Action purpose: Creates human-readable string from last session data
    including mode and agent if available.

    Args:
        identity: SystemIdentity instance with session data

    Returns:
        Formatted session string, or None if no session data
    """
    ##Condition purpose: Check if we have session data
    if not identity.last_mode:
        ##Action purpose: Return None if no session history
        return None

    ##Action purpose: Build session info string
    session_info = f"{identity.last_mode.upper()}"
    ##Condition purpose: Add agent if available
    if identity.last_agent:
        session_info += f" / {identity.last_agent}"

    ##Action purpose: Return formatted session info
    return session_info


##Function purpose: Handle mode selection input
def select_mode() -> str | None:
    """
    ##Function purpose: Prompts user for mode selection.

    ##Action purpose: Displays mode options and handles user input to select
    Daedelus or DEUS mode, validating input and returning mode string.

    Returns:
        Mode string ("daedelus" or "deus"), or None if cancelled
    """
    ##Loop purpose: Handle input until valid selection or cancel
    while True:
        try:
            ##Action purpose: Get user input
            choice = input("\nYour choice: ").strip().upper()

            ##Action purpose: Validate input for security
            is_valid, error = validate_input(choice, max_length=20, allowed_chars="DUFSTQ0123456789")
            if not is_valid:
                ##Action purpose: Display validation error and prompt again
                print(f"Invalid input: {error}")
                continue

            ##Condition purpose: Map input to mode or action
            if choice in ["D", "DAEDELUS"]:
                return "daedelus"
            elif choice in ["U", "DEUS"]:
                return "deus"
            elif choice in ["F", "FACTION"]:
                ##Action purpose: Faction change (not implemented yet)
                print("Faction change not yet implemented")
                continue
            elif choice in ["S", "SYSTEM", "INFO"]:
                ##Action purpose: System info (not implemented yet)
                print("System info not yet implemented")
                continue
            elif choice in ["T", "STATS", "STATISTICS"]:
                ##Action purpose: Show faction statistics
                return "stats"
            elif choice in ["Q", "QUIT", "EXIT", "0"]:
                ##Action purpose: Allow user to exit
                return None
            else:
                ##Action purpose: Invalid input, prompt again
                print("Invalid selection. Please enter 'D' (Daedelus), 'U' (DEUS), or 'Q' (Quit)")
        except (EOFError, KeyboardInterrupt):
            ##Action purpose: Handle Ctrl+C or EOF
            return None


##Function purpose: Main mode selection function
def run_mode_selection(identity: SystemIdentity) -> int:
    """
    ##Function purpose: Runs the main mode selection loop.

    ##Action purpose: Orchestrates welcome screen display, mode selection,
    session tracking updates, and routing to agent selection.

    Args:
        identity: SystemIdentity instance with user context

    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    ##Loop purpose: Main CLI loop until user exits
    while True:
        try:
            ##Action purpose: Clear screen for clean display
            clear_screen()

            ##Action purpose: Get faction instance for display
            faction = FACTIONS.get(identity.faction)
            faction_name = faction.name if faction else identity.faction

            ##Action purpose: Format OS info
            os_info = f"{identity.os_name} {identity.os_version}".strip()

            ##Action purpose: Format last session info
            last_session = format_last_session(identity)

            ##Action purpose: Display welcome screen with context
            display_welcome_screen(
                username=identity.username,
                hostname=identity.hostname,
                faction=faction_name,
                faction_key=identity.faction,
                os_info=os_info,
                last_session=last_session,
                faction_prompt_counts=identity.faction_prompt_counts,
            )

            ##Action purpose: Display mode selection menu
            display_mode_selection()

            ##Action purpose: Get mode selection from user
            mode = select_mode()
            ##Condition purpose: Check if user wants to exit
            if mode is None:
                ##Action purpose: Exit gracefully
                print("\nExiting LOGOS...")
                return 0

            ##Condition purpose: Check if user wants to see statistics
            if mode == "stats":
                ##Action purpose: Display faction statistics
                display_faction_statistics(
                    identity.faction_prompt_counts,
                    identity.mode_prompt_counts,
                )
                ##Action purpose: Wait for user to continue
                try:
                    input("\nPress Enter to continue...")
                except (EOFError, KeyboardInterrupt):
                    pass
                continue

            ##Action purpose: Run agent selection for selected mode
            result = run_agent_selection(mode, identity)
            ##Condition purpose: Check if agent selection wants to exit
            if result == 1:  # Exit code 1 means return to mode selection
                ##Action purpose: Reload identity to get latest updates
                from logos.core.identity import load_identity as reload_identity

                updated = reload_identity()
                if updated:
                    identity = updated
                continue
            elif result == 0:  # Exit code 0 means user wants to quit
                return 0
            else:
                ##Action purpose: Continue loop for other cases
                continue

        except KeyboardInterrupt:
            ##Action purpose: Handle Ctrl+C gracefully
            print("\n\nExiting LOGOS...")
            return 0
        except Exception as e:
            ##Action purpose: Handle unexpected errors
            display_error("Unexpected error in mode selection", str(e))
            ##Action purpose: Continue loop after error
            input("\nPress Enter to continue...")
            continue
