"""
##Script function and purpose: Beautiful layout components for CLI screens.

Provides pre-built, beautiful layouts for first-run wizard, mode selection,
agent selection, and other CLI interfaces.

##Action purpose: Creates consistent, visually appealing terminal interfaces
using the UI component library.
"""

from logos.core.constants import Colors, UILayout
from logos.core.factions import FACTIONS
from logos.core.types import AgentGroup, WelcomeScreenContext
from logos.core.ui import (
    UIColors,
    create_box,
    create_content_line,
    print_box,
    print_header,
    print_success,
    print_warning,
)


##Function purpose: Get ASCII art logo for a faction
def get_faction_logo(faction_key: str) -> list[str]:
    """
    ##Function purpose: Returns ASCII art logo for specified faction.

    ##Action purpose: Provides beautiful ASCII art representation of each
    faction that aligns with their philosophical identity.

    Args:
        faction_key: Faction identifier ("daedelus", "deus", "revanchist", "orphic", "technomancer")

    Returns:
        List of strings representing the ASCII art logo
    """
    ##Action purpose: Define ASCII art logos for each faction (all 15 chars wide for alignment)
    logos = {
        ##Action purpose: Daedelus logo - craftsmanship, tools, building (hammer and anvil)
        "daedelus": [
            "     ╔═══╗",
            "    ╔╝ ⚒ ╚╗",
            "   ╔╝ ═══ ╚╗",
            "  ╔╝  ═══  ╚╗",
            " ╔╝  CRAFT  ╚╗",
            " ╚═══════════╝",
        ],
        ##Action purpose: DEUS logo - sovereignty, authority, control (crown/throne)
        "deus": [
            "   ╔═══════╗",
            "  ╔╝   ║   ╚╗",
            " ╔╝    ║    ╚╗",
            "╔╝  ═══╬═══  ╚╗",
            "╚══════╩══════╝",
            "   SOVEREIGN",
        ],
        ##Action purpose: Revanchist logo - traditional, human-focused, shield (protective)
        "revanchist": [
            "     ╔═══╗",
            "    ╔╝ ║ ╚╗",
            "   ╔╝  ║  ╚╗",
            "  ╔╝   ║   ╚╗",
            " ╔╝  HUMAN  ╚╗",
            " ╚═══════════╝",
        ],
        ##Action purpose: Orphic logo - balance, harmony, connection (yin-yang inspired)
        "orphic": [
            "     ╔═══╗",
            "    ╔╝ ═ ╚╗",
            "   ╔╝  ╬  ╚╗",
            "  ╔╝   ═   ╚╗",
            " ╔╝ BALANCE ╚╗",
            " ╚═══════════╝",
        ],
        ##Action purpose: Technomancer logo - futuristic, tech, transformation (circuit/network)
        "technomancer": [
            "   ╔═══════╗",
            "  ╔╝ ═══ ╚╗",
            " ╔╝  ═══  ╚╗",
            "╔╝ ═══════ ╚╗",
            "╚════════════╝",
            "  TRANSFORM",
        ],
    }

    ##Action purpose: Return logo for faction or empty list if not found
    return logos.get(faction_key, [])


##Function purpose: Display faction logo with color
def display_faction_logo(faction_key: str, color: str = UIColors.WHITE, width: int = 70) -> None:
    """
    ##Function purpose: Displays faction ASCII art logo with specified color.

    ##Action purpose: Prints the faction logo centered within the specified width,
    using the provided color for all logo lines.

    Args:
        faction_key: Faction identifier
        color: ANSI color code for the logo
        width: Total width for centering
    """
    ##Action purpose: Get logo lines
    logo_lines = get_faction_logo(faction_key)

    ##Condition purpose: Check if logo exists
    if not logo_lines:
        ##Action purpose: Return early if no logo found
        return

    ##Action purpose: Get reset code
    reset = Colors.RESET

    ##Loop purpose: Print each logo line centered
    for line in logo_lines:
        ##Action purpose: Calculate padding for centering
        padding = (width - len(line)) // 2
        ##Action purpose: Print centered logo line with color
        print(" " * padding + color + line + reset)


##Function purpose: Display all faction logos with counters
def display_faction_logos_with_counters(
    current_faction: str,
    faction_prompt_counts: dict[str, int],
    width: int = 70,
) -> None:
    """
    ##Function purpose: Displays all 5 faction logos with prompt counters.

    ##Action purpose: Creates a beautiful display showing all faction logos
    in a grid layout, with the current faction highlighted in gold and others
    in white. Each logo shows the prompt count below it.

    Args:
        current_faction: Currently selected faction key
        faction_prompt_counts: Dictionary mapping faction keys to prompt counts
        width: Total display width
    """
    ui = UIColors
    reset = Colors.RESET

    ##Action purpose: Define all faction keys in display order

    ##Step purpose: Calculate layout for 5 logos (2 rows: 3 on top, 2 on bottom)
    logo_width = UILayout.LOGO_WIDTH  # Width of each logo (standardized)
    spacing = UILayout.LOGO_SPACING  # Space between logos

    ##Step purpose: Print header
    print(create_content_line("", width))  # Spacing
    print(create_content_line("FACTION FEDERATION", width, align="center", color=ui.PRIMARY))
    print(create_content_line("", width))  # Spacing

    ##Step purpose: Display first row (3 logos: Revanchist, Orphic, Technomancer)
    row1_factions = ["revanchist", "orphic", "technomancer"]
    row1_logos = []

    ##Loop purpose: Collect logos for first row
    for faction_key in row1_factions:
        logo_lines = get_faction_logo(faction_key)
        ##Condition purpose: Use empty list if logo not found
        if not logo_lines:
            logo_lines = [""] * 6
        row1_logos.append(logo_lines)

    ##Loop purpose: Print first row line by line
    for line_idx in range(6):  # All logos are 6 lines tall
        line_parts = []
        ##Loop purpose: Build line with all three logos
        for logo_idx, logo_lines in enumerate(row1_logos):
            faction_key = row1_factions[logo_idx]
            ##Condition purpose: Choose color based on current faction
            logo_color = ui.GOLD if faction_key == current_faction else ui.WHITE
            ##Action purpose: Get logo line or empty string
            logo_line = logo_lines[line_idx] if line_idx < len(logo_lines) else ""
            ##Action purpose: Add logo line with color
            line_parts.append((logo_line, logo_color))

        ##Action purpose: Calculate spacing and print combined line
        total_logo_width = sum(len(part[0]) for part in line_parts)
        total_spacing = spacing * (len(line_parts) - 1)
        left_padding = (width - total_logo_width - total_spacing) // 2

        ##Action purpose: Build and print the line
        combined_line = " " * left_padding
        for i, (logo_line, logo_color) in enumerate(line_parts):
            if i > 0:
                combined_line += " " * spacing
            combined_line += logo_color + logo_line + reset
        print(combined_line)

    ##Step purpose: Print counters for first row
    counter_line = " " * ((width - (logo_width * 3 + spacing * 2)) // 2)  # Center the counters
    for i, faction_key in enumerate(row1_factions):
        if i > 0:
            counter_line += " " * spacing
        count = faction_prompt_counts.get(faction_key, 0)
        counter_color = ui.GOLD if faction_key == current_faction else ui.WHITE
        ##Action purpose: Center counter within logo width
        counter_padding = (logo_width - len(str(count))) // 2
        counter_line += (
            " " * counter_padding
            + counter_color
            + f"{count}"
            + reset
            + " " * (logo_width - counter_padding - len(str(count)))
        )
    print(counter_line)
    print()  # Extra spacing

    ##Step purpose: Display second row (2 logos: Daedelus, DEUS)
    row2_factions = ["daedelus", "deus"]
    row2_logos = []

    ##Loop purpose: Collect logos for second row
    for faction_key in row2_factions:
        logo_lines = get_faction_logo(faction_key)
        ##Condition purpose: Use empty list if logo not found
        if not logo_lines:
            logo_lines = [""] * 6
        row2_logos.append(logo_lines)

    ##Loop purpose: Print second row line by line
    for line_idx in range(6):  # All logos are 6 lines tall
        line_parts = []
        ##Loop purpose: Build line with both logos
        for logo_idx, logo_lines in enumerate(row2_logos):
            faction_key = row2_factions[logo_idx]
            ##Condition purpose: Choose color based on current faction
            logo_color = ui.GOLD if faction_key == current_faction else ui.WHITE
            ##Action purpose: Get logo line or empty string
            logo_line = logo_lines[line_idx] if line_idx < len(logo_lines) else ""
            ##Action purpose: Add logo line with color
            line_parts.append((logo_line, logo_color))

        ##Action purpose: Calculate spacing and print combined line
        total_logo_width = sum(len(part[0]) for part in line_parts)
        total_spacing = spacing * (len(line_parts) - 1)
        left_padding = (width - total_logo_width - total_spacing) // 2

        ##Action purpose: Build and print the line
        combined_line = " " * left_padding
        for i, (logo_line, logo_color) in enumerate(line_parts):
            if i > 0:
                combined_line += " " * spacing
            combined_line += logo_color + logo_line + reset
        print(combined_line)

    ##Step purpose: Print counters for second row
    counter_line = " " * ((width - (logo_width * 2 + spacing)) // 2)  # Center the counters
    for i, faction_key in enumerate(row2_factions):
        if i > 0:
            counter_line += " " * spacing
        count = faction_prompt_counts.get(faction_key, 0)
        counter_color = ui.GOLD if faction_key == current_faction else ui.WHITE
        ##Action purpose: Center counter within logo width
        counter_padding = (logo_width - len(str(count))) // 2
        counter_line += (
            " " * counter_padding
            + counter_color
            + f"{count}"
            + reset
            + " " * (logo_width - counter_padding - len(str(count)))
        )
    print(counter_line)
    print()  # Extra spacing


##Function purpose: Display the LOGOS welcome screen
def display_welcome_screen(
    context: WelcomeScreenContext | None = None,
    username: str | None = None,
    hostname: str | None = None,
    faction: str | None = None,
    faction_key: str | None = None,
    os_info: str | None = None,
    last_session: str | None = None,
    faction_prompt_counts: dict[str, int] | None = None,
) -> None:
    """
    ##Function purpose: Display beautiful welcome screen with user context.

    ##Action purpose: Creates the main LOGOS federation welcome screen
    with personalized information, faction logos, and prompt counters.

    Args:
        context: WelcomeScreenContext dataclass with all context data (preferred)
        username: Current username (legacy parameter, use context instead)
        hostname: System hostname (legacy parameter, use context instead)
        faction: Selected faction name (legacy parameter, use context instead)
        faction_key: Selected faction key (legacy parameter, use context instead)
        os_info: Operating system information (legacy parameter, use context instead)
        last_session: Last session information (legacy parameter, use context instead)
        faction_prompt_counts: Dictionary mapping faction keys to prompt counts (legacy parameter, use context instead)
    """
    ##Action purpose: Extract values from context if provided, otherwise use legacy parameters
    if context:
        username = context.username
        hostname = context.hostname
        faction = context.faction
        faction_key = context.faction_key
        os_info = context.os_info
        last_session = context.last_session
        faction_prompt_counts = context.faction_prompt_counts

    width = UILayout.DISPLAY_WIDTH
    ui = UIColors

    ##Step purpose: Create top border with title
    title = "THE LOGOS FEDERATION"
    top, _ = create_box(width, title, ui.PRIMARY, ui.BOLD + ui.PRIMARY)
    print(top)

    ##Step purpose: Display welcome message
    if username and hostname:
        ##Action purpose: Personalized welcome
        welcome_line = f"Welcome back, {username}@{hostname}"
        print(create_content_line(welcome_line, width, color=ui.WHITE))

        ##Step purpose: Display context information
        info_lines = []
        if faction:
            info_lines.append(f"Faction: {faction}")
        if os_info:
            info_lines.append(f"System: {os_info}")
        if last_session:
            info_lines.append(f"Last session: {last_session}")

        ##Condition purpose: Add separator if we have info
        if info_lines:
            print(create_content_line("", width))  # Empty line
            for info in info_lines:
                print(create_content_line(info, width, color=ui.CYAN))
    else:
        ##Action purpose: First-time welcome
        print(create_content_line("Welcome to the LOGOS Federation", width, color=ui.WHITE))
        print(create_content_line("Unified AI Agent System", width, color=ui.CYAN))

    ##Step purpose: Print bottom border
    _, bottom = create_box(width, None, ui.PRIMARY)
    print(bottom)
    print()  # Extra spacing

    ##Step purpose: Display faction logos with counters if available
    if faction_key and faction_prompt_counts is not None:
        ##Action purpose: Display all faction logos with prompt counters
        display_faction_logos_with_counters(
            current_faction=faction_key,
            faction_prompt_counts=faction_prompt_counts,
            width=width,
        )


##Function purpose: Display mode selection menu
def display_mode_selection() -> None:
    """
    ##Function purpose: Display beautiful mode selection interface.

    ##Action purpose: Creates the Daedelus/DEUS mode selection screen
    with clear options and descriptions.
    """
    width = UILayout.DISPLAY_WIDTH
    ui = UIColors

    ##Step purpose: Create mode selection box
    lines = [
        "",
        "[D] Daedelus - Software Development",
        "    AI-powered development workflow system",
        "",
        "[U] DEUS - System Administration",
        "    FreeBSD system administration federation",
        "",
        "[F] Change Faction | [S] System Info | [T] Faction Stats | [Q] Quit",
        "",
    ]

    print_box(width, lines, title="SELECT MODE", border_color=ui.PRIMARY)


##Function purpose: Display agent selection menu
def display_agent_menu(
    mode: str,
    agent_groups: list[AgentGroup],
    faction_name: str | None = None,
    faction_key: str | None = None,
) -> None:
    """
    ##Function purpose: Display beautiful agent selection menu.

    ##Action purpose: Creates a formatted agent selection interface
    with color-coded groups, clear organization, and chosen faction logo.

    Args:
        mode: Current mode ("daedelus" or "deus")
        agent_groups: List of AgentGroup instances
        faction_name: Optional faction name to display
        faction_key: Optional faction key for logo display
    """
    width = UILayout.DISPLAY_WIDTH
    ui = UIColors

    ##Step purpose: Create header with mode and faction
    mode_title = "DAEDELUS" if mode == "daedelus" else "DEUS"
    if faction_name:
        title = f"{mode_title} - {faction_name}"
    else:
        title = mode_title

    ##Step purpose: Print top border
    top, _ = create_box(width, title, ui.PRIMARY, ui.BOLD + ui.PRIMARY)
    print(top)

    ##Step purpose: Display chosen faction logo if available
    if faction_key:
        print(create_content_line("", width))  # Spacing
        ##Action purpose: Display faction logo in gold
        display_faction_logo(faction_key, color=ui.GOLD, width=width)
        print(create_content_line("", width))  # Spacing

    ##Step purpose: Display agent groups
    for group in agent_groups:
        ##Action purpose: Print group header
        group_header = f"GROUP {group.id}: {group.name} ({group.category})"
        print(create_content_line("", width))  # Spacing
        print(create_content_line(group_header, width, color=group.color))
        print(create_content_line(f"Purpose: {group.purpose}", width, color=ui.CYAN))

        ##Step purpose: Display agents in group
        for key, agent in group.agents.items():
            agent_line = f"{key}. {agent.name:<30} ({agent.desc})"
            print(create_content_line(agent_line, width, color=ui.WHITE))

    ##Step purpose: Print system options
    print(create_content_line("", width))  # Spacing
    print(create_content_line("[ SYSTEM ]", width, color=ui.WHITE))
    print(create_content_line("  0. Exit", width, color=ui.WHITE))

    ##Step purpose: Print bottom border
    _, bottom = create_box(width, None, ui.PRIMARY)
    print(bottom)
    print()  # Extra spacing


##Function purpose: Display first-run wizard
def display_first_run_wizard(
    system_info: dict[str, str],
    factions: list[tuple[str, str, str]],
) -> None:
    """
    ##Function purpose: Display beautiful first-run setup wizard.

    ##Action purpose: Creates the initial setup screen with system scan
    results and faction selection.

    Args:
        system_info: Dictionary with system information (hostname, username, os, etc.)
        factions: List of (faction_key, faction_name, description) tuples
    """
    width = UILayout.DISPLAY_WIDTH
    ui = UIColors

    ##Step purpose: Display welcome header
    print_header("LOGOS FEDERATION - FIRST RUN SETUP", width, color=ui.PRIMARY)
    print()

    ##Step purpose: Display system scan results
    print_box(
        width,
        [
            "System Scan Results:",
            "",
            f"Hostname: {system_info.get('hostname', 'Unknown')}",
            f"Username: {system_info.get('username', 'Unknown')}",
            f"OS: {system_info.get('os_name', 'Unknown')} {system_info.get('os_version', '')}",
            "",
        ],
        title="SYSTEM IDENTITY",
        border_color=ui.INFO,
    )
    print()

    ##Step purpose: Display faction selection
    faction_lines = [
        "Select your philosophical faction:",
        "",
    ]

    ##Loop purpose: Add faction options
    for key, name, desc in factions:
        faction_lines.append(f"[{key}] {name}")
        faction_lines.append(f"     {desc}")
        faction_lines.append("")

    print_box(
        width,
        faction_lines,
        title="FACTION SELECTION",
        border_color=ui.HIGHLIGHT,
    )
    print()


##Function purpose: Display agent prompt result
def display_agent_result(
    agent_name: str,
    agent_group: str,
    purpose: str,
    success: bool,
    show_prompt: bool = False,
    prompt_text: str | None = None,
) -> None:
    """
    ##Function purpose: Display agent selection result beautifully.

    ##Action purpose: Shows the result of agent selection with
    appropriate success/error messaging.

    Args:
        agent_name: Name of selected agent
        agent_group: Agent group identifier
        purpose: Agent purpose statement
        success: Whether clipboard copy succeeded
        show_prompt: Whether to display full prompt
        prompt_text: Full prompt text (if show_prompt is True)
    """
    width = UILayout.DISPLAY_WIDTH
    ui = UIColors

    ##Step purpose: Display result header
    agent_title = f"Group {agent_group} - {agent_name}"
    print_header(agent_title, width, color=ui.PRIMARY)
    print()

    ##Condition purpose: Display success or failure message
    if success:
        print_success(f"Prompt for '{agent_name}' copied to clipboard!")
    else:
        print_warning("Clipboard unavailable - prompt displayed below")

    ##Step purpose: Display purpose
    print()
    print(f"{ui.YELLOW}Purpose:{Colors.RESET}")
    print(purpose)

    ##Condition purpose: Display full prompt if requested
    if show_prompt and prompt_text:
        print()
        print(f"{ui.BOLD}Full Prompt:{Colors.RESET}")
        print(prompt_text)

    print()


##Function purpose: Display error message
def display_error(message: str, details: str | None = None) -> None:
    """
    ##Function purpose: Display error message beautifully.

    Args:
        message: Error message
        details: Optional detailed error information
    """
    width = UILayout.DISPLAY_WIDTH
    ui = UIColors

    error_lines = [message]
    if details:
        error_lines.append("")
        error_lines.append(details)

    print_box(
        width,
        error_lines,
        title="ERROR",
        border_color=ui.ERROR,
        title_color=ui.BOLD + ui.ERROR,
    )
    print()


##Function purpose: Display faction prompt statistics
def display_faction_statistics(
    faction_prompt_counts: dict[str, int],
    mode_prompt_counts: dict[str, int],
) -> None:
    """
    ##Function purpose: Display faction and mode prompt statistics beautifully.

    ##Action purpose: Shows how many prompts have been selected for each faction
    and mode, formatted in a clear, readable display.

    Args:
        faction_prompt_counts: Dictionary of faction name to prompt count
        mode_prompt_counts: Dictionary of mode name to prompt count
    """
    width = UILayout.DISPLAY_WIDTH
    ui = UIColors

    ##Action purpose: Build statistics lines
    stats_lines = [
        "",
        "Faction Prompt Counts:",
        "",
    ]

    ##Loop purpose: Display faction counts in order (show all, even if 0)
    for faction_key in ["revanchist", "orphic", "technomancer", "daedelus", "deus"]:
        count = faction_prompt_counts.get(faction_key, 0)
        faction = FACTIONS.get(faction_key)
        faction_name = faction.name if faction else faction_key.title()
        stats_lines.append(f"  {faction_name:<20} {count:>6} prompts")

    stats_lines.append("")
    stats_lines.append("Mode Prompt Counts:")
    stats_lines.append("")

    ##Loop purpose: Display mode counts
    for mode in ["daedelus", "deus"]:
        count = mode_prompt_counts.get(mode, 0)
        mode_name = "Daedelus" if mode == "daedelus" else "DEUS"
        stats_lines.append(f"  {mode_name:<20} {count:>6} prompts")

    stats_lines.append("")

    ##Action purpose: Display statistics in a box
    print_box(
        width,
        stats_lines,
        title="FACTION STATISTICS",
        border_color=ui.HIGHLIGHT,
        title_color=ui.BOLD + ui.HIGHLIGHT,
    )
    print()
