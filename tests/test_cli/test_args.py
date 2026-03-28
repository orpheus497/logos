"""
##Script function and purpose: Tests for CLI argument parsing.

Tests the logos.cli.args module including verbose/quiet flags,
version flag, and verbosity state management.
Phase 5 implementation.
"""

from logos.cli.args import (
    VERBOSITY_NORMAL,
    VERBOSITY_QUIET,
    VERBOSITY_VERBOSE,
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
