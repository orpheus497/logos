##Script function and purpose: Tests for the .devdocs utility module

import pytest
from pathlib import Path
from logos.core.devdocs import (
    validate_devdocs_structure,
    check_devdocs_gitignored,
    generate_priority_read_warning,
    enforce_devdocs_priority,
    get_outstanding_agents,
    calculate_devdocs_size,
    validate_dev_state_structure
)

@pytest.fixture
def mock_project(tmp_path):
    """Create a mock project structure with complete .devdocs"""
    devdocs = tmp_path / ".devdocs"
    devdocs.mkdir()
    
    (devdocs / "DEV_STATE.md").write_text("## OUTSTANDING AGENT ASSIGNMENTS\n- A2 (Logic Engineer) - 3 tasks\n## PROJECT SNAPSHOT\n## RECENT ACTIONS\n## UNIFIED TASK LIST\n## ACTIVE BLOCKERS\n## NEXT IMMEDIATE STEPS\n## PROJECT METRICS\n## COHERENCE STATUS\n")
    
    agent_logs = devdocs / "AGENT_LOGS"
    agent_logs.mkdir()
    for group in ["group_a", "group_b", "group_c", "group_d", "group_e"]:
        (agent_logs / group).mkdir()
        
    (devdocs / "WORKFLOW_TRACKING").mkdir()
    (devdocs / ".archive").mkdir()
    
    (tmp_path / ".gitignore").write_text(".devdocs/\n")
    
    return tmp_path

def test_validate_devdocs_structure_complete(mock_project):
    result = validate_devdocs_structure(mock_project)
    assert result.exists is True
    assert result.valid_structure is True
    assert result.has_dev_state is True
    assert result.has_agent_logs is True
    assert result.has_workflow_tracking is True
    assert result.has_archive is True
    assert len(result.missing_components) == 0

def test_validate_devdocs_structure_missing_dir(tmp_path):
    result = validate_devdocs_structure(tmp_path)
    assert result.exists is False
    assert result.valid_structure is False
    assert ".devdocs/ folder does not exist" in result.errors

def test_check_devdocs_gitignored(mock_project):
    assert check_devdocs_gitignored(mock_project) is True

def test_check_devdocs_gitignored_missing(tmp_path):
    assert check_devdocs_gitignored(tmp_path) is False

def test_generate_priority_read_warning():
    warning = generate_priority_read_warning()
    assert "HIDDEN FOLDER PRIORITY READ VIOLATION" in warning
    assert "DEV_STATE.md" in warning

def test_enforce_devdocs_priority():
    enforcement = enforce_devdocs_priority()
    assert "NON-NEGOTIABLE RULE: HIDDEN FOLDER PRIORITY READ" in enforcement
    assert "DEV_STATE.md" in enforcement

def test_get_outstanding_agents(mock_project):
    agents = get_outstanding_agents(mock_project)
    assert len(agents) == 1
    assert agents[0]["key"] == "A2"
    assert agents[0]["name"] == "Logic Engineer"
    assert agents[0]["task_count"] == 3

def test_calculate_devdocs_size(mock_project):
    size = calculate_devdocs_size(mock_project)
    assert size > 0.0

def test_validate_dev_state_structure(mock_project):
    valid, missing = validate_dev_state_structure(mock_project)
    assert valid is True
    assert len(missing) == 0

def test_validate_dev_state_structure_missing_file(tmp_path):
    valid, missing = validate_dev_state_structure(tmp_path)
    assert valid is False
    assert "DEV_STATE.md file missing" in missing
