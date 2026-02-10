"""
##Script function and purpose: Unit tests for logos.cli.layouts module.

Tests layout and display functions including system information display.
"""

import sys
from io import StringIO
from unittest.mock import patch

from logos.cli.layouts import (
    _wrap_text,
    display_logos_banner,
    display_system_info,
    get_logos_banner,
)
from logos.core.constants import UILayout
from logos.core.identity import SystemIdentity


##Function purpose: Test display_system_info displays system information
def test_display_system_info_displays_info():
    """##Function purpose: Verify display_system_info displays system information without errors."""
    ##Action purpose: Create test identity
    identity = SystemIdentity(
        hostname="testhost",
        username="testuser",
        os_name="Linux",
        os_version="5.15.0",
        faction="orphic",
        created_at="2026-01-20T12:00:00Z",
        last_session="2026-01-20T12:00:00Z",
    )

    ##Action purpose: Capture stdout
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        ##Action purpose: Mock scan_system to return test data
        with patch("logos.core.identity.scan_system") as mock_scan:
            mock_scan.return_value = {
                "python_version": "3.11.0",
                "logos_config_exists": True,
                "devdocs_exists": True,
                "sysdocs_exists": False,
            }

            ##Action purpose: Display system info
            display_system_info(identity)

            ##Action purpose: Get output
            output = sys.stdout.getvalue()

            ##Condition purpose: Verify output contains expected elements
            assert "SYSTEM INFORMATION" in output
            assert "testhost" in output
            assert "testuser" in output
            assert "Linux" in output
            assert "5.15.0" in output
    finally:
        ##Action purpose: Restore stdout
        sys.stdout = old_stdout


##Function purpose: Test display_system_info displays date and time
def test_display_system_info_displays_date_time():
    """##Function purpose: Verify display_system_info displays date and time information."""
    ##Action purpose: Create test identity
    identity = SystemIdentity(
        hostname="testhost",
        username="testuser",
        os_name="Linux",
        os_version="5.15.0",
        faction="orphic",
        created_at="2026-01-20T12:00:00Z",
        last_session="2026-01-20T12:00:00Z",
    )

    ##Action purpose: Capture stdout
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        ##Action purpose: Mock scan_system
        with patch("logos.core.identity.scan_system") as mock_scan:
            mock_scan.return_value = {
                "python_version": "3.11.0",
                "logos_config_exists": True,
                "devdocs_exists": True,
                "sysdocs_exists": False,
            }

            ##Action purpose: Display system info
            display_system_info(identity)

            ##Action purpose: Get output
            output = sys.stdout.getvalue()

            ##Condition purpose: Verify date and time sections present
            assert "Date and Time" in output
            assert "UTC Date" in output
            assert "UTC Time" in output
            assert "UTC DateTime" in output
            assert "Local Date" in output
            assert "Local Time" in output
            assert "Local DateTime" in output
            assert "Timezone" in output
    finally:
        ##Action purpose: Restore stdout
        sys.stdout = old_stdout


##Function purpose: Test display_system_info displays timezone
def test_display_system_info_displays_timezone():
    """##Function purpose: Verify display_system_info displays timezone information."""
    ##Action purpose: Create test identity
    identity = SystemIdentity(
        hostname="testhost",
        username="testuser",
        os_name="Linux",
        os_version="5.15.0",
        faction="orphic",
        created_at="2026-01-20T12:00:00Z",
        last_session="2026-01-20T12:00:00Z",
    )

    ##Action purpose: Capture stdout
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        ##Action purpose: Mock scan_system
        with patch("logos.core.identity.scan_system") as mock_scan:
            mock_scan.return_value = {
                "python_version": "3.11.0",
                "logos_config_exists": True,
                "devdocs_exists": True,
                "sysdocs_exists": False,
            }

            ##Action purpose: Display system info
            display_system_info(identity)

            ##Action purpose: Get output
            output = sys.stdout.getvalue()

            ##Condition purpose: Verify timezone information displayed
            assert "Timezone:" in output
    finally:
        ##Action purpose: Restore stdout
        sys.stdout = old_stdout


##Function purpose: Test display_system_info displays Python environment
def test_display_system_info_displays_python_env():
    """##Function purpose: Verify display_system_info displays Python environment information."""
    ##Action purpose: Create test identity
    identity = SystemIdentity(
        hostname="testhost",
        username="testuser",
        os_name="Linux",
        os_version="5.15.0",
        faction="orphic",
        created_at="2026-01-20T12:00:00Z",
        last_session="2026-01-20T12:00:00Z",
    )

    ##Action purpose: Capture stdout
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        ##Action purpose: Mock scan_system with Python version
        with patch("logos.core.identity.scan_system") as mock_scan:
            mock_scan.return_value = {
                "python_version": "3.11.0",
                "logos_config_exists": True,
                "devdocs_exists": True,
                "sysdocs_exists": False,
            }

            ##Action purpose: Display system info
            display_system_info(identity)

            ##Action purpose: Get output
            output = sys.stdout.getvalue()

            ##Condition purpose: Verify Python environment section present
            assert "Python Environment" in output
            assert "Python Version" in output
            assert "3.11.0" in output
    finally:
        ##Action purpose: Restore stdout
        sys.stdout = old_stdout


##Function purpose: Test display_system_info displays LOGOS state
def test_display_system_info_displays_logos_state():
    """##Function purpose: Verify display_system_info displays LOGOS state information."""
    ##Action purpose: Create test identity
    identity = SystemIdentity(
        hostname="testhost",
        username="testuser",
        os_name="Linux",
        os_version="5.15.0",
        faction="orphic",
        created_at="2026-01-20T12:00:00Z",
        last_session="2026-01-20T12:00:00Z",
    )

    ##Action purpose: Capture stdout
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        ##Action purpose: Mock scan_system with LOGOS state
        with patch("logos.core.identity.scan_system") as mock_scan:
            mock_scan.return_value = {
                "python_version": "3.11.0",
                "logos_config_exists": True,
                "devdocs_exists": True,
                "sysdocs_exists": False,
            }

            ##Action purpose: Display system info
            display_system_info(identity)

            ##Action purpose: Get output
            output = sys.stdout.getvalue()

            ##Condition purpose: Verify LOGOS state section present
            assert "LOGOS State" in output
            assert "LOGOS configuration" in output or "LOGOS config" in output
            assert "Development docs" in output or "devdocs" in output
    finally:
        ##Action purpose: Restore stdout
        sys.stdout = old_stdout


##Function purpose: Test display_system_info handles missing scan data
def test_display_system_info_handles_missing_data():
    """##Function purpose: Verify display_system_info handles missing scan data gracefully."""
    ##Action purpose: Create test identity
    identity = SystemIdentity(
        hostname="testhost",
        username="testuser",
        os_name="Linux",
        os_version="5.15.0",
        faction="orphic",
        created_at="2026-01-20T12:00:00Z",
        last_session="2026-01-20T12:00:00Z",
    )

    ##Action purpose: Capture stdout
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        ##Action purpose: Mock scan_system to return minimal data
        with patch("logos.core.identity.scan_system") as mock_scan:
            mock_scan.return_value = {}

            ##Action purpose: Display system info (should not crash)
            display_system_info(identity)

            ##Action purpose: Get output
            output = sys.stdout.getvalue()

            ##Condition purpose: Verify output still contains basic info
            assert "SYSTEM INFORMATION" in output
            assert "testhost" in output
            assert "testuser" in output
    finally:
        ##Action purpose: Restore stdout
        sys.stdout = old_stdout


##Function purpose: Test _wrap_text function
def test_wrap_text_short_text():
    """##Function purpose: Verify _wrap_text handles short text that fits within width.."""
    ##Action purpose: Wrap short text
    text = "Short text"
    wrapped = _wrap_text(text, 100)

    ##Condition purpose: Verify text is not split
    assert len(wrapped) == 1
    assert wrapped[0] == "Short text"


##Function purpose: Test _wrap_text function with long text
def test_wrap_text_long_text():
    """##Function purpose: Verify _wrap_text wraps long text to fit within width.."""
    ##Action purpose: Wrap long text that exceeds the specified width
    text = "This is a very long text that should be wrapped to fit within the specified width of only fifty characters maximum"
    wrapped = _wrap_text(text, 50)

    ##Condition purpose: Verify text is wrapped into multiple lines
    assert len(wrapped) > 1
    ##Condition purpose: Verify each line is within width
    for line in wrapped:
        assert len(line) <= 50


##Function purpose: Test _wrap_text function with exact width
def test_wrap_text_exact_width():
    """##Function purpose: Verify _wrap_text handles text that exactly fits width.."""
    ##Action purpose: Wrap text that exactly fits
    text = "A" * 100
    wrapped = _wrap_text(text, 100)

    ##Condition purpose: Verify text fits in one line
    assert len(wrapped) == 1
    assert len(wrapped[0]) == 100


##Function purpose: Test get_logos_banner function
def test_get_logos_banner():
    """##Function purpose: Verify get_logos_banner returns banner lines.."""
    ##Action purpose: Get LOGOS banner
    banner = get_logos_banner()

    ##Condition purpose: Verify banner is a list
    assert isinstance(banner, list)
    ##Condition purpose: Verify banner has content
    assert len(banner) > 0
    ##Condition purpose: Verify all lines are strings
    for line in banner:
        assert isinstance(line, str)


##Function purpose: Test get_logos_banner contains LOGOS text
def test_get_logos_banner_contains_logos():
    """##Function purpose: Verify get_logos_banner contains LOGOS text.."""
    ##Action purpose: Get LOGOS banner
    banner = get_logos_banner()
    banner_text = "\n".join(banner)

    ##Condition purpose: Verify banner contains L O G O S letters in spaced format
    # Banner has letters spaced out like "    L      O      G      O      S"
    # Check that the spaced pattern exists in the last line
    assert len(banner) > 0
    last_line = banner[-1] if banner else ""
    # Check for the spaced LOGOS pattern (with multiple spaces between letters)
    import re
    # Pattern matches "L", then spaces, then "O", then spaces, etc.
    spaced_pattern = r"L\s+O\s+G\s+O\s+S"
    assert re.search(spaced_pattern, last_line), f"Expected spaced 'L O G O S' pattern in banner, got: {last_line}"


##Function purpose: Test display_logos_banner displays banner
def test_display_logos_banner():
    """##Function purpose: Verify display_logos_banner displays banner without errors.."""
    ##Action purpose: Capture stdout
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        ##Action purpose: Display LOGOS banner
        display_logos_banner(width=100)

        ##Action purpose: Get output
        output = sys.stdout.getvalue()

        ##Condition purpose: Verify output contains banner content
        assert len(output) > 0
    finally:
        ##Action purpose: Restore stdout
        sys.stdout = old_stdout


##Function purpose: Test display_logos_banner with custom width
def test_display_logos_banner_custom_width():
    """##Function purpose: Verify display_logos_banner respects width parameter.."""
    ##Action purpose: Capture stdout
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        ##Action purpose: Display LOGOS banner with custom width
        display_logos_banner(width=UILayout.DISPLAY_WIDTH)

        ##Action purpose: Get output
        output = sys.stdout.getvalue()

        ##Condition purpose: Verify output is generated
        assert len(output) > 0
    finally:
        ##Action purpose: Restore stdout
        sys.stdout = old_stdout
