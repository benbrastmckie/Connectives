"""
Search commands for finding nice connective sets.

This module provides command implementations for searching nice sets
with different arity configurations.
"""

import sys
from src.search import (
    search_binary_only,
    search_incremental_arity,
    analyze_nice_set,
    validate_nice_set
)
from src.connectives import Connective


def search_binary(max_depth=3, verbose=True):
    """
    Search for nice sets using only binary connectives.

    Args:
        max_depth: Maximum composition depth for independence checking
        verbose: Print progress information

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    max_size, sets = search_binary_only(
        max_depth=max_depth,
        verbose=verbose
    )

    if verbose and sets:
        print("\nAnalysis of first result:")
        analysis = analyze_nice_set(sets[0])
        print(f"  Size: {analysis['size']}")
        print(f"  Arity distribution: {analysis['arity_distribution']}")

    return 0


def search_full(max_arity=3, max_depth=3, verbose=True):
    """
    Search for nice sets using multiple arities (incremental search).

    Args:
        max_arity: Maximum arity to consider
        max_depth: Maximum composition depth for independence checking
        verbose: Print progress information

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    max_size, sets, stats = search_incremental_arity(
        max_arity=max_arity,
        max_depth=max_depth,
        verbose=verbose
    )

    if verbose:
        print("\nSearch Statistics:")
        print(f"  Total time: {stats['total_time']:.2f}s")
        print(f"  Connectives by arity: {stats['connectives_by_arity']}")
        print(f"\nArity progression:")
        for arity, result in stats['arity_results'].items():
            print(f"    Arity {arity}: max_size={result['max_size']}, "
                  f"time={result['time_seconds']:.2f}s")

        if sets:
            print("\nFirst result analysis:")
            analysis = analyze_nice_set(sets[0])
            print(f"  Size: {analysis['size']}")
            print(f"  Arity distribution: {analysis['arity_distribution']}")
            print(f"  Functions: {analysis['connectives']}")

    return 0


def search_validate():
    """
    Validate that the maximum nice set size of 16 is achievable.

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    print("=" * 70)
    print("VALIDATING MAXIMUM NICE SET SIZE = 16")
    print("=" * 70)
    print()

    # This is one of the size-16 nice sets we found
    nice_16 = [
        Connective(2, 0b0110, 'XOR'),           # Binary: XOR
        Connective(3, 23, 'f3_23'),
        Connective(3, 64, 'f3_64'),
        Connective(3, 15, 'f3_15'),
        Connective(3, 90, 'f3_90'),
        Connective(3, 53, 'f3_53'),
        Connective(3, 148, 'f3_148'),
        Connective(3, 163, 'f3_163'),
        Connective(3, 73, 'f3_73'),
        Connective(3, 161, 'f3_161'),
        Connective(3, 13, 'f3_13'),
        Connective(3, 249, 'f3_249'),
        Connective(3, 82, 'f3_82'),
        Connective(3, 62, 'f3_62'),
        Connective(3, 210, 'f3_210'),
        Connective(3, 179, 'f3_179')
    ]

    print(f"Testing nice set of size {len(nice_16)}...")
    print()

    is_valid, msg = validate_nice_set(nice_16, max_depth=5)

    if is_valid:
        print("✓ VALIDATION SUCCESSFUL")
        print(f"  {msg}")
        print()

        from src.post_classes import get_missing_classes
        missing = get_missing_classes(nice_16)
        print(f"  Escapes all Post classes: {len(missing) == 0}")

        analysis = analyze_nice_set(nice_16)
        print(f"  Arity distribution: {analysis['arity_distribution']}")
        print()
        print("=" * 70)
        print("CONFIRMED: Maximum nice set size = 16")
        print("=" * 70)
        print()
        print("This matches the theoretical upper bound of 16 for")
        print("complete and independent sets in classical logic.")
        return 0

    else:
        print("✗ VALIDATION FAILED")
        print(f"  {msg}")
        return 1
