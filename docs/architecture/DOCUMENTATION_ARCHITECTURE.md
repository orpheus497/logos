# LOGOS Documentation Architecture

> **Maintained by:** C7 — The Doc Updater (Daedelus) / The Manual Keeper (DEUS)
>
> **Last Updated:** 2026-03-28

---

## Table of Contents

1. [Overview](#overview)
2. [Three-Layer Architecture](#three-layer-architecture)
3. [Layer 1: Agent Context — `.devdocs/`](#layer-1-agent-context--devdocs)
4. [Layer 2: Project Documentation — `/docs/` and Root](#layer-2-project-documentation--docs-and-root)
5. [Layer 3: Code Documentation — Inline](#layer-3-code-documentation--inline)
6. [Data Flow Between Layers](#data-flow-between-layers)
7. [Folder Structure and Ownership](#folder-structure-and-ownership)
8. [Agent Coordination Model](#agent-coordination-model)
9. [Coherence and Drift Detection](#coherence-and-drift-detection)
10. [References](#references)

---

## Overview

The LOGOS documentation system is structured as a **three-layer architecture** that separates
concerns by audience, lifecycle, and ownership. Each layer has a designated constitutional
owner, a distinct purpose, and clear rules for when and how content is modified.

This architecture ensures that AI agents, developers, and end users each have documentation
tailored to their needs — without conflicts, duplication, or drift.

---

## Three-Layer Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     LOGOS Documentation Stack                   │
│                                                                 │
│  Layer 3 ─ Code Docs    │ logos/**/*.py                         │
│  (C7 Owns)              │ Docstrings, comments, type hints      │
│                         │ Lifecycle: changes with code           │
│─────────────────────────┼───────────────────────────────────────│
│  Layer 2 ─ Project Docs │ /docs/, README.md, CONSTITUTION.md    │
│  (C7 Owns)              │ Guides, references, architecture      │
│                         │ Lifecycle: committed to git            │
│─────────────────────────┼───────────────────────────────────────│
│  Layer 1 ─ Agent Context│ .devdocs/                             │
│  (E1 Owns)              │ DEV_STATE.md, agent logs, workflows   │
│                         │ Lifecycle: ephemeral working memory    │
└─────────────────────────────────────────────────────────────────┘
```

### Layer Comparison

| Aspect | Layer 1: Agent Context | Layer 2: Project Docs | Layer 3: Code Docs |
|--------|----------------------|----------------------|-------------------|
| **Location** | `.devdocs/` | `/docs/` + root | `logos/**/*.py` |
| **Owner** | E1 (Orchestrator) | C7 (Doc Updater) | C7 (Doc Updater) |
| **Audience** | AI agents | Developers & users | Developers |
| **Committed to git** | ❌ No | ✅ Yes | ✅ Yes |
| **Lifecycle** | Ephemeral | Permanent | Permanent |
| **Update frequency** | Per task / daily | Per feature / release | Per code change |
| **Format** | Markdown templates | Markdown documents | Python docstrings |
| **Timestamps** | ISO 8601 required | ISO 8601 required | Not required |

---

## Layer 1: Agent Context — `.devdocs/`

### Purpose

Ephemeral working memory for AI agents. Provides real-time project state that agents read
before taking action (Folder Priority Read Rule — [CONSTITUTION.md](../CONSTITUTION.md), Article VII).

### Architecture

```
.devdocs/
├── DEV_STATE.md                 ← Single source of truth (E1 manages)
├── AGENT_LOGS/
│   ├── group_a/                 ← Builders (A1–A5)
│   ├── group_b/                 ← Guardians (B6–B10)
│   ├── group_c/                 ← Maintainers (C1, C6–C11)
│   ├── group_d/                 ← Workers (D2–D5)
│   └── group_e/                 ← Operators (E1–E5)
├── WORKFLOW_TRACKING/
│   ├── diamond_workflow.md      ← Creation: A1 → A2/A3/A4 → A5
│   ├── funnel_workflow.md       ← Review: B6/B7/B8/B9 → B10
│   └── maintenance_workflow.md  ← Cycle: C1 → C6 → C7 → C8 → ...
└── .archive/                    ← E1 exclusive access
    └── archival_log.md          ← Record of all archival actions
```

### Key Properties

- **Constitutional authority:** E1 holds exclusive governance ([CONSTITUTION.md](../CONSTITUTION.md), Article VII)
- **Temporal management:** Daily → Weekly → Monthly archival cycles
- **Bloat prevention:** E1 prunes stale entries and enforces size limits
- **Not version-controlled:** `.devdocs/` is excluded from git

---

## Layer 2: Project Documentation — `/docs/` and Root

### Purpose

Permanent, version-controlled documentation for developers and users. Describes the project,
its architecture, usage, governance, and contribution guidelines.

### Architecture

```
/                                    ← Root documentation
├── README.md                        ← Project overview
├── CONSTITUTION.md                  ← Governance framework
├── PLAN.md                          ← Development roadmap
├── PROJECT_STATUS.md                ← Phase status analysis
├── CHANGELOG.md                     ← Version history
├── DEVELOPMENT.md                   ← Development quick links
├── INSTALL.md                       ← Installation guide
├── CONTRIBUTING.md                  ← Contribution guidelines
│
docs/                                ← Detailed documentation
├── CLI_USAGE.md                     ← CLI reference
├── AGENT_BOUNDARIES.md              ← Agent boundary specs (50 agents)
├── AGENT_RECOMMENDATIONS.md         ← Agent selection matrix
├── WORKFLOWS.md                     ← Workflow summaries
├── FACTIONS.md                      ← Faction system
├── DOCUMENTATION_GUIDE.md           ← Documentation system guide
├── DOCUMENTATION_INDEX.md           ← Cross-reference index
├── OS_ADAPTATIONS.md                ← OS adaptation architecture
├── DEUS_LINUX_REFERENCE.md          ← Linux reference
├── DEUS_FREEBSD_REFERENCE.md        ← FreeBSD reference
├── SHELL_COMPLETION.md              ← Shell completion guide
├── architecture/                    ← Architecture documents
│   └── DOCUMENTATION_ARCHITECTURE.md  ← This document
└── examples/                        ← Workflow examples
    ├── ORCHESTRATOR_WORKFLOW.md      ← E1 workflow example
    └── DOC_UPDATER_WORKFLOW.md       ← C7 workflow example
```

### Key Properties

- **Version-controlled:** All files committed to git
- **Maintained by C7:** The Doc Updater syncs after code changes
- **Cross-referenced:** Documents link to each other via relative paths
- **Follows markdown standards:** Consistent heading hierarchy, tables, code blocks

---

## Layer 3: Code Documentation — Inline

### Purpose

Documentation embedded directly in Python source code. Provides immediate context for
developers reading or modifying the codebase.

### Architecture

```
logos/
├── cli/                    ← CLI layer documentation
│   ├── main.py             ← ##Script function and purpose: CLI entry point
│   ├── agent_select.py     ← ##Script function and purpose: Agent selection UI
│   └── ...
├── core/                   ← Core module documentation
│   ├── devdocs.py          ← ##Script function and purpose: .devdocs/ governance
│   ├── temporal_logs.py    ← ##Script function and purpose: DEV_STATE.md management
│   ├── refusal.py          ← ##Script function and purpose: Boundary enforcement
│   └── ...
├── daedelus/               ← Daedelus domain documentation
│   ├── agents.py           ← ##Script function and purpose: 24 agent definitions
│   └── prompts/            ← Agent system prompts
└── deus/                   ← DEUS domain documentation
    ├── agents.py           ← ##Script function and purpose: 26 agent definitions
    └── prompts/            ← Agent system prompts
```

### Documentation Tags

| Tag | Usage |
|-----|-------|
| `##Script function and purpose:` | Module-level description |
| `##Class purpose:` | Class-level description |
| `##Function purpose:` | Function-level description |
| `##Action purpose:` | Inline code block description |

---

## Data Flow Between Layers

```
    ┌──────────────────┐
    │  Code Changes     │
    │  (by A1–A5, etc.) │
    └────────┬─────────┘
             │
             ▼
    ┌──────────────────┐        ┌──────────────────┐
    │  Layer 3: Code   │───────▶│  Layer 2: Docs   │
    │  (C7 updates     │        │  (C7 syncs after │
    │   docstrings)    │        │   feature done)  │
    └──────────────────┘        └────────┬─────────┘
                                         │
                                         ▼
                                ┌──────────────────┐
                                │  Layer 1: Agent  │
                                │  (E1 records in  │
                                │   DEV_STATE.md)  │
                                └──────────────────┘

    ┌──────────────────┐
    │  E1 Coherence    │
    │  Audit           │
    └────────┬─────────┘
             │ Detects drift
             ▼
    ┌──────────────────┐        ┌──────────────────┐
    │  Layer 1: Agent  │───────▶│  Layer 2: Docs   │
    │  (E1 flags drift │        │  (C7 updates     │
    │   in DEV_STATE)  │        │   flagged docs)  │
    └──────────────────┘        └──────────────────┘
```

### Flow Summary

1. **Code → Code Docs:** When code changes, C7 updates inline documentation (Layer 3)
2. **Code → Project Docs:** After features complete, C7 syncs project documentation (Layer 2)
3. **Project Docs → Agent Context:** E1 records documentation state in `DEV_STATE.md` (Layer 1)
4. **Agent Context → Project Docs:** When E1 detects drift, C7 is recommended for updates
5. **Release Cycle:** B10 (Gatekeeper) dispatches C7 to sync release documentation across all layers

---

## Agent Coordination Model

### Primary Actors

| Agent | Layer | Authority | Constitutional Basis |
|-------|-------|-----------|---------------------|
| **E1** | 1 | Exclusive `.devdocs/` governance | Article VII |
| **C7** | 2, 3 | Project docs and code docs maintenance | Agent Boundaries |
| **A5** | 2 | New documentation creation (initial only) | Builder role |
| **B10** | — | Triggers documentation sync on release | Gatekeeper role |

### Coordination Protocol

1. **E1 initializes** `.devdocs/` using templates from `templates/.devdocs/`
2. **Agents work** and record progress in their respective `AGENT_LOGS/` entries
3. **E1 monitors** for coherence, bloat, and documentation drift
4. **E1 recommends** C7 when project documentation needs updating
5. **C7 updates** `/docs/`, root files, and inline code docs
6. **E1 records** the completed update in `DEV_STATE.md`

---

## Coherence and Drift Detection

### What E1 Checks

| Check | Description | Resolution |
|-------|-------------|------------|
| **Stale entries** | Agent logs older than archival threshold | Archive to `.devdocs/.archive/` |
| **Bloat** | `DEV_STATE.md` exceeds recommended size | Prune completed items, archive old entries |
| **Documentation drift** | Project docs don't match codebase state | Recommend C7 for update |
| **Missing timestamps** | Entries without ISO 8601 dates | Flag as constitutional violation |
| **Orphaned references** | Cross-references to deleted content | Recommend C7 for cleanup |

### Drift Detection Triggers

- New feature merged without documentation update
- Agent boundary changes not reflected in `AGENT_BOUNDARIES.md`
- Configuration changes not reflected in `CLI_USAGE.md` or `INSTALL.md`
- Workflow changes not reflected in `WORKFLOWS.md`

---

## References

- [DOCUMENTATION_GUIDE.md](../DOCUMENTATION_GUIDE.md) — Comprehensive documentation system guide
- [DOCUMENTATION_INDEX.md](../DOCUMENTATION_INDEX.md) — Cross-reference index
- [CONSTITUTION.md](../../CONSTITUTION.md) — Governance framework (Article VII)
- [AGENT_BOUNDARIES.md](../AGENT_BOUNDARIES.md) — Agent boundary specifications
- [WORKFLOWS.md](../WORKFLOWS.md) — Workflow summaries
