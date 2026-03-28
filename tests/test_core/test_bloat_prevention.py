from logos.core.bloat_prevention import (
    analyze_agent_log_sizes,
    analyze_bloat,
    calculate_devdocs_size,
    find_oversized_files,
    find_stale_files,
    generate_health_report,
)


def test_calculate_devdocs_size(tmp_path):
    """##Function purpose: Verify calculate_devdocs_size returns 0 for empty path."""
    assert calculate_devdocs_size(tmp_path) == 0.0


def test_find_oversized_files(tmp_path):
    """##Function purpose: Verify find_oversized_files returns empty list for empty path."""
    assert find_oversized_files(tmp_path) == []


def test_find_stale_files(tmp_path):
    """##Function purpose: Verify find_stale_files returns empty list for empty path."""
    assert find_stale_files(tmp_path) == []


def test_analyze_agent_log_sizes(tmp_path):
    """##Function purpose: Verify analyze_agent_log_sizes returns empty dict for empty path."""
    assert analyze_agent_log_sizes(tmp_path) == {}


def test_calculate_devdocs_size_file_at_path(tmp_path):
    """##Function purpose: Verify calculate_devdocs_size returns 0 when path is a regular file."""
    file_path = tmp_path / ".devdocs"
    file_path.write_text("not a directory")
    assert calculate_devdocs_size(file_path) == 0.0


def test_find_oversized_files_file_at_path(tmp_path):
    """##Function purpose: Verify find_oversized_files returns empty list when path is a regular file."""
    file_path = tmp_path / ".devdocs"
    file_path.write_text("not a directory")
    assert find_oversized_files(file_path) == []


def test_find_stale_files_file_at_path(tmp_path):
    """##Function purpose: Verify find_stale_files returns empty list when path is a regular file."""
    file_path = tmp_path / ".devdocs"
    file_path.write_text("not a directory")
    assert find_stale_files(file_path) == []


def test_analyze_agent_log_sizes_file_at_path(tmp_path):
    """##Function purpose: Verify analyze_agent_log_sizes returns empty dict when AGENT_LOGS path is a regular file."""
    devdocs = tmp_path / ".devdocs"
    devdocs.mkdir()
    agent_logs_file = devdocs / "AGENT_LOGS"
    agent_logs_file.write_text("not a directory")
    assert analyze_agent_log_sizes(devdocs) == {}


def test_analyze_bloat(tmp_path):
    """##Function purpose: Verify analyze_bloat returns low risk for empty devdocs."""
    analysis = analyze_bloat(tmp_path)
    assert analysis.total_size_mb == 0.0
    assert analysis.risk_level == "LOW"


def test_generate_health_report(tmp_path):
    """##Function purpose: Verify generate_health_report returns formatted health report."""
    analysis = analyze_bloat(tmp_path)
    report = generate_health_report(analysis)
    assert "HEALTH REPORT" in report
    assert "✅" in report
