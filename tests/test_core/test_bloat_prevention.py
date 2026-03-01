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
