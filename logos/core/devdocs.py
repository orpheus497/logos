##Script function and purpose: .devdocs validation and utility functions for Orchestrator

"""Provides utilities for validating .devdocs/ folder structure.

Enforces standards and assists Orchestrator with governance tasks.
These functions are used by LOGOS during prompt composition or by
Orchestrator prompts to describe validation logic.
"""

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


##Class purpose: .devdocs structure validation result
@dataclass
class DevdocsValidation:
    """
    ##Class purpose: Contains results of .devdocs/ structure validation.

    Attributes:
        exists: Whether .devdocs/ folder exists
        valid_structure: Whether folder structure is correct
        has_dev_state: Whether DEV_STATE.md exists
        has_agent_logs: Whether AGENT_LOGS/ folder exists
        has_workflow_tracking: Whether WORKFLOW_TRACKING/ folder exists
        has_archive: Whether .archive/ folder exists
        missing_components: List of missing required components
        errors: List of validation errors
    """

    exists: bool
    valid_structure: bool
    has_dev_state: bool
    has_agent_logs: bool
    has_workflow_tracking: bool
    has_archive: bool
    missing_components: list[str]
    errors: list[str]


##Function purpose: Validate .devdocs/ folder structure
def validate_devdocs_structure(project_path: Path = Path(".")) -> DevdocsValidation:
    """
    ##Function purpose: Check if .devdocs/ folder has correct structure.

    Args:
        project_path: Path to project root (default: current directory)

    Returns:
        DevdocsValidation object with validation results
    """
    ##Action purpose: Define expected paths
    devdocs_path = project_path / ".devdocs"
    dev_state_path = devdocs_path / "DEV_STATE.md"
    agent_logs_path = devdocs_path / "AGENT_LOGS"
    workflow_path = devdocs_path / "WORKFLOW_TRACKING"
    archive_path = devdocs_path / ".archive"

    ##Action purpose: Initialize validation result
    missing = []
    errors = []

    ##Condition purpose: Check if .devdocs exists
    exists = devdocs_path.exists() and devdocs_path.is_dir()

    if not exists:
        return DevdocsValidation(
            exists=False,
            valid_structure=False,
            has_dev_state=False,
            has_agent_logs=False,
            has_workflow_tracking=False,
            has_archive=False,
            missing_components=[".devdocs/ folder"],
            errors=[".devdocs/ folder does not exist"],
        )

    ##Action purpose: Check required components
    has_dev_state = dev_state_path.exists() and dev_state_path.is_file()
    has_agent_logs = agent_logs_path.exists() and agent_logs_path.is_dir()
    has_workflow = workflow_path.exists() and workflow_path.is_dir()
    has_archive = archive_path.exists() and archive_path.is_dir()

    ##Action purpose: Build missing components list
    if not has_dev_state:
        missing.append("DEV_STATE.md")
    if not has_agent_logs:
        missing.append("AGENT_LOGS/ folder")
    if not has_workflow:
        missing.append("WORKFLOW_TRACKING/ folder")
    if not has_archive:
        missing.append(".archive/ folder")

    ##Action purpose: Check agent log group folders
    if has_agent_logs:
        expected_groups = ["group_a", "group_b", "group_c", "group_d", "group_e"]
        for group in expected_groups:
            group_path = agent_logs_path / group
            if not group_path.is_dir():
                missing.append(f"AGENT_LOGS/{group}/ folder")

    ##Action purpose: Determine validity
    valid_structure = len(missing) == 0 and len(errors) == 0

    ##Action purpose: Return validation result
    return DevdocsValidation(
        exists=True,
        valid_structure=valid_structure,
        has_dev_state=has_dev_state,
        has_agent_logs=has_agent_logs,
        has_workflow_tracking=has_workflow,
        has_archive=has_archive,
        missing_components=missing,
        errors=errors,
    )


##Function purpose: Check if .devdocs is in .gitignore
def check_devdocs_gitignored(project_path: Path = Path(".")) -> bool:
    """
    ##Function purpose: Verify .devdocs/ is properly ignored by git.

    Args:
        project_path: Path to project root

    Returns:
        True if .devdocs/ is in .gitignore, False otherwise
    """
    ##Action purpose: Find .gitignore file
    gitignore_path = project_path / ".gitignore"

    ##Condition purpose: Check if .gitignore exists
    if not gitignore_path.exists():
        return False

    ##Action purpose: Read .gitignore contents
    with open(gitignore_path, encoding="utf-8") as f:
        content = f.read()

    ##Condition purpose: Check for .devdocs entry (skip comments)
    for line in content.splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            if stripped in (".devdocs/", ".devdocs", ".devdocs/*"):
                return True
    return False


##Function purpose: Generate .devdocs priority read warning
def generate_priority_read_warning() -> str:
    """
    ##Function purpose: Create warning message for agents that skip .devdocs read.

    Returns:
        Formatted warning message
    """
    ##Action purpose: Build warning message
    warning = """
⚠️ HIDDEN FOLDER PRIORITY READ VIOLATION

You must read `.devdocs/DEV_STATE.md` BEFORE proceeding with any action.

The .devdocs/ folder contains:
- Current project state
- Unified task list with assignments
- Recent actions by other agents
- Active blockers
- Workflow status

Proceeding without reading .devdocs/ risks:
- Duplicate work
- Conflicting changes
- Context loss
- Wasted effort

ACTION REQUIRED:
1. Check if .devdocs/ folder exists
2. Read .devdocs/DEV_STATE.md completely
3. Check your agent log: .devdocs/AGENT_LOGS/group_X/[your_key].md
4. Understand current context
5. THEN proceed with task
"""
    return warning.strip()


##Function purpose: Enforce .devdocs priority read in prompts
def enforce_devdocs_priority() -> str:
    """
    ##Function purpose: Generate enforcement text for base prompts.

    Returns:
        Text to be inserted in base prompts requiring .devdocs read
    """
    ##Action purpose: Build enforcement instructions
    enforcement = """
## NON-NEGOTIABLE RULE: HIDDEN FOLDER PRIORITY READ

The `.devdocs/` folder is a **HIDDEN FOLDER** (dotfile starting with `.`).
It contains AI agent context and coordination data.

⚠️ **BEFORE ANY ACTION, YOU MUST:**

[ ] Check if `.devdocs/` folder exists in project root
[ ] If exists: Read `.devdocs/DEV_STATE.md` completely
[ ] Read your agent log: `.devdocs/AGENT_LOGS/group_X/[your_key].md`
[ ] If missing: Recommend user invoke Orchestrator (E1) to initialize
[ ] If corrupted: Report error to user

**Why this matters:**

`.devdocs/DEV_STATE.md` contains:
- **UNIFIED TASK LIST:** All project tasks with assignments and status
- **RECENT ACTIONS:** What other agents just completed
- **ACTIVE BLOCKERS:** Current obstacles preventing progress
- **WORKFLOW STATE:** Current workflow pattern (Diamond/Funnel/Maintenance)
- **OUTSTANDING AGENTS:** Which agents have pending work

**Reading .devdocs/ prevents:**
- Duplicate work (another agent already did this)
- Conflicting changes (two agents editing same file)
- Context loss (missing recent decisions)
- Blocked work (unknown blocker exists)

**If .devdocs/ does not exist:**
You are likely in a project without initialized agent context.
Recommend user invoke Orchestrator:
- Daedelus projects: `logos E1`
- DEUS projects: `logos E1`

Orchestrator will initialize .devdocs/ structure.

**⛔ DO NOT proceed without .devdocs/ context.**
"""
    return enforcement.strip()


##Function purpose: Get list of outstanding agent assignments
def get_outstanding_agents(project_path: Path = Path(".")) -> list[dict[str, Any]]:
    """
    ##Function purpose: Extract outstanding agent assignments from DEV_STATE.md.

    Used by system detection to display agents with remaining work.

    Args:
        project_path: Path to project root

    Returns:
        List of dicts with agent info: [{"key": "A2", "name": "Logic Engineer", "task_count": 3}, ...]
    """
    ##Action purpose: Define DEV_STATE.md path
    dev_state_path = project_path / ".devdocs" / "DEV_STATE.md"

    ##Condition purpose: Check if file exists
    if not dev_state_path.exists():
        return []

    ##Action purpose: Read DEV_STATE.md
    with open(dev_state_path, encoding="utf-8") as f:
        content = f.read()

    ##Condition purpose: Check if OUTSTANDING AGENT ASSIGNMENTS section exists
    if "OUTSTANDING AGENT ASSIGNMENTS" not in content:
        return []

    ##Action purpose: Extract section (handles emoji-prefixed or plain headings)
    section_match = re.search(
        r"##\s+(?:📌\s+)?OUTSTANDING AGENT ASSIGNMENTS\n(.*?)(?=\n##|\Z)",
        content,
        re.DOTALL,
    )
    if not section_match:
        return []
    section = section_match.group(1)

    ##Action purpose: Parse agent lines using regex, stripping markdown emphasis
    outstanding = []
    for line in section.split("\n"):
        ##Condition purpose: Look for agent assignment lines
        if line.strip().startswith("- ") and "(" in line and ")" in line:
            ##Action purpose: Strip common markdown emphasis characters
            clean = re.sub(r"[\*_`]", "", line.strip()[2:])

            ##Action purpose: Match agent key, name, task count, and status
            agent_match = re.match(
                r"(\w+)\s+\(([^)]+)\)(?:\s+-\s+(\d+)\s+tasks?)?",
                clean,
            )
            if agent_match:
                key = agent_match.group(1)
                name = agent_match.group(2)
                task_count = int(agent_match.group(3)) if agent_match.group(3) else 1

                outstanding.append(
                    {
                        "key": key,
                        "name": name,
                        "task_count": task_count,
                        "status": "in progress" if "in progress" in clean.lower() else "pending",
                    }
                )

    return outstanding


##Function purpose: Calculate .devdocs folder size
def calculate_devdocs_size(project_path: Path = Path(".")) -> float:
    """
    ##Function purpose: Calculate total size of .devdocs/ folder in MB.

    Args:
        project_path: Path to project root

    Returns:
        Size in megabytes (float)
    """
    ##Action purpose: Define .devdocs path
    devdocs_path = project_path / ".devdocs"

    ##Condition purpose: Check if exists
    if not devdocs_path.exists():
        return 0.0

    ##Action purpose: Calculate total size
    total_bytes = 0
    for file_path in devdocs_path.rglob("*"):
        if file_path.is_file():
            total_bytes += file_path.stat().st_size

    ##Action purpose: Convert to MB
    return total_bytes / (1024 * 1024)


##Function purpose: Validate DEV_STATE.md has required sections
def validate_dev_state_structure(project_path: Path = Path(".")) -> tuple[bool, list[str]]:
    """
    ##Function purpose: Check if DEV_STATE.md has all required sections.

    Args:
        project_path: Path to project root

    Returns:
        Tuple of (valid: bool, missing_sections: List[str])
    """
    ##Action purpose: Define path
    dev_state_path = project_path / ".devdocs" / "DEV_STATE.md"

    ##Condition purpose: Check if exists
    if not dev_state_path.exists():
        return False, ["DEV_STATE.md file missing"]

    ##Action purpose: Read content
    with open(dev_state_path, encoding="utf-8") as f:
        content = f.read()

    ##Action purpose: Define required sections
    required_sections = [
        "## 📊 PROJECT STATUS",
        "## 📝 RECENT ACTIONS",
        "## 🎯 UNIFIED TASK LIST",
        "## 🚧 ACTIVE BLOCKERS",
        "## 🔜 NEXT IMMEDIATE STEPS",
        "## 📈 PROJECT METRICS",
        "## 🔍 COHERENCE STATUS",
        "## 📌 OUTSTANDING AGENT ASSIGNMENTS",
    ]

    ##Action purpose: Check for missing sections
    missing = []
    for section in required_sections:
        if section not in content:
            missing.append(section)

    ##Action purpose: Return validation result
    return len(missing) == 0, missing
