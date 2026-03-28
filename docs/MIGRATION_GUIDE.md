# LOGOS Migration Guide: v0.1.0 → v0.2.0

## Overview

LOGOS v0.2.0 is a fully backward-compatible release. All changes are additive — no
existing functionality has been removed or altered in a breaking way. This guide covers
the new features introduced in v0.2.0 and how to take advantage of them.

---

## What's Changed

| Area | v0.1.0 | v0.2.0 |
|---|---|---|
| Agent boundaries | None | All 50 agents have explicit scope boundaries |
| `.devdocs/` governance | None | Temporal logs, bloat prevention, archival |
| Workflow coordination | Ad-hoc | END-OF-TASK protocol, 3 workflow patterns |
| OS adaptations | FreeBSD only | Linux + FreeBSD per-agent instructions |
| Configuration | None | `~/.logos/config.yaml` (auto-created) |
| Agent aliases | None | 50 built-in + custom aliases |
| Shell completions | None | Bash, Zsh, Fish |
| CLI flags | None | `-v`, `-q`, `--version` |
| Constitution | Articles I–V | Articles I–XI |
| Search/filter | None | `/` prefix to search agents |

---

## No Migration Required

The following features are entirely new and require no changes to existing workflows:

- **Agent boundary enforcement** — Agents now have explicit scope rules. Existing prompts
  continue to work; boundaries are enforced within the prompt content itself.
- **Workflow coordination** — The END-OF-TASK protocol is embedded in agent prompts.
  No user action is needed.
- **OS adaptations** — Linux and FreeBSD instructions are automatically included in DEUS
  agent prompts based on your detected operating system.
- **Constitution Articles VI–XI** — These govern agent behavior internally and do not
  require user interaction.

---

## New Features to Enable

### Configuration File

LOGOS v0.2.0 introduces a user-level configuration file at `~/.logos/config.yaml`.

- **Auto-created:** The file is created automatically on first run with sensible defaults.
- **No action required:** If you do not need to customize behavior, ignore this file.
- **To customize:** Edit `~/.logos/config.yaml` to change settings such as:
  - Default mode (Daedelus or DEUS)
  - Prompt preview length
  - Custom agent aliases
  - Quiet/verbose defaults

```yaml
# Example ~/.logos/config.yaml
default_mode: daedelus
prompt_preview: true
preview_lines: 5
quiet: false
verbose: false
```

### Shell Completions

Tab completion is now available for Bash, Zsh, and Fish shells.

To install:

```bash
# Auto-detect your shell and install
./install-completion.sh

# Or install for a specific shell
./install-completion.sh bash
./install-completion.sh zsh
./install-completion.sh fish
```

After installation, restart your shell or source the completion file:

```bash
# Bash
source ~/.bash_completion.d/logos

# Zsh
source ~/.zsh/completions/_logos

# Fish (automatic)
```

See [docs/SHELL_COMPLETION.md](SHELL_COMPLETION.md) for full details.

### Agent Aliases

All 50 agents now have human-friendly aliases. Use them in agent selection:

```
# Instead of selecting "A1" you can type:
architect        → Daedelus A1 (The Architect)
kernel           → DEUS A1 (The Kernel Architect)
sentinel         → Daedelus B6 (The Sentinel)
orchestrator     → Daedelus E1 (The Orchestrator)
```

Custom aliases can be defined in `~/.logos/config.yaml`:

```yaml
aliases:
  mybuilder: "daedelus:A1"
  myauditor: "deus:B6"
```

### CLI Flags

New command-line flags are available:

```bash
# Verbose mode — shows agent metadata and prompt statistics
logos -v

# Quiet mode — suppresses banners and decorative output
logos -q

# Show version
logos --version
```

### .devdocs Governance System

The `.devdocs/` system is new in v0.2.0. It provides a governed workspace for
development state tracking, temporal logs, and project documentation.

- **Auto-initialized:** Running `logos` in a project directory will detect and
  initialize `.devdocs/` if not present.
- **No action required:** The system works automatically through orchestrator agents.
- **Structure:** See `templates/.devdocs/README.md` for the expected directory layout.

### Agent Search and Filter

In agent selection, type `/` followed by a search term to filter agents:

```
Select agent: /security
```

This searches agent names, keys, aliases, and descriptions.

---

## Constitution Updates

LOGOS v0.2.0 adds six new articles to the Constitution:

| Article | Title | Phase |
|---|---|---|
| VI | Agent Scope Boundaries and Enforcement | 1 |
| VII | .devdocs Governance | 2 |
| VIII | Workflow Coordination Protocol | 3 |
| IX | Operating System Adaptations | 4 |
| X | User Experience and CLI Standards | 5 |
| XI | Documentation Standards and Ownership | 6 |

These articles govern internal agent behavior and do not require user action.

---

## Step-by-Step Upgrade Procedure

1. **Update the codebase:**

   ```bash
   git pull origin main
   # Or if installed via pip:
   pip install --upgrade logos
   ```

2. **Verify the version:**

   ```bash
   logos --version
   # Expected: logos 0.2.0
   ```

3. **Run LOGOS to auto-initialize new features:**

   ```bash
   logos
   ```

   This will:
   - Create `~/.logos/config.yaml` if it does not exist
   - Detect and initialize `.devdocs/` in the current project directory

4. **(Optional) Install shell completions:**

   ```bash
   ./install-completion.sh
   ```

5. **(Optional) Customize configuration:**

   ```bash
   # Edit with your preferred editor
   nano ~/.logos/config.yaml
   ```

6. **Verify everything works:**

   ```bash
   # Run the test suite
   pytest tests/
   ```

---

## Compatibility Notes

- **Python:** Requires Python 3.10 or higher (unchanged from v0.1.0)
- **Dependencies:** `pyyaml>=6.0` and `wcwidth>=0.2.0` (unchanged)
- **Identity files:** Existing `~/.logos/identity.yaml` files are fully compatible
- **Agent prompts:** All v0.1.0 prompts continue to work; new boundary and OS sections
  are additive

---

## Troubleshooting

| Issue | Solution |
|---|---|
| `config.yaml` not created | Run `logos` once — it auto-creates on first use |
| Shell completions not working | Re-run `./install-completion.sh` and restart your shell |
| Agent alias not recognized | Check spelling; see `docs/CLI_USAGE.md` for the full alias list |
| `.devdocs/` not initialized | Ensure you are in a project root directory when running `logos` |
| Invalid YAML in config | Delete `~/.logos/config.yaml` and re-run `logos` to regenerate defaults |

For additional help, see [docs/CLI_USAGE.md](CLI_USAGE.md) or open an issue on
[GitHub](https://github.com/orpheus497/logos/issues).

---

**For The LOGOS Federation**
**For Human Empowerment**
**For Excellence and Quality**
