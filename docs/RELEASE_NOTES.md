# LOGOS v0.2.0 Release Notes

## Release Information

| Field | Value |
|---|---|
| **Version** | 0.2.0 |
| **Release Date** | TBD |
| **Release Type** | Major Feature Release (Alpha → Beta) |
| **Previous Version** | 0.1.0 |
| **Python** | 3.10+ |
| **License** | AGPL-3.0 |

---

## Summary

LOGOS v0.2.0 is a major feature release that advances the project from Alpha to Beta status.
This release completes all seven development phases, adding constitutional governance,
agent boundary enforcement, OS adaptations, an enhanced CLI experience, and comprehensive
documentation across all 50 agents in both the Daedelus (software development) and DEUS
(system administration) domains.

---

## Phase Highlights

### Phase 1: Agent Boundary Enforcement

All 50 agents across both domains now have explicit scope boundaries with IN SCOPE,
FORBIDDEN ACTIONS, REQUIRES COLLABORATION, and REFUSAL TEMPLATE sections. A boundary
validation test suite (326 tests) ensures ongoing compliance.

### Phase 2: .devdocs Governance

Introduced the Temporal Log Management System for automated summarization (daily, weekly,
monthly) and archival. Bloat prevention utilities enforce size limits on `.devdocs/` and
automatically archive stale content. Constitution Article VII codifies governance rules.

### Phase 3: Workflow Coordination

Implemented the END-OF-TASK protocol for structured handoffs between agents. Three workflow
patterns are now supported: sequential pipeline, parallel fan-out/fan-in, and iterative
review cycles. See `docs/WORKFLOWS.md` for details.

### Phase 4: OS Adaptations

Added OS-SPECIFIC INSTRUCTIONS sections (Linux and FreeBSD) to all 26 DEUS agents across
5 prompt files. Dedicated quick-reference guides provide per-OS command and configuration
details. Constitution Article IX formalizes OS adaptation requirements.

### Phase 5: Enhanced CLI & UX

Added user-level configuration (`~/.logos/config.yaml`), agent aliases for all 50 agents,
shell completions (Bash, Zsh, Fish), agent search/filter, prompt preview, recent agent
tracking, and verbose/quiet modes. Constitution Article X establishes UX standards.

### Phase 6: Documentation Consolidation

Created architecture guides, workflow examples, a documentation cross-reference index,
contribution guidelines, and a documentation audit module. Constitution Article XI defines
documentation standards and ownership. Agent prompts for E1 and C7 were enhanced with
domain boundary tables.

### Phase 7: Integration & Release

Final integration testing, version bump from 0.2.0.dev0 to 0.2.0, release notes,
migration guide, and known issues documentation. Ensures all phases work together
as a cohesive release.

---

## What's New

### Added

- Agent boundary enforcement for all 50 agents (Phase 1)
- `.devdocs/` governance system with temporal logs, bloat prevention, and archival (Phase 2)
- END-OF-TASK protocol and 3 workflow coordination patterns (Phase 3)
- Linux and FreeBSD OS-specific instructions for all 26 DEUS agents (Phase 4)
- User-level configuration file (`~/.logos/config.yaml`) (Phase 5)
- Agent alias system — 50 built-in aliases plus custom user aliases (Phase 5)
- Shell completions for Bash, Zsh, and Fish (Phase 5)
- Agent search/filter with `/` prefix in agent selection (Phase 5)
- Prompt preview feature (Phase 5)
- Recent agents tracking (last 10 selections) (Phase 5)
- Verbose mode (`-v`) and quiet mode (`-q`) CLI flags (Phase 5)
- `--version` flag (Phase 5)
- Documentation architecture guides, workflow examples, and audit tools (Phase 6)
- Contribution guidelines (`CONTRIBUTING.md`) (Phase 6)
- CONSTITUTION.md Articles VI–XI (Phases 1–6)
- Comprehensive test suite covering all new features

### Changed

- Version: 0.1.0 → 0.2.0
- Status: Alpha → Beta
- CONSTITUTION.md updated from v1.0 to v2.0 with six new articles

### Fixed

- Corrected DEUS agent names to match actual implementation (see CHANGELOG.md)

---

## Breaking Changes

**None.** This release is fully backward compatible with v0.1.0. All new features are
additive. Existing identity files, agent prompts, and workflows continue to work without
modification.

---

## Dependencies

| Package | Version | Status |
|---|---|---|
| `pyyaml` | >=6.0 | Unchanged |
| `wcwidth` | >=0.2.0 | Unchanged |
| `pyperclip` | >=1.8.0 | Optional (clipboard) |

No new required dependencies have been added in this release.

---

## Known Issues

See [docs/KNOWN_ISSUES.md](KNOWN_ISSUES.md) for the full list of known issues.

Key items:

- Arrow-key interactive navigation is not yet implemented (uses `input()` prompts)
- Clipboard integration requires external tools on Linux/FreeBSD
- Shell completions require manual installation

---

## Upgrade Instructions

See [docs/MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) for step-by-step upgrade instructions
from v0.1.0 to v0.2.0.

---

## Testing

The v0.2.0 test suite includes:

- 326 agent boundary validation tests (Phase 1)
- `.devdocs` governance tests (Phase 2)
- 135 CLI tests across 6 test modules (Phase 5)
- 34 documentation role boundary tests (Phase 6)
- 32 documentation audit tests (Phase 6)
- All tests pass on Python 3.10, 3.11, and 3.12

---

## Links

- [Repository](https://github.com/orpheus497/logos)
- [Changelog](../CHANGELOG.md)
- [Constitution](../CONSTITUTION.md)
- [Installation](../INSTALL.md)
- [CLI Usage Guide](CLI_USAGE.md)

---

**For The LOGOS Federation**
**For Human Empowerment**
**For Excellence and Quality**

---

*Release notes maintained by Agent B10 — The Gatekeeper*
