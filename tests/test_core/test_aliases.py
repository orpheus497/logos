"""Tests for logos.core.aliases agent alias system."""

from logos.core.aliases import (
    DAEDELUS_ALIASES,
    DEUS_ALIASES,
    _get_builtin_aliases,
    get_all_aliases,
    resolve_alias,
    validate_custom_aliases,
)


class TestBuiltinAliases:
    """##Class purpose: Verify built-in alias dictionaries are well-formed."""

    def test_daedelus_aliases_not_empty(self):
        """Daedelus aliases dictionary is not empty."""
        assert len(DAEDELUS_ALIASES) > 0

    def test_deus_aliases_not_empty(self):
        """DEUS aliases dictionary is not empty."""
        assert len(DEUS_ALIASES) > 0

    def test_daedelus_aliases_cover_all_groups(self):
        """Daedelus aliases include agents from all 5 groups."""
        values = set(DAEDELUS_ALIASES.values())
        groups = {v[0] for v in values}
        assert groups == {"A", "B", "C", "D", "E"}

    def test_deus_aliases_cover_all_groups(self):
        """DEUS aliases include agents from all 5 groups."""
        values = set(DEUS_ALIASES.values())
        groups = {v[0] for v in values}
        assert groups == {"A", "B", "C", "D", "E"}

    def test_daedelus_alias_keys_are_lowercase(self):
        """All Daedelus alias keys are lowercase."""
        for key in DAEDELUS_ALIASES:
            assert key == key.lower(), f"Alias key '{key}' is not lowercase"

    def test_deus_alias_keys_are_lowercase(self):
        """All DEUS alias keys are lowercase."""
        for key in DEUS_ALIASES:
            assert key == key.lower(), f"Alias key '{key}' is not lowercase"

    def test_daedelus_alias_values_are_uppercase(self):
        """All Daedelus alias values are uppercase agent keys."""
        for value in DAEDELUS_ALIASES.values():
            assert value == value.upper(), f"Alias value '{value}' is not uppercase"

    def test_deus_alias_values_are_uppercase(self):
        """All DEUS alias values are uppercase agent keys."""
        for value in DEUS_ALIASES.values():
            assert value == value.upper(), f"Alias value '{value}' is not uppercase"


class TestGetBuiltinAliases:
    """##Class purpose: Verify mode-based alias lookup."""

    def test_daedelus_mode(self):
        """Daedelus mode returns Daedelus aliases."""
        result = _get_builtin_aliases("daedelus")
        assert result is DAEDELUS_ALIASES

    def test_deus_mode(self):
        """DEUS mode returns DEUS aliases."""
        result = _get_builtin_aliases("deus")
        assert result is DEUS_ALIASES

    def test_unknown_mode(self):
        """Unknown mode returns empty dict."""
        result = _get_builtin_aliases("unknown")
        assert result == {}


class TestResolveAlias:
    """##Class purpose: Verify alias resolution logic."""

    def test_resolve_daedelus_architect(self):
        """Architect alias resolves to A1 in Daedelus mode."""
        result = resolve_alias("architect", "daedelus")
        assert result == "A1"

    def test_resolve_deus_kernel(self):
        """Kernel alias resolves to A1 in DEUS mode."""
        result = resolve_alias("kernel", "deus")
        assert result == "A1"

    def test_resolve_case_insensitive(self):
        """Alias resolution is case-insensitive."""
        result = resolve_alias("ARCHITECT", "daedelus")
        assert result == "A1"

    def test_resolve_with_whitespace(self):
        """Alias resolution trims whitespace."""
        result = resolve_alias("  architect  ", "daedelus")
        assert result == "A1"

    def test_resolve_unknown_alias(self):
        """Unknown alias returns None."""
        result = resolve_alias("nonexistent", "daedelus")
        assert result is None

    def test_custom_alias_takes_precedence(self):
        """Custom alias overrides built-in alias."""
        custom = {"architect": "B6"}
        result = resolve_alias("architect", "daedelus", custom)
        assert result == "B6"

    def test_custom_alias_new_name(self):
        """Custom alias with new name resolves correctly."""
        custom = {"myagent": "D3"}
        result = resolve_alias("myagent", "daedelus", custom)
        assert result == "D3"

    def test_resolve_orchestrator_daedelus(self):
        """Orchestrator alias resolves to E1 in Daedelus."""
        result = resolve_alias("orchestrator", "daedelus")
        assert result == "E1"

    def test_resolve_orchestrator_deus(self):
        """Orchestrator alias resolves to E1 in DEUS."""
        result = resolve_alias("orchestrator", "deus")
        assert result == "E1"

    def test_resolve_security_daedelus(self):
        """Security alias resolves to B6 in Daedelus."""
        result = resolve_alias("security", "daedelus")
        assert result == "B6"

    def test_resolve_zfs_deus(self):
        """ZFS alias resolves to D5 in DEUS."""
        result = resolve_alias("zfs", "deus")
        assert result == "D5"

    def test_resolve_jail_deus(self):
        """Jail alias resolves to D4 in DEUS."""
        result = resolve_alias("jail", "deus")
        assert result == "D4"


class TestGetAllAliases:
    """##Class purpose: Verify combined alias retrieval."""

    def test_returns_dict(self):
        """Get all aliases returns a dictionary."""
        result = get_all_aliases("daedelus")
        assert isinstance(result, dict)

    def test_includes_builtin(self):
        """All built-in aliases are included."""
        result = get_all_aliases("daedelus")
        assert "architect" in result

    def test_includes_custom(self):
        """Custom aliases are included in result."""
        custom = {"myalias": "A1"}
        result = get_all_aliases("daedelus", custom)
        assert "myalias" in result

    def test_custom_overrides_builtin(self):
        """Custom alias overrides built-in."""
        custom = {"architect": "C1"}
        result = get_all_aliases("daedelus", custom)
        assert result["architect"] == "C1"

    def test_does_not_mutate_builtin(self):
        """Getting all aliases does not mutate the built-in dict."""
        original_len = len(DAEDELUS_ALIASES)
        get_all_aliases("daedelus", {"new": "A1"})
        assert len(DAEDELUS_ALIASES) == original_len


class TestValidateCustomAliases:
    """##Class purpose: Verify custom alias validation."""

    def test_valid_aliases(self):
        """Valid aliases pass validation."""
        result = validate_custom_aliases({"arch": "A1", "sec": "B6"})
        assert result == {"arch": "A1", "sec": "B6"}

    def test_normalizes_keys_lowercase(self):
        """Keys are normalized to lowercase."""
        result = validate_custom_aliases({"ARCH": "A1"})
        assert "arch" in result

    def test_normalizes_values_uppercase(self):
        """Values are normalized to uppercase."""
        result = validate_custom_aliases({"arch": "a1"})
        assert result["arch"] == "A1"

    def test_strips_whitespace(self):
        """Whitespace is stripped from keys and values."""
        result = validate_custom_aliases({"  arch  ": "  A1  "})
        assert "arch" in result
        assert result["arch"] == "A1"

    def test_rejects_non_dict(self):
        """Non-dict input returns empty dict."""
        result = validate_custom_aliases("not a dict")
        assert result == {}

    def test_rejects_non_dict_none(self):
        """None input returns empty dict."""
        result = validate_custom_aliases(None)
        assert result == {}

    def test_skips_non_string_keys(self):
        """Non-string keys are skipped."""
        result = validate_custom_aliases({123: "A1", "valid": "B6"})
        assert 123 not in result
        assert "valid" in result

    def test_skips_non_string_values(self):
        """Non-string values are skipped."""
        result = validate_custom_aliases({"arch": 42, "valid": "B6"})
        assert "arch" not in result
        assert "valid" in result
