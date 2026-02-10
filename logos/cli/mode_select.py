"""
##Script function and purpose: Mode selection interface.

Allows user to choose between Daedelus and DEUS modes.
Phase 4 implementation.

##Action purpose: Provides mode selection interface with identity context display
and routes to appropriate agent selection based on user's mode choice.
"""

from logos.cli.agent_select import run_agent_selection
from logos.cli.layouts import (
    display_error,
    display_faction_statistics,
    display_mode_selection,
    display_system_info,
    display_welcome_screen,
)
from logos.core.factions import FACTIONS
from logos.core.identity import SystemIdentity, load_identity, save_identity
from logos.core.terminal import clear_screen
from logos.core.validation import validate_input


##Function purpose: Display faction selection menu for faction change
def display_faction_selection_menu() -> None:
    """
    ##Function purpose: Displays faction selection menu for changing faction.

    ##Action purpose: Shows all 5 available factions with their keys and names
    for user selection during faction change operation.

    Returns:
        None (displays to stdout)
    """
    ##Action purpose: Get all 5 factions in order
    faction_keys = ["revanchist", "daedalus", "orphic", "technomancer", "deus"]

    ##Action purpose: Print header
    print("\n" + "=" * 70)
    print("  CHANGE FACTION".center(70))
    print("=" * 70)
    print()
    print("  Select your new faction:")
    print()

    ##Loop purpose: Display each faction option
    for key in faction_keys:
        faction = FACTIONS.get(key)
        ##Condition purpose: Skip if faction not found
        if faction:
            ##Action purpose: Display faction option with key and name
            print(f"  [{key[0].upper()}] {faction.name}")
            print(f"      {faction.philosophy[:60]}...")
            print()

    ##Action purpose: Display cancel option
    print("  [Q] Cancel / Quit")
    print()


##Function purpose: Handle faction selection input for faction change
def select_faction_for_change() -> str | None:
    """
    ##Function purpose: Prompts user for faction selection during faction change.

    ##Action purpose: Handles user input to select a new faction from all 5
    available factions, validating input and returning faction key.

    Returns:
        Faction key string, or None if cancelled
    """
    ##Loop purpose: Handle input until valid selection or cancel
    while True:
        try:
            ##Action purpose: Get user input
            choice = input("\nSelect faction (r/d/o/t/u/q): ").strip().lower()

            ##Action purpose: Validate input for security
            is_valid, error = validate_input(choice, max_length=20)
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


##Function purpose: Handle faction change operation
def change_faction(identity: SystemIdentity) -> SystemIdentity | None:
    """
    Handles faction change operation.

    Displays faction selection menu, gets user selection, updates identity
    faction field, saves to persistent storage, and returns updated identity.

    Args:
        identity: Current SystemIdentity instance

    Returns:
        Updated SystemIdentity instance if change successful, None if cancelled or failed
    """
    ##Action purpose: Displays faction selection menu, gets user selection,
    ##Step purpose: updates identity faction field, saves to persistent storage
    try:
        ##Action purpose: Clear screen for clean display
        clear_screen()

        ##Action purpose: Display faction selection menu
        display_faction_selection_menu()

        ##Action purpose: Get faction selection from user
        new_faction_key = select_faction_for_change()
        ##Condition purpose: Check if user cancelled
        if new_faction_key is None:
            ##Action purpose: Return None if cancelled
            return None

        ##Condition purpose: Check if selecting same faction
        if new_faction_key == identity.faction:
            ##Action purpose: Get faction name for message
            faction = FACTIONS.get(new_faction_key)
            faction_name = faction.name if faction else new_faction_key
            ##Action purpose: Inform user they already have this faction
            print(f"\nYou are already a member of {faction_name}.")
            try:
                input("\nPress Enter to continue...")
            except (EOFError, KeyboardInterrupt):
                pass
            ##Action purpose: Return current identity unchanged (no faction change)
            return identity

        ##Action purpose: Create new identity with updated faction (immutable pattern)
        ##Fix: Create new identity before save to prevent state inconsistency if save fails
        from datetime import datetime, timezone

        now = datetime.now(timezone.utc).isoformat()
        updated_identity = SystemIdentity(
            hostname=identity.hostname,
            username=identity.username,
            os_name=identity.os_name,
            os_version=identity.os_version,
            faction=new_faction_key,
            created_at=identity.created_at,
            last_session=identity.last_session,
            last_mode=identity.last_mode,
            last_agent=identity.last_agent,
            total_sessions=identity.total_sessions,
            faction_prompt_counts=identity.faction_prompt_counts.copy(),
            mode_prompt_counts=identity.mode_prompt_counts.copy(),
            faction_selected_at=now,  # Update faction selection timestamp
        )

        ##Action purpose: Save updated identity to persistent storage
        success = save_identity(updated_identity)
        ##Condition purpose: Check if save succeeded
        if not success:
            ##Action purpose: Display error if save failed
            display_error(
                "Failed to save faction change", "Could not save identity configuration. Please check permissions."
            )
            try:
                input("\nPress Enter to continue...")
            except (EOFError, KeyboardInterrupt):
                pass
            ##Action purpose: Return None if save failed (original identity unchanged)
            return None

        ##Action purpose: Get faction name for success message
        faction = FACTIONS.get(new_faction_key)
        faction_name = faction.name if faction else new_faction_key

        ##Action purpose: Display success message
        print(f"\n✓ Faction changed to: {faction_name}")
        try:
            input("\nPress Enter to continue...")
        except (EOFError, KeyboardInterrupt):
            pass

        ##Action purpose: Return updated identity (only after successful save)
        return updated_identity

    except KeyboardInterrupt:
        ##Action purpose: Handle Ctrl+C gracefully
        return None
    except (OSError, ValueError) as e:
        ##Error purpose: Handle specific expected errors (file I/O, validation)
        display_error("Error in faction change", str(e))
        try:
            input("\nPress Enter to continue...")
        except (EOFError, KeyboardInterrupt):
            ##Error purpose: Handle Ctrl+C or EOF during wait (user interruption)
            pass
        ##Action purpose: Return None on error
        return None
    except Exception as e:
        ##Error purpose: Handle unexpected errors (graceful CLI degradation)
        display_error("Unexpected error in faction change", str(e))
        try:
            input("\nPress Enter to continue...")
        except (EOFError, KeyboardInterrupt):
            ##Error purpose: Handle Ctrl+C or EOF during wait (user interruption)
            pass
        ##Action purpose: Return None on error
        return None


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
                ##Action purpose: Handle faction change request
                return "change_faction"
            elif choice in ["S", "SYSTEM", "INFO"]:
                ##Action purpose: Handle system info request
                return "system_info"
            elif choice in ["T", "STATS", "STATISTICS"]:
                ##Action purpose: Show faction statistics
                return "stats"
            elif choice in ["Q", "QUIT", "EXIT", "0"]:
                ##Action purpose: Allow user to exit
                return None
            else:
                ##Action purpose: Invalid input, prompt again
                print(
                    "Invalid selection. Please enter:\n"
                    "  'D' (Daedelus), 'U' (DEUS), 'F' (Change Faction),\n"
                    "  'S' (System Info), 'T' (Statistics), or 'Q' (Quit)"
                )
        except (EOFError, KeyboardInterrupt):
            ##Error purpose: Handle Ctrl+C or EOF gracefully (user interruption)
            print("\n")  # Add newline for clean exit
            return None


##Function purpose: Display mode selection screen with welcome and menu
def _display_mode_selection_screen(identity: SystemIdentity) -> None:
    """
    ##Function purpose: Displays welcome screen and mode selection menu.

    ##Action purpose: Prepares and displays the welcome screen with identity
    context and the mode selection menu.

    Args:
        identity: SystemIdentity instance with user context
    """
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


##Function purpose: Handle statistics display request
def _handle_stats_display(identity: SystemIdentity) -> None:
    """
    ##Function purpose: Handles faction statistics display.

    ##Action purpose: Displays faction statistics and waits for user to continue.

    Args:
        identity: SystemIdentity instance with statistics data
    """
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


##Function purpose: Handle system information display request
def _handle_system_info(identity: SystemIdentity) -> None:
    """
    ##Function purpose: Handles system information display.

    ##Action purpose: Clears screen, displays system information, and waits for user to continue.

    Args:
        identity: SystemIdentity instance with system data
    """
    ##Action purpose: Clear screen and display system information
    clear_screen()
    display_system_info(identity)
    ##Action purpose: Wait for user to continue
    try:
        input("\nPress Enter to continue...")
    except (EOFError, KeyboardInterrupt):
        pass


##Function purpose: Handle faction change request
def _handle_faction_change(identity: SystemIdentity) -> SystemIdentity:
    """
    ##Function purpose: Handles faction change operation.

    ##Action purpose: Processes faction change, updates identity, and reloads from disk.

    Args:
        identity: Current SystemIdentity instance

    Returns:
        Updated SystemIdentity instance (may be same as input if change failed)
    """
    ##Action purpose: Handle faction change
    updated_identity = change_faction(identity)
    ##Condition purpose: Check if faction change succeeded
    if updated_identity is not None:
        ##Action purpose: Update identity reference with new faction
        identity = updated_identity
        ##Action purpose: Reload identity from disk to ensure consistency
        reloaded = load_identity()
        if reloaded:
            identity = reloaded
    ##Action purpose: Return updated identity
    return identity


##Function purpose: Handle agent selection routing
def _handle_agent_selection(mode: str, identity: SystemIdentity) -> tuple[int, SystemIdentity]:
    """
    ##Function purpose: Handles agent selection routing and identity updates.

    ##Action purpose: Runs agent selection for selected mode, handles exit codes,
    and reloads identity if needed.

    Args:
        mode: Selected mode string ("daedelus" or "deus")
        identity: Current SystemIdentity instance

    Returns:
        Tuple of (exit_code, updated_identity)
        Exit code: 0 to quit, 1 to return to mode selection, 2 to continue
    """
    ##Action purpose: Run agent selection for selected mode
    result = run_agent_selection(mode, identity)
    ##Condition purpose: Check if agent selection wants to exit
    if result == 1:  # Exit code 1 means return to mode selection
        ##Action purpose: Reload identity to get latest updates
        from logos.core.identity import load_identity as reload_identity

        updated = reload_identity()
        if updated:
            identity = updated
        return (1, identity)
    elif result == 0:  # Exit code 0 means user wants to quit
        return (0, identity)
    else:
        ##Action purpose: Continue loop for other cases
        return (2, identity)


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
            ##Action purpose: Display welcome screen and mode selection menu
            _display_mode_selection_screen(identity)

            ##Action purpose: Get mode selection from user
            mode = select_mode()
            ##Condition purpose: Check if user wants to exit
            if mode is None:
                ##Action purpose: Exit gracefully
                print("\nExiting LOGOS...")
                return 0

            ##Condition purpose: Check if user wants to see statistics
            if mode == "stats":
                _handle_stats_display(identity)
                continue

            ##Condition purpose: Check if user wants to see system information
            if mode == "system_info":
                _handle_system_info(identity)
                continue

            ##Condition purpose: Check if user wants to change faction
            if mode == "change_faction":
                identity = _handle_faction_change(identity)
                continue

            ##Action purpose: Handle agent selection and get result
            exit_code, identity = _handle_agent_selection(mode, identity)
            ##Condition purpose: Check exit code
            if exit_code == 0:
                return 0
            elif exit_code == 1:
                continue
            else:
                continue

        except KeyboardInterrupt:
            ##Error purpose: Handle Ctrl+C gracefully (user interruption)
            print("\n\nExiting LOGOS...")
            ##Action purpose: Ensure clean exit without traceback
            return 0
        except (OSError, ValueError) as e:
            ##Error purpose: Handle specific expected errors (file I/O, validation)
            display_error("Error in mode selection", str(e))
            ##Action purpose: Continue loop after error
            try:
                input("\nPress Enter to continue...")
            except (EOFError, KeyboardInterrupt):
                ##Error purpose: Handle Ctrl+C or EOF during wait (user interruption)
                pass
            continue
        except Exception as e:
            ##Error purpose: Handle unexpected errors (graceful CLI degradation)
            display_error("Unexpected error in mode selection", str(e))
            ##Action purpose: Continue loop after error
            try:
                input("\nPress Enter to continue...")
            except (EOFError, KeyboardInterrupt):
                ##Error purpose: Handle Ctrl+C or EOF during wait (user interruption)
                pass
            continue
