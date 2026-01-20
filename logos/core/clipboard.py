"""
##Script function and purpose: Shared clipboard utilities.

Cross-platform clipboard operations used by both Daedelus and DEUS.
Unified implementation that tries all available methods in order:
1. Wayland (wl-copy) - preferred on Wayland compositors
2. X11 (xclip, xsel) - common on X11 systems including FreeBSD
3. Python pyperclip - cross-platform fallback

##Action purpose: Addresses shell injection risk (P0-003) by using subprocess.run()
with explicit arguments instead of shell=True.
"""

import logging
import shutil
import subprocess

##Action purpose: Initialize logger for clipboard operations
logger = logging.getLogger(__name__)

##Action purpose: Check for pyperclip availability at module level to avoid repeated imports
try:
    import pyperclip

    _PYPERCLIP_AVAILABLE = True
except ImportError:
    pyperclip = None  # type: ignore[assignment]
    _PYPERCLIP_AVAILABLE = False
    logger.debug("pyperclip not installed - will use native clipboard tools")


def copy_to_clipboard(text: str) -> bool:
    """
    ##Function purpose: Copy text to system clipboard using platform-appropriate method.

    ##Step purpose: Unified clipboard implementation that tries multiple methods:
    - Wayland-first for modern Linux desktops
    - X11 fallback for traditional X11 systems (including FreeBSD)
    - Python pyperclip as final cross-platform fallback

    ##Action purpose: Uses subprocess.run() with explicit arguments to avoid shell injection.

    Args:
        text: The text content to copy to clipboard.

    Returns:
        True if copy succeeded, False otherwise.
    """
    ##Step purpose: Try Wayland clipboard (wl-copy) - preferred on Wayland compositors
    if wl_copy_path := shutil.which("wl-copy"):
        try:
            result = subprocess.run(
                [wl_copy_path],
                input=text.encode("utf-8"),
                capture_output=True,
                timeout=5,
            )
            ##Condition purpose: Check if wl-copy succeeded
            if result.returncode == 0:
                return True
            logger.debug(f"wl-copy failed: {result.stderr.decode()}")
        except subprocess.TimeoutExpired:
            logger.warning("wl-copy timed out")
        except Exception as e:
            logger.debug(f"wl-copy exception: {e}")

    ##Step purpose: Try X11 clipboard tools (xclip, xsel) - common on X11 systems
    x11_commands = [
        (["xclip", "-selection", "clipboard"], "xclip"),
        (["xsel", "--clipboard", "--input"], "xsel"),
    ]

    ##Loop purpose: Try each X11 clipboard tool in order
    for cmd, name in x11_commands:
        ##Condition purpose: Check if X11 tool is available
        if cmd_path := shutil.which(cmd[0]):
            try:
                ##Action purpose: Replace first element with full path for security
                full_cmd = [cmd_path] + cmd[1:]
                result = subprocess.run(
                    full_cmd,
                    input=text.encode("utf-8"),
                    capture_output=True,
                    timeout=5,
                )
                ##Condition purpose: Check if X11 tool succeeded
                if result.returncode == 0:
                    return True
                logger.debug(f"{name} failed: {result.stderr.decode()}")
            except subprocess.TimeoutExpired:
                logger.warning(f"{name} timed out")
            except Exception as e:
                logger.debug(f"{name} exception: {e}")

    ##Step purpose: Try Python pyperclip library (cross-platform fallback)
    if _PYPERCLIP_AVAILABLE:
        try:
            pyperclip.copy(text)
            return True
        except Exception as e:
            logger.debug(f"pyperclip exception: {e}")

    ##Action purpose: Return False if all methods failed
    return False
