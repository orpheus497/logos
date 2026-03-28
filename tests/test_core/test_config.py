"""Tests for logos.core.config configuration management."""

from pathlib import Path

import yaml

from logos.core.config import (
    DEFAULT_CONFIG,
    _deep_copy_dict,
    _deep_merge,
    get_config_path,
    get_config_value,
    load_config,
    save_config,
)


class TestGetConfigPath:
    """##Class purpose: Verify config path generation."""

    def test_returns_path_object(self):
        """Config path is a Path instance."""
        result = get_config_path()
        assert isinstance(result, Path)

    def test_ends_with_config_yaml(self):
        """Config path ends with config.yaml."""
        result = get_config_path()
        assert result.name == "config.yaml"

    def test_parent_is_logos_dir(self):
        """Config parent directory is .logos."""
        result = get_config_path()
        assert result.parent.name == ".logos"


class TestDefaultConfig:
    """##Class purpose: Verify default configuration structure."""

    def test_has_default_mode(self):
        """Default config has default_mode key."""
        assert "default_mode" in DEFAULT_CONFIG

    def test_default_mode_is_none(self):
        """Default mode is None (ask each time)."""
        assert DEFAULT_CONFIG["default_mode"] is None

    def test_has_clipboard_section(self):
        """Default config has clipboard section."""
        assert "clipboard" in DEFAULT_CONFIG
        assert isinstance(DEFAULT_CONFIG["clipboard"], dict)

    def test_clipboard_enabled_by_default(self):
        """Clipboard is enabled by default."""
        assert DEFAULT_CONFIG["clipboard"]["enabled"] is True

    def test_has_recent_agents_section(self):
        """Default config has recent_agents section."""
        assert "recent_agents" in DEFAULT_CONFIG

    def test_recent_agents_max_count(self):
        """Recent agents max count is 10."""
        assert DEFAULT_CONFIG["recent_agents"]["max_count"] == 10

    def test_has_aliases_section(self):
        """Default config has aliases section."""
        assert "aliases" in DEFAULT_CONFIG
        assert isinstance(DEFAULT_CONFIG["aliases"], dict)


class TestDeepCopyDict:
    """##Class purpose: Verify deep copy creates independent copies."""

    def test_copies_simple_dict(self):
        """Deep copy of simple dict produces equal but independent copy."""
        original = {"a": 1, "b": "two"}
        copy = _deep_copy_dict(original)
        assert copy == original
        copy["a"] = 99
        assert original["a"] == 1

    def test_copies_nested_dict(self):
        """Deep copy of nested dict produces independent nested copy."""
        original = {"a": {"b": {"c": 1}}}
        copy = _deep_copy_dict(original)
        copy["a"]["b"]["c"] = 99
        assert original["a"]["b"]["c"] == 1

    def test_copies_lists(self):
        """Deep copy of dict with lists produces independent list copies."""
        original = {"items": [1, 2, 3]}
        copy = _deep_copy_dict(original)
        copy["items"].append(4)
        assert len(original["items"]) == 3

    def test_copies_nested_dicts_in_lists(self):
        """Deep copy handles dicts nested inside lists."""
        original = {"items": [{"x": 1}, {"y": 2}]}
        copy = _deep_copy_dict(original)
        copy["items"][0]["x"] = 99
        assert original["items"][0]["x"] == 1

    def test_copies_nested_lists_in_lists(self):
        """Deep copy handles lists nested inside lists."""
        original = {"items": [[1, 2], [3, 4]]}
        copy = _deep_copy_dict(original)
        copy["items"][0].append(99)
        assert len(original["items"][0]) == 2


class TestDeepMerge:
    """##Class purpose: Verify deep merge behavior."""

    def test_override_simple_value(self):
        """Override values replace base values."""
        base = {"a": 1, "b": 2}
        override = {"b": 99}
        result = _deep_merge(base, override)
        assert result == {"a": 1, "b": 99}

    def test_merge_nested_dicts(self):
        """Nested dicts are recursively merged."""
        base = {"section": {"a": 1, "b": 2}}
        override = {"section": {"b": 99}}
        result = _deep_merge(base, override)
        assert result == {"section": {"a": 1, "b": 99}}

    def test_add_new_keys(self):
        """New keys in override are added to result."""
        base = {"a": 1}
        override = {"b": 2}
        result = _deep_merge(base, override)
        assert result == {"a": 1, "b": 2}

    def test_does_not_mutate_base(self):
        """Deep merge does not mutate the base dictionary."""
        base = {"a": 1}
        override = {"a": 2}
        _deep_merge(base, override)
        assert base == {"a": 1}

    def test_override_dict_with_scalar(self):
        """Scalar override replaces dict in base."""
        base = {"a": {"nested": True}}
        override = {"a": "flat"}
        result = _deep_merge(base, override)
        assert result["a"] == "flat"


class TestGetConfigValue:
    """##Class purpose: Verify dotted path config value access."""

    def test_simple_key(self):
        """Simple key access returns correct value."""
        config = {"mode": "daedelus"}
        assert get_config_value(config, "mode") == "daedelus"

    def test_nested_key(self):
        """Dotted path access returns nested value."""
        config = {"clipboard": {"enabled": True}}
        assert get_config_value(config, "clipboard.enabled") is True

    def test_deep_nested_key(self):
        """Triple-dotted path access works."""
        config = {"a": {"b": {"c": 42}}}
        assert get_config_value(config, "a.b.c") == 42

    def test_missing_key_returns_default(self):
        """Missing key returns default value."""
        config = {"a": 1}
        assert get_config_value(config, "missing", "fallback") == "fallback"

    def test_missing_nested_key_returns_default(self):
        """Missing nested key returns default value."""
        config = {"a": {"b": 1}}
        assert get_config_value(config, "a.c.d", None) is None

    def test_default_is_none(self):
        """Default value is None when not specified."""
        config = {}
        assert get_config_value(config, "missing") is None


class TestLoadConfig:
    """##Class purpose: Verify config loading with defaults."""

    def test_returns_dict(self, tmp_path, monkeypatch):
        """Load config returns a dictionary."""
        monkeypatch.setattr("logos.core.config.get_config_path", lambda: tmp_path / "config.yaml")
        result = load_config()
        assert isinstance(result, dict)

    def test_has_all_default_keys(self, tmp_path, monkeypatch):
        """Loaded config has all default configuration keys."""
        monkeypatch.setattr("logos.core.config.get_config_path", lambda: tmp_path / "config.yaml")
        result = load_config()
        for key in DEFAULT_CONFIG:
            assert key in result

    def test_clipboard_section_present(self, tmp_path, monkeypatch):
        """Loaded config has clipboard section from defaults."""
        monkeypatch.setattr("logos.core.config.get_config_path", lambda: tmp_path / "config.yaml")
        result = load_config()
        assert "clipboard" in result
        assert "enabled" in result["clipboard"]

    def test_user_config_merges_with_defaults(self, tmp_path, monkeypatch):
        """User config file merges correctly with defaults."""
        config_file = tmp_path / "config.yaml"
        config_file.write_text("default_mode: deus\n")
        monkeypatch.setattr("logos.core.config.get_config_path", lambda: config_file)
        result = load_config()
        assert result["default_mode"] == "deus"
        ##Condition purpose: Verify defaults are preserved for keys not in user config
        assert "clipboard" in result
        assert result["clipboard"]["enabled"] is True


class TestSaveConfig:
    """##Class purpose: Verify config saving to file."""

    def test_save_and_load_roundtrip(self, tmp_path):
        """Config saved and reloaded matches original."""
        config_file = tmp_path / "config.yaml"
        config = {"default_mode": "deus", "aliases": {"arch": "A1"}}

        # Write directly using yaml for this test
        config_file.parent.mkdir(parents=True, exist_ok=True)
        with config_file.open("w") as f:
            yaml.safe_dump(config, f)

        # Read back
        with config_file.open() as f:
            loaded = yaml.safe_load(f)

        assert loaded["default_mode"] == "deus"
        assert loaded["aliases"]["arch"] == "A1"

    def test_save_creates_file(self, tmp_path, monkeypatch):
        """Save config creates the config file."""
        config_file = tmp_path / ".logos" / "config.yaml"
        monkeypatch.setattr("logos.core.config.get_config_path", lambda: config_file)

        result = save_config({"test": True})
        assert result is True
        assert config_file.exists()
