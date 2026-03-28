# LOGOS Documentation System Guide

> **Maintained by:** C7 — The Doc Updater (Daedelus) / The Manual Keeper (DEUS)
>
> **Last Updated:** 2026-03-28

---

## Table of Contents

1. [Overview](#overview)
2. [The Three Documentation Domains](#the-three-documentation-domains)
3. [Responsibilities Matrix](#responsibilities-matrix)
4. [Domain 1: Agent Working Memory — `.devdocs/`](#domain-1-agent-working-memory--devdocs)
5. [Domain 2: Project Documentation — `/docs/` and Root](#domain-2-project-documentation--docs-and-root)
6. [Domain 3: Inline Code Documentation](#domain-3-inline-code-documentation)
7. [When to Update Each Domain](#when-to-update-each-domain)
8. [Documentation Standards](#documentation-standards)
9. [Cross-Domain Coordination](#cross-domain-coordination)
10. [Common Mistakes](#common-mistakes)
11. [References](#references)

---

## Overview

LOGOS uses a **three-domain documentation architecture** governed by constitutional authority.
Documentation is not ancillary — it is a first-class deliverable. Failures to maintain documentation
are treated as constitutional violations (see [CONSTITUTION.md](../CONSTITUTION.md), Article II).

Every documentation entry **MUST** include an ISO 8601 date/time stamp per constitutional mandate.

---

## The Three Documentation Domains

| Domain | Location | Owner | Purpose | Audience |
|--------|----------|-------|---------|----------|
| **Agent Working Memory** | `.devdocs/` | E1 — The Orchestrator | AI agent context, project state, workflow tracking | Agents |
| **Project Documentation** | `/docs/` + root `.md` files | C7 — The Doc Updater / Manual Keeper | User guides, architecture, reference docs | Developers & users |
| **Inline Code Docs** | `logos/**/*.py` | C7 — The Doc Updater | Docstrings, code comments, type annotations | Developers |

### How the Domains Relate

```
┌─────────────────────────────────────────────────────────┐
│                    LOGOS Documentation                   │
│                                                         │
│  ┌──────────────┐  ┌───────────────┐  ┌──────────────┐  │
│  │  .devdocs/   │  │  /docs/ +     │  │  Inline Code │  │
│  │  (E1 Owns)   │──│  Root Docs    │──│  Docs        │  │
│  │              │  │  (C7 Owns)    │  │  (C7 Owns)   │  │
│  │  Agent state │  │  User-facing  │  │  Docstrings  │  │
│  │  Workflows   │  │  Guides       │  │  Comments    │  │
│  │  Logs        │  │  References   │  │  Type hints  │  │
│  └──────────────┘  └───────────────┘  └──────────────┘  │
│                                                         │
│       E1 detects drift ──→ Recommends C7 update         │
│       C7 updates docs  ──→ E1 records in DEV_STATE.md   │
└─────────────────────────────────────────────────────────┘
```

---

## Responsibilities Matrix

### Agent Documentation Ownership

| Agent | Domain | Daedelus Role | DEUS Role | Can Modify |
|-------|--------|---------------|-----------|------------|
| **E1** | Operators | The Orchestrator | The System Orchestrator | `.devdocs/` structure, `DEV_STATE.md`, `.archive/`, workflow tracking |
| **C7** | Maintainers | The Doc Updater | The Manual Keeper | `/docs/`, root `.md` files, `README.md`, code docstrings, shared `.devdocs` files (`BRIEFING.md`, `AGENTS.md`) |
| **A5** | Builders | The Scribe | The Config Scribe | New documentation (initial creation only) |
| **B10** | Guardians | The Gatekeeper | The Release Guardian | Dispatches C7 after release approval |

### What Each Agent **Cannot** Do

| Agent | Forbidden Documentation Actions | Redirect To |
|-------|--------------------------------|-------------|
| E1 | Writing project documentation content | → C7 |
| C7 | Modifying `.devdocs/` folder structure | → E1 |
| C1 (Bug Hunter) | Any documentation updates | → C7 |
| A1–A4 | Updating existing documentation | → C7 |
| All non-E1 agents | Accessing `.devdocs/.archive/` | → E1 |

See [AGENT_BOUNDARIES.md](AGENT_BOUNDARIES.md) for complete boundary specifications.

---

## Domain 1: Agent Working Memory — `.devdocs/`

### Purpose

The `.devdocs/` folder is the **AI agent working memory** — a hidden directory that serves as
the single source of truth for project state during active development.

### Owner: E1 — The Orchestrator

E1 holds **exclusive constitutional authority** over `.devdocs/` governance
(see [CONSTITUTION.md](../CONSTITUTION.md), Article VII).

### Structure

```
.devdocs/
├── DEV_STATE.md                    # Unified project state (SINGLE SOURCE OF TRUTH)
├── AGENT_LOGS/
│   └── group_a/
│       └── AGENT_LOG_TEMPLATE.md   # Per-agent working log
├── WORKFLOW_TRACKING/
│   ├── diamond_workflow.md         # Creation workflow (A1 → Parallel → A5)
│   ├── funnel_workflow.md          # Review workflow (B6–B9 → B10)
│   └── maintenance_workflow.md     # Maintenance cycle (C1 → C6 → C7 → ...)
└── .archive/                       # Archived entries (E1 EXCLUSIVE ACCESS)
    └── archival_log.md             # Record of all archival actions
```

### Key Rules

1. **Folder Priority Read Rule** — All non-Orchestrator agents MUST check for `.devdocs/` and read `DEV_STATE.md` before proceeding
2. **Do NOT commit `.devdocs/` to git** — It is working memory, not permanent record
3. **ISO 8601 timestamps required** on all entries
4. **Temporal log management** — E1 enforces Daily → Weekly → Monthly archival cycles
5. **Coherence auditing** — E1 runs continuous checks for bloat and drift

### Templates

Templates for `.devdocs/` are maintained in [`templates/.devdocs/`](../templates/.devdocs/).
See the [template README](../templates/.devdocs/README.md) for details.

---

## Domain 2: Project Documentation — `/docs/` and Root

### Purpose

User-facing and developer-facing documentation that describes the project, its architecture,
usage, and contribution guidelines. This documentation **is** committed to git.

### Owner: C7 — The Doc Updater (Daedelus) / The Manual Keeper (DEUS)

C7 is responsible for keeping all project documentation synchronized with the current state
of the codebase.

### Root Documentation Files

| File | Purpose |
|------|---------|
| `README.md` | Primary project overview, installation, usage |
| `CONSTITUTION.md` | Governance framework and constitutional authority |
| `PLAN.md` | Development roadmap (v0.1.0 → v0.2.0) |
| `PROJECT_STATUS.md` | Phase-by-phase status analysis |
| `CHANGELOG.md` | Version history and release notes |
| `DEVELOPMENT.md` | Development status and quick links |
| `INSTALL.md` | Installation guide |
| `CONTRIBUTING.md` | Contribution guidelines |
| `LICENSE` | GNU AGPL v3.0 |

### `/docs/` Folder Contents

| File | Purpose |
|------|---------|
| `CLI_USAGE.md` | CLI reference with examples and agent tables |
| `AGENT_BOUNDARIES.md` | Complete agent boundary specifications (50 agents) |
| `AGENT_RECOMMENDATIONS.md` | Cross-reference workflow matrix for agent selection |
| `WORKFLOWS.md` | Workflow summaries (Diamond, Funnel, Maintenance) |
| `FACTIONS.md` | Faction philosophy and autonomy levels |
| `OS_ADAPTATIONS.md` | OS adaptation architecture |
| `DEUS_LINUX_REFERENCE.md` | Linux quick reference for DEUS agents |
| `DEUS_FREEBSD_REFERENCE.md` | FreeBSD quick reference for DEUS agents |
| `SHELL_COMPLETION.md` | Shell completion guide |
| `DOCUMENTATION_GUIDE.md` | This document |
| `DOCUMENTATION_INDEX.md` | Cross-reference index of all documentation |

### Key Rules

1. Documentation updates follow code changes — never the reverse
2. C7 syncs documentation after any feature completion, bug fix, or configuration change
3. Cross-references between documents must use relative paths
4. All documentation must be factual and match the current codebase

---

## Domain 3: Inline Code Documentation

### Purpose

Code-level documentation embedded in Python source files: docstrings, comments, and type
annotations within the `logos/` package.

### Owner: C7 — The Doc Updater

### Code Comment Conventions

LOGOS uses structured comment tags for code documentation:

```python
##Script function and purpose: Brief description of the module
##Class purpose: What this class does
##Function purpose: What this function does
##Action purpose: What this block of code does
```

### Docstring Requirements

- All public modules, classes, and functions should have docstrings
- All test methods **MUST** have docstrings (enforced by ruff D102)
- Follow Python conventions compatible with the ruff linter configuration

### Code Style Reference

See `pyproject.toml` for the complete ruff configuration:
- **Line length:** 120 characters
- **Target Python:** 3.10+
- **Lint rules:** E, F, W, I, N, D, UP

---

## When to Update Each Domain

### `.devdocs/` Updates (by E1)

| Trigger | Action |
|---------|--------|
| Project initialization | Create `.devdocs/` structure from templates |
| Agent completes a task | Update `DEV_STATE.md` with results |
| Workflow state change | Update relevant workflow tracking file |
| Weekly cycle | Archive old entries, update summaries |
| Coherence audit | Check for drift, bloat, and stale entries |
| Documentation drift detected | Recommend C7 for project doc updates |

### `/docs/` and Root Updates (by C7)

| Trigger | Action |
|---------|--------|
| Feature completed | Update relevant docs, README sections |
| Bug fixed with behavior change | Update affected documentation |
| Configuration change | Update INSTALL.md, CLI_USAGE.md as needed |
| Release approved (by B10) | Sync CHANGELOG.md, version references |
| E1 detects documentation drift | Update flagged documents |
| New agent or workflow added | Update AGENT_BOUNDARIES.md, WORKFLOWS.md |

### Inline Code Updates (by C7)

| Trigger | Action |
|---------|--------|
| Function signature change | Update docstring |
| New module or class | Add structured comment tags |
| API behavior change | Update docstrings and code comments |
| Code refactoring | Sync inline docs with new structure |

---

## Documentation Standards

### Markdown Formatting

- **Headings:** H1 (`#`) for page title, H2 (`##`) for sections, H3 (`###`) for subsections
- **Tables:** Use markdown tables for structured data (agents, status, reference)
- **Code blocks:** Use fenced code blocks with language identifiers (```python, ```bash, ```yaml)
- **Cross-references:** Relative links (`[text](../file.md)`)
- **Status indicators:** ✅ Complete, ❌ Not Started, ⚠️ In Progress
- **Emoji:** Use sparingly for visual markers (📝, 🔧, 📊)

### ISO 8601 Timestamps

All documentation entries must include timestamps in ISO 8601 format:

```
2026-03-28T14:30:00Z
```

### File Naming

- Use `UPPER_SNAKE_CASE.md` for documentation files
- Use lowercase for directories (`docs/`, `templates/`, `examples/`)

---

## Cross-Domain Coordination

### E1 → C7 Handoff

When E1 detects that project documentation is out of sync with the codebase:

1. E1 records the drift in `DEV_STATE.md` under **ACTIVE BLOCKERS**
2. E1 recommends C7 for the update via agent recommendation
3. C7 performs the documentation update
4. E1 removes the blocker and updates `DEV_STATE.md`

### C7 → E1 Notification

When C7 completes a documentation update that affects agent workflows:

1. C7 updates the relevant `/docs/` or root file
2. C7 notifies E1 that shared `.devdocs` files may need updating
3. E1 updates `DEV_STATE.md` to reflect the change

### Cross-Domain (Daedelus ↔ DEUS)

- Daedelus C7 (Doc Updater) handles software documentation
- DEUS C7 (Manual Keeper) handles system administration documentation
- Both coordinate through shared `/docs/` files

---

## Common Mistakes

| ❌ Mistake | ✅ Correct Approach |
|-----------|-------------------|
| Committing `.devdocs/` to git | `.devdocs/` is working memory — keep it local |
| Non-E1 agent modifying `.devdocs/` structure | Only E1 manages `.devdocs/` structure |
| Updating docs before code is complete | Documentation follows code, never the reverse |
| Skipping timestamps on documentation entries | ISO 8601 timestamps are constitutionally required |
| C1 (Bug Hunter) updating documentation | C1 redirects documentation tasks to C7 |
| Writing new docs instead of updating existing | A5 creates new docs; C7 updates existing ones |

---

## References

- [CONSTITUTION.md](../CONSTITUTION.md) — Governance framework (Article VII: Domain of the Orchestrator)
- [AGENT_BOUNDARIES.md](AGENT_BOUNDARIES.md) — Complete agent boundary specifications
- [AGENT_RECOMMENDATIONS.md](AGENT_RECOMMENDATIONS.md) — Agent selection workflow matrix
- [WORKFLOWS.md](WORKFLOWS.md) — Workflow summaries (Diamond, Funnel, Maintenance)
- [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md) — Cross-reference index of all documentation
- [DOCUMENTATION_ARCHITECTURE.md](architecture/DOCUMENTATION_ARCHITECTURE.md) — Architecture overview
- [templates/.devdocs/](../templates/.devdocs/) — `.devdocs/` templates
