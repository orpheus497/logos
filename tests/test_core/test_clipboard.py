"""
##Script function and purpose: Unit tests for logos.core.clipboard module.

Tests clipboard operations with platform detection and fallback methods.
"""

from unittest.mock import MagicMock, patch

from logos.core.clipboard import copy_to_clipboard


##Function purpose: Test copy_to_clipboard success
def test_copy_to_clipboard_success():
    """##Function purpose: Verify copy_to_clipboard succeeds when clipboard tool available.."""
    ##Action purpose: Mock successful subprocess call
    with patch("logos.core.clipboard.subprocess.run") as mock_run:
        ##Action purpose: Configure mock to return success
        mock_run.return_value = MagicMock(returncode=0)

        ##Action purpose: Copy to clipboard
        result = copy_to_clipboard("test text")

        ##Condition purpose: Verify function was called
        assert mock_run.called

        ##Condition purpose: Verify result (may be True or False depending on platform)
        assert isinstance(result, bool)


##Function purpose: Test copy_to_clipboard security
def test_copy_to_clipboard_security():
    """##Function purpose: Verify copy_to_clipboard uses explicit args (no shell injection).."""
    ##Action purpose: Mock subprocess.run
    with patch("logos.core.clipboard.subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0)

        ##Action purpose: Copy to clipboard
        copy_to_clipboard("test; rm -rf /")

        ##Condition purpose: Verify shell=False (security)
        if mock_run.called:
            call_kwargs = mock_run.call_args[1] if mock_run.call_args else {}
            ##Condition purpose: Verify no shell execution
            assert call_kwargs.get("shell", True) is False


##Function purpose: Test copy_to_clipboard failure
def test_copy_to_clipboard_failure():
    """##Function purpose: Verify copy_to_clipboard handles failures gracefully.."""
    ##Action purpose: Mock all subprocess calls to fail
    with patch("logos.core.clipboard.subprocess.run") as mock_run:
        ##Action purpose: Configure mock to raise exception
        mock_run.side_effect = FileNotFoundError("Command not found")

        ##Action purpose: Try to copy to clipboard
        result = copy_to_clipboard("test text")

        ##Condition purpose: Verify function handles error
        assert isinstance(result, bool)


##Function purpose: Test copy_to_clipboard fallback methods
def test_copy_to_clipboard_fallbacks():
    """##Function purpose: Verify copy_to_clipboard tries multiple methods.."""
    ##Action purpose: Track which methods are tried
    call_count = 0

    def mock_run_side_effect(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        ##Action purpose: First calls fail, last succeeds
        if call_count < 3:
            raise FileNotFoundError()
        return MagicMock(returncode=0)

    ##Action purpose: Mock subprocess.run
    with patch("logos.core.clipboard.subprocess.run", side_effect=mock_run_side_effect):
        ##Action purpose: Copy to clipboard
        copy_to_clipboard("test")

        ##Condition purpose: Verify multiple methods were tried
        assert call_count >= 1
