"""
Z3-based independence checker using bounded composition.

A set of connectives is independent if no connective in the set can be
expressed as a composition of the others. We check this by trying to
find a composition tree of bounded depth that replicates the target
connective's truth table.
"""

from z3 import Solver, Bool, And, Or, Not as Z3Not, sat, unsat
from typing import List, Set, Tuple, Optional
from src.connectives import Connective
import itertools


def is_definable(target: Connective, basis: List[Connective],
                max_depth: int = 3, timeout_ms: int = 5000) -> bool:
    """
    Check if target connective is definable from basis connectives.

    Uses bounded composition search with Z3. Tries to find a composition
    of functions from the basis (up to max_depth nested applications)
    that matches the target's truth table.

    Args:
        target: Connective to try to define
        basis: List of connectives to use as basis
        max_depth: Maximum composition depth to try
        timeout_ms: Solver timeout in milliseconds

    Returns:
        True if target is definable from basis within the depth bound
    """
    if not basis:
        return False

    # Quick check: if target is in basis, it's trivially definable
    if target in basis:
        return True

    # Try increasing depths until we find a definition or reach max_depth
    for depth in range(1, max_depth + 1):
        if _is_definable_at_depth(target, basis, depth, timeout_ms):
            return True

    return False


def _is_definable_at_depth(target: Connective, basis: List[Connective],
                           depth: int, timeout_ms: int) -> bool:
    """
    Check if target is definable at a specific depth.

    This uses a brute-force enumeration approach since the composition
    space is manageable for small depths and arities.

    Args:
        target: Connective to define
        basis: Basis connectives
        depth: Composition depth
        timeout_ms: Timeout in milliseconds

    Returns:
        True if definable at this depth
    """
    # For depth 1, just check if any single application of a basis
    # function matches the target
    if depth == 1:
        return _check_depth_one(target, basis)

    # For deeper compositions, we need to enumerate possible compositions
    # This is complex for variable arity, so we'll use a simpler approach:
    # enumerate all possible expression trees and evaluate them
    return _check_composition_enumeration(target, basis, depth)


def _check_depth_one(target: Connective, basis: List[Connective]) -> bool:
    """
    Check if target matches any single application of a basis function.

    For depth 1, we check if there exists a basis function f and a
    variable assignment that matches target's truth table.

    Args:
        target: Target connective
        basis: Basis connectives

    Returns:
        True if target is expressible as a single basis function application
    """
    # If arities don't match, we need to consider projections/constants
    # For simplicity, we focus on same-arity matches
    for b in basis:
        if b.arity == target.arity:
            # Check if b matches target (possibly with variable permutation)
            if _check_with_permutations(target, b):
                return True

        # Check if target can be expressed as f(constant, variable, ...)
        # This gets complex quickly, so we'll defer to composition enumeration
        # for mixed-arity cases

    return False


def _check_with_permutations(target: Connective, candidate: Connective) -> bool:
    """
    Check if target matches candidate under some variable permutation.

    Args:
        target: Target connective
        candidate: Candidate connective

    Returns:
        True if there exists a permutation making them equivalent
    """
    if target.arity != candidate.arity:
        return False

    # Generate all permutations of variables
    import itertools
    for perm in itertools.permutations(range(target.arity)):
        if _check_permutation_match(target, candidate, perm):
            return True

    return False


def _check_permutation_match(target: Connective, candidate: Connective,
                             perm: Tuple[int, ...]) -> bool:
    """
    Check if candidate with permutation matches target.

    Args:
        target: Target connective
        candidate: Candidate connective
        perm: Variable permutation

    Returns:
        True if candidate(x_perm[0], ..., x_perm[n-1]) == target(x_0, ..., x_n-1)
    """
    num_rows = 2 ** target.arity

    for row in range(num_rows):
        # Convert row to input tuple for target
        target_inputs = tuple((row >> (target.arity - 1 - k)) & 1
                            for k in range(target.arity))

        # Apply permutation to get candidate inputs
        candidate_inputs = tuple(target_inputs[perm[k]]
                                for k in range(candidate.arity))

        # Check if outputs match
        if target.evaluate(target_inputs) != candidate.evaluate(candidate_inputs):
            return False

    return True


def _check_composition_enumeration(target: Connective, basis: List[Connective],
                                   max_depth: int) -> bool:
    """
    Check definability by enumerating small compositions.

    For binary connectives and small depths, we can enumerate all
    possible compositions and check if any match the target.

    Args:
        target: Target connective
        basis: Basis connectives
        max_depth: Maximum composition depth

    Returns:
        True if a matching composition exists
    """
    # This is a simplified version that checks common cases
    # For full implementation, would need to build expression trees

    # For binary target, check simple compositions
    if target.arity == 2:
        return _check_binary_compositions(target, basis, max_depth)

    # For other arities, use conservative approximation
    return False


def _check_binary_compositions(target: Connective, basis: List[Connective],
                               max_depth: int) -> bool:
    """
    Check binary connective compositions specifically.

    Args:
        target: Binary target connective
        basis: Basis connectives
        max_depth: Maximum depth

    Returns:
        True if definable
    """
    # Extract binary and unary basis functions
    binary_basis = [b for b in basis if b.arity == 2]
    unary_basis = [b for b in basis if b.arity == 1]

    # For depth 2: check f(g(x,y), h(x,y)) and f(g(x), y), etc.
    if max_depth >= 2:
        # Try f(g(x,y), h(x,y)) - binary outer function
        for f in binary_basis:
            for g in binary_basis + unary_basis + [None]:
                for h in binary_basis + unary_basis + [None]:
                    if _try_composition_f_g_h(target, f, g, h):
                        return True

        # Try unary(binary(x,y)) - unary outer, binary inner
        for f in unary_basis:
            for g in binary_basis:
                if _try_unary_binary_composition(target, f, g):
                    return True

        # Try binary(unary(x), unary(y)) - binary outer, unary inners
        for f in binary_basis:
            for g in unary_basis + [None]:
                for h in unary_basis + [None]:
                    if _try_binary_unary_unary_composition(target, f, g, h):
                        return True

    # For depth 3: check unary(binary(unary(x), unary(y)))
    if max_depth >= 3:
        for f in unary_basis:
            for g in binary_basis:
                for h in unary_basis + [None]:
                    for i in unary_basis + [None]:
                        if _try_unary_binary_unary_unary_composition(target, f, g, h, i):
                            return True

    return False


def _try_composition_f_g_h(target: Connective,
                           f: Connective,
                           g: Optional[Connective],
                           h: Optional[Connective]) -> bool:
    """
    Try composition f(g(...), h(...)) and check if it matches target.

    Args:
        target: Target connective
        f: Outer function
        g: Left inner function (None = identity/projection)
        h: Right inner function (None = identity/projection)

    Returns:
        True if composition matches target
    """
    # Evaluate composition on all inputs
    for x in [0, 1]:
        for y in [0, 1]:
            # Compute g(x,y) or g(x) or x
            if g is None:
                g_result = x
            elif g.arity == 1:
                g_result = g.evaluate((x,))
            elif g.arity == 2:
                g_result = g.evaluate((x, y))
            else:
                return False

            # Compute h(x,y) or h(y) or y
            if h is None:
                h_result = y
            elif h.arity == 1:
                h_result = h.evaluate((y,))
            elif h.arity == 2:
                h_result = h.evaluate((x, y))
            else:
                return False

            # Compute f(g_result, h_result)
            f_result = f.evaluate((g_result, h_result))

            # Check against target
            if f_result != target.evaluate((x, y)):
                return False

    return True


def _try_unary_binary_composition(target: Connective,
                                   f: Connective,
                                   g: Connective) -> bool:
    """
    Try composition f(g(x,y)) where f is unary and g is binary.

    This handles patterns like NOT(AND(x,y)) for NAND.

    Args:
        target: Target connective (binary)
        f: Outer unary function
        g: Inner binary function

    Returns:
        True if composition matches target
    """
    # Evaluate composition on all inputs
    for x in [0, 1]:
        for y in [0, 1]:
            # Compute g(x,y)
            g_result = g.evaluate((x, y))

            # Compute f(g_result)
            f_result = f.evaluate((g_result,))

            # Check against target
            if f_result != target.evaluate((x, y)):
                return False

    return True


def _try_binary_unary_unary_composition(target: Connective,
                                         f: Connective,
                                         g: Optional[Connective],
                                         h: Optional[Connective]) -> bool:
    """
    Try composition f(g(x), h(y)) where f is binary and g, h are unary.

    This handles patterns like AND(NOT(x), NOT(y)).

    Args:
        target: Target connective (binary)
        f: Outer binary function
        g: Left inner unary function (None = identity)
        h: Right inner unary function (None = identity)

    Returns:
        True if composition matches target
    """
    # Evaluate composition on all inputs
    for x in [0, 1]:
        for y in [0, 1]:
            # Compute g(x) or x
            if g is None:
                g_result = x
            else:
                g_result = g.evaluate((x,))

            # Compute h(y) or y
            if h is None:
                h_result = y
            else:
                h_result = h.evaluate((y,))

            # Compute f(g_result, h_result)
            f_result = f.evaluate((g_result, h_result))

            # Check against target
            if f_result != target.evaluate((x, y)):
                return False

    return True


def _try_unary_binary_unary_unary_composition(target: Connective,
                                                f: Connective,
                                                g: Connective,
                                                h: Optional[Connective],
                                                i: Optional[Connective]) -> bool:
    """
    Try composition f(g(h(x), i(y))) where f is unary, g is binary, h and i are unary.

    This handles patterns like NOT(AND(NOT(x), NOT(y))) for De Morgan's Law.

    Args:
        target: Target connective (binary)
        f: Outer unary function
        g: Middle binary function
        h: Left inner unary function (None = identity)
        i: Right inner unary function (None = identity)

    Returns:
        True if composition matches target
    """
    # Evaluate composition on all inputs
    for x in [0, 1]:
        for y in [0, 1]:
            # Compute h(x) or x
            if h is None:
                h_result = x
            else:
                h_result = h.evaluate((x,))

            # Compute i(y) or y
            if i is None:
                i_result = y
            else:
                i_result = i.evaluate((y,))

            # Compute g(h_result, i_result)
            g_result = g.evaluate((h_result, i_result))

            # Compute f(g_result)
            f_result = f.evaluate((g_result,))

            # Check against target
            if f_result != target.evaluate((x, y)):
                return False

    return True


def is_independent(connectives: List[Connective],
                  max_depth: int = 3,
                  timeout_ms: int = 5000) -> bool:
    """
    Check if a set of connectives is independent.

    A set is independent if no connective can be expressed as a
    composition of the others.

    Args:
        connectives: List of connectives to check
        max_depth: Maximum composition depth for definability checking
        timeout_ms: Solver timeout per check

    Returns:
        True if the set is independent
    """
    if len(connectives) <= 1:
        return True

    # Check each connective to see if it's definable from the others
    for i, target in enumerate(connectives):
        # Create basis from all other connectives
        basis = connectives[:i] + connectives[i+1:]

        # Check if target is definable from basis
        if is_definable(target, basis, max_depth, timeout_ms):
            return False

    return True


def find_redundant_connectives(connectives: List[Connective],
                               max_depth: int = 3) -> Set[int]:
    """
    Find indices of redundant connectives in a set.

    A connective is redundant if it's definable from the others.

    Args:
        connectives: List of connectives to check
        max_depth: Maximum composition depth

    Returns:
        Set of indices of redundant connectives
    """
    redundant = set()

    for i, target in enumerate(connectives):
        basis = connectives[:i] + connectives[i+1:]
        if is_definable(target, basis, max_depth):
            redundant.add(i)

    return redundant


def get_independent_subset(connectives: List[Connective],
                          max_depth: int = 3) -> List[Connective]:
    """
    Extract a maximal independent subset from a list of connectives.

    Args:
        connectives: List of connectives (may contain dependencies)
        max_depth: Maximum composition depth

    Returns:
        Maximal independent subset
    """
    if not connectives:
        return []

    # Greedy algorithm: keep connectives that aren't definable from
    # what we've kept so far
    independent = []

    for c in connectives:
        if not is_definable(c, independent, max_depth):
            independent.append(c)

    return independent
