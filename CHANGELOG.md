# Changelog

All notable changes to LOGOS will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added

- **Phase 7: Integration & Release**
  - `docs/RELEASE_NOTES.md` — v0.2.0 release notes with all 7 phase highlights
  - `docs/MIGRATION_GUIDE.md` — Step-by-step migration guide from v0.1.0 to v0.2.0
  - `docs/KNOWN_ISSUES.md` — Known issues with workarounds and status
  - `tests/test_integration/test_v0_2_0_features.py` — Cross-phase integration tests (28 tests)
  - `tests/test_integration/test_workflow_coordination.py` — Workflow coordination integration tests (112 tests)
  - `requirements.txt` — Python dependencies file for pip install
  - `requirements-dev.txt` — Development dependencies file
  - `install-requirements.sh` — Automated dependency installation script with `--dev` flag
  - `scripts/audit_documentation.py` — Documentation audit CLI tool (Phase 6 completion)

### Changed

- Version bumped from 0.2.0.dev0 to 0.2.0
- Development classifier updated from Pre-Alpha to Beta
- DEVELOPMENT.md updated with all phases marked complete

- **Phase 6: Documentation Consolidation**
  - `docs/DOCUMENTATION_GUIDE.md` — Comprehensive documentation system guide covering three-domain architecture
  - `docs/architecture/DOCUMENTATION_ARCHITECTURE.md` — Technical architecture of the documentation system
  - `docs/examples/ORCHESTRATOR_WORKFLOW.md` — E1 Orchestrator workflow example
  - `docs/examples/DOC_UPDATER_WORKFLOW.md` — C7 Doc Updater/Manual Keeper workflow example
  - `docs/DOCUMENTATION_INDEX.md` — Cross-reference index of all project documentation
  - `CONTRIBUTING.md` — Contribution guidelines with code style, testing, and documentation standards
  - `templates/.devdocs/README.md` — Template explaining .devdocs/ folder purpose
  - `templates/docs/README.md` — Template explaining /docs/ folder purpose
  - `logos/core/doc_audit.py` — Documentation audit utilities (link validation, cross-reference checking)
  - `tests/test_documentation/test_role_boundaries.py` — Documentation role boundary validation tests (34 tests)
  - `tests/test_documentation/test_doc_audit.py` — Documentation audit module tests (32 tests)
  - CONSTITUTION.md Article XI: Documentation Standards and Ownership
  - E1 Orchestrator prompts enhanced with documentation domain boundary tables (Daedelus + DEUS)
  - C7 Doc Updater/Manual Keeper prompts enhanced with documentation domain clarification (Daedelus + DEUS)
  - `docs/AGENT_BOUNDARIES.md` updated with E1/C7 documentation role clarifications

- **Phase 5 Progress: Enhanced CLI & UX**
  - `logos/core/config.py` — User-level configuration file support (`~/.logos/config.yaml`)
  - `logos/core/aliases.py` — Agent alias system with built-in aliases for all 50 agents plus custom user aliases
  - `logos/cli/args.py` — CLI argument parsing with `-v`/`--verbose` and `-q`/`--quiet` flags, `--version` support
  - `logos/core/version.py` — Version information module for programmatic version access
  - Shell completion scripts for Bash (`completions/bash/logos`), Zsh (`completions/zsh/_logos`), and Fish (`completions/fish/logos.fish`)
  - `install-completion.sh` — Shell completion installer with auto-detection and per-shell options
  - `docs/SHELL_COMPLETION.md` — Dedicated shell completion installation and usage guide
  - Agent search/filter — `/` prefix in agent selection to search by name, key, alias, or description
  - Prompt preview feature — configurable preview of prompt content before clipboard copy
  - Recent agents tracking — tracks last 10 agent selections globally (stored as `mode:agent` entries) in identity
  - Alias resolution in agent selection — users can select agents by alias (e.g., `architect` → A1)
  - Verbose mode (`-v`) — shows agent metadata and prompt statistics (character count, line count)
  - Quiet mode (`-q`) — suppresses decorative banners and non-essential output
  - CONSTITUTION.md Article X: User Experience and CLI Standards
  - `docs/CLI_USAGE.md` — Comprehensive CLI usage guide with agent aliases, configuration, and troubleshooting
  - `tests/test_cli/test_args.py` — CLI argument parsing tests (14 tests)
  - `tests/test_cli/test_search.py` — Agent search/filter tests (16 tests)
  - `tests/test_cli/test_main.py` — CLI entry point tests (9 tests, updated for argparse support)
  - `tests/test_core/test_version.py` — Version module tests (4 tests)
  - `tests/test_core/test_config.py` — Configuration system tests (24 tests)
  - `tests/test_core/test_aliases.py` — Alias system tests (32 tests)
  - `tests/test_cli/test_agent_select.py` — Agent selection tests (27 tests)
  - `tests/test_core/test_recent_agents.py` — Recent agents tracking tests (12 tests)

- **Phase 4 Complete: OS-Specific Adaptations**
- Added OS-SPECIFIC INSTRUCTIONS sections (Linux + FreeBSD) to all 26 DEUS agents across 5 prompt files
- Created `docs/OS_ADAPTATIONS.md` — OS adaptation architecture overview
- Created `docs/DEUS_LINUX_REFERENCE.md` — Linux command and configuration quick reference
- Created `docs/DEUS_FREEBSD_REFERENCE.md` — FreeBSD command and configuration quick reference
- Added CONSTITUTION.md Article IX: Operating System Adaptations
- Added `tests/test_deus/test_linux_specifics.py` — validates Linux OS sections for all 26 agents
- Added `tests/test_deus/test_freebsd_specifics.py` — validates FreeBSD OS sections for all 26 agents

- **Phase 2 Complete: .devdocs Governance System**
- Implemented Temporal Log Management System (`logos/core/temporal_logs.py`) for automated summarization (daily, weekly, monthly) and archival.
- Implemented `.devdocs` bloat prevention and file archival utilities (`logos/core/bloat_prevention.py`, `logos/core/archival.py`).
- Enhanced all base prompts (`logos/daedelus/prompts/base_orchestrator.py`, `logos/daedelus/prompts/base_maintenance.py`, `logos/deus/prompts/base_system_orchestrator.py`, `logos/deus/prompts/base_maintenance.py`) with strict constitutional `.devdocs` priority read rules.
- Orchestrator agent (E1) updated with specific temporal management and bloat prevention routines.
- `logos/core/devdocs.py` with validation and structural management functions for `.devdocs/`
- Standardized templates for `.devdocs/` initialization including `DEV_STATE.md` and workflow tracking structures
- Tests for `.devdocs` utilities in `tests/test_core/test_devdocs.py`
- CONSTITUTION.md Article VII: .DEVDOCS GOVERNANCE
- `README.md` .devdocs Governance System documentation

- **Phase 1 Complete: Agent Boundary Enforcement System** — all 50 agents across both domains now have explicit scope boundaries with IN SCOPE, FORBIDDEN ACTIONS, REQUIRES COLLABORATION, and REFUSAL TEMPLATE sections
- Refusal response generation utility (`logos/core/refusal.py`)
- Complete agent boundaries reference documentation (`docs/AGENT_BOUNDARIES.md`)
- Agent recommendations cross-reference guide (`docs/AGENT_RECOMMENDATIONS.md`)
- CONSTITUTION.md Article VI: Agent Scope Boundaries and Enforcement
- Scope boundaries implemented for Daedelus Group A (Builders):
  - A1 (The Architect)
  - A2 (The Logic Engineer)
  - A3 (The Interface Designer)
  - A4 (The Test Engineer)
  - A5 (The Scribe)
- Scope boundaries implemented for Daedelus Group B (Guardians):
  - B6 (The Sentinel)
  - B7 (The Marshal)
  - B8 (The Profiler)
  - B9 (The Critic)
  - B10 (The Gatekeeper)
- Scope boundaries implemented for Daedelus Group C (Maintainers):
  - C1 (The Bug Hunter)
  - C6 (The Security Patcher)
  - C7 (The Doc Updater)
  - C8 (The Configurator)
  - C9 (The Optimizer)
  - C10 (The Janitor)
  - C11 (The Librarian)
- Scope boundaries implemented for Daedelus Group D (Workers):
  - D2 (The Feature Sprinter)
  - D3 (The Refactorer)
  - D4 (The UI Tweaker)
  - D5 (The Test Extender)
- Scope boundaries implemented for Daedelus Group E (Operators):
  - E1 (The Orchestrator)
  - E2 (The Operational Control Manager)
  - E3 (Daedelus - The Brutal Perfectionist Supreme Review)
- Scope boundaries implemented for DEUS Group A (Engineers):
  - A1 (The Kernel Architect)
  - A2 (The Driver Engineer)
  - A3 (The Network Architect)
  - A4 (The Boot Engineer)
  - A5 (The Service Scribe)
- Scope boundaries implemented for DEUS Group B (Auditors):
  - B6 (The Security Auditor)
  - B7 (The Syntax Marshal)
  - B8 (The Performance Analyst)
  - B9 (The Compliance Critic)
  - B10 (The Release Gatekeeper)
- Scope boundaries implemented for DEUS Group C (Maintainers):
  - C1 (The Bug Hunter)
  - C6 (The Security Patcher)
  - C7 (The Manual Keeper)
  - C8 (The Sysctl Tuner)
  - C9 (The Optimizer)
  - C10 (The System Janitor)
  - C11 (The Port Librarian)
- Scope boundaries implemented for DEUS Group D (Specialists):
  - D2 (The Port Builder)
  - D3 (The Compatibility Engineer)
  - D4 (The Jail Architect)
  - D5 (The ZFS Engineer)
- Scope boundaries implemented for DEUS Group E (Operators):
  - E1 (The System Orchestrator)
  - E2 (The Administrator)
  - E3 (The General Manager)
  - E4 (The Ombudsman)
  - E5 (DEUS - The Supreme Security Guardian)
- Boundary validation test suite (326 tests across both domains)

### Changed

- Enhanced `E1 The Orchestrator` (Daedelus) and `E1 The System Orchestrator` (DEUS) with constitutional authority over `.devdocs/`
- Updated agent definition descriptions for Orchestrators to emphasize governance
- Modified `docs/AGENT_BOUNDARIES.md` to explicitly list Orchestrator's `.devdocs` management scope and exclusive `.archive/` access
- Version set to 0.2.0.dev0 for active development
- Orchestrator agent now has activation prompt with scope boundaries
- Note: Current project implementation status can be tracked in [DEVELOPMENT.md](DEVELOPMENT.md).

### Fixed

- Corrected DEUS agent names to match actual implementation:
  - A4: The Boot Configurator → The Boot Engineer
  - B7: Syntax Validator → Syntax Marshal
  - B8: Performance Profiler → Performance Analyst
  - B9: Compliance Auditor → Compliance Critic
  - D2: ZFS Specialist → Port Builder
  - D3: Network Specialist → Compatibility Engineer
  - D4: Security Hardener → Jail Architect
  - D5: Automation Specialist → ZFS Engineer

## [0.1.0] - 2026-01-20

### 🎉 Major Milestone: First Stable Release

**Release Type:** Major Release (Pre-Alpha → Alpha)  
**Status:** Stable Alpha

### Added

#### Core Features
- **Unified Agent Federation:** 50 specialized AI agents across two domains
  - 24 Daedelus agents (software development workflow)
  - 26 DEUS agents (system administration)
  - Unified CLI interface for seamless access

- **Persistent Identity System:**
  - System scanning on first run (hostname, username, OS, capabilities)
  - Identity persistence across sessions (YAML-based)
  - Context-aware prompt composition
  - Session history tracking (total sessions, last mode, last agent)

- **Faction System:**
  - 5 philosophical factions (Revanchist, Daedalus, Orphic, Technomancer, Deus)
  - Faction-based behavioral modifiers
  - Consistent experience across domains
  - Faction statistics tracking

- **Cross-Domain Integration:**
  - Unified identity and context sharing
  - Seamless mode switching (Daedelus ↔ DEUS)
  - Shared infrastructure and utilities
  - Coordinated workflows

#### Daedelus Domain (24 Agents)
- **Group A: Builders (A1-A5)**
  - A1: The Architect
  - A2: The Logic Engineer
  - A3: The Interface Designer
  - A4: The Test Engineer
  - A5: The Scribe

- **Group B: Guardians (B6-B10)**
  - B6: The Sentinel
  - B7: The Marshal
  - B8: The Profiler
  - B9: The Critic
  - B10: The Gatekeeper

- **Group C: Maintainers (C1, C6-C11)**
  - C1: The Bug Hunter
  - C6: The Security Patcher
  - C7: The Doc Updater
  - C8: The Configurator
  - C9: The Optimizer
  - C10: The Janitor
  - C11: The Librarian

- **Group D: Workers (D2-D5)**
  - D2: The Feature Sprinter
  - D3: The Refactorer
  - D4: The UI Tweaker
  - D5: The Test Extender

- **Group E: Operators**
  - Orchestrator
  - Operational Control Manager (OCM)
  - Daedelus

#### DEUS Domain (26 Agents)
- **Group A: Engineers (A1-A5)**
  - A1: The Kernel Architect
  - A2: The Driver Engineer
  - A3: The Network Architect
  - A4: The Boot Configurator
  - A5: The Service Scribe

- **Group B: Auditors (B6-B10)**
  - B6: The Security Auditor
  - B7: The Syntax Validator
  - B8: The Performance Profiler
  - B9: The Compliance Auditor
  - B10: The Release Gatekeeper

- **Group C: Maintainers (C1, C6-C11)**
  - C1: The Bug Hunter
  - C6: The Security Patcher
  - C7: The Doc Updater
  - C8: The Configurator
  - C9: The Optimizer
  - C10: The Janitor
  - C11: The Librarian

- **Group D: Specialists (D2-D5)**
  - D2: The ZFS Specialist
  - D3: The Network Specialist
  - D4: The Security Hardener
  - D5: The Automation Specialist

- **Group E: Operators (E1-E5)**
  - E1: The System Orchestrator
  - E2: The Administrator
  - E3: The General Manager
  - E4: The Ombudsman
  - E5: DEUS

#### Technical Infrastructure
- **System Scanning:**
  - Parallel subprocess execution (5-10x faster)
  - FreeBSD-specific capability detection (ZFS, jails)
  - OS version and architecture detection
  - Python version detection

- **Identity Management:**
  - YAML-based persistence with secure file permissions (0o600)
  - Comprehensive schema validation
  - Session tracking and statistics

- **Prompt Composition:**
  - Context injection (identity, faction, session history)
  - OS adaptation (FreeBSD → Linux for DEUS agents)
  - Faction modifier application
  - Agent-specific prompt generation

- **CLI Interface:**
  - First-run wizard (system scan, faction selection)
  - Mode selection (Daedelus/DEUS)
  - Agent selection with navigation
  - Clipboard integration (xclip, xsel, wl-copy, pyperclip)

#### Security Features
- Input validation and sanitization
- Secure file permissions (automatic 0o600/0o700)
- Subprocess security (timeouts, command lists)
- Dependency vulnerability scanning (pip-audit integration)
- No telemetry or data collection

#### Performance Optimizations
- Parallel system scanning (5-10x faster)
- Dictionary-based agent lookup (O(1) access)
- Lazy agent loading (memory efficient)
- Fast startup (<1 second after first run)

### Documentation

#### Core Documentation
- **README.md:** Comprehensive 1370+ line documentation covering:
  - What is LOGOS
  - Why LOGOS (rationale and market position)
  - How LOGOS works
  - Installation and setup
  - Usage guide
  - Technical architecture
  - Maintenance and troubleshooting
  - FAQs
  - Security
  - Performance
  - Development
  - License

- **CONSTITUTION.md:** Complete LOGOS Federation Constitution v2.0
  - Foundational principles
  - Prime Directives (8 non-negotiable directives)
  - Agent architecture and separation of duties
  - Rights, regulations, rules, and laws
  - Enforcement and remediation
  - Amendments and evolution

- **blueprint.md:** Integration analysis and architecture plan

- **INSTALL.md:** Installation instructions

#### Domain Documentation
- **docs/FACTIONS.md:** Detailed faction system documentation
- **docs/WORKFLOWS.md:** Workflow guides

#### Code Documentation
- **100% Documentation Compliance:** All 69 Python files use structured comment schema
- **Docstrings:** All public functions have comprehensive docstrings
- **Structured Comments:** All code uses `##` prefix schema for implementation details

### Testing

- **Test Suite:** 13 test modules covering:
  - Core functionality (identity, persistence, validation, prompts, etc.)
  - CLI components (first-run, mode selection, layouts)
  - Domain-specific functionality
  - Constitutional compliance

- **CI/CD:** GitHub Actions workflow
  - Tests on Python 3.10, 3.11, 3.12
  - Linting with Ruff
  - Security auditing with pip-audit
  - Coverage reporting

### Changed

- **Version:** 0.0.1 (Pre-Alpha) → 0.1.0 (Alpha)
- **Status:** Pre-Alpha → Alpha (stable release)

### Fixed

- All critical bugs from Pre-Alpha release
- Security hardening (input validation, file permissions)
- Performance optimizations (parallel scanning, lazy loading)

### Security

- Comprehensive input validation
- Secure file permissions (0o600, 0o700)
- Subprocess security (timeouts, no shell injection)
- Dependency vulnerability scanning

---

## [0.0.1] - Pre-Alpha (Deprecated)

### Added

- Initial Pre-Alpha release
- Basic agent system
- Initial CLI implementation
- Core infrastructure

### Note

**This version is deprecated.** Users should upgrade to v0.1.0.

---

## Version History

- **0.1.0** (2026-01-20): First stable Alpha release
- **0.0.1** (Pre-Alpha): Initial development release (deprecated)

---

## Links

- [Repository](https://github.com/orpheus497/logos)
- [Issues](https://github.com/orpheus497/logos/issues)
- [Documentation](README.md)

---

**For The LOGOS Federation**  
**For Human Empowerment**  
**For Excellence and Quality**

---

*Changelog maintained by Agent #10 - The Gatekeeper*  
*Following Semantic Versioning and Keep a Changelog format*
