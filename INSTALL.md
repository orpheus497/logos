# LOGOS Installation Guide

## Overview

LOGOS can be installed as a system package using the automated installation script, which handles all dependencies and configuration automatically.

## Quick Installation

```bash
git clone https://github.com/orpheus497/logos.git
cd logos
./install.sh
```

That's it! The script will:
1. Detect your OS (FreeBSD or Linux)
2. Verify Python 3.10+ is installed
3. Install Python dependencies (PyYAML, pyperclip)
4. Install system clipboard tools (xclip/xsel/wl-copy) if needed
5. Install LOGOS to `~/.logos`
6. Create `logos` command in `~/.local/bin`
7. Configure PATH if needed

## Installation Details

### Directory Structure

After installation:
```
~/.logos/
  └── logos/          # LOGOS package
      ├── __init__.py
      ├── __main__.py
      ├── core/
      ├── cli/
      ├── daedelus/
      └── deus/

~/.local/bin/
  └── logos           # Command wrapper script
```

### Dependencies

#### Required
- **Python 3.10+** - Checked automatically
- **PyYAML 6.0+** - Installed automatically via pip

#### Optional (for clipboard support)
- **pyperclip** - Python package, installed automatically
- **xclip** or **xsel** - System tools (Linux/FreeBSD)
- **wl-copy** - Wayland clipboard tool (Linux)

### OS-Specific Behavior

#### FreeBSD
- Uses `pkg` package manager for system dependencies
- Installs `xclip` if available and user confirms

#### Linux
- Detects package manager (apt-get, yum, dnf, pacman, zypper)
- Installs `xclip` using appropriate package manager
- Supports both X11 and Wayland clipboard tools

### PATH Configuration

The script automatically adds `~/.local/bin` to your PATH if:
- It's not already in PATH
- You confirm the action
- A shell configuration file is detected (~/.bashrc, ~/.zshrc, or ~/.profile)

If PATH is not configured automatically:
```bash
# Add to your shell configuration file
export PATH="$HOME/.local/bin:$PATH"

# Then reload
source ~/.bashrc  # or ~/.zshrc, or ~/.profile
```

## Manual Installation

If you prefer to install manually:

### Step 1: Install Python Dependencies

```bash
pip3 install --user pyyaml>=6.0 pyperclip>=1.8.0
```

### Step 2: Install System Dependencies

**FreeBSD:**
```bash
pkg install xclip  # or xsel
```

**Linux (Debian/Ubuntu):**
```bash
sudo apt-get install xclip  # or xsel, or wl-clipboard (Wayland)
```

**Linux (RedHat/CentOS):**
```bash
sudo yum install xclip  # or xsel
```

**Linux (Fedora):**
```bash
sudo dnf install xclip  # or xsel, or wl-clipboard (Wayland)
```

**Linux (Arch):**
```bash
sudo pacman -S xclip  # or xsel, or wl-clipboard (Wayland)
```

### Step 3: Install LOGOS Package

```bash
# Create installation directory
mkdir -p ~/.logos

# Copy package
cp -r logos ~/.logos/
```

### Step 4: Create Command Wrapper

```bash
# Create bin directory
mkdir -p ~/.local/bin

# Create wrapper script
cat > ~/.local/bin/logos << 'EOF'
#!/bin/bash
cd ~/.logos && python3 -m logos "$@"
EOF

# Make executable
chmod +x ~/.local/bin/logos
```

### Step 5: Configure PATH

Add to your shell configuration file:
```bash
export PATH="$HOME/.local/bin:$PATH"
```

## Verification

After installation, verify it works:

```bash
# Check command is available
which logos

# Run LOGOS
logos

# Check version (if implemented)
logos --version
```

## Troubleshooting

### Command Not Found

If `logos` command is not found:
1. Check if `~/.local/bin` is in PATH: `echo $PATH`
2. Add to PATH if missing (see PATH Configuration above)
3. Reload shell: `source ~/.bashrc` (or your shell config)

### Python Not Found

If Python 3 is not found:
- **FreeBSD:** `pkg install python3`
- **Linux:** Use your package manager to install `python3`

### Clipboard Not Working

If clipboard operations fail:
1. Install system clipboard tool: `xclip`, `xsel`, or `wl-copy`
2. Install pyperclip: `pip3 install --user pyperclip>=1.8.0`
3. Check if tool is in PATH: `which xclip`

### Permission Errors

If you get permission errors:
- Use `--user` flag with pip: `pip3 install --user ...`
- Check `~/.local/bin` permissions: `chmod +x ~/.local/bin/logos`
- Check `~/.logos` permissions: `chmod -R u+rw ~/.logos`

## Uninstallation

To uninstall LOGOS:

```bash
# Remove installation directory
rm -rf ~/.logos

# Remove command wrapper
rm ~/.local/bin/logos

# Remove from PATH (edit ~/.bashrc, ~/.zshrc, or ~/.profile)
# Remove the line: export PATH="$HOME/.local/bin:$PATH"
```

## Development Installation

For development work, use editable installation:

```bash
git clone https://github.com/orpheus497/logos.git
cd logos
pip install -e ".[dev,clipboard]"
```

This installs LOGOS in development mode with all dependencies.

---

**Maintained By:** LOGOS Installation System  
**Last Updated:** 2026-01-20
