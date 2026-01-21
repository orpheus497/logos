"""
##Script function and purpose: LOGOS CLI entry point.

Enables running as `python -m logos` for package execution.
This is the single source of truth for the CLI interface.

##Action purpose: Provides package-level entry point that delegates to main CLI
implementation for unified LOGOS command execution.
"""

import sys

from logos.cli.main import main

##Function purpose: Entry point when run as module
if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        ##Error purpose: Handle Ctrl+C at module level (user interruption)
        print("\nExiting LOGOS...")
        sys.exit(0)
