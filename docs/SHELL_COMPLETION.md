# Shell Completion Guide

LOGOS provides tab completion scripts for **Bash**, **Zsh**, and **Fish** shells.

## Quick Install

Run the installer script from the LOGOS root directory:

```bash
# Install for current shell (auto-detected)
./install-completion.sh

# Install for a specific shell
./install-completion.sh --bash
./install-completion.sh --zsh
./install-completion.sh --fish

# Install for all detected shells
./install-completion.sh --all
```

## Manual Installation

### Bash

Copy the completion script to your completions directory:

```bash
# System-wide (requires root/sudo)
sudo cp completions/bash/logos /etc/bash_completion.d/logos

# User-level
mkdir -p ~/.local/share/bash-completion/completions
cp completions/bash/logos ~/.local/share/bash-completion/completions/logos
```

Reload completions:

```bash
source ~/.local/share/bash-completion/completions/logos
```

### Zsh

Copy the completion script to a directory in your `fpath`:

```bash
# System-wide (requires root/sudo)
sudo cp completions/zsh/_logos /usr/local/share/zsh/site-functions/_logos

# User-level
mkdir -p ~/.zsh/completions
cp completions/zsh/_logos ~/.zsh/completions/_logos
```

Ensure the directory is in your `fpath` (add to `~/.zshrc`):

```zsh
fpath=(~/.zsh/completions $fpath)
autoload -Uz compinit && compinit
```

### Fish

Copy the completion script to Fish's completions directory:

```bash
mkdir -p ~/.config/fish/completions
cp completions/fish/logos.fish ~/.config/fish/completions/logos.fish
```

Fish completions are loaded automatically on the next session.

## What Completions Provide

The completion scripts support:

- **Mode selection:** `logos --mode daedelus` / `logos --mode deus`
- **Agent keys:** Tab-complete agent identifiers (A1–A5, B6–B10, C1, C6–C11, D2–D5, E1–E5)
- **Agent aliases:** Complete built-in aliases (e.g., `architect`, `kernel`, `sentinel`)
- **CLI flags:** `--verbose` / `-v`, `--quiet` / `-q`, `--version`, `--help`

## Completion Script Locations

| Shell | Source File |
|-------|-----------|
| Bash  | `completions/bash/logos` |
| Zsh   | `completions/zsh/_logos` |
| Fish  | `completions/fish/logos.fish` |

## Troubleshooting

### Completions not working after install

1. **Bash:** Run `source ~/.local/share/bash-completion/completions/logos` or open a new terminal
2. **Zsh:** Run `autoload -Uz compinit && compinit` or open a new terminal
3. **Fish:** Open a new Fish session

### Permission issues

If installing system-wide, use `sudo` with the install commands. User-level installation does not require elevated privileges.

### Verifying installation

```bash
# Bash/Zsh: Check if completion function is loaded
type _logos 2>/dev/null && echo "Completion loaded" || echo "Not loaded"

# Fish: Check if completion file exists
test -f ~/.config/fish/completions/logos.fish && echo "Installed" || echo "Not found"
```

---

See also: [CLI Usage Guide](CLI_USAGE.md)
