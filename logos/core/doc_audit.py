"""
##Script function and purpose: doc_audit - Documentation audit utilities.

Provides utilities for auditing markdown documentation across the LOGOS project.
Finds markdown files, extracts links, validates internal references, and reports
broken links or missing references.

##Action purpose: Supports documentation quality by programmatically detecting
broken internal links and missing cross-references before they reach users.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from pathlib import Path

##Action purpose: Default directories to exclude from markdown file discovery
_DEFAULT_EXCLUDE_DIRS: tuple[str, ...] = (".git", ".venv", "node_modules", "__pycache__", ".devdocs")

##Action purpose: Regex for standard markdown links: [text](target)
_MARKDOWN_LINK_PATTERN: re.Pattern[str] = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")


@dataclass(slots=True)
class AuditResult:
    """
    ##Class purpose: Holds the audit outcome for a single markdown file.

    ##Action purpose: Collects all link-validation data so callers can inspect
    totals, broken links, missing references, and warnings in one object.

    Attributes:
        file_path: Path to the audited markdown file.
        total_links: Total number of links discovered in the file.
        broken_links: List of dicts each containing 'link', 'line', and 'reason'.
        missing_references: List of reference identifiers that could not be resolved.
        warnings: Free-form warning messages produced during the audit.
        passed: Whether the file passed the audit (no broken links or missing refs).
    """

    file_path: Path
    total_links: int = 0
    broken_links: list[dict] = field(default_factory=list)
    missing_references: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    passed: bool = True


def find_markdown_files(root_path: Path, exclude_dirs: list[str] | None = None) -> list[Path]:
    """
    ##Function purpose: Recursively discover all markdown files under *root_path*.

    ##Action purpose: Walks the directory tree using os.walk with in-place directory
    pruning so that excluded directories are never entered, avoiding unnecessary I/O.

    Args:
        root_path: Root directory to search.
        exclude_dirs: Directory names to skip.  Defaults to common non-source dirs.

    Returns:
        Sorted list of Path objects pointing to markdown files.
    """
    if exclude_dirs is None:
        exclude_dirs = list(_DEFAULT_EXCLUDE_DIRS)

    exclude_set = set(exclude_dirs)
    md_files: list[Path] = []

    if not root_path.is_dir():
        return md_files

    ##Action purpose: Walk tree with in-place pruning of excluded directories
    for dirpath, dirnames, filenames in os.walk(root_path):
        ##Action purpose: Prune excluded dirs in-place so os.walk never descends into them
        dirnames[:] = [d for d in dirnames if d not in exclude_set]

        for fname in filenames:
            if fname.endswith(".md"):
                md_files.append(Path(dirpath) / fname)

    md_files.sort()
    return md_files


def extract_links(file_path: Path) -> list[tuple[str, int]]:
    """
    ##Function purpose: Extract all markdown links from a file.

    ##Action purpose: Parses each line for ``[text](link)`` patterns and records
    the link target together with its 1-based line number.

    Args:
        file_path: Path to the markdown file to scan.

    Returns:
        List of (link_target, line_number) tuples.
    """
    links: list[tuple[str, int]] = []

    if not file_path.is_file():
        return links

    text = file_path.read_text(encoding="utf-8")
    for line_number, line in enumerate(text.splitlines(), start=1):
        for match in _MARKDOWN_LINK_PATTERN.finditer(line):
            link_target = match.group(2).strip()
            links.append((link_target, line_number))

    return links


def validate_internal_links(
    file_path: Path,
    links: list[tuple[str, int]],
    root_path: Path,
) -> list[dict]:
    """
    ##Function purpose: Check that internal file links point to existing files.

    ##Action purpose: Skips external (http/https), anchor-only (#…), and empty
    links.  Resolves relative paths against the file's parent and absolute-style
    paths (starting with ``/``) against *root_path*.  Rejects any resolved path
    that escapes the project root to prevent directory-traversal issues.

    Args:
        file_path: The markdown file that contains the links.
        links: Output of :func:`extract_links`.
        root_path: Project root used to resolve absolute-style paths.

    Returns:
        List of dicts with keys ``link``, ``line``, and ``reason`` for every
        broken internal link.
    """
    broken: list[dict] = []
    resolved_root = root_path.resolve()

    for link_target, line_number in links:
        ##Condition purpose: Skip links that are not internal file references
        if not link_target or link_target.startswith(("http://", "https://", "mailto:")):
            continue
        if link_target.startswith("#"):
            continue

        ##Action purpose: Strip fragment identifiers so we only check the file portion
        clean_target = link_target.split("#")[0]
        if not clean_target:
            continue

        ##Action purpose: Resolve the target to an absolute filesystem path
        if clean_target.startswith("/"):
            resolved = root_path / clean_target.lstrip("/")
        else:
            resolved = file_path.parent / clean_target

        resolved = resolved.resolve()

        ##Condition purpose: Reject links that escape the project root (path traversal)
        try:
            resolved.relative_to(resolved_root)
        except ValueError:
            broken.append(
                {
                    "link": link_target,
                    "line": line_number,
                    "reason": f"Link escapes project root: {clean_target}",
                }
            )
            continue

        if not resolved.exists():
            broken.append(
                {
                    "link": link_target,
                    "line": line_number,
                    "reason": f"File not found: {clean_target}",
                }
            )

    return broken


def audit_file(file_path: Path, root_path: Path) -> AuditResult:
    """
    ##Function purpose: Perform a full documentation audit on a single markdown file.

    ##Action purpose: Orchestrates link extraction and validation, then packages
    the results into an :class:`AuditResult`.

    Args:
        file_path: Markdown file to audit.
        root_path: Project root for resolving absolute-style paths.

    Returns:
        An :class:`AuditResult` summarizing the audit.
    """
    links = extract_links(file_path)
    broken = validate_internal_links(file_path, links, root_path)

    passed = len(broken) == 0

    return AuditResult(
        file_path=file_path,
        total_links=len(links),
        broken_links=broken,
        passed=passed,
    )


def audit_project(root_path: Path, exclude_dirs: list[str] | None = None) -> list[AuditResult]:
    """
    ##Function purpose: Audit every markdown file in the project.

    ##Action purpose: Combines :func:`find_markdown_files` and :func:`audit_file`
    to produce a list of audit results for the whole project tree.

    Args:
        root_path: Project root directory.
        exclude_dirs: Directory names to skip during file discovery.

    Returns:
        List of :class:`AuditResult`, one per markdown file found.
    """
    md_files = find_markdown_files(root_path, exclude_dirs=exclude_dirs)
    return [audit_file(md_file, root_path) for md_file in md_files]
