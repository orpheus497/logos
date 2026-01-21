"""
##Script function and purpose: Beautiful terminal UI components and styling.

Provides modern, beautiful terminal interface components using box-drawing characters,
enhanced colors, and professional layouts for the LOGOS CLI.

##Action purpose: Creates a cohesive, visually appealing terminal experience that
matches the sophistication of the LOGOS federation concept.
"""

from logos.core.constants import Colors


##Class purpose: Box-drawing characters for beautiful terminal borders
class BoxChars:
    """
    ##Class purpose: Unicode box-drawing characters for terminal borders.

    Provides consistent box-drawing characters for creating beautiful
    terminal interfaces with borders and frames.
    """

    # Single-line box drawing
    HORIZONTAL: str = "═"
    VERTICAL: str = "║"
    TOP_LEFT: str = "╔"
    TOP_RIGHT: str = "╗"
    BOTTOM_LEFT: str = "╚"
    BOTTOM_RIGHT: str = "╝"
    T_LEFT: str = "╠"
    T_RIGHT: str = "╣"
    T_TOP: str = "╦"
    T_BOTTOM: str = "╩"
    CROSS: str = "╬"

    # Double-line box drawing (alternative style)
    D_HORIZONTAL: str = "═"
    D_VERTICAL: str = "║"
    D_TOP_LEFT: str = "╔"
    D_TOP_RIGHT: str = "╗"
    D_BOTTOM_LEFT: str = "╚"
    D_BOTTOM_RIGHT: str = "╝"


##Class purpose: Enhanced color palette with semantic meanings
class UIColors:
    """
    ##Class purpose: Enhanced color palette for UI components.

    Extends base Colors with semantic color meanings and UI-specific colors.
    """

    # Base colors (from Colors)
    RED: str = Colors.RED
    GREEN: str = Colors.GREEN
    YELLOW: str = Colors.YELLOW
    BLUE: str = Colors.BLUE
    MAGENTA: str = Colors.MAGENTA
    CYAN: str = Colors.CYAN
    WHITE: str = Colors.WHITE
    RESET: str = Colors.RESET
    BOLD: str = Colors.BOLD

    # Semantic UI colors
    PRIMARY: str = Colors.CYAN  # Main brand color
    SUCCESS: str = Colors.GREEN  # Success messages
    WARNING: str = Colors.YELLOW  # Warnings
    ERROR: str = Colors.RED  # Errors
    INFO: str = Colors.BLUE  # Information
    HIGHLIGHT: str = Colors.MAGENTA  # Highlights

    # Group colors (matching agent groups and their roles)
    GROUP_A: str = Colors.GREEN  # Builders/Engineers - Growth, creation, building
    GROUP_B: str = Colors.BLUE  # Guardians/Auditors - Trust, security, stability
    GROUP_C: str = Colors.YELLOW  # Maintainers - Caution, maintenance, attention
    GROUP_D: str = Colors.MAGENTA  # Workers/Specialists - Specialty, distinct, transformation
    GROUP_E: str = Colors.CYAN  # Operators - Primary orchestration, coordination, leadership

    # Special colors
    GOLD: str = Colors.YELLOW  # Gold color for chosen faction (using YELLOW)


##Function purpose: Create a beautiful box frame with optional title
def create_box(
    width: int,
    title: str | None = None,
    border_color: str = UIColors.PRIMARY,
    title_color: str = UIColors.BOLD + UIColors.PRIMARY,
) -> list[str]:
    """
    Create a beautiful box frame with optional title.

    Generates a list of strings representing a box frame using Unicode
    box-drawing characters.

    Args:
        width: Width of the box (excluding border characters)
        title: Optional title to center in the top border
        border_color: ANSI color code for border
        title_color: ANSI color code for title

    Returns:
        List of strings representing the box (top border, empty lines, bottom border)
    """
    box = BoxChars
    reset = Colors.RESET

    ##Step purpose: Calculate top border with optional title
    if title:
        ##Action purpose: Center title in border
        title_len = len(title)
        padding = (width - title_len - 2) // 2  # -2 for spaces around title
        left_pad = padding
        right_pad = width - title_len - left_pad - 2

        top_border = (
            f"{border_color}{box.TOP_LEFT}{box.HORIZONTAL * left_pad} "
            f"{title_color}{title}{reset}{border_color} "
            f"{box.HORIZONTAL * right_pad}{box.TOP_RIGHT}{reset}"
        )
    else:
        ##Action purpose: Create plain top border
        top_border = f"{border_color}{box.TOP_LEFT}{box.HORIZONTAL * width}{box.TOP_RIGHT}{reset}"

    ##Step purpose: Create bottom border
    bottom_border = f"{border_color}{box.BOTTOM_LEFT}{box.HORIZONTAL * width}{box.BOTTOM_RIGHT}{reset}"

    return [top_border, bottom_border]


##Function purpose: Create a horizontal separator line
def create_separator(
    width: int,
    char: str = BoxChars.HORIZONTAL,
    color: str = UIColors.PRIMARY,
) -> str:
    """
    Create a horizontal separator line.

    Args:
        width: Width of separator
        char: Character to use (default: horizontal box character)
        color: ANSI color code

    Returns:
        Formatted separator string
    """
    return f"{color}{char * width}{Colors.RESET}"


##Function purpose: Create a content line within a box frame
def create_content_line(
    text: str,
    width: int,
    padding: int = 1,
    align: str = "left",
    color: str = Colors.WHITE,
) -> str:
    """
    Create a content line within a box frame.

    Formats text with padding and alignment for box content.

    Args:
        text: Text content
        width: Total width (excluding border)
        padding: Padding on each side
        align: Alignment ("left", "center", "right")
        color: Text color

    Returns:
        Formatted line string
    """
    ##Action purpose: Formats text with padding and alignment for box content
    box = BoxChars
    reset = Colors.RESET
    content_width = width - (padding * 2)

    ##Condition purpose: Handle text that's too long
    if len(text) > content_width:
        text = text[: content_width - 3] + "..."

    ##Step purpose: Format text based on alignment
    if align == "center":
        ##Action purpose: Center-align text
        text_padding = (content_width - len(text)) // 2
        formatted = " " * text_padding + text + " " * (content_width - len(text) - text_padding)
    elif align == "right":
        ##Action purpose: Right-align text
        formatted = " " * (content_width - len(text)) + text
    else:
        ##Action purpose: Left-align text (default)
        formatted = text + " " * (content_width - len(text))

    ##Action purpose: Add border and padding
    return f"{box.VERTICAL}{' ' * padding}{color}{formatted}{reset}{' ' * padding}{box.VERTICAL}"


##Function purpose: Print a complete box with content
def print_box(
    width: int,
    lines: list[str],
    title: str | None = None,
    border_color: str = UIColors.PRIMARY,
    title_color: str = UIColors.BOLD + UIColors.PRIMARY,
) -> None:
    """
    Print a complete box with content.

    Convenience function to print a box frame with content lines.

    Args:
        width: Box width
        lines: List of content lines (will be formatted)
        title: Optional title
        border_color: Border color
        title_color: Title color
    """
    ##Action purpose: Convenience function to print a box frame with content lines
    ##Step purpose: Print top border
    top, bottom = create_box(width, title, border_color, title_color)
    print(top)

    ##Step purpose: Print content lines
    for line in lines:
        print(create_content_line(line, width, color=Colors.WHITE))

    ##Step purpose: Print bottom border
    print(bottom)


##Function purpose: Print a beautiful header with separator
def print_header(
    text: str,
    width: int = 100,
    char: str = "═",
    color: str = UIColors.PRIMARY,
    bold: bool = True,
) -> None:
    """
    Print a beautiful header with separator.

    Creates a centered header with decorative separators.

    Args:
        text: Header text
        width: Total width
        char: Separator character
        color: Color code
        bold: Whether to make text bold
    """
    ##Action purpose: Creates a centered header with decorative separators
    reset = Colors.RESET
    bold_code = Colors.BOLD if bold else ""

    ##Action purpose: Calculate padding for centering
    text_len = len(text)
    padding = (width - text_len) // 2

    ##Action purpose: Create separator lines
    sep = char * width

    ##Action purpose: Print header
    print(f"{color}{sep}{reset}")
    print(f"{color}{' ' * padding}{bold_code}{text}{reset}")
    print(f"{color}{sep}{reset}")


##Function purpose: Print a formatted menu item
def print_menu_item(
    key: str,
    label: str,
    description: str | None = None,
    color: str = Colors.WHITE,
    key_color: str = UIColors.HIGHLIGHT,
) -> None:
    """
    Print a formatted menu item.

    Creates a consistent menu item format with key and label.

    Args:
        key: Menu key/option (e.g., "A1", "D", "Q")
        label: Menu item label
        description: Optional description
        color: Label color
        key_color: Key color
    """
    ##Action purpose: Creates a consistent menu item format with key and label
    reset = Colors.RESET

    ##Step purpose: Format menu item
    if description:
        ##Action purpose: Include description
        print(f"  {key_color}[{key}]{reset} {color}{label:<30} {Colors.RESET}{description}{reset}")
    else:
        ##Action purpose: Simple format without description
        print(f"  {key_color}[{key}]{reset} {color}{label}{reset}")


##Function purpose: Print a success message with icon
def print_success(message: str) -> None:
    """
    Print a success message with icon.

    Args:
        message: Success message text
    """
    print(f"{UIColors.SUCCESS}✔ {message}{Colors.RESET}")


##Function purpose: Print an error message with icon
def print_error(message: str) -> None:
    """
    Print an error message with icon.

    Args:
        message: Error message text
    """
    print(f"{UIColors.ERROR}✗ {message}{Colors.RESET}")


##Function purpose: Print a warning message with icon
def print_warning(message: str) -> None:
    """
    Print a warning message with icon.

    Args:
        message: Warning message text
    """
    print(f"{UIColors.WARNING}⚠ {message}{Colors.RESET}")


##Function purpose: Print an info message with icon
def print_info(message: str) -> None:
    """
    Print an info message with icon.

    Args:
        message: Info message text
    """
    print(f"{UIColors.INFO}ℹ {message}{Colors.RESET}")
