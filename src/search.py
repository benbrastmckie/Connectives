"""
Search algorithms for finding nice (complete and independent) connective sets.

A nice set is one that is both:
1. Complete: Can define all classical connectives (Post's lattice)
2. Independent: No connective is definable from the others
"""

from typing import List, Set, Tuple, Dict
from itertools import combinations
from src.connectives import Connective, generate_all_connectives
from src.post_classes import is_complete, equivalence_class_representative
from src.independence import is_independent
import time


def filter_by_equivalence(connectives: List[Connective]) -> List[Connective]:
    """
    Filter connectives to one representative per equivalence class.

    Equivalence classes group connectives that differ only by:
    - Variable permutation (e.g., AND(x,y) vs AND(y,x))
    - Variable/output negation (e.g., NAND vs NOT(AND))

    This reduces search space by ~2-8× depending on arity.

    Args:
        connectives: List of connectives to filter

    Returns:
        List containing one representative from each equivalence class
    """
    seen_classes = set()
    representatives = []

    for conn in connectives:
        # Get canonical representative for this connective's equivalence class
        canonical = equivalence_class_representative(conn)

        # Only add if we haven't seen this equivalence class
        if canonical not in seen_classes:
            seen_classes.add(canonical)
            representatives.append(conn)

    return representatives


def find_nice_sets_of_size(
    connectives: List[Connective],
    size: int,
    max_depth: int = 3,
    verbose: bool = False,
    use_z3: bool = False
) -> List[List[Connective]]:
    """
    Find all nice sets of a specific size from a pool of connectives.

    Args:
        connectives: Pool of connectives to search
        size: Target set size
        max_depth: Maximum composition depth for independence checking
        verbose: Print progress information
        use_z3: Use Z3 SAT (True) or pattern enumeration (False, default)

    Returns:
        List of nice sets (each set is a list of connectives)
    """
    nice_sets = []
    total_combinations = len(list(combinations(range(len(connectives)), size)))
    checked = 0

    if verbose:
        print(f"Searching for nice sets of size {size}...")
        print(f"Total combinations to check: {total_combinations}")

    for combo in combinations(connectives, size):
        checked += 1
        if verbose and checked % 1000 == 0:
            print(f"  Checked {checked}/{total_combinations} combinations...")

        # First check completeness (fast)
        combo_list = list(combo)
        if not is_complete(combo_list):
            continue

        # Then check independence (slower)
        if is_independent(combo_list, max_depth, use_z3=use_z3):
            nice_sets.append(combo_list)
            if verbose:
                print(f"  Found nice set: {[c.name for c in combo_list]}")

    if verbose:
        print(f"Found {len(nice_sets)} nice sets of size {size}")

    return nice_sets


def find_maximum_nice_set(
    connectives: List[Connective],
    max_size: int = 10,
    max_depth: int = 3,
    verbose: bool = False,
    use_z3: bool = False
) -> Tuple[int, List[List[Connective]], Dict[str, any]]:
    """
    Find the maximum size of nice sets and examples.

    Searches incrementally from size 1 upward until no nice sets are found.

    Args:
        connectives: Pool of connectives to search
        max_size: Maximum size to search up to
        max_depth: Maximum composition depth for independence checking
        verbose: Print progress information
        use_z3: Use Z3 SAT (True) or pattern enumeration (False, default)

    Returns:
        Tuple of (maximum_size, list_of_maximal_nice_sets, metadata)
        where metadata includes:
            - composition_depth: max_depth used
            - strategy: "enumeration" or "z3_sat"
            - search_time: total seconds
            - basis_size: number of connectives searched
    """
    maximum_size = 0
    maximal_sets = []
    search_start_time = time.time()

    if verbose:
        print(f"Searching for maximum nice set size...")
        print(f"Connective pool size: {len(connectives)}")
        print(f"Composition depth: {max_depth}")
        print(f"Strategy: {'z3_sat' if use_z3 else 'enumeration'}")

    for size in range(1, min(max_size + 1, len(connectives) + 1)):
        start_time = time.time()
        nice_sets = find_nice_sets_of_size(connectives, size, max_depth, verbose, use_z3)
        elapsed = time.time() - start_time

        if nice_sets:
            maximum_size = size
            maximal_sets = nice_sets
            if verbose:
                print(f"Size {size}: Found {len(nice_sets)} nice sets ({elapsed:.2f}s)")
        else:
            if verbose:
                print(f"Size {size}: No nice sets found ({elapsed:.2f}s)")
            # Continue searching - it's possible that size N has no nice sets
            # but size N+1 does (e.g., size 1 has none, but size 2 does)

    total_search_time = time.time() - search_start_time

    metadata = {
        'composition_depth': max_depth,
        'strategy': 'z3_sat' if use_z3 else 'enumeration',
        'search_time': total_search_time,
        'basis_size': len(connectives)
    }

    if verbose:
        print(f"\nSearch completed in {total_search_time:.2f}s")

    return maximum_size, maximal_sets, metadata


def search_binary_only(
    max_depth: int = 3,
    verbose: bool = True,
    use_z3: bool = False,
    use_symmetry_breaking: bool = False
) -> Tuple[int, List[List[Connective]]]:
    """
    Search for maximum nice set using only binary connectives.

    This should reproduce the known result that max=3 for binary-only.

    Args:
        max_depth: Maximum composition depth for independence checking
        verbose: Print progress information
        use_z3: Use Z3 SAT (True) or pattern enumeration (False, default)
        use_symmetry_breaking: Apply equivalence class filtering (default False)

    Returns:
        Tuple of (maximum_size, list_of_maximal_nice_sets)
    """
    if verbose:
        print("=" * 60)
        print("BINARY-ONLY SEARCH")
        print("=" * 60)

    # Generate all binary connectives
    binary_connectives = generate_all_connectives(2)

    if verbose:
        print(f"Total binary connectives: {len(binary_connectives)}")

    # Apply symmetry breaking if requested
    if use_symmetry_breaking:
        filter_start = time.time()
        binary_connectives = filter_by_equivalence(binary_connectives)
        filter_time = time.time() - filter_start

        if verbose:
            print(f"After equivalence filtering: {len(binary_connectives)}")
            print(f"Filtering time: {filter_time:.3f}s")
            print(f"Reduction ratio: {16 / len(binary_connectives):.2f}×")

    # Search for maximum nice set
    max_size, nice_sets, metadata = find_maximum_nice_set(
        binary_connectives,
        max_size=5,  # Binary-only max is 3, so 5 is safe upper bound
        max_depth=max_depth,
        verbose=verbose,
        use_z3=use_z3
    )

    if verbose:
        print("\n" + "=" * 60)
        print(f"RESULT: Maximum nice set size = {max_size}")
        print("=" * 60)
        print(f"Composition depth: {metadata['composition_depth']}")
        print(f"Strategy: {metadata['strategy']}")
        print(f"Search time: {metadata['search_time']:.2f}s")
        if nice_sets:
            print(f"Found {len(nice_sets)} maximal nice sets")
            print("\nExample nice sets:")
            for i, nice_set in enumerate(nice_sets[:5]):  # Show first 5
                names = [c.name for c in nice_set]
                print(f"  Set {i+1}: {names}")

    return max_size, nice_sets


def search_incremental_arity(
    max_arity: int = 3,
    max_depth: int = 3,
    stopping_criterion: int = 3,
    verbose: bool = True
) -> Tuple[int, List[List[Connective]], Dict[str, any]]:
    """
    Incremental search adding connectives of increasing arity.

    Starts with binary, then adds unary, then ternary, etc.
    Stops when no improvement is seen for 'stopping_criterion' arities.

    Args:
        max_arity: Maximum arity to consider
        max_depth: Maximum composition depth for independence checking
        stopping_criterion: Stop if no improvement for this many arities
        verbose: Print progress information

    Returns:
        Tuple of (maximum_size, list_of_maximal_nice_sets, statistics)
    """
    if verbose:
        print("=" * 60)
        print("INCREMENTAL ARITY SEARCH")
        print("=" * 60)

    # Build connective pool incrementally
    connective_pool = []
    best_size = 0
    best_sets = []
    no_improvement_count = 0
    stats = {
        'arity_results': {},
        'total_time': 0,
        'connectives_by_arity': {}
    }

    start_total = time.time()

    # Try arities in order: 2 (binary), 1 (unary), 3 (ternary), 4, ...
    # Binary first since that's the most common case
    arity_order = [2, 1] + list(range(3, max_arity + 1))

    for arity in arity_order:
        if arity > max_arity:
            break

        if verbose:
            print(f"\n{'=' * 60}")
            print(f"Adding arity {arity} connectives...")
            print(f"{'=' * 60}")

        # Generate connectives of this arity
        new_connectives = generate_all_connectives(arity)
        connective_pool.extend(new_connectives)

        stats['connectives_by_arity'][arity] = len(new_connectives)

        if verbose:
            print(f"Added {len(new_connectives)} connectives of arity {arity}")
            print(f"Total pool size: {len(connective_pool)}")

        # Search with current pool
        start_time = time.time()
        max_size, nice_sets, metadata = find_maximum_nice_set(
            connective_pool,
            max_size=min(10, len(connective_pool)),
            max_depth=max_depth,
            verbose=verbose
        )
        elapsed = time.time() - start_time

        stats['arity_results'][arity] = {
            'max_size': max_size,
            'num_sets': len(nice_sets),
            'time_seconds': elapsed,
            'composition_depth': metadata['composition_depth'],
            'strategy': metadata['strategy']
        }

        if verbose:
            print(f"\nArity {arity} result: max size = {max_size}")
            print(f"Time: {elapsed:.2f}s")

        # Check if we improved
        if max_size > best_size:
            best_size = max_size
            best_sets = nice_sets
            no_improvement_count = 0
            if verbose:
                print(f"NEW BEST: {best_size}")
        else:
            no_improvement_count += 1
            if verbose:
                print(f"No improvement (count: {no_improvement_count})")

        # Check stopping criterion
        if no_improvement_count >= stopping_criterion:
            if verbose:
                print(f"\nStopping: No improvement for {stopping_criterion} arities")
            break

    stats['total_time'] = time.time() - start_total

    if verbose:
        print("\n" + "=" * 60)
        print(f"FINAL RESULT: Maximum nice set size = {best_size}")
        print("=" * 60)
        print(f"Total time: {stats['total_time']:.2f}s")
        print(f"Found {len(best_sets)} maximal nice sets")

        if best_sets:
            print("\nExample nice sets:")
            for i, nice_set in enumerate(best_sets[:3]):  # Show first 3
                print(f"\nSet {i+1}:")
                for c in nice_set:
                    arity_name = f"arity-{c.arity}"
                    print(f"  {c.name} ({arity_name})")

    return best_size, best_sets, stats


def analyze_nice_set(nice_set: List[Connective]) -> Dict[str, any]:
    """
    Analyze properties of a nice set.

    Args:
        nice_set: A nice set of connectives

    Returns:
        Dictionary of properties
    """
    from src.post_classes import get_post_class_membership

    analysis = {
        'size': len(nice_set),
        'arities': [c.arity for c in nice_set],
        'arity_distribution': {},
        'post_classes': {},
        'connectives': [c.name for c in nice_set]
    }

    # Count arities
    for c in nice_set:
        arity = c.arity
        if arity not in analysis['arity_distribution']:
            analysis['arity_distribution'][arity] = 0
        analysis['arity_distribution'][arity] += 1

    # Analyze Post class membership for each connective
    for c in nice_set:
        classes = get_post_class_membership(c)
        analysis['post_classes'][c.name] = list(classes)

    return analysis


def validate_nice_set(nice_set: List[Connective], max_depth: int = 3) -> Tuple[bool, str]:
    """
    Validate that a set is truly nice (complete and independent).

    Args:
        nice_set: Set to validate
        max_depth: Maximum composition depth for independence checking

    Returns:
        Tuple of (is_valid, message)
    """
    # Check completeness
    if not is_complete(nice_set):
        return False, "Set is not complete"

    # Check independence
    if not is_independent(nice_set, max_depth):
        return False, "Set is not independent"

    return True, "Set is valid (complete and independent)"
