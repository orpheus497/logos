##Script function and purpose: .devdocs bloat detection and prevention utilities

"""
Provides utilities for Orchestrator to detect and prevent .devdocs/ folder bloat.

- Calculate folder and file sizes
- Identify oversized files
- Detect stale content
- Generate health reports
- Recommend cleanup actions
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path

##Action purpose: Define bloat thresholds
WARN_SIZE_MB = 10
CRITICAL_SIZE_MB = 25
FILE_WARN_KB = 500
FILE_CRITICAL_KB = 1024
STALE_DAYS = 7
TASK_STALE_DAYS = 14
COMPLETED_TASK_ARCHIVE_DAYS = 30


##Class purpose: Bloat analysis result container
@dataclass
class BloatAnalysis:
    """
    ##Class purpose: Structured bloat analysis results.

    Attributes:
        total_size_mb: Total size of .devdocs/ folder in MB
        file_count: Number of files in .devdocs/
        oversized_files: List of files exceeding size thresholds
        stale_files: List of files not modified in >STALE_DAYS
        risk_level: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL"
        recommendations: List of recommended cleanup actions
        agent_log_sizes: Dict of agent_key -> size_kb
        largest_logs: Top 5 largest agent logs
    """

    total_size_mb: float
    file_count: int
    oversized_files: list[dict[str, any]]
    stale_files: list[dict[str, any]]
    risk_level: str
    recommendations: list[str]
    agent_log_sizes: dict[str, float]
    largest_logs: list[dict[str, any]]


##Function purpose: Calculate total .devdocs/ folder size
def calculate_devdocs_size(devdocs_path: Path = Path(".devdocs")) -> float:
    """
    ##Function purpose: Recursively calculate .devdocs/ folder size.

    Args:
        devdocs_path: Path to .devdocs/ folder

    Returns:
        Total size in megabytes (float)
    """
    ##Condition purpose: Check if folder exists
    if not devdocs_path.exists():
        return 0.0

    total_bytes = 0

    ##Loop purpose: Sum size of all files recursively
    for file_path in devdocs_path.rglob("*"):
        ##Condition purpose: Skip directories, count files only
        if file_path.is_file():
            total_bytes += file_path.stat().st_size

    ##Action purpose: Convert bytes to megabytes
    return total_bytes / (1024 * 1024)


##Function purpose: Find files exceeding size thresholds
def find_oversized_files(devdocs_path: Path = Path(".devdocs")) -> list[dict[str, any]]:
    """
    ##Function purpose: Scan .devdocs/ for files exceeding size limits.

    Args:
        devdocs_path: Path to .devdocs/ folder

    Returns:
        List of dicts: [{"path": str, "size_kb": float, "severity": str}, ...]
    """
    oversized = []

    ##Condition purpose: Check if folder exists
    if not devdocs_path.exists():
        return oversized

    ##Loop purpose: Check each file against thresholds
    for file_path in devdocs_path.rglob("*.md"):
        ##Condition purpose: Skip archive folder (not included in size checks)
        if ".archive" in str(file_path):
            continue

        size_kb = file_path.stat().st_size / 1024

        ##Condition purpose: Check if file exceeds warning threshold
        if size_kb > FILE_WARN_KB:
            severity = "CRITICAL" if size_kb > FILE_CRITICAL_KB else "WARN"
            oversized.append(
                {"path": str(file_path.relative_to(devdocs_path)), "size_kb": round(size_kb, 2), "severity": severity}
            )

    return oversized


##Function purpose: Find files not modified recently
def find_stale_files(devdocs_path: Path = Path(".devdocs")) -> list[dict[str, any]]:
    """
    ##Function purpose: Find files not modified in >STALE_DAYS.

    Args:
        devdocs_path: Path to .devdocs/ folder

    Returns:
        List of dicts: [{"path": str, "age_days": int, "last_modified": str}, ...]
    """
    stale = []
    cutoff_date = datetime.now() - timedelta(days=STALE_DAYS)

    ##Condition purpose: Check if folder exists
    if not devdocs_path.exists():
        return stale

    ##Loop purpose: Check modification time of each file
    for file_path in devdocs_path.rglob("*.md"):
        ##Condition purpose: Skip DEV_STATE.md (never stale) and archive
        if file_path.name == "DEV_STATE.md" or ".archive" in str(file_path):
            continue

        modified_time = datetime.fromtimestamp(file_path.stat().st_mtime)

        ##Condition purpose: Check if file is older than cutoff
        if modified_time < cutoff_date:
            age_days = (datetime.now() - modified_time).days
            stale.append(
                {
                    "path": str(file_path.relative_to(devdocs_path)),
                    "age_days": age_days,
                    "last_modified": modified_time.strftime("%Y-%m-%d %H:%M"),
                }
            )

    return stale


##Function purpose: Analyze agent log sizes
def analyze_agent_log_sizes(devdocs_path: Path = Path(".devdocs")) -> dict[str, float]:
    """
    ##Function purpose: Calculate size of each agent log file.

    Args:
        devdocs_path: Path to .devdocs/ folder

    Returns:
        Dict mapping agent_key to size in KB
    """
    agent_logs_path = devdocs_path / "AGENT_LOGS"
    log_sizes = {}

    ##Condition purpose: Check if folder exists
    if not agent_logs_path.exists():
        return log_sizes

    ##Loop purpose: Scan all group folders
    for group_folder in agent_logs_path.iterdir():
        if group_folder.is_dir():
            ##Loop purpose: Measure each agent log
            for log_file in group_folder.glob("*.md"):
                ##Condition purpose: Skip templates
                if "TEMPLATE" in log_file.name:
                    continue

                agent_key = log_file.stem
                size_kb = log_file.stat().st_size / 1024
                log_sizes[agent_key] = round(size_kb, 2)

    return log_sizes


##Function purpose: Run complete bloat analysis
def analyze_bloat(devdocs_path: Path = Path(".devdocs")) -> BloatAnalysis:
    """
    ##Function purpose: Comprehensive .devdocs/ health analysis.

    Args:
        devdocs_path: Path to .devdocs/ folder

    Returns:
        BloatAnalysis object with complete results
    """
    ##Action purpose: Gather all metrics
    total_size = calculate_devdocs_size(devdocs_path)
    file_count = len(list(devdocs_path.rglob("*.md"))) if devdocs_path.exists() else 0
    oversized = find_oversized_files(devdocs_path)
    stale = find_stale_files(devdocs_path)
    agent_log_sizes = analyze_agent_log_sizes(devdocs_path)

    ##Action purpose: Find largest logs
    largest_logs = sorted(
        [{"agent": k, "size_kb": v} for k, v in agent_log_sizes.items()], key=lambda x: x["size_kb"], reverse=True
    )[:5]

    ##Action purpose: Assess risk level
    risk_level = "LOW"
    if total_size > WARN_SIZE_MB or len(oversized) > 0:
        risk_level = "MEDIUM"
    if total_size > CRITICAL_SIZE_MB or len(oversized) > 5 or any(f["severity"] == "CRITICAL" for f in oversized):
        risk_level = "CRITICAL"

    ##Action purpose: Generate recommendations
    recommendations = []

    if len(stale) > 0:
        recommendations.append(f"Archive {len(stale)} stale files (>{STALE_DAYS} days old)")

    if len(oversized) > 0:
        recommendations.append(f"Review {len(oversized)} oversized files for consolidation")
        for file in oversized:
            if file["severity"] == "CRITICAL":
                recommendations.append(f"URGENT: {file['path']} is {file['size_kb']}KB (>{FILE_CRITICAL_KB}KB)")

    if total_size > WARN_SIZE_MB:
        recommendations.append(
            f"Total .devdocs/ size is {round(total_size, 2)}MB (warning threshold: {WARN_SIZE_MB}MB)"
        )

    if total_size > CRITICAL_SIZE_MB:
        recommendations.append(
            f"CRITICAL: Total size {round(total_size, 2)}MB exceeds {CRITICAL_SIZE_MB}MB - immediate archival required"
        )

    if not recommendations:
        recommendations.append("No bloat detected - .devdocs/ health is good")

    ##Action purpose: Return structured analysis
    return BloatAnalysis(
        total_size_mb=round(total_size, 2),
        file_count=file_count,
        oversized_files=oversized,
        stale_files=stale,
        risk_level=risk_level,
        recommendations=recommendations,
        agent_log_sizes=agent_log_sizes,
        largest_logs=largest_logs,
    )


##Function purpose: Generate health report text for Orchestrator
def generate_health_report(analysis: BloatAnalysis) -> str:
    """
    ##Function purpose: Create formatted health report from analysis.

    Args:
        analysis: BloatAnalysis object from analyze_bloat()

    Returns:
        Formatted markdown health report
    """
    ##Action purpose: Determine status emoji
    status_emoji = {"LOW": "✅", "MEDIUM": "⚠️", "HIGH": "🔶", "CRITICAL": "🚨"}

    ##Action purpose: Build report
    report = f"""

🔍 .DEVDOCS/ HEALTH REPORT

**Overall Status:** {status_emoji[analysis.risk_level]} **{analysis.risk_level}**

**Metrics:**
- Total .devdocs/ size: {analysis.total_size_mb} MB
- File count: {analysis.file_count} files
- Oversized files: {len(analysis.oversized_files)}
- Stale files: {len(analysis.stale_files)}

**Largest Agent Logs:**
"""

    ##Loop purpose: List largest logs
    for log in analysis.largest_logs:
        report += f"- {log['agent']}: {log['size_kb']} KB\n"

    report += "\n**Issues Detected:**\n"

    ##Condition purpose: List oversized files
    if analysis.oversized_files:
        report += "\n*Oversized Files:*\n"
        for file in analysis.oversized_files[:10]:  # Top 10
            report += f"- [{file['severity']}] {file['path']}: {file['size_kb']} KB\n"

    ##Condition purpose: List stale files
    if analysis.stale_files:
        report += "\n*Stale Files (not modified in >{STALE_DAYS} days):*\n"
        for file in analysis.stale_files[:10]:  # Top 10
            report += f"- {file['path']}: {file['age_days']} days old (last: {file['last_modified']})\n"

    ##Condition purpose: Add recommendations
    report += "\n**Recommendations:**\n"
    for i, rec in enumerate(analysis.recommendations, 1):
        report += f"{i}. {rec}\n"

    return report.strip()
