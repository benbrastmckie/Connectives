"""
Post's Lattice implementation for completeness checking.

According to Post's Completeness Theorem, a set of connectives is complete
if and only if it escapes all five maximal clones:
- T0: 0-preserving functions
- T1: 1-preserving functions
- M: Monotone functions
- D: Self-dual functions
- A: Affine (linear) functions

A set is complete iff for each clone, at least one function in the set
does NOT belong to that clone.
"""

from typing import List, Set, Tuple
from src.connectives import Connective


def is_t0_preserving(connective: Connective) -> bool:
    """
    Check if a connective is 0-preserving (belongs to T0).

    A function is 0-preserving if f(0, 0, ..., 0) = 0.

    Args:
        connective: Connective to check

    Returns:
        True if connective is 0-preserving
    """
    # All-zeros input
    zeros = tuple(0 for _ in range(connective.arity))
    return connective.evaluate(zeros) == 0


def is_t1_preserving(connective: Connective) -> bool:
    """
    Check if a connective is 1-preserving (belongs to T1).

    A function is 1-preserving if f(1, 1, ..., 1) = 1.

    Args:
        connective: Connective to check

    Returns:
        True if connective is 1-preserving
    """
    # All-ones input
    ones = tuple(1 for _ in range(connective.arity))
    return connective.evaluate(ones) == 1


def is_monotone(connective: Connective) -> bool:
    """
    Check if a connective is monotone (belongs to M).

    A function is monotone if for all inputs x, y where x ≤ y componentwise,
    we have f(x) ≤ f(y).

    Args:
        connective: Connective to check

    Returns:
        True if connective is monotone
    """
    # Generate all input pairs
    num_rows = 2 ** connective.arity

    for i in range(num_rows):
        for j in range(num_rows):
            # Convert indices to input tuples
            input_i = tuple((i >> (connective.arity - 1 - k)) & 1
                          for k in range(connective.arity))
            input_j = tuple((j >> (connective.arity - 1 - k)) & 1
                          for k in range(connective.arity))

            # Check if input_i ≤ input_j componentwise
            if all(input_i[k] <= input_j[k] for k in range(connective.arity)):
                # Then f(input_i) must be ≤ f(input_j)
                if connective.evaluate(input_i) > connective.evaluate(input_j):
                    return False

    return True


def is_self_dual(connective: Connective) -> bool:
    """
    Check if a connective is self-dual (belongs to D).

    A function is self-dual if ¬f(x1, ..., xn) = f(¬x1, ..., ¬xn) for all inputs.

    Args:
        connective: Connective to check

    Returns:
        True if connective is self-dual
    """
    num_rows = 2 ** connective.arity

    for row in range(num_rows):
        # Convert row to input tuple
        inputs = tuple((row >> (connective.arity - 1 - k)) & 1
                      for k in range(connective.arity))

        # Compute f(inputs)
        f_inputs = connective.evaluate(inputs)

        # Compute negated inputs
        neg_inputs = tuple(1 - val for val in inputs)

        # Compute f(¬inputs)
        f_neg_inputs = connective.evaluate(neg_inputs)

        # Check if ¬f(inputs) == f(¬inputs)
        # i.e., f_neg_inputs == 1 - f_inputs
        if f_neg_inputs != (1 - f_inputs):
            return False

    return True


def is_affine(connective: Connective) -> bool:
    """
    Check if a connective is affine/linear (belongs to A).

    A function is affine if it can be expressed as a XOR of a subset of
    variables plus an optional constant. This is equivalent to having
    the property that f(x ⊕ y ⊕ z) = f(x) ⊕ f(y) ⊕ f(z) ⊕ f(0...0).

    Alternatively, a function is affine iff its truth table has an
    even number of 1s after XORing any three distinct rows that
    XOR to the zero row.

    For practical checking, we use the fact that a Boolean function is
    affine iff it can be written as c0 ⊕ c1*x1 ⊕ c2*x2 ⊕ ... ⊕ cn*xn
    where ci ∈ {0,1}.

    Args:
        connective: Connective to check

    Returns:
        True if connective is affine
    """
    # For small arities, we can check directly by trying to find
    # a linear representation using Gaussian elimination.
    # A function is affine iff it satisfies:
    # f(x ⊕ y) ⊕ f(x) ⊕ f(y) ⊕ f(0) = 0 for all x, y

    num_rows = 2 ** connective.arity

    # Get f(0...0)
    zeros = tuple(0 for _ in range(connective.arity))
    f_zeros = connective.evaluate(zeros)

    # Check affine property for all pairs of inputs
    for i in range(num_rows):
        for j in range(num_rows):
            # Convert indices to input tuples
            input_i = tuple((i >> (connective.arity - 1 - k)) & 1
                          for k in range(connective.arity))
            input_j = tuple((j >> (connective.arity - 1 - k)) & 1
                          for k in range(connective.arity))

            # Compute i ⊕ j (XOR componentwise)
            input_xor = tuple(input_i[k] ^ input_j[k]
                            for k in range(connective.arity))

            # Get function values
            f_i = connective.evaluate(input_i)
            f_j = connective.evaluate(input_j)
            f_xor = connective.evaluate(input_xor)

            # Check affine property: f(x ⊕ y) = f(x) ⊕ f(y) ⊕ f(0)
            if f_xor != (f_i ^ f_j ^ f_zeros):
                return False

    return True


def get_post_class_membership(connective: Connective) -> Set[str]:
    """
    Determine which Post classes a connective belongs to.

    Args:
        connective: Connective to classify

    Returns:
        Set of class names ('T0', 'T1', 'M', 'D', 'A')
    """
    classes = set()

    if is_t0_preserving(connective):
        classes.add('T0')
    if is_t1_preserving(connective):
        classes.add('T1')
    if is_monotone(connective):
        classes.add('M')
    if is_self_dual(connective):
        classes.add('D')
    if is_affine(connective):
        classes.add('A')

    return classes


def is_complete(connectives: List[Connective]) -> bool:
    """
    Check if a set of connectives is complete using Post's theorem.

    A set is complete if it escapes all five maximal clones:
    for each clone, at least one connective is not in that clone.

    Args:
        connectives: List of connectives to check

    Returns:
        True if the set is complete
    """
    if not connectives:
        return False

    # Check if we escape each maximal clone
    escapes_t0 = any(not is_t0_preserving(c) for c in connectives)
    escapes_t1 = any(not is_t1_preserving(c) for c in connectives)
    escapes_m = any(not is_monotone(c) for c in connectives)
    escapes_d = any(not is_self_dual(c) for c in connectives)
    escapes_a = any(not is_affine(c) for c in connectives)

    return (escapes_t0 and escapes_t1 and escapes_m and
            escapes_d and escapes_a)


def get_missing_classes(connectives: List[Connective]) -> Set[str]:
    """
    Determine which Post classes are NOT escaped by the connective set.

    Args:
        connectives: List of connectives to check

    Returns:
        Set of class names that are not escaped (i.e., all connectives
        in the set belong to these classes)
    """
    if not connectives:
        return {'T0', 'T1', 'M', 'D', 'A'}

    missing = set()

    if all(is_t0_preserving(c) for c in connectives):
        missing.add('T0')
    if all(is_t1_preserving(c) for c in connectives):
        missing.add('T1')
    if all(is_monotone(c) for c in connectives):
        missing.add('M')
    if all(is_self_dual(c) for c in connectives):
        missing.add('D')
    if all(is_affine(c) for c in connectives):
        missing.add('A')

    return missing


def equivalence_class_representative(connective: Connective) -> int:
    """
    Get a canonical representative for the equivalence class of a connective.

    Two connectives are equivalent if one can be obtained from the other by:
    - Permuting variables
    - Negating variables
    - Negating the output

    This function returns a canonical form (smallest truth table value)
    among all equivalent connectives.

    Args:
        connective: Connective to canonicalize

    Returns:
        Truth table value of canonical representative
    """
    # For now, just return the connective itself
    # Full symmetry breaking would require checking all permutations/negations
    # This is a placeholder for potential optimization in Phase 7
    return connective.truth_table_int


def filter_by_post_classes(connectives: List[Connective],
                           must_escape: Set[str]) -> List[Connective]:
    """
    Filter connectives to only those that escape specified Post classes.

    Args:
        connectives: List of connectives to filter
        must_escape: Set of class names that must be escaped

    Returns:
        Filtered list of connectives
    """
    filtered = []

    for c in connectives:
        classes = get_post_class_membership(c)

        # Check if this connective escapes all required classes
        escapes_all = True
        for class_name in must_escape:
            if class_name in classes:
                # Connective is in this class, so doesn't escape it
                escapes_all = False
                break

        if escapes_all:
            filtered.append(c)

    return filtered
