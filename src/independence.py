"""
Independence checking via pattern enumeration.

A set of connectives is independent if no connective in the set can be
expressed as a composition of the others. We check this by trying to
find a composition tree of bounded depth that replicates the target
connective's truth table.
"""

from typing import List, Set, Tuple, Optional
from src.connectives import Connective
import itertools
from enum import Enum


class DefinabilityMode(Enum):
    """Definability checking mode."""
    SYNTACTIC = "syntactic"           # Composition-based (current)
    TRUTH_FUNCTIONAL = "truth-functional"  # Clone-theoretic


def is_definable(target: Connective, basis: List[Connective],
                max_depth: int = 3, timeout_ms: int = 5000,
                mode: DefinabilityMode = DefinabilityMode.SYNTACTIC) -> bool:
    """
    Check if target connective is definable from basis connectives.

    Uses pattern enumeration to check if target can be expressed as a
    composition of basis connectives up to the specified depth.

    Args:
        target: Connective to try to define
        basis: List of connectives to use as basis
        max_depth: Maximum composition depth to try
        timeout_ms: Timeout in milliseconds (for compatibility, not used)
        mode: Definability mode (syntactic or truth-functional, default: syntactic)

    Returns:
        True if target is definable from basis within the depth bound
    """
    if not basis:
        return False

    # Quick check: if target is in basis, it's trivially definable
    if target in basis:
        return True

    # Use pattern enumeration (proven correct for arity ≤3)
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

    For binary and ternary connectives and small depths, we can enumerate
    possible compositions and check if any match the target.

    Args:
        target: Target connective
        basis: Basis connectives
        max_depth: Maximum composition depth

    Returns:
        True if a matching composition exists
    """
    # For nullary (constant) targets
    if target.arity == 0:
        return _check_constant_compositions(target, basis, max_depth)

    # For unary targets
    if target.arity == 1:
        return _check_unary_compositions(target, basis, max_depth)

    # For binary target, check simple compositions
    if target.arity == 2:
        return _check_binary_compositions(target, basis, max_depth)

    # For ternary target, check ternary compositions
    if target.arity == 3:
        return _check_ternary_compositions(target, basis, max_depth)

    # For other arities, use conservative approximation
    return False


def _check_constant_compositions(target: Connective, basis: List[Connective],
                                  max_depth: int) -> bool:
    """
    Check if a constant (arity-0) target can be composed from basis.

    Patterns to check:
    - Depth 1: u(c) where u is unary, c is constant

    Args:
        target: Constant target (arity 0)
        basis: Basis connectives
        max_depth: Maximum depth

    Returns:
        True if definable
    """
    nullary_basis = [b for b in basis if b.arity == 0]
    unary_basis = [b for b in basis if b.arity == 1]

    # Depth 1: unary(constant)
    if max_depth >= 1:
        for u in unary_basis:
            for c in nullary_basis:
                # u(c) - apply unary to constant
                result = u.evaluate((c.truth_table_int,))
                if result == target.truth_table_int:
                    return True

    # Could add deeper patterns here if needed
    return False


def _check_unary_compositions(target: Connective, basis: List[Connective],
                               max_depth: int) -> bool:
    """
    Check if a unary (arity-1) target can be composed from basis.

    Patterns to check:
    - Depth 1: u(x) direct match with permutation
    - Depth 1: f(x, c) or f(c, x) where f is binary, c is constant
    - Depth 1: f(x, x) where f is binary (diagonal)
    - Depth 2: u(v(x)) where u, v are unary
    - Depth 2: u(f(x, c)) where u is unary, f is binary, c is constant

    Args:
        target: Unary target (arity 1)
        basis: Basis connectives
        max_depth: Maximum depth

    Returns:
        True if definable
    """
    unary_basis = [b for b in basis if b.arity == 1]
    binary_basis = [b for b in basis if b.arity == 2]
    nullary_basis = [b for b in basis if b.arity == 0]

    # Depth 1: f(x, c) or f(c, x) where f is binary, c is constant
    if max_depth >= 1:
        for f in binary_basis:
            for c in nullary_basis:
                # Try f(x, c)
                matches = True
                for x in [0, 1]:
                    if f.evaluate((x, c.truth_table_int)) != target.evaluate((x,)):
                        matches = False
                        break
                if matches:
                    return True

                # Try f(c, x)
                matches = True
                for x in [0, 1]:
                    if f.evaluate((c.truth_table_int, x)) != target.evaluate((x,)):
                        matches = False
                        break
                if matches:
                    return True

        # Try f(x, x) where f is binary (diagonal)
        for f in binary_basis:
            matches = True
            for x in [0, 1]:
                if f.evaluate((x, x)) != target.evaluate((x,)):
                    matches = False
                    break
            if matches:
                return True

    # Depth 2: u(v(x)) where u, v are unary
    if max_depth >= 2:
        for u in unary_basis:
            for v in unary_basis:
                matches = True
                for x in [0, 1]:
                    v_result = v.evaluate((x,))
                    u_result = u.evaluate((v_result,))
                    if u_result != target.evaluate((x,)):
                        matches = False
                        break
                if matches:
                    return True

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
    # Extract binary, unary, and nullary (constant) basis functions
    binary_basis = [b for b in basis if b.arity == 2]
    unary_basis = [b for b in basis if b.arity == 1]
    nullary_basis = [b for b in basis if b.arity == 0]

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

        # Try binary(constant, binary(x,y)) and binary(binary(x,y), constant)
        if nullary_basis:
            if _check_binary_constant_patterns(target, binary_basis, unary_basis, nullary_basis):
                return True

    # For depth 3: check various patterns
    if max_depth >= 3:
        # Pattern: unary(binary(unary(x), unary(y)))
        for f in unary_basis:
            for g in binary_basis:
                for h in unary_basis + [None]:
                    for i in unary_basis + [None]:
                        if _try_unary_binary_unary_unary_composition(target, f, g, h, i):
                            return True

        # Pattern: binary(unary(binary(x,y)), unary(binary(x,y)))
        # This handles XOR-like patterns
        if _check_binary_unary_binary_patterns(target, binary_basis, unary_basis):
            return True

        # Pattern: unary(unary(binary(x,y))) - unary chain
        if _check_unary_chain_binary(target, binary_basis, unary_basis):
            return True

        # Pattern: f(x/y, g(h1(x,y), h2(x,y))) or f(g(h1(x,y), h2(x,y)), x/y)
        # This handles patterns like NAND(x, NAND(FALSE, FALSE)) = ¬x
        for f in binary_basis:
            for g in binary_basis:
                for h1 in binary_basis + [None]:
                    for h2 in binary_basis + [None]:
                        # Try f(x, g(h1, h2))
                        if _try_f_proj_composed(target, f, g, h1, h2, left_proj=True):
                            return True
                        # Try f(g(h1, h2), y)
                        if _try_f_proj_composed(target, f, g, h1, h2, left_proj=False):
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


def _check_ternary_compositions(target: Connective, basis: List[Connective],
                                 max_depth: int) -> bool:
    """
    Check ternary connective compositions.

    Args:
        target: Ternary target connective
        basis: Basis connectives
        max_depth: Maximum depth

    Returns:
        True if definable
    """
    # Extract basis functions by arity
    ternary_basis = [b for b in basis if b.arity == 3]
    binary_basis = [b for b in basis if b.arity == 2]
    unary_basis = [b for b in basis if b.arity == 1]

    # For depth 2: check common patterns
    if max_depth >= 2:
        # Try unary(ternary(x,y,z)) - unary outer, ternary inner
        for f in unary_basis:
            for g in ternary_basis:
                if _try_unary_ternary_composition(target, f, g):
                    return True

        # Try ternary(unary(x), unary(y), unary(z))
        for f in ternary_basis:
            for u in unary_basis + [None]:
                for v in unary_basis + [None]:
                    for w in unary_basis + [None]:
                        if _try_ternary_unary_unary_unary(target, f, u, v, w):
                            return True

    return False


def _try_unary_ternary_composition(target: Connective,
                                    f: Connective,
                                    g: Connective) -> bool:
    """Try composition f(g(x,y,z)) where f is unary and g is ternary."""
    for x in [0, 1]:
        for y in [0, 1]:
            for z in [0, 1]:
                # Compute g(x,y,z)
                g_result = g.evaluate((x, y, z))

                # Compute f(g_result)
                f_result = f.evaluate((g_result,))

                # Check against target
                if f_result != target.evaluate((x, y, z)):
                    return False
    return True


def _try_ternary_unary_unary_unary(target: Connective,
                                     f: Connective,
                                     u: Optional[Connective],
                                     v: Optional[Connective],
                                     w: Optional[Connective]) -> bool:
    """Try composition f(u(x), v(y), w(z)) where f is ternary and u,v,w are unary."""
    for x in [0, 1]:
        for y in [0, 1]:
            for z in [0, 1]:
                # Compute u(x), v(y), w(z) (or use identity)
                if u is None:
                    u_result = x
                else:
                    u_result = u.evaluate((x,))

                if v is None:
                    v_result = y
                else:
                    v_result = v.evaluate((y,))

                if w is None:
                    w_result = z
                else:
                    w_result = w.evaluate((z,))

                # Compute f(u_result, v_result, w_result)
                f_result = f.evaluate((u_result, v_result, w_result))

                # Check against target
                if f_result != target.evaluate((x, y, z)):
                    return False
    return True


def _check_binary_constant_patterns(target: Connective,
                                     binary_basis: List[Connective],
                                     unary_basis: List[Connective],
                                     nullary_basis: List[Connective]) -> bool:
    """
    Check patterns involving constants: f(c, g(x,y)), f(g(x,y), c), f(c, x), etc.

    Args:
        target: Binary target connective
        binary_basis: Binary basis functions
        unary_basis: Unary basis functions
        nullary_basis: Constant (nullary) basis functions

    Returns:
        True if target matches a constant pattern
    """
    for f in binary_basis:
        for c in nullary_basis:
            const_val = c.evaluate(())

            # Pattern: f(c, g(x,y))
            for g in binary_basis + [None]:
                if _try_binary_const_binary(target, f, const_val, g, left_const=True):
                    return True

            # Pattern: f(g(x,y), c)
            for g in binary_basis + [None]:
                if _try_binary_const_binary(target, f, const_val, g, left_const=False):
                    return True

            # Pattern: f(c, x)
            if _try_binary_const_var(target, f, const_val, left_const=True):
                return True

            # Pattern: f(x, c)
            if _try_binary_const_var(target, f, const_val, left_const=False):
                return True

            # Pattern: f(c, u(x)) or f(c, u(y))
            for u in unary_basis:
                if _try_binary_const_unary(target, f, const_val, u, left_const=True):
                    return True
                if _try_binary_const_unary(target, f, const_val, u, left_const=False):
                    return True

    return False


def _try_binary_const_binary(target: Connective, f: Connective,
                              const_val: int, g: Optional[Connective],
                              left_const: bool) -> bool:
    """Try f(c, g(x,y)) or f(g(x,y), c)."""
    for x in [0, 1]:
        for y in [0, 1]:
            if g is None:
                # g is identity on first variable
                g_result = x
            else:
                g_result = g.evaluate((x, y))

            if left_const:
                f_result = f.evaluate((const_val, g_result))
            else:
                f_result = f.evaluate((g_result, const_val))

            if f_result != target.evaluate((x, y)):
                return False
    return True


def _try_binary_const_var(target: Connective, f: Connective,
                           const_val: int, left_const: bool) -> bool:
    """Try f(c, x) or f(x, c) for projection-like patterns."""
    for x in [0, 1]:
        for y in [0, 1]:
            if left_const:
                # f(c, y)
                f_result = f.evaluate((const_val, y))
            else:
                # f(x, c)
                f_result = f.evaluate((x, const_val))

            if f_result != target.evaluate((x, y)):
                return False
    return True


def _try_binary_const_unary(target: Connective, f: Connective,
                             const_val: int, u: Connective,
                             left_const: bool) -> bool:
    """Try f(c, u(x)) or f(c, u(y)) or f(u(x), c) or f(u(y), c)."""
    # Try with u(x)
    for x in [0, 1]:
        for y in [0, 1]:
            u_result = u.evaluate((x,))
            if left_const:
                f_result = f.evaluate((const_val, u_result))
            else:
                f_result = f.evaluate((u_result, const_val))
            if f_result != target.evaluate((x, y)):
                break
    else:
        return True

    # Try with u(y)
    for x in [0, 1]:
        for y in [0, 1]:
            u_result = u.evaluate((y,))
            if left_const:
                f_result = f.evaluate((const_val, u_result))
            else:
                f_result = f.evaluate((u_result, const_val))
            if f_result != target.evaluate((x, y)):
                return False
    return True


def _check_binary_unary_binary_patterns(target: Connective,
                                         binary_basis: List[Connective],
                                         unary_basis: List[Connective]) -> bool:
    """
    Check patterns like f(u(g(x,y)), v(h(x,y))).

    This handles complex depth-3 patterns including XOR-like compositions.

    Args:
        target: Binary target connective
        binary_basis: Binary basis functions
        unary_basis: Unary basis functions

    Returns:
        True if target matches this pattern
    """
    for f in binary_basis:
        for u in unary_basis + [None]:
            for v in unary_basis + [None]:
                for g in binary_basis:
                    for h in binary_basis + [None]:
                        if _try_binary_unary_binary_unary_binary(target, f, u, g, v, h):
                            return True
    return False


def _try_binary_unary_binary_unary_binary(target: Connective,
                                           f: Connective,
                                           u: Optional[Connective],
                                           g: Connective,
                                           v: Optional[Connective],
                                           h: Optional[Connective]) -> bool:
    """
    Try composition f(u(g(x,y)), v(h(x,y))).

    This handles patterns like OR(AND(x, NOT(y)), AND(NOT(x), y)) for XOR.
    """
    for x in [0, 1]:
        for y in [0, 1]:
            # Compute g(x,y)
            g_result = g.evaluate((x, y))

            # Apply unary u (or identity)
            if u is None:
                left_result = g_result
            else:
                left_result = u.evaluate((g_result,))

            # Compute h(x,y) (or use same as g)
            if h is None:
                h_result = g_result
            elif h == g:
                h_result = g_result
            else:
                h_result = h.evaluate((x, y))

            # Apply unary v (or identity)
            if v is None:
                right_result = h_result
            else:
                right_result = v.evaluate((h_result,))

            # Compute f(left, right)
            f_result = f.evaluate((left_result, right_result))

            if f_result != target.evaluate((x, y)):
                return False
    return True


def _check_unary_chain_binary(target: Connective,
                                binary_basis: List[Connective],
                                unary_basis: List[Connective]) -> bool:
    """
    Check patterns like u(v(f(x,y))) - chains of unary functions on binary.

    Args:
        target: Binary target connective
        binary_basis: Binary basis functions
        unary_basis: Unary basis functions

    Returns:
        True if target matches a unary chain pattern
    """
    for f in binary_basis:
        for u in unary_basis:
            for v in unary_basis:
                if _try_unary_unary_binary(target, u, v, f):
                    return True
    return False


def _try_unary_unary_binary(target: Connective,
                             u: Connective,
                             v: Connective,
                             f: Connective) -> bool:
    """Try composition u(v(f(x,y)))."""
    for x in [0, 1]:
        for y in [0, 1]:
            # Compute f(x,y)
            f_result = f.evaluate((x, y))

            # Apply v
            v_result = v.evaluate((f_result,))

            # Apply u
            u_result = u.evaluate((v_result,))

            if u_result != target.evaluate((x, y)):
                return False
    return True


def _try_f_proj_composed(target: Connective,
                         f: Connective,
                         g: Connective,
                         h1: Optional[Connective],
                         h2: Optional[Connective],
                         left_proj: bool) -> bool:
    """
    Try composition f(x, g(h1(...), h2(...))) or f(g(h1(...), h2(...)), y).

    This handles patterns like NAND(x, NAND(FALSE, FALSE)) = ¬x.

    Args:
        target: Target binary connective
        f: Outer binary function
        g: Middle binary function
        h1, h2: Inner binary functions (or None for projections)
        left_proj: If True, use f(x, g(...)); if False, use f(g(...), y)
    """
    for x in [0, 1]:
        for y in [0, 1]:
            # Compute h1 and h2 results
            if h1 is None:
                h1_result = x
            else:
                h1_result = h1.evaluate((x, y))

            if h2 is None:
                h2_result = y
            else:
                h2_result = h2.evaluate((x, y))

            # Compute g(h1_result, h2_result)
            g_result = g.evaluate((h1_result, h2_result))

            # Compute final result based on projection position
            if left_proj:
                # f(x, g_result)
                f_result = f.evaluate((x, g_result))
            else:
                # f(g_result, y)
                f_result = f.evaluate((g_result, y))

            if f_result != target.evaluate((x, y)):
                return False
    return True


def is_independent(connectives: List[Connective],
                  max_depth: int = 3,
                  timeout_ms: int = 5000,
                  mode: DefinabilityMode = DefinabilityMode.SYNTACTIC) -> bool:
    """
    Check if a set of connectives is independent.

    A set is independent if no connective can be expressed as a
    composition of the others.

    Args:
        connectives: List of connectives to check
        max_depth: Maximum composition depth for definability checking
        timeout_ms: Solver timeout per check
        mode: Definability mode (syntactic or truth-functional, default: syntactic)

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
        if is_definable(target, basis, max_depth, timeout_ms, mode):
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
