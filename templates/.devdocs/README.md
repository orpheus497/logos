# `.devdocs/` — Agent Working Memory

> **Managed by:** E1 — The Orchestrator
>
> **Constitutional Authority:** [CONSTITUTION.md](../../CONSTITUTION.md), Article VII

---

## Purpose

The `.devdocs/` folder is the **AI agent working memory** for LOGOS projects. It provides
a real-time snapshot of project state, agent activity, and workflow progress that agents
read before taking any action.

This is **not** user documentation. It is an ephemeral context layer managed exclusively
by E1 (The Orchestrator).

---

## Folder Structure

```
.devdocs/
├── DEV_STATE.md                    # Unified project state — SINGLE SOURCE OF TRUTH
├── AGENT_LOGS/                     # Per-agent working logs
│   └── group_a/                    # Builders (A1–A5)
│       └── AGENT_LOG_TEMPLATE.md   # Template for agent log entries
├── WORKFLOW_TRACKING/              # Active workflow state
│   ├── diamond_workflow.md         # Creation workflow (A1 → Parallel → A5)
│   ├── funnel_workflow.md          # Review workflow (B6–B9 → B10)
│   └── maintenance_workflow.md     # Maintenance cycle (C1 → C6 → C7 → ...)
└── .archive/                       # Archived entries (E1 EXCLUSIVE ACCESS)
    └── archival_log.md             # Record of all archival actions
```

---

## Who Manages This Folder

**E1 — The Orchestrator** holds exclusive constitutional authority over `.devdocs/`.

| Action | Who |
|--------|-----|
| Create/modify folder structure | E1 only |
| Update `DEV_STATE.md` | E1 only |
| Access `.archive/` | E1 only |
| Read `DEV_STATE.md` | All agents (required before any action) |
| Update shared files (`BRIEFING.md`, `AGENTS.md`) | C7 (Doc Updater) |
| Write to own agent log | Each agent in their designated folder |

---

## What NOT to Do

⛔ **Do NOT commit `.devdocs/` to git.** It is working memory, not permanent record.

⛔ **Do NOT modify the folder structure** unless you are E1.

⛔ **Do NOT access `.archive/`** unless you are E1.

⛔ **Do NOT skip reading `DEV_STATE.md`** before starting work — this is the
Folder Priority Read Rule ([CONSTITUTION.md](../../CONSTITUTION.md), Article VII, Section 2).

⛔ **Do NOT create entries without ISO 8601 timestamps.**

---

## Using These Templates

To initialize `.devdocs/` for a new project or branch, copy this entire directory:

```bash
cp -r templates/.devdocs/ .devdocs/
```

Then have E1 populate `DEV_STATE.md` with the current project state.

See [docs/examples/ORCHESTRATOR_WORKFLOW.md](../../docs/examples/ORCHESTRATOR_WORKFLOW.md)
for a complete initialization walkthrough.

---

## References

- [DOCUMENTATION_GUIDE.md](../../docs/DOCUMENTATION_GUIDE.md) — Documentation system guide
- [DOCUMENTATION_ARCHITECTURE.md](../../docs/architecture/DOCUMENTATION_ARCHITECTURE.md) — Architecture overview
- [CONSTITUTION.md](../../CONSTITUTION.md) — Article VII: Domain of the Orchestrator
- [AGENT_BOUNDARIES.md](../../docs/AGENT_BOUNDARIES.md) — E1 boundary specification
