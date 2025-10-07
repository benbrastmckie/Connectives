"""
Prove commands for demonstrating maximum nice set size.

This module provides command implementations for formal proofs of maximum
nice set size using different methodologies (Z3 and enumeration).
"""

import sys
import os
from pathlib import Path


def prove_z3(checkpoint=None, interval=100, target_size=17, max_depth=3):
    """
    Run Z3-based proof for maximum nice set size.

    Args:
        checkpoint: Path to checkpoint file for saving/loading progress
        interval: Save checkpoint every N candidates
        target_size: Target nice set size to search for
        max_depth: Maximum composition depth for independence checking

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    # Add scripts/proofs_z3 to path for imports
    script_dir = Path(__file__).parent.parent.parent / "scripts" / "proofs_z3"
    sys.path.insert(0, str(script_dir))

    try:
        from z3_prove_maximum import (
            build_connective_pool,
            z3_proof_approach_1_symmetry_breaking
        )

        print()
        print("=" * 70)
        print(f"Z3-BASED PROOF: MAXIMUM NICE SET SIZE = {target_size - 1}")
        print("=" * 70)
        print()

        # Build pool
        pool = build_connective_pool(max_arity=3)

        # Run Z3 proof
        no_target_size = z3_proof_approach_1_symmetry_breaking(
            pool,
            target_size=target_size,
            max_depth=max_depth,
            checkpoint_path=checkpoint,
            checkpoint_interval=interval
        )

        print()
        print("=" * 70)
        print("CONCLUSION")
        print("=" * 70)
        print()

        if no_target_size:
            print(f"✓ PROVEN: No size-{target_size} nice sets exist")
            print(f"✓ Combined with size-{target_size - 1} example: max = {target_size - 1} exactly")
            return 0
        else:
            print(f"✗ Size-{target_size} nice sets exist!")
            print(f"✗ Maximum is at least {target_size}")
            return 1

    except ImportError as e:
        print(f"Error importing Z3 proof module: {e}", file=sys.stderr)
        return 1
    finally:
        # Clean up path
        if str(script_dir) in sys.path:
            sys.path.remove(str(script_dir))


def prove_enumeration():
    """
    Run enumeration-based proof for maximum nice set size.

    This provides a definitive proof through exhaustive pattern enumeration.

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    # Add scripts/proofs_enumeration to path for imports
    script_dir = Path(__file__).parent.parent.parent / "scripts" / "proofs_enumeration"
    sys.path.insert(0, str(script_dir))

    try:
        # Import and run the main function from prove_maximum
        import prove_maximum
        return prove_maximum.main()

    except ImportError as e:
        print(f"Error importing enumeration proof module: {e}", file=sys.stderr)
        return 1
    finally:
        # Clean up path
        if str(script_dir) in sys.path:
            sys.path.remove(str(script_dir))
