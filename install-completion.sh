#!/bin/sh
# LOGOS Shell Completion Installer
# Installs shell completion scripts for Bash, Zsh, and Fish.
#
# Usage:
#   ./install-completion.sh [--bash] [--zsh] [--fish] [--all]
#
# If no options are given, installs completions for the current shell.

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
COMPLETIONS_DIR="${SCRIPT_DIR}/completions"

# Detect available shells
HAS_BASH=false
HAS_ZSH=false
HAS_FISH=false

if command -v bash >/dev/null 2>&1; then HAS_BASH=true; fi
if command -v zsh >/dev/null 2>&1; then HAS_ZSH=true; fi
if command -v fish >/dev/null 2>&1; then HAS_FISH=true; fi

install_bash() {
    SRC="${COMPLETIONS_DIR}/bash/logos"
    if [ ! -f "$SRC" ]; then
        echo "Error: Bash completion script not found at ${SRC}"
        return 1
    fi

    FINAL_PATH=""
    # Try system-wide first, fall back to user-level
    if [ -d /etc/bash_completion.d ] && [ -w /etc/bash_completion.d ]; then
        FINAL_PATH="/etc/bash_completion.d/logos"
        cp "$SRC" "$FINAL_PATH"
        echo "Installed Bash completion to ${FINAL_PATH}"
    elif [ -d "${HOME}/.local/share/bash-completion/completions" ]; then
        FINAL_PATH="${HOME}/.local/share/bash-completion/completions/logos"
        cp "$SRC" "$FINAL_PATH"
        echo "Installed Bash completion to ${FINAL_PATH}"
    else
        DEST="${HOME}/.local/share/bash-completion/completions"
        mkdir -p "$DEST"
        FINAL_PATH="${DEST}/logos"
        cp "$SRC" "$FINAL_PATH"
        echo "Installed Bash completion to ${FINAL_PATH}"
    fi
    echo "  Reload with: source ${FINAL_PATH}"
}

install_zsh() {
    SRC="${COMPLETIONS_DIR}/zsh/_logos"
    if [ ! -f "$SRC" ]; then
        echo "Error: Zsh completion script not found at ${SRC}"
        return 1
    fi

    # Try common Zsh completion paths
    if [ -d /usr/local/share/zsh/site-functions ] && [ -w /usr/local/share/zsh/site-functions ]; then
        DEST="/usr/local/share/zsh/site-functions/_logos"
        cp "$SRC" "$DEST"
        echo "Installed Zsh completion to ${DEST}"
    elif [ -d "${HOME}/.zsh/completions" ]; then
        DEST="${HOME}/.zsh/completions/_logos"
        cp "$SRC" "$DEST"
        echo "Installed Zsh completion to ${DEST}"
    else
        DEST="${HOME}/.zsh/completions"
        mkdir -p "$DEST"
        cp "$SRC" "${DEST}/_logos"
        echo "Installed Zsh completion to ${DEST}/_logos"
        echo "  Add to .zshrc: fpath=(${DEST} \$fpath)"
    fi
    echo "  Reload with: autoload -Uz compinit && compinit"
}

install_fish() {
    SRC="${COMPLETIONS_DIR}/fish/logos.fish"
    if [ ! -f "$SRC" ]; then
        echo "Error: Fish completion script not found at ${SRC}"
        return 1
    fi

    DEST="${HOME}/.config/fish/completions"
    mkdir -p "$DEST"
    cp "$SRC" "${DEST}/logos.fish"
    echo "Installed Fish completion to ${DEST}/logos.fish"
    echo "  Completions will be loaded automatically on next Fish session."
}

show_usage() {
    echo "LOGOS Shell Completion Installer"
    echo ""
    echo "Usage: $0 [--bash] [--zsh] [--fish] [--all]"
    echo ""
    echo "Options:"
    echo "  --bash    Install Bash completions"
    echo "  --zsh     Install Zsh completions"
    echo "  --fish    Install Fish completions"
    echo "  --all     Install completions for all detected shells"
    echo "  --help    Show this help message"
    echo ""
    echo "If no options are given, installs for the current shell (\$SHELL)."
}

# Parse arguments
INSTALL_BASH=false
INSTALL_ZSH=false
INSTALL_FISH=false

if [ $# -eq 0 ]; then
    # Auto-detect current shell
    CURRENT_SHELL="$(basename "${SHELL:-/bin/sh}")"
    case "$CURRENT_SHELL" in
        bash) INSTALL_BASH=true ;;
        zsh)  INSTALL_ZSH=true ;;
        fish) INSTALL_FISH=true ;;
        *)
            echo "Unknown shell: ${CURRENT_SHELL}"
            echo "Please specify: $0 --bash, --zsh, or --fish"
            exit 1
            ;;
    esac
else
    for arg in "$@"; do
        case "$arg" in
            --bash) INSTALL_BASH=true ;;
            --zsh)  INSTALL_ZSH=true ;;
            --fish) INSTALL_FISH=true ;;
            --all)
                INSTALL_BASH=$HAS_BASH
                INSTALL_ZSH=$HAS_ZSH
                INSTALL_FISH=$HAS_FISH
                ;;
            --help|-h)
                show_usage
                exit 0
                ;;
            *)
                echo "Unknown option: $arg"
                show_usage
                exit 1
                ;;
        esac
    done
fi

echo "LOGOS Shell Completion Installer"
echo "================================"
echo ""

INSTALLED=0

if [ "$INSTALL_BASH" = true ]; then
    echo "Installing Bash completions..."
    install_bash && INSTALLED=$((INSTALLED + 1))
    echo ""
fi

if [ "$INSTALL_ZSH" = true ]; then
    echo "Installing Zsh completions..."
    install_zsh && INSTALLED=$((INSTALLED + 1))
    echo ""
fi

if [ "$INSTALL_FISH" = true ]; then
    echo "Installing Fish completions..."
    install_fish && INSTALLED=$((INSTALLED + 1))
    echo ""
fi

if [ "$INSTALLED" -eq 0 ]; then
    echo "No completions were installed."
    echo "Run '$0 --help' for usage information."
    exit 1
fi

echo "Done! Installed ${INSTALLED} completion script(s)."
