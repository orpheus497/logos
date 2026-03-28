##Script function and purpose: Workflow state tracking and management utilities

"""Provides utilities for tracking multi-agent workflow state.

Supports three workflow patterns:
- Diamond Workflow: Parallel execution followed by convergence
- Funnel Workflow: Parallel reviews converging to gatekeeper
- Maintenance Workflow: Sequential handoff between maintenance agents

Used by agents to update workflow state and by Orchestrator for coordination.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Optional


##Class purpose: Workflow type enumeration
class WorkflowType(Enum):
    """
    ##Class purpose: Enumerate available workflow patterns.
    """

    DIAMOND = "diamond"
    FUNNEL = "funnel"
    MAINTENANCE = "maintenance"


##Class purpose: Agent status in workflow
class AgentStatus(Enum):
    """
    ##Class purpose: Enumerate agent workflow step statuses.
    """

    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETE = "complete"
    WAITING = "waiting"
    BLOCKED = "blocked"


##Class purpose: Workflow step data
@dataclass
class WorkflowStep:
    """
    ##Class purpose: Represents a single step in a workflow.

    Attributes:
        step_number: Sequential step number (1, 2, 3...)
        step_name: Human-readable step name
        step_type: "sequential", "parallel", or "convergence"
        agents: List of agent keys involved in this step
        status: Overall step status
        agent_statuses: Dict mapping agent_key -> AgentStatus
        started: Datetime when step started (if applicable)
        completed: Datetime when step completed (if applicable)
        notes: Optional notes about this step
    """

    step_number: int
    step_name: str
    step_type: str
    agents: list[str]
    status: AgentStatus = AgentStatus.NOT_STARTED
    agent_statuses: dict[str, AgentStatus] = field(default_factory=dict)
    started: Optional[datetime] = None
    completed: Optional[datetime] = None
    notes: Optional[str] = None

    def all_agents_complete(self) -> bool:
        """
        ##Method purpose: Check if all agents in this step are complete.
        """
        return all(
            self.agent_statuses.get(agent) == AgentStatus.COMPLETE
            for agent in self.agents
        )

    def update_agent(self, agent_key: str, status: AgentStatus) -> None:
        """
        ##Method purpose: Update status for a specific agent in this step.
        """
        if agent_key not in self.agents:
            return
        self.agent_statuses[agent_key] = status
        if self.all_agents_complete():
            self.status = AgentStatus.COMPLETE
            self.completed = datetime.now(timezone.utc)
        elif any(
            s == AgentStatus.IN_PROGRESS for s in self.agent_statuses.values()
        ):
            self.status = AgentStatus.IN_PROGRESS


##Class purpose: Complete workflow state
@dataclass
class WorkflowState:
    """
    ##Class purpose: Represents complete workflow state.

    Attributes:
        workflow_type: Type of workflow (Diamond/Funnel/Maintenance)
        workflow_name: Human-readable workflow name
        started_by: Agent key that initiated workflow
        started_at: When workflow started
        current_step: Current step number
        steps: List of WorkflowStep objects
        overall_status: Overall workflow status
        completed_at: When workflow completed (if complete)
    """

    workflow_type: WorkflowType
    workflow_name: str
    started_by: str
    started_at: datetime
    current_step: int
    steps: list[WorkflowStep]
    overall_status: AgentStatus = AgentStatus.NOT_STARTED
    completed_at: Optional[datetime] = None

    @property
    def total_steps(self) -> int:
        """##Method purpose: Return total number of steps."""
        return len(self.steps)

    def advance_step(self) -> bool:
        """
        ##Method purpose: Advance to the next step if current is complete.

        Returns:
            True if advanced, False if current step not complete or already at end.
        """
        if self.current_step > len(self.steps):
            return False
        current = self.steps[self.current_step - 1]
        if current.status != AgentStatus.COMPLETE:
            return False
        if self.current_step >= len(self.steps):
            self.overall_status = AgentStatus.COMPLETE
            self.completed_at = datetime.now(timezone.utc)
            return False
        self.current_step += 1
        next_step = self.steps[self.current_step - 1]
        next_step.status = AgentStatus.NOT_STARTED
        next_step.started = datetime.now(timezone.utc)
        return True


##Function purpose: Create a standard Diamond workflow
def create_diamond_workflow(initiated_by: str, name: str = "Diamond Workflow") -> WorkflowState:
    """
    ##Function purpose: Create Diamond workflow (A1 -> [A2,A3,A4] -> A5 -> [B6-B9] -> B10).

    Args:
        initiated_by: Agent key that initiated the workflow
        name: Human-readable workflow name

    Returns:
        WorkflowState configured for Diamond pattern
    """
    now = datetime.now(timezone.utc)
    steps = [
        WorkflowStep(
            step_number=1,
            step_name="Architecture",
            step_type="sequential",
            agents=["A1"],
            agent_statuses={"A1": AgentStatus.NOT_STARTED},
        ),
        WorkflowStep(
            step_number=2,
            step_name="Parallel Implementation",
            step_type="parallel",
            agents=["A2", "A3", "A4"],
            agent_statuses={
                "A2": AgentStatus.NOT_STARTED,
                "A3": AgentStatus.NOT_STARTED,
                "A4": AgentStatus.NOT_STARTED,
            },
        ),
        WorkflowStep(
            step_number=3,
            step_name="Documentation",
            step_type="sequential",
            agents=["A5"],
            agent_statuses={"A5": AgentStatus.NOT_STARTED},
        ),
        WorkflowStep(
            step_number=4,
            step_name="Parallel Review",
            step_type="parallel",
            agents=["B6", "B7", "B8", "B9"],
            agent_statuses={
                "B6": AgentStatus.NOT_STARTED,
                "B7": AgentStatus.NOT_STARTED,
                "B8": AgentStatus.NOT_STARTED,
                "B9": AgentStatus.NOT_STARTED,
            },
        ),
        WorkflowStep(
            step_number=5,
            step_name="Release Approval",
            step_type="convergence",
            agents=["B10"],
            agent_statuses={"B10": AgentStatus.NOT_STARTED},
        ),
    ]
    return WorkflowState(
        workflow_type=WorkflowType.DIAMOND,
        workflow_name=name,
        started_by=initiated_by,
        started_at=now,
        current_step=1,
        steps=steps,
        overall_status=AgentStatus.NOT_STARTED,
    )


##Function purpose: Create a standard Funnel workflow
def create_funnel_workflow(initiated_by: str, name: str = "Funnel Workflow") -> WorkflowState:
    """
    ##Function purpose: Create Funnel workflow ([B6,B7,B8,B9] -> B10).

    Args:
        initiated_by: Agent key that initiated the workflow
        name: Human-readable workflow name

    Returns:
        WorkflowState configured for Funnel pattern
    """
    now = datetime.now(timezone.utc)
    steps = [
        WorkflowStep(
            step_number=1,
            step_name="Parallel Review",
            step_type="parallel",
            agents=["B6", "B7", "B8", "B9"],
            agent_statuses={
                "B6": AgentStatus.NOT_STARTED,
                "B7": AgentStatus.NOT_STARTED,
                "B8": AgentStatus.NOT_STARTED,
                "B9": AgentStatus.NOT_STARTED,
            },
        ),
        WorkflowStep(
            step_number=2,
            step_name="Release Approval",
            step_type="convergence",
            agents=["B10"],
            agent_statuses={"B10": AgentStatus.NOT_STARTED},
        ),
    ]
    return WorkflowState(
        workflow_type=WorkflowType.FUNNEL,
        workflow_name=name,
        started_by=initiated_by,
        started_at=now,
        current_step=1,
        steps=steps,
        overall_status=AgentStatus.NOT_STARTED,
    )


##Function purpose: Create a standard Maintenance workflow
def create_maintenance_workflow(
    agents: list[str],
    initiated_by: str,
    name: str = "Maintenance Workflow",
) -> WorkflowState:
    """
    ##Function purpose: Create Maintenance workflow (sequential agent handoff).

    Args:
        agents: Ordered list of agent keys for sequential execution
        initiated_by: Agent key that initiated the workflow
        name: Human-readable workflow name

    Returns:
        WorkflowState configured for Maintenance pattern
    """
    now = datetime.now(timezone.utc)
    steps = [
        WorkflowStep(
            step_number=i + 1,
            step_name=f"Step {i + 1}: {agent_key}",
            step_type="sequential",
            agents=[agent_key],
            agent_statuses={agent_key: AgentStatus.NOT_STARTED},
        )
        for i, agent_key in enumerate(agents)
    ]
    return WorkflowState(
        workflow_type=WorkflowType.MAINTENANCE,
        workflow_name=name,
        started_by=initiated_by,
        started_at=now,
        current_step=1,
        steps=steps,
        overall_status=AgentStatus.NOT_STARTED,
    )


##Function purpose: Get active workflow from tracking file
def get_active_workflow(devdocs_path: Path = Path(".devdocs")) -> Optional[WorkflowState]:
    """
    ##Function purpose: Read current active workflow from WORKFLOW_TRACKING/.

    Args:
        devdocs_path: Path to .devdocs folder

    Returns:
        WorkflowState object if active workflow exists, None if no workflow active
    """
    tracking_path = devdocs_path / "WORKFLOW_TRACKING"

    if not tracking_path.is_dir():
        return None

    workflow_files = {
        WorkflowType.DIAMOND: tracking_path / "diamond_workflow.md",
        WorkflowType.FUNNEL: tracking_path / "funnel_workflow.md",
        WorkflowType.MAINTENANCE: tracking_path / "maintenance_workflow.md",
    }

    for workflow_type, file_path in workflow_files.items():
        if not file_path.is_file():
            continue
        content = file_path.read_text(encoding="utf-8")
        ##Action purpose: Check status line for active workflows (handles both plain and markdown bold)
        has_active = ("Status:** ACTIVE" in content or "Status: ACTIVE" in content
                      or "Status:** IN PROGRESS" in content or "Status: IN PROGRESS" in content)
        if has_active:
            return parse_workflow_file(content, workflow_type)

    return None


##Function purpose: Parse workflow file content into WorkflowState
def parse_workflow_file(content: str, workflow_type: WorkflowType) -> WorkflowState:
    """
    ##Function purpose: Parse markdown workflow file into structured state.

    Args:
        content: Workflow file content
        workflow_type: Type of workflow

    Returns:
        WorkflowState object
    """
    lines = content.split("\n")

    ##Action purpose: Extract workflow name from header
    workflow_name = workflow_type.value.title() + " Workflow"
    for line in lines:
        if line.startswith("# "):
            workflow_name = line[2:].strip()
            break

    ##Action purpose: Extract initiated by from metadata
    started_by = "unknown"
    for line in lines:
        if "Initiated By:" in line or "Started By:" in line:
            parts = line.split(":", 1)
            if len(parts) > 1:
                started_by = parts[1].strip().strip("[]").strip("*").strip()
            break

    ##Action purpose: Parse step checkboxes to determine progress
    steps: list[WorkflowStep] = []
    step_num = 0
    for line in lines:
        if line.strip().startswith("- ["):
            step_num += 1
            is_complete = line.strip().startswith("- [x]") or line.strip().startswith("- [X]")
            step_text = line.strip()[6:].strip()

            ##Action purpose: Extract agent keys from step text
            agents: list[str] = []
            import re

            agent_matches = re.findall(r"\b([A-E]\d{1,2})\b", step_text)
            if agent_matches:
                agents = agent_matches

            status = AgentStatus.COMPLETE if is_complete else AgentStatus.NOT_STARTED
            agent_statuses = {a: status for a in agents}

            steps.append(
                WorkflowStep(
                    step_number=step_num,
                    step_name=step_text,
                    step_type="sequential",
                    agents=agents,
                    status=status,
                    agent_statuses=agent_statuses,
                )
            )

    ##Action purpose: Determine current step
    current_step = 1
    for step in steps:
        if step.status != AgentStatus.COMPLETE:
            current_step = step.step_number
            break
    else:
        current_step = len(steps) if steps else 1

    return WorkflowState(
        workflow_type=workflow_type,
        workflow_name=workflow_name,
        started_by=started_by,
        started_at=datetime.now(timezone.utc),
        current_step=current_step,
        steps=steps,
        overall_status=AgentStatus.COMPLETE if all(s.status == AgentStatus.COMPLETE for s in steps) else AgentStatus.IN_PROGRESS,
    )


##Function purpose: Format workflow state as markdown for tracking file
def format_workflow_markdown(state: WorkflowState) -> str:
    """
    ##Function purpose: Render WorkflowState as markdown for .devdocs tracking file.

    Args:
        state: WorkflowState to format

    Returns:
        Markdown string for writing to workflow tracking file
    """
    status_label = "ACTIVE" if state.overall_status != AgentStatus.COMPLETE else "COMPLETE"
    lines = [
        f"# {state.workflow_name}",
        "",
        f"**Status:** {status_label}",
        f"**Started:** {state.started_at.strftime('%Y-%m-%d')}",
        f"**Initiated By:** {state.started_by}",
        "",
        "## Current Progress",
        "",
    ]

    for step in state.steps:
        check = "x" if step.status == AgentStatus.COMPLETE else " "
        agent_list = ", ".join(step.agents)
        lines.append(f"- [{check}] **Step {step.step_number}: {step.step_name}** ({agent_list})")

        ##Action purpose: Show sub-agent status for parallel steps
        if step.step_type == "parallel" and len(step.agents) > 1:
            for agent in step.agents:
                agent_status = step.agent_statuses.get(agent, AgentStatus.NOT_STARTED)
                sub_check = "x" if agent_status == AgentStatus.COMPLETE else " "
                lines.append(f"  - [{sub_check}] {agent}: {agent_status.value}")

    lines.extend(["", "## Blockers", "- None"])

    if state.completed_at:
        lines.extend([
            "",
            f"## Completed: {state.completed_at.strftime('%Y-%m-%d %H:%M')} UTC",
        ])

    return "\n".join(lines) + "\n"
