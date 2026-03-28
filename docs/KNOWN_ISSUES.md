# LOGOS Known Issues

**Version:** 0.2.0
**Last Updated:** TBD

---

## Interactive Navigation

**Arrow-key navigation is not yet implemented.**

The agent selection interface currently uses `input()` prompts for navigation.
Arrow-key interactive navigation (e.g., using `blessed` or `curses`) is planned
for a future release. Users select agents by typing the agent key, alias, or
search term.

**Workaround:** Use the `/` search prefix to quickly filter agents by name,
key, alias, or description.

---

## Clipboard Integration

**Clipboard requires external tools on Linux and FreeBSD.**

LOGOS uses system clipboard tools to copy composed prompts. The following tools
are supported:

| Platform | Supported Tools |
|---|---|
| Linux (X11) | `xclip`, `xsel` |
| Linux (Wayland) | `wl-copy` |
| FreeBSD | `xclip`, `xsel` |
| macOS | `pbcopy` (built-in) |

If none of these tools are installed, clipboard copy will fail silently and
the prompt will be displayed for manual copying.

**`pyperclip` is optional.** Install it for cross-platform clipboard support:

```bash
pip install logos[clipboard]
# Or directly:
pip install pyperclip
```

If `pyperclip` is not installed, LOGOS falls back to the system clipboard tools
listed above.

---

## Shell Completions

**Shell completions require manual installation.**

Tab completions for Bash, Zsh, and Fish are included but not installed
automatically. Run the installer to enable them:

```bash
./install-completion.sh
```

After installation, restart your shell or source the completion file for
changes to take effect. See [SHELL_COMPLETION.md](SHELL_COMPLETION.md) for
detailed instructions.

---

## Configuration File

**Invalid YAML in the configuration file causes a silent fallback to defaults.**

The user configuration file at `~/.logos/config.yaml` must be valid YAML.
If the file contains syntax errors or is unreadable, LOGOS silently falls back
to built-in default values for that session. The file is **not** automatically
overwritten or regenerated.

**Workaround:** Use a YAML linter or validator before editing the config file.
To reset the configuration, delete the file and recreate it manually:

```bash
rm ~/.logos/config.yaml
# Then create a fresh config (see docs/MIGRATION_GUIDE.md for the schema)
```

---

## .devdocs Governance

**The `.devdocs/` folder must be at the project root for governance to work.**

The `.devdocs/` governance system expects the folder to be located at the root
of the project directory (the same level as `pyproject.toml` or `.git/`).
Placing `.devdocs/` in a subdirectory is not supported and will not be detected
by the temporal log management or bloat prevention systems.

**Workaround:** Always initialize `.devdocs/` from the project root:

```bash
cd /path/to/your/project
logos
```

---

## Reporting Issues

If you encounter an issue not listed here, please open a report on
[GitHub Issues](https://github.com/orpheus497/logos/issues) with:

1. Your Python version (`python --version`)
2. Your OS and version
3. Steps to reproduce the issue
4. Expected vs actual behavior
5. Any error messages or tracebacks

---

**For The LOGOS Federation**
**For Human Empowerment**
**For Excellence and Quality**
