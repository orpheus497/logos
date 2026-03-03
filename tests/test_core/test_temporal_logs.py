from datetime import datetime, timedelta

from logos.core.temporal_logs import (
    LogSection,
    analyze_agent_log,
    generate_monthly_summary,
    generate_weekly_summary,
    parse_agent_log,
)


def test_parse_agent_log(tmp_path):
    """##Function purpose: Verify parse_agent_log extracts sections from log file."""
    log_file = tmp_path / "A1.md"
    log_file.write_text("### 2026-02-19\nContent here")
    sections = parse_agent_log(log_file)
    assert len(sections) == 1
    assert sections[0].section_type == "daily_entry"


def test_analyze_agent_log(tmp_path):
    """##Function purpose: Verify analyze_agent_log returns correct analysis for agent."""
    log_file = tmp_path / "A1.md"
    old_date = (datetime.now() - timedelta(days=8)).strftime("%Y-%m-%d")
    log_file.write_text(f"### {old_date}\nContent here")
    analysis = analyze_agent_log(log_file, "A1")
    assert analysis.agent_key == "A1"
    assert analysis.needs_archival


def test_generate_weekly_summary():
    """##Function purpose: Verify generate_weekly_summary includes daily entry content."""
    sections = [
        LogSection("daily_entry", datetime.now(), "**Work Performed:**\n- Tested things", "### 2026-02-19", 0, 1)
    ]
    summary = generate_weekly_summary(sections, datetime.now())
    assert "Tested things" in summary


def test_generate_monthly_summary():
    """##Function purpose: Verify generate_monthly_summary includes weekly summary content."""
    sections = [
        LogSection("week_summary", datetime.now(), "**Accomplishments:**\n- Great success", "**Week of...**", 0, 1)
    ]
    summary = generate_monthly_summary(sections, datetime.now())
    assert "Great success" in summary
