"""
##Script function and purpose: Tests for CLI argument parsing.

Tests the logos.cli.args module including verbose/quiet flags,
version flag, verbosity state management, and config-driven defaults.
Phase 5 implementation.
"""

from logos.cli.args import (
    VERBOSITY_NORMAL,
    VERBOSITY_QUIET,
    VERBOSITY_VERBOSE,
    _get_config_verbosity,
    get_verbosity,
    is_quiet,
    is_verbose,
    parse_args,
)


class TestParseArgs:
    """Tests for parse_args function."""

    def test_default_args(self):
        """Test default arguments produce normal verbosity."""
        result = parse_args([])
        assert result.verbose is False
        assert result.quiet is False
        assert result.version is False

    def test_verbose_short_flag(self):
        """Test -v flag sets verbose."""
        result = parse_args(["-v"])
        assert result.verbose is True
        assert result.quiet is False

    def test_verbose_long_flag(self):
        """Test --verbose flag sets verbose."""
        result = parse_args(["--verbose"])
        assert result.verbose is True

    def test_quiet_short_flag(self):
        """Test -q flag sets quiet."""
        result = parse_args(["-q"])
        assert result.quiet is True
        assert result.verbose is False

    def test_quiet_long_flag(self):
        """Test --quiet flag sets quiet."""
        result = parse_args(["--quiet"])
        assert result.quiet is True

    def test_version_flag(self):
        """Test --version flag."""
        result = parse_args(["--version"])
        assert result.version is True

    def test_verbose_and_quiet_mutually_exclusive(self):
        """Test that -v and -q cannot be used together."""
        import pytest

        with pytest.raises(SystemExit):
            parse_args(["-v", "-q"])


class TestVerbosityState:
    """Tests for module-level verbosity state."""

    def test_default_verbosity(self):
        """Test default verbosity is normal."""
        parse_args([])
        assert get_verbosity() == VERBOSITY_NORMAL

    def test_verbose_sets_state(self):
        """Test verbose flag sets module state."""
        parse_args(["-v"])
        assert get_verbosity() == VERBOSITY_VERBOSE
        assert is_verbose() is True
        assert is_quiet() is False

    def test_quiet_sets_state(self):
        """Test quiet flag sets module state."""
        parse_args(["-q"])
        assert get_verbosity() == VERBOSITY_QUIET
        assert is_quiet() is True
        assert is_verbose() is False

    def test_normal_resets_state(self):
        """Test normal mode resets verbose/quiet state."""
        parse_args(["-v"])
        assert is_verbose() is True
        parse_args([])
        assert is_verbose() is False
        assert is_quiet() is False
        assert get_verbosity() == VERBOSITY_NORMAL

    def test_state_changes_between_calls(self):
        """Test that state changes correctly between parse_args calls."""
        parse_args(["-q"])
        assert is_quiet() is True
        parse_args(["-v"])
        assert is_verbose() is True
        assert is_quiet() is False


class TestConfigVerbosity:
    """Tests for config-driven verbosity defaults."""

    def test_config_verbosity_quiet(self, monkeypatch):
        """Test config verbosity=quiet is used when no CLI flag provided."""
        monkeypatch.setattr(
            "logos.cli.args._get_config_verbosity",
            lambda: VERBOSITY_QUIET,
        )
        parse_args([])
        assert get_verbosity() == VERBOSITY_QUIET

    def test_config_verbosity_verbose(self, monkeypatch):
        """Test config verbosity=verbose is used when no CLI flag provided."""
        monkeypatch.setattr(
            "logos.cli.args._get_config_verbosity",
            lambda: VERBOSITY_VERBOSE,
        )
        parse_args([])
        assert get_verbosity() == VERBOSITY_VERBOSE

    def test_cli_flag_overrides_config(self, monkeypatch):
        """Test CLI -v flag overrides config verbosity=quiet."""
        monkeypatch.setattr(
            "logos.cli.args._get_config_verbosity",
            lambda: VERBOSITY_QUIET,
        )
        parse_args(["-v"])
        assert get_verbosity() == VERBOSITY_VERBOSE

    def test_cli_quiet_overrides_config_verbose(self, monkeypatch):
        """Test CLI -q flag overrides config verbosity=verbose."""
        monkeypatch.setattr(
            "logos.cli.args._get_config_verbosity",
            lambda: VERBOSITY_VERBOSE,
        )
        parse_args(["-q"])
        assert get_verbosity() == VERBOSITY_QUIET

    def test_get_config_verbosity_returns_normal_on_error(self, monkeypatch):
        """Test _get_config_verbosity returns normal on import error."""
        monkeypatch.setattr(
            "logos.cli.args._get_config_verbosity",
            lambda: VERBOSITY_NORMAL,
        )
        result = _get_config_verbosity()
        assert result == VERBOSITY_NORMAL

    def test_get_config_verbosity_with_valid_config(self, tmp_path, monkeypatch):
        """Test _get_config_verbosity reads from config file."""
        import yaml

        from logos.cli.args import _get_config_verbosity

        config_dir = tmp_path / ".logos"
        config_dir.mkdir()
        config_file = config_dir / "config.yaml"
        config_file.write_text(yaml.dump({"verbosity": "quiet"}))
        monkeypatch.setattr("logos.core.config.get_config_path", lambda: config_file)
        result = _get_config_verbosity()
        assert result == VERBOSITY_QUIET

    def test_get_config_verbosity_invalid_value(self, tmp_path, monkeypatch):
        """Test _get_config_verbosity returns normal for invalid verbosity value."""
        import yaml

        from logos.cli.args import _get_config_verbosity

        config_dir = tmp_path / ".logos"
        config_dir.mkdir()
        config_file = config_dir / "config.yaml"
        config_file.write_text(yaml.dump({"verbosity": "invalid_level"}))
        monkeypatch.setattr("logos.core.config.get_config_path", lambda: config_file)
        result = _get_config_verbosity()
        assert result == VERBOSITY_NORMAL
