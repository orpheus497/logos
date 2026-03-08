from logos.core.prompts import build_complete_prompt

def test_missing_devdocs_warning(tmp_path, monkeypatch):
    """Test that missing .devdocs/ triggers a warning in the composed prompt."""
    monkeypatch.chdir(tmp_path)
    
    agent_prompt = "You are an agent."
    composed = build_complete_prompt(agent_prompt)
    
    assert "⚠️ **SYSTEM WARNING:** `.devdocs/` folder is MISSING." in composed
    assert "The Orchestrator (E1) must be invoked" in composed
    assert "You are an agent." in composed

def test_invalid_devdocs_structure_warning(tmp_path, monkeypatch):
    """Test that invalid .devdocs/ structure triggers a warning."""
    monkeypatch.chdir(tmp_path)
    
    # Create incomplete .devdocs
    devdocs = tmp_path / ".devdocs"
    devdocs.mkdir()
    (devdocs / "DEV_STATE.md").touch()
    # Missing AGENT_LOGS, WORKFLOW_TRACKING, .archive
    
    agent_prompt = "You are an agent."
    composed = build_complete_prompt(agent_prompt)
    
    assert "⚠️ **SYSTEM WARNING:** `.devdocs/` structure is INVALID or incomplete." in composed
    assert "Missing components: AGENT_LOGS/ folder, WORKFLOW_TRACKING/ folder, .archive/ folder" in composed

def test_valid_devdocs_no_warning(tmp_path, monkeypatch):
    """Test that a valid .devdocs/ structure does not trigger a warning."""
    monkeypatch.chdir(tmp_path)
    
    # Create complete .devdocs with all required subdirectories
    devdocs = tmp_path / ".devdocs"
    devdocs.mkdir()
    (devdocs / "DEV_STATE.md").touch()
    agent_logs = devdocs / "AGENT_LOGS"
    agent_logs.mkdir()
    for group in ["group_a", "group_b", "group_c", "group_d", "group_e"]:
        (agent_logs / group).mkdir()
    (devdocs / "WORKFLOW_TRACKING").mkdir()
    (devdocs / ".archive").mkdir()
    
    agent_prompt = "You are an agent."
    composed = build_complete_prompt(agent_prompt)
    
    assert "⚠️ **SYSTEM WARNING:**" not in composed
    assert composed == agent_prompt
