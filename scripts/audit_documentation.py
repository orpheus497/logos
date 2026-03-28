#!/usr/bin/env python3
"""
##Script function and purpose: audit_documentation - CLI wrapper for documentation auditing.

Provides a command-line interface around the logos.core.doc_audit module to detect
broken internal links and missing cross-references in the project's markdown files.
Supports single-file and whole-project audits with optional JSON output.

##Action purpose: Enables developers and CI pipelines to quickly validate documentation
integrity from the terminal without writing custom scripts.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from logos.core.doc_audit import AuditResult, audit_file, audit_project, find_markdown_files

##Action purpose: ANSI escape sequences for colored terminal output
_GREEN = "\033[92m"
_RED = "\033[91m"
_YELLOW = "\033[93m"
_BOLD = "\033[1m"
_RESET = "\033[0m"


def _build_parser() -> argparse.ArgumentParser:
    """
    ##Function purpose: Build and return the argument parser for the CLI.

    ##Action purpose: Centralises all CLI flag definitions so they can be tested
    independently of the main entry point.

    Returns:
        Configured :class:`argparse.ArgumentParser`.
    """
    parser = argparse.ArgumentParser(
        prog="audit_documentation",
        description="Audit markdown documentation for broken internal links.",
    )
    parser.add_argument(
        "--root",
        "-r",
        type=Path,
        default=Path("."),
        help="Root directory to audit (default: current directory).",
    )
    parser.add_argument(
        "--file",
        "-f",
        type=Path,
        default=None,
        help="Audit a single markdown file instead of the whole project.",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        default=False,
        help="Show detailed output including passing files.",
    )
    parser.add_argument(
        "--json",
        dest="json_output",
        action="store_true",
        default=False,
        help="Output results in JSON format (no colors).",
    )
    parser.add_argument(
        "--fix-suggestions",
        action="store_true",
        default=False,
        help="Show fix suggestions for broken links.",
    )
    return parser


def _suggest_fix(broken_link: dict, root_path: Path) -> str | None:
    """
    ##Function purpose: Generate a fix suggestion for a broken link.

    ##Action purpose: Searches the project for markdown files whose name matches the
    broken target and proposes the closest candidate path.

    Args:
        broken_link: Dict with 'link', 'line', and 'reason' keys.
        root_path: Project root used for file discovery.

    Returns:
        A human-readable suggestion string, or ``None`` if no candidate is found.
    """
    link_target = broken_link["link"].split("#")[0]
    if not link_target:
        return None

    target_name = Path(link_target).name
    if not target_name:
        return None

    ##Action purpose: Search project for files matching the broken link's filename
    all_md = find_markdown_files(root_path)
    resolved_root = root_path.resolve()
    candidates = [p for p in all_md if p.name == target_name]

    if not candidates:
        return None

    ##Action purpose: Rank candidates by number of shared path parts with the broken link
    target_parts = Path(link_target).parts
    candidates.sort(
        key=lambda c: len(set(c.relative_to(resolved_root).parts) & set(target_parts)),
        reverse=True,
    )
    suggestion_path = candidates[0].relative_to(resolved_root)
    return f"Did you mean '{suggestion_path}'?"


def _format_result_text(result: AuditResult, root_path: Path, *, verbose: bool, fix_suggestions: bool) -> str:
    """
    ##Function purpose: Format a single AuditResult as colored terminal text.

    ##Action purpose: Produces human-readable output with ANSI colors indicating
    pass/fail status and optional fix suggestions for broken links.

    Args:
        result: The audit result to format.
        root_path: Project root for computing relative paths.
        verbose: When False, passing files are omitted from the output.
        fix_suggestions: When True, appends fix suggestions for broken links.

    Returns:
        Formatted string (may be empty when verbose is False and the file passed).
    """
    try:
        rel = result.file_path.relative_to(root_path.resolve())
    except ValueError:
        rel = result.file_path

    lines: list[str] = []

    if result.passed:
        if verbose:
            lines.append(f"  {_GREEN}✓{_RESET} {rel} ({result.total_links} links)")
        return "\n".join(lines)

    ##Action purpose: Report failing file with count of broken links
    lines.append(f"  {_RED}✗{_RESET} {rel} ({result.total_links} links, {len(result.broken_links)} broken)")

    for bl in result.broken_links:
        lines.append(f"    {_RED}Line {bl['line']}{_RESET}: {bl['link']}")
        lines.append(f"      {_YELLOW}{bl['reason']}{_RESET}")
        if fix_suggestions:
            suggestion = _suggest_fix(bl, root_path)
            if suggestion:
                lines.append(f"      {_GREEN}{suggestion}{_RESET}")

    for warning in result.warnings:
        lines.append(f"    {_YELLOW}⚠ {warning}{_RESET}")

    return "\n".join(lines)


def _results_to_json(results: list[AuditResult], root_path: Path) -> str:
    """
    ##Function purpose: Serialise a list of AuditResults to a JSON string.

    ##Action purpose: Produces machine-readable output suitable for CI pipelines and
    downstream tooling that cannot parse ANSI-colored text.

    Args:
        results: List of audit results.
        root_path: Project root for computing relative paths.

    Returns:
        Pretty-printed JSON string.
    """
    resolved_root = root_path.resolve()
    output: list[dict] = []

    for r in results:
        try:
            rel = str(r.file_path.relative_to(resolved_root))
        except ValueError:
            rel = str(r.file_path)

        output.append(
            {
                "file": rel,
                "total_links": r.total_links,
                "broken_links": r.broken_links,
                "missing_references": r.missing_references,
                "warnings": r.warnings,
                "passed": r.passed,
            }
        )

    return json.dumps(output, indent=2)


def main(argv: list[str] | None = None) -> int:
    """
    ##Function purpose: Entry point for the documentation audit CLI.

    ##Action purpose: Parses arguments, runs the appropriate audit (single-file or
    whole-project), formats and prints results, and returns the exit code.

    Args:
        argv: Command-line arguments (defaults to sys.argv[1:]).

    Returns:
        Exit code: 0 if all files pass, 1 if any file has failures.
    """
    parser = _build_parser()
    args = parser.parse_args(argv)

    root_path = args.root.resolve()

    ##Action purpose: Collect audit results for either a single file or the full project
    if args.file is not None:
        file_path = args.file.resolve()
        if not file_path.is_file():
            print(f"Error: file not found: {args.file}", file=sys.stderr)
            return 1
        results = [audit_file(file_path, root_path)]
    else:
        results = audit_project(root_path)

    ##Action purpose: Emit JSON output and exit early when --json is requested
    if args.json_output:
        print(_results_to_json(results, root_path))
        total_broken = sum(len(r.broken_links) for r in results)
        return 1 if total_broken > 0 else 0

    ##Action purpose: Print colored human-readable report
    total_files = len(results)
    passed = sum(1 for r in results if r.passed)
    failed = total_files - passed
    total_broken = sum(len(r.broken_links) for r in results)

    print(f"\n{_BOLD}Documentation Audit{_RESET}")
    print(f"{_BOLD}{'=' * 40}{_RESET}\n")

    for result in results:
        text = _format_result_text(result, root_path, verbose=args.verbose, fix_suggestions=args.fix_suggestions)
        if text:
            print(text)

    ##Action purpose: Print summary line with counts
    print(f"\n{_BOLD}Summary:{_RESET} {total_files} files audited, ", end="")
    print(f"{_GREEN}{passed} passed{_RESET}, ", end="")
    print(f"{_RED}{failed} failed{_RESET}, ", end="")
    print(f"{total_broken} broken links found\n")

    return 1 if failed > 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
