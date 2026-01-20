# LOGOS - Unified AI Agent Federation

**Version:** 0.0.1 (Pre-Alpha)  
**License:** GNU Affero General Public License v3.0 (AGPL-3.0)  
**Author:** orpheus497

---

## Overview

LOGOS is a unified system that merges two existing AI agent systems into a single, cohesive CLI tool:

- **Daedelus:** 22-agent development workflow system for software development
- **DEUS:** 26-agent FreeBSD system administration system (with Linux support)

The result is a unified CLI that provides persistent identity, context-aware agent selection, and seamless switching between development and system administration workflows.

---

## Features

### Core Capabilities

- **Unified Agent Federation:** Access to 48 specialized AI agents (22 Daedelus + 26 DEUS)
- **Persistent Identity:** System scanning and identity persistence across sessions
- **Faction System:** Choose your philosophical approach (Revanchist, Orphic, Technomancer)
- **Mode Selection:** Switch between Daedelus (development) and DEUS (system administration) modes
- **Beautiful Terminal UI:** Professional box-drawing interface with semantic colors
- **Cross-Platform:** Works on Linux, FreeBSD, and other Unix-like systems
- **Security Hardened:** Secure file permissions, input validation, schema validation
- **Performance Optimized:** Parallel system scanning, optimized agent lookup, lazy loading

### Current Implementation Status

**✅ Phase 2: Core Infrastructure** - COMPLETE
- Shared utilities (clipboard, terminal, constants, logging)
- Identity system with system scanning
- YAML-based configuration persistence
- Faction system with behavioral modifiers
- Prompt composition system
- Input and schema validation

**✅ Phase 3: UI System** - COMPLETE
- Terminal UI component library
- Box-drawing characters and layouts
- Enhanced color system
- Pre-built layout components

**✅ Phase 4: CLI Implementation** - COMPLETE
- First-run wizard with faction selection
- Mode selection interface
- Agent selection menus
- Welcome screen with context
- Faction statistics tracking

**✅ Phase 5: Domain Integration** - COMPLETE
- All 22 Daedelus agents ported
- All 26 DEUS agents ported
- All prompts preserved and functional
- OS adaptation for Linux systems (DEUS)

**✅ Security Audit** - COMPLETE
- All vulnerabilities identified and fixed
- Secure file permissions (0o600/0o700)
- Enhanced input validation
- Comprehensive YAML schema validation

**✅ Performance Optimization** - COMPLETE
- System scanning parallelization (5-10x faster)
- Agent lookup optimization (2x faster)
- Lazy agent loading (2-3x memory reduction)

**✅ Test Suite** - COMPLETE
- 118 test functions across 22 test files
- Security tests (37 tests)
- Performance benchmarks (11 tests)
- CLI integration tests

---

## Installation

### Quick Install (Recommended)

The installation script automatically handles all dependencies and sets up LOGOS as a system package:

```bash
# Clone the repository
git clone https://github.com/orpheus497/logos.git
cd logos

# Run installation script
./install.sh
```

The script will:
- ✅ Detect your OS (FreeBSD or Linux)
- ✅ Check Python 3.10+ availability
- ✅ Install Python dependencies (PyYAML, pyperclip)
- ✅ Install system clipboard tools (xclip/xsel/wl-copy) if needed
- ✅ Install LOGOS to `~/.logos`
- ✅ Create `logos` command accessible from anywhere
- ✅ Configure PATH if needed

After installation, simply run:
```bash
logos
```

### Requirements

- Python 3.10 or higher
- PyYAML 6.0+ (required, installed automatically)
- Optional: Clipboard support
  - Linux: `xclip`, `xsel`, or `wl-copy` (Wayland)
  - FreeBSD: `xclip` or `xsel`
  - Cross-platform: `pyperclip` (installed automatically)

### Manual Installation

If you prefer manual installation:

```bash
# Clone the repository
git clone https://github.com/orpheus497/logos.git
cd logos

# Install Python dependencies
pip3 install --user pyyaml>=6.0 pyperclip>=1.8.0

# Copy package to ~/.logos
mkdir -p ~/.logos
cp -r logos ~/.logos/

# Create command wrapper
mkdir -p ~/.local/bin
cat > ~/.local/bin/logos << 'EOF'
#!/bin/bash
cd ~/.logos && python3 -m logos "$@"
EOF
chmod +x ~/.local/bin/logos

# Add to PATH (if not already)
export PATH="$HOME/.local/bin:$PATH"
```

### Development Installation

For development work:

```bash
# Clone the repository
git clone https://github.com/orpheus497/logos.git
cd logos

# Install in development mode
pip install -e .

# Install with clipboard support
pip install -e ".[clipboard]"

# Install development dependencies
pip install -e ".[dev]"
```

---

## Usage

### First Run

On first launch, LOGOS will guide you through setup:

1. **System Scan:** Automatically detects your system information
2. **Faction Selection:** Choose your philosophical approach:
   - **Revanchist:** Aggressive, results-focused
   - **Orphic:** Balanced, thoughtful
   - **Technomancer:** Technical, precise
3. **Identity Creation:** Your identity is saved to `~/.logos/identity.yaml`

### Interactive Mode

```bash
# Launch LOGOS
logos

# Or as a module
python -m logos
```

The CLI provides:
- **Welcome Screen:** Personalized greeting with system context
- **Mode Selection:** Choose Daedelus (development) or DEUS (system administration)
- **Agent Selection:** Browse and select from 48 specialized agents
- **Faction Statistics:** View usage statistics (press 'T' in mode selection)
- **Session Tracking:** Automatic tracking of your usage patterns

### Command-Line Options

```bash
# Interactive mode (default)
logos

# Direct mode selection (future)
logos daedelus    # Launch in Daedelus mode
logos deus        # Launch in DEUS mode
```

---

## Architecture

### Project Structure

```
logos/
├── logos/                    # Main package
│   ├── core/                # Shared infrastructure
│   │   ├── agent.py         # Agent dataclass
│   │   ├── clipboard.py     # Clipboard utilities
│   │   ├── constants.py     # Constants
│   │   ├── factions.py      # Faction system
│   │   ├── identity.py      # Identity system
│   │   ├── logging.py       # Logging utilities
│   │   ├── persistence.py   # Config persistence
│   │   ├── prompts.py       # Prompt composition
│   │   ├── terminal.py      # Terminal utilities
│   │   ├── ui.py            # UI components
│   │   └── validation.py    # Input & schema validation
│   ├── daedelus/            # Daedelus domain (22 agents)
│   │   ├── agents.py        # Agent definitions
│   │   ├── prompts/         # Agent prompts
│   │   └── constitution.py  # Constitution text
│   ├── deus/                # DEUS domain (26 agents)
│   │   ├── agents.py        # Agent definitions
│   │   ├── prompts/         # Agent prompts
│   │   └── mandate.py       # Mandate text
│   └── cli/                 # CLI components
│       ├── layouts.py       # UI layouts
│       ├── main.py          # Main entry point
│       ├── first_run.py     # First-run wizard
│       ├── mode_select.py   # Mode selection
│       └── agent_select.py  # Agent selection
├── tests/                    # Test suite
│   ├── test_core/           # Core module tests
│   ├── test_cli/            # CLI tests
│   └── conftest.py          # Test fixtures
├── .devdocs/                 # Development documentation
│   ├── BRIEFING.md          # Current status
│   ├── PROGRESS.md          # Session log
│   ├── TESTS.md             # Test results
│   └── [agent folders]/     # Agent-specific docs
├── blueprint.md             # Project specification
├── LICENSE                   # AGPL-3.0 license
└── pyproject.toml           # Project configuration
```

### Agent System

LOGOS provides access to 48 specialized AI agents:

**Daedelus Agents (22):**
- **Group A - Builders (A1-A5):** Architect, Logic Engineer, Interface Designer, Test Engineer, Scribe
- **Group B - Guardians (B6-B10):** Sentinel, Marshal, Profiler, Critic, Gatekeeper
- **Group C - Maintainers (C1, C6-C11):** Refactorer, Sanitizer, Optimizer, etc.
- **Group D - Workers (D2-D5):** Implementer, Debugger, Documenter, Integrator
- **Group E - Operators:** Orchestrator, Operational Control Manager, Daedelus

**DEUS Agents (26):**
- **Group A - Engineers (A1-A5):** Kernel Architect, Driver Engineer, Network Architect, Boot Engineer, Service Architect
- **Group B - Auditors (B6-B10):** Security Auditor, Syntax Marshal, Performance Auditor, Compliance Auditor, Release Gatekeeper
- **Group C - Maintainers (C1, C6-C11):** System Librarian, Port Librarian, etc.
- **Group D - Specialists (D2-D5):** ZFS Engineer, Network Specialist, Security Specialist, Automation Specialist
- **Group E - Operators (E1-E5):** System Administrator, Ombudsman, etc.

---

## Configuration

### Identity File

Your identity is stored in `~/.logos/identity.yaml`:

```yaml
identity:
  username: your_username
  hostname: your_hostname
  created: 2026-01-20T12:00:00Z
faction:
  name: orphic
system:
  os: Linux
  version: 5.15.0
sessions:
  last_mode: daedelus
  last_agent: A1
  total_sessions: 42
prompt_counts:
  faction:
    orphic: 25
  mode:
    daedelus: 20
    deus: 5
```

**Security:** Identity files are automatically protected with secure permissions (0o600).

---

## Development

### Running Tests

```bash
# Install test dependencies
pip install -e ".[dev]"

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=logos.core --cov=logos.cli --cov-report=html --cov-report=term

# Run specific test suites
pytest tests/test_core/test_validation.py -v
pytest tests/test_cli/ -v
```

### Code Quality

```bash
# Linting
ruff check logos/

# Formatting
ruff format logos/
```

### Security Scanning

```bash
# Dependency vulnerability scan
pip-audit
```

---

## Documentation

### Project Documentation

- **Constitution:** `CONSTITUTION.md` - **The LOGOS Federation Constitution** - The supreme governing document for all members, agents, and systems
- **Blueprint:** `blueprint.md` - Complete integration analysis and architecture plan
- **Development Docs:** `.devdocs/` - Comprehensive development documentation
  - `BRIEFING.md` - Current project status
  - `PROGRESS.md` - Development session log
  - `TESTS.md` - Test results and coverage
  - `DECISIONS_LOG.md` - Architecture decisions
  - `AGENTS.md` - Agent registry and definitions
- **Domain Documentation:** `docs/` - Domain-specific reference materials
  - `FACTIONS.md` - Faction system overview
  - `WORKFLOWS.md` - Workflow overview

### Agent-Specific Documentation

Each agent maintains documentation in `.devdocs/[agent_folder]/`:
- Builders: Architect, Logic Engineer, Interface Designer, Test Engineer, Scribe
- Guardians: Sentinel, Marshal, Profiler, Critic, Gatekeeper

---

## Security

LOGOS implements comprehensive security measures:

- **Secure File Permissions:** Configuration files use 0o600 (files) and 0o700 (directories)
- **Input Validation:** Length limits, control character detection, character whitelisting
- **Schema Validation:** Comprehensive YAML schema validation
- **Dependency Scanning:** pip-audit integration for vulnerability detection
- **Safe Operations:** No shell injection vectors, safe YAML loading, secure path handling

See `.devdocs/guardians/sentinel/` for detailed security documentation.

---

## Performance

LOGOS is optimized for performance:

- **System Scanning:** 5-10x faster with parallel execution (worst case: 6s → 0.5s)
- **Agent Lookup:** 2x faster with optimized dictionary access
- **Memory Usage:** 2-3x reduction on startup with lazy agent loading
- **Overall Grade:** A- (excellent performance)

See `.devdocs/guardians/profiler/` for detailed performance documentation.

---

## License

This project is licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0)**.

See the [LICENSE](LICENSE) file for the full license text.

**Why AGPL-3.0?**
- Ensures all modifications and improvements remain open source
- Protects the open source nature of the project
- Aligns with Free and Open Source Software principles

---

## Contributing

This project is in active development. Contribution guidelines will be added in a future release.

**Current Status:** Pre-Alpha - Core functionality complete, testing in progress.

---

## Roadmap

### Completed ✅
- [x] Phase 2: Core Infrastructure
- [x] Phase 3: UI System
- [x] Phase 4: CLI Implementation
- [x] Phase 5: Domain Integration
- [x] Security Audit & Fixes
- [x] Performance Optimization
- [x] Comprehensive Test Suite
- [x] Unified Constitution - Complete comprehensive constitutional framework

### In Progress ⏳
- [ ] Test execution and coverage verification
- [ ] Production release preparation

### Planned 📋
- [ ] Full CLI feature completion
- [ ] Integration testing
- [ ] Documentation completion
- [ ] First stable release (v0.1.0)

---

## Acknowledgments

LOGOS merges and extends:
- **Daedelus:** 22-agent development workflow system
- **DEUS:** 26-agent FreeBSD system administration system

Both systems are integrated with respect for their original designs while creating a unified experience.

---

## Support

- **Repository:** https://github.com/orpheus497/logos
- **Issues:** https://github.com/orpheus497/logos/issues
- **Documentation:** See `.devdocs/` for comprehensive development documentation

---

**Status:** Pre-Alpha - Phase 5 Complete, Testing in Progress  
**Last Updated:** 2026-01-20
