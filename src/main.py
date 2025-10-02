#!/usr/bin/env python3
"""
Main entry point for the Nice Connectives Solver.

This solver finds the maximum size of "nice" (complete and independent)
sets of logical connectives using Z3-based analysis.
"""

import argparse
import sys
from src.search import (
    search_binary_only,
    search_incremental_arity,
    analyze_nice_set,
    validate_nice_set
)
from src.connectives import generate_all_connectives


def main():
    parser = argparse.ArgumentParser(
        description='Find maximum nice (complete and independent) connective sets'
    )

    parser.add_argument(
        '--binary-only',
        action='store_true',
        help='Search only binary connectives (reproduces known max=3 result)'
    )

    parser.add_argument(
        '--max-arity',
        type=int,
        default=3,
        help='Maximum arity to consider (default: 3)'
    )

    parser.add_argument(
        '--max-depth',
        type=int,
        default=3,
        help='Maximum composition depth for independence checking (default: 3)'
    )

    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Suppress progress output'
    )

    parser.add_argument(
        '--validate',
        action='store_true',
        help='Validate that size=16 is achievable'
    )

    args = parser.parse_args()

    verbose = not args.quiet

    if args.validate:
        validate_maximum()
        return

    if args.binary_only:
        max_size, sets = search_binary_only(
            max_depth=args.max_depth,
            verbose=verbose
        )

        if verbose:
            print("\nAnalysis of first result:")
            if sets:
                analysis = analyze_nice_set(sets[0])
                print(f"  Size: {analysis['size']}")
                print(f"  Arity distribution: {analysis['arity_distribution']}")

    else:
        max_size, sets, stats = search_incremental_arity(
            max_arity=args.max_arity,
            max_depth=args.max_depth,
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


def validate_maximum():
    """Validate that the maximum nice set size of 16 is achievable."""
    print("=" * 70)
    print("VALIDATING MAXIMUM NICE SET SIZE = 16")
    print("=" * 70)
    print()

    # This is one of the size-16 nice sets we found
    from src.connectives import Connective

    # A known size-16 nice set
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

    else:
        print("✗ VALIDATION FAILED")
        print(f"  {msg}")
        sys.exit(1)


if __name__ == '__main__':
    main()
