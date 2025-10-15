"""
Prove commands for demonstrating maximum nice set size.

This module provides command implementations for formal proofs of maximum
nice set size using different methodologies (Z3 and enumeration).
"""

import sys

from src.independence import DefinabilityMode
from src.proofs.z3_proof import (
    build_connective_pool,
    z3_proof_approach_1_symmetry_breaking
)
from src.proofs import enumeration_proof


def prove_z3(checkpoint=None, interval=100, target_size=17, max_depth=3, max_arity=3,
             max_candidates=10000, definability_mode=DefinabilityMode.SYNTACTIC):
    """
    Run Z3-based proof for maximum nice set size.

    Args:
        checkpoint: Path to checkpoint file for saving/loading progress
        interval: Save checkpoint every N candidates
        target_size: Target nice set size to search for
        max_depth: Maximum composition depth for independence checking
        max_arity: Maximum arity to include in connective pool
        max_candidates: Maximum number of complete sets to check before stopping
        definability_mode: Definability mode (syntactic or truth-functional)

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    print()
    print("=" * 70)
    print(f"Z3-BASED PROOF: MAXIMUM NICE SET SIZE = {target_size - 1}")
    print(f"Arity range: 0-{max_arity}, Depth: {max_depth}")
    print("=" * 70)
    print()

    # Build pool
    pool = build_connective_pool(max_arity=max_arity)
    print(f"Connective pool size: {len(pool)}")
    print()

    # Run Z3 proof
    no_target_size = z3_proof_approach_1_symmetry_breaking(
        pool,
        target_size=target_size,
        max_depth=max_depth,
        checkpoint_path=checkpoint,
        checkpoint_interval=interval,
        max_candidates=max_candidates,
        definability_mode=definability_mode
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


def prove_enumeration(definability_mode=DefinabilityMode.SYNTACTIC):
    """
    Run enumeration-based proof for maximum nice set size.

    This provides a definitive proof through exhaustive pattern enumeration.

    Args:
        definability_mode: Definability mode (syntactic or truth-functional)

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    return enumeration_proof.main(definability_mode=definability_mode)
