#!/usr/bin/env bash
set -e

echo "Uninstalling LOGOS..."

# Remove installation directory
if [ -d "$HOME/.logos" ]; then
    rm -rf "$HOME/.logos"
    echo "Removed ~/.logos"
else
    echo "~/.logos not found."
fi

# Remove binary
if [ -f "$HOME/.local/bin/logos" ]; then
    rm "$HOME/.local/bin/logos"
    echo "Removed ~/.local/bin/logos"
else
    echo "~/.local/bin/logos not found."
fi

echo "Uninstallation complete."
echo "Note: You may want to remove the 'export PATH' line from your shell configuration file (e.g. .bashrc) manually."
echo "Note: Python dependencies (pyyaml, pyperclip) were not removed to avoid breaking other tools."
