"""
##Script function and purpose: Tests for version module.

Tests the logos.core.version module.
Phase 5 implementation.
"""

from logos.core.version import VERSION, get_version


class TestVersion:
    """Tests for version module."""

    def test_version_string_exists(self):
        """Test VERSION constant is a non-empty string."""
        assert isinstance(VERSION, str)
        assert len(VERSION) > 0

    def test_get_version_returns_string(self):
        """Test get_version returns a string."""
        result = get_version()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_get_version_matches_constant(self):
        """Test get_version returns same value as VERSION constant."""
        assert get_version() == VERSION

    def test_version_format(self):
        """Test version follows semver-like format."""
        version = get_version()
        # Should contain at least one dot (major.minor)
        assert "." in version
        # Should start with a digit
        assert version[0].isdigit()
