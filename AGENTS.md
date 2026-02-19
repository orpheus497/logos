# AGENTS.md — Copilot Coding Agent Instructions

**Project:** LOGOS — Unified AI Agent Federation
**Branch:** `task1/infrastructure` (based on `develop`)

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

**Branch:** `task1/infrastructure` — Phase 1: Agent Boundary Enforcement
**Base version:** 0.1.0 (on `develop`) → 0.2.0.dev0 (on this branch)

### Completed Work (unstaged, requires commit)

| File | Status | Verification |
|------|--------|-------------|
| `docs/AGENT_BOUNDARIES.md` | Created — 1329 lines, all 50 agents documented | Complete |
| `docs/AGENT_RECOMMENDATIONS.md` | Created — 728 lines, all 50 agents with next-steps | Complete |
| `logos/core/refusal.py` | Created — 168 lines, passes ruff, imports clean | Complete |
| `tests/test_core/test_refusal.py` | Created — 207 lines, 16/16 tests passing | Complete |
| `CHANGELOG.md` | Modified — v0.2.0.dev0 entry added | Complete |
| `README.md` | Modified — development notice and version updated | Complete |
| `pyproject.toml` | Modified — version bumped to 0.2.0.dev0 | Complete |

### Issues Resolved

All issues identified during review have been addressed. Changes are ready for commit.

---

## Git Actions Required

The following git operations need to be performed by the repository owner. All changes are currently unstaged on the `task1/infrastructure` branch.

### Staging

```bash
# Stage new files
git add docs/AGENT_BOUNDARIES.md
git add docs/AGENT_RECOMMENDATIONS.md
git add logos/core/refusal.py
git add tests/test_core/test_refusal.py

# Stage modified files
git add CHANGELOG.md
git add README.md
git add pyproject.toml
git add AGENTS.md
```

### Recommended Commits

```bash
# Commit 1: Documentation infrastructure
git commit -m "feat: add agent boundaries and recommendations documentation

- Create docs/AGENT_BOUNDARIES.md with scope definitions for all 50 agents
- Create docs/AGENT_RECOMMENDATIONS.md with workflow cross-reference for all 50 agents
- Each agent entry includes: IN SCOPE, FORBIDDEN ACTIONS, COLLABORATION, WORKFLOW

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"

# Commit 2: Refusal module
git commit -m "feat: add refusal response generation utility

- Create logos/core/refusal.py with RefusalResponse dataclass
- Implement generate_refusal() for formatted out-of-scope messages
- Implement quick_refusal() convenience function
- Implement validate_refusal_response() field validation

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"

# Commit 3: Tests
git commit -m "test: add refusal module tests

- Create tests/test_core/test_refusal.py with 16 test cases
- Cover dataclass creation, output formatting, convenience function, validation

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"

# Commit 4: Version and metadata (after resolving CHANGELOG/README issues)
git commit -m "chore: bump version to 0.2.0.dev0 and update project metadata

- Update pyproject.toml version to 0.2.0.dev0
- Add v0.2.0.dev0 entry to CHANGELOG.md
- Update README.md with development status
- Replace raw plan in AGENTS.md with coding agent instructions

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>"
```

---

## Remaining v0.2.0 Phases

For full roadmap details, create a `docs/ROADMAP.md`. Remaining work after Phase 1:
- Phase 2: .devdocs Governance — unified task management with temporal log system
- Phase 3: Workflow Coordination — agents recommend next steps automatically
- Phase 4: OS Adaptations — Linux and FreeBSD-specific DEUS prompts
- Phase 5: UI Enhancements — ASCII logo and agent assignment display
- Phase 6: Documentation Consolidation
- Phase 7: Integration and Release
