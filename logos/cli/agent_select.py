"""
##Script function and purpose: Agent selection within mode.

Displays appropriate agent menu based on selected mode (Daedelus or DEUS).
Phase 5 implementation.

##Action purpose: Provides agent selection interface with mode-aware agent listing,
prompt composition with identity and faction context, clipboard integration,
alias resolution, search/filter capability, and prompt preview support.
"""

from logos.cli.args import is_verbose
from logos.cli.layouts import display_agent_menu, display_agent_result, display_error
from logos.core.agent import Agent
from logos.core.aliases import get_all_aliases, resolve_alias, validate_custom_aliases
from logos.core.clipboard import copy_to_clipboard
from logos.core.config import get_config_value, load_config
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


##Function purpose: Search agents by name, key, or description
def search_agents(mode: str, query: str) -> list[tuple[str, Agent]]:
    """
    Searches agents by name, key, alias, or description.

    Matches query against agent key, name, description, and aliases.
    Returns a list of (agent_key, Agent) tuples matching the query.

    Args:
        mode: Current mode ("daedelus" or "deus")
        query: Search query string (case-insensitive)

    Returns:
        List of (agent_key, Agent) tuples matching the search query
    """
    ##Action purpose: Get all agent groups for the mode
    if mode == "daedelus":
        groups = get_daedelus_groups()
    elif mode == "deus":
        groups = get_deus_groups()
    else:
        return []

    ##Action purpose: Normalize query for case-insensitive matching
    query_lower = query.lower().strip()
    if not query_lower:
        return []

    ##Action purpose: Get aliases for reverse lookup
    config = load_config()
    custom_aliases = validate_custom_aliases(get_config_value(config, "aliases", {}))
    all_aliases = get_all_aliases(mode, custom_aliases)
    ##Action purpose: Build reverse map: agent_key -> list of aliases
    key_to_aliases: dict[str, list[str]] = {}
    for alias_name, agent_key in all_aliases.items():
        key_to_aliases.setdefault(agent_key, []).append(alias_name)

    results: list[tuple[str, Agent]] = []
    for group in groups:
        for agent_key, agent in group.agents.items():
            ##Action purpose: Check if query matches key, name, desc, or aliases
            searchable = f"{agent_key} {agent.name} {agent.desc}".lower()
            ##Action purpose: Also include aliases in searchable text
            agent_aliases = key_to_aliases.get(agent_key, [])
            searchable += " " + " ".join(agent_aliases)

            if query_lower in searchable:
                results.append((agent_key, agent))

    return results


##Function purpose: Display search results to user
def display_search_results(results: list[tuple[str, Agent]], query: str) -> None:
    """
    Displays agent search results in a formatted list.

    Args:
        results: List of (agent_key, Agent) tuples from search_agents
        query: Original search query for display
    """
    if not results:
        print(f"\n  {Colors.YELLOW}No agents found matching '{query}'.{Colors.RESET}")
        return

    print(f"\n  {Colors.CYAN}Search results for '{query}' ({len(results)} found):{Colors.RESET}")
    print(f"  {Colors.CYAN}{'─' * 56}{Colors.RESET}")
    for agent_key, agent in results:
        print(f"  {Colors.BOLD}[{agent_key}]{Colors.RESET} {agent.name} — {agent.desc}")
    print(f"  {Colors.CYAN}{'─' * 56}{Colors.RESET}")
    print(f"  {Colors.YELLOW}Enter an agent key to select, or '0' to go back.{Colors.RESET}")


##Function purpose: Handle agent selection input
def select_agent(mode: str) -> str | None:
    """
    ##Function purpose: Prompts user for agent selection.

    ##Action purpose: Displays agent menu and handles user input to select
    an agent, validating input, resolving aliases, and supporting search
    via '/' prefix. Returns agent key.

    Args:
        mode: Current mode ("daedelus" or "deus")

    Returns:
        Agent key string, or None if cancelled
    """
    ##Action purpose: Load config for alias resolution
    config = load_config()
    custom_aliases = validate_custom_aliases(get_config_value(config, "aliases", {}))

    ##Loop purpose: Handle input until valid selection or cancel
    while True:
        try:
            ##Action purpose: Get user input
            choice = input("\nYour choice: ").strip()

            ##Condition purpose: Check for exit command
            if choice.upper() in ["0", "Q", "QUIT", "EXIT", "BACK"]:
                ##Action purpose: Return None to go back to mode selection
                return None

            ##Condition purpose: Check for search command (/ prefix)
            if choice.startswith("/"):
                query = choice[1:].strip()
                if query:
                    results = search_agents(mode, query)
                    display_search_results(results, query)
                else:
                    print(f"  {Colors.YELLOW}Usage: /search_term (e.g., /architect, /security){Colors.RESET}")
                continue

            ##Action purpose: Try direct agent key first (uppercase)
            agent_key = choice.upper()
            agent = get_agent_for_mode(mode, agent_key)
            if agent:
                ##Action purpose: Return valid agent key
                return agent_key

            ##Action purpose: Try alias resolution
            resolved = resolve_alias(choice, mode, custom_aliases)
            if resolved:
                agent = get_agent_for_mode(mode, resolved)
                if agent:
                    if is_verbose():
                        print(f"  {Colors.CYAN}→ Resolved alias '{choice}' to {resolved}{Colors.RESET}")
                    return resolved

            ##Action purpose: Invalid selection, prompt again
            print(f"Invalid selection '{choice}'. Use /term to search, or enter '0' to go back.")
        except (EOFError, KeyboardInterrupt):
            ##Error purpose: Handle Ctrl+C or EOF (user interruption)
            return None


##Function purpose: Handle agent selection, prompt building, and clipboard operations
def handle_agent_selection(mode: str, agent_key: str, identity: SystemIdentity) -> tuple[bool, SystemIdentity]:
    """
    Handles agent selection, prompt building, and clipboard operations.

    Retrieves agent, builds complete prompt with identity and faction,
    optionally shows prompt preview, copies to clipboard, and displays result
    to user. Returns updated identity to ensure state synchronization
    in the calling loop.

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

    ##Action purpose: Load config for preview settings
    config = load_config()
    show_preview = get_config_value(config, "clipboard.show_preview", False)
    preview_lines = get_config_value(config, "clipboard.preview_lines", 10)

    ##Condition purpose: Show prompt preview if configured or verbose mode
    if show_preview or is_verbose():
        _show_prompt_preview(complete_prompt, preview_lines)

    ##Condition purpose: Show verbose agent details
    if is_verbose():
        print(f"\n  {Colors.CYAN}Agent:{Colors.RESET} {agent.name} [{agent_key}]")
        print(f"  {Colors.CYAN}Group:{Colors.RESET} {agent.group}")
        print(f"  {Colors.CYAN}Mode:{Colors.RESET} {mode}")
        print(
            f"  {Colors.CYAN}Prompt length:{Colors.RESET} {len(complete_prompt)} chars, {len(complete_prompt.splitlines())} lines"
        )

    ##Action purpose: Copy prompt to clipboard
    clipboard_enabled = get_config_value(config, "clipboard.enabled", True)
    clipboard_success = False
    if clipboard_enabled:
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


##Function purpose: Display prompt preview
def _show_prompt_preview(prompt_text: str, preview_lines: int = 10) -> None:
    """
    Displays a preview of the prompt before clipboard copy.

    Shows the first and last N/2 lines of the prompt to let the user
    verify the content before it's copied.

    Args:
        prompt_text: Full prompt text
        preview_lines: Total number of lines to show (split between first/last)
    """
    lines = prompt_text.splitlines()
    total = len(lines)
    line_budget = max(0, preview_lines or 0)

    print(f"\n{Colors.CYAN}{'═' * 60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}  Prompt Preview ({total} lines total){Colors.RESET}")
    print(f"{Colors.CYAN}{'═' * 60}{Colors.RESET}")

    if total == 0:
        ##Action purpose: Handle empty prompt
        print("  (prompt is empty)")
    elif line_budget <= 0:
        ##Action purpose: Preview disabled or zero-length budget
        print(f"\n  {Colors.YELLOW}... ({total} lines omitted; preview disabled) ...{Colors.RESET}\n")
    elif total <= line_budget:
        ##Action purpose: Show all lines if within budget
        for line in lines:
            print(f"  {line}")
    else:
        ##Action purpose: Split budget between first and last segments
        first_count = line_budget // 2
        ##Action purpose: last_count is the remaining budget, capped to lines actually available after first segment
        last_count = min(line_budget - first_count, max(0, total - first_count))
        shown = min(total, first_count + last_count)
        omitted = total - shown

        ##Action purpose: Show first segment
        for line in lines[:first_count]:
            print(f"  {line}")

        if omitted > 0:
            print(f"\n  {Colors.YELLOW}... ({omitted} lines omitted) ...{Colors.RESET}\n")

        ##Action purpose: Show last segment
        if last_count > 0:
            for line in lines[-last_count:]:
                print(f"  {line}")

    print(f"{Colors.CYAN}{'═' * 60}{Colors.RESET}")


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
