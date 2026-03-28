"""Tests for logos.cli.agent_select agent selection module."""

from logos.cli.agent_select import (
    _show_prompt_preview,
    get_agent_for_mode,
    get_daedelus_groups,
    get_deus_groups,
)
from logos.core.types import AgentGroup


class TestGetDaedelusGroups:
    """##Class purpose: Verify Daedelus agent group structure."""

    def test_returns_list(self):
        """Returns a list of agent groups."""
        groups = get_daedelus_groups()
        assert isinstance(groups, list)

    def test_has_five_groups(self):
        """Returns exactly 5 agent groups (A-E)."""
        groups = get_daedelus_groups()
        assert len(groups) == 5

    def test_groups_are_agent_group_type(self):
        """Each group is an AgentGroup dataclass."""
        groups = get_daedelus_groups()
        for group in groups:
            assert isinstance(group, AgentGroup)

    def test_group_ids_ordered(self):
        """Group IDs are A, B, C, D, E in order."""
        groups = get_daedelus_groups()
        ids = [g.id for g in groups]
        assert ids == ["A", "B", "C", "D", "E"]

    def test_groups_have_agents(self):
        """Each group has at least one agent."""
        groups = get_daedelus_groups()
        for group in groups:
            assert len(group.agents) > 0

    def test_group_a_is_builders(self):
        """Group A is named THE BUILDERS."""
        groups = get_daedelus_groups()
        assert groups[0].name == "THE BUILDERS"

    def test_group_e_is_operators(self):
        """Group E is named THE OPERATORS."""
        groups = get_daedelus_groups()
        assert groups[4].name == "THE OPERATORS"


class TestGetDeusGroups:
    """##Class purpose: Verify DEUS agent group structure."""

    def test_returns_list(self):
        """Returns a list of agent groups."""
        groups = get_deus_groups()
        assert isinstance(groups, list)

    def test_has_five_groups(self):
        """Returns exactly 5 agent groups (A-E)."""
        groups = get_deus_groups()
        assert len(groups) == 5

    def test_groups_are_agent_group_type(self):
        """Each group is an AgentGroup dataclass."""
        groups = get_deus_groups()
        for group in groups:
            assert isinstance(group, AgentGroup)

    def test_group_ids_ordered(self):
        """Group IDs are A, B, C, D, E in order."""
        groups = get_deus_groups()
        ids = [g.id for g in groups]
        assert ids == ["A", "B", "C", "D", "E"]

    def test_groups_have_agents(self):
        """Each group has at least one agent."""
        groups = get_deus_groups()
        for group in groups:
            assert len(group.agents) > 0

    def test_group_a_is_engineers(self):
        """Group A is named THE ENGINEERS."""
        groups = get_deus_groups()
        assert groups[0].name == "THE ENGINEERS"

    def test_group_e_is_operators(self):
        """Group E is named THE OPERATORS."""
        groups = get_deus_groups()
        assert groups[4].name == "THE OPERATORS"


class TestGetAgentForMode:
    """##Class purpose: Verify agent lookup by mode and key."""

    def test_daedelus_a1(self):
        """Can get Daedelus A1 (The Architect)."""
        agent = get_agent_for_mode("daedelus", "A1")
        assert agent is not None
        assert agent.name == "The Architect"

    def test_deus_a1(self):
        """Can get DEUS A1 (The Kernel Architect)."""
        agent = get_agent_for_mode("deus", "A1")
        assert agent is not None
        assert agent.name == "The Kernel Architect"

    def test_daedelus_e3(self):
        """Can get Daedelus E3 (Daedelus)."""
        agent = get_agent_for_mode("daedelus", "E3")
        assert agent is not None

    def test_deus_e5(self):
        """Can get DEUS E5 (DEUS)."""
        agent = get_agent_for_mode("deus", "E5")
        assert agent is not None

    def test_invalid_mode_returns_none(self):
        """Invalid mode returns None."""
        agent = get_agent_for_mode("invalid", "A1")
        assert agent is None

    def test_invalid_key_returns_none(self):
        """Invalid agent key returns None."""
        agent = get_agent_for_mode("daedelus", "Z99")
        assert agent is None

    def test_deus_does_not_have_e4_e5_daedelus(self):
        """Daedelus does not have E4 or E5 agents."""
        assert get_agent_for_mode("daedelus", "E4") is None
        assert get_agent_for_mode("daedelus", "E5") is None

    def test_deus_has_e4_e5(self):
        """DEUS has E4 and E5 agents."""
        assert get_agent_for_mode("deus", "E4") is not None
        assert get_agent_for_mode("deus", "E5") is not None


class TestShowPromptPreview:
    """##Class purpose: Verify prompt preview formatting."""

    def test_short_prompt_shows_all(self, capsys):
        """Short prompt (fewer lines than preview) shows all lines."""
        _show_prompt_preview("line1\nline2\nline3", preview_lines=10)
        captured = capsys.readouterr()
        assert "line1" in captured.out
        assert "line2" in captured.out
        assert "line3" in captured.out

    def test_long_prompt_shows_first_and_last(self, capsys):
        """Long prompt shows first and last lines with omission notice."""
        lines = "\n".join(f"line{i}" for i in range(50))
        _show_prompt_preview(lines, preview_lines=6)
        captured = capsys.readouterr()
        assert "line0" in captured.out
        assert "line49" in captured.out
        assert "omitted" in captured.out

    def test_preview_shows_total_count(self, capsys):
        """Preview header shows total line count."""
        lines = "\n".join(f"line{i}" for i in range(20))
        _show_prompt_preview(lines, preview_lines=4)
        captured = capsys.readouterr()
        assert "20 lines total" in captured.out

    def test_empty_prompt(self, capsys):
        """Empty prompt shows empty message."""
        _show_prompt_preview("", preview_lines=5)
        captured = capsys.readouterr()
        assert "Preview" in captured.out
        assert "prompt is empty" in captured.out

    def test_zero_preview_lines(self, capsys):
        """Zero preview_lines shows omission message."""
        _show_prompt_preview("line1\nline2", preview_lines=0)
        captured = capsys.readouterr()
        assert "omitted" in captured.out
        assert "preview disabled" in captured.out

    def test_correct_omission_count(self, capsys):
        """Omission count is correctly calculated."""
        lines = "\n".join(f"line{i}" for i in range(50))
        _show_prompt_preview(lines, preview_lines=6)
        captured = capsys.readouterr()
        ##Action purpose: 6 budget -> 3 first + 3 last = 6 shown, 44 omitted
        assert "44 lines omitted" in captured.out


class TestDaedelusAgentCoverage:
    """##Class purpose: Verify all 24 Daedelus agents are accessible."""

    DAEDELUS_KEYS = [
        "A1",
        "A2",
        "A3",
        "A4",
        "A5",
        "B6",
        "B7",
        "B8",
        "B9",
        "B10",
        "C1",
        "C6",
        "C7",
        "C8",
        "C9",
        "C10",
        "C11",
        "D2",
        "D3",
        "D4",
        "D5",
        "E1",
        "E2",
        "E3",
    ]

    def test_all_daedelus_agents_exist(self):
        """All 24 Daedelus agent keys return valid agents."""
        for key in self.DAEDELUS_KEYS:
            agent = get_agent_for_mode("daedelus", key)
            assert agent is not None, f"Daedelus agent {key} not found"

    def test_daedelus_count(self):
        """Daedelus has exactly 24 agents across all groups."""
        groups = get_daedelus_groups()
        total = sum(len(g.agents) for g in groups)
        assert total == 24


class TestDeusAgentCoverage:
    """##Class purpose: Verify all 26 DEUS agents are accessible."""

    DEUS_KEYS = [
        "A1",
        "A2",
        "A3",
        "A4",
        "A5",
        "B6",
        "B7",
        "B8",
        "B9",
        "B10",
        "C1",
        "C6",
        "C7",
        "C8",
        "C9",
        "C10",
        "C11",
        "D2",
        "D3",
        "D4",
        "D5",
        "E1",
        "E2",
        "E3",
        "E4",
        "E5",
    ]

    def test_all_deus_agents_exist(self):
        """All 26 DEUS agent keys return valid agents."""
        for key in self.DEUS_KEYS:
            agent = get_agent_for_mode("deus", key)
            assert agent is not None, f"DEUS agent {key} not found"

    def test_deus_count(self):
        """DEUS has exactly 26 agents across all groups."""
        groups = get_deus_groups()
        total = sum(len(g.agents) for g in groups)
        assert total == 26
