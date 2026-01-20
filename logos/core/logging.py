"""
##Script function and purpose: Logging configuration for LOGOS.

Provides a standardized logging setup with configurable verbosity via
environment variables. Used by both Daedelus and DEUS domains.

##Action purpose: Single source of truth for logging configuration across LOGOS.

Usage:
    from logos.core.logging import get_logger

    logger = get_logger(__name__)
    logger.info("Agent selected: %s", agent_key)
    logger.debug("Clipboard method: wl-copy")
    logger.error("Clipboard failed: %s", error)

Environment Variables:
    LOGOS_LOG_LEVEL: DEBUG, INFO, WARNING, ERROR, CRITICAL (default: WARNING)
    LOGOS_LOG_FILE: Path to log file (default: stderr only)
"""

import logging
import os
import sys

##Action purpose: Default logging configuration constants
DEFAULT_LOG_LEVEL = "WARNING"
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def _get_log_level() -> int:
    """
    ##Function purpose: Get log level from environment variable.

    ##Action purpose: Reads LOGOS_LOG_LEVEL environment variable and converts to logging level.

    Returns:
        Logging level integer (logging.DEBUG, logging.INFO, etc.)
    """
    ##Action purpose: Get log level from environment, defaulting to WARNING
    level_name = os.environ.get("LOGOS_LOG_LEVEL", DEFAULT_LOG_LEVEL).upper()
    ##Action purpose: Convert string level name to logging constant
    return getattr(logging, level_name, logging.WARNING)


def _get_log_file() -> str | None:
    """
    ##Function purpose: Get log file path from environment variable.

    ##Action purpose: Reads LOGOS_LOG_FILE environment variable.

    Returns:
        Log file path string or None if not configured
    """
    return os.environ.get("LOGOS_LOG_FILE")


def configure_logging() -> None:
    """
    ##Function purpose: Configure the root logger for LOGOS.

    ##Step purpose: Sets up logging with stderr handler and optional file handler.

    ##Action purpose: Called automatically when the module is imported, but can be called
    again to reconfigure if environment variables change.
    """
    ##Action purpose: Get root logger for logos namespace
    root_logger = logging.getLogger("logos")

    ##Action purpose: Clear existing handlers to avoid duplicates
    root_logger.handlers.clear()

    ##Action purpose: Set logging level from environment
    level = _get_log_level()
    root_logger.setLevel(level)

    ##Action purpose: Create formatter for log messages
    formatter = logging.Formatter(LOG_FORMAT, LOG_DATE_FORMAT)

    ##Step purpose: Add stderr handler for console output
    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(level)
    stderr_handler.setFormatter(formatter)
    root_logger.addHandler(stderr_handler)

    ##Step purpose: Add file handler if configured
    log_file = _get_log_file()
    ##Condition purpose: Check if file logging is configured
    if log_file:
        try:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)
        except OSError as e:
            ##Error purpose: Handle file handler creation failures gracefully
            root_logger.warning("Could not open log file %s: %s", log_file, e)


def get_logger(name: str) -> logging.Logger:
    """
    ##Function purpose: Get a logger for a specific module.

    ##Action purpose: Creates child logger under logos namespace.

    Args:
        name: Module name (typically __name__)

    Returns:
        Logger instance configured for LOGOS
    """
    ##Action purpose: Ensure logging is configured before creating logger
    if not logging.getLogger("logos").handlers:
        configure_logging()

    ##Action purpose: Create child logger under logos namespace
    ##Condition purpose: Handle names that already start with logos
    if name.startswith("logos"):
        return logging.getLogger(name)
    return logging.getLogger(f"logos.{name}")


##Action purpose: Configure logging on import
configure_logging()
