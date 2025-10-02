"""
Core connective representation using Z3 BitVec truth tables.

A connective is represented by its truth table encoded as a BitVector,
where the i-th bit represents the output for the i-th input assignment.
"""

from z3 import BitVec, BitVecVal, Extract, Concat
from typing import List, Tuple, Optional


class Connective:
    """
    Represents a logical connective by its truth table.

    Attributes:
        arity: Number of input variables (0-5)
        truth_table: BitVec representation of the truth table
        name: Optional name for the connective
    """

    def __init__(self, arity: int, truth_table: int, name: Optional[str] = None):
        """
        Initialize a connective.

        Args:
            arity: Number of input variables (0-5)
            truth_table: Integer representing the truth table
            name: Optional name for debugging/display

        Raises:
            ValueError: If arity is not in range 0-5 or truth_table is invalid
        """
        if not 0 <= arity <= 5:
            raise ValueError(f"Arity must be in range 0-5, got {arity}")

        table_size = 2 ** arity
        max_value = 2 ** table_size - 1

        if not 0 <= truth_table <= max_value:
            raise ValueError(
                f"Truth table value {truth_table} invalid for arity {arity}. "
                f"Must be in range 0-{max_value}"
            )

        self.arity = arity
        self.truth_table_int = truth_table
        self.truth_table = BitVecVal(truth_table, table_size)
        self.name = name or f"f{arity}_{truth_table}"

    def evaluate(self, inputs: Tuple[int, ...]) -> int:
        """
        Evaluate the connective on a specific input assignment.

        Args:
            inputs: Tuple of input values (0 or 1)

        Returns:
            Output value (0 or 1)

        Raises:
            ValueError: If number of inputs doesn't match arity
        """
        if len(inputs) != self.arity:
            raise ValueError(
                f"Expected {self.arity} inputs, got {len(inputs)}"
            )

        # Convert input tuple to row index
        # For inputs (x1, x2, ..., xn), index = x1*2^(n-1) + x2*2^(n-2) + ... + xn
        index = 0
        for i, val in enumerate(inputs):
            if val not in (0, 1):
                raise ValueError(f"Input values must be 0 or 1, got {val}")
            index = index * 2 + val

        # Extract the bit at position 'index'
        return (self.truth_table_int >> index) & 1

    def evaluate_all(self) -> List[Tuple[Tuple[int, ...], int]]:
        """
        Generate all input-output pairs for this connective.

        Returns:
            List of (input_tuple, output) pairs
        """
        results = []
        num_rows = 2 ** self.arity

        for row in range(num_rows):
            # Convert row index to input tuple
            inputs = tuple((row >> (self.arity - 1 - i)) & 1
                          for i in range(self.arity))
            output = self.evaluate(inputs)
            results.append((inputs, output))

        return results

    def __eq__(self, other) -> bool:
        """
        Check if two connectives are equal.

        Args:
            other: Another Connective instance

        Returns:
            True if connectives have same arity and truth table
        """
        if not isinstance(other, Connective):
            return False
        return (self.arity == other.arity and
                self.truth_table_int == other.truth_table_int)

    def __hash__(self) -> int:
        """Hash based on arity and truth table for use in sets/dicts."""
        return hash((self.arity, self.truth_table_int))

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"Connective(arity={self.arity}, name='{self.name}')"

    def __str__(self) -> str:
        """
        Human-readable truth table representation.

        Returns:
            Formatted truth table string
        """
        if self.arity == 0:
            # Constants: no inputs
            output = self.truth_table_int
            return f"{self.name}: {output}"

        lines = [f"{self.name} (arity {self.arity}):"]
        lines.append("-" * (self.arity * 4 + 6))

        # Header
        header_parts = [f"x{i}" for i in range(self.arity)]
        header_parts.append("out")
        lines.append(" | ".join(header_parts))
        lines.append("-" * (self.arity * 4 + 6))

        # Rows
        for inputs, output in self.evaluate_all():
            row_parts = [str(val) for val in inputs]
            row_parts.append(str(output))
            lines.append("  | ".join(row_parts))

        return "\n".join(lines)


def generate_all_connectives(arity: int) -> List[Connective]:
    """
    Generate all possible connectives of a given arity.

    Args:
        arity: Number of input variables (0-5)

    Returns:
        List of all possible connectives for the given arity

    Raises:
        ValueError: If arity is not in range 0-5
    """
    if not 0 <= arity <= 5:
        raise ValueError(f"Arity must be in range 0-5, got {arity}")

    table_size = 2 ** arity
    num_connectives = 2 ** table_size

    return [Connective(arity, i) for i in range(num_connectives)]


def get_connective_count(arity: int) -> int:
    """
    Calculate the number of possible connectives for a given arity.

    Args:
        arity: Number of input variables

    Returns:
        Number of possible connectives (2^(2^arity))
    """
    return 2 ** (2 ** arity)
