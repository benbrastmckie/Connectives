#!/usr/bin/env python3
"""
Validation script for binary search with comprehensive logging.

Runs binary search to confirm the known max=3 result and test metadata logging.
"""

import sys
from pathlib import Path

# Add project root directory to path for imports (now 2 levels up from scripts/validation/)
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.search import search_binary_only
import argparse


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Validate binary search with comprehensive logging'
    )
    parser.add_argument(
        '--depth',
        type=int,
        default=3,
        help='Maximum composition depth (default: 3)'
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

    args = parser.parse_args()

    print("=" * 80)
    print("BINARY-ONLY SEARCH VALIDATION")
    print("=" * 80)
    print(f"Parameters:")
    print(f"  Composition depth: {args.depth}")
    print(f"  Strategy: {'z3_sat' if args.use_z3 else 'enumeration'}")
    print(f"  Symmetry breaking: {not args.no_symmetry_breaking}")
    print()

    # Run binary-only search
    max_size, nice_sets = search_binary_only(
        max_depth=args.depth,
        verbose=True,
        use_z3=args.use_z3,
        use_symmetry_breaking=not args.no_symmetry_breaking
    )

    print()
    print("=" * 80)
    print("VALIDATION STATUS")
    print("=" * 80)

    if max_size == 3:
        print("✓ PASS: Found expected maximum size of 3")
    else:
        print(f"✗ FAIL: Expected max=3, got max={max_size}")

    print()


if __name__ == '__main__':
    main()
