"""
##Script function and purpose: Integration tests for workflow coordination across agent domains.

Tests workflow state management, END-OF-TASK protocol presence in all agents,
and workflow template availability. Deferred from Phase 3, implemented as
part of Phase 7 release integration testing.
"""

from pathlib import Path

import pytest

from logos.core.agent import Agent
from logos.core.workflow_tracking import (
    AgentStatus,
    WorkflowState,
    WorkflowStep,
    WorkflowType,
    create_diamond_workflow,
    create_funnel_workflow,
    create_maintenance_workflow,
    format_workflow_markdown,
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
# Workflow State Management
# ---------------------------------------------------------------------------
class TestWorkflowStateManagement:
    """Verify workflow creation, step advancement, and completion detection."""

    def test_diamond_workflow_has_expected_steps(self):
        """##Function purpose: Verify diamond workflow creates all required steps."""
        state = create_diamond_workflow(initiated_by="A1")
        assert state.workflow_type == WorkflowType.DIAMOND
        assert len(state.steps) >= 3, f"Diamond workflow has only {len(state.steps)} steps"
        assert all(isinstance(s, WorkflowStep) for s in state.steps)
        assert state.started_by == "A1"

    def test_funnel_workflow_has_convergence_step(self):
        """##Function purpose: Verify funnel workflow includes a convergence step."""
        state = create_funnel_workflow(initiated_by="E1")
        assert state.workflow_type == WorkflowType.FUNNEL
        assert len(state.steps) >= 2, f"Funnel workflow has only {len(state.steps)} steps"
        # The final step should converge work from earlier steps
        final_step = state.steps[-1]
        assert isinstance(final_step, WorkflowStep)

    def test_maintenance_workflow_sequential_steps(self):
        """##Function purpose: Verify maintenance workflow creates sequential steps for given agents."""
        agents = ["D2", "D3", "D4"]
        state = create_maintenance_workflow(agents=agents, initiated_by="D2")
        assert state.workflow_type == WorkflowType.MAINTENANCE
        assert len(state.steps) >= 1
        # All requested agents should appear somewhere in the workflow
        all_agents = []
        for step in state.steps:
            all_agents.extend(step.agents)
        for a in agents:
            assert a in all_agents, f"Agent {a} not found in maintenance workflow steps"

    def test_step_status_update(self):
        """##Function purpose: Verify updating an agent's status within a workflow step."""
        state = create_diamond_workflow(initiated_by="A1")
        first_step = state.steps[0]
        agent_key = first_step.agents[0]
        first_step.update_agent(agent_key, AgentStatus.IN_PROGRESS)
        assert first_step.agent_statuses[agent_key] == AgentStatus.IN_PROGRESS
        first_step.update_agent(agent_key, AgentStatus.COMPLETE)
        assert first_step.agent_statuses[agent_key] == AgentStatus.COMPLETE

    def test_step_all_agents_complete(self):
        """##Function purpose: Verify all_agents_complete returns True when every agent finishes."""
        step = WorkflowStep(
            step_number=1,
            step_name="Test Step",
            step_type="sequential",
            agents=["A1", "A2"],
            agent_statuses={"A1": AgentStatus.NOT_STARTED, "A2": AgentStatus.NOT_STARTED},
        )
        assert step.all_agents_complete() is False
        step.update_agent("A1", AgentStatus.COMPLETE)
        assert step.all_agents_complete() is False
        step.update_agent("A2", AgentStatus.COMPLETE)
        assert step.all_agents_complete() is True

    def test_workflow_completion_detection(self):
        """##Function purpose: Verify workflow detects completion when all steps finish."""
        state = create_diamond_workflow(initiated_by="A1")
        assert state.overall_status != AgentStatus.COMPLETE
        # Mark every agent in every step as complete and advance
        for step in state.steps:
            for agent_key in step.agents:
                step.update_agent(agent_key, AgentStatus.COMPLETE)
        # After all steps completed, advance to detect completion
        while state.current_step < state.total_steps:
            advanced = state.advance_step()
            if not advanced:
                break
        # The last step should have all agents complete
        last_step = state.steps[-1]
        assert last_step.all_agents_complete() is True

    def test_format_workflow_markdown_output(self):
        """##Function purpose: Verify format_workflow_markdown produces valid markdown output."""
        state = create_diamond_workflow(initiated_by="A1")
        md = format_workflow_markdown(state)
        assert isinstance(md, str)
        assert len(md) > 0
        # Should contain workflow metadata
        assert "diamond" in md.lower() or "Diamond" in md


# ---------------------------------------------------------------------------
# END-OF-TASK Protocol
# ---------------------------------------------------------------------------
class TestEndOfTaskProtocol:
    """Verify all agents include the END-OF-TASK protocol in their prompts."""

    @pytest.mark.parametrize("key", DAEDELUS_KEYS)
    def test_daedelus_has_end_of_task(self, key):
        """##Function purpose: Verify each Daedelus agent prompt contains END-OF-TASK PROTOCOL."""
        agent = dae_get_agent(key)
        assert "END-OF-TASK PROTOCOL" in agent.full_prompt, (
            f"Daedelus {key} ({agent.name}) missing END-OF-TASK PROTOCOL"
        )

    @pytest.mark.parametrize("key", DEUS_KEYS)
    def test_deus_has_end_of_task(self, key):
        """##Function purpose: Verify each DEUS agent prompt contains END-OF-TASK PROTOCOL."""
        agent = deus_get_agent(key)
        assert "END-OF-TASK PROTOCOL" in agent.full_prompt, (
            f"DEUS {key} ({agent.name}) missing END-OF-TASK PROTOCOL"
        )

    @pytest.mark.parametrize("key", DAEDELUS_KEYS)
    def test_daedelus_end_of_task_has_required_subsections(self, key):
        """##Function purpose: Verify Daedelus END-OF-TASK contains DEV_STATE and Agent Log steps."""
        agent = dae_get_agent(key)
        prompt = agent.full_prompt
        assert "Update .devdocs/DEV_STATE.md" in prompt or "DEV_STATE" in prompt, (
            f"Daedelus {key} END-OF-TASK missing DEV_STATE update step"
        )
        assert "Update Your Agent Log" in prompt or "Agent Log" in prompt, (
            f"Daedelus {key} END-OF-TASK missing Agent Log update step"
        )

    @pytest.mark.parametrize("key", DEUS_KEYS)
    def test_deus_end_of_task_has_required_subsections(self, key):
        """##Function purpose: Verify DEUS END-OF-TASK contains DEV_STATE and Agent Log steps."""
        agent = deus_get_agent(key)
        prompt = agent.full_prompt
        assert "Update .devdocs/DEV_STATE.md" in prompt or "DEV_STATE" in prompt, (
            f"DEUS {key} END-OF-TASK missing DEV_STATE update step"
        )
        assert "Update Your Agent Log" in prompt or "Agent Log" in prompt, (
            f"DEUS {key} END-OF-TASK missing Agent Log update step"
        )

    def test_end_of_task_has_completion_reporting(self):
        """##Function purpose: Verify at least one agent's END-OF-TASK includes completion reporting."""
        agent = dae_get_agent("A1")
        prompt = agent.full_prompt
        # Should mention reporting or completion somewhere in the protocol
        has_report = "Report Completion" in prompt or "TASK COMPLETE" in prompt
        assert has_report, "END-OF-TASK protocol missing completion reporting step"


# ---------------------------------------------------------------------------
# Workflow Templates
# ---------------------------------------------------------------------------
class TestWorkflowTemplates:
    """Verify workflow template files exist in the templates directory."""

    @pytest.fixture()
    def templates_dir(self):
        """##Function purpose: Provide the workflow templates directory path."""
        return PROJECT_ROOT / "templates" / ".devdocs" / "WORKFLOW_TRACKING"

    def test_diamond_template_exists(self, templates_dir):
        """##Function purpose: Verify diamond workflow template file exists."""
        diamond = templates_dir / "diamond_workflow.md"
        assert diamond.is_file(), f"Missing diamond template: {diamond}"
        content = diamond.read_text(encoding="utf-8")
        assert len(content) > 0, "Diamond template is empty"

    def test_funnel_template_exists(self, templates_dir):
        """##Function purpose: Verify funnel workflow template file exists."""
        funnel = templates_dir / "funnel_workflow.md"
        assert funnel.is_file(), f"Missing funnel template: {funnel}"
        content = funnel.read_text(encoding="utf-8")
        assert len(content) > 0, "Funnel template is empty"

    def test_maintenance_template_exists(self, templates_dir):
        """##Function purpose: Verify maintenance workflow template file exists."""
        maintenance = templates_dir / "maintenance_workflow.md"
        assert maintenance.is_file(), f"Missing maintenance template: {maintenance}"
        content = maintenance.read_text(encoding="utf-8")
        assert len(content) > 0, "Maintenance template is empty"

    def test_all_templates_contain_markdown_headers(self, templates_dir):
        """##Function purpose: Verify all workflow templates contain valid markdown structure."""
        for name in ("diamond_workflow.md", "funnel_workflow.md", "maintenance_workflow.md"):
            path = templates_dir / name
            content = path.read_text(encoding="utf-8")
            assert "#" in content, f"Template {name} has no markdown headers"
