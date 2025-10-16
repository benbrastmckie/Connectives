"""
Shared pytest fixtures for nice-connectives test suite.

This module provides common fixtures used across multiple test files:
- Sample connective pools for testing
- Temporary file fixtures for checkpoint testing
- Mock Z3 solver for unit testing

Fixture Scoping Strategy:
- session scope: Immutable test data (connective pools, constants)
  Generated once per test session and reused across all tests.
  Safe because data is read-only and never modified.

- function scope (default): Mutable fixtures, temporary files, mocks
  Created fresh for each test to ensure test isolation.
  Required for fixtures that track state or modify data.
"""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import Mock, MagicMock

from src.connectives import generate_all_connectives
from src.constants import ALL_BINARY, AND, OR, NOT, CONST_FALSE


@pytest.fixture(scope="session")
def sample_connective_pool():
    """
    Provide a small connective pool for testing.

    Returns a pool with:
    - 2 constants (arity 0)
    - 4 unary connectives (arity 1)
    - 16 binary connectives (arity 2)
    Total: 22 connectives

    This is suitable for fast unit tests without the overhead
    of including all 256 ternary connectives.

    Note: Uses session scope - generated once per test session and reused
    across all tests. Safe because the pool is immutable (read-only).
    """
    pool = []
    pool.extend(generate_all_connectives(0))  # 2 constants
    pool.extend(generate_all_connectives(1))  # 4 unary
    pool.extend(ALL_BINARY)                   # 16 binary
    return pool


@pytest.fixture(scope="session")
def minimal_complete_set():
    """
    Provide a minimal complete connective set for testing.

    Returns {NOT, AND} which is known to be complete.

    Note: Uses session scope - created once and reused across all tests.
    Safe because the connective set is immutable (read-only).
    """
    return [NOT, AND]


@pytest.fixture(scope="session")
def standard_complete_set():
    """
    Provide a standard complete connective set for testing.

    Returns {NOT, AND, OR} which is a common complete set.

    Note: Uses session scope - created once and reused across all tests.
    Safe because the connective set is immutable (read-only).
    """
    return [NOT, AND, OR]


@pytest.fixture(scope="session")
def tiny_connective_pool():
    """
    Provide a tiny connective pool for ultra-fast unit tests.

    Returns a minimal pool with:
    - 2 constants (arity 0)
    - 4 unary connectives (arity 1)
    - 2 binary connectives (AND, OR)
    Total: 8 connectives

    This is optimized for tests that just need "some connectives" without
    requiring the full 16 binary connectives. Use this when test speed
    is critical and coverage doesn't require all connectives.

    Note: Uses session scope - generated once and reused across all tests.
    """
    pool = []
    pool.extend(generate_all_connectives(0))  # 2 constants
    pool.extend(generate_all_connectives(1))  # 4 unary
    pool.extend([AND, OR])                     # 2 common binary
    return pool


@pytest.fixture
def temp_checkpoint_file(tmp_path):
    """
    Provide a temporary checkpoint file path.

    Args:
        tmp_path: pytest's built-in temporary directory fixture

    Returns:
        Path object for a temporary checkpoint file

    The file is automatically cleaned up after the test.
    """
    checkpoint_path = tmp_path / "test_checkpoint.json"
    return checkpoint_path


@pytest.fixture
def temp_output_dir(tmp_path):
    """
    Provide a temporary output directory for test files.

    Args:
        tmp_path: pytest's built-in temporary directory fixture

    Returns:
        Path object for a temporary output directory

    The directory and all contents are automatically cleaned up after the test.
    """
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    return output_dir


@pytest.fixture
def mock_z3_solver():
    """
    Provide a mocked Z3 Solver for unit testing.

    Returns a Mock object with common Z3 Solver methods:
    - add(): Records constraints
    - check(): Returns mock result (sat, unsat, or unknown)
    - model(): Returns mock model
    - push(): Records solver state push
    - pop(): Records solver state pop

    This allows testing Z3-based logic without actually invoking Z3,
    making tests fast and deterministic.

    Example usage:
        def test_something(mock_z3_solver):
            mock_z3_solver.check.return_value = sat
            # Test code using the mock solver
            assert mock_z3_solver.add.called
    """
    solver = MagicMock()

    # Set up default mock behaviors
    solver.add = Mock()
    solver.check = Mock(return_value=Mock())  # Can be configured per test
    solver.model = Mock(return_value=Mock())
    solver.push = Mock()
    solver.pop = Mock()

    # Track constraint additions
    solver.constraints = []

    def add_constraint(constraint):
        solver.constraints.append(constraint)

    solver.add.side_effect = add_constraint

    return solver


@pytest.fixture
def mock_z3_bool():
    """
    Provide a factory for creating mock Z3 Bool variables.

    Returns a function that creates mock Bool variables.
    Each mock Bool has a name and can be used in Z3 expressions.

    Example usage:
        def test_something(mock_z3_bool):
            var = mock_z3_bool('x')
            assert var.name == 'x'
    """
    def create_bool(name):
        mock_var = Mock()
        mock_var.name = name
        mock_var.__repr__ = lambda self: f"Bool('{name}')"
        return mock_var

    return create_bool

