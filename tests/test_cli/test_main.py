"""Tests for logos.cli.main CLI entry point."""

from logos.cli.main import is_first_run, main


class TestIsFirstRun:
    """##Class purpose: Verify first-run detection logic."""

    def test_first_run_without_identity(self, tmp_path, monkeypatch):
        """First run detected when identity file does not exist."""
        monkeypatch.setattr(
            "logos.cli.main.get_identity_path",
            lambda: tmp_path / "nonexistent" / "identity.yaml",
        )
        assert is_first_run() is True

    def test_not_first_run_with_identity(self, tmp_path, monkeypatch):
        """Not first run when identity file exists."""
        identity_file = tmp_path / "identity.yaml"
        identity_file.write_text("test: true")
        monkeypatch.setattr("logos.cli.main.get_identity_path", lambda: identity_file)
        assert is_first_run() is False


class TestMainFunction:
    """##Class purpose: Verify main CLI entry point behavior."""

    def test_main_returns_int(self, monkeypatch):
        """Main function returns an integer exit code."""
        # Simulate first run that gets cancelled
        monkeypatch.setattr("logos.cli.main.is_first_run", lambda: True)
        monkeypatch.setattr("logos.cli.main.clear_screen", lambda: None)
        monkeypatch.setattr("logos.cli.main.run_first_run_wizard", lambda: False)
        result = main()
        assert isinstance(result, int)

    def test_main_cancelled_wizard_returns_1(self, monkeypatch):
        """Cancelled first-run wizard returns exit code 1."""
        monkeypatch.setattr("logos.cli.main.is_first_run", lambda: True)
        monkeypatch.setattr("logos.cli.main.clear_screen", lambda: None)
        monkeypatch.setattr("logos.cli.main.run_first_run_wizard", lambda: False)
        assert main() == 1

    def test_main_handles_keyboard_interrupt(self, monkeypatch):
        """KeyboardInterrupt is handled gracefully with exit code 0."""
        monkeypatch.setattr("logos.cli.main.clear_screen", _raise_keyboard_interrupt)
        result = main()
        assert result == 0

    def test_main_handles_os_error(self, monkeypatch):
        """OSError returns exit code 1."""

        def raise_os_error():
            raise OSError("test error")

        monkeypatch.setattr("logos.cli.main.clear_screen", raise_os_error)
        result = main()
        assert result == 1

    def test_main_handles_value_error(self, monkeypatch):
        """ValueError returns exit code 1."""

        def raise_value_error():
            raise ValueError("test error")

        monkeypatch.setattr("logos.cli.main.clear_screen", raise_value_error)
        result = main()
        assert result == 1


def _raise_keyboard_interrupt():
    """Helper to raise KeyboardInterrupt."""
    raise KeyboardInterrupt()
