# LOGOS CLI Usage Guide

## Overview

LOGOS is a unified AI agent federation that prepares context-rich prompts for AI models.
The CLI provides an interactive interface for selecting agents, composing prompts, and
copying them to your clipboard for use with AI assistants.

## Quick Start

```bash
# Run LOGOS
logos

# Run with verbose output
logos -v

# Run with minimal output
logos -q

# Show version
logos --version

# Or run as Python module
python -m logos
```

On first run, LOGOS will:
1. Scan your system for identity context (OS, hostname, username)
2. Ask you to select a philosophical faction
3. Save your identity to `~/.logos/identity.yaml`

## Modes

LOGOS offers two operational modes:

| Mode | Domain | Agents | Focus |
|------|--------|--------|-------|
| **Daedelus** | Software Development | 24 | Code creation, review, maintenance |
| **DEUS** | System Administration | 26 | FreeBSD/Linux system management |

## Agent Selection

### By Key

Each agent has a unique key (e.g., `A1`, `B6`, `E1`). Enter the key directly:

```
Your choice: A1
```

### By Alias

Agents can also be selected by memorable alias names:

```
Your choice: architect     → A1 (The Architect)
Your choice: security      → B6 (The Sentinel / Security Auditor)
Your choice: orchestrator  → E1 (The Orchestrator)
```

### Daedelus Aliases

| Alias | Key | Agent |
|-------|-----|-------|
| `architect` | A1 | The Architect |
| `logic` | A2 | The Logic Engineer |
| `interface` | A3 | The Interface Designer |
| `test-engineer` | A4 | The Test Engineer |
| `scribe` | A5 | The Scribe |
| `sentinel`, `security` | B6 | The Sentinel |
| `marshal` | B7 | The Marshal |
| `profiler` | B8 | The Profiler |
| `critic` | B9 | The Critic |
| `gatekeeper` | B10 | The Gatekeeper |
| `bughunter`, `bugfix` | C1 | The Bug Hunter |
| `secpatch` | C6 | The Security Patcher |
| `docupdate` | C7 | The Doc Updater |
| `configurator` | C8 | The Configurator |
| `optimizer` | C9 | The Optimizer |
| `janitor` | C10 | The Janitor |
| `librarian` | C11 | The Librarian |
| `sprinter`, `feature` | D2 | The Feature Sprinter |
| `refactor` | D3 | The Refactorer |
| `uitweak` | D4 | The UI Tweaker |
| `testextend` | D5 | The Test Extender |
| `orchestrator` | E1 | The Orchestrator |
| `ocm` | E2 | The Operational Control Manager |
| `daedelus` | E3 | Daedelus |

### DEUS Aliases

| Alias | Key | Agent |
|-------|-----|-------|
| `kernel` | A1 | The Kernel Architect |
| `driver` | A2 | The Driver Engineer |
| `network` | A3 | The Network Architect |
| `boot` | A4 | The Boot Engineer |
| `service` | A5 | The Service Scribe |
| `secaudit`, `audit` | B6 | The Security Auditor |
| `syntax` | B7 | The Syntax Marshal |
| `perf` | B8 | The Performance Analyst |
| `compliance` | B9 | The Compliance Critic |
| `release` | B10 | The Release Gatekeeper |
| `bughunter`, `bugfix` | C1 | The Bug Hunter |
| `secpatch` | C6 | The Security Patcher |
| `manual` | C7 | The Manual Keeper |
| `sysctl` | C8 | The Sysctl Tuner |
| `optimizer` | C9 | The Optimizer |
| `janitor` | C10 | The System Janitor |
| `portlib` | C11 | The Port Librarian |
| `portbuild` | D2 | The Port Builder |
| `compat` | D3 | The Compatibility Engineer |
| `jail` | D4 | The Jail Architect |
| `zfs` | D5 | The ZFS Engineer |
| `orchestrator` | E1 | The System Orchestrator |
| `admin` | E2 | The Administrator |
| `manager` | E3 | The General Manager |
| `ombudsman` | E4 | The Ombudsman |
| `deus` | E5 | DEUS |

## Configuration

LOGOS supports user-level configuration via `~/.logos/config.yaml`.

### Default Configuration

```yaml
# Default mode (null = ask each time, "daedelus" or "deus")
# Reserved for future use
default_mode: null

# Clipboard settings
clipboard:
  enabled: true          # Auto-copy prompts to clipboard
  show_preview: false    # Show prompt preview before copying
  preview_lines: 10      # Lines to show in preview (first + last)

# Recent agents tracking
recent_agents:
  enabled: true          # Track recent selections
  max_count: 10          # Maximum tracked agents

# Custom aliases (user-defined)
aliases:
  # Example: arch: A1
  # Example: sec: B6
```

### Custom Aliases

Add custom aliases in your config file:

```yaml
aliases:
  arch: A1
  sec: B6
  orch: E1
  k: A1        # Short alias for kernel (DEUS)
```

Custom aliases take precedence over built-in aliases.

## Shell Completion

LOGOS provides shell completion scripts for Bash, Zsh, and Fish.
See [SHELL_COMPLETION.md](SHELL_COMPLETION.md) for detailed installation instructions.

### Quick Install

```bash
# Auto-detect and install for current shell
./install-completion.sh

# Install for all detected shells
./install-completion.sh --all
```

### Manual Installation

#### Bash

```bash
# Add to ~/.bashrc
source /path/to/logos/completions/bash/logos
```

### Zsh

```bash
# Copy to a directory in your $fpath
cp /path/to/logos/completions/zsh/_logos ~/.zsh/completions/
# Add to ~/.zshrc (if not already set)
fpath=(~/.zsh/completions $fpath)
autoload -Uz compinit && compinit
```

### Fish

```bash
# Copy to Fish completions directory
cp /path/to/logos/completions/fish/logos.fish ~/.config/fish/completions/
```

## Recent Agents

LOGOS tracks your last 10 agent selections across all modes in a single, shared
list. Each entry is qualified with its mode (for example `daedelus:A1` or
`deus:A1`) and stored in your identity file at `~/.logos/identity.yaml`.

## Navigation

| Key | Action |
|-----|--------|
| `0`, `Q`, `QUIT` | Go back / Exit |
| `F` | Change faction |
| `I` | View system info |
| `S` | View usage statistics |
| Agent key or alias | Select agent |
| `/search_term` | Search agents by name, key, or description |

## Agent Search

Use the `/` prefix during agent selection to search across all agents by name, key, alias, or description:

```
Your choice: /security     → Lists all security-related agents
Your choice: /architect    → Lists agents matching "architect"
Your choice: /opt          → Lists agents matching "opt" (e.g., Optimizer)
```

Search is case-insensitive and matches partial strings.

## Command-Line Flags

| Flag | Short | Description |
|------|-------|-------------|
| `--verbose` | `-v` | Verbose output: shows agent metadata, prompt stats (char/line count), and auto-enables prompt preview |
| `--quiet` | `-q` | Quiet output: suppresses banners and decorative elements |
| `--version` | | Shows LOGOS version and exits |
| `--help` | `-h` | Shows help message and exits |

The `-v` and `-q` flags are mutually exclusive.

## Prompt Preview

Enable prompt preview in your config to see prompt content before clipboard copy:

```yaml
clipboard:
  show_preview: true
  preview_lines: 10    # Shows first 5 + last 5 lines
```

## Files

| Path | Purpose |
|------|---------|
| `~/.logos/identity.yaml` | User identity and session tracking |
| `~/.logos/config.yaml` | User preferences and custom aliases |

## Troubleshooting

### Clipboard Not Working

LOGOS tries multiple clipboard methods in order:
1. `wl-copy` (Wayland)
2. `xclip` (X11)
3. `xsel` (X11)
4. `pyperclip` (Python library)

If clipboard fails, the prompt is displayed on screen for manual copying.

Install a clipboard tool:
```bash
# Debian/Ubuntu
sudo apt install xclip

# FreeBSD
sudo pkg install xclip

# Or install pyperclip
pip install pyperclip
```

### Reset Identity

To reset your LOGOS identity and start fresh:
```bash
rm ~/.logos/identity.yaml
logos  # Will trigger first-run wizard
```
