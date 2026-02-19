# AGENTS.md — Copilot Coding Agent Instructions

**Project:** LOGOS — Unified AI Agent Federation
**Branch:** `task2/dadelus1` (based on `task1/infrastructure`)

---

## Project Overview

LOGOS is a CLI-based AI agent federation system with 50 specialized agents across two domains:
- **Daedelus** (24 agents): Software development workflow
- **DEUS** (26 agents): System administration

The codebase uses Python 3.10+, setuptools for packaging, pytest for testing, and ruff for linting.

---

## Repository Structure

```text
logos/
├── logos/              # Main package
│   ├── core/           # Core modules (identity, persistence, prompts, refusal, etc.)
│   ├── cli/            # CLI interface (mode select, first run, layouts)
│   ├── daedelus/       # Daedelus domain agents and prompts
│   └── deus/           # DEUS domain agents and prompts
├── tests/              # Test suite
│   └── test_core/      # Core module tests
├── docs/               # Documentation
│   ├── AGENT_BOUNDARIES.md     # Agent scope reference (all 50 agents)
│   ├── AGENT_RECOMMENDATIONS.md # Agent workflow cross-reference
│   ├── FACTIONS.md     # Faction system docs
│   └── WORKFLOWS.md    # Workflow pattern docs
├── CONSTITUTION.md     # Federation constitution v2.0
├── CHANGELOG.md        # Keep a Changelog format
├── README.md           # Project documentation
├── pyproject.toml      # Project configuration
├── install.sh          # Installation script
└── uninstall.sh        # Uninstallation script
```

---

## Code Conventions

- **Documentation comments** use `##` prefix schema: `##Script function and purpose:`, `##Class purpose:`, `##Function purpose:`, `##Action purpose:`, `##Condition purpose:`
- **Docstrings** on all public functions, following the `##Function purpose:` pattern
- **Type hints** required on all function signatures
- **Line length** 120 chars max (ruff config)
- **Imports** sorted by ruff (isort)

---

## Testing

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test module
python -m pytest tests/test_core/test_refusal.py -v

# Lint
python -m ruff check logos/
```

---

## Current Development Status

**Branch:** `task2/dadelus1` — PR #2: Daedelus Agent Boundaries (Group A-B)
**Base version:** 0.1.0 (on `develop`) → 0.2.0.dev0 (on this branch)

### PR #2 Progress: Daedelus Group A-B Scope Boundaries

| Commit | Agent | File | Status |
|--------|-------|------|--------|
| 1/14 | A1 - The Architect | `builders.py` | ✅ Committed |
| 2/14 | A2 - The Logic Engineer | `builders.py` | ⬜ Pending |
| 3/14 | A3 - The Interface Designer | `builders.py` | ⬜ Pending |
| 4/14 | A4 - The Test Engineer | `builders.py` | ⬜ Pending |
| 5/14 | A5 - The Scribe | `builders.py` | ⬜ Pending |
| 6/14 | B6 - The Sentinel | `guardians.py` | ⬜ Pending |
| 7/14 | B7 - The Marshal | `guardians.py` | ⬜ Pending |
| 8/14 | B8 - The Profiler | `guardians.py` | ⬜ Pending |
| 9/14 | B9 - The Critic | `guardians.py` | ⬜ Pending |
| 10/14 | B10 - The Gatekeeper | `guardians.py` | ⬜ Pending |
| 11/14 | Docs: AGENT_BOUNDARIES.md | `docs/` | ⬜ Pending |
| 12/14 | Docs: AGENT_RECOMMENDATIONS.md | `docs/` | ⬜ Pending |
| 13/14 | Tests: boundary validation | `tests/` | ⬜ Pending |
| 14/14 | CHANGELOG.md update | root | ⬜ Pending |

### Each SCOPE BOUNDARIES Section Must Include
- ✅ IN SCOPE: minimum 5 categorized items with sub-items
- ⛔ FORBIDDEN ACTIONS: minimum 10 with agent redirects and "Why" explanations
- 🤝 REQUIRES COLLABORATION: minimum 3 scenarios
- 🚫 REFUSAL TEMPLATE: with concrete example

### Resumption Instructions
Next commit: `feat(daedelus): add scope boundaries to A2 (Logic Engineer)` — add SCOPE BOUNDARIES to `LOGIC_ENGINEER_ACTIVATION` in `logos/daedelus/prompts/agents/builders.py`.

Reference `PLAN.md` lines 1144-1194 for agent-specific scope definitions. Follow the pattern established in commit 1 (A1 Architect).

---

## Completed Phases

### Phase 1: Agent Boundary Infrastructure (task1/infrastructure) ✅
- `docs/AGENT_BOUNDARIES.md` — all 50 agents documented
- `docs/AGENT_RECOMMENDATIONS.md` — all 50 agents with workflow recommendations
- `logos/core/refusal.py` — refusal response generation utility
- `tests/test_core/test_refusal.py` — 16 tests passing
- Version bumped to 0.2.0.dev0

---

## Remaining v0.2.0 Phases

For full roadmap details, see `PLAN.md`. Remaining work after PR #2:
- PR #3-5: Remaining agent boundaries (Daedelus C-E, DEUS A-B, DEUS C-E)
- Phase 2: .devdocs Governance — unified task management with temporal log system
- Phase 3: Workflow Coordination — agents recommend next steps automatically
- Phase 4: OS Adaptations — Linux and FreeBSD-specific DEUS prompts
- Phase 5: UI Enhancements — ASCII logo and agent assignment display
- Phase 6: Documentation Consolidation
- Phase 7: Integration and Release
