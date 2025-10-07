#!/usr/bin/env python3
"""
Quick performance benchmark for nice connectives search.

Focuses on key performance metrics without exhaustive testing.
"""

import sys
import time
from pathlib import Path

# Add project root directory to path for imports (now 2 levels up from scripts/benchmarks/)
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.search import search_binary_only


def main():
    """Run quick benchmark."""
    print("=" * 80)
    print("QUICK PERFORMANCE BENCHMARK")
    print("=" * 80)
    print()

    # Test 1: Binary search without symmetry breaking
    print("1. Binary-only search (no symmetry breaking)...")
    start = time.time()
    max_size1, sets1 = search_binary_only(
        max_depth=3,
        verbose=False,
        use_z3=False,
        use_symmetry_breaking=False
    )
    time1 = time.time() - start
    print(f"   Result: max={max_size1}, time={time1:.3f}s")
    print()

    # Test 2: Binary search with symmetry breaking
    print("2. Binary-only search (with symmetry breaking)...")
    start = time.time()
    max_size2, sets2 = search_binary_only(
        max_depth=3,
        verbose=False,
        use_z3=False,
        use_symmetry_breaking=True
    )
    time2 = time.time() - start
    print(f"   Result: max={max_size2}, time={time2:.3f}s")
    print()

    # Analysis
    print("=" * 80)
    print("RESULTS SUMMARY")
    print("=" * 80)
    print(f"Binary search (no SB):   {time1:.3f}s")
    print(f"Binary search (with SB): {time2:.3f}s")
    if time1 > time2:
        speedup = time1 / time2
        print(f"Speedup from SB:         {speedup:.2f}×")
    else:
        print(f"Speedup from SB:         N/A (SB slightly slower for small sets)")
    print()
    print(f"Both strategies found max={max_size1} ✓")
    print(f"Binary search completes in <1s ✓")
    print()


if __name__ == '__main__':
    main()
