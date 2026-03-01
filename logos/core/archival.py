##Script function and purpose: File archival utilities for Orchestrator

"""
Provides functions for archiving .devdocs/ files while maintaining retrievability.
Orchestrator uses these to move obsolete files to .archive/ folder.
"""

import shutil
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Optional, Dict


##Function purpose: Archive single file with timestamp
def archive_file(
    file_path: Path,
    archive_base_path: Path,
    reason: str = "Manual archival"
) -> bool:
    """
    ##Function purpose: Move file to .archive/ with timestamp prefix.
    
    Args:
        file_path: Path to file to archive (relative to .devdocs/)
        archive_base_path: Path to .archive/ folder
        reason: Reason for archival (logged in archival_log.md)
    
    Returns:
        True if successful, False if failed
    """
    ##Condition purpose: Validate file exists
    if not file_path.exists():
        print(f"❌ Cannot archive {file_path}: File not found")
        return False

    ##Action purpose: Create timestamped archive directory
    timestamp = datetime.now().strftime("%Y-%m-%d")
    archive_dir = archive_base_path / timestamp
    archive_dir.mkdir(parents=True, exist_ok=True)

    ##Action purpose: Determine destination filename
    destination = archive_dir / file_path.name

    ##Condition purpose: Handle filename conflicts
    if destination.exists():
        counter = 1
        while destination.exists():
            stem = file_path.stem
            suffix = file_path.suffix
            destination = archive_dir / f"{stem}-{counter}{suffix}"
            counter += 1

    ##Action purpose: Move file to archive
    try:
        shutil.move(str(file_path), str(destination))
    except Exception as e:
        print(f"❌ Failed to archive {file_path}: {e}")
        return False

    ##Action purpose: Log archival action
    log_archival(
        filename=file_path.name,
        timestamp=timestamp,
        reason=reason,
        archive_log_path=archive_base_path / "archival_log.md"
    )

    print(f"✅ Archived {file_path.name} → {destination}")
    return True


##Function purpose: Archive multiple files in batch
def archive_files_batch(
    file_paths: list[Path],
    archive_base_path: Path,
    reason: str
) -> dict[str, bool]:
    """
    ##Function purpose: Archive multiple files with single timestamp.
    
    Args:
        file_paths: List of file paths to archive
        archive_base_path: Path to .archive/ folder
        reason: Reason for batch archival
    
    Returns:
        Dict mapping file paths to success status
    """
    results = {}

    ##Loop purpose: Archive each file
    for file_path in file_paths:
        success = archive_file(file_path, archive_base_path, reason)
        results[str(file_path)] = success

    return results


##Function purpose: Retrieve file from archive
def retrieve_from_archive(
    filename: str,
    archive_base_path: Path,
    target_date: str | None = None
) -> str | None:
    """
    ##Function purpose: Retrieve archived file content.
    
    Operator-only function to retrieve historical context when needed.
    
    Args:
        filename: Name of file to retrieve
        archive_base_path: Path to .archive/ folder
        target_date: Optional date to search (YYYY-MM-DD), searches all if None
    
    Returns:
        File content if found, None if not found
    """
    ##Condition purpose: Check if archive exists
    if not archive_base_path.exists():
        print("❌ No archive folder found")
        return None

    ##Condition purpose: Search specific date or all dates
    if target_date:
        search_dirs = [archive_base_path / target_date]
    else:
        ##Action purpose: Search all date directories
        search_dirs = [d for d in archive_base_path.iterdir() if d.is_dir() and d.name != ".gitkeep"]
        ##Action purpose: Sort by date descending (most recent first)
        search_dirs = sorted(search_dirs, key=lambda d: d.name, reverse=True)

    ##Loop purpose: Search for file in archive directories
    for dir_path in search_dirs:
        ##Condition purpose: Skip if not a directory
        if not dir_path.is_dir():
            continue

        ##Action purpose: Check for exact filename match
        file_path = dir_path / filename
        if file_path.exists():
            ##Action purpose: Read and return content
            with open(file_path) as f:
                content = f.read()
            print(f"✅ Retrieved {filename} from archive ({dir_path.name})")
            return content

        ##Action purpose: Check for filename with counter suffix
        for archived_file in dir_path.glob(f"{Path(filename).stem}*{Path(filename).suffix}"):
            with open(archived_file) as f:
                content = f.read()
            print(f"✅ Retrieved {archived_file.name} from archive ({dir_path.name})")
            return content

    print(f"❌ {filename} not found in archive")
    return None


##Function purpose: Log archival action
def log_archival(
    filename: str,
    timestamp: str,
    reason: str,
    archive_log_path: Path
):
    """
    ##Function purpose: Append archival action to governance log.
    
    Args:
        filename: Name of archived file
        timestamp: Date of archival (YYYY-MM-DD)
        reason: Reason for archival
        archive_log_path: Path to archival_log.md
    """
    ##Action purpose: Create log file if doesn't exist
    archive_log_path.parent.mkdir(parents=True, exist_ok=True)

    ##Condition purpose: Initialize log if new file
    if not archive_log_path.exists():
        with open(archive_log_path, "w") as f:
            f.write("# .devdocs/ Archival Log\n\n")
            f.write("**Purpose:** Record of all archival actions performed by Orchestrator\n\n")
            f.write("---\n\n")

    ##Action purpose: Append log entry
    with open(archive_log_path, "a") as f:
        f.write(f"## {timestamp}\n\n")
        f.write(f"- **File:** `{filename}`\n")
        f.write(f"- **Reason:** {reason}\n")
        f.write(f"- **Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("- **Agent:** E0/E1 (Orchestrator)\n\n")
        f.write("---\n\n")


##Function purpose: List all archived files
def list_archived_files(archive_base_path: Path) -> dict[str, list[str]]:
    """
    ##Function purpose: Get list of all archived files organized by date.
    
    Args:
        archive_base_path: Path to .archive/ folder
    
    Returns:
        Dict mapping date (YYYY-MM-DD) to list of filenames
    """
    archived = {}

    ##Condition purpose: Check if archive exists
    if not archive_base_path.exists():
        return archived

    ##Loop purpose: Scan all date directories
    for date_dir in archive_base_path.iterdir():
        ##Condition purpose: Skip non-directories and log file
        if not date_dir.is_dir() or date_dir.name.startswith("."):
            continue

        ##Action purpose: List files in this date directory
        files = [f.name for f in date_dir.iterdir() if f.is_file()]
        archived[date_dir.name] = files

    return archived


##Function purpose: Clean old archives
def clean_old_archives(
    archive_base_path: Path,
    days_to_keep: int = 90
) -> Tuple[int, int]:
    """
    ##Function purpose: Remove archive directories older than specified days.
    
    Args:
        archive_base_path: Path to .archive/ folder
        days_to_keep: Number of days to retain (default: 90)
    
    Returns:
        Tuple of (directories_removed, files_removed)
    """
    ##Condition purpose: Check if archive exists
    if not archive_base_path.exists():
        return 0, 0

    cutoff_date = datetime.now() - timedelta(days=days_to_keep)
    dirs_removed = 0
    files_removed = 0

    ##Loop purpose: Check each date directory
    for date_dir in archive_base_path.iterdir():
        ##Condition purpose: Skip non-directories
        if not date_dir.is_dir() or date_dir.name.startswith("."):
            continue

        ##Condition purpose: Parse date from directory name
        try:
            dir_date = datetime.strptime(date_dir.name, "%Y-%m-%d")
        except ValueError:
            continue

        ##Condition purpose: Remove if older than cutoff
        if dir_date < cutoff_date:
            ##Action purpose: Count files before deletion
            file_count = len(list(date_dir.iterdir()))

            ##Action purpose: Remove directory
            shutil.rmtree(date_dir)
            dirs_removed += 1
            files_removed += file_count

            ##Action purpose: Log cleanup
            log_archival(
                filename=f"Cleaned {file_count} files from {date_dir.name}/",
                timestamp=datetime.now().strftime("%Y-%m-%d"),
                reason=f"Archive cleanup (>{days_to_keep} days old)",
                archive_log_path=archive_base_path / "archival_log.md"
            )

    return dirs_removed, files_removed
