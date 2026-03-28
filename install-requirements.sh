#!/usr/bin/env bash
##
##Script function and purpose: LOGOS Python Requirements Installer
##
##Action purpose: Installs Python dependencies from requirements.txt or
##requirements-dev.txt with automatic Python 3 and pip detection.
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

##Function purpose: Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

##Function purpose: Detect Python 3 interpreter
detect_python() {
    if command_exists python3; then
        PYTHON_CMD="python3"
    elif command_exists python; then
        ##Action purpose: Verify that 'python' is actually Python 3
        PYTHON_MAJOR=$(python -c 'import sys; print(sys.version_info[0])' 2>/dev/null || echo "0")
        if [ "$PYTHON_MAJOR" = "3" ]; then
            PYTHON_CMD="python"
        else
            print_error "Python 3 is required but only Python $PYTHON_MAJOR was found."
            exit 1
        fi
    else
        print_error "Python 3 is not installed. Please install Python 3 first."
        exit 1
    fi

    PYTHON_VERSION=$($PYTHON_CMD -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    print_success "Python $PYTHON_VERSION detected ($PYTHON_CMD)"
}

##Function purpose: Detect pip and set PIP_CMD array
detect_pip() {
    if command_exists pip3; then
        PIP_CMD=(pip3)
    elif "$PYTHON_CMD" -m pip --version >/dev/null 2>&1; then
        PIP_CMD=("$PYTHON_CMD" -m pip)
    elif command_exists pip; then
        PIP_CMD=(pip)
    else
        print_error "pip is not available. Please install pip first."
        print_info "Try: $PYTHON_CMD -m ensurepip --upgrade"
        exit 1
    fi

    PIP_VERSION=$("${PIP_CMD[@]}" --version | head -1)
    print_success "pip detected: $PIP_VERSION"
}

##Function purpose: Install requirements from the specified file
install_requirements() {
    local req_file="$1"

    if [ ! -f "$req_file" ]; then
        print_error "Requirements file not found: $req_file"
        exit 1
    fi

    print_info "Installing dependencies from $req_file..."
    "${PIP_CMD[@]}" install --user --upgrade -r "$req_file" || {
        print_error "Failed to install dependencies from $req_file"
        exit 1
    }
    print_success "Dependencies from $req_file installed"
}

##Function purpose: Install optional clipboard support
install_clipboard() {
    print_info "Installing pyperclip (optional, for clipboard support)..."
    "${PIP_CMD[@]}" install --user --upgrade "pyperclip>=1.8.0" || {
        print_warning "Failed to install pyperclip. Clipboard support may be limited."
    }
}

##Function purpose: Display usage information
usage() {
    echo "Usage: $(basename "$0") [OPTIONS]"
    echo ""
    echo "Install LOGOS Python dependencies."
    echo ""
    echo "Options:"
    echo "  --dev     Install development dependencies (requirements-dev.txt)"
    echo "  --help    Show this help message"
}

##Function purpose: Main installation function
main() {
    ##Action purpose: Parse command-line arguments
    DEV_MODE=false
    for arg in "$@"; do
        case "$arg" in
            --dev)
                DEV_MODE=true
                ;;
            --help)
                usage
                exit 0
                ;;
            *)
                print_error "Unknown option: $arg"
                usage
                exit 1
                ;;
        esac
    done

    ##Action purpose: Resolve script directory for locating requirements files
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

    print_info "LOGOS Requirements Installer"
    print_info "============================"
    echo ""

    ##Action purpose: Detect Python 3 and pip
    detect_python
    detect_pip
    echo ""

    ##Action purpose: Select and install the appropriate requirements file
    if [ "$DEV_MODE" = true ]; then
        print_info "Installing development dependencies..."
        install_requirements "$SCRIPT_DIR/requirements-dev.txt"
    else
        print_info "Installing production dependencies..."
        install_requirements "$SCRIPT_DIR/requirements.txt"
    fi
    echo ""

    ##Action purpose: Install optional clipboard dependency
    install_clipboard
    echo ""

    print_success "All Python dependencies installed successfully!"
}

##Action purpose: Run main function
main "$@"
