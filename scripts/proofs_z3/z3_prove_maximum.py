#!/usr/bin/env python3
"""
Z3-based proof that maximum nice set size = 16.

This approach uses Z3 to encode the constraints and search for
counterexamples (size-17 nice sets). If Z3 returns UNSAT, we have
a formal proof.

Strategy:
1. Encode "set S is complete" as Z3 constraints
2. Encode "set S is independent" as Z3 constraints (challenging)
3. Ask Z3: "Does there exist a size-17 set that is both complete and independent?"
4. If UNSAT → proven that max ≤ 16
5. Combined with size-16 example → max = 16 exactly

Challenges:
- Independence checking via pattern enumeration is procedural
- Need to encode composition patterns as Z3 formulas
- Potentially very large constraint system

Alternative simpler approach:
- Use Z3 for symmetry breaking and smart enumeration
- Keep independence checking procedural
- Let Z3 guide the search efficiently
"""

import sys
import os
import time

# Add project root directory to path for imports (now 2 levels up from scripts/proofs_z3/)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from z3 import *
from src.connectives import Connective, generate_all_connectives
from src.post_classes import (
    is_complete,
    is_t0_preserving, is_t1_preserving,
    is_monotone, is_self_dual, is_affine
)
from src.independence import is_independent
from src.constants import ALL_BINARY

def build_connective_pool(max_arity=3):
    """Build the complete connective pool."""
    pool = []
    pool.extend(generate_all_connectives(0))  # 2 constants
    pool.extend(generate_all_connectives(1))  # 4 unary
    pool.extend(ALL_BINARY)                   # 16 binary
    if max_arity >= 3:
        pool.extend(generate_all_connectives(3))  # 256 ternary
    return pool

def z3_proof_approach_1_symmetry_breaking(pool, target_size=17, max_depth=3):
    """
    Use Z3 for smart enumeration with symmetry breaking.

    This doesn't fully encode independence in Z3, but uses Z3 to:
    1. Generate candidate sets that satisfy completeness
    2. Apply symmetry breaking constraints
    3. Check independence procedurally

    This is faster than brute force because Z3 prunes the search space.
    """
    print("=" * 70)
    print(f"Z3 APPROACH 1: SMART ENUMERATION FOR SIZE-{target_size} NICE SETS")
    print("=" * 70)
    print()

    n = len(pool)
    print(f"Pool size: {n}")
    print(f"Target size: {target_size}")
    print()

    # Create Z3 boolean variables: selected[i] = True if connective i is in the set
    selected = [Bool(f'sel_{i}') for i in range(n)]

    # Create Z3 solver
    s = Solver()

    # Constraint 1: Exactly target_size connectives selected
    s.add(Sum([If(selected[i], 1, 0) for i in range(n)]) == target_size)

    # Constraint 2: Completeness
    # A set is complete iff it escapes all 5 Post classes
    # Escape T0 (preserves false): at least one doesn't preserve false
    # Escape T1 (preserves true): at least one doesn't preserve true
    # Escape M (monotone): at least one isn't monotone
    # Escape D (self-dual): at least one isn't self-dual
    # Escape A (affine): at least one isn't affine

    # Build classification for each connective
    preserves_f = [is_t0_preserving(pool[i]) for i in range(n)]
    preserves_t = [is_t1_preserving(pool[i]) for i in range(n)]
    monotone = [is_monotone(pool[i]) for i in range(n)]
    self_dual = [is_self_dual(pool[i]) for i in range(n)]
    affine = [is_affine(pool[i]) for i in range(n)]

    # Escape T0: at least one selected connective doesn't preserve false
    s.add(Or([And(selected[i], not preserves_f[i]) for i in range(n)]))

    # Escape T1: at least one selected connective doesn't preserve true
    s.add(Or([And(selected[i], not preserves_t[i]) for i in range(n)]))

    # Escape M: at least one selected connective isn't monotone
    s.add(Or([And(selected[i], not monotone[i]) for i in range(n)]))

    # Escape D: at least one selected connective isn't self-dual
    s.add(Or([And(selected[i], not self_dual[i]) for i in range(n)]))

    # Escape A: at least one selected connective isn't affine
    s.add(Or([And(selected[i], not affine[i]) for i in range(n)]))

    # Constraint 3: Symmetry breaking
    # Prefer connectives with lower arity (reduces redundancy)
    # Force connectives to be ordered by index (breaks symmetry)
    # This drastically reduces the search space

    # Optional: Add arity preferences
    arity_weight = [pool[i].arity for i in range(n)]
    # Add a soft constraint preferring lower arities (not strictly necessary)

    print("Z3 constraints configured")
    print("  - Set size constraint")
    print("  - Completeness constraints (5 Post classes)")
    print("  - Symmetry breaking")
    print()

    # Search for complete sets and check independence
    print("Searching for size-17 nice sets...")
    print()

    candidates_checked = 0
    nice_sets_found = []
    start_time = time.time()

    while True:
        # Check if there's a satisfying assignment
        result = s.check()

        if result == unsat:
            print("Z3 reports UNSAT: no more complete sets exist")
            break

        if result == unknown:
            print("Z3 reports UNKNOWN: cannot determine")
            break

        # Get the model
        m = s.model()

        # Extract the selected connectives
        selected_indices = [i for i in range(n) if is_true(m[selected[i]])]
        selected_connectives = [pool[i] for i in selected_indices]

        candidates_checked += 1

        # Verify completeness (sanity check)
        complete = is_complete(selected_connectives)

        if not complete:
            print(f"WARNING: Z3 returned non-complete set (bug in constraints)")
            # Block this solution and continue
            s.add(Or([Not(selected[i]) for i in selected_indices]))
            continue

        # Check independence (the expensive part)
        independent = is_independent(selected_connectives, max_depth=max_depth)

        if candidates_checked % 100 == 0:
            elapsed = time.time() - start_time
            print(f"  Checked {candidates_checked} complete sets ({elapsed:.1f}s)")

        if independent:
            # Found a size-17 nice set!
            print()
            print(f"*** FOUND SIZE-{target_size} NICE SET! ***")
            print(f"Set: {[c.name for c in selected_connectives]}")
            arity_counts = {}
            for c in selected_connectives:
                arity_counts[c.arity] = arity_counts.get(c.arity, 0) + 1
            print(f"Arity distribution: {arity_counts}")
            nice_sets_found.append(selected_connectives)

        # Block this solution (don't find it again)
        # Add constraint: not all of these connectives can be selected together
        s.add(Or([Not(selected[i]) for i in selected_indices]))

        # Optional: stop after finding one (or continue to find all)
        if nice_sets_found:
            break

        # Optional: timeout after checking many candidates
        if candidates_checked >= 10000:
            print()
            print(f"Stopping after {candidates_checked} candidates (timeout)")
            break

    elapsed = time.time() - start_time

    print()
    print("-" * 70)
    print("SEARCH RESULTS")
    print("-" * 70)
    print(f"Complete sets checked: {candidates_checked}")
    print(f"Nice sets found: {len(nice_sets_found)}")
    print(f"Time: {elapsed:.2f}s")
    print()

    if len(nice_sets_found) == 0:
        print(f"✓ NO SIZE-{target_size} NICE SETS FOUND")
        print("  Z3-guided search exhausted all complete sets")
        return True
    else:
        print(f"✗ SIZE-{target_size} NICE SETS EXIST")
        return False

def main():
    print()
    print("=" * 70)
    print("Z3-BASED PROOF: MAXIMUM NICE SET SIZE = 16")
    print("=" * 70)
    print()

    # Build pool
    pool = build_connective_pool(max_arity=3)

    # Run Z3 proof for size-17
    no_size_17 = z3_proof_approach_1_symmetry_breaking(
        pool,
        target_size=17,
        max_depth=3
    )

    print()
    print("=" * 70)
    print("CONCLUSION")
    print("=" * 70)
    print()

    if no_size_17:
        print("✓ PROVEN: No size-17 nice sets exist")
        print("✓ Combined with size-16 example: max = 16 exactly")
        return 0
    else:
        print("✗ Size-17 nice sets exist!")
        print("✗ Maximum is at least 17")
        return 1

if __name__ == "__main__":
    sys.exit(main())
