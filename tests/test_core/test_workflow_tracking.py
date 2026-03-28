"""
##Script function and purpose: Tests for workflow tracking module.

Tests workflow state management, creation helpers, step advancement,
and markdown formatting.
"""

from datetime import datetime, timezone

import pytest

from logos.core.workflow_tracking import (
    AgentStatus,
    WorkflowStep,
    WorkflowType,
    create_diamond_workflow,
    create_funnel_workflow,
    create_maintenance_workflow,
    format_workflow_markdown,
    get_active_workflow,
    parse_workflow_file,
)


##Class purpose: Test WorkflowType enum
class TestWorkflowType:
    """Tests for WorkflowType enumeration."""

    def test_diamond_value(self):
        """Test diamond value."""
        assert WorkflowType.DIAMOND.value == "diamond"

    def test_funnel_value(self):
        """Test funnel value."""
        assert WorkflowType.FUNNEL.value == "funnel"

    def test_maintenance_value(self):
        """Test maintenance value."""
        assert WorkflowType.MAINTENANCE.value == "maintenance"


##Class purpose: Test AgentStatus enum
class TestAgentStatus:
    """Tests for AgentStatus enumeration."""

    def test_all_statuses_exist(self):
        """Test all statuses exist."""
        statuses = [s.value for s in AgentStatus]
        assert "not_started" in statuses
        assert "in_progress" in statuses
        assert "complete" in statuses
        assert "waiting" in statuses
        assert "blocked" in statuses


##Class purpose: Test WorkflowStep dataclass
class TestWorkflowStep:
    """Tests for WorkflowStep dataclass."""

    def test_creation(self):
        """Test creation."""
        step = WorkflowStep(
            step_number=1,
            step_name="Architecture",
            step_type="sequential",
            agents=["A1"],
        )
        assert step.step_number == 1
        assert step.step_name == "Architecture"
        assert step.agents == ["A1"]
        assert step.status == AgentStatus.NOT_STARTED

    def test_all_agents_complete_single(self):
        """Test all agents complete single."""
        step = WorkflowStep(
            step_number=1,
            step_name="Architecture",
            step_type="sequential",
            agents=["A1"],
            agent_statuses={"A1": AgentStatus.COMPLETE},
        )
        assert step.all_agents_complete() is True

    def test_all_agents_complete_parallel(self):
        """Test all agents complete parallel."""
        step = WorkflowStep(
            step_number=2,
            step_name="Implementation",
            step_type="parallel",
            agents=["A2", "A3", "A4"],
            agent_statuses={
                "A2": AgentStatus.COMPLETE,
                "A3": AgentStatus.COMPLETE,
                "A4": AgentStatus.COMPLETE,
            },
        )
        assert step.all_agents_complete() is True

    def test_not_all_agents_complete(self):
        """Test not all agents complete."""
        step = WorkflowStep(
            step_number=2,
            step_name="Implementation",
            step_type="parallel",
            agents=["A2", "A3", "A4"],
            agent_statuses={
                "A2": AgentStatus.COMPLETE,
                "A3": AgentStatus.IN_PROGRESS,
                "A4": AgentStatus.NOT_STARTED,
            },
        )
        assert step.all_agents_complete() is False

    def test_update_agent_sets_status(self):
        """Test update agent sets status."""
        step = WorkflowStep(
            step_number=1,
            step_name="Architecture",
            step_type="sequential",
            agents=["A1"],
            agent_statuses={"A1": AgentStatus.NOT_STARTED},
        )
        step.update_agent("A1", AgentStatus.IN_PROGRESS)
        assert step.agent_statuses["A1"] == AgentStatus.IN_PROGRESS
        assert step.status == AgentStatus.IN_PROGRESS

    def test_update_agent_completes_step(self):
        """Test update agent completes step."""
        step = WorkflowStep(
            step_number=1,
            step_name="Architecture",
            step_type="sequential",
            agents=["A1"],
            agent_statuses={"A1": AgentStatus.NOT_STARTED},
        )
        step.update_agent("A1", AgentStatus.COMPLETE)
        assert step.status == AgentStatus.COMPLETE
        assert step.completed is not None

    def test_update_unknown_agent_ignored(self):
        """Test update unknown agent ignored."""
        step = WorkflowStep(
            step_number=1,
            step_name="Architecture",
            step_type="sequential",
            agents=["A1"],
            agent_statuses={"A1": AgentStatus.NOT_STARTED},
        )
        step.update_agent("B6", AgentStatus.COMPLETE)
        assert step.agent_statuses.get("B6") is None

    def test_parallel_step_completes_when_all_done(self):
        """Test parallel step completes when all done."""
        step = WorkflowStep(
            step_number=2,
            step_name="Implementation",
            step_type="parallel",
            agents=["A2", "A3"],
            agent_statuses={
                "A2": AgentStatus.NOT_STARTED,
                "A3": AgentStatus.NOT_STARTED,
            },
        )
        step.update_agent("A2", AgentStatus.COMPLETE)
        assert step.status != AgentStatus.COMPLETE

        step.update_agent("A3", AgentStatus.COMPLETE)
        assert step.status == AgentStatus.COMPLETE


##Class purpose: Test Diamond workflow creation
class TestCreateDiamondWorkflow:
    """Tests for create_diamond_workflow helper."""

    def test_creates_five_steps(self):
        """Test creates five steps."""
        wf = create_diamond_workflow("A1")
        assert len(wf.steps) == 5
        assert wf.total_steps == 5

    def test_workflow_type(self):
        """Test workflow type."""
        wf = create_diamond_workflow("A1")
        assert wf.workflow_type == WorkflowType.DIAMOND

    def test_step_names(self):
        """Test step names."""
        wf = create_diamond_workflow("A1")
        names = [s.step_name for s in wf.steps]
        assert "Architecture" in names
        assert "Parallel Implementation" in names
        assert "Documentation" in names
        assert "Parallel Review" in names
        assert "Release Approval" in names

    def test_parallel_step_has_multiple_agents(self):
        """Test parallel step has multiple agents."""
        wf = create_diamond_workflow("A1")
        impl_step = wf.steps[1]
        assert len(impl_step.agents) == 3
        assert impl_step.step_type == "parallel"

    def test_started_by(self):
        """Test started by."""
        wf = create_diamond_workflow("A1", name="Test Diamond")
        assert wf.started_by == "A1"
        assert wf.workflow_name == "Test Diamond"

    def test_initial_status(self):
        """Test initial status."""
        wf = create_diamond_workflow("A1")
        assert wf.overall_status == AgentStatus.NOT_STARTED
        assert wf.current_step == 1


##Class purpose: Test Funnel workflow creation
class TestCreateFunnelWorkflow:
    """Tests for create_funnel_workflow helper."""

    def test_creates_two_steps(self):
        """Test creates two steps."""
        wf = create_funnel_workflow("B6")
        assert len(wf.steps) == 2

    def test_parallel_review_step(self):
        """Test parallel review step."""
        wf = create_funnel_workflow("B6")
        assert wf.steps[0].step_type == "parallel"
        assert len(wf.steps[0].agents) == 4

    def test_convergence_step(self):
        """Test convergence step."""
        wf = create_funnel_workflow("B6")
        assert wf.steps[1].step_type == "convergence"
        assert wf.steps[1].agents == ["B10"]


##Class purpose: Test Maintenance workflow creation
class TestCreateMaintenanceWorkflow:
    """Tests for create_maintenance_workflow helper."""

    def test_creates_sequential_steps(self):
        """Test creates sequential steps."""
        agents = ["C1", "C6", "C7"]
        wf = create_maintenance_workflow(agents, "C1")
        assert len(wf.steps) == 3
        for step in wf.steps:
            assert step.step_type == "sequential"

    def test_each_step_has_one_agent(self):
        """Test each step has one agent."""
        agents = ["C1", "C6"]
        wf = create_maintenance_workflow(agents, "C1")
        for step in wf.steps:
            assert len(step.agents) == 1


##Class purpose: Test WorkflowState advancement
class TestWorkflowStateAdvancement:
    """Tests for WorkflowState step advancement."""

    def test_advance_step_when_complete(self):
        """Test advance step when complete."""
        wf = create_diamond_workflow("A1")
        wf.steps[0].status = AgentStatus.COMPLETE
        wf.steps[0].agent_statuses["A1"] = AgentStatus.COMPLETE
        result = wf.advance_step()
        assert result is True
        assert wf.current_step == 2

    def test_advance_step_when_not_complete(self):
        """Test advance step when not complete."""
        wf = create_diamond_workflow("A1")
        result = wf.advance_step()
        assert result is False
        assert wf.current_step == 1

    def test_advance_last_step_completes_workflow(self):
        """Test advance last step completes workflow."""
        wf = create_funnel_workflow("B6")
        wf.current_step = 2
        wf.steps[0].status = AgentStatus.COMPLETE
        wf.steps[1].status = AgentStatus.COMPLETE
        wf.steps[1].agent_statuses["B10"] = AgentStatus.COMPLETE
        result = wf.advance_step()
        assert result is False
        assert wf.overall_status == AgentStatus.COMPLETE
        assert wf.completed_at is not None


##Class purpose: Test markdown formatting
class TestFormatWorkflowMarkdown:
    """Tests for format_workflow_markdown."""

    def test_contains_workflow_name(self):
        """Test contains workflow name."""
        wf = create_diamond_workflow("A1", name="Feature X Diamond")
        md = format_workflow_markdown(wf)
        assert "# Feature X Diamond" in md

    def test_contains_status(self):
        """Test contains status."""
        wf = create_diamond_workflow("A1")
        md = format_workflow_markdown(wf)
        assert "**Status:** ACTIVE" in md

    def test_complete_status(self):
        """Test complete status."""
        wf = create_diamond_workflow("A1")
        wf.overall_status = AgentStatus.COMPLETE
        wf.completed_at = datetime(2026, 3, 28, 12, 0, tzinfo=timezone.utc)
        md = format_workflow_markdown(wf)
        assert "**Status:** COMPLETE" in md
        assert "## Completed:" in md

    def test_contains_step_checkboxes(self):
        """Test contains step checkboxes."""
        wf = create_diamond_workflow("A1")
        md = format_workflow_markdown(wf)
        assert "- [ ]" in md
        assert "Step 1" in md

    def test_complete_step_checked(self):
        """Test complete step checked."""
        wf = create_diamond_workflow("A1")
        wf.steps[0].status = AgentStatus.COMPLETE
        md = format_workflow_markdown(wf)
        assert "- [x]" in md

    def test_parallel_step_shows_sub_agents(self):
        """Test parallel step shows sub agents."""
        wf = create_diamond_workflow("A1")
        md = format_workflow_markdown(wf)
        assert "A2:" in md
        assert "A3:" in md


##Class purpose: Test parse_workflow_file
class TestParseWorkflowFile:
    """Tests for parse_workflow_file."""

    def test_parses_active_workflow(self):
        """Test parses active workflow."""
        content = """# Test Workflow

**Status:** ACTIVE
**Started:** 2026-03-28
**Initiated By:** A1

## Current Progress

- [x] **Step 1: Architecture (A1)** - Complete
- [ ] **Step 2: Implementation (A2, A3)** - In Progress
- [ ] **Step 3: Review (B9)** - Not Started
"""
        state = parse_workflow_file(content, WorkflowType.DIAMOND)
        assert state.workflow_name == "Test Workflow"
        assert state.workflow_type == WorkflowType.DIAMOND
        assert len(state.steps) == 3
        assert state.steps[0].status == AgentStatus.COMPLETE

    def test_parses_initiated_by(self):
        """Test parses initiated by."""
        content = """# Workflow
**Initiated By:** B6
- [ ] Step 1 (B6)
"""
        state = parse_workflow_file(content, WorkflowType.FUNNEL)
        assert state.started_by == "B6"

    def test_parses_agent_keys_from_steps(self):
        """Test parses agent keys from steps."""
        content = """# Workflow
- [ ] **Step 1 (A2, A3, A4)**
"""
        state = parse_workflow_file(content, WorkflowType.DIAMOND)
        assert "A2" in state.steps[0].agents
        assert "A3" in state.steps[0].agents
        assert "A4" in state.steps[0].agents


##Class purpose: Test get_active_workflow
class TestGetActiveWorkflow:
    """Tests for get_active_workflow."""

    def test_returns_none_when_no_devdocs(self, tmp_path):
        """Test returns none when no devdocs."""
        result = get_active_workflow(tmp_path / "nonexistent")
        assert result is None

    def test_returns_none_when_no_active(self, tmp_path):
        """Test returns none when no active."""
        tracking = tmp_path / "WORKFLOW_TRACKING"
        tracking.mkdir(parents=True)
        (tracking / "diamond_workflow.md").write_text("# Diamond\n**Status:** COMPLETE\n")
        result = get_active_workflow(tmp_path)
        assert result is None

    def test_returns_active_workflow(self, tmp_path):
        """Test returns active workflow."""
        tracking = tmp_path / "WORKFLOW_TRACKING"
        tracking.mkdir(parents=True)
        (tracking / "diamond_workflow.md").write_text("# Active Diamond\n**Status:** ACTIVE\n- [ ] **Step 1 (A1)**\n")
        result = get_active_workflow(tmp_path)
        assert result is not None
        assert result.workflow_name == "Active Diamond"
        assert result.workflow_type == WorkflowType.DIAMOND

    def test_returns_in_progress_workflow(self, tmp_path):
        """Test returns in progress workflow."""
        tracking = tmp_path / "WORKFLOW_TRACKING"
        tracking.mkdir(parents=True)
        (tracking / "funnel_workflow.md").write_text("# Funnel\n**Status:** IN PROGRESS\n- [ ] **Step 1 (B6)**\n")
        result = get_active_workflow(tmp_path)
        assert result is not None
        assert result.workflow_type == WorkflowType.FUNNEL


##Class purpose: Test END-OF-TASK protocol presence in agent prompts
class TestEndOfTaskProtocolPresence:
    """Tests that all 50 agent activation prompts contain END-OF-TASK protocol."""

    @pytest.fixture()
    def daedelus_prompts(self):
        """Provide Daedelus agent prompt fixtures."""
        from logos.daedelus.prompts.agents import builders, guardians, maintainers, operators, workers

        return {
            "A1": builders.ARCHITECT_ACTIVATION,
            "A2": builders.LOGIC_ENGINEER_ACTIVATION,
            "A3": builders.INTERFACE_DESIGNER_ACTIVATION,
            "A4": builders.TEST_ENGINEER_ACTIVATION,
            "A5": builders.SCRIBE_ACTIVATION,
            "B6": guardians.SENTINEL_ACTIVATION,
            "B7": guardians.MARSHAL_ACTIVATION,
            "B8": guardians.PROFILER_ACTIVATION,
            "B9": guardians.CRITIC_ACTIVATION,
            "B10": guardians.GATEKEEPER_ACTIVATION,
            "C1": maintainers.BUG_HUNTER_ACTIVATION,
            "C6": maintainers.SECURITY_PATCHER_ACTIVATION,
            "C7": maintainers.DOC_UPDATER_ACTIVATION,
            "C8": maintainers.CONFIGURATOR_ACTIVATION,
            "C9": maintainers.OPTIMIZER_ACTIVATION,
            "C10": maintainers.JANITOR_ACTIVATION,
            "C11": maintainers.LIBRARIAN_ACTIVATION,
            "D2": workers.FEATURE_SPRINTER_ACTIVATION,
            "D3": workers.REFACTORER_ACTIVATION,
            "D4": workers.UI_TWEAKER_ACTIVATION,
            "D5": workers.TEST_EXTENDER_ACTIVATION,
            "E1": operators.ORCHESTRATOR_ACTIVATION,
            "E2": operators.OPERATIONAL_CONTROL_MANAGER_ACTIVATION,
            "E3": operators.DAEDELUS_ACTIVATION,
        }

    @pytest.fixture()
    def deus_prompts(self):
        """Provide DEUS agent prompt fixtures."""
        from logos.deus.prompts.agents import auditors, engineers, maintainers, operators, specialists

        return {
            "A1": engineers.KERNEL_ARCHITECT_ACTIVATION,
            "A2": engineers.DRIVER_ENGINEER_ACTIVATION,
            "A3": engineers.NETWORK_ARCHITECT_ACTIVATION,
            "A4": engineers.BOOT_ENGINEER_ACTIVATION,
            "A5": engineers.SERVICE_SCRIBE_ACTIVATION,
            "B6": auditors.SECURITY_AUDITOR_ACTIVATION,
            "B7": auditors.SYNTAX_MARSHAL_ACTIVATION,
            "B8": auditors.PERFORMANCE_ANALYST_ACTIVATION,
            "B9": auditors.COMPLIANCE_CRITIC_ACTIVATION,
            "B10": auditors.RELEASE_GATEKEEPER_ACTIVATION,
            "C1": maintainers.BUG_HUNTER_ACTIVATION,
            "C6": maintainers.SECURITY_PATCHER_ACTIVATION,
            "C7": maintainers.MANUAL_KEEPER_ACTIVATION,
            "C8": maintainers.SYSCTL_TUNER_ACTIVATION,
            "C9": maintainers.OPTIMIZER_ACTIVATION,
            "C10": maintainers.SYSTEM_JANITOR_ACTIVATION,
            "C11": maintainers.PORT_LIBRARIAN_ACTIVATION,
            "D2": specialists.PORT_BUILDER_ACTIVATION,
            "D3": specialists.COMPATIBILITY_ENGINEER_ACTIVATION,
            "D4": specialists.JAIL_ARCHITECT_ACTIVATION,
            "D5": specialists.ZFS_ENGINEER_ACTIVATION,
            "E1": operators.SYSTEM_ORCHESTRATOR_ACTIVATION,
            "E2": operators.ADMINISTRATOR_ACTIVATION,
            "E3": operators.GENERAL_MANAGER_ACTIVATION,
            "E4": operators.OMBUDSMAN_ACTIVATION,
            "E5": operators.DEUS_ACTIVATION,
        }

    def test_all_daedelus_agents_have_end_of_task(self, daedelus_prompts):
        """Verify all 24 Daedelus agents have END-OF-TASK protocol."""
        for agent_key, prompt in daedelus_prompts.items():
            assert "END-OF-TASK PROTOCOL" in prompt, f"Daedelus agent {agent_key} missing END-OF-TASK protocol"

    def test_all_deus_agents_have_end_of_task(self, deus_prompts):
        """Verify all 26 DEUS agents have END-OF-TASK protocol."""
        for agent_key, prompt in deus_prompts.items():
            assert "END-OF-TASK PROTOCOL" in prompt, f"DEUS agent {agent_key} missing END-OF-TASK protocol"

    def test_daedelus_end_of_task_contains_required_steps(self, daedelus_prompts):
        """Verify END-OF-TASK contains all 4 required steps."""
        for agent_key, prompt in daedelus_prompts.items():
            assert "Step 1: Update .devdocs/DEV_STATE.md" in prompt, f"Daedelus {agent_key} missing Step 1"
            assert "Step 2: Update Your Agent Log" in prompt, f"Daedelus {agent_key} missing Step 2"
            assert "Step 3: Recommend Next Agent" in prompt, f"Daedelus {agent_key} missing Step 3"
            assert "Step 4: Report Completion" in prompt, f"Daedelus {agent_key} missing Step 4"

    def test_deus_end_of_task_contains_required_steps(self, deus_prompts):
        """Verify END-OF-TASK contains all 4 required steps."""
        for agent_key, prompt in deus_prompts.items():
            assert "Step 1: Update .devdocs/DEV_STATE.md" in prompt, f"DEUS {agent_key} missing Step 1"
            assert "Step 2: Update Your Agent Log" in prompt, f"DEUS {agent_key} missing Step 2"
            assert "Step 3: Recommend Next Agent" in prompt, f"DEUS {agent_key} missing Step 3"
            assert "Step 4: Report Completion" in prompt, f"DEUS {agent_key} missing Step 4"

    def test_daedelus_end_of_task_has_agent_specific_recommendations(self, daedelus_prompts):
        """Verify each agent has specific next-agent recommendations (not generic)."""
        for agent_key, prompt in daedelus_prompts.items():
            assert "Recommend" in prompt or "recommend" in prompt, f"Daedelus {agent_key} missing recommendations"

    def test_deus_end_of_task_has_agent_specific_recommendations(self, deus_prompts):
        """Verify each agent has specific next-agent recommendations."""
        for agent_key, prompt in deus_prompts.items():
            assert "Recommend" in prompt or "recommend" in prompt, f"DEUS {agent_key} missing recommendations"

    def test_end_of_task_count_matches_agent_count(self, daedelus_prompts, deus_prompts):
        """Verify we have exactly 50 agents with END-OF-TASK."""
        daedelus_count = sum(1 for p in daedelus_prompts.values() if "END-OF-TASK PROTOCOL" in p)
        deus_count = sum(1 for p in deus_prompts.values() if "END-OF-TASK PROTOCOL" in p)
        assert daedelus_count == 24, f"Expected 24 Daedelus agents, got {daedelus_count}"
        assert deus_count == 26, f"Expected 26 DEUS agents, got {deus_count}"
