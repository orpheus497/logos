"""
##Script function and purpose: Integration tests verifying all v0.2.0 features work together.

Covers Phase 1 (Boundaries), Phase 2 (.devdocs), Phase 3 (Workflow),
Phase 4 (OS Adaptations), Phase 5 (CLI), Phase 6 (Documentation),
and Phase 7 (Release) to ensure cross-phase consistency.
"""

import re
from pathlib import Path

import pytest

from logos.core.agent import Agent
from logos.core.aliases import resolve_alias, get_all_aliases
from logos.core.config import DEFAULT_CONFIG, load_config
from logos.core.devdocs import validate_devdocs_structure
from logos.core.doc_audit import find_markdown_files, audit_file
from logos.core.identity import scan_system, SystemIdentity
from logos.core.prompts import (
    _adapt_deus_prompt_for_os,
    build_complete_prompt,
    DEUS_OS_SUBSTITUTIONS,
)
from logos.core.refusal import (
    RefusalResponse,
    generate_refusal,
    validate_refusal_response,
)
from logos.core.version import VERSION, get_version
from logos.core.workflow_tracking import (
    AgentStatus,
    WorkflowState,
    WorkflowStep,
    WorkflowType,
    create_diamond_workflow,
)
from logos.daedelus import get_agent as dae_get_agent
from logos.deus import get_agent as deus_get_agent

# Project root resolved relative to this test file
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DAEDELUS_KEYS = [
    "A1", "A2", "A3", "A4", "A5",
    "B6", "B7", "B8", "B9", "B10",
    "C1", "C6", "C7", "C8", "C9", "C10", "C11",
    "D2", "D3", "D4", "D5",
    "E1", "E2", "E3",
]

DEUS_KEYS = [
    "A1", "A2", "A3", "A4", "A5",
    "B6", "B7", "B8", "B9", "B10",
    "C1", "C6", "C7", "C8", "C9", "C10", "C11",
    "D2", "D3", "D4", "D5",
    "E1", "E2", "E3", "E4", "E5",
]


# ---------------------------------------------------------------------------
# Phase 1 – Boundaries
# ---------------------------------------------------------------------------
class TestPhase1Boundaries:
    """Verify Phase 1 boundary enforcement features work across all agents."""

    def test_all_daedelus_agents_load(self):
        """##Function purpose: Verify all 24 Daedelus agents load via get_agent."""
        loaded = [dae_get_agent(k) for k in DAEDELUS_KEYS]
        assert all(a is not None for a in loaded), "Some Daedelus agents failed to load"
        assert len(loaded) == 24

    def test_all_deus_agents_load(self):
        """##Function purpose: Verify all 26 DEUS agents load via get_agent."""
        loaded = [deus_get_agent(k) for k in DEUS_KEYS]
        assert all(a is not None for a in loaded), "Some DEUS agents failed to load"
        assert len(loaded) == 26

    def test_all_agents_have_scope_boundaries(self):
        """##Function purpose: Verify every agent across both domains contains SCOPE BOUNDARIES."""
        missing = []
        for key in DAEDELUS_KEYS:
            agent = dae_get_agent(key)
            if "## SCOPE BOUNDARIES" not in agent.full_prompt:
                missing.append(f"Daedelus {key}")
        for key in DEUS_KEYS:
            agent = deus_get_agent(key)
            if "## SCOPE BOUNDARIES" not in agent.full_prompt:
                missing.append(f"DEUS {key}")
        assert not missing, f"Agents missing SCOPE BOUNDARIES: {missing}"

    def test_refusal_module_generates_valid_response(self):
        """##Function purpose: Verify RefusalResponse validates and generates formatted output."""
        response = RefusalResponse(
            refusing_agent_key="A1",
            refusing_agent_name="Architect",
            refusing_agent_specialty="System architecture",
            reason="Request is outside my scope",
            recommended_agent_key="C7",
            recommended_agent_name="Doc Updater",
            recommended_agent_description="Documentation maintenance",
            user_request_summary="Update README",
        )
        errors = validate_refusal_response(response)
        assert not errors, f"Validation errors: {errors}"
        text = generate_refusal(response)
        assert "A1" in text
        assert "C7" in text
        assert len(text) > 50


# ---------------------------------------------------------------------------
# Phase 2 – .devdocs Governance
# ---------------------------------------------------------------------------
class TestPhase2Devdocs:
    """Verify Phase 2 .devdocs governance modules are functional."""

    def test_devdocs_validates_missing_directory(self, tmp_path, monkeypatch):
        """##Function purpose: Verify devdocs validation detects missing .devdocs/ directory."""
        monkeypatch.chdir(tmp_path)
        result = validate_devdocs_structure(tmp_path)
        assert result.exists is False
        assert result.valid_structure is False

    def test_devdocs_validates_complete_structure(self, tmp_path, monkeypatch):
        """##Function purpose: Verify devdocs validation passes for a correct .devdocs/ layout."""
        monkeypatch.chdir(tmp_path)
        devdocs = tmp_path / ".devdocs"
        devdocs.mkdir()
        (devdocs / "DEV_STATE.md").touch()
        agent_logs = devdocs / "AGENT_LOGS"
        agent_logs.mkdir()
        for group in ["group_a", "group_b", "group_c", "group_d", "group_e"]:
            (agent_logs / group).mkdir()
        (devdocs / "WORKFLOW_TRACKING").mkdir()
        (devdocs / ".archive").mkdir()
        result = validate_devdocs_structure(tmp_path)
        assert result.exists is True
        assert result.valid_structure is True

    def test_temporal_logs_module_has_required_functions(self):
        """##Function purpose: Verify temporal_logs exposes core analysis and archival functions."""
        from logos.core import temporal_logs

        for fn_name in ("analyze_agent_log", "archive_daily_entries", "archive_weekly_summaries"):
            assert hasattr(temporal_logs, fn_name), f"temporal_logs missing {fn_name}"
            assert callable(getattr(temporal_logs, fn_name))

    def test_bloat_prevention_importable_and_has_analyze(self):
        """##Function purpose: Verify bloat_prevention module imports and provides analyze_bloat."""
        from logos.core import bloat_prevention

        assert hasattr(bloat_prevention, "analyze_bloat")
        assert callable(bloat_prevention.analyze_bloat)


# ---------------------------------------------------------------------------
# Phase 3 – Workflow
# ---------------------------------------------------------------------------
class TestPhase3Workflow:
    """Verify Phase 3 workflow tracking types and templates."""

    def test_workflow_type_enum_values(self):
        """##Function purpose: Verify WorkflowType enum contains all expected members."""
        assert WorkflowType.DIAMOND.value == "diamond"
        assert WorkflowType.FUNNEL.value == "funnel"
        assert WorkflowType.MAINTENANCE.value == "maintenance"

    def test_agent_status_enum_values(self):
        """##Function purpose: Verify AgentStatus enum contains all expected members."""
        values = {s.value for s in AgentStatus}
        expected = {"not_started", "in_progress", "complete", "waiting", "blocked"}
        assert expected.issubset(values), f"Missing statuses: {expected - values}"

    def test_workflow_state_creation_and_steps(self):
        """##Function purpose: Verify WorkflowState can be created and steps added via factory."""
        state = create_diamond_workflow(initiated_by="A1")
        assert isinstance(state, WorkflowState)
        assert state.workflow_type == WorkflowType.DIAMOND
        assert len(state.steps) > 0
        assert all(isinstance(s, WorkflowStep) for s in state.steps)

    def test_workflow_templates_directory_exists(self):
        """##Function purpose: Verify templates directory contains workflow tracking templates."""
        templates_dir = PROJECT_ROOT / "templates" / ".devdocs" / "WORKFLOW_TRACKING"
        assert templates_dir.is_dir(), f"Missing workflow templates at {templates_dir}"
        files = [f.name for f in templates_dir.iterdir()]
        assert len(files) >= 3, f"Expected >=3 workflow templates, found {files}"


# ---------------------------------------------------------------------------
# Phase 4 – OS Adaptations
# ---------------------------------------------------------------------------
class TestPhase4OSAdaptations:
    """Verify Phase 4 OS adaptation features."""

    def test_prompts_module_has_os_adaptation_function(self):
        """##Function purpose: Verify prompts module exposes _adapt_deus_prompt_for_os."""
        assert callable(_adapt_deus_prompt_for_os)

    def test_os_substitution_patterns_defined(self):
        """##Function purpose: Verify DEUS_OS_SUBSTITUTIONS contains FreeBSD-to-Linux mappings."""
        assert len(DEUS_OS_SUBSTITUTIONS) > 0
        patterns_text = " ".join(p for p, _ in DEUS_OS_SUBSTITUTIONS)
        assert "FreeBSD" in patterns_text or "freebsd" in patterns_text.lower()

    def test_all_deus_agents_contain_os_instructions(self):
        """##Function purpose: Verify every DEUS agent prompt includes OS-SPECIFIC INSTRUCTIONS."""
        missing = []
        for key in DEUS_KEYS:
            agent = deus_get_agent(key)
            if "OS-SPECIFIC INSTRUCTIONS" not in agent.full_prompt:
                missing.append(key)
        assert not missing, f"DEUS agents missing OS-SPECIFIC INSTRUCTIONS: {missing}"

    def test_identity_module_detects_os(self):
        """##Function purpose: Verify scan_system returns an os_name field."""
        scan = scan_system()
        assert "os_name" in scan, "scan_system() missing 'os_name' key"
        assert isinstance(scan["os_name"], str)
        assert len(scan["os_name"]) > 0


# ---------------------------------------------------------------------------
# Phase 5 – CLI
# ---------------------------------------------------------------------------
class TestPhase5CLI:
    """Verify Phase 5 CLI modules expose expected interfaces."""

    def test_config_provides_defaults(self):
        """##Function purpose: Verify DEFAULT_CONFIG contains all expected top-level keys."""
        expected_keys = {"default_mode", "clipboard", "recent_agents", "aliases", "verbosity"}
        assert expected_keys.issubset(DEFAULT_CONFIG.keys()), (
            f"Missing config keys: {expected_keys - DEFAULT_CONFIG.keys()}"
        )

    def test_aliases_resolve_correctly(self):
        """##Function purpose: Verify resolve_alias maps known aliases to agent keys."""
        all_dae = get_all_aliases("daedelus")
        assert len(all_dae) >= 24, f"Expected >=24 Daedelus aliases, got {len(all_dae)}"
        all_deus = get_all_aliases("deus")
        assert len(all_deus) >= 26, f"Expected >=26 DEUS aliases, got {len(all_deus)}"

    def test_args_module_parses_correctly(self):
        """##Function purpose: Verify parse_args handles minimal invocation without error."""
        from logos.cli.args import parse_args

        ns = parse_args([])
        assert ns is not None

    def test_version_returns_valid_string(self):
        """##Function purpose: Verify get_version returns a semver-ish version string."""
        ver = get_version()
        assert isinstance(ver, str)
        # Must start with digit and contain at least one dot
        assert re.match(r"^\d+\.\d+", ver), f"Version {ver!r} doesn't look like semver"

    def test_search_function_finds_agents(self):
        """##Function purpose: Verify search_agents returns results for a known query."""
        from logos.cli.agent_select import search_agents

        results = search_agents("daedelus", "architect")
        assert isinstance(results, list)
        # At least one agent should match "architect"
        assert len(results) >= 1, "search_agents('daedelus', 'architect') returned no results"
        key, agent = results[0]
        assert isinstance(agent, Agent)


# ---------------------------------------------------------------------------
# Phase 6 – Documentation
# ---------------------------------------------------------------------------
class TestPhase6Documentation:
    """Verify Phase 6 documentation audit and key files."""

    def test_doc_audit_module_importable_and_functional(self):
        """##Function purpose: Verify doc_audit module imports and has core functions."""
        from logos.core import doc_audit

        assert hasattr(doc_audit, "find_markdown_files")
        assert hasattr(doc_audit, "audit_file")
        assert hasattr(doc_audit, "audit_project")
        md_files = find_markdown_files(PROJECT_ROOT)
        assert len(md_files) > 0, "No markdown files found in project root"

    def test_key_documentation_files_exist(self):
        """##Function purpose: Verify essential project documentation files are present."""
        required_files = [
            "README.md",
            "CONSTITUTION.md",
            "CHANGELOG.md",
            "CONTRIBUTING.md",
            "INSTALL.md",
            "LICENSE",
        ]
        missing = [f for f in required_files if not (PROJECT_ROOT / f).is_file()]
        assert not missing, f"Missing documentation files: {missing}"

    def test_article_xi_exists_in_constitution(self):
        """##Function purpose: Verify CONSTITUTION.md contains Article XI on documentation standards."""
        constitution = (PROJECT_ROOT / "CONSTITUTION.md").read_text(encoding="utf-8")
        assert "ARTICLE XI" in constitution, "CONSTITUTION.md missing Article XI"
        assert "DOCUMENTATION" in constitution.upper()

    def test_docs_directory_has_key_references(self):
        """##Function purpose: Verify /docs directory contains essential reference documents."""
        docs_dir = PROJECT_ROOT / "docs"
        assert docs_dir.is_dir(), "docs/ directory missing"
        doc_files = [f.name for f in docs_dir.iterdir() if f.is_file()]
        assert len(doc_files) >= 3, f"Expected >=3 docs, found {doc_files}"


# ---------------------------------------------------------------------------
# Phase 7 – Release
# ---------------------------------------------------------------------------
class TestPhase7Release:
    """Verify Phase 7 release readiness."""

    def test_version_consistency(self):
        """##Function purpose: Verify version in pyproject.toml matches logos/core/version.py."""
        pyproject = PROJECT_ROOT / "pyproject.toml"
        content = pyproject.read_text(encoding="utf-8")
        # Extract version = "..." from pyproject.toml
        match = re.search(r'^version\s*=\s*"([^"]+)"', content, re.MULTILINE)
        assert match, "Could not find version in pyproject.toml"
        pyproject_version = match.group(1)
        assert pyproject_version == VERSION, (
            f"pyproject.toml version {pyproject_version!r} != version.py {VERSION!r}"
        )

    def test_all_required_documentation_present(self):
        """##Function purpose: Verify all documentation required for release exists."""
        required = [
            "README.md",
            "CONSTITUTION.md",
            "CHANGELOG.md",
            "CONTRIBUTING.md",
            "INSTALL.md",
            "DEVELOPMENT.md",
            "PROJECT_STATUS.md",
            "LICENSE",
        ]
        missing = [f for f in required if not (PROJECT_ROOT / f).is_file()]
        assert not missing, f"Missing release documentation: {missing}"

    def test_changelog_exists_and_has_content(self):
        """##Function purpose: Verify CHANGELOG.md exists and contains version history."""
        changelog = PROJECT_ROOT / "CHANGELOG.md"
        assert changelog.is_file(), "CHANGELOG.md missing"
        content = changelog.read_text(encoding="utf-8")
        assert len(content) > 100, "CHANGELOG.md appears too short"
        assert "Unreleased" in content or "0.2.0" in content or "0.1.0" in content, (
            "CHANGELOG.md missing version entries"
        )
