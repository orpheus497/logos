"""Tests for recent agents tracking in logos.core.identity."""

from logos.core.identity import SystemIdentity, create_identity, update_session_tracking


class TestRecentAgentsTracking:
    """##Class purpose: Verify recent agents list management in session tracking."""

    def _make_identity(self, recent_agents=None):
        """Helper to create a test identity with optional recent agents."""
        return SystemIdentity(
            hostname="test-host",
            username="testuser",
            os_name="Linux",
            os_version="6.0",
            faction="orphic",
            created_at="2026-01-01T00:00:00+00:00",
            last_session="2026-01-01T00:00:00+00:00",
            total_sessions=0,
            faction_prompt_counts={},
            mode_prompt_counts={},
            recent_agents=recent_agents if recent_agents else [],
        )

    def test_initial_empty_list(self):
        """New identity has empty recent agents list."""
        identity = self._make_identity()
        assert identity.recent_agents == []

    def test_first_agent_added(self):
        """First agent selection adds to recent list."""
        identity = self._make_identity()
        updated = update_session_tracking(identity, mode="daedelus", agent="A1")
        assert len(updated.recent_agents) == 1
        assert updated.recent_agents[0] == "daedelus:A1"

    def test_multiple_agents_tracked(self):
        """Multiple agent selections are tracked in order."""
        identity = self._make_identity()
        updated = update_session_tracking(identity, mode="daedelus", agent="A1")
        updated = update_session_tracking(updated, mode="daedelus", agent="B6")
        updated = update_session_tracking(updated, mode="deus", agent="A1")
        assert len(updated.recent_agents) == 3
        assert updated.recent_agents[0] == "deus:A1"
        assert updated.recent_agents[1] == "daedelus:B6"
        assert updated.recent_agents[2] == "daedelus:A1"

    def test_most_recent_first(self):
        """Most recent agent is first in the list."""
        identity = self._make_identity()
        updated = update_session_tracking(identity, mode="daedelus", agent="A1")
        updated = update_session_tracking(updated, mode="daedelus", agent="B6")
        assert updated.recent_agents[0] == "daedelus:B6"

    def test_duplicate_moves_to_front(self):
        """Re-selecting an agent moves it to front (no duplicates)."""
        identity = self._make_identity(recent_agents=["daedelus:A1", "daedelus:B6", "deus:A1"])
        updated = update_session_tracking(identity, mode="deus", agent="A1")
        assert updated.recent_agents[0] == "deus:A1"
        assert updated.recent_agents.count("deus:A1") == 1
        assert len(updated.recent_agents) == 3

    def test_max_ten_entries(self):
        """Recent agents list is capped at 10 entries."""
        identity = self._make_identity()
        for i in range(15):
            identity = update_session_tracking(identity, mode="daedelus", agent=f"A{i}")
        assert len(identity.recent_agents) == 10

    def test_oldest_dropped_when_full(self):
        """Oldest entry is dropped when list exceeds 10."""
        agents = [f"daedelus:X{i}" for i in range(10)]
        identity = self._make_identity(recent_agents=agents)
        updated = update_session_tracking(identity, mode="daedelus", agent="NEW")
        assert len(updated.recent_agents) == 10
        assert updated.recent_agents[0] == "daedelus:NEW"
        assert "daedelus:X9" not in updated.recent_agents

    def test_mode_qualified_entries(self):
        """Entries include mode prefix (mode:agent)."""
        identity = self._make_identity()
        updated = update_session_tracking(identity, mode="deus", agent="E5")
        assert updated.recent_agents[0] == "deus:E5"

    def test_same_agent_different_modes(self):
        """Same agent key in different modes creates separate entries."""
        identity = self._make_identity()
        updated = update_session_tracking(identity, mode="daedelus", agent="A1")
        updated = update_session_tracking(updated, mode="deus", agent="A1")
        assert "deus:A1" in updated.recent_agents
        assert "daedelus:A1" in updated.recent_agents
        assert len(updated.recent_agents) == 2


class TestCreateIdentityRecentAgents:
    """##Class purpose: Verify create_identity initializes recent agents."""

    def test_new_identity_empty_recent(self):
        """Newly created identity has empty recent agents list."""
        scan_data = {
            "hostname": "test",
            "username": "user",
            "os_name": "Linux",
            "os_version": "6.0",
        }
        identity = create_identity("orphic", scan_data)
        assert identity.recent_agents == []
