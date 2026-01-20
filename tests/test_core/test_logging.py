"""
##Script function and purpose: Unit tests for logos.core.logging module.

Tests logging configuration, environment variable handling, and logger creation.
"""

import logging
import os
from unittest.mock import patch

from logos.core.logging import configure_logging, get_logger


##Function purpose: Test get_logger
def test_get_logger():
    """##Function purpose: Verify get_logger creates logger with correct name.."""
    ##Action purpose: Get logger
    logger = get_logger("test_module")

    ##Condition purpose: Verify logger is created
    assert isinstance(logger, logging.Logger)
    assert logger.name == "logos.test_module"


##Function purpose: Test logger reuse
def test_logger_reuse():
    """##Function purpose: Verify same name returns same logger instance.."""
    ##Action purpose: Get logger twice with same name
    logger1 = get_logger("test_module")
    logger2 = get_logger("test_module")

    ##Condition purpose: Verify same logger instance
    assert logger1 is logger2


##Function purpose: Test configure_logging
def test_configure_logging():
    """##Function purpose: Verify configure_logging sets up logging correctly.."""
    ##Action purpose: Configure logging
    configure_logging()

    ##Action purpose: Get logger
    logger = get_logger("test")

    ##Condition purpose: Verify logger is configured
    assert logger.level >= logging.DEBUG


##Function purpose: Test environment variable log level
def test_log_level_environment_variable():
    """##Function purpose: Verify LOGOS_LOG_LEVEL environment variable is respected.."""
    ##Action purpose: Set environment variable
    with patch.dict(os.environ, {"LOGOS_LOG_LEVEL": "ERROR"}):
        ##Action purpose: Reconfigure logging
        configure_logging()

        ##Action purpose: Get logger
        logger = get_logger("test_env")

        ##Condition purpose: Verify log level is set
        assert logger.level >= logging.ERROR


##Function purpose: Test default log level
def test_default_log_level():
    """##Function purpose: Verify default log level when environment variable not set.."""
    ##Action purpose: Remove environment variable if set
    with patch.dict(os.environ, {}, clear=True):
        ##Action purpose: Reconfigure logging
        configure_logging()

        ##Action purpose: Get logger
        logger = get_logger("test_default")

        ##Condition purpose: Verify logger has valid level
        assert logger.level in [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]
