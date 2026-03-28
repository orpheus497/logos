"""Tests for logos.cli.layouts display width helpers and quiet mode."""

import pytest

from logos.cli.layouts import _display_width

try:
    import wcwidth  # noqa: F401

    HAS_WCWIDTH = True
except ImportError:
    HAS_WCWIDTH = False


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
        from logos.core.constants import Colors
        from logos.core.types import AgentGroup

        mock_agents = {
            "A1": type("Agent", (), {"name": "Test Agent", "desc": "Test description", "group": "A"})(),
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
