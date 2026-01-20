#!/usr/bin/env bash
##
##Script function and purpose: LOGOS Installation Script
##
##Action purpose: Installs LOGOS as a system package in ~/.logos with
##smart OS detection (FreeBSD/Linux) and dependency management.
##

set -euo pipefail

##Action purpose: Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

##Function purpose: Print colored messages
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

##Function purpose: Detect operating system
detect_os() {
    if [ "$(uname)" = "FreeBSD" ]; then
        echo "freebsd"
    elif [ "$(uname)" = "Linux" ]; then
        echo "linux"
    else
        echo "unknown"
    fi
}

##Function purpose: Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

##Function purpose: Check Python version
check_python() {
    if ! command_exists python3; then
        print_error "Python 3 is not installed. Please install Python 3.10 or higher."
        exit 1
    fi

    PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    PYTHON_MAJOR=$(echo "$PYTHON_VERSION" | cut -d. -f1)
    PYTHON_MINOR=$(echo "$PYTHON_VERSION" | cut -d. -f2)

    if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 10 ]); then
        print_error "Python 3.10 or higher is required. Found: $PYTHON_VERSION"
        exit 1
    fi

    print_success "Python $PYTHON_VERSION detected"
}

##Function purpose: Install Python dependencies
install_python_deps() {
    print_info "Installing Python dependencies..."

    # Check if pip is available
    if ! command_exists pip3 && ! python3 -m pip --version >/dev/null 2>&1; then
        print_error "pip3 is not available. Please install pip first."
        exit 1
    fi

    # Use pip3 or python3 -m pip
    if command_exists pip3; then
        PIP_CMD="pip3"
    else
        PIP_CMD="python3 -m pip"
    fi

    # Install required dependencies
    print_info "Installing PyYAML (required)..."
    $PIP_CMD install --user --upgrade "pyyaml>=6.0" || {
        print_error "Failed to install PyYAML"
        exit 1
    }

    # Install optional clipboard support
    print_info "Installing pyperclip (optional, for clipboard support)..."
    $PIP_CMD install --user --upgrade "pyperclip>=1.8.0" || {
        print_warning "Failed to install pyperclip. Clipboard support may be limited."
    }

    print_success "Python dependencies installed"
}

##Function purpose: Install system dependencies (FreeBSD)
install_freebsd_deps() {
    print_info "Checking FreeBSD system dependencies..."

    MISSING_DEPS=()

    # Check for clipboard tools
    if ! command_exists xclip && ! command_exists xsel && ! command_exists wl-copy; then
        MISSING_DEPS+=("xclip")
    fi

    if [ ${#MISSING_DEPS[@]} -gt 0 ]; then
        print_warning "Missing clipboard tools: ${MISSING_DEPS[*]}"
        print_info "To install clipboard support on FreeBSD:"
        print_info "  pkg install xclip  # or xsel"
        read -p "Install xclip now? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            if command_exists pkg; then
                sudo pkg install -y xclip || {
                    print_warning "Failed to install xclip. You can install it manually later."
                }
            else
                print_warning "pkg command not found. Please install xclip manually: pkg install xclip"
            fi
        fi
    else
        print_success "All clipboard tools available"
    fi
}

##Function purpose: Install system dependencies (Linux)
install_linux_deps() {
    print_info "Checking Linux system dependencies..."

    MISSING_DEPS=()

    # Check for clipboard tools
    if ! command_exists xclip && ! command_exists xsel && ! command_exists wl-copy; then
        # Detect package manager
        if command_exists apt-get; then
            MISSING_DEPS+=("xclip")
        elif command_exists yum; then
            MISSING_DEPS+=("xclip")
        elif command_exists dnf; then
            MISSING_DEPS+=("xclip")
        elif command_exists pacman; then
            MISSING_DEPS+=("xclip")
        elif command_exists zypper; then
            MISSING_DEPS+=("xclip")
        fi
    fi

    if [ ${#MISSING_DEPS[@]} -gt 0 ]; then
        print_warning "Missing clipboard tools: ${MISSING_DEPS[*]}"
        print_info "To install clipboard support on Linux:"
        if command_exists apt-get; then
            print_info "  sudo apt-get install xclip  # or xsel, or wl-clipboard (Wayland)"
        elif command_exists yum; then
            print_info "  sudo yum install xclip  # or xsel"
        elif command_exists dnf; then
            print_info "  sudo dnf install xclip  # or xsel, or wl-clipboard (Wayland)"
        elif command_exists pacman; then
            print_info "  sudo pacman -S xclip  # or xsel, or wl-clipboard (Wayland)"
        elif command_exists zypper; then
            print_info "  sudo zypper install xclip  # or xsel"
        fi
        read -p "Install xclip now? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            if command_exists apt-get; then
                sudo apt-get install -y xclip || {
                    print_warning "Failed to install xclip. You can install it manually later."
                }
            elif command_exists yum; then
                sudo yum install -y xclip || {
                    print_warning "Failed to install xclip. You can install it manually later."
                }
            elif command_exists dnf; then
                sudo dnf install -y xclip || {
                    print_warning "Failed to install xclip. You can install it manually later."
                }
            elif command_exists pacman; then
                sudo pacman -S --noconfirm xclip || {
                    print_warning "Failed to install xclip. You can install it manually later."
                }
            elif command_exists zypper; then
                sudo zypper install -y xclip || {
                    print_warning "Failed to install xclip. You can install it manually later."
                }
            else
                print_warning "Package manager not detected. Please install xclip manually."
            fi
        fi
    else
        print_success "All clipboard tools available"
    fi
}

##Function purpose: Install LOGOS package
install_logos() {
    print_info "Installing LOGOS to ~/.logos..."

    INSTALL_DIR="$HOME/.logos"
    SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

    # Create installation directory
    mkdir -p "$INSTALL_DIR"

    # Copy package files
    print_info "Copying package files..."
    cp -r "$SRC_DIR/logos" "$INSTALL_DIR/" || {
        print_error "Failed to copy package files"
        exit 1
    }

    # Copy essential files
    if [ -f "$SRC_DIR/pyproject.toml" ]; then
        cp "$SRC_DIR/pyproject.toml" "$INSTALL_DIR/" || {
            print_warning "Failed to copy pyproject.toml"
        }
    fi

    print_success "Package files copied to $INSTALL_DIR"
}

##Function purpose: Create logos command wrapper
create_logos_command() {
    print_info "Creating logos command..."

    INSTALL_DIR="$HOME/.logos"
    BIN_DIR="$HOME/.local/bin"

    # Create ~/.local/bin if it doesn't exist
    mkdir -p "$BIN_DIR"

    # Create logos wrapper script
    cat > "$BIN_DIR/logos" << 'EOF'
#!/usr/bin/env bash
##
##Script function and purpose: LOGOS command wrapper
##
##Action purpose: Executes LOGOS from installation directory
##

INSTALL_DIR="$HOME/.logos"
PYTHON_CMD="python3"

# Check if installation exists
if [ ! -d "$INSTALL_DIR" ]; then
    echo "Error: LOGOS is not installed. Run install.sh first." >&2
    exit 1
fi

# Execute LOGOS
cd "$INSTALL_DIR" || exit 1
exec "$PYTHON_CMD" -m logos "$@"
EOF

    chmod +x "$BIN_DIR/logos"

    # Check if ~/.local/bin is in PATH
    if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
        print_warning "~/.local/bin is not in your PATH"
        print_info "Add this line to your ~/.bashrc, ~/.zshrc, or ~/.profile:"
        print_info "  export PATH=\"\$HOME/.local/bin:\$PATH\""
        print_info ""
        read -p "Add to PATH now? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            SHELL_RC=""
            if [ -f "$HOME/.bashrc" ]; then
                SHELL_RC="$HOME/.bashrc"
            elif [ -f "$HOME/.zshrc" ]; then
                SHELL_RC="$HOME/.zshrc"
            elif [ -f "$HOME/.profile" ]; then
                SHELL_RC="$HOME/.profile"
            fi

            if [ -n "$SHELL_RC" ]; then
                if ! grep -q 'export PATH="$HOME/.local/bin:$PATH"' "$SHELL_RC"; then
                    echo '' >> "$SHELL_RC"
                    echo '# LOGOS installation' >> "$SHELL_RC"
                    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$SHELL_RC"
                    print_success "Added ~/.local/bin to PATH in $SHELL_RC"
                    print_info "Run 'source $SHELL_RC' or restart your terminal to use the logos command"
                else
                    print_info "PATH already configured in $SHELL_RC"
                fi
            else
                print_warning "Could not detect shell configuration file"
            fi
        fi
    else
        print_success "~/.local/bin is already in PATH"
    fi

    print_success "logos command created at $BIN_DIR/logos"
}

##Function purpose: Main installation function
main() {
    print_info "LOGOS Installation Script"
    print_info "========================"
    echo ""

    # Detect OS
    OS=$(detect_os)
    if [ "$OS" = "unknown" ]; then
        print_error "Unsupported operating system: $(uname)"
        print_info "LOGOS supports FreeBSD and Linux"
        exit 1
    fi

    print_success "Detected OS: $OS"
    echo ""

    # Check Python
    check_python
    echo ""

    # Install Python dependencies
    install_python_deps
    echo ""

    # Install system dependencies based on OS
    if [ "$OS" = "freebsd" ]; then
        install_freebsd_deps
    elif [ "$OS" = "linux" ]; then
        install_linux_deps
    fi
    echo ""

    # Install LOGOS package
    install_logos
    echo ""

    # Create logos command
    create_logos_command
    echo ""

    print_success "Installation complete!"
    print_info ""
    print_info "To use LOGOS:"
    if [[ ":$PATH:" == *":$HOME/.local/bin:"* ]]; then
        print_info "  logos"
    else
        print_info "  ~/.local/bin/logos"
        print_info "  (or add ~/.local/bin to your PATH)"
    fi
    print_info ""
    print_info "Installation directory: $HOME/.logos"
    print_info "Command location: $HOME/.local/bin/logos"
}

##Action purpose: Run main function
main "$@"
