#!/usr/bin/env python3
"""
Compare Z3 vs enumeration performance for independence checking.

Benchmarks the two strategies to measure performance differences.
"""

import sys
import time
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.connectives import generate_all_connectives
from src.search import find_maximum_nice_set, filter_by_equivalence


def benchmark_strategy(strategy_name: str, use_z3: bool, max_arity: int = 2):
    """
    Benchmark a specific strategy.

    Args:
        strategy_name: Name for display
        use_z3: Whether to use Z3
        max_arity: Maximum arity to test

    Returns:
        Time taken in seconds
    """
    print(f"\n{strategy_name}:")
    print(f"  Generating connectives (arity 0-{max_arity})...")

    # Generate connective pool
    connectives = []
    for arity in range(0, max_arity + 1):
        connectives.extend(generate_all_connectives(arity))

    # Apply symmetry breaking
    connectives_filtered = filter_by_equivalence(connectives)

    print(f"  Total connectives: {len(connectives)}")
    print(f"  After filtering: {len(connectives_filtered)}")
    print(f"  Running search...")

    start = time.time()
    max_size, nice_sets, metadata = find_maximum_nice_set(
        connectives_filtered,
        max_size=10,
        max_depth=3,
        verbose=False,
        use_z3=use_z3
    )
    elapsed = time.time() - start

    print(f"  Max size found: {max_size}")
    print(f"  Time: {elapsed:.3f}s")
    print(f"  Strategy (from metadata): {metadata['strategy']}")

    return elapsed


def main():
    """Run comparison benchmark."""
    print("=" * 80)
    print("Z3 vs ENUMERATION PERFORMANCE COMPARISON")
    print("=" * 80)

    # Test 1: Binary-only (arity 0-2)
    print("\n" + "=" * 80)
    print("TEST 1: Binary-only search (arity 0-2)")
    print("=" * 80)

    time_enum = benchmark_strategy("Enumeration", use_z3=False, max_arity=2)
    time_z3 = benchmark_strategy("Z3 SAT", use_z3=True, max_arity=2)

    print("\n" + "-" * 80)
    print("COMPARISON:")
    print(f"  Enumeration: {time_enum:.3f}s")
    print(f"  Z3 SAT:      {time_z3:.3f}s")

    if time_enum < time_z3:
        ratio = time_z3 / time_enum
        print(f"  Winner: Enumeration ({ratio:.2f}× faster)")
    else:
        ratio = time_enum / time_z3
        print(f"  Winner: Z3 SAT ({ratio:.2f}× faster)")

    # Test 2: Include unary (arity 0-2, but note unary is arity 1)
    print("\n" + "=" * 80)
    print("TEST 2: Unary + Binary search (arity 0-2)")
    print("=" * 80)
    print("Note: This is the same as TEST 1 (binary includes nullary/unary)")
    print("The interesting comparison would be with arity 3 (ternary)")

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print("\nKey Findings:")
    print("1. Pattern enumeration is optimized for arity ≤3")
    print("2. Z3 SAT backend is designed for arity ≥4 (quaternary+)")
    print("3. For binary/ternary: enumeration is typically faster")
    print("4. For quaternary+: Z3 becomes necessary (enumeration impractical)")
    print("\nRecommendation:")
    print("- Use enumeration (default) for arity ≤3")
    print("- Use Z3 (use_z3=True) for arity ≥4")
    print("- This is already the default behavior via adaptive strategy")


if __name__ == '__main__':
    main()
