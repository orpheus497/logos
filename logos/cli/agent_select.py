"""
##Script function and purpose: Agent selection within mode.

Displays appropriate agent menu based on selected mode (Daedelus or DEUS).
Phase 4 implementation.

##Action purpose: Provides agent selection interface with mode-aware agent listing,
prompt composition with identity and faction context, and clipboard integration.
"""

from logos.cli.layouts import display_agent_menu, display_agent_result, display_error
from logos.core.agent import Agent
from logos.core.clipboard import copy_to_clipboard
from logos.core.constants import Colors
from logos.core.factions import FACTIONS
from logos.core.identity import SystemIdentity, save_identity, update_session_tracking
from logos.core.prompts import build_complete_prompt
from logos.core.terminal import clear_screen
from logos.core.types import AgentGroup
from logos.core.ui import UIColors


##Function purpose: Get agent groups for Daedelus mode
def get_daedelus_groups() -> list[AgentGroup]:
    """
    ##Function purpose: Builds agent group data structure for Daedelus mode.

    ##Action purpose: Creates list of AgentGroup dataclass instances
    for all Daedelus agent groups in display order.

    Returns:
        List of AgentGroup instances
    """
    from logos.daedelus import (
        GROUP_A_BUILDERS,
        GROUP_B_GUARDIANS,
        GROUP_C_MAINTAINERS,
        GROUP_D_WORKERS,
        GROUP_E_OPERATORS,
    )

    ##Action purpose: Build groups list matching Daedelus structure
    groups = [
        AgentGroup(
            "A",
            "THE BUILDERS",
            "Creation",
            "Create new projects, features, and code from scratch",
            Colors.GREEN,
            GROUP_A_BUILDERS,
        ),
        AgentGroup(
            "B",
            "THE GUARDIANS",
            "Review",
            "Audit, review, and ensure code quality before release",
            Colors.BLUE,
            GROUP_B_GUARDIANS,
        ),
        AgentGroup(
            "C",
            "THE MAINTAINERS",
            "Maintenance",
            "Fix, patch, and maintain existing mature codebases",
            Colors.YELLOW,
            GROUP_C_MAINTAINERS,
        ),
        AgentGroup(
            "D",
            "THE WORKERS",
            "Extension",
            "Add features, refactor, and extend existing code",
            Colors.MAGENTA,
            GROUP_D_WORKERS,
        ),
        AgentGroup(
            "E",
            "THE OPERATORS",
            "Review Systems",
            "Comprehensive review and system orchestration",
            UIColors.GROUP_E,  # CYAN - Primary orchestration, coordination, leadership
            GROUP_E_OPERATORS,
        ),
    ]

    ##Action purpose: Return groups list
    return groups


##Function purpose: Get agent groups for DEUS mode
def get_deus_groups() -> list[AgentGroup]:
    """
    ##Function purpose: Builds agent group data structure for DEUS mode.

    ##Action purpose: Creates list of AgentGroup dataclass instances
    for all DEUS agent groups in display order.

    Returns:
        List of AgentGroup instances
    """
    from logos.deus import (
        GROUP_A_ENGINEERS,
        GROUP_B_AUDITORS,
        GROUP_C_MAINTAINERS,
        GROUP_D_SPECIALISTS,
        GROUP_E_OPERATORS,
    )

    ##Action purpose: Build groups list matching DEUS structure
    groups = [
        AgentGroup(
            "A",
            "THE ENGINEERS",
            "System Building",
            "Build new kernel, network, boot, and service configurations",
            Colors.GREEN,
            GROUP_A_ENGINEERS,
        ),
        AgentGroup(
            "B",
            "THE AUDITORS",
            "System Verification",
            "Audit security, syntax, performance, and compliance (read-only)",
            Colors.BLUE,
            GROUP_B_AUDITORS,
        ),
        AgentGroup(
            "C",
            "THE MAINTAINERS",
            "System Preservation",
            "Fix bugs, patch security, tune sysctls, maintain packages",
            Colors.YELLOW,
            GROUP_C_MAINTAINERS,
        ),
        AgentGroup(
            "D",
            "THE SPECIALISTS",
            "System Extension",
            "Build ports, configure jails, manage ZFS, enable compatibility",
            Colors.MAGENTA,
            GROUP_D_SPECIALISTS,
        ),
        AgentGroup(
            "E",
            "THE OPERATORS",
            "System Governance",
            "Orchestration, monitoring, documentation, and supreme oversight",
            Colors.RED,
            GROUP_E_OPERATORS,
        ),
    ]

    ##Action purpose: Return groups list
    return groups


##Function purpose: Get agent by key for selected mode
def get_agent_for_mode(mode: str, agent_key: str) -> Agent | None:
    """
    ##Function purpose: Retrieves agent by key for specified mode.

    ##Action purpose: Looks up agent in appropriate domain (Daedelus or DEUS)
    based on mode and returns Agent instance.

    Args:
        mode: Mode string ("daedelus" or "deus")
        agent_key: Agent identifier (e.g., "A1", "B6", "ocm")

    Returns:
        Agent instance, or None if not found
    """
    ##Condition purpose: Import appropriate domain based on mode
    if mode == "daedelus":
        from logos.daedelus import get_agent
    elif mode == "deus":
        from logos.deus import get_agent
    else:
        ##Action purpose: Return None for invalid mode
        return None

    ##Action purpose: Get agent by key
    return get_agent(agent_key)


##Function purpose: Handle agent selection input
def select_agent(mode: str) -> str | None:
    """
    ##Function purpose: Prompts user for agent selection.

    ##Action purpose: Displays agent menu and handles user input to select
    an agent, validating input and returning agent key.

    Args:
        mode: Current mode ("daedelus" or "deus")

    Returns:
        Agent key string, or None if cancelled
    """
    ##Loop purpose: Handle input until valid selection or cancel
    while True:
        try:
            ##Action purpose: Get user input
            choice = input("\nYour choice: ").strip().upper()

            ##Condition purpose: Check for exit command
            if choice in ["0", "Q", "QUIT", "EXIT", "BACK"]:
                ##Action purpose: Return None to go back to mode selection
                return None

            ##Action purpose: Normalize choice (handle lowercase)
            choice = choice.upper()

            ##Action purpose: Get agent to validate key
            agent = get_agent_for_mode(mode, choice)
            ##Condition purpose: Check if agent found
            if agent:
                ##Action purpose: Return valid agent key
                return choice
            else:
                ##Action purpose: Invalid selection, prompt again
                print(f"Invalid selection '{choice}'. Please try again or enter '0' to go back.")
        except (EOFError, KeyboardInterrupt):
            ##Error purpose: Handle Ctrl+C or EOF (user interruption)
            return None


##Function purpose: Handle agent selection, prompt building, and clipboard operations
def handle_agent_selection(mode: str, agent_key: str, identity: SystemIdentity) -> tuple[bool, SystemIdentity]:
    """
    Handles agent selection, prompt building, and clipboard operations.

    Retrieves agent, builds complete prompt with identity and faction,
    copies to clipboard, and displays result to user. Returns updated identity
    to ensure state synchronization in the calling loop.

    Args:
        mode: Current mode ("daedelus" or "deus")
        agent_key: Selected agent identifier
        identity: SystemIdentity instance for context

    Returns:
        Tuple of (success: bool, updated_identity: SystemIdentity)
        On failure, returns (False, original identity)
    """
    ##Action purpose: Retrieves agent, builds complete prompt with identity and faction,
    ##Step purpose: copies to clipboard, and displays result to user
    ##Action purpose: Get agent instance
    agent = get_agent_for_mode(mode, agent_key)
    ##Condition purpose: Check if agent found
    if agent is None:
        ##Action purpose: Display error if agent not found
        display_error("Agent not found", f"Could not find agent '{agent_key}' in {mode} mode.")
        ##Action purpose: Return failure with original identity
        return (False, identity)

    ##Action purpose: Build complete prompt with identity and faction, with OS adaptation for DEUS
    complete_prompt = build_complete_prompt(
        agent_prompt=agent.full_prompt,
        identity=identity,
        faction_name=identity.faction,
        domain=mode,  # Pass mode for OS adaptation (DEUS only)
    )

    ##Action purpose: Copy prompt to clipboard
    clipboard_success = copy_to_clipboard(complete_prompt)

    ##Action purpose: Update session tracking with agent selection
    updated_identity = update_session_tracking(identity, mode=mode, agent=agent_key)
    ##Action purpose: Save updated identity
    save_identity(updated_identity)

    ##Action purpose: Display result to user
    display_agent_result(
        agent_name=agent.name,
        agent_group=agent.group,
        purpose=agent.purpose,
        success=clipboard_success,
        show_prompt=not clipboard_success,  # Show prompt if clipboard failed
        prompt_text=complete_prompt if not clipboard_success else None,
    )

    ##Action purpose: Return success status and updated identity
    return (True, updated_identity)


##Function purpose: Run the agent selection loop for specified mode
def run_agent_selection(mode: str, identity: SystemIdentity) -> int:
    """
    Runs the agent selection loop for specified mode.

    Orchestrates agent menu display, agent selection, prompt generation,
    and clipboard operations in a loop until user exits.

    Args:
        mode: Current mode ("daedelus" or "deus")
        identity: SystemIdentity instance with user context

    Returns:
        Exit code (0 to quit, 1 to return to mode selection)
    """
    ##Action purpose: Orchestrates agent menu display, agent selection, prompt
    ##Step purpose: generation, and clipboard operations in a loop until user exits
    ##Loop purpose: Agent selection loop until user exits
    while True:
        try:
            ##Action purpose: Clear screen for clean display
            clear_screen()

            ##Action purpose: Get faction name for display
            faction = FACTIONS.get(identity.faction)
            faction_name = faction.name if faction else identity.faction

            ##Condition purpose: Get agent groups based on mode
            if mode == "daedelus":
                agent_groups = get_daedelus_groups()
            elif mode == "deus":
                agent_groups = get_deus_groups()
            else:
                ##Action purpose: Invalid mode, return error
                display_error("Invalid mode", f"Mode '{mode}' is not valid. Must be 'daedelus' or 'deus'.")
                return 1

            ##Action purpose: Display agent menu
            display_agent_menu(mode, agent_groups, faction_name, faction_key=identity.faction)

            ##Action purpose: Get agent selection from user
            agent_key = select_agent(mode)
            ##Condition purpose: Check if user wants to go back
            if agent_key is None:
                ##Action purpose: Return 1 to go back to mode selection
                return 1

            ##Action purpose: Handle agent selection and get updated identity
            success, identity = handle_agent_selection(mode, agent_key, identity)
            ##Condition purpose: Check if operation succeeded
            if not success:
                ##Action purpose: Continue loop on failure (error already displayed)
                continue

            ##Action purpose: Wait for user to continue
            try:
                input("\nPress Enter to continue...")
            except (EOFError, KeyboardInterrupt):
                ##Error purpose: Handle Ctrl+C during wait (user interruption)
                return 1

        except KeyboardInterrupt:
            ##Error purpose: Handle Ctrl+C gracefully (user interruption)
            print("\n\nReturning to mode selection...")
            return 1
        except (OSError, ValueError, KeyError) as e:
            ##Error purpose: Handle specific expected errors (file I/O, validation, key lookup)
            display_error("Error in agent selection", str(e))
            ##Action purpose: Wait for user acknowledgment
            try:
                input("\nPress Enter to continue...")
            except (EOFError, KeyboardInterrupt):
                ##Error purpose: Handle Ctrl+C or EOF during wait (user interruption)
                return 1
            continue
        except Exception as e:
            ##Error purpose: Handle unexpected errors (graceful CLI degradation)
            display_error("Unexpected error in agent selection", str(e))
            ##Action purpose: Wait for user acknowledgment
            try:
                input("\nPress Enter to continue...")
            except (EOFError, KeyboardInterrupt):
                ##Error purpose: Handle Ctrl+C or EOF during wait (user interruption)
                return 1
            continue
