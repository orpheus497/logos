"""Tests for logos.cli.layouts display width helpers."""

import pytest

from logos.cli.layouts import _display_width


try:
    from wcwidth import wcswidth as _wcswidth
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
        """##Function purpose: String with only combining chars triggers len() fallback."""
        combining_only = "\u0300"
        result = _display_width(combining_only)
        # wcswidth returns -1 for combining-only strings (or wcwidth not installed) → fallback to len()
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
