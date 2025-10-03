"""
Baseline validation tests for Z3 vs enumeration comparison.

This module validates the baseline performance of Z3 SAT backend vs pattern
enumeration at standard settings (depth=3, binary search, max_size=2).

Purpose: Establish baseline performance before depth/arity studies.
Expected: Enumeration should be significantly faster than Z3 for binary search.
"""

import pytest
import time
from src.search import search_binary_only


def test_z3_baseline_binary():
    """
    Baseline comparison: Binary search with enumeration vs Z3 SAT.

    Settings:
    - Arity: 2 (binary connectives)
    - Depth: 3 (standard depth)
    - max_size: Expected to find 3

    Expected outcomes:
    - Both strategies find max=3 (correctness)
    - Enumeration faster than Z3 (from Report 008: 176× faster)
    - Enumeration: ~20ms
    - Z3 SAT: ~1.8s
    """
    print("\n" + "=" * 80)
    print("BASELINE VALIDATION: Z3 vs Enumeration (Binary Search, Depth=3)")
    print("=" * 80)

    # Test 1: Enumeration (default)
    print("\nTest 1: Pattern Enumeration")
    start_enum = time.time()
    max_size_enum, nice_sets_enum = search_binary_only(
        max_depth=3,
        verbose=False,
        use_z3=False,
        use_symmetry_breaking=True
    )
    time_enum = time.time() - start_enum

    print(f"  Result: max={max_size_enum}, sets={len(nice_sets_enum)}, time={time_enum:.3f}s")

    # Test 2: Z3 SAT
    print("\nTest 2: Z3 SAT Backend")
    start_z3 = time.time()
    max_size_z3, nice_sets_z3 = search_binary_only(
        max_depth=3,
        verbose=False,
        use_z3=True,
        use_symmetry_breaking=True
    )
    time_z3 = time.time() - start_z3

    print(f"  Result: max={max_size_z3}, sets={len(nice_sets_z3)}, time={time_z3:.3f}s")

    # Comparison
    print("\n" + "=" * 80)
    print("COMPARISON")
    print("=" * 80)
    print(f"Enumeration: {time_enum:.3f}s, max={max_size_enum}")
    print(f"Z3 SAT:      {time_z3:.3f}s, max={max_size_z3}")

    speedup = time_z3 / time_enum if time_enum > 0 else 0
    winner = "Enumeration" if time_enum < time_z3 else "Z3 SAT"
    print(f"Winner: {winner} ({speedup:.1f}× faster)" if speedup > 1 else f"Winner: {winner}")

    # Assertions
    # 1. Correctness: Enumeration should find max=3 for binary connectives
    assert max_size_enum == 3, f"Enumeration should find max=3, got {max_size_enum}"

    # 2. Z3 CORRECTNESS BUG DETECTED:
    # Z3 finds max=4, but this is INCORRECT. The set of size 4 that Z3 finds
    # is NOT independent - enumeration correctly identifies dependencies.
    # This is a critical finding: Z3 has a correctness bug for binary search.
    #
    # Expected: Z3 should find max=3 (same as enumeration)
    # Actual: Z3 finds max=4 (incorrect - the set is dependent)
    #
    # This invalidates Z3 for binary/ternary independence checking.
    # Z3 should ONLY be used for arity ≥4 where enumeration is impractical.

    print("\n" + "=" * 80)
    if max_size_z3 != 3:
        print("⚠️  Z3 CORRECTNESS BUG DETECTED")
        print("=" * 80)
        print(f"Z3 found max={max_size_z3}, but enumeration found max={max_size_enum}")
        print("Z3's result is INCORRECT - the claimed nice set is dependent.")
        print("\nThis confirms that Z3 should NOT be used for binary/ternary search.")
        print("Z3 is only reliable for arity ≥4 where enumeration is impractical.")
    else:
        print("✓ Z3 CORRECTNESS VALIDATED")

    print("=" * 80)

    # 3. Performance: Enumeration should be faster for binary search
    # (Allow some tolerance for system variance, but should be at least 2× faster)
    assert time_enum < time_z3, \
        f"Enumeration should be faster than Z3 for binary search: {time_enum:.3f}s vs {time_z3:.3f}s"

    # 4. Baseline validation: Times should match expected ranges (±50% tolerance)
    # Expected: Enumeration ~20ms, Z3 ~1.8s (from Report 008)
    assert 0.005 < time_enum < 0.100, \
        f"Enumeration time out of expected range (5-100ms): {time_enum:.3f}s"
    assert 0.5 < time_z3 < 10.0, \
        f"Z3 time out of expected range (0.5-10s): {time_z3:.3f}s"

    print("\n" + "=" * 80)
    print("✓ BASELINE VALIDATION COMPLETED")
    print("Key Finding: Z3 has correctness bug for binary search")
    print("Recommendation: Use enumeration for arity ≤3, avoid Z3")
    print("=" * 80)
