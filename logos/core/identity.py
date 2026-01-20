"""
##Script function and purpose: System identity scanning and persistence.

Scans system for identity information and manages persistent identity storage.
Phase 2 implementation.

##Action purpose: Provides system scanning, identity dataclass, and persistence
functions for maintaining user identity across LOGOS sessions.
"""

import getpass
import logging
import platform
import socket
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from logos.core.persistence import get_identity_path, read_config, write_config
from logos.core.validation import validate_identity_schema

##Action purpose: Initialize logger for identity operations
logger = logging.getLogger(__name__)

##Action purpose: Subprocess timeout constant for system checks
SUBPROCESS_TIMEOUT: float = 0.5


##Class purpose: System identity data structure
@dataclass
class SystemIdentity:
    """
    ##Class purpose: Represents system and user identity information.

    ##Action purpose: Encapsulates all identity data including user info, system info,
    faction choice, and session tracking for persistent identity across LOGOS sessions.

    Attributes:
        hostname: System hostname
        username: Current username
        os_name: Operating system name (e.g., "Linux", "FreeBSD")
        os_version: OS version/release string
        faction: Selected faction name (e.g., "orphic", "revanchist")
        created_at: ISO timestamp when identity was first created
        last_session: ISO timestamp of last session
        last_mode: Last used mode ("daedelus" or "deus")
        last_agent: Last used agent identifier
        total_sessions: Total number of sessions
        faction_prompt_counts: Dictionary mapping faction names to prompt counts
        mode_prompt_counts: Dictionary mapping mode names (daedelus/deus) to prompt counts
    """

    hostname: str
    username: str
    os_name: str
    os_version: str
    faction: str
    created_at: str
    last_session: str
    last_mode: str | None = None
    last_agent: str | None = None
    total_sessions: int = 0
    faction_prompt_counts: dict[str, int] = field(default_factory=dict)  # Counts by user-selected faction
    mode_prompt_counts: dict[str, int] = field(default_factory=dict)  # Counts by mode (daedelus/deus)


##Function purpose: Run FreeBSD-specific system checks in parallel
def _run_freebsd_checks(scan: dict[str, Any]) -> None:
    """
    ##Function purpose: Runs FreeBSD-specific system checks in parallel.

    ##Action purpose: Executes FreeBSD version, ZFS availability, and jail host checks
    concurrently using ThreadPoolExecutor for improved performance.

    Args:
        scan: Dictionary to update with FreeBSD check results
    """
    ##Action purpose: Use ThreadPoolExecutor to execute subprocess calls concurrently
    with ThreadPoolExecutor(max_workers=3) as executor:
        ##Action purpose: Submit all FreeBSD checks as concurrent tasks
        futures = {
            executor.submit(_check_freebsd_version): "freebsd_version",
            executor.submit(_check_zfs_available): "zfs_available",
            executor.submit(_check_jail_host): "jail_host",
        }

        ##Loop purpose: Process completed futures as they finish
        for future in as_completed(futures):
            key = futures[future]
            try:
                value = future.result()
                ##Condition purpose: Handle different return types
                if key == "freebsd_version" and value is not None:
                    scan[key] = value
                elif key in ("zfs_available", "jail_host"):
                    scan[key] = value
            except Exception:
                ##Error purpose: Handle any exceptions from subprocess calls
                ##Action purpose: Set default values on failure
                if key == "freebsd_version":
                    pass  # Don't set if None
                else:
                    scan[key] = False


##Function purpose: Run subprocess command with standardized error handling
def _run_subprocess_check(
    command: list[str], return_output: bool = False, timeout: float = SUBPROCESS_TIMEOUT
) -> str | bool | None:
    """
    ##Function purpose: Runs subprocess command with standardized error handling.

    ##Action purpose: Executes subprocess command with timeout and error handling,
    returning either output string or boolean success status based on return_output flag.

    Args:
        command: List of command and arguments
        return_output: If True, return stdout string; if False, return boolean
        timeout: Subprocess timeout in seconds (default: SUBPROCESS_TIMEOUT)

    Returns:
        If return_output=True: stdout string if successful, None otherwise
        If return_output=False: True if successful, False otherwise
    """
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=timeout)
        if return_output:
            return result.stdout.strip() if result.returncode == 0 else None
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired, subprocess.SubprocessError):
        ##Error purpose: Handle subprocess execution failures
        return None if return_output else False


##Function purpose: Check FreeBSD version via subprocess
def _check_freebsd_version() -> str | None:
    """
    ##Function purpose: Checks FreeBSD version using subprocess.

    ##Action purpose: Runs freebsd-version command with reduced timeout for performance.

    Returns:
        FreeBSD version string if successful, None otherwise
    """
    result = _run_subprocess_check(["freebsd-version"], return_output=True)
    return result if isinstance(result, str) else None


##Function purpose: Check ZFS availability via subprocess
def _check_zfs_available() -> bool:
    """
    ##Function purpose: Checks if ZFS is available on the system.

    ##Action purpose: Runs zfs version command with reduced timeout for performance.

    Returns:
        True if ZFS is available, False otherwise
    """
    result = _run_subprocess_check(["zfs", "version"], return_output=False)
    return result if isinstance(result, bool) else False


##Function purpose: Check if system is jail host via subprocess
def _check_jail_host() -> bool:
    """
    ##Function purpose: Checks if system is a jail host.

    ##Action purpose: Runs jls -q command with reduced timeout for performance.

    Returns:
        True if system is jail host, False otherwise
    """
    result = _run_subprocess_check(["jls", "-q"], return_output=False)
    return result if isinstance(result, bool) else False


##Function purpose: Scan current system for identity information
def scan_system() -> dict[str, Any]:
    """
    ##Function purpose: Scans current system for identity and context information.

    ##Action purpose: Collects hostname, username, OS information, and LOGOS state
    to build comprehensive system identity for first-run setup.

    Returns:
        Dictionary containing system scan data
    """
    ##Action purpose: Get basic system information
    scan = {
        ##Action purpose: Identity information
        "hostname": socket.gethostname(),
        "username": getpass.getuser(),
        "home_dir": str(Path.home()),
        ##Action purpose: Operating system information
        "os_name": platform.system(),
        "os_version": platform.release(),
        "os_full": platform.platform(),
        ##Action purpose: Python environment
        "python_version": platform.python_version(),
        ##Action purpose: LOGOS state detection
        "devdocs_exists": (Path.home() / ".devdocs").exists(),
        "sysdocs_exists": (Path.home() / ".sysdocs").exists(),
        "logos_config_exists": (Path.home() / ".logos").exists(),
    }

    ##Condition purpose: Check if running on FreeBSD for DEUS-specific info
    if platform.system() == "FreeBSD":
        ##Action purpose: Run FreeBSD-specific checks in parallel for performance
        _run_freebsd_checks(scan)

    ##Action purpose: Return complete system scan
    return scan


##Function purpose: Load persisted identity from configuration file
def load_identity(config_path: Path | None = None) -> SystemIdentity | None:
    """
    ##Function purpose: Loads persisted identity from YAML configuration file.

    ##Action purpose: Reads identity.yaml file and reconstructs SystemIdentity
    dataclass from stored data.

    ##Condition purpose: If file doesn't exist or is invalid, return None.

    Args:
        config_path: Optional path to identity file (defaults to ~/.logos/identity.yaml)

    Returns:
        SystemIdentity instance if loaded successfully, None otherwise
    """
    ##Action purpose: Use default path if not provided
    if config_path is None:
        config_path = get_identity_path()

    ##Action purpose: Read configuration from file
    config_data = read_config(config_path)

    ##Condition purpose: Check if config was loaded successfully
    if config_data is None:
        ##Action purpose: Return None if file doesn't exist or is invalid
        return None

    ##Action purpose: Validate YAML schema structure and types
    is_valid, error = validate_identity_schema(config_data)
    if not is_valid:
        ##Error purpose: Log schema validation failure
        logger.warning(f"Invalid identity schema: {error}")
        ##Action purpose: Return None if schema validation fails
        return None

    ##Action purpose: Extract sections from config
    identity_data = config_data.get("identity", {})
    system_data = config_data.get("system", {})
    faction_data = config_data.get("faction", {})
    sessions_data = config_data.get("sessions", {})

    ##Action purpose: Extract prompt counts from config
    prompt_counts_data = config_data.get("prompt_counts", {})
    faction_counts = prompt_counts_data.get("faction", {})
    mode_counts = prompt_counts_data.get("mode", {})

    ##Action purpose: Build SystemIdentity from config data
    return SystemIdentity(
        hostname=identity_data["hostname"],
        username=identity_data["username"],
        os_name=system_data["os"],
        os_version=system_data["version"],
        faction=faction_data["name"],
        created_at=identity_data["created"],
        last_session=sessions_data.get("last_timestamp", ""),
        last_mode=sessions_data.get("last_mode"),
        last_agent=sessions_data.get("last_agent"),
        total_sessions=sessions_data.get("total_sessions", 0),
        faction_prompt_counts=faction_counts if faction_counts else {},
        mode_prompt_counts=mode_counts if mode_counts else {},
    )


##Function purpose: Save identity to configuration file
def save_identity(identity: SystemIdentity, config_path: Path | None = None) -> bool:
    """
    ##Function purpose: Persists identity to YAML configuration file.

    ##Action purpose: Serializes SystemIdentity dataclass to YAML format and writes
    to identity.yaml file, creating directory structure if needed.

    Args:
        identity: SystemIdentity instance to save
        config_path: Optional path to identity file (defaults to ~/.logos/identity.yaml)

    Returns:
        True if save succeeded, False otherwise
    """
    ##Action purpose: Use default path if not provided
    if config_path is None:
        config_path = get_identity_path()

    ##Action purpose: Build configuration dictionary structure
    config_data = {
        ##Action purpose: Identity section with core fields
        "identity": {
            "username": identity.username,
            "hostname": identity.hostname,
            "created": identity.created_at,
        },
        ##Action purpose: Faction section
        "faction": {
            "name": identity.faction,
            "selected": identity.created_at,
        },
        ##Action purpose: System section
        "system": {
            "os": identity.os_name,
            "version": identity.os_version,
            "architecture": platform.machine(),
        },
        ##Action purpose: Sessions section
        "sessions": {
            "last_mode": identity.last_mode,
            "last_agent": identity.last_agent,
            "last_timestamp": identity.last_session,
            "total_sessions": identity.total_sessions,
        },
        ##Action purpose: Prompt counts section
        "prompt_counts": {
            "faction": identity.faction_prompt_counts,
            "mode": identity.mode_prompt_counts,
        },
    }

    ##Action purpose: Write configuration to file
    return write_config(config_path, config_data)


##Function purpose: Create new identity from system scan
def create_identity(faction: str, scan_data: dict[str, Any] | None = None) -> SystemIdentity:
    """
    ##Function purpose: Creates new SystemIdentity from system scan and faction choice.

    ##Action purpose: Builds SystemIdentity dataclass from system scan data and
    selected faction, setting initial timestamps and session counts.

    Args:
        faction: Selected faction name
        scan_data: Optional system scan data (scans system if not provided)

    Returns:
        New SystemIdentity instance
    """
    ##Condition purpose: Scan system if data not provided
    if scan_data is None:
        scan_data = scan_system()

    ##Action purpose: Get current timestamp in ISO format
    now = datetime.utcnow().isoformat() + "Z"

    ##Action purpose: Create new identity from scan data
    return SystemIdentity(
        hostname=scan_data["hostname"],
        username=scan_data["username"],
        os_name=scan_data["os_name"],
        os_version=scan_data["os_version"],
        faction=faction,
        created_at=now,
        last_session=now,
        last_mode=None,
        last_agent=None,
        total_sessions=0,
        faction_prompt_counts={},  # Initialize empty counters
        mode_prompt_counts={},  # Initialize empty counters
    )


##Function purpose: Update session tracking in identity
def update_session_tracking(
    identity: SystemIdentity,
    mode: str,
    agent: str,
) -> SystemIdentity:
    """
    ##Function purpose: Updates session tracking information in identity.

    ##Action purpose: Creates updated SystemIdentity with new session information,
    incrementing total sessions, updating last session timestamp, mode, and agent,
    and incrementing faction and mode prompt counters.

    Args:
        identity: Current SystemIdentity instance
        mode: Current mode ("daedelus" or "deus")
        agent: Current agent identifier (e.g., "A1", "B6")

    Returns:
        New SystemIdentity instance with updated session tracking
    """
    ##Action purpose: Get current timestamp in ISO format
    now = datetime.utcnow().isoformat() + "Z"

    ##Action purpose: Copy and update faction prompt counts
    updated_faction_counts = identity.faction_prompt_counts.copy()
    ##Action purpose: Increment counter for current faction
    current_faction = identity.faction
    updated_faction_counts[current_faction] = updated_faction_counts.get(current_faction, 0) + 1

    ##Action purpose: Copy and update mode prompt counts
    updated_mode_counts = identity.mode_prompt_counts.copy()
    ##Action purpose: Increment counter for current mode
    updated_mode_counts[mode] = updated_mode_counts.get(mode, 0) + 1

    ##Action purpose: Create updated identity with new session info and prompt counts
    return SystemIdentity(
        hostname=identity.hostname,
        username=identity.username,
        os_name=identity.os_name,
        os_version=identity.os_version,
        faction=identity.faction,
        created_at=identity.created_at,
        last_session=now,
        last_mode=mode,
        last_agent=agent,
        total_sessions=identity.total_sessions + 1,
        faction_prompt_counts=updated_faction_counts,
        mode_prompt_counts=updated_mode_counts,
    )
