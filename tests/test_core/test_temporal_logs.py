from datetime import datetime

from logos.core.temporal_logs import (
    LogSection,
    analyze_agent_log,
    generate_monthly_summary,
    generate_weekly_summary,
    parse_agent_log,
)


def test_parse_agent_log(tmp_path):
    log_file = tmp_path / "A1.md"
    log_file.write_text("### 2026-02-19\nContent here")
    sections = parse_agent_log(log_file)
    assert len(sections) == 1
    assert sections[0].section_type == "daily_entry"

def test_analyze_agent_log(tmp_path):
    log_file = tmp_path / "A1.md"
    log_file.write_text("### 2026-02-19\nContent here")
    analysis = analyze_agent_log(log_file, "A1")
    assert analysis.agent_key == "A1"
    assert analysis.needs_archival

def test_generate_weekly_summary():
    sections = [LogSection("daily_entry", datetime.now(), "**Work Performed:**\n- Tested things", "### 2026-02-19", 0, 1)]
    summary = generate_weekly_summary(sections, datetime.now())
    assert "Tested things" in summary

def test_generate_monthly_summary():
    sections = [LogSection("week_summary", datetime.now(), "**Accomplishments:**\n- Great success", "**Week of...**", 0, 1)]
    summary = generate_monthly_summary(sections, datetime.now())
    assert "Great success" in summary
