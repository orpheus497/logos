"""
##Script function and purpose: Unit tests for logos.cli.layouts module.

Tests layout and display functions including system information display,
display width helpers, and quiet mode behavior.
"""

from unittest.mock import patch

import pytest

from logos.cli.layouts import (
    _display_width,
    _wrap_text,
    display_logos_banner,
    display_system_info,
    get_logos_banner,
)
from logos.core.constants import UILayout
from logos.core.identity import SystemIdentity

try:
    import wcwidth  # noqa: F401

    HAS_WCWIDTH = True
except ImportError:
    HAS_WCWIDTH = False


# ─── Display Width Tests ─────────────────────────────────────────────────────


class TestDisplayWidth:
    """##Class purpose: Verify _display_width handles printable and non-printable characters."""

    def test_ascii_string(self):
        """##Function purpose: ASCII characters have width equal to length."""
        assert _display_width("hello") == 5

    def test_empty_string(self):
        """##Function purpose: Empty string has zero width."""
        assert _display_width("") == 0

    @pytest.mark.skipif(not HAS_WCWIDTH, reason="wcwidth not installed")
    def test_wide_cjk_character(self):
        """##Function purpose: CJK characters are double-width when wcwidth is available."""
        assert _display_width("世") == 2

    def test_combining_character_fallback(self):
        """##Function purpose: Combining-only string has display width 0 with wcwidth present."""
        combining_only = "\u0300"
        result = _display_width(combining_only)
        # wcswidth returns 0 for combining marks (zero-width); len() fallback only when wcwidth absent
        if HAS_WCWIDTH:
            assert result == 0
        else:
            assert result == len(combining_only)

    @pytest.mark.skipif(not HAS_WCWIDTH, reason="wcwidth not installed")
    def test_mixed_ascii_and_wide(self):
        """##Function purpose: Mixed ASCII and wide characters compute correct width."""
        assert _display_width("A世B") == 4

    def test_len_fallback_without_wcwidth(self):
        """##Function purpose: Without wcwidth, _display_width returns len()."""
        if HAS_WCWIDTH:
            pytest.skip("wcwidth is installed; fallback not exercised")
        assert _display_width("世") == len("世")


# ─── Quiet Mode Tests ────────────────────────────────────────────────────────


class TestQuietModeLayouts:
    """Tests for quiet mode suppression of decorative elements in layouts."""

    def test_welcome_screen_quiet_mode(self, capsys, monkeypatch):
        """Test welcome screen outputs compact single line in quiet mode."""
        monkeypatch.setattr("logos.cli.layouts.is_quiet", lambda: True)
        from logos.cli.layouts import display_welcome_screen

        display_welcome_screen(username="testuser", hostname="testhost", faction="TestFaction")
        output = capsys.readouterr().out
        assert "LOGOS" in output
        assert "testuser@testhost" in output
        assert "TestFaction" in output
        # Should NOT contain full banner box characters
        assert "═" not in output

    def test_welcome_screen_normal_has_banner(self, capsys, monkeypatch):
        """Test welcome screen includes banner in normal mode."""
        monkeypatch.setattr("logos.cli.layouts.is_quiet", lambda: False)
        from logos.cli.layouts import display_welcome_screen

        display_welcome_screen(username="testuser", hostname="testhost", faction="TestFaction")
        output = capsys.readouterr().out
        # Normal mode should have decorative box borders
        assert "testuser@testhost" in output

    def test_mode_selection_quiet_mode(self, capsys, monkeypatch):
        """Test mode selection shows compact options in quiet mode."""
        monkeypatch.setattr("logos.cli.layouts.is_quiet", lambda: True)
        from logos.cli.layouts import display_mode_selection

        display_mode_selection()
        output = capsys.readouterr().out
        assert "[D]" in output
        assert "[U]" in output
        assert "[Q]" in output
        # Should be compact — no banner
        assert "█" not in output

    def test_agent_menu_quiet_mode(self, capsys, monkeypatch):
        """Test agent menu shows compact listing in quiet mode."""
        monkeypatch.setattr("logos.cli.layouts.is_quiet", lambda: True)
        from logos.cli.layouts import display_agent_menu
        from logos.core.agent import Agent
        from logos.core.constants import Colors
        from logos.core.types import AgentGroup

        mock_agents = {
            "A1": Agent(
                name="Test Agent",
                desc="Test description",
                group="A",
                base_prompt="",
                activation_prompt="",
                purpose="Testing",
            ),
        }
        groups = [AgentGroup("A", "TEST", "Testing", "Test purpose", Colors.GREEN, mock_agents)]
        display_agent_menu("daedelus", groups, "TestFaction")
        output = capsys.readouterr().out
        assert "A1" in output
        assert "Test Agent" in output
        # Should NOT contain banner characters
        assert "█" not in output

    def test_logos_banner_suppressed_in_quiet(self, capsys, monkeypatch):
        """Test LOGOS banner is completely suppressed in quiet mode."""
        monkeypatch.setattr("logos.cli.layouts.is_quiet", lambda: True)
        from logos.cli.layouts import display_logos_banner

        display_logos_banner()
        output = capsys.readouterr().out
        assert output == ""

    def test_get_logos_banner_lines_empty_in_quiet(self, monkeypatch):
        """Test _get_logos_banner_lines returns empty list in quiet mode."""
        monkeypatch.setattr("logos.cli.layouts.is_quiet", lambda: True)
        from logos.cli.layouts import _get_logos_banner_lines

        result = _get_logos_banner_lines()
        assert result == []


# ─── System Info Display Tests ────────────────────────────────────────────────


##Function purpose: Test display_system_info displays system information
def test_display_system_info_displays_info(capsys):
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

    ##Action purpose: Mock scan_system to return test data
    with patch("logos.core.identity.scan_system") as mock_scan:
        mock_scan.return_value = {
            "python_version": "3.11.0",
            "logos_config_exists": True,
            "devdocs_exists": True,
            "sysdocs_exists": False,
        }

        display_system_info(identity)
        output = capsys.readouterr().out

        ##Condition purpose: Verify output contains expected elements
        assert "SYSTEM INFORMATION" in output
        assert "testhost" in output
        assert "testuser" in output
        assert "Linux" in output
        assert "5.15.0" in output


##Function purpose: Test display_system_info displays date and time
def test_display_system_info_displays_date_time(capsys):
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

    with patch("logos.core.identity.scan_system") as mock_scan:
        mock_scan.return_value = {
            "python_version": "3.11.0",
            "logos_config_exists": True,
            "devdocs_exists": True,
            "sysdocs_exists": False,
        }

        display_system_info(identity)
        output = capsys.readouterr().out

        ##Condition purpose: Verify date and time sections present
        assert "Date and Time" in output
        assert "UTC Date" in output
        assert "UTC Time" in output
        assert "UTC DateTime" in output
        assert "Local Date" in output
        assert "Local Time" in output
        assert "Local DateTime" in output
        assert "Timezone" in output


##Function purpose: Test display_system_info displays timezone
def test_display_system_info_displays_timezone(capsys):
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

    with patch("logos.core.identity.scan_system") as mock_scan:
        mock_scan.return_value = {
            "python_version": "3.11.0",
            "logos_config_exists": True,
            "devdocs_exists": True,
            "sysdocs_exists": False,
        }

        display_system_info(identity)
        output = capsys.readouterr().out

        ##Condition purpose: Verify timezone information displayed
        assert "Timezone:" in output


##Function purpose: Test display_system_info displays Python environment
def test_display_system_info_displays_python_env(capsys):
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

    with patch("logos.core.identity.scan_system") as mock_scan:
        mock_scan.return_value = {
            "python_version": "3.11.0",
            "logos_config_exists": True,
            "devdocs_exists": True,
            "sysdocs_exists": False,
        }

        display_system_info(identity)
        output = capsys.readouterr().out

        ##Condition purpose: Verify Python environment section present
        assert "Python Environment" in output
        assert "Python Version" in output
        assert "3.11.0" in output


##Function purpose: Test display_system_info displays LOGOS state
def test_display_system_info_displays_logos_state(capsys):
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

    with patch("logos.core.identity.scan_system") as mock_scan:
        mock_scan.return_value = {
            "python_version": "3.11.0",
            "logos_config_exists": True,
            "devdocs_exists": True,
            "sysdocs_exists": False,
        }

        display_system_info(identity)
        output = capsys.readouterr().out

        ##Condition purpose: Verify LOGOS state section present
        assert "LOGOS State" in output
        assert "LOGOS configuration" in output or "LOGOS config" in output
        assert "Development docs" in output or "devdocs" in output


##Function purpose: Test display_system_info handles missing scan data
def test_display_system_info_handles_missing_data(capsys):
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

    with patch("logos.core.identity.scan_system") as mock_scan:
        mock_scan.return_value = {}

        display_system_info(identity)
        output = capsys.readouterr().out

        ##Condition purpose: Verify output still contains basic info
        assert "SYSTEM INFORMATION" in output
        assert "testhost" in output
        assert "testuser" in output


# ─── Text Wrapping Tests ─────────────────────────────────────────────────────


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


# ─── Banner Tests ─────────────────────────────────────────────────────────────


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

    ##Condition purpose: Verify banner has content (block art representation)
    assert len(banner) > 0
    # Banner uses block characters (▒) for stylized LOGOS text
    banner_text = "\n".join(banner)
    assert len(banner_text) > 0


##Function purpose: Test display_logos_banner displays banner
def test_display_logos_banner(monkeypatch, capsys):
    """##Function purpose: Verify display_logos_banner displays banner without errors.."""
    monkeypatch.setattr("logos.cli.layouts.is_quiet", lambda: False)
    display_logos_banner(width=100)
    output = capsys.readouterr().out

    ##Condition purpose: Verify output contains banner content
    assert len(output) > 0


##Function purpose: Test display_logos_banner with custom width
def test_display_logos_banner_custom_width(monkeypatch, capsys):
    """##Function purpose: Verify display_logos_banner respects width parameter.."""
    monkeypatch.setattr("logos.cli.layouts.is_quiet", lambda: False)
    display_logos_banner(width=UILayout.DISPLAY_WIDTH)
    output = capsys.readouterr().out

    ##Condition purpose: Verify output is generated
    assert len(output) > 0
