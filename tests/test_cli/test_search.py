"""
##Script function and purpose: Tests for agent search/filter functionality.

Tests the search_agents and display_search_results functions in
logos.cli.agent_select module.
Phase 5 implementation.
"""

from logos.cli.agent_select import display_search_results, search_agents


class TestSearchAgents:
    """Tests for agent search functionality."""

    def test_search_by_agent_name(self):
        """Test searching agents by name returns matches."""
        results = search_agents("daedelus", "architect")
        assert len(results) >= 1
        keys = [k for k, _ in results]
        assert "A1" in keys

    def test_search_by_agent_key(self):
        """Test searching agents by key returns matches."""
        results = search_agents("daedelus", "A1")
        assert len(results) >= 1
        keys = [k for k, _ in results]
        assert "A1" in keys

    def test_search_by_description(self):
        """Test searching agents by description keyword."""
        results = search_agents("daedelus", "security")
        assert len(results) >= 1

    def test_search_case_insensitive(self):
        """Test that search is case-insensitive."""
        results_lower = search_agents("daedelus", "architect")
        results_upper = search_agents("daedelus", "ARCHITECT")
        results_mixed = search_agents("daedelus", "Architect")
        assert len(results_lower) == len(results_upper) == len(results_mixed)

    def test_search_empty_query(self):
        """Test empty query returns no results."""
        results = search_agents("daedelus", "")
        assert results == []

    def test_search_whitespace_query(self):
        """Test whitespace-only query returns no results."""
        results = search_agents("daedelus", "   ")
        assert results == []

    def test_search_no_match(self):
        """Test non-matching query returns empty list."""
        results = search_agents("daedelus", "xyznonexistent")
        assert results == []

    def test_search_deus_mode(self):
        """Test search works in DEUS mode."""
        results = search_agents("deus", "kernel")
        assert len(results) >= 1
        keys = [k for k, _ in results]
        assert "A1" in keys

    def test_search_invalid_mode(self):
        """Test search with invalid mode returns empty."""
        results = search_agents("invalid_mode", "architect")
        assert results == []

    def test_search_by_alias(self):
        """Test searching by alias name finds the agent."""
        results = search_agents("daedelus", "sentinel")
        assert len(results) >= 1
        keys = [k for k, _ in results]
        assert "B6" in keys

    def test_search_returns_agent_objects(self):
        """Test search results contain valid Agent objects."""
        results = search_agents("daedelus", "architect")
        for key, agent in results:
            assert hasattr(agent, "name")
            assert hasattr(agent, "desc")
            assert hasattr(agent, "group")

    def test_search_partial_match(self):
        """Test partial string matching works."""
        results = search_agents("daedelus", "opt")
        assert len(results) >= 1  # Should match "Optimizer" at minimum

    def test_search_multiple_results(self):
        """Test queries that match multiple agents return all matches."""
        results = search_agents("deus", "security")
        assert len(results) >= 2  # Security Auditor and Security Patcher at minimum


class TestDisplaySearchResults:
    """Tests for display_search_results function."""

    def test_display_no_results(self, capsys):
        """Test display with no results shows appropriate message."""
        display_search_results([], "nonexistent")
        output = capsys.readouterr().out
        assert "No agents found" in output
        assert "nonexistent" in output

    def test_display_with_results(self, capsys):
        """Test display with results shows agent info."""
        results = search_agents("daedelus", "architect")
        display_search_results(results, "architect")
        output = capsys.readouterr().out
        assert "architect" in output
        assert "A1" in output

    def test_display_shows_count(self, capsys):
        """Test display shows result count."""
        results = search_agents("daedelus", "architect")
        display_search_results(results, "architect")
        output = capsys.readouterr().out
        assert f"{len(results)} found" in output
