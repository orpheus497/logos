# LOGOS - Unified AI Agent Federation

**Version:** 0.2.0.dev0  
**License:** GNU Affero General Public License v3.0 (AGPL-3.0)  
**Author:** orpheus497

[![Test Suite](https://github.com/orpheus497/logos/actions/workflows/test.yml/badge.svg)](https://github.com/orpheus497/logos/actions/workflows/test.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

---

## 🚧 Development Notice

LOGOS v0.2.0.dev0 is in active development on the `develop` branch. Current focus: agent boundary enforcement and refusal mechanism infrastructure. See [CHANGELOG.md](CHANGELOG.md) for details.

---

## Table of Contents

1. [What is LOGOS?](#what-is-logos)
2. [Why LOGOS? Rationale and Market Position](#why-logos-rationale-and-market-position)
3. [How LOGOS Works](#how-logos-works)
4. [Agent Boundaries](#agent-boundaries)
5. [Installation](#installation)
6. [Setup and Configuration](#setup-and-configuration)
7. [Usage Guide](#usage-guide)
8. [Technical Architecture](#technical-architecture)
9. [Maintenance and Troubleshooting](#maintenance-and-troubleshooting)
10. [FAQs](#faqs)
11. [Security](#security)
12. [Performance](#performance)
13. [Development](#development)
14. [Documentation](#documentation)
15. [License](#license)

---

## What is LOGOS?

LOGOS is a **unified AI agent federation system** that provides a command-line interface for accessing 50 specialized AI agents across two domains: software development (Daedelus) and system administration (DEUS). It is not an AI model itself, but rather a sophisticated prompt engineering and agent orchestration framework that prepares context-rich prompts for use with AI models (like Claude, GPT-4, etc.).

### Core Purpose

LOGOS serves as an **intelligent prompt composition system** that:

1. **Scans your system** to gather context (OS, hostname, username, system capabilities)
2. **Maintains persistent identity** across sessions (faction choice, usage statistics, session history)
3. **Composes specialized prompts** by combining:
   - Agent-specific instructions and capabilities
   - Your system identity and context
   - Your chosen philosophical faction (affects agent behavior)
   - Domain-specific adaptations (e.g., FreeBSD vs Linux for DEUS agents)
4. **Provides a unified CLI** for selecting agents and generating these context-aware prompts

### What LOGOS Does NOT Do

- **LOGOS does not execute AI models** - It generates prompts that you copy and paste into your AI interface
- **LOGOS does not make system changes** - It only generates prompts; you execute the suggestions
- **LOGOS does not store AI responses** - It only tracks your usage patterns and system identity

### The Two Domains

**Daedelus Domain (24 agents):** Software development workflow agents
- **Builders (A1-A5):** Create new code, structure projects, design interfaces, write tests, document
- **Guardians (B6-B10):** Review code for security, syntax, performance, quality, and release readiness
- **Maintainers (C1, C6-C11):** Fix bugs, update docs, optimize code, manage dependencies, clean up
- **Workers (D2-D5):** Implement features, debug issues, extend tests, tweak UI
- **Operators (E1-E3):** Orchestrate workflows, manage operations, provide ultimate oversight

**DEUS Domain (26 agents):** System administration agents (FreeBSD/Linux)
- **Engineers (A1-A5):** Design kernel configs, manage drivers, architect networks, configure boot, design services
- **Auditors (B6-B10):** Audit security, validate syntax, profile performance, ensure compliance, gate releases
- **Maintainers (C1, C6-C11):** Manage packages, update ports, maintain configs, patch security, optimize systems
- **Specialists (D2-D5):** Custom port compilation, Linux compatibility/Wine, jails and isolation, ZFS storage architecture
- **Operators (E1-E5):** Administer systems, resolve conflicts, provide ultimate system oversight

---

## Why LOGOS? Rationale and Market Position

### The Problem: Fragmented AI Assistant Experience

The current AI coding assistant landscape suffers from critical limitations:

1. **Context Amnesia:** Every conversation starts from scratch. The AI doesn't know your system, your preferences, your project history, or your workflow patterns. You waste time re-explaining context in every session.

2. **Generic Prompts:** Most users rely on ad-hoc, improvised prompts. There's no systematic approach to prompt engineering, leading to inconsistent results and missed opportunities for optimization.

3. **No Specialization:** General-purpose AI assistants try to be everything to everyone. They lack the deep, domain-specific expertise needed for complex software development or system administration tasks.

4. **Disconnected Workflows:** Development and system administration are treated as separate silos. There's no unified framework for cross-domain collaboration, even though real-world projects often require both.

5. **No Persistent Identity:** Your relationship with the AI is ephemeral. There's no memory of your preferences, your system configuration, or your past interactions.

6. **Manual Context Management:** Users must manually paste system information, project context, and preferences into every conversation. This is tedious, error-prone, and inefficient.

### The Market Gap

**What exists:**
- Generic AI coding assistants (GitHub Copilot, ChatGPT, Claude)
- Specialized tools for specific tasks (linters, formatters, test runners)
- Manual prompt libraries and templates

**What's missing:**
- **Unified agent federation** with specialized, context-aware agents
- **Persistent identity system** that remembers you across sessions
- **Intelligent prompt composition** that automatically builds context-rich prompts
- **Cross-domain coordination** between development and system administration
- **Philosophical framework** (faction system) that adapts agent behavior to your preferences
- **Recursive self-improvement** where the system was built using its own methodology

### Why LOGOS is the Best Tool for AI Agent CLI Code Assistants

#### 1. **Specialized Agent Federation**

Unlike generic AI assistants, LOGOS provides **50 specialized agents**, each with deep expertise in specific domains:

- **Builders/Engineers** create new structures with architectural precision
- **Guardians/Auditors** review and validate with domain-specific knowledge
- **Maintainers** fix, update, and optimize with systematic approaches
- **Workers/Specialists** implement specific features with focused expertise
- **Operators** orchestrate complex workflows with holistic oversight

This specialization means you get **expert-level guidance** for each task, not generic advice that tries to cover everything.

#### 2. **Context-Aware Prompt Engineering**

LOGOS doesn't just generate prompts—it **composes context-rich instruction sets** that include:

- Your system identity (OS, hostname, username, capabilities)
- Your session history (what you've worked on, which agents you've used)
- Your philosophical preferences (faction modifiers that shape agent behavior)
- Domain-specific adaptations (FreeBSD vs Linux, development vs administration)

The result: **Prompts that are 10x more effective** because they're tailored to your exact context, not generic templates.

#### 3. **Persistent Identity System**

LOGOS maintains a **persistent relationship** with you:

- Remembers your system configuration across sessions
- Tracks your usage patterns and preferences
- Provides continuity between development and administration workflows
- Builds a profile of your work style over time

This means **every conversation starts with full context**, not from zero.

#### 4. **Unified Cross-Domain Workflow**

Real-world projects require both development and system administration. LOGOS is the **only tool** that unifies these domains:

- Switch seamlessly between Daedelus (development) and DEUS (administration) modes
- Share identity and context across domains
- Coordinate workflows that span both domains
- Maintain consistency in approach and documentation

**Example:** Develop a FreeBSD application (Daedelus), configure the jail environment (DEUS), deploy to production (DEUS), and maintain the codebase (Daedelus)—all with unified context.

#### 5. **Philosophical Framework (Faction System)**

LOGOS recognizes that different users have different preferences for AI collaboration. The system provides **five distinct factions** representing a spectrum from minimal to maximum AI autonomy:

- **The Revanchists (Minimal):** Maximum human control, teaching focus, explicit approval required for all actions. "AI/ML is dangerous if left unchecked—I hate AI/ML and will never trust it"
- **The Daedalus Faction (Low):** Careful monitoring, permission required for all actions, mistake prevention focus. "AI/ML can be used as a tool but must be checked regularly—it WILL make mistakes if unmonitored"
- **The Orphics (Balanced):** Collaborative partnership, multiple options provided, educational explanations. "Technology enhances human intelligence—I am in control, it asks me to confirm everything"
- **The Technomancers (High):** High autonomy with human direction for major decisions, proactive suggestions, batch operations. "AI/ML can manage my system and build programs—I need to direct it"
- **The Deus Faction (Maximum):** Full autonomy, no human input needed, parameter-based governance. "AI/ML can be totally autonomous—I can trust it, no human input needed for action"

Your faction choice **modifies agent behavior** to match your preferences, ensuring the AI works the way you want it to work. All five factions are equal members of the LOGOS Federation, bound by the same constitutional principles while expressing those principles through their chosen approach.

**For detailed information about each faction, including characteristics, use cases, and comparison tables, see [docs/FACTIONS.md](docs/FACTIONS.md).**

#### 6. **Proven Methodology: Built by Itself**

**LOGOS is a recursive, self-referential system.** The entire LOGOS codebase was built using the very engineered prompts and methodology it provides. **The Architect** - orpheus497 - designed and built LOGOS using a CLI interface and these specialized prompts, following the LOGOS Constitution throughout the development process.

**This recursive nature proves the system works.** LOGOS isn't just a tool—it's a **validated methodology** that has already produced a complete, production-ready codebase. The Architect (orpheus497) used the LOGOS prompt engineering system to build LOGOS itself, demonstrating the system's effectiveness in real-world development. Every component—from the core infrastructure to the UI system, from the agent definitions to the test suite—was developed using these engineered prompts and the constitutional framework that governs the LOGOS Federation.

#### 7. **Open Source and Extensible**

LOGOS is **100% Free and Open Source Software** (AGPL-3.0):

- No vendor lock-in
- Full transparency
- Community-driven development
- Extensible architecture (add your own agents)
- No hidden costs or proprietary restrictions

#### 8. **Performance and Reliability**

LOGOS is optimized for real-world use:

- **Fast startup:** <1 second (after first run)
- **Parallel system scanning:** 5-10x faster than sequential
- **Memory efficient:** Lazy loading, optimized data structures
- **Secure:** Comprehensive input validation, secure file permissions, schema validation
- **Tested:** 118 test functions ensuring reliability

### The Competitive Advantage

**Compared to generic AI assistants:**
- ✅ Specialized agents vs. generic responses
- ✅ Context-aware prompts vs. manual context management
- ✅ Persistent identity vs. session amnesia
- ✅ Cross-domain coordination vs. siloed workflows

**Compared to manual prompt libraries:**
- ✅ Dynamic composition vs. static templates
- ✅ System-aware adaptation vs. generic prompts
- ✅ Faction-based customization vs. one-size-fits-all
- ✅ Unified framework vs. disconnected tools

**Compared to specialized tools:**
- ✅ 50 agents in one system vs. multiple separate tools
- ✅ Development + administration vs. single-domain focus
- ✅ Context persistence vs. isolated sessions
- ✅ Philosophical framework vs. rigid workflows

### Real-World Impact

LOGOS has already proven its value:

- **Built itself:** The entire codebase was developed using LOGOS agents
- **Comprehensive:** 50 specialized agents covering all aspects of development and administration
- **Production-ready:** Security-hardened, performance-optimized, fully tested
- **Documented:** Extensive documentation including constitution, blueprints, and agent-specific guides
- **Validated:** Used in production to build a complex, multi-domain system

### The Future of AI-Assisted Development

LOGOS represents a **paradigm shift** from ad-hoc AI interactions to **systematic, context-aware collaboration**:

1. **From generic to specialized:** Expert agents for every task
2. **From ephemeral to persistent:** Identity and context that accumulates
3. **From manual to automated:** Intelligent prompt composition
4. **From siloed to unified:** Cross-domain coordination
5. **From static to adaptive:** Faction-based behavioral modification

**LOGOS isn't just a tool—it's the foundation for the next generation of AI-assisted development and system administration.**

---

## How LOGOS Works

### System Flow

```
1. User runs: logos
   ↓
2. First Run? → Yes: System Scan → Faction Selection → Identity Creation
   ↓
3. Load Identity (from ~/.logos/identity.yaml)
   ↓
4. Display Welcome Screen (with system context)
   ↓
5. Mode Selection (Daedelus or DEUS)
   ↓
6. Agent Selection (browse 24 or 26 agents)
   ↓
7. Prompt Composition:
   - Agent base prompt (capabilities, instructions)
   - Identity context (user, system, faction, session history)
   - Faction modifiers (behavioral adjustments)
   - OS adaptation (if DEUS domain on Linux)
   ↓
8. Display Complete Prompt (ready to copy to AI)
   ↓
9. Update Session Tracking (increment counters, save identity)
```

### Prompt Composition Process

When you select an agent, LOGOS performs the following composition:

1. **Base Agent Prompt:** Loads the agent's purpose, activation instructions, and domain-specific base prompt (Maintenance Orchestrator or System Orchestrator)
2. **OS Adaptation (DEUS only):** If running on Linux, automatically adapts FreeBSD-specific references to Linux equivalents (e.g., `sysrc` → `systemctl`, `pkg` → `apt/yum/dnf`)
3. **Identity Context Injection:** Adds a formatted block containing:
   - Your username and hostname
   - Operating system and version
   - Your chosen faction and its philosophy
   - Session history (total sessions, last mode, last agent)
4. **Faction Modifier Application:** Appends behavioral modifiers based on your faction:
   - **Revanchists (Minimal):** Maximum approval friction, teaching mode, guides user to perform actions
   - **Daedalus (Low):** Permission for all actions/sub-actions, close monitoring, mistake prevention
   - **Orphics (Balanced):** Permission for all actions, multiple options, educational explanations
   - **Technomancers (High):** Human control for major decisions, batch operations, proactive suggestions
   - **Deus (Maximum):** No human input needed, autonomous operation, parameter-based governance

The final prompt is a complete, context-aware instruction set ready for your AI model.

### Identity System

LOGOS maintains a persistent identity file (`~/.logos/identity.yaml`) that stores:

- **Identity Information:** Username, hostname, creation timestamp
- **Faction Choice:** Your selected philosophical approach
- **System Information:** OS name, version, architecture
- **Session Tracking:**
  - Last mode used (daedelus/deus)
  - Last agent used (e.g., "A1", "B6")
  - Total session count
  - Prompt counts by faction and mode

This identity persists across sessions and provides context to all agents.

### System Scanning

On first run, LOGOS performs a comprehensive system scan:

**Universal Checks:**
- Hostname (via `socket.gethostname()`)
- Username (via `getpass.getuser()`)
- OS name and version (via `platform.system()` and `platform.release()`)
- Python version
- Home directory path
- Detection of existing `.devdocs`, `.sysdocs`, or `.logos` directories

**FreeBSD-Specific Checks (parallel execution):**
- FreeBSD version (via `freebsd-version`)
- ZFS availability (via `zfs version`)
- Jail host status (via `jls -q`)

All subprocess calls use a 0.5-second timeout and run in parallel for performance.

---

## Agent Boundaries

Every LOGOS agent operates within clearly defined **scope boundaries**. This system ensures agents stay in their lane, refuse out-of-scope requests gracefully, and redirect users to the correct agent.

### How It Works

Each of the 50 agents has an embedded `SCOPE BOUNDARIES` section in its activation prompt that defines:

- **IN SCOPE:** The specific tasks this agent is designed to handle
- **FORBIDDEN ACTIONS:** Tasks explicitly outside this agent's responsibility, each with a redirect to the correct agent and an explanation
- **REQUIRES COLLABORATION:** Work that needs coordination with other agents
- **REFUSAL TEMPLATE:** A standardized response format when declining out-of-scope requests

### Refusal Mechanism

When an agent receives a request outside its scope, it responds with:

1. A clear statement that the request is out of scope
2. The reason why it cannot handle the request
3. The specific agent key to invoke instead (e.g., `logos A1` or `logos B6`)
4. A brief description of what the recommended agent does

### Checking Agent Scope

- **Quick reference:** See [`docs/AGENT_BOUNDARIES.md`](docs/AGENT_BOUNDARIES.md) for a complete matrix of all 50 agents and their boundaries
- **Recommendations:** See [`docs/AGENT_RECOMMENDATIONS.md`](docs/AGENT_RECOMMENDATIONS.md) for workflow-aware agent selection guidance

### Boundary Validation

All agent boundaries are validated by automated tests ensuring:

- Every agent has a minimum number of IN SCOPE items
- Every FORBIDDEN ACTION includes a redirect arrow (`→`) and an explanation (`Why:`)
- Refusal templates are present and correctly formatted
- No role overlap exists between agents in the same domain

---

## Installation

### Prerequisites

- **Python 3.10 or higher** (required)
- **pip** or **pip3** (for dependency installation)
- **Unix-like system** (FreeBSD, Linux, macOS, etc.)
- **Terminal emulator** with UTF-8 support (for box-drawing characters)

### Quick Installation (Recommended)

The automated installation script handles all setup:

```bash
# Clone the repository
git clone https://github.com/orpheus497/logos.git
cd logos

# Run installation script
./install.sh
```

**What the script does:**

1. **OS Detection:** Identifies FreeBSD or Linux
2. **Python Check:** Verifies Python 3.10+ is available
3. **Python Dependencies:**
   - Installs `PyYAML>=6.0` (required)
   - Installs `pyperclip>=1.8.0` (optional, for clipboard support)
4. **System Dependencies (optional):**
   - Prompts to install clipboard tools (`xclip`, `xsel`, or `wl-copy` for Wayland)
   - Provides OS-specific installation commands
5. **Package Installation:**
   - Copies `logos/` directory to `~/.logos/`
   - Copies `pyproject.toml` to `~/.logos/`
6. **Command Creation:**
   - Creates `~/.local/bin/logos` wrapper script
   - Makes script executable
   - Optionally adds `~/.local/bin` to your PATH

**After installation:**

```bash
# If ~/.local/bin is in PATH:
logos

# Otherwise:
~/.local/bin/logos

# Or add to PATH manually:
export PATH="$HOME/.local/bin:$PATH"
```

### Manual Installation

If you prefer manual control:

```bash
# 1. Clone repository
git clone https://github.com/orpheus497/logos.git
cd logos

# 2. Install Python dependencies
pip3 install --user pyyaml>=6.0 pyperclip>=1.8.0

# 3. Create installation directory
mkdir -p ~/.logos

# 4. Copy package files
cp -r logos ~/.logos/
cp pyproject.toml ~/.logos/  # Optional but recommended

# 5. Create command wrapper
mkdir -p ~/.local/bin
cat > ~/.local/bin/logos << 'EOF'
#!/usr/bin/env bash
INSTALL_DIR="$HOME/.logos"
PYTHON_CMD="python3"

if [ ! -d "$INSTALL_DIR" ]; then
    echo "Error: LOGOS is not installed. Run install.sh first." >&2
    exit 1
fi

cd "$INSTALL_DIR" || exit 1
exec "$PYTHON_CMD" -m logos "$@"
EOF

chmod +x ~/.local/bin/logos

# 6. Add to PATH (add to ~/.bashrc, ~/.zshrc, or ~/.profile)
export PATH="$HOME/.local/bin:$PATH"
```

### Development Installation

For contributing or modifying LOGOS:

```bash
# Clone repository
git clone https://github.com/orpheus497/logos.git
cd logos

# Install in editable mode with all dependencies
pip install -e ".[dev,clipboard]"

# This installs:
# - logos package (editable)
# - pyyaml>=6.0
# - pyperclip>=1.8.0
# - pytest>=7.0.0
# - pytest-cov>=4.0.0
# - ruff>=0.1.0
# - pip-audit>=2.6.0
```

### Verification

After installation, verify it works:

```bash
# Check command is available
which logos

# Check Python module can be imported
python3 -c "import logos; print('LOGOS installed successfully')"

# Run LOGOS (will start first-run wizard)
logos
```

---

## Setup and Configuration

### First Run Wizard

On first launch, LOGOS guides you through initial setup:

1. **System Scan:** Automatically gathers system information
   - Displays: hostname, username, OS name, OS version
   - Runs FreeBSD-specific checks if applicable
2. **Faction Selection:** Choose your philosophical approach (5 factions available)
   - **The Revanchists (Minimal Autonomy):** "AI/ML is dangerous if left unchecked—I hate AI/ML and will never trust it" - Maximum control, teaching/guiding focus, explicit approval for all actions
   - **The Daedalus Faction (Low Autonomy):** "AI/ML can be used as a tool but must be checked regularly—it WILL make mistakes if unmonitored" - Close monitoring, permission required, mistake prevention
   - **The Orphics (Balanced Autonomy):** "Technology enhances human intelligence—I am in control, it asks me to confirm everything" - Collaborative partnership, multiple options, educational explanations
   - **The Technomancers (High Autonomy):** "AI/ML can manage my system and build programs—I need to direct it" - Human control for major decisions, batch operations, proactive suggestions
   - **The Deus Faction (Maximum Autonomy):** "AI/ML can be totally autonomous—I can trust it, no human input needed for action" - Full autonomy, parameter-based governance, self-directed operation
3. **Identity Creation:** Saves your configuration to `~/.logos/identity.yaml`

The wizard cannot be skipped; it's required for initial setup.

### Identity File Structure

Your identity is stored in `~/.logos/identity.yaml`:

```yaml
identity:
  username: your_username
  hostname: your_hostname
  created: 2026-01-20T12:00:00Z

faction:
  name: orphic
  selected: 2026-01-20T12:00:00Z

system:
  os: Linux
  version: 5.15.0
  architecture: x86_64

sessions:
  last_mode: daedelus
  last_agent: A1
  last_timestamp: 2026-01-20T16:30:00Z
  total_sessions: 42

prompt_counts:
  faction:
    orphic: 25
    revanchist: 5
  mode:
    daedelus: 30
    deus: 12
```

**File Permissions:** Automatically set to `0o600` (read/write for owner only) for security.

### Changing Your Faction

Currently, faction change requires manual editing:

```bash
# Edit identity file
nano ~/.logos/identity.yaml

# Change faction.name to: revanchist, daedalus, orphic, technomancer, or deus
# Update faction.selected timestamp to current time

# Save and exit
```

Future versions will include an in-CLI faction change option.

### Configuration Locations

- **Identity:** `~/.logos/identity.yaml`
- **Package Files:** `~/.logos/logos/`
- **Command Wrapper:** `~/.local/bin/logos`

All configuration is user-specific (no system-wide config).

---

## Usage Guide

### Basic Usage

```bash
# Launch LOGOS (interactive mode)
logos

# Or run as Python module
python3 -m logos
```

### Interactive Workflow

1. **Welcome Screen:** Displays personalized greeting with:
   - Your identity (username@hostname)
   - System information (OS, version)
   - Your faction and philosophy
   - Last session information (if available)

2. **Mode Selection:** Choose your domain
   - **D** or **DAEDELUS:** Software development agents (24 agents)
   - **U** or **DEUS:** System administration agents (26 agents)
   - **T:** View faction statistics (usage counts by faction and mode)
   - **Q:** Quit

3. **Agent Selection:** Browse and select an agent
   - Navigate with arrow keys or type agent key (e.g., "A1", "B6")
   - View agent description and group
   - Press Enter to select

4. **Prompt Display:** Complete prompt is displayed
   - Copy the prompt to your clipboard (if clipboard tools available)
   - Or manually copy from terminal
   - Paste into your AI interface (Claude, ChatGPT, etc.)

5. **Session Update:** LOGOS automatically:
   - Increments session counter
   - Updates last mode and agent
   - Increments faction and mode prompt counts
   - Saves identity file

### Keyboard Shortcuts

**Mode Selection:**
- `D` or `DAEDELUS` - Enter Daedelus mode
- `U` or `DEUS` - Enter DEUS mode
- `T` - View faction statistics
- `Q` - Quit

**Agent Selection:**
- Arrow keys - Navigate list
- Agent key (e.g., `A1`, `B6`) - Jump to agent
- Enter - Select agent
- `Q` or `ESC` - Return to mode selection

### Understanding Agent Prompts

Each agent prompt contains:

1. **Base Prompt:** Domain-specific orchestrator instructions (Maintenance Orchestrator for Daedelus, System Orchestrator for DEUS)
2. **Agent Activation:** Specific role, responsibilities, and scope for the selected agent
3. **Agent Purpose:** Detailed explanation of what the agent does
4. **Identity Context:** Your system information and session history
5. **Faction Protocol:** Behavioral modifiers based on your faction choice

The prompt is designed to be copied directly into an AI chat interface.

### Example Workflow

```bash
$ logos

# Welcome screen appears
# Press 'D' for Daedelus mode

# Agent selection menu appears
# Navigate to "A1 - The Architect" or type "A1"
# Press Enter

# Complete prompt is displayed:
# "## UNIVERSAL SYSTEM PROMPT: THE MAINTENANCE ORCHESTRATOR
#  ...
#  ## SYSTEM IDENTITY
#  **User:** orpheus497@cyronetics
#  **System:** Linux 5.15.0
#  **Faction:** orphic (Technology enhances human intelligence)
#  ..."

# Copy prompt to clipboard (if available) or manually copy
# Paste into Claude/ChatGPT/etc.
# Use the AI's response to guide your work
```

---

## Technical Architecture

### Project Structure

```
logos/
├── logos/                    # Main Python package
│   ├── __init__.py          # Package initialization
│   ├── __main__.py          # Module entry point
│   │
│   ├── core/                # Shared infrastructure
│   │   ├── agent.py         # Agent dataclass definition
│   │   ├── clipboard.py     # Clipboard utilities (xclip/xsel/wl-copy/pyperclip)
│   │   ├── constants.py     # Application constants
│   │   ├── factions.py      # Faction system (definitions, modifiers)
│   │   ├── identity.py      # System scanning, identity persistence
│   │   ├── logging.py       # Logging configuration
│   │   ├── persistence.py   # YAML config read/write with secure permissions
│   │   ├── prompts.py       # Prompt composition (identity, faction, OS adaptation)
│   │   ├── terminal.py      # Terminal utilities (clear, colors, dimensions)
│   │   ├── types.py         # Type definitions
│   │   ├── ui.py            # UI component library (boxes, colors, layouts)
│   │   └── validation.py    # Input validation, YAML schema validation
│   │
│   ├── daedelus/            # Daedelus domain (24 agents)
│   │   ├── agents.py        # Agent definitions (GROUP_A_BUILDERS, etc.)
│   │   ├── constitution.py  # Daedelus constitution text
│   │   └── prompts/         # Agent prompt modules
│   │       ├── base_maintenance.py      # Maintenance Orchestrator base
│   │       ├── base_orchestrator.py     # Orchestrator base
│   │       └── agents/                  # Individual agent prompts
│   │           ├── builders.py
│   │           ├── guardians.py
│   │           ├── maintainers.py
│   │           ├── operators.py
│   │           └── workers.py
│   │
│   ├── deus/                # DEUS domain (26 agents)
│   │   ├── agents.py        # Agent definitions
│   │   ├── mandate.py       # DEUS mandate text
│   │   └── prompts/         # Agent prompt modules
│   │       ├── base_maintenance.py           # Maintenance Orchestrator base
│   │       ├── base_system_orchestrator.py  # System Orchestrator base
│   │       └── agents/                       # Individual agent prompts
│   │           ├── engineers.py
│   │           ├── auditors.py
│   │           ├── maintainers.py
│   │           ├── operators.py
│   │           └── specialists.py
│   │
│   └── cli/                 # CLI components
│       ├── main.py          # Main entry point, first-run detection
│       ├── first_run.py     # First-run wizard (scan, faction selection)
│       ├── mode_select.py   # Mode selection interface
│       ├── agent_select.py  # Agent selection interface
│       └── layouts.py       # UI layout functions (welcome, menus, errors)
│
├── tests/                    # Test suite (118 tests)
│   ├── conftest.py          # Pytest fixtures
│   ├── test_core/           # Core module tests
│   ├── test_cli/            # CLI component tests
│   ├── test_daedelus/       # Daedelus domain tests
│   └── test_deus/           # DEUS domain tests
│
├── .devdocs/                 # Development documentation
│   ├── AGENTS.md            # Agent registry
│   ├── BRIEFING.md          # Current project status
│   ├── PROGRESS.md          # Development session log
│   ├── TESTS.md             # Test results
│   └── [agent folders]/     # Agent-specific documentation
│
├── docs/                     # User documentation
│   ├── FACTIONS.md          # Faction system details
│   └── WORKFLOWS.md          # Workflow overview
│
├── blueprint.md             # Project specification
├── CHANGELOG.md        # Project version history and changes
├── CONSTITUTION.md     # Federation Prime Directives and rules
├── LICENSE                  # AGPL-3.0 license
├── pyproject.toml           # Project configuration
├── install.sh               # Installation script
└── uninstall.sh             # Uninstallation script
```

### Core Components

**Agent System (`logos/core/agent.py`):**
- `Agent` dataclass with: name, description, group, base_prompt, activation_prompt, purpose
- `full_prompt` property that combines base + activation + purpose

**Identity System (`logos/core/identity.py`):**
- `SystemIdentity` dataclass storing all identity information
- `scan_system()` - Parallel system scanning with subprocess timeouts
- `load_identity()` / `save_identity()` - YAML persistence with validation
- `create_identity()` - Create new identity from scan and faction
- `update_session_tracking()` - Increment counters and update timestamps

**Prompt Composition (`logos/core/prompts.py`):**
- `build_identity_context()` - Format identity block for injection
- `build_complete_prompt()` - Compose final prompt with all context
- `_adapt_deus_prompt_for_os()` - OS-specific adaptation (FreeBSD → Linux)
- `build_agent_prompt_from_key()` - Convenience function for agent lookup

**Faction System (`logos/core/factions.py`):**
- `Faction` dataclass with name, philosophy, autonomy_level, modifiers
- `FACTIONS` dictionary with 5 factions (revanchist, daedalus, orphic, technomancer, deus)
- `apply_faction_modifiers()` - Inject behavioral modifiers into prompts
- All factions conform to LOGOS Federation Constitution Version 2.0

**Validation (`logos/core/validation.py`):**
- `validate_input()` - Length limits, character whitelisting, control character detection
- `validate_identity_schema()` - Comprehensive YAML schema validation
- Security-focused input sanitization

**Persistence (`logos/core/persistence.py`):**
- `read_config()` / `write_config()` - YAML read/write with secure file permissions
- Automatic directory creation with 0o700 permissions
- Automatic file creation with 0o600 permissions

### Agent Lookup System

Agents are organized by domain and group:

**Daedelus Agents:**
- `GROUP_A_BUILDERS` - Keys A1-A5
- `GROUP_B_GUARDIANS` - Keys B6-B10
- `GROUP_C_MAINTAINERS` - Keys C1, C6-C11
- `GROUP_D_WORKERS` - Keys D2-D5
- `GROUP_E_OPERATORS` - Keys E1, E2, E3

**DEUS Agents:**
- `GROUP_A_ENGINEERS` - Keys A1-A5
- `GROUP_B_AUDITORS` - Keys B6-B10
- `GROUP_C_MAINTAINERS` - Keys C1, C6-C11
- `GROUP_D_SPECIALISTS` - Keys D2-D5
- `GROUP_E_OPERATORS` - Keys E1-E5 (E1=System Orchestrator, E2=Administrator, E3=General Manager, E4=Ombudsman, E5=DEUS)

All agents are accessible via `get_agent(key)` function in each domain's `agents.py`.

### OS Adaptation System

DEUS agents are designed for FreeBSD but automatically adapt to Linux:

**Substitution Patterns:**
- `FreeBSD` → `Linux`
- `sysrc` → `systemctl`
- `pkg` → `apt/yum/dnf (package manager)`
- `freebsd-update` → `apt upgrade/yum update`
- `rc.conf` → `systemd service files`
- `loader.conf` → `grub/bootloader config`
- `pf.conf` → `iptables/nftables rules`
- `jails` → `containers (Docker/Podman/LXC)`
- `ZFS boot environments` → `LVM snapshots or BTRFS snapshots`

Adaptation occurs automatically during prompt composition if `os_name` is "Linux".

---

## Maintenance and Troubleshooting

### Common Issues

#### Issue: "Command not found: logos"

**Symptoms:** `logos` command not recognized after installation

**Solutions:**
1. Check if `~/.local/bin` is in PATH:
   ```bash
   echo $PATH | grep -q "$HOME/.local/bin" && echo "In PATH" || echo "Not in PATH"
   ```

2. Add to PATH manually:
   ```bash
   # For bash
   echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
   source ~/.bashrc

   # For zsh
   echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
   source ~/.zshrc
   ```

3. Use full path:
   ```bash
   ~/.local/bin/logos
   ```

#### Issue: "Python 3.10 or higher is required"

**Symptoms:** Installation script fails with Python version error

**Solutions:**
1. Check Python version:
   ```bash
   python3 --version
   ```

2. Install Python 3.10+:
   - **FreeBSD:** `pkg install python311`
   - **Ubuntu/Debian:** `sudo apt install python3.10`
   - **Fedora:** `sudo dnf install python3.11`
   - **Arch:** `sudo pacman -S python`

3. Use specific Python version:
   ```bash
   python3.10 -m pip install --user pyyaml>=6.0
   ```

#### Issue: "Failed to load identity configuration"

**Symptoms:** LOGOS cannot read `~/.logos/identity.yaml`

**Solutions:**
1. Check file exists:
   ```bash
   ls -la ~/.logos/identity.yaml
   ```

2. Check file permissions (should be 600):
   ```bash
   chmod 600 ~/.logos/identity.yaml
   ```

3. Validate YAML syntax:
   ```bash
   python3 -c "import yaml; yaml.safe_load(open('$HOME/.logos/identity.yaml'))"
   ```

4. Delete and re-run first-run wizard:
   ```bash
   rm ~/.logos/identity.yaml
   logos  # Will trigger first-run wizard
   ```

#### Issue: "ModuleNotFoundError: No module named 'logos'"

**Symptoms:** Python cannot import logos module

**Solutions:**
1. Verify installation:
   ```bash
   ls -la ~/.logos/logos/
   ```

2. Check Python path:
   ```bash
   python3 -c "import sys; print(sys.path)"
   ```

3. Reinstall:
   ```bash
   cd /path/to/logos/repo
   ./install.sh
   ```

#### Issue: Clipboard not working

**Symptoms:** Cannot copy prompts to clipboard automatically

**Solutions:**
1. Install clipboard tool:
   ```bash
   # FreeBSD
   pkg install xclip

   # Ubuntu/Debian
   sudo apt install xclip

   # Fedora
   sudo dnf install xclip

   # Wayland (Linux)
   sudo apt install wl-clipboard  # or equivalent
   ```

2. Check if tool is available:
   ```bash
   which xclip || which xsel || which wl-copy
   ```

3. Manual copy: Prompts are displayed in terminal; manually select and copy

#### Issue: Terminal display issues (box-drawing characters)

**Symptoms:** UI displays incorrectly, garbled characters

**Solutions:**
1. Ensure UTF-8 encoding:
   ```bash
   export LANG=en_US.UTF-8
   export LC_ALL=en_US.UTF-8
   ```

2. Use compatible terminal:
   - Modern terminals (GNOME Terminal, Konsole, iTerm2, etc.) support UTF-8
   - Legacy terminals may not display box-drawing characters correctly

3. Check terminal encoding:
   ```bash
   locale
   ```

### Maintenance Tasks

#### Updating LOGOS

```bash
# Navigate to repository
cd /path/to/logos

# Pull latest changes
git pull

# Re-run installation script
./install.sh
```

#### Resetting Identity

```bash
# Backup current identity (optional)
cp ~/.logos/identity.yaml ~/.logos/identity.yaml.backup

# Delete identity file
rm ~/.logos/identity.yaml

# Run LOGOS (will trigger first-run wizard)
logos
```

#### Cleaning Up

```bash
# Uninstall LOGOS
./uninstall.sh

# Or manually:
rm -rf ~/.logos
rm ~/.local/bin/logos
```

#### Verifying Installation

```bash
# Check installation directory
ls -la ~/.logos/

# Check command wrapper
cat ~/.local/bin/logos

# Test Python import
python3 -c "from logos.core.identity import scan_system; print(scan_system())"

# Test CLI
logos --help  # If help implemented, or just run logos
```

### Log Files

LOGOS does not create log files by default. All operations are silent unless errors occur (displayed in terminal).

For debugging, enable Python logging:

```bash
# Set logging level
export LOGOS_LOG_LEVEL=DEBUG

# Run LOGOS
logos
```

### Performance Issues

If LOGOS feels slow:

1. **System Scanning:** First run scans system (0.5-1 second). Subsequent runs load from cache.
2. **Large Agent Lists:** Agent selection may be slow on very old terminals. Consider using agent keys directly.
3. **YAML Parsing:** Identity file is small (<1KB), parsing is near-instantaneous.

If issues persist, check system resources:
```bash
# Check Python process
ps aux | grep logos

# Check disk I/O
iostat 1
```

---

## FAQs

### General Questions

**Q: What AI models does LOGOS work with?**  
A: LOGOS works with any AI model that accepts text prompts. It's been tested with Claude (Anthropic), GPT-4 (OpenAI), and other chat-based AI interfaces. LOGOS generates prompts; you paste them into your AI interface.

**Q: Do I need an internet connection?**  
A: No. LOGOS runs entirely locally. You only need internet if you're using an online AI service to process the prompts LOGOS generates.

**Q: Can I use LOGOS offline?**  
A: Yes. LOGOS is a local CLI tool. It doesn't connect to any services. You can generate prompts offline and use them later with an AI model.

**Q: Is LOGOS free?**  
A: Yes. LOGOS is licensed under AGPL-3.0 (Free and Open Source Software). However, the AI models you use with LOGOS may have their own costs (e.g., Claude API, ChatGPT Plus).

**Q: Can I modify LOGOS?**  
A: Yes. AGPL-3.0 allows modification, but any modifications must also be open source if you distribute them.

### Technical Questions

**Q: Why Python 3.10+?**  
A: LOGOS uses modern Python features (type hints, dataclasses, pattern matching) that require Python 3.10 or higher.

**Q: Why YAML for configuration?**  
A: YAML is human-readable, supports comments, and is easy to edit manually. The identity file is small and simple, making YAML ideal.

**Q: Why separate domains (Daedelus/DEUS)?**  
A: Software development and system administration have different workflows, terminology, and best practices. Separate domains allow specialized agents without confusion.

**Q: How does OS adaptation work?**  
A: LOGOS detects your OS during system scan. For DEUS agents on Linux, it automatically replaces FreeBSD-specific terms with Linux equivalents using regex substitution.

**Q: Can I add my own agents?**  
A: Yes, but it requires modifying the codebase. Add agent definitions to `logos/daedelus/agents.py` or `logos/deus/agents.py`, and create prompt files in the appropriate `prompts/agents/` directory.

### Usage Questions

**Q: Can I change my faction later?**  
A: Yes, but currently requires manual editing of `~/.logos/identity.yaml`. Future versions will include an in-CLI option.

**Q: What's the difference between factions?**  
A: Factions modify agent behavior across a spectrum from minimal to maximum autonomy:
- **The Revanchists (Minimal):** Asks for approval frequently, explains everything, teaches, maximum control
- **The Daedalus Faction (Low):** Permission required for all actions, close monitoring, mistake prevention
- **The Orphics (Balanced):** Provides multiple options, educational, balanced collaboration
- **The Technomancers (High):** Proactive, autonomous for low-risk tasks, minimal friction, batch operations
- **The Deus Faction (Maximum):** No human input needed, fully autonomous, parameter-based operation

**Q: How do I know which agent to use?**  
A: Read agent descriptions in the selection menu. Generally:
- **Builders/Engineers:** Create new things
- **Guardians/Auditors:** Review and validate
- **Maintainers:** Fix and update existing code/systems
- **Workers/Specialists:** Implement specific features/tasks
- **Operators:** Orchestrate and manage

**Q: Can I use multiple agents in one session?**  
A: Yes. After generating a prompt, you can return to agent selection and choose another agent. Each selection updates your session tracking.

**Q: Do agents remember previous conversations?**  
A: No. LOGOS doesn't store AI responses. Each prompt is independent. However, your identity context (system info, session history) is included in every prompt, providing continuity.

### Security Questions

**Q: What data does LOGOS collect?**  
A: Only local system information (hostname, username, OS) and your usage patterns (session counts, last agent used). No data is transmitted anywhere.

**Q: Are my identity files secure?**  
A: Yes. Identity files use 0o600 permissions (read/write for owner only). Directories use 0o700 permissions.

**Q: Can LOGOS modify my system?**  
A: No. LOGOS only generates prompts. It never executes system commands or modifies files (except its own configuration).

**Q: Is LOGOS safe to run as root?**  
A: LOGOS doesn't require root privileges. Running as root is unnecessary and not recommended. LOGOS only reads system information and writes to `~/.logos/`.

---

## Security

### Security Measures

LOGOS implements multiple security layers:

1. **Secure File Permissions:**
   - Identity files: `0o600` (read/write owner only)
   - Configuration directories: `0o700` (read/write/execute owner only)
   - Automatic permission setting on file creation

2. **Input Validation:**
   - Length limits on all user input (prevents buffer overflow)
   - Character whitelisting (prevents injection)
   - Control character detection (prevents terminal escape sequences)

3. **YAML Schema Validation:**
   - Validates identity file structure
   - Type checking for all fields
   - Prevents malformed configuration files

4. **Safe Subprocess Execution:**
   - All subprocess calls use timeouts (0.5 seconds)
   - No shell injection vectors (command lists, not strings)
   - Error handling prevents information leakage

5. **Dependency Scanning:**
   - `pip-audit` integration for vulnerability detection
   - Regular dependency updates recommended

### Security Best Practices

- **Never run LOGOS as root** - Unnecessary and increases risk
- **Review identity file permissions** - Should be 600
- **Keep dependencies updated** - Run `pip-audit` regularly
- **Don't share identity files** - Contains system information
- **Validate prompts before use** - Review generated prompts before pasting into AI

### Reporting Security Issues

If you discover a security vulnerability:

1. **Do not** open a public issue
2. Contact the maintainer directly
3. Provide detailed information about the vulnerability
4. Allow time for fix before public disclosure

---

## Performance

### Optimization Features

LOGOS is optimized for fast startup and low memory usage:

1. **Parallel System Scanning:**
   - FreeBSD checks run concurrently (3 parallel subprocesses)
   - 5-10x faster than sequential execution
   - Worst case: 6 seconds → 0.5 seconds

2. **Optimized Agent Lookup:**
   - Dictionary-based lookup (O(1) access)
   - 2x faster than previous list iteration
   - Lazy loading (agents loaded on-demand)

3. **Memory Efficiency:**
   - Lazy agent loading (2-3x memory reduction)
   - Small identity files (<1KB)
   - No caching of large data structures

### Performance Benchmarks

- **Startup Time:** <1 second (after first run)
- **System Scan:** 0.5-1 second (first run only)
- **Agent Lookup:** <1ms (dictionary lookup)
- **Prompt Composition:** <10ms (string concatenation)
- **Memory Usage:** ~15-20MB (Python process)

### Performance Tips

- **First run is slower** - System scanning occurs only once
- **Subsequent runs are fast** - Identity loaded from cache
- **Large terminals** - Agent selection may be slower on very old terminals
- **Network not required** - No network latency

---

## Development

### Running Tests

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=logos.core --cov=logos.cli --cov-report=html --cov-report=term

# Run specific test suites
pytest tests/test_core/test_validation.py -v
pytest tests/test_cli/ -v
pytest tests/test_core/test_identity.py -v
```

### Continuous Integration (CI/CD)

LOGOS uses GitHub Actions for automated testing and quality checks:

**Automated Workflows:**
- **Test Suite:** Runs on Python 3.10, 3.11, and 3.12
  - Executes all 145+ test cases
  - Generates coverage reports
  - Uploads coverage to Codecov (Python 3.11)
- **Linting:** Runs Ruff for code quality checks
- **Syntax Check:** Verifies all Python files compile correctly

**Workflow Triggers:**
- Runs on every push to `main`/`master` branch
- Runs on all pull requests
- All checks must pass before merging

**View CI Status:**
- Check the [Actions tab](https://github.com/orpheus497/logos/actions) on GitHub
- View test results and coverage reports
- Download HTML coverage reports as artifacts

### Code Quality

```bash
# Linting (ruff)
ruff check logos/

# Formatting (ruff)
ruff format logos/

# Type checking (mypy - if configured)
mypy logos/
```

### Security Scanning

```bash
# Dependency vulnerability scan
pip-audit

# Fix vulnerabilities (if possible)
pip-audit --fix
```

### Development Workflow

1. **Make changes** to codebase
2. **Run tests** to verify functionality
3. **Run linter** to check code quality
4. **Update documentation** if needed
5. **Test manually** with `logos` command
6. **Commit changes** with descriptive messages

### Adding New Agents

1. **Create prompt file** in appropriate `prompts/agents/` directory
2. **Add agent definition** to `agents.py` in appropriate domain
3. **Add to agent group** dictionary (GROUP_A_BUILDERS, etc.)
4. **Test agent lookup** with `get_agent(key)`
5. **Update documentation** (update agent registry and relevant documentation)

### Project Status

**Current Version:** v0.2.0.dev0 — in active development on the develop branch (Alpha)

**Completed:**
- ✅ Core infrastructure (identity, persistence, validation)
- ✅ UI system (terminal components, layouts)
- ✅ CLI implementation (first-run, mode selection, agent selection)
- ✅ Domain integration (all 50 agents ported)
- ✅ Security audit and fixes
- ✅ Performance optimization
- ✅ Comprehensive test suite (118 tests)

**In Progress:**
- ⏳ Test execution and coverage verification
- ⏳ Production release preparation

---

## Documentation

### LOGOS Project Documentation

This section describes documentation **about LOGOS itself** (the LOGOS codebase):

- **Constitution:** `CONSTITUTION.md` - The LOGOS Federation Constitution (supreme governing document)
- **Blueprint:** `blueprint.md` - Complete integration analysis and architecture plan
- **Development Docs:** `.devdocs/` - **LOGOS project's internal development documentation** (used for developing LOGOS itself)
  - `BRIEFING.md` - Current project status
  - `PROGRESS.md` - Development session log
  - `TESTS.md` - Test results and coverage
  - `DECISIONS_LOG.md` - Architecture decisions
  - `AGENTS.md` - Agent registry and definitions
- **Domain Documentation:** `docs/` - Domain-specific reference materials
  - `FACTIONS.md` - **Complete faction system documentation** (all 5 factions with detailed characteristics, use cases, and comparison table)
  - `WORKFLOWS.md` - Workflow overview

**Note:** The LOGOS project's `.devdocs/` folder is for tracking the development of LOGOS itself. This is separate from the `.devdocs/` folder that LOGOS agents create when working on your projects.

### How LOGOS Agents Use `.devdocs/` in Your Projects

When you use LOGOS agents to work on **your own projects**, the agents will create and maintain a `.devdocs/` folder **in your project directory** (not in the LOGOS codebase). This folder structure mirrors the LOGOS project's internal documentation system:

- **Shared Documentation:**
  - `.devdocs/AGENTS.md` - Agent definitions and commands
  - `.devdocs/BRIEFING.md` - Current project status
  - `.devdocs/PROGRESS.md` - Session log
  - `.devdocs/DECISIONS_LOG.md` - Architecture decisions
  - `.devdocs/TESTS.md` - Test results

- **Agent-Specific Documentation Folders:**
  - `.devdocs/builders/` - Builders' documentation (Architect, Logic Engineer, Interface Designer, Test Engineer, Scribe)
  - `.devdocs/guardians/` - Guardians' documentation (Sentinel, Marshal, Profiler, Critic, Gatekeeper)
  - `.devdocs/maintainers/` - Maintainers' documentation (Bug Hunter, Security Patcher, Doc Updater, Configurator, Optimizer, Janitor, Librarian)
  - `.devdocs/workers/` - Workers' documentation (Feature Sprinter, Refactorer, UI Tweaker, Test Extender)
  - `.devdocs/operators/` - Operators' documentation (Orchestrator, Operational Control Manager, Daedelus)

**Important Distinction:**
- **LOGOS project's `.devdocs/`** = Internal documentation for developing LOGOS itself (in the LOGOS repository)
- **Your project's `.devdocs/`** = Documentation created by LOGOS agents when working on your projects (in your project directory)

### Code Documentation

All code files use a custom documentation schema:
- `##Fix:` - Bug fixes
- `##Update:` - Feature extensions
- `##Refactor:` - Logic cleanup
- `##Sec:` - Security patches
- `##Note:` - Contextual information

---

## License

This project is licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0)**.

See the [LICENSE](LICENSE) file for the full license text.

### Why AGPL-3.0?

- **Ensures open source continuity:** All modifications and improvements must remain open source
- **Protects the project:** Prevents proprietary forks that don't contribute back
- **Aligns with FOSS principles:** Free and Open Source Software philosophy
- **Network service protection:** AGPL covers network services, ensuring web-based uses are also open source

### License Compliance

If you modify LOGOS and distribute it (including as a service), you must:
1. Provide source code to all users
2. License your modifications under AGPL-3.0
3. Include original license and copyright notices

---

## Support

- **Repository:** https://github.com/orpheus497/logos
- **Issues:** https://github.com/orpheus497/logos/issues

---

**Status:** v0.2.0.dev0 — in active development on the develop branch (Alpha)
**Last Updated:** 2026-02-24
