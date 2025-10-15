"""
Validate commands for verification and testing.

This module provides command implementations for validating search results
using different arity configurations.
"""

import sys
from pathlib import Path

from src.independence import DefinabilityMode


def validate_binary(depth=3, use_z3=False, use_symmetry_breaking=True,
                    definability_mode=DefinabilityMode.SYNTACTIC):
    """
    Validate binary-only search results.

    Args:
        depth: Maximum composition depth
        use_z3: Use Z3 SAT backend instead of pattern enumeration
        use_symmetry_breaking: Enable symmetry breaking optimizations
        definability_mode: Definability mode (syntactic or truth-functional)

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    # Add scripts/validation to path for imports
    script_dir = Path(__file__).parent.parent.parent / "scripts" / "validation"
    sys.path.insert(0, str(script_dir))

    try:
        from src.search import search_binary_only

        print("=" * 80)
        print("BINARY-ONLY SEARCH VALIDATION")
        print("=" * 80)
        print(f"Parameters:")
        print(f"  Composition depth: {depth}")
        print(f"  Strategy: {'z3_sat' if use_z3 else 'enumeration'}")
        print(f"  Symmetry breaking: {use_symmetry_breaking}")
        print()

        # Run binary-only search
        max_size, nice_sets = search_binary_only(
            max_depth=depth,
            verbose=True,
            use_symmetry_breaking=use_symmetry_breaking,
            definability_mode=definability_mode
        )

        print()
        print("=" * 80)
        print("VALIDATION STATUS")
        print("=" * 80)

        if max_size == 3:
            print("✓ PASS: Found expected maximum size of 3")
            print()
            return 0
        else:
            print(f"✗ FAIL: Expected max=3, got max={max_size}")
            print()
            return 1

    except ImportError as e:
        print(f"Error importing validation module: {e}", file=sys.stderr)
        return 1
    finally:
        # Clean up path
        if str(script_dir) in sys.path:
            sys.path.remove(str(script_dir))


def validate_ternary(depth=3, compare=False, use_z3=False,
                     use_symmetry_breaking=True, verbose=False,
                     definability_mode=DefinabilityMode.SYNTACTIC):
    """
    Validate ternary search results.

    Args:
        depth: Maximum composition depth
        compare: Compare multiple depths (3, 5, 7)
        use_z3: Use Z3 SAT backend instead of pattern enumeration
        use_symmetry_breaking: Enable symmetry breaking optimizations
        verbose: Print detailed progress information
        definability_mode: Definability mode (syntactic or truth-functional)

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    # Add scripts/validation to path for imports
    script_dir = Path(__file__).parent.parent.parent / "scripts" / "validation"
    sys.path.insert(0, str(script_dir))

    try:
        from validate_ternary_search import run_validation, compare_depths

        if compare:
            # Compare multiple depths
            compare_depths([3, 5, 7], use_z3=use_z3, verbose=verbose)
        else:
            # Single depth validation
            run_validation(
                depth,
                verbose=verbose,
                use_z3=use_z3,
                use_symmetry_breaking=use_symmetry_breaking
            )

        return 0

    except ImportError as e:
        print(f"Error importing validation module: {e}", file=sys.stderr)
        return 1
    finally:
        # Clean up path
        if str(script_dir) in sys.path:
            sys.path.remove(str(script_dir))
