#!/usr/bin/env python3
"""
Validation script for ternary search with comprehensive logging.

Runs ternary search with different depth parameters and logs results
to help resolve the 16 vs ≥42 discrepancy in documentation.
"""

import sys
import argparse
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.connectives import generate_all_connectives
from src.search import find_maximum_nice_set, filter_by_equivalence
import time


def run_validation(max_depth: int, verbose: bool = True, use_z3: bool = False,
                   use_symmetry_breaking: bool = True):
    """
    Run ternary search validation with specified depth.

    Args:
        max_depth: Maximum composition depth for independence checking
        verbose: Print detailed progress
        use_z3: Use Z3 SAT backend instead of pattern enumeration
        use_symmetry_breaking: Apply equivalence class filtering

    Returns:
        Dictionary with results and metadata
    """
    print("=" * 80)
    print(f"TERNARY SEARCH VALIDATION - Depth {max_depth}")
    print("=" * 80)
    print(f"Parameters:")
    print(f"  Composition depth: {max_depth}")
    print(f"  Strategy: {'z3_sat' if use_z3 else 'enumeration'}")
    print(f"  Symmetry breaking: {use_symmetry_breaking}")
    print()

    # Generate all connectives up to arity 3
    print("Generating connectives...")
    all_connectives = []

    for arity in [0, 1, 2, 3]:
        connectives = generate_all_connectives(arity)
        all_connectives.extend(connectives)
        print(f"  Arity {arity}: {len(connectives)} connectives")

    print(f"Total connectives: {len(all_connectives)}")
    print()

    # Apply symmetry breaking if requested
    if use_symmetry_breaking:
        print("Applying symmetry breaking...")
        filter_start = time.time()
        filtered_connectives = filter_by_equivalence(all_connectives)
        filter_time = time.time() - filter_start

        print(f"  Before filtering: {len(all_connectives)}")
        print(f"  After filtering: {len(filtered_connectives)}")
        print(f"  Reduction ratio: {len(all_connectives) / len(filtered_connectives):.2f}×")
        print(f"  Filtering time: {filter_time:.3f}s")
        print()

        search_connectives = filtered_connectives
    else:
        search_connectives = all_connectives

    # Run search
    print(f"Searching for maximum nice set (max_size=20)...")
    print()

    search_start = time.time()
    max_size, nice_sets, metadata = find_maximum_nice_set(
        search_connectives,
        max_size=20,  # Search up to size 20
        max_depth=max_depth,
        verbose=verbose,
        use_z3=use_z3
    )
    search_time = time.time() - search_start

    # Compile results
    results = {
        'max_size': max_size,
        'num_nice_sets': len(nice_sets),
        'metadata': metadata,
        'total_time': search_time,
        'symmetry_breaking': use_symmetry_breaking,
        'connectives_searched': len(search_connectives),
        'total_connectives': len(all_connectives)
    }

    # Print summary
    print()
    print("=" * 80)
    print("RESULTS SUMMARY")
    print("=" * 80)
    print(f"Maximum nice set size: {max_size}")
    print(f"Number of maximal nice sets found: {len(nice_sets)}")
    print(f"Composition depth: {metadata['composition_depth']}")
    print(f"Strategy: {metadata['strategy']}")
    print(f"Search time: {metadata['search_time']:.2f}s")
    print(f"Basis size: {metadata['basis_size']}")
    print(f"Total time (including setup): {search_time:.2f}s")
    print()

    # Show example nice sets
    if nice_sets:
        print("Example maximal nice sets:")
        for i, nice_set in enumerate(nice_sets[:3]):  # Show first 3
            print(f"\nSet {i+1}:")
            for c in nice_set:
                print(f"  - {c.name} (arity {c.arity})")

    print()
    print("=" * 80)

    return results


def compare_depths(depths: list, use_z3: bool = False, verbose: bool = False):
    """
    Compare results across multiple depths.

    Args:
        depths: List of depth values to test
        use_z3: Use Z3 SAT backend
        verbose: Print detailed progress for each search
    """
    print("=" * 80)
    print("DEPTH COMPARISON")
    print("=" * 80)
    print(f"Testing depths: {depths}")
    print(f"Strategy: {'z3_sat' if use_z3 else 'enumeration'}")
    print()

    all_results = []

    for depth in depths:
        results = run_validation(depth, verbose=verbose, use_z3=use_z3)
        all_results.append((depth, results))
        print()

    # Print comparison table
    print("=" * 80)
    print("COMPARISON TABLE")
    print("=" * 80)
    print(f"{'Depth':<8} {'Max Size':<12} {'# Sets':<10} {'Time (s)':<12} {'Strategy':<15}")
    print("-" * 80)

    for depth, results in all_results:
        print(f"{depth:<8} {results['max_size']:<12} {results['num_nice_sets']:<10} "
              f"{results['total_time']:<12.2f} {results['metadata']['strategy']:<15}")

    print("=" * 80)
    print()

    # Analysis
    max_sizes = [r['max_size'] for _, r in all_results]
    if len(set(max_sizes)) == 1:
        print(f"✓ All depths found the same maximum size: {max_sizes[0]}")
    else:
        print(f"⚠ Different depths found different maximum sizes!")
        for depth, results in all_results:
            print(f"  Depth {depth}: max = {results['max_size']}")

    print()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Validate ternary search with comprehensive logging'
    )
    parser.add_argument(
        '--depth',
        type=int,
        default=3,
        help='Maximum composition depth (default: 3)'
    )
    parser.add_argument(
        '--compare',
        action='store_true',
        help='Compare multiple depths (3, 5, 7)'
    )
    parser.add_argument(
        '--use-z3',
        action='store_true',
        help='Use Z3 SAT backend instead of pattern enumeration'
    )
    parser.add_argument(
        '--no-symmetry-breaking',
        action='store_true',
        help='Disable symmetry breaking (slower)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Print detailed progress information'
    )

    args = parser.parse_args()

    if args.compare:
        # Compare multiple depths
        compare_depths([3, 5, 7], use_z3=args.use_z3, verbose=args.verbose)
    else:
        # Single depth validation
        run_validation(
            args.depth,
            verbose=args.verbose,
            use_z3=args.use_z3,
            use_symmetry_breaking=not args.no_symmetry_breaking
        )


if __name__ == '__main__':
    main()
