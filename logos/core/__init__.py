"""
##Script function and purpose: LOGOS Core - Shared Infrastructure

Shared utilities and infrastructure used by both Daedelus and DEUS domains.

##Action purpose: Provides unified access to all shared utilities extracted from
both source codebases to eliminate duplication.
"""

from logos.core.agent import Agent
from logos.core.archival import (
    archive_file,
    archive_files_batch,
    clean_old_archives,
    list_archived_files,
    retrieve_from_archive,
)
from logos.core.bloat_prevention import (
    BloatAnalysis,
    analyze_agent_log_sizes,
    analyze_bloat,
    calculate_devdocs_size,
    find_oversized_files,
    find_stale_files,
    generate_health_report,
)
from logos.core.clipboard import copy_to_clipboard
from logos.core.constants import SEPARATOR_WIDTH, AgentGroups, Colors, UILayout
from logos.core.factions import FACTIONS, Faction, apply_faction_modifiers
from logos.core.identity import (
    SystemIdentity,
    create_identity,
    load_identity,
    save_identity,
    scan_system,
    update_session_tracking,
)
from logos.core.logging import configure_logging, get_logger
from logos.core.persistence import (
    get_config_dir,
    get_identity_path,
    read_config,
    write_config,
)
from logos.core.prompts import (
    build_agent_prompt_from_key,
    build_complete_prompt,
    build_identity_context,
)
from logos.core.temporal_logs import (
    LogAnalysis,
    LogSection,
    analyze_agent_log,
    archive_daily_entries,
    archive_weekly_summaries,
    generate_monthly_summary,
    generate_weekly_summary,
    parse_agent_log,
    scan_all_agent_logs,
)
from logos.core.terminal import clear_screen
from logos.core.types import AgentGroup, Err, Mode, Ok, Result, WelcomeScreenContext
from logos.core.ui import (
    BoxChars,
    UIColors,
    create_box,
    create_content_line,
    create_separator,
    print_box,
    print_error,
    print_header,
    print_info,
    print_menu_item,
    print_success,
    print_warning,
)
from logos.core.validation import validate_identity_schema, validate_input

__all__ = [
    # Agent dataclass
    "Agent",
    # Clipboard utilities
    "copy_to_clipboard",
    # Constants
    "Colors",
    "AgentGroups",
    "SEPARATOR_WIDTH",
    "UILayout",
    # Type definitions
    "Mode",
    "AgentGroup",
    "WelcomeScreenContext",
    # Result type pattern
    "Result",
    "Ok",
    "Err",
    # Faction system
    "Faction",
    "FACTIONS",
    "apply_faction_modifiers",
    # Identity system
    "SystemIdentity",
    "scan_system",
    "load_identity",
    "save_identity",
    "create_identity",
    "update_session_tracking",
    # Persistence utilities
    "read_config",
    "write_config",
    "get_config_dir",
    "get_identity_path",
    # Logging utilities
    "get_logger",
    "configure_logging",
    # Terminal utilities
    "clear_screen",
    # Prompt composition
    "build_identity_context",
    "build_complete_prompt",
    "build_agent_prompt_from_key",
    # UI components
    "BoxChars",
    "UIColors",
    "create_box",
    "create_separator",
    "create_content_line",
    "print_box",
    "print_header",
    "print_menu_item",
    "print_success",
    "print_error",
    "print_warning",
    "print_info",
    # Validation utilities
    "validate_input",
    "validate_identity_schema",
    # Archival utilities
    "archive_file",
    "archive_files_batch",
    "retrieve_from_archive",
    "list_archived_files",
    "clean_old_archives",
    # Bloat prevention utilities
    "BloatAnalysis",
    "calculate_devdocs_size",
    "find_oversized_files",
    "find_stale_files",
    "analyze_agent_log_sizes",
    "analyze_bloat",
    "generate_health_report",
    # Temporal logs utilities
    "LogSection",
    "LogAnalysis",
    "parse_agent_log",
    "analyze_agent_log",
    "generate_weekly_summary",
    "generate_monthly_summary",
    "archive_daily_entries",
    "archive_weekly_summaries",
    "scan_all_agent_logs",
]
