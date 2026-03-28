# Example Workflow: C7 Doc Updater Maintaining Documentation

> This document walks through a realistic workflow showing how **C7 — The Doc Updater**
> (Daedelus) / **The Manual Keeper** (DEUS) maintains project and code documentation.

---

## Table of Contents

1. [Scenario](#scenario)
2. [Step 1: Updating Docs After a Feature Is Complete](#step-1-updating-docs-after-a-feature-is-complete)
3. [Step 2: Syncing README.md with Code Changes](#step-2-syncing-readmemd-with-code-changes)
4. [Step 3: Updating Inline Code Documentation](#step-3-updating-inline-code-documentation)
5. [Step 4: Coordinating with E1 Orchestrator](#step-4-coordinating-with-e1-orchestrator)
6. [Step 5: Post-Release Documentation Sync](#step-5-post-release-documentation-sync)
7. [Key Takeaways](#key-takeaways)
8. [References](#references)

---

## Scenario

A new CLI flag `--doc-check` has been implemented by A2 (The Coder) and tested by A4
(The Tester). E1 (The Orchestrator) has detected documentation drift and assigned C7 to
update all affected documentation. C7 must update project docs, the README, and inline
code documentation.

---

## Step 1: Updating Docs After a Feature Is Complete

C7 receives an assignment from E1 via `DEV_STATE.md`:

```markdown
## OUTSTANDING AGENT ASSIGNMENTS
| Agent | Task | Priority |
|-------|------|----------|
| C7 | Update CLI_USAGE.md with --doc-check flag documentation | High |
```

### Actions

1. **Review the code change** to understand the new feature:
   - Read `logos/cli/args.py` for the new flag definition
   - Read `logos/cli/main.py` for how the flag is used
   - Check test files to understand expected behavior

2. **Update `docs/CLI_USAGE.md`** — Add the new flag to the CLI reference:

````markdown
### Documentation Check

Verify that documentation is in sync with the current codebase:

```bash
logos --doc-check
```

This flag runs a quick coherence check and reports any documentation
that may be out of date.
````

3. **Update the CLI flags table** in the same document:

```markdown
| Flag | Description |
|------|-------------|
| `-v` | Verbose output |
| `-q` | Quiet mode |
| `--version` | Show version |
| `--help` | Show help |
| `--doc-check` | Check documentation freshness |
```

4. **Verify cross-references** — Ensure no other docs reference CLI flags without
   including the new one.

---

## Step 2: Syncing README.md with Code Changes

The `README.md` contains a CLI usage section that must stay current.

### Actions

1. **Locate the CLI section** in `README.md`

2. **Add a brief mention** of the new feature:

```markdown
### CLI Flags

LOGOS supports several command-line flags for controlling behavior:

| Flag | Description |
|------|-------------|
| `--doc-check` | Verify documentation freshness |
| `--version` | Display current version |
| `--help` | Show usage information |

See [CLI_USAGE.md](docs/CLI_USAGE.md) for the complete reference.
```

3. **Check version references** — If the feature is tied to a version bump,
   update any version mentions.

4. **Verify all links** in README.md still resolve correctly.

### What C7 Does NOT Do

- ❌ Add new sections to README.md (that's A5 — The Scribe)
- ❌ Modify code to match documentation (documentation follows code)
- ❌ Change the `.devdocs/` folder structure (that's E1 — The Orchestrator)

---

## Step 3: Updating Inline Code Documentation

The new `--doc-check` flag needs proper inline documentation in the source code.

### Actions

1. **Update the module docstring** in `logos/cli/args.py`:

```python
##Function purpose: Parse --doc-check flag for documentation freshness verification
def add_doc_check_arg(parser):
    """Add the --doc-check argument to the CLI parser.

    When enabled, LOGOS runs a documentation coherence check
    before launching the agent interface.
    """
    parser.add_argument(
        "--doc-check",
        action="store_true",
        help="Check documentation freshness",
    )
```

2. **Verify all related functions** have docstrings:
   - Check that handler functions have `##Function purpose:` comments
   - Check that test methods have docstrings (D102 requirement)

3. **Update type annotations** if the function signature has changed.

### Code Documentation Standards

| Convention | Example |
|------------|---------|
| Module-level | `##Script function and purpose: CLI argument parsing` |
| Class-level | `##Class purpose: Manages argument parser state` |
| Function-level | `##Function purpose: Parse --doc-check flag` |
| Action-level | `##Action purpose: Validate flag combination` |

---

## Step 4: Coordinating with E1 Orchestrator

After completing documentation updates, C7 coordinates with E1 to update the
project state.

### Actions

1. **Notify E1** that documentation updates are complete by updating shared
   `.devdocs` files (C7 can update `BRIEFING.md` and `AGENTS.md`):

```markdown
## BRIEFING.md — Latest Updates
| Timestamp | Agent | Update |
|-----------|-------|--------|
| 2026-03-28T15:00:00Z | C7 | Updated CLI_USAGE.md, README.md, inline docs for --doc-check |
```

2. **E1 records the completion** in `DEV_STATE.md`:

```markdown
## RECENT ACTIONS
| Timestamp | Agent | Action | Result |
|-----------|-------|--------|--------|
| 2026-03-28T15:00:00Z | C7 | Documentation sync for --doc-check | ✅ Complete |
```

3. **E1 clears the blocker**:

```markdown
## ACTIVE BLOCKERS
(none)
```

### Coordination Rules

- C7 updates documentation content, E1 updates `.devdocs/` state
- C7 can modify shared `.devdocs` files (`BRIEFING.md`, `AGENTS.md`) but not the folder structure
- E1 cannot write documentation content but records that C7 has completed the update

---

## Step 5: Post-Release Documentation Sync

When B10 (The Gatekeeper) approves a release, C7 is dispatched to perform a
comprehensive documentation sync.

### Actions

1. **Update `CHANGELOG.md`** with the new release entry:

```markdown
## [0.2.0] - 2026-04-01

### Added
- `--doc-check` CLI flag for documentation freshness verification
- Documentation architecture docs (`docs/architecture/`)
- Workflow example docs (`docs/examples/`)

### Changed
- Updated CLI_USAGE.md with new flags
- Updated README.md CLI section
```

2. **Verify version references** across all documentation files

3. **Check all cross-references** to ensure no broken links

4. **Update `DEVELOPMENT.md`** with new phase completion status

5. **Update `PROJECT_STATUS.md`** with current metrics

---

## Key Takeaways

1. **C7 updates existing documentation** — not create new docs (that's A5)
2. **Documentation follows code** — C7 updates docs after code changes, never before
3. **C7 covers all three layers** — project docs (`/docs/`), root docs, and inline code docs
4. **C7 coordinates with E1** — E1 detects drift and assigns; C7 updates; E1 records completion
5. **Cross-references must be verified** — every update should check for broken links
6. **Agent boundaries are strict** — C7 does not modify `.devdocs/` structure or write code

---

## References

- [DOCUMENTATION_GUIDE.md](../DOCUMENTATION_GUIDE.md) — Documentation system guide
- [DOCUMENTATION_ARCHITECTURE.md](../architecture/DOCUMENTATION_ARCHITECTURE.md) — Architecture overview
- [AGENT_BOUNDARIES.md](../AGENT_BOUNDARIES.md) — C7 boundary specification
- [ORCHESTRATOR_WORKFLOW.md](ORCHESTRATOR_WORKFLOW.md) — E1 workflow example
- [WORKFLOWS.md](../WORKFLOWS.md) — Maintenance workflow (includes C7)
