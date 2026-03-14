##Script function and purpose: Temporal log management for agent logs with automatic archival and summarization

"""
Provides utilities for managing agent log files with temporal structure.

- Daily entries (today + last 6 days)
- Weekly summaries (generated before archival)
- Monthly summaries (permanent project memory)
- Automatic archival based on age thresholds

Used by Orchestrator (E0/E1) for .devdocs/ maintenance.
"""

import re
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path


##Class purpose: Represents a temporal section in an agent log
@dataclass
class LogSection:
    """
    ##Class purpose: Contains parsed section from agent log.

    Attributes:
        section_type: "month_summary" | "week_summary" | "daily_entry"
        date: Date of the section (datetime object)
        content: Full text content of the section
        heading: Section heading text
        start_line: Line number where section starts
        end_line: Line number where section ends
    """

    section_type: str
    date: datetime
    content: str
    heading: str
    start_line: int
    end_line: int


##Class purpose: Result of temporal log analysis
@dataclass
class LogAnalysis:
    """
    ##Class purpose: Contains analysis results for an agent log file.

    Attributes:
        agent_key: Agent identifier (e.g., "A1")
        file_path: Path to log file
        file_size_kb: Size in kilobytes
        last_updated: Last modification timestamp
        month_summaries: List of month summary sections
        week_summaries: List of week summary sections
        daily_entries: List of daily entry sections (should be 7 max)
        days_since_update: Days since last modification
        stale: Whether log is stale (>7 days untouched)
        bloated: Whether log exceeds size threshold (>500KB)
        needs_archival: Whether daily entries >7 days old exist
        archival_candidates: List of sections to archive
    """

    agent_key: str
    file_path: Path
    file_size_kb: float
    last_updated: datetime
    month_summaries: list[LogSection]
    week_summaries: list[LogSection]
    daily_entries: list[LogSection]
    days_since_update: int
    stale: bool
    bloated: bool
    needs_archival: bool
    archival_candidates: list[LogSection]


##Function purpose: Parse agent log file into temporal sections
def parse_agent_log(log_path: Path) -> list[LogSection]:
    """
    ##Function purpose: Parse agent log file and extract temporal sections.

    Args:
        log_path: Path to agent log file

    Returns:
        List of LogSection objects in chronological order
    """
    ##Condition purpose: Check if file exists
    if not log_path.exists():
        return []

    ##Action purpose: Read log content
    with open(log_path, encoding="utf-8") as f:
        lines = f.readlines()

    ##Action purpose: Initialize sections list
    sections = []
    current_section = None
    current_lines = []
    current_start = 0

    ##Loop purpose: Parse file line by line
    for i, line in enumerate(lines):
        ##Condition purpose: Detect month summary headers
        if re.match(r"### \w+ \d{4} Summary", line):
            ##Action purpose: Save previous section if exists
            if current_section:
                sections.append(
                    LogSection(
                        section_type=current_section["type"],
                        date=current_section["date"],
                        content="".join(current_lines),
                        heading=current_section["heading"],
                        start_line=current_start,
                        end_line=i - 1,
                    )
                )

            ##Action purpose: Start new month summary section
            month_match = re.search(r"(\w+) (\d{4})", line)
            if month_match:
                month_name = month_match.group(1)
                year = int(month_match.group(2))
                ##Action purpose: Parse month name to number
                month_num = datetime.strptime(month_name, "%B").month
                section_date = datetime(year, month_num, 1)

                current_section = {"type": "month_summary", "date": section_date, "heading": line.strip()}
                current_lines = [line]
                current_start = i

        ##Condition purpose: Detect week summary headers
        elif re.match(r"\*\*Week of \d{4}-\d{2}-\d{2}", line):
            ##Action purpose: Save previous section
            if current_section:
                sections.append(
                    LogSection(
                        section_type=current_section["type"],
                        date=current_section["date"],
                        content="".join(current_lines),
                        heading=current_section["heading"],
                        start_line=current_start,
                        end_line=i - 1,
                    )
                )

            ##Action purpose: Start new week summary section
            date_match = re.search(r"(\d{4}-\d{2}-\d{2})", line)
            if date_match:
                section_date = datetime.strptime(date_match.group(1), "%Y-%m-%d")

                current_section = {"type": "week_summary", "date": section_date, "heading": line.strip()}
                current_lines = [line]
                current_start = i

        ##Condition purpose: Detect daily entry headers
        elif re.match(r"### \d{4}-\d{2}-\d{2}", line):
            ##Action purpose: Save previous section
            if current_section:
                sections.append(
                    LogSection(
                        section_type=current_section["type"],
                        date=current_section["date"],
                        content="".join(current_lines),
                        heading=current_section["heading"],
                        start_line=current_start,
                        end_line=i - 1,
                    )
                )

            ##Action purpose: Start new daily entry section
            date_match = re.search(r"(\d{4}-\d{2}-\d{2})", line)
            if date_match:
                section_date = datetime.strptime(date_match.group(1), "%Y-%m-%d")

                current_section = {"type": "daily_entry", "date": section_date, "heading": line.strip()}
                current_lines = [line]
                current_start = i

        ##Condition purpose: Not a header, accumulate content
        else:
            if current_section:
                current_lines.append(line)

    ##Action purpose: Save final section
    if current_section:
        sections.append(
            LogSection(
                section_type=current_section["type"],
                date=current_section["date"],
                content="".join(current_lines),
                heading=current_section["heading"],
                start_line=current_start,
                end_line=len(lines) - 1,
            )
        )

    return sections


##Function purpose: Analyze agent log for archival needs
def analyze_agent_log(log_path: Path, agent_key: str) -> LogAnalysis:
    """
    ##Function purpose: Analyze agent log file for temporal management.

    Args:
        log_path: Path to agent log file
        agent_key: Agent identifier (e.g., "A1")

    Returns:
        LogAnalysis object with complete analysis
    """
    ##Condition purpose: Check if file exists
    if not log_path.exists():
        return LogAnalysis(
            agent_key=agent_key,
            file_path=log_path,
            file_size_kb=0.0,
            last_updated=datetime.now(),
            month_summaries=[],
            week_summaries=[],
            daily_entries=[],
            days_since_update=999,
            stale=True,
            bloated=False,
            needs_archival=False,
            archival_candidates=[],
        )

    ##Action purpose: Get file stats
    file_stat = log_path.stat()
    file_size_kb = file_stat.st_size / 1024
    last_modified = datetime.fromtimestamp(file_stat.st_mtime)
    days_since_update = (datetime.now() - last_modified).days

    ##Action purpose: Parse log sections
    sections = parse_agent_log(log_path)

    ##Action purpose: Categorize sections
    month_summaries = [s for s in sections if s.section_type == "month_summary"]
    week_summaries = [s for s in sections if s.section_type == "week_summary"]
    daily_entries = [s for s in sections if s.section_type == "daily_entry"]

    ##Action purpose: Check thresholds
    stale = days_since_update > 7
    bloated = file_size_kb > 500

    ##Action purpose: Identify archival candidates (daily entries ≥7 days old; keep today + last 6 days)
    cutoff_date = datetime.now() - timedelta(days=7)
    archival_candidates = [entry for entry in daily_entries if entry.date <= cutoff_date]
    needs_archival = len(archival_candidates) > 0

    ##Action purpose: Return analysis
    return LogAnalysis(
        agent_key=agent_key,
        file_path=log_path,
        file_size_kb=file_size_kb,
        last_updated=last_modified,
        month_summaries=month_summaries,
        week_summaries=week_summaries,
        daily_entries=daily_entries,
        days_since_update=days_since_update,
        stale=stale,
        bloated=bloated,
        needs_archival=needs_archival,
        archival_candidates=archival_candidates,
    )


##Function purpose: Generate weekly summary from daily entries
def generate_weekly_summary(daily_entries: list[LogSection], week_start_date: datetime) -> str:
    """
    ##Function purpose: Create weekly summary from week's daily entries.

    Args:
        daily_entries: List of daily entry sections for the week
        week_start_date: Start date of the week

    Returns:
        Formatted weekly summary markdown
    """
    ##Action purpose: Sort entries by date
    sorted_entries = sorted(daily_entries, key=lambda e: e.date)

    ##Action purpose: Extract accomplishments
    accomplishments = []
    files_modified = set()
    collaborations = []
    blockers = []

    ##Loop purpose: Parse each daily entry
    for entry in sorted_entries:
        content = entry.content

        ##Action purpose: Extract work performed
        if "**Work Performed:**" in content:
            work_section = content.split("**Work Performed:**")[1].split("**")[0]
            for line in work_section.split("\n"):
                if line.strip().startswith("-"):
                    accomplishments.append(line.strip()[2:])

        ##Action purpose: Extract files
        if "**Files Created:**" in content or "**Files Modified:**" in content:
            files_section = re.findall(r"\*\*Files (?:Created|Modified):\*\*\n(.*?)(?:\n\n|\*\*)", content, re.DOTALL)
            for section in files_section:
                for line in section.split("\n"):
                    if line.strip().startswith("-"):
                        file_match = re.search(r"`([^`]+)`", line)
                        if file_match:
                            files_modified.add(file_match.group(1))

        ##Action purpose: Extract collaborations
        if "**Collaborations:**" in content:
            collab_section = content.split("**Collaborations:**")[1].split("**")[0]
            for line in collab_section.split("\n"):
                if line.strip().startswith("-"):
                    collaborations.append(line.strip()[2:])

        ##Action purpose: Extract blockers
        if "**Blockers:**" in content:
            blocker_section = content.split("**Blockers:**")[1].split("**")[0]
            for line in blocker_section.split("\n"):
                if line.strip().startswith("-") and "None" not in line:
                    blockers.append(line.strip()[2:])

    ##Action purpose: Format week end date
    week_end_date = week_start_date + timedelta(days=6)

    ##Action purpose: Build summary
    summary = f"## WEEKLY SUMMARY (Generated by Orchestrator)\n\n**Week of {week_start_date.strftime('%Y-%m-%d')} to {week_end_date.strftime('%Y-%m-%d')}**\n\n**This Week's Work:**\n"

    ##Condition purpose: Add accomplishments
    if accomplishments:
        summary += "\n**Accomplishments:**\n"
        for item in accomplishments[:10]:  # Limit to top 10
            summary += f"- {item}\n"

    ##Condition purpose: Add files
    if files_modified:
        summary += "\n**Files Modified:**\n"
        for file in sorted(files_modified)[:15]:  # Limit to 15 files
            summary += f"- `{file}`\n"

    ##Condition purpose: Add collaborations
    if collaborations:
        summary += "\n**Collaborations:**\n"
        for collab in set(collaborations):  # Deduplicate
            summary += f"- {collab}\n"

    ##Condition purpose: Add blockers
    if blockers:
        summary += "\n**Blockers Encountered:**\n"
        for blocker in set(blockers):
            summary += f"- {blocker}\n"

    summary += "\n---\n"

    return summary


##Function purpose: Generate monthly summary from weekly summaries
def generate_monthly_summary(week_summaries: list[LogSection], month_date: datetime) -> str:
    """
    ##Function purpose: Create monthly summary from month's weekly summaries.

    Args:
        week_summaries: List of weekly summary sections for the month
        month_date: Date representing the month (datetime with day=1)

    Returns:
        Formatted monthly summary markdown
    """
    ##Action purpose: Sort summaries by date
    sorted_summaries = sorted(week_summaries, key=lambda s: s.date)

    ##Action purpose: Extract key information
    all_accomplishments = []
    all_files = set()
    all_collaborations = set()

    ##Loop purpose: Parse each weekly summary
    for summary in sorted_summaries:
        content = summary.content

        ##Action purpose: Extract accomplishments
        if "**Accomplishments:**" in content:
            accom_section = content.split("**Accomplishments:**")[1].split("**")[0]
            for line in accom_section.split("\n"):
                if line.strip().startswith("-"):
                    all_accomplishments.append(line.strip()[2:])

        ##Action purpose: Extract files
        if "**Files Modified:**" in content:
            files_section = content.split("**Files Modified:**")[1].split("**")[0]
            for line in files_section.split("\n"):
                file_match = re.search(r"`([^`]+)`", line)
                if file_match:
                    all_files.add(file_match.group(1))

        ##Action purpose: Extract collaborations
        if "**Collaborations:**" in content:
            collab_section = content.split("**Collaborations:**")[1].split("**")[0]
            for line in collab_section.split("\n"):
                if line.strip().startswith("-"):
                    all_collaborations.add(line.strip()[2:])

    ##Action purpose: Format month name
    month_name = month_date.strftime("%B %Y")
    next_month = (month_date + timedelta(days=32)).replace(day=1)
    next_month_name = next_month.strftime("%B %Y")

    ##Action purpose: Build summary
    summary = f"### {month_name} Summary\n\n**Generated:** {datetime.now().strftime('%Y-%m-%d')} by Orchestrator\n\n**Key Accomplishments:**\n"

    ##Condition purpose: Add top accomplishments
    if all_accomplishments:
        for item in all_accomplishments[:15]:  # Top 15 for month
            summary += f"- {item}\n"
    else:
        summary += "- No recorded accomplishments this month\n"

    summary += "\n**Major Decisions:**\n"
    ##Condition purpose: Add decisions (would be extracted from decision sections)
    summary += "- [Extracted from decision logs during the month]\n"

    summary += "\n**Files Created/Modified:**\n"
    ##Condition purpose: Add files
    if all_files:
        for file in sorted(all_files)[:20]:  # Top 20 files
            summary += f"- `{file}`\n"
    else:
        summary += "- No recorded file changes this month\n"

    summary += "\n**Collaborations:**\n"
    ##Condition purpose: Add collaborations
    if all_collaborations:
        for collab in sorted(all_collaborations):
            summary += f"- {collab}\n"
    else:
        summary += "- No recorded collaborations this month\n"

    summary += f"\n**{next_month_name} Priorities:**\n"
    summary += "- [To be determined]\n"

    summary += "\n---\n"

    return summary


##Function purpose: Archive old daily entries from agent log
def archive_daily_entries(log_path: Path, analysis: LogAnalysis, archive_base_path: Path) -> tuple[bool, str]:
    """
    ##Function purpose: Archive daily entries >7 days old, generate weekly summary.

    Args:
        log_path: Path to agent log file
        analysis: LogAnalysis object from analyze_agent_log()
        archive_base_path: Base path for archives (e.g., .devdocs/.archive/)

    Returns:
        Tuple of (success: bool, message: str)
    """
    ##Condition purpose: Check if archival needed
    if not analysis.needs_archival:
        return True, "No archival needed"

    ##Action purpose: Read current log content
    with open(log_path, encoding="utf-8") as f:
        content = f.read()

    ##Action purpose: Group archival candidates by week
    weeks = {}
    for candidate in analysis.archival_candidates:
        ##Action purpose: Calculate week start (Monday)
        week_start = candidate.date - timedelta(days=candidate.date.weekday())
        week_key = week_start.strftime("%Y-%m-%d")

        if week_key not in weeks:
            weeks[week_key] = []
        weeks[week_key].append(candidate)

    ##Loop purpose: Archive each week
    for week_key, entries in weeks.items():
        ##Action purpose: Parse week start date
        week_start = datetime.strptime(week_key, "%Y-%m-%d")

        ##Action purpose: Generate weekly summary
        weekly_summary = generate_weekly_summary(entries, week_start)

        ##Action purpose: Create archive directory
        archive_date = datetime.now().strftime("%Y-%m-%d")
        archive_dir = archive_base_path / archive_date
        archive_dir.mkdir(parents=True, exist_ok=True)

        ##Action purpose: Create archive file
        archive_file = archive_dir / f"{analysis.agent_key}.md.week-{week_key}"
        with open(archive_file, "w", encoding="utf-8") as f:
            f.write(f"# Archived Daily Entries - Week of {week_key}\n\n")
            f.write(f"**Agent:** {analysis.agent_key}\n")
            f.write(f"**Archived:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")

            ##Loop purpose: Write each archived entry
            for entry in sorted(entries, key=lambda e: e.date):
                f.write(entry.content)
                f.write("\n---\n\n")

        ##Action purpose: Insert weekly summary into log (before daily entries section)
        if "## DAILY ENTRIES" in content:
            parts = content.split("## DAILY ENTRIES")
            content = parts[0] + weekly_summary + "\n## DAILY ENTRIES" + parts[1]

        ##Action purpose: Remove archived daily entries from content
        for entry in entries:
            content = content.replace(entry.content, "")

    ##Action purpose: Write updated log
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(content)

    ##Action purpose: Return success
    return True, f"Archived {len(analysis.archival_candidates)} daily entries from {len(weeks)} weeks"


##Function purpose: Archive weekly summaries and generate monthly summary
def archive_weekly_summaries(
    log_path: Path, analysis: LogAnalysis, archive_base_path: Path, month_date: datetime
) -> tuple[bool, str]:
    """
    ##Function purpose: Archive weekly summaries when new month starts, generate monthly summary.

    Args:
        log_path: Path to agent log file
        analysis: LogAnalysis object
        archive_base_path: Base path for archives
        month_date: Month to archive (datetime with day=1)

    Returns:
        Tuple of (success: bool, message: str)
    """
    ##Action purpose: Filter weekly summaries for the month
    month_summaries = [
        s for s in analysis.week_summaries if s.date.year == month_date.year and s.date.month == month_date.month
    ]

    ##Condition purpose: Check if any summaries to archive
    if not month_summaries:
        return True, "No weekly summaries to archive"

    ##Action purpose: Generate monthly summary
    monthly_summary = generate_monthly_summary(month_summaries, month_date)

    ##Action purpose: Read current log
    with open(log_path, encoding="utf-8") as f:
        content = f.read()

    ##Action purpose: Insert monthly summary (after MONTH SUMMARIES header)
    if "## MONTH SUMMARIES" in content:
        parts = content.split("## MONTH SUMMARIES", 1)
        ##Action purpose: Insert as first month summary, preserving all existing content after the header
        rest = parts[1]
        ##Condition purpose: Strip leading newlines before existing content
        rest_stripped = rest.lstrip("\n")
        content = parts[0] + "## MONTH SUMMARIES\n" + monthly_summary + "\n" + rest_stripped

    ##Action purpose: Create archive for weekly summaries
    archive_date = datetime.now().strftime("%Y-%m-%d")
    archive_dir = archive_base_path / archive_date
    archive_dir.mkdir(parents=True, exist_ok=True)

    month_key = month_date.strftime("%Y-%m")
    archive_file = archive_dir / f"{analysis.agent_key}.md.month-{month_key}"

    with open(archive_file, "w", encoding="utf-8") as f:
        f.write(f"# Archived Weekly Summaries - {month_date.strftime('%B %Y')}\n\n")
        f.write(f"**Agent:** {analysis.agent_key}\n")
        f.write(f"**Archived:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")

        for summary in month_summaries:
            f.write(summary.content)
            f.write("\n---\n\n")

    ##Action purpose: Remove archived weekly summaries from log
    for summary in month_summaries:
        content = content.replace(summary.content, "")

    ##Action purpose: Write updated log
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(content)

    return True, f"Archived {len(month_summaries)} weekly summaries, generated monthly summary"


def scan_all_agent_logs(devdocs_path: Path) -> list[LogAnalysis]:
    """
    ##Function purpose: Analyze all agent logs in .devdocs/AGENT_LOGS/.

    Args:
        devdocs_path: Path to .devdocs/ folder

    Returns:
        List of LogAnalysis objects for all agent logs
    """
    ##Action purpose: Define agent logs path
    agent_logs_path = devdocs_path / "AGENT_LOGS"

    ##Condition purpose: Check if folder exists
    if not agent_logs_path.exists():
        return []

    ##Action purpose: Initialize results list
    analyses = []

    ##Loop purpose: Scan all group folders
    for group_folder in agent_logs_path.iterdir():
        if group_folder.is_dir():
            ##Loop purpose: Scan all agent logs in group
            for log_file in group_folder.glob("*.md"):
                ##Condition purpose: Skip template files
                if "TEMPLATE" in log_file.name:
                    continue

                ##Action purpose: Extract agent key from filename
                agent_key = log_file.stem

                ##Action purpose: Analyze log
                analysis = analyze_agent_log(log_file, agent_key)
                analyses.append(analysis)

    return analyses
