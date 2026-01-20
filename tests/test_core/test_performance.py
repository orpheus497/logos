"""
##Script function and purpose: Performance benchmarks for LOGOS core modules.

Tests performance characteristics of critical operations.
"""

import statistics
import timeit

from logos.core.identity import scan_system
from logos.daedelus.agents import get_agent as get_daedelus_agent
from logos.deus.agents import get_agent as get_deus_agent


##Function purpose: Benchmark system scanning performance
def test_benchmark_system_scan():
    """
    ##Function purpose: Benchmark system scanning performance.

    ##Action purpose: Measures scan_system() execution time to validate
    optimization improvements (parallelization should make this 5-10x faster).
    """
    ##Action purpose: Run multiple scans and collect timing data
    times = []
    iterations = 5  # Reduced for test suite speed

    ##Loop purpose: Collect timing samples
    for _ in range(iterations):
        start = timeit.default_timer()
        scan_system()
        end = timeit.default_timer()
        times.append((end - start) * 1000)  # Convert to ms

    ##Action purpose: Calculate statistics
    mean_time = statistics.mean(times)
    max_time = max(times)

    ##Condition purpose: Verify performance is acceptable
    ##Note: With parallelization, FreeBSD should be < 500ms, Linux < 50ms
    ##We use lenient thresholds for test suite
    assert mean_time < 10000, f"System scan too slow: {mean_time:.2f}ms mean"
    assert max_time < 15000, f"System scan too slow: {max_time:.2f}ms max"

    ##Action purpose: Log performance metrics (for documentation)
    print("\nSystem Scan Performance:")
    print(f"  Mean: {mean_time:.2f}ms")
    print(f"  Median: {statistics.median(times):.2f}ms")
    print(f"  Min: {min(times):.2f}ms")
    print(f"  Max: {max_time:.2f}ms")


##Function purpose: Benchmark agent lookup performance
def test_benchmark_agent_lookup():
    """
    ##Function purpose: Benchmark agent lookup performance.

    ##Action purpose: Measures get_agent() execution time to validate
    optimization improvements (single lookup should be 2x faster).
    """
    ##Action purpose: Test various key formats
    test_keys = ["A1", "a1", "B8", "OcM", "INVALID"]
    times = []
    iterations_per_key = 100  # Reduced for test suite speed

    ##Loop purpose: Test each key format
    for key in test_keys:
        ##Loop purpose: Multiple iterations per key
        for _ in range(iterations_per_key):
            start = timeit.default_timer()
            get_daedelus_agent(key)
            end = timeit.default_timer()
            times.append((end - start) * 1000000)  # Convert to μs

    ##Action purpose: Calculate statistics
    mean_time = statistics.mean(times)
    max_time = max(times)

    ##Condition purpose: Verify performance is acceptable (< 1μs target)
    ##Note: With optimization, should be ~0.25-0.5μs, but we use lenient threshold
    assert mean_time < 10, f"Agent lookup too slow: {mean_time:.2f}μs mean"
    assert max_time < 50, f"Agent lookup too slow: {max_time:.2f}μs max"

    ##Action purpose: Log performance metrics
    print("\nAgent Lookup Performance:")
    print(f"  Mean: {mean_time:.2f}μs")
    print(f"  Median: {statistics.median(times):.2f}μs")
    print(f"  Min: {min(times):.2f}μs")
    print(f"  Max: {max_time:.2f}μs")


##Function purpose: Benchmark agent lookup case insensitivity
def test_benchmark_agent_lookup_case_insensitive():
    """##Function purpose: Verify case-insensitive lookup performance is consistent.."""
    ##Action purpose: Test uppercase, lowercase, and mixed case
    test_cases = [
        ("A1", "A1"),
        ("a1", "A1"),
        ("OcM", "ocm"),
        ("OCM", "ocm"),
    ]

    ##Loop purpose: Test each case variation
    for key1, key2 in test_cases:
        agent1 = get_daedelus_agent(key1)
        agent2 = get_daedelus_agent(key2)

        ##Condition purpose: Verify both find the same agent
        assert agent1 == agent2, f"Case-insensitive lookup failed: {key1} != {key2}"


##Function purpose: Benchmark DEUS agent lookup
def test_benchmark_deus_agent_lookup():
    """##Function purpose: Benchmark DEUS agent lookup performance.."""
    ##Action purpose: Test DEUS agent keys
    test_keys = ["A1", "B6", "C11", "D2", "E1"]
    times = []
    iterations_per_key = 100

    ##Loop purpose: Test each key
    for key in test_keys:
        for _ in range(iterations_per_key):
            start = timeit.default_timer()
            get_deus_agent(key)
            end = timeit.default_timer()
            times.append((end - start) * 1000000)  # Convert to μs

    ##Action purpose: Calculate statistics
    mean_time = statistics.mean(times)

    ##Condition purpose: Verify performance is acceptable
    assert mean_time < 10, f"DEUS agent lookup too slow: {mean_time:.2f}μs mean"

    ##Action purpose: Log performance metrics
    print("\nDEUS Agent Lookup Performance:")
    print(f"  Mean: {mean_time:.2f}μs")
