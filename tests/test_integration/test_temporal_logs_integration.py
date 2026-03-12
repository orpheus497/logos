from datetime import datetime, timedelta
from unittest.mock import patch

from logos.core.temporal_logs import (
    analyze_agent_log,
    archive_daily_entries,
    archive_weekly_summaries,
)


def test_temporal_log_lifecycle_integration(tmp_path):
    """Test the complete lifecycle of temporal log management."""
    # Setup test workspace
    devdocs = tmp_path / ".devdocs"
    devdocs.mkdir()
    agent_logs = devdocs / "AGENT_LOGS" / "group_a"
    agent_logs.mkdir(parents=True)
    archive = devdocs / ".archive"
    archive.mkdir()

    agent_key = "A1"
    log_path = agent_logs / f"{agent_key}.md"

    # Fixed "now" so archival cutoff (>7 days) is deterministic
    now = datetime(2023, 10, 27, 12, 0, 0)
    log_content = f"# Agent {agent_key} - Working Log\n\n## DAILY ENTRIES\n\n"

    # Add 11 entries: days 10..0 relative to `now`
    for i in range(10, -1, -1):
        entry_date = now - timedelta(days=i)
        date_str = entry_date.strftime("%Y-%m-%d")
        log_content += f"### {date_str}\n\n"
        log_content += "**Work Performed:**\n- Completed task X\n\n"
        log_content += f"**Files Modified:**\n- `file_{i}.py`\n\n"

    log_path.write_text(log_content)

    # Patch datetime.now() inside temporal_logs so the cutoff is relative to our fixed `now`
    with patch("logos.core.temporal_logs.datetime", wraps=datetime) as mock_dt:
        mock_dt.now.return_value = now

        # 1. Analyze agent log
        analysis = analyze_agent_log(log_path, agent_key)

    assert analysis.agent_key == agent_key
    assert len(analysis.daily_entries) == 11
    assert analysis.needs_archival is True
    # The oldest 4 entries (days 10, 9, 8, 7 ago) should be archival candidates
    assert len(analysis.archival_candidates) == 4

    # 2. Archive daily entries (generates weekly summary)
    success, _msg = archive_daily_entries(log_path, analysis, archive)
    assert success is True

    # Verify log content updated
    updated_content = log_path.read_text()
    assert "## WEEKLY SUMMARY" in updated_content
    assert "## DAILY ENTRIES" in updated_content

    # 3. Simulate multiple weekly summaries and trigger monthly archival
    # Re-write the log to have weekly summaries and no daily entries to simplify
    month_date = now.replace(day=1)
    prev_month_date = (month_date - timedelta(days=1)).replace(day=1)

    week1_start = prev_month_date
    week2_start = prev_month_date + timedelta(days=7)

    log_content = f"# Agent {agent_key} - Working Log\n\n## MONTH SUMMARIES\n\n## WEEKLY SUMMARY\n"
    log_content += (
        f"**Week of {week1_start.strftime('%Y-%m-%d')} to {(week1_start + timedelta(days=6)).strftime('%Y-%m-%d')}**\n"
    )
    log_content += "**Accomplishments:**\n- Week 1 work\n\n## WEEKLY SUMMARY\n"
    log_content += (
        f"**Week of {week2_start.strftime('%Y-%m-%d')} to {(week2_start + timedelta(days=6)).strftime('%Y-%m-%d')}**\n"
    )
    log_content += "**Accomplishments:**\n- Week 2 work\n\n"

    log_path.write_text(log_content)

    # Re-analyze
    analysis2 = analyze_agent_log(log_path, agent_key)
    assert len(analysis2.week_summaries) == 2

    # Archive weekly summaries to create a monthly summary
    success, _msg = archive_weekly_summaries(log_path, analysis2, archive, prev_month_date)
    assert success is True

    final_content = log_path.read_text()
    assert "## MONTH SUMMARIES" in final_content
    assert f"### {prev_month_date.strftime('%B %Y')} Summary" in final_content
    assert "Week 1 work" in final_content
    assert "Week 2 work" in final_content
    # The individual weekly summaries should be removed
    assert "**Week of" not in final_content
