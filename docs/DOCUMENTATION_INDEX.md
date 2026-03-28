# LOGOS Documentation Index

> **Cross-reference index of all documentation files in the LOGOS project.**
>
> **Maintained by:** C7 — The Doc Updater (Daedelus) / The Manual Keeper (DEUS)
>
> **Last Updated:** 2026-03-28

---

## Root Documentation

| File | Purpose | Audience |
|------|---------|----------|
| [README.md](../README.md) | Project overview, installation, usage, architecture | All |
| [CONSTITUTION.md](../CONSTITUTION.md) | Governance framework, agent architecture, constitutional authority | All |
| [PLAN.md](../PLAN.md) | Development roadmap v0.1.0 → v0.2.0, phase breakdown | Developers |
| [PROJECT_STATUS.md](../PROJECT_STATUS.md) | Phase-by-phase status analysis, completion metrics | Developers |
| [CHANGELOG.md](../CHANGELOG.md) | Version history and release notes | All |
| [DEVELOPMENT.md](../DEVELOPMENT.md) | Development status quick links, phase tracker | Developers |
| [INSTALL.md](../INSTALL.md) | Installation guide (Linux, FreeBSD) | Users |
| [CONTRIBUTING.md](../CONTRIBUTING.md) | Contribution guidelines, code style, PR process | Contributors |
| [LICENSE](../LICENSE) | GNU Affero General Public License v3.0 | All |
| [doc.md](../doc.md) | Additional documentation | Developers |

---

## `/docs/` — Project Documentation

### Guides and References

| File | Purpose | Key Agents |
|------|---------|------------|
| [CLI_USAGE.md](CLI_USAGE.md) | CLI reference: modes, flags, aliases, configuration | All |
| [AGENT_BOUNDARIES.md](AGENT_BOUNDARIES.md) | Boundary specs for all 50 agents (scope, forbidden, redirects) | All |
| [AGENT_RECOMMENDATIONS.md](AGENT_RECOMMENDATIONS.md) | Agent selection workflow matrix | All |
| [WORKFLOWS.md](WORKFLOWS.md) | Workflow summaries: Diamond, Funnel, Maintenance | All |
| [FACTIONS.md](FACTIONS.md) | Five factions: philosophy, autonomy levels, use cases | All |
| [DOCUMENTATION_GUIDE.md](DOCUMENTATION_GUIDE.md) | Documentation system guide (three domains) | C7, E1 |
| [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md) | This file — cross-reference index | All |
| [OS_ADAPTATIONS.md](OS_ADAPTATIONS.md) | OS adaptation architecture | DEUS agents |
| [DEUS_LINUX_REFERENCE.md](DEUS_LINUX_REFERENCE.md) | Linux commands and config reference | DEUS agents |
| [DEUS_FREEBSD_REFERENCE.md](DEUS_FREEBSD_REFERENCE.md) | FreeBSD commands and config reference | DEUS agents |
| [SHELL_COMPLETION.md](SHELL_COMPLETION.md) | Shell completion setup (Bash, Zsh, Fish) | Users |

### Architecture Documents

| File | Purpose |
|------|---------|
| [architecture/DOCUMENTATION_ARCHITECTURE.md](architecture/DOCUMENTATION_ARCHITECTURE.md) | Three-layer documentation architecture overview |

### Workflow Examples

| File | Purpose |
|------|---------|
| [examples/ORCHESTRATOR_WORKFLOW.md](examples/ORCHESTRATOR_WORKFLOW.md) | E1 managing `.devdocs/`: init, audit, drift detection, archival |
| [examples/DOC_UPDATER_WORKFLOW.md](examples/DOC_UPDATER_WORKFLOW.md) | C7 maintaining docs: update, sync, inline docs, coordination |

---

## `/templates/` — Templates

### `.devdocs/` Templates (Agent Working Memory)

| File | Purpose | Owner |
|------|---------|-------|
| [templates/.devdocs/README.md](../templates/.devdocs/README.md) | `.devdocs/` folder guide | E1 |
| [templates/.devdocs/DEV_STATE.md](../templates/.devdocs/DEV_STATE.md) | Project state template (single source of truth) | E1 |
| [templates/.devdocs/AGENT_LOGS/group_a/AGENT_LOG_TEMPLATE.md](../templates/.devdocs/AGENT_LOGS/group_a/AGENT_LOG_TEMPLATE.md) | Per-agent log entry template | E1 |
| [templates/.devdocs/WORKFLOW_TRACKING/diamond_workflow.md](../templates/.devdocs/WORKFLOW_TRACKING/diamond_workflow.md) | Diamond workflow tracking (creation) | E1 |
| [templates/.devdocs/WORKFLOW_TRACKING/funnel_workflow.md](../templates/.devdocs/WORKFLOW_TRACKING/funnel_workflow.md) | Funnel workflow tracking (review) | E1 |
| [templates/.devdocs/WORKFLOW_TRACKING/maintenance_workflow.md](../templates/.devdocs/WORKFLOW_TRACKING/maintenance_workflow.md) | Maintenance workflow tracking (cycle) | E1 |
| [templates/.devdocs/.archive/archival_log.md](../templates/.devdocs/.archive/archival_log.md) | Archival action log template | E1 |

### Docs Templates

| File | Purpose | Owner |
|------|---------|-------|
| [templates/docs/README.md](../templates/docs/README.md) | `/docs/` folder guide | C7 |

---

## Code Documentation Locations

### Python Package Structure

| Directory | Purpose | Documentation Type |
|-----------|---------|-------------------|
| `logos/cli/` | Command-line interface | `##Script function and purpose:` comments, docstrings |
| `logos/core/` | Core functionality (24 modules) | `##Script function and purpose:` comments, docstrings |
| `logos/core/devdocs.py` | `.devdocs/` governance logic | E1 implementation |
| `logos/core/temporal_logs.py` | `DEV_STATE.md` management | E1 implementation |
| `logos/core/refusal.py` | Agent boundary enforcement | Boundary redirects |
| `logos/core/workflow_tracking.py` | Workflow templates and tracking | Workflow implementation |
| `logos/daedelus/` | Daedelus domain (24 agents) | Agent definitions, prompts |
| `logos/deus/` | DEUS domain (26 agents) | Agent definitions, prompts |
| `tests/` | Test suite | Test docstrings (D102 enforced) |

---

## Documentation by Topic

### For New Users

1. [README.md](../README.md) — Start here
2. [INSTALL.md](../INSTALL.md) — Installation
3. [CLI_USAGE.md](CLI_USAGE.md) — Using the CLI

### For Contributors

1. [CONTRIBUTING.md](../CONTRIBUTING.md) — How to contribute
2. [DEVELOPMENT.md](../DEVELOPMENT.md) — Development status
3. [DOCUMENTATION_GUIDE.md](DOCUMENTATION_GUIDE.md) — Documentation system

### For Understanding the Architecture

1. [CONSTITUTION.md](../CONSTITUTION.md) — Governance model
2. [AGENT_BOUNDARIES.md](AGENT_BOUNDARIES.md) — Agent specifications
3. [WORKFLOWS.md](WORKFLOWS.md) — Workflow patterns
4. [FACTIONS.md](FACTIONS.md) — Faction system
5. [architecture/DOCUMENTATION_ARCHITECTURE.md](architecture/DOCUMENTATION_ARCHITECTURE.md) — Doc architecture

### For AI Agents

1. [AGENT_BOUNDARIES.md](AGENT_BOUNDARIES.md) — Know your boundaries
2. [AGENT_RECOMMENDATIONS.md](AGENT_RECOMMENDATIONS.md) — When to redirect
3. [WORKFLOWS.md](WORKFLOWS.md) — Coordination workflows
4. [templates/.devdocs/DEV_STATE.md](../templates/.devdocs/DEV_STATE.md) — State template
