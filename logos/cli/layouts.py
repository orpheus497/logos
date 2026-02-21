"""
##Script function and purpose: Beautiful layout components for CLI screens.

Provides pre-built, beautiful layouts for first-run wizard, mode selection,
agent selection, and other CLI interfaces.

##Action purpose: Creates consistent, visually appealing terminal interfaces
using the UI component library.
"""

import textwrap

from logos.core.constants import Colors, UILayout
from logos.core.factions import FACTIONS
from logos.core.identity import SystemIdentity
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


##Function purpose: Wrap text to fit within specified width
def _wrap_text(text: str, width: int) -> list[str]:
    """
    Wraps text to fit within specified width.

    Breaks long text into multiple lines that fit within the specified width,
    preserving word boundaries.

    Args:
        text: Text to wrap
        width: Maximum width per line

    Returns:
        List of wrapped lines
    """
    ##Action purpose: Breaks long text into multiple lines that fit within
    ##Step purpose: the specified width, preserving word boundaries
    ##Action purpose: Use textwrap to break text into lines
    wrapped_lines = textwrap.wrap(text, width=width, break_long_words=False, break_on_hyphens=False)
    ##Condition purpose: Return wrapped lines or single line if empty
    return wrapped_lines if wrapped_lines else [text]


##Function purpose: Return Unicode art banner for "LOGOS" word
def get_logos_banner() -> list[str]:
    """
    Returns Unicode art banner for "LOGOS" word.

    Provides beautiful Unicode art representation of the LOGOS federation name for
    display at the top of all screens using block-drawing characters (U+2588, U+2592).

    Returns:
        List of strings representing the Unicode art banner
    """
    ##Action purpose: Provides beautiful Unicode art representation of the LOGOS
    ##Step purpose: federation name for display at the top of all screens using block-drawing characters
    ##Action purpose: Create impressive Unicode art banner for LOGOS using block-drawing characters
    ##Action purpose: Clear, readable banner that spells "LOGOS" clearly
    banner = [
        "█████          ███████      █████████     ███████     █████████  ",
        "▒▒███         ███▒▒▒▒▒███   ███▒▒▒▒▒███  ███▒▒▒▒▒███  ███▒▒▒▒▒███",
        " ▒███        ███     ▒▒███ ███     ▒▒▒  ███     ▒▒███▒███    ▒▒▒ ",
        " ▒███       ▒███      ▒███▒███         ▒███      ▒███▒▒█████████ ",
        " ▒███       ▒███      ▒███▒███    █████▒███      ▒███ ▒▒▒▒▒▒▒▒███",
        " ▒███      █▒▒███     ███ ▒▒███  ▒▒███ ▒▒███     ███  ███    ▒███",
        " ███████████ ▒▒▒███████▒   ▒▒█████████  ▒▒▒███████▒  ▒▒█████████ ",
        "▒▒▒▒▒▒▒▒▒▒▒    ▒▒▒▒▒▒▒      ▒▒▒▒▒▒▒▒▒     ▒▒▒▒▒▒▒     ▒▒▒▒▒▒▒▒▒  ",
    ]
    ##Action purpose: Ensure all lines are padded to uniform length
    max_length = max(len(line) for line in banner) if banner else 0
    banner = [line.ljust(max_length) for line in banner]
    return banner


##Function purpose: Display the LOGOS Unicode art banner
def display_logos_banner(width: int = 100, color: str = UIColors.PRIMARY) -> None:
    """
    Displays the LOGOS Unicode art banner.

    Prints the LOGOS banner centered within the specified width, using the
    provided color.

    Args:
        width: Total width for centering
        color: ANSI color code for the banner
    """
    ##Action purpose: Prints the LOGOS banner centered within the specified width,
    ##Step purpose: using the provided color
    ##Action purpose: Get banner lines
    banner_lines = get_logos_banner()
    reset = Colors.RESET

    ##Loop purpose: Print each banner line centered
    for line in banner_lines:
        ##Action purpose: Calculate padding for centering
        padding = (width - len(line)) // 2
        ##Action purpose: Print centered banner line with color
        print(" " * padding + color + line + reset)
    print()  # Extra spacing after banner


##Function purpose: Return ASCII art logo for specified faction
def get_faction_logo(faction_key: str) -> list[str]:
    """
    Returns ASCII art logo for specified faction.

    Provides beautiful ASCII art representation of each faction that aligns
    with their philosophical identity.

    Args:
        faction_key: Faction identifier ("daedalus", "deus", "revanchist", "orphic", "technomancer")
        Note: "daedelus" is a mode name, "daedalus" is the faction key in FACTIONS dictionary

    Returns:
        List of strings representing the ASCII art logo
    """
    ##Action purpose: Provides beautiful ASCII art representation of each
    ##Step purpose: faction that aligns with their philosophical identity
    ##Action purpose: Define unique ASCII art logos for each faction (all exactly 20 chars wide for perfect alignment)
    logos = {
        ##Action purpose: Revanchist logo - traditional, human-focused, shield (protective, minimal autonomy)
        ##Action purpose: Shield design representing protection and human-first philosophy
        "revanchist": [
            "     ╔═══════╗      ",  # 20 chars - Shield with cross
            "    ╔╝  ║ ║  ╚╗     ",  # 20 chars
            "   ╔╝   ║ ║   ╚╗    ",  # 20 chars
            "  ╔╝    ║ ║    ╚╗   ",  # 20 chars
            " ╔╝    HUMAN   ╚╗   ",  # 20 chars
            " ╚═══════════════╝  ",  # 20 chars
        ],
        ##Action purpose: Daedalus logo - craftsmanship, tools, building (low autonomy, careful monitoring)
        ##Action purpose: Hammer and anvil representing craftsmanship and careful work
        "daedelus": [
            "   ╔═══════════╗    ",  # 20 chars - Workshop
            "  ╔╝  ⚒   ⚒   ╚╗    ",  # 20 chars - Tools
            " ╔╝   ═══ ═══   ╚╗  ",  # 20 chars - Workbench
            "╔╝   CRAFTING   ╚╗  ",  # 20 chars - Craft text
            "╚════════════════╝  ",  # 20 chars - Base
            "    ║ TOOLS ║       ",  # 20 chars - Label
        ],
        ##Action purpose: Orphic logo - balance, harmony, connection (balanced autonomy, yin-yang inspired)
        ##Action purpose: Yin-yang symbol representing balance and harmony
        "orphic": [
            "   ╔═══════════╗    ",  # 20 chars - Circle
            "  ╔╝  ════ ═══ ╝╗   ",  # 20 chars - Yin-yang
            " ╔╝   ╬═══╬    ╚╗   ",  # 20 chars - Balance
            "╔╝   BALANCE   ╚╗   ",  # 20 chars - Text
            "╚════════════════╝  ",  # 20 chars - Base
            "    ═══ ╬ ═══       ",  # 20 chars - Symbol
        ],
        ##Action purpose: Technomancer logo - futuristic, tech, transformation (high autonomy, circuit/network)
        ##Action purpose: Circuit board pattern representing technology and transformation
        "technomancer": [
            "  ╔═════════════╗   ",  # 20 chars - Circuit
            " ╔╝ ════ ════  ╚╗   ",  # 20 chars - Nodes
            "╔╝  ════ ════   ╚╗  ",  # 20 chars - Network
            "╚═════════════════╝ ",  # 20 chars - Base
            "   TRANSFORM        ",  # 20 chars - Text
            "  ════ ╬ ════       ",  # 20 chars - Tech symbol
        ],
        ##Action purpose: DEUS logo - sovereignty, authority, control (maximum autonomy, crown/throne)
        ##Action purpose: Crown design representing sovereignty and authority
        "deus": [
            "  ╔═════════════╗   ",  # 20 chars - Crown base
            " ╔╝     ║║      ╚╗  ",  # 20 chars - Crown top
            "╔╝      ║║       ╚╗ ",  # 20 chars - Authority
            "╚═══ ═══╬╬═══ ════╝ ",  # 20 chars - Throne
            "    SOVEREIGN       ",  # 20 chars - Text
            "   ════╩╩═══        ",  # 20 chars - Base
        ],
    }

    ##Action purpose: Return logo for faction or empty list if not found
    return logos.get(faction_key, [])


##Function purpose: Display faction ASCII art logo with specified color
def display_faction_logo(faction_key: str, color: str = UIColors.WHITE, width: int = 100) -> None:
    """
    Displays faction ASCII art logo with specified color.

    Prints the faction logo centered within the specified width, using the
    provided color for all logo lines.

    Args:
        faction_key: Faction identifier
        color: ANSI color code for the logo
        width: Total width for centering
    """
    ##Action purpose: Prints the faction logo centered within the specified width,
    ##Step purpose: using the provided color for all logo lines
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


##Function purpose: Render a single row of logos line by line
def _render_logo_row(
    logos: list[list[str]],
    logo_keys: list[str],
    faction_keys: list[str],
    current_faction: str,
    width: int,
    spacing: int,
) -> None:
    """
    Renders a single row of logos line by line.

    Prints each line of logos with proper spacing and colors, handling the
    mode/faction key distinction when logo_keys and faction_keys differ.

    Args:
        logos: List of logo line lists (one per logo)
        logo_keys: List of logo keys (for logo lookup)
        faction_keys: List of faction keys (for faction data lookup and color comparison)
        current_faction: Currently selected faction key
        width: Total display width
        spacing: Space between logos
    """
    ##Action purpose: Prints each line of logos with proper spacing and colors,
    ##Step purpose: handling the mode/faction key distinction when logo_keys and faction_keys differ
    ui = UIColors
    reset = Colors.RESET

    ##Loop purpose: Print each line of logos
    for line_idx in range(UILayout.LOGO_HEIGHT):  # All logos are 6 lines tall (standardized)
        line_parts = []
        ##Loop purpose: Build line with all logos
        for logo_idx, logo_lines in enumerate(logos):
            ##Action purpose: Use faction key for color comparison (preserves mode/faction distinction)
            faction_key = faction_keys[logo_idx]
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


##Function purpose: Print prompt counters below a row of logos
def _print_logo_counters(
    logo_keys: list[str],
    faction_keys: list[str],
    faction_prompt_counts: dict[str, int],
    current_faction: str,
    width: int,
    logo_width: int,
    spacing: int,
) -> None:
    """
    Prints prompt counters below a row of logos.

    Displays prompt counts centered below each logo, using faction keys (not
    logo keys) for count lookup to preserve mode/faction distinction.

    Args:
        logo_keys: List of logo keys (for reference, not used for lookup)
        faction_keys: List of faction keys (for count lookup and color comparison)
        faction_prompt_counts: Dictionary mapping faction keys to prompt counts
        current_faction: Currently selected faction key
        width: Total display width
        logo_width: Width of each logo
        spacing: Space between logos
    """
    ##Action purpose: Displays prompt counts centered below each logo, using
    ##Step purpose: faction keys (not logo keys) for count lookup to preserve mode/faction distinction
    ui = UIColors
    reset = Colors.RESET

    ##Action purpose: Calculate counter line padding
    num_logos = len(faction_keys)
    total_logo_width = logo_width * num_logos
    total_spacing = spacing * (num_logos - 1)
    counter_line = " " * ((width - (total_logo_width + total_spacing)) // 2)

    ##Loop purpose: Build counter line for each logo
    for i, faction_key in enumerate(faction_keys):
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


##Function purpose: Display all 5 faction logos with prompt counters
def display_faction_logos_with_counters(
    current_faction: str,
    faction_prompt_counts: dict[str, int],
    width: int = 100,
) -> None:
    """
    Displays all 5 faction logos with prompt counters.

    Creates a beautiful display showing all faction logos in a grid layout,
    with the current faction highlighted in gold and others in white. Each
    logo shows the prompt count below it.

    Args:
        current_faction: Currently selected faction key
        faction_prompt_counts: Dictionary mapping faction keys to prompt counts
        width: Total display width
    """
    ##Action purpose: Creates a beautiful display showing all faction logos
    ##Step purpose: in a grid layout, with the current faction highlighted in gold
    ui = UIColors

    ##Step purpose: Calculate layout for 5 logos (2 rows: 3 on top, 2 on bottom)
    logo_width = UILayout.LOGO_WIDTH  # Width of each logo (standardized, now 20 chars)
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
            logo_lines = [""] * UILayout.LOGO_HEIGHT
        row1_logos.append(logo_lines)

    ##Action purpose: Render first row of logos
    _render_logo_row(row1_logos, row1_factions, row1_factions, current_faction, width, spacing)

    ##Action purpose: Print counters for first row
    _print_logo_counters(
        row1_factions, row1_factions, faction_prompt_counts, current_faction, width, logo_width, spacing
    )

    ##Step purpose: Display second row (2 logos: Daedalus, DEUS)
    ##Note: Using "daedelus" for logo lookup (mode name), but "daedalus" for faction data lookup
    row2_factions = ["daedelus", "deus"]  # Logo keys (mode names for display)
    row2_faction_keys = ["daedalus", "deus"]  # Faction keys for FACTIONS dictionary lookup
    row2_logos = []

    ##Loop purpose: Collect logos for second row
    for logo_key in row2_factions:
        logo_lines = get_faction_logo(logo_key)
        ##Condition purpose: Use empty list if logo not found
        if not logo_lines:
            logo_lines = [""] * UILayout.LOGO_HEIGHT
        row2_logos.append(logo_lines)

    ##Action purpose: Render second row of logos (preserves mode/faction key distinction)
    _render_logo_row(row2_logos, row2_factions, row2_faction_keys, current_faction, width, spacing)

    ##Action purpose: Print counters for second row (uses faction keys for lookup)
    _print_logo_counters(
        row2_factions, row2_faction_keys, faction_prompt_counts, current_faction, width, logo_width, spacing
    )


##Function purpose: Display beautiful welcome screen with user context
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
    Display beautiful welcome screen with user context.

    Creates the main LOGOS federation welcome screen with personalized information,
    faction logos, and prompt counters.

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
    ##Action purpose: Creates the main LOGOS federation welcome screen
    ##Step purpose: with personalized information, faction logos, and prompt counters
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

    ##Step purpose: Display LOGOS banner at top
    display_logos_banner(width, ui.PRIMARY)

    ##Step purpose: Create top border with subtitle
    title = "THE FEDERATION"
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


##Function purpose: Display beautiful mode selection interface
def display_mode_selection() -> None:
    """
    Display beautiful mode selection interface.

    Creates the Daedelus/DEUS mode selection screen with clear options and
    descriptions.

    """
    ##Action purpose: Creates the Daedelus/DEUS mode selection screen
    ##Step purpose: with clear options and descriptions
    width = UILayout.DISPLAY_WIDTH
    ui = UIColors

    ##Step purpose: Display LOGOS banner at top
    display_logos_banner(width, ui.PRIMARY)

    ##Step purpose: Create mode selection box
    lines = [
        "",
        "[D] Daedelus - Software Development",
        "    AI-powered development workflow system",
        "",
        "[U] DEUS - System Administration",
        "    FreeBSD system administration federation",
        "",
        "Additional Options:",
        "",
        "[F] Change Faction",
        "    Switch to a different philosophical faction",
        "",
        "[S] System Information",
        "    View detailed system and environment information",
        "",
        "[T] Faction Statistics",
        "    View prompt usage statistics by faction and mode",
        "",
        "[Q] Quit",
        "    Exit LOGOS",
        "",
    ]

    print_box(width, lines, title="SELECT MODE", border_color=ui.PRIMARY)


##Function purpose: Get LOGOS banner lines for batching (performance optimization)
def _get_logos_banner_lines(width: int = 100, color: str = UIColors.PRIMARY) -> list[str]:
    """
    Gets LOGOS banner lines for batching (performance optimization).

    Returns banner lines as a list instead of printing directly, allowing
    batch output operations for improved performance.

    Args:
        width: Total width for centering
        color: ANSI color code for the banner

    Returns:
        List of banner lines with formatting
    """
    ##Action purpose: Returns banner lines as a list instead of printing directly,
    ##Step purpose: allowing batch output operations for improved performance
    ##Action purpose: Get banner lines
    banner_lines = get_logos_banner()
    reset = Colors.RESET
    output_lines = []

    ##Loop purpose: Build each banner line centered
    for line in banner_lines:
        ##Action purpose: Calculate padding for centering
        padding = (width - len(line)) // 2
        ##Action purpose: Build centered banner line with color
        output_lines.append(" " * padding + color + line + reset)
    output_lines.append("")  # Extra spacing after banner

    ##Action purpose: Return banner lines
    return output_lines


##Function purpose: Get faction logo lines for batching (performance optimization)
def _get_faction_logo_lines(faction_key: str, color: str = UIColors.WHITE, width: int = 100) -> list[str]:
    """
    Gets faction logo lines for batching (performance optimization).

    Returns logo lines as a list instead of printing directly, allowing
    batch output operations for improved performance.

    Args:
        faction_key: Faction identifier
        color: ANSI color code for the logo
        width: Total width for centering

    Returns:
        List of logo lines with formatting
    """
    ##Action purpose: Returns logo lines as a list instead of printing directly,
    ##Step purpose: allowing batch output operations for improved performance
    ##Action purpose: Get logo lines
    logo_lines = get_faction_logo(faction_key)
    output_lines = []

    ##Condition purpose: Check if logo exists
    if not logo_lines:
        ##Action purpose: Return empty list if no logo found
        return output_lines

    ##Action purpose: Get reset code
    reset = Colors.RESET

    ##Loop purpose: Build each logo line centered
    for line in logo_lines:
        ##Action purpose: Calculate padding for centering
        padding = (width - len(line)) // 2
        ##Action purpose: Build centered logo line with color
        output_lines.append(" " * padding + color + line + reset)

    ##Action purpose: Return logo lines
    return output_lines


##Function purpose: Display beautiful agent selection menu
def display_agent_menu(
    mode: str,
    agent_groups: list[AgentGroup],
    faction_name: str | None = None,
    faction_key: str | None = None,
) -> None:
    """
    Display beautiful agent selection menu.

    Creates a formatted agent selection interface with color-coded groups, clear
    organization, and chosen faction logo. Uses batched output (single print
    operation) for improved performance.

    Args:
        mode: Current mode ("daedelus" or "deus")
        agent_groups: List of AgentGroup instances
        faction_name: Optional faction name to display
        faction_key: Optional faction key for logo display
    """
    ##Action purpose: Creates a formatted agent selection interface
    ##Step purpose: with color-coded groups, clear organization, and chosen faction logo
    width = UILayout.DISPLAY_WIDTH
    ui = UIColors

    ##Action purpose: Collect all output lines for batch printing (performance optimization)
    output_lines = []

    ##Step purpose: Collect LOGOS banner lines
    output_lines.extend(_get_logos_banner_lines(width, ui.PRIMARY))

    ##Step purpose: Create header with mode and faction
    mode_title = "DAEDELUS" if mode == "daedelus" else "DEUS"
    if faction_name:
        title = f"{mode_title} - {faction_name}"
    else:
        title = mode_title

    ##Step purpose: Collect top border
    top, _ = create_box(width, title, ui.PRIMARY, ui.BOLD + ui.PRIMARY)
    output_lines.append(top)

    ##Step purpose: Collect chosen faction logo if available
    if faction_key:
        output_lines.append(create_content_line("", width))  # Spacing
        ##Action purpose: Collect faction logo lines in gold
        output_lines.extend(_get_faction_logo_lines(faction_key, color=ui.GOLD, width=width))
        output_lines.append(create_content_line("", width))  # Spacing

    ##Step purpose: Collect agent groups
    for group in agent_groups:
        ##Action purpose: Collect group header
        group_header = f"GROUP {group.id}: {group.name} ({group.category})"
        output_lines.append(create_content_line("", width))  # Spacing
        output_lines.append(create_content_line(group_header, width, color=group.color))
        output_lines.append(create_content_line(f"Purpose: {group.purpose}", width, color=ui.CYAN))

        ##Step purpose: Collect agents in group
        for key, agent in group.agents.items():
            agent_line = f"{key}. {agent.name:<30} ({agent.desc})"
            output_lines.append(create_content_line(agent_line, width, color=ui.WHITE))

    ##Step purpose: Collect system options
    output_lines.append(create_content_line("", width))  # Spacing
    output_lines.append(create_content_line("[ SYSTEM ]", width, color=ui.WHITE))
    output_lines.append(create_content_line("  0. Exit", width, color=ui.WHITE))

    ##Step purpose: Collect bottom border
    _, bottom = create_box(width, None, ui.PRIMARY)
    output_lines.append(bottom)
    output_lines.append("")  # Extra spacing

    ##Action purpose: Print all lines in single operation (performance optimization - C9)
    print("\n".join(output_lines))


##Function purpose: Display beautiful first-run setup wizard
def display_first_run_wizard(
    system_info: dict[str, str],
    factions: list[tuple[str, str, str]],
) -> None:
    """
    Display beautiful first-run setup wizard.

    Creates the initial setup screen with system scan results and faction
    selection.

    Args:
        system_info: Dictionary with system information (hostname, username, os, etc.)
        factions: List of (faction_key, faction_name, description) tuples
    """
    ##Action purpose: Creates the initial setup screen with system scan
    ##Step purpose: results and faction selection
    width = UILayout.DISPLAY_WIDTH
    ui = UIColors

    ##Step purpose: Display LOGOS banner at top
    display_logos_banner(width, ui.PRIMARY)

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


##Function purpose: Display comprehensive system information
def display_system_info(identity: SystemIdentity) -> None:
    """
    Displays comprehensive system information.

    Shows system identity, date/time/timezone, and system capabilities in a
    formatted display box.

    Args:
        identity: SystemIdentity instance with system information
    """
    ##Action purpose: Shows system identity, date/time/timezone, and system
    ##Step purpose: capabilities in a formatted display box
    import time
    from datetime import datetime, timezone

    from logos.core.identity import scan_system

    width = UILayout.DISPLAY_WIDTH
    ui = UIColors

    ##Action purpose: Get current date/time/timezone information
    now_utc = datetime.now(timezone.utc)
    now_local = datetime.now().astimezone()  ##Fix: Use astimezone() to get timezone-aware datetime
    timezone_offset = now_local.utcoffset()
    timezone_name = time.tzname[0] if time.tzname else "UTC"

    ##Action purpose: Format timezone offset as ±HH:MM
    if timezone_offset:
        offset_seconds = int(timezone_offset.total_seconds())
        offset_hours = offset_seconds // 3600
        offset_minutes = abs((offset_seconds % 3600) // 60)
        timezone_str = f"{offset_hours:+03d}:{offset_minutes:02d}"
    else:
        timezone_str = "+00:00"

    ##Action purpose: Scan system for additional information
    scan_data = scan_system()

    ##Action purpose: Build system info lines
    info_lines = [
        "System Identity:",
        "",
        f"Hostname: {identity.hostname}",
        f"Username: {identity.username}",
        f"OS: {identity.os_name} {identity.os_version}",
        "",
        "Date and Time:",
        "",
        f"UTC Date: {now_utc.strftime('%Y-%m-%d')}",
        f"UTC Time: {now_utc.strftime('%H:%M:%S')}",
        ##Fix: isoformat() on timezone-aware UTC datetime already includes Z suffix
        f"UTC DateTime: {now_utc.isoformat()}",
        "",
        f"Local Date: {now_local.strftime('%Y-%m-%d')}",
        f"Local Time: {now_local.strftime('%H:%M:%S')}",
        f"Local DateTime: {now_local.isoformat()}",
        "",
        f"Timezone: {timezone_name} ({timezone_str})",
        "",
        "Python Environment:",
        "",
        f"Python Version: {scan_data.get('python_version', 'Unknown')}",
        "",
        "LOGOS State:",
        "",
    ]

    ##Action purpose: Add LOGOS state information
    if scan_data.get("logos_config_exists"):
        info_lines.append("✓ LOGOS configuration exists")
    else:
        info_lines.append("✗ LOGOS configuration not found")

    if scan_data.get("devdocs_exists"):
        info_lines.append("✓ Development docs exist")
    else:
        info_lines.append("✗ Development docs not found")

    if scan_data.get("sysdocs_exists"):
        info_lines.append("✓ System docs exist")
    else:
        info_lines.append("✗ System docs not found")

    ##Action purpose: Add FreeBSD-specific info if available
    if scan_data.get("freebsd_version"):
        info_lines.append("")
        info_lines.append("FreeBSD Information:")
        info_lines.append("")
        info_lines.append(f"FreeBSD Version: {scan_data.get('freebsd_version')}")
        if scan_data.get("zfs_available"):
            info_lines.append("✓ ZFS available")
        if scan_data.get("jail_host"):
            info_lines.append("✓ Jail host detected")

    ##Action purpose: Display system info in formatted box
    print_header("SYSTEM INFORMATION", width, color=ui.PRIMARY)
    print()
    print_box(
        width,
        info_lines,
        title="SYSTEM DETAILS",
        border_color=ui.INFO,
    )
    print()


##Function purpose: Display agent selection result beautifully
def display_agent_result(
    agent_name: str,
    agent_group: str,
    purpose: str,
    success: bool,
    show_prompt: bool = False,
    prompt_text: str | None = None,
) -> None:
    """
    Display agent selection result beautifully.

    Shows the result of agent selection with appropriate success/error messaging.

    Args:
        agent_name: Name of selected agent
        agent_group: Agent group identifier
        purpose: Agent purpose statement
        success: Whether clipboard copy succeeded
        show_prompt: Whether to display full prompt
        prompt_text: Full prompt text (if show_prompt is True)
    """
    ##Action purpose: Shows the result of agent selection with
    ##Step purpose: appropriate success/error messaging
    width = UILayout.DISPLAY_WIDTH
    ui = UIColors

    ##Step purpose: Display LOGOS banner at top
    display_logos_banner(width, ui.PRIMARY)

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
        ##Action purpose: Wrap prompt text to fit within display width
        prompt_lines = _wrap_text(prompt_text, width - UILayout.PROMPT_PADDING)  # Apply padding for text wrapping
        ##Loop purpose: Print each wrapped line
        for line in prompt_lines:
            print(line)

    print()


##Function purpose: Display error message beautifully
def display_error(message: str, details: str | None = None) -> None:
    """
    Display error message beautifully.

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


##Function purpose: Display faction and mode prompt statistics beautifully
def display_faction_statistics(
    faction_prompt_counts: dict[str, int],
    mode_prompt_counts: dict[str, int],
) -> None:
    """
    Display faction and mode prompt statistics beautifully.

    Shows how many prompts have been selected for each faction and mode,
    formatted in a clear, readable display.

    Args:
        faction_prompt_counts: Dictionary of faction name to prompt count
        mode_prompt_counts: Dictionary of mode name to prompt count
    """
    ##Action purpose: Shows how many prompts have been selected for each faction
    ##Step purpose: and mode, formatted in a clear, readable display
    width = UILayout.DISPLAY_WIDTH
    ui = UIColors

    ##Action purpose: Build statistics lines
    stats_lines = [
        "",
        "Faction Prompt Counts:",
        "",
    ]

    ##Loop purpose: Display faction counts in order (show all, even if 0)
    ##Note: Use faction keys (not mode names) for FACTIONS lookup
    for faction_key in ["revanchist", "orphic", "technomancer", "daedalus", "deus"]:
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
