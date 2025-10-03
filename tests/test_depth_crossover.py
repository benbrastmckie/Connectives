"""
Tests for depth crossover analysis.

This module tests the performance and correctness of independence checking
across different composition depths to identify empirical crossover points.
"""

import pytest
import time
from src.search import search_binary_only


# Depths to test: 1, 2, 3, 4, 5, 7, 10
FAST_DEPTHS = [1, 2, 3, 4, 5]  # Should complete in < 30 seconds
SLOW_DEPTHS = [7, 10]  # May take minutes

ALL_DEPTHS = FAST_DEPTHS + SLOW_DEPTHS


@pytest.mark.parametrize("depth", FAST_DEPTHS)
def test_depth_performance_fast(depth):
    """
    Test binary-only search performance at different depths (fast subset).

    Depth 1 finds max=5 (insufficient depth to detect all dependencies).
    Depth ≥2 finds correct max=3 for binary connectives.
    Performance should degrade exponentially with depth.

    Args:
        depth: Composition depth to test
    """
    start = time.time()

    # Run binary-only search with this depth
    max_size, nice_sets = search_binary_only(
        max_depth=depth,
        verbose=False,
        use_z3=False,
        use_symmetry_breaking=True
    )

    elapsed = time.time() - start

    # Validate correctness (depth-dependent)
    expected_max = 5 if depth == 1 else 3
    assert max_size == expected_max, f"Depth {depth} should find max={expected_max}, got {max_size}"
    assert len(nice_sets) > 0, f"Depth {depth} should find at least one nice set"

    # Log performance for analysis
    print(f"\n  Depth {depth}: {elapsed:.3f}s, max={max_size}, sets={len(nice_sets)}")

    # Timeout check (fast depths should complete in < 60 seconds)
    assert elapsed < 60, f"Depth {depth} took {elapsed:.1f}s (too slow for fast test)"


@pytest.mark.slow
@pytest.mark.parametrize("depth", SLOW_DEPTHS)
def test_depth_performance_slow(depth):
    """
    Test binary-only search performance at high depths (slow subset).

    All slow depths (≥7) should find correct max=3.
    These tests may take minutes. Only run manually, not in CI.

    Args:
        depth: Composition depth to test
    """
    start = time.time()

    # Run binary-only search with this depth
    max_size, nice_sets = search_binary_only(
        max_depth=depth,
        verbose=False,
        use_z3=False,
        use_symmetry_breaking=True
    )

    elapsed = time.time() - start

    # Validate correctness (high depths always find max=3)
    assert max_size == 3, f"Depth {depth} should find max=3, got {max_size}"
    assert len(nice_sets) > 0, f"Depth {depth} should find at least one nice set"

    # Log performance for analysis
    print(f"\n  Depth {depth}: {elapsed:.3f}s, max={max_size}, sets={len(nice_sets)}")

    # Timeout check (slow depths should complete in < 5 minutes)
    assert elapsed < 300, f"Depth {depth} took {elapsed:.1f}s (too slow even for slow test)"


def test_depth_consistency():
    """
    Validate that different depths produce consistent results.

    Depth 1 finds max=5 (insufficient).
    Depths ≥2 find correct max=3 (consistent).
    """
    results = {}

    for depth in FAST_DEPTHS:
        max_size, nice_sets = search_binary_only(
            max_depth=depth,
            verbose=False,
            use_z3=False,
            use_symmetry_breaking=True
        )
        results[depth] = max_size

    # Validate depth-dependent correctness
    assert results[1] == 5, f"Depth 1 should find max=5, got {results[1]}"

    # All depths ≥2 should find max=3
    for depth in FAST_DEPTHS[1:]:  # Skip depth 1
        assert results[depth] == 3, f"Depth {depth} should find max=3, got {results[depth]}"


def test_depth_performance_trend():
    """
    Validate that performance degrades exponentially with depth.

    Each depth should be slower than the previous (with some tolerance).
    """
    times = {}

    for depth in FAST_DEPTHS[:4]:  # Test depths 1-4 only (for speed)
        start = time.time()
        max_size, nice_sets = search_binary_only(
            max_depth=depth,
            verbose=False,
            use_z3=False,
            use_symmetry_breaking=True
        )
        elapsed = time.time() - start
        times[depth] = elapsed

    # Validate monotonic increase (with 20% tolerance for noise)
    for i in range(len(FAST_DEPTHS[:3])):
        depth1 = FAST_DEPTHS[i]
        depth2 = FAST_DEPTHS[i + 1]
        time1 = times[depth1]
        time2 = times[depth2]

        # Depth2 should be >= depth1 (or within 20% tolerance)
        assert time2 >= time1 * 0.8, \
            f"Depth {depth2} ({time2:.3f}s) should not be much faster than depth {depth1} ({time1:.3f}s)"

    print("\n  Performance trend validated:")
    for depth in sorted(times.keys()):
        print(f"    Depth {depth}: {times[depth]:.3f}s")
